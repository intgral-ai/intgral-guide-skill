import importlib.util
import json
import subprocess
import tempfile
import unittest
import shutil
from pathlib import Path

spec = importlib.util.spec_from_file_location('publication_guard', Path(__file__).resolve().parents[1] / 'scripts/validate.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class PublicationGuardTests(unittest.TestCase):
    def test_workflow_package_resolves_both_apps_and_entrypoints(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(guard.check_workflow_plugin(root), [])

    def test_workflow_package_rejects_missing_or_optional_dependency(self):
        source = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(source / '.codex-plugin', root / '.codex-plugin')
            shutil.copytree(source / 'skills', root / 'skills')
            self.assertEqual(guard.check_workflow_plugin(root),
                             ['workflow plugin: missing or invalid manifest, app dependency or skill'])
            dependency = {'apps': {'app-6a5ae9736be0819199d06d61ac171080': {
                'id': 'asdk_app_6a5ae9736be0819199d06d61ac171080', 'required': False},
                'slack': {'id': 'asdk_app_69a1d78e929881919bba0dbda1f6436d', 'required': True}}}
            (root / '.app.json').write_text(json.dumps(dependency))
            self.assertEqual(guard.check_workflow_plugin(root),
                             ['workflow plugin: Wispr Flow and Slack must be required apps'])

    def test_detects_token_without_echoing_it(self):
        token = 'ghp_' + 'a' * 36
        findings = guard.sensitive_findings('token=' + token, 'sample')
        self.assertTrue(findings)
        self.assertNotIn(token, '\n'.join(findings))

    def test_workflow_skill_errors_identify_the_affected_entrypoint(self):
        source = Path(__file__).resolve().parents[1]
        for name in ('intgral-knowledge-workflow', 'intgral-meeting', 'intgral-meeting-prepare'):
            for case in ('missing', 'frontmatter', 'identity'):
                with self.subTest(name=name, case=case), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    shutil.copytree(source / '.codex-plugin', root / '.codex-plugin')
                    shutil.copytree(source / 'skills', root / 'skills')
                    shutil.copyfile(source / '.app.json', root / '.app.json')
                    skill = root / 'skills' / name / 'SKILL.md'
                    if case == 'missing':
                        skill.unlink()
                    elif case == 'frontmatter':
                        skill.write_text('# A skill without frontmatter\n')
                    else:
                        skill.write_text('---\nname: wrong-entry\ndescription: A test skill\n---\n')
                    errors = guard.check_workflow_plugin(root)
                    self.assertEqual(len(errors), 1)
                    self.assertIn(skill.relative_to(root).as_posix(), errors[0])
                    self.assertIn({'missing': 'missing workflow skill file',
                                   'frontmatter': 'missing frontmatter',
                                   'identity': 'invalid name or description'}[case], errors[0])

    def test_personal_path_and_email_are_rejected(self):
        path = '/' + 'Users' + '/example/private-file'
        email = 'person' + '@' + 'example.invalid'
        self.assertEqual(len(guard.sensitive_findings(path + '\n' + email, 'sample')), 2)

    def test_private_platform_links_are_rejected(self):
        urls = [
            'https://docs.intgral.ai/' + 'doc/' + 'synthetic-page',
            'https://www.figma.com/' + 'design/' + 'synthetic-file',
            'https://drive.google.com/' + 'file/d/' + 'synthetic-file',
            'https://app.slack.com/' + 'client/' + 'synthetic-workspace',
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(guard.sensitive_findings(url, 'sample'))

    def test_public_documentation_home_is_allowed(self):
        self.assertEqual(guard.sensitive_findings('https://docs.intgral.ai', 'sample'), [])

    def test_private_configuration_cannot_join_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'team-context.json').write_text('{}')
            self.assertTrue(any('outside the publication allowlist' in e for e in guard.validate(root)))

    def test_example_cannot_publish_populated_local_indexes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'assets').mkdir()
            source = Path(__file__).resolve().parents[1] / 'assets/team-context.example.json'
            example = json.loads(source.read_text())
            example.setdefault('local_indexes', {})['documentation'] = 'workspace/' + 'private-doc-index.json'
            (root / 'assets/team-context.example.json').write_text(json.dumps(example))
            errors = guard.validate(root)
            self.assertTrue(any('must contain no real team assignments or internal sources' in e for e in errors))

    def test_example_rejects_missing_or_malformed_local_indexes(self):
        source = Path(__file__).resolve().parents[1] / 'assets/team-context.example.json'
        for case in ('missing', None, [], 'not-an-index-map', False):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / 'assets').mkdir()
                example = json.loads(source.read_text())
                if case == 'missing':
                    example.pop('local_indexes')
                else:
                    example['local_indexes'] = case
                (root / 'assets/team-context.example.json').write_text(json.dumps(example))
                errors = guard.validate(root)
                self.assertTrue(any('must contain no real team assignments or internal sources' in e for e in errors))

    def test_symlink_cannot_import_external_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').symlink_to(root.parent / 'external-private-data')
            self.assertTrue(any('symlink' in e for e in guard.validate(root)))

    def test_local_links_cannot_escape_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / 'README.md'
            document.write_text('[outside](../outside.md)')
            self.assertTrue(guard.check_links(root, [document]))

    def test_removed_credential_is_still_detected_in_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True)
            git('init', '-b', 'main')
            git('config', 'user.name', 'Example Contributor')
            git('config', 'user.email', 'example' + '@' + 'users.noreply.github.com')
            document = root / 'README.md'
            document.write_text('ghp_' + 'b' * 36)
            git('add', 'README.md')
            git('commit', '-m', 'Synthetic unsafe version')
            document.write_text('Public guidance only.')
            git('add', 'README.md')
            git('commit', '-m', 'Synthetic clean tip')
            self.assertEqual(guard.sensitive_findings(document.read_text(), 'current'), [])
            self.assertTrue(guard.scan_history(root))


if __name__ == '__main__':
    unittest.main()
