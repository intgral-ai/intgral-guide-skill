import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/intgral-knowledge-workflow/scripts/ledger.py'
spec = importlib.util.spec_from_file_location('workflow_ledger', SCRIPT)
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)


class WorkflowLedgerTests(unittest.TestCase):
    def setUp(self):
        self.state = ledger.empty_state()
        self.issue = {'key': 'topic-1:scope', 'question': 'Which scope is accepted?',
                      'audience': 'founders', 'source_revision': 'source-v1'}

    def test_repeat_cycle_keeps_same_issue_without_reopening(self):
        first = copy.deepcopy(ledger.register(self.state, self.issue))
        response = {'id': first['id'], 'revision': 1, 'actor': 'owner',
                    'authorized_actors': ['owner'], 'action': 'approve', 'evidence': 'reply-1'}
        ledger.resolve(self.state, response)
        repeated = ledger.register(self.state, self.issue)
        self.assertEqual(repeated['id'], first['id'])
        self.assertEqual(repeated['revision'], 1)
        self.assertEqual(repeated['status'], 'approved')
        self.assertEqual(len(self.state['issues']), 1)

    def test_source_change_reopens_and_rejects_old_approval(self):
        first = ledger.register(self.state, self.issue)
        ledger.resolve(self.state, {'id': first['id'], 'revision': 1, 'actor': 'owner',
                                   'authorized_actors': ['owner'], 'action': 'approve', 'evidence': 'reply-1'})
        changed = ledger.register(self.state, {**self.issue, 'source_revision': 'source-v2'})
        self.assertEqual(changed['revision'], 2)
        self.assertEqual(changed['status'], 'pending')
        self.assertEqual(changed['history'][0]['status'], 'approved')
        with self.assertRaises(ValueError):
            ledger.resolve(self.state, {'id': changed['id'], 'revision': 1, 'actor': 'owner',
                                       'authorized_actors': ['owner'], 'action': 'approve', 'evidence': 'reply-1'})

    def test_audience_cannot_be_widened_by_registering_again(self):
        ledger.register(self.state, self.issue)
        before = copy.deepcopy(self.state)
        with self.assertRaises(ValueError):
            ledger.register(self.state, {**self.issue, 'audience': 'team'})
        self.assertEqual(self.state, before)

    def test_unauthorized_actor_or_ambiguous_reply_does_not_resolve(self):
        issue = ledger.register(self.state, self.issue)
        reply = {'id': issue['id'], 'revision': 1, 'actor': 'other',
                 'authorized_actors': ['owner'], 'action': 'approve', 'evidence': 'reply-2'}
        with self.assertRaises(ValueError):
            ledger.resolve(self.state, reply)
        with self.assertRaises(ValueError):
            ledger.resolve(self.state, {**reply, 'actor': 'owner', 'action': 'looks-good'})
        self.assertEqual(issue['status'], 'pending')

    def test_unverified_write_requires_reconciliation_before_retry_or_replacement(self):
        payload = {'target': 'decision:issue-1', 'revision': 1, 'hash': 'first'}
        self.assertEqual(ledger.prepare(self.state, payload)['action'], 'write')
        self.assertEqual(ledger.prepare(self.state, payload)['action'], 'reconcile')
        self.assertEqual(ledger.prepare(self.state, {**payload, 'revision': 2, 'hash': 'second'})['action'], 'reconcile')
        self.assertEqual(self.state['deliveries'][payload['target']]['hash'], 'first')

    def test_readback_is_per_destination_and_repeat_is_skipped(self):
        payload = {'target': 'docs:topic-1', 'revision': 1, 'hash': 'first'}
        ledger.prepare(self.state, payload)
        with self.assertRaises(ValueError):
            ledger.verify(self.state, {**payload, 'hash': 'wrong', 'observed': True, 'url': 'remote-doc'})
        ledger.verify(self.state, {**payload, 'observed': True, 'url': 'remote-doc'})
        self.assertEqual(ledger.prepare(self.state, payload)['action'], 'skip')
        self.assertEqual(ledger.prepare(self.state, {**payload, 'target': 'slack:update-1'})['action'], 'write')

    def test_atomic_file_restart_preserves_pending_and_refuses_foreign_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'state.json'
            first = ledger.update_file(path, 'register', self.issue)
            second = ledger.update_file(path, 'register', self.issue)
            self.assertEqual(first, second)
            old_state = {'schema_version': 2, 'legacy_checkpoint': 'keep'}
            path.write_text(json.dumps(old_state))
            with self.assertRaises(ValueError):
                ledger.update_file(path, 'register', self.issue)
            self.assertEqual(json.loads(path.read_text()), old_state)
            self.assertFalse(path.with_name('state.json.lock').exists())


if __name__ == '__main__':
    unittest.main()
