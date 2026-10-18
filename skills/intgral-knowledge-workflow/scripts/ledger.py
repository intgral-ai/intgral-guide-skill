"""Private local decision and delivery ledger; no remote writes or authority inference."""

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def empty_state():
    return {'schema_version': 1, 'issues': {}, 'deliveries': {}}


def required_text(data, key):
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{key} must be non-empty text')
    return value


def positive_revision(data):
    value = data['revision']
    if type(value) is not int or value < 1:
        raise ValueError('revision must be a positive integer')
    return value


def register(state, data):
    key = required_text(data, 'key')
    audience = required_text(data, 'audience')
    if audience not in {'personal', 'founders', 'team'}:
        raise ValueError('Unknown audience: keep the source private until classified')
    content = {k: required_text(data, k) for k in ('question', 'source_revision', 'audience')}
    issue_id = digest(key)[:24]
    previous = state['issues'].get(issue_id)
    if previous and previous['audience'] != audience:
        raise ValueError('Audience change requires a separate explicitly approved release')
    if previous and previous['content_hash'] == digest(content):
        return previous
    history = [] if not previous else previous['history'] + [{
        k: v for k, v in previous.items() if k != 'history'}]
    issue = {'id': issue_id, 'key': key, **content, 'content_hash': digest(content),
             'revision': 1 if not previous else previous['revision'] + 1,
             'status': 'pending', 'answer': None, 'history': history}
    state['issues'][issue_id] = issue
    return issue


def resolve(state, data):
    issue = state['issues'][required_text(data, 'id')]
    if positive_revision(data) != issue['revision']:
        raise ValueError('Stale answer: source or question revision changed')
    actor = required_text(data, 'actor')
    authorities = data['authorized_actors']
    if not isinstance(authorities, list) or actor not in authorities:
        raise ValueError('Answer requires a caller-verified authorized actor')
    action = data['action']
    if action not in {'approve', 'reject', 'defer'}:
        raise ValueError('Expected explicit approve, reject or defer')
    evidence = required_text(data, 'evidence')
    if issue['status'] != 'pending':
        raise ValueError('Preserve a settled answer; reopen through a new revision')
    answer = {'actor': actor, 'action': action, 'evidence': evidence}
    if issue['answer']:
        issue['history'].append({'revision': issue['revision'], 'answer': issue['answer']})
    issue['answer'] = answer
    issue['status'] = {'approve': 'approved', 'reject': 'rejected', 'defer': 'pending'}[action]
    return issue


def prepare(state, data):
    target = required_text(data, 'target')
    revision = positive_revision(data)
    content_hash = required_text(data, 'hash')
    previous = state['deliveries'].get(target)
    if previous and previous['status'] != 'verified':
        return {'action': 'reconcile', 'delivery': previous}
    if previous and previous['revision'] == revision and previous['hash'] == content_hash:
        return {'action': 'skip', 'delivery': previous}
    if previous and revision <= previous['revision']:
        raise ValueError('A changed payload needs a newer revision')
    delivery = {'target': target, 'revision': revision, 'hash': content_hash,
                'status': 'pending', 'url': None}
    state['deliveries'][target] = delivery
    return {'action': 'write', 'delivery': delivery}


def verify(state, data):
    target = required_text(data, 'target')
    delivery = state['deliveries'][target]
    if (positive_revision(data) != delivery['revision']
            or required_text(data, 'hash') != delivery['hash'] or data.get('observed') is not True):
        raise ValueError('Actual readback must match the pending revision and hash')
    url = required_text(data, 'url')
    delivery.update(status='verified', url=url)
    return delivery


def update_file(path, command, data):
    skill_root = Path(__file__).resolve().parents[1]
    package_root = next((p for p in (skill_root, *skill_root.parents)
                         if (p / '.git').exists()), skill_root)
    path = path.resolve()
    if path.is_relative_to(package_root):
        raise ValueError('Keep ledger files outside the public package/repository')
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock = path.with_name(path.name + '.lock')
    lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(lock_fd)
    temporary = None
    try:
        state = json.loads(path.read_text()) if path.exists() else empty_state()
        if (not isinstance(state, dict) or state.get('schema_version') != 1 or not isinstance(state.get('issues'), dict)
                or not isinstance(state.get('deliveries'), dict)):
            raise ValueError('Unrecognized ledger: preserve it and migrate explicitly')
        result = state if command == 'show' else {
            'register': register, 'resolve': resolve, 'prepare': prepare, 'verify': verify,
        }[command](state, data)
        if command != 'show':
            fd, temporary = tempfile.mkstemp(prefix=path.name + '.', dir=path.parent)
            with os.fdopen(fd, 'w') as output:
                json.dump(state, output, ensure_ascii=False, indent=2)
                output.write('\n')
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, path)
            temporary = None
        return result
    finally:
        if temporary:
            Path(temporary).unlink(missing_ok=True)
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', required=True, type=Path)
    parser.add_argument('command', choices=['register', 'resolve', 'prepare', 'verify', 'show'])
    args = parser.parse_args()
    try:
        data = {} if args.command == 'show' else json.load(sys.stdin)
        result = update_file(args.state, args.command, data)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({'error': str(error)}), file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
