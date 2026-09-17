#!/usr/bin/env python3
"""Small synthetic receipt/archive tests; never run Lean or copy the dependency tree."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import package


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'companion'
        self.root.mkdir()
        self.tex = b'Synthetic manuscript for packaging tests.\n'
        self.pdf = b'%PDF-1.4 synthetic test payload\n'
        self.tex_sha = package.digest(self.tex)
        self.pdf_sha = package.digest(self.pdf)
        self.blob = hashlib.sha1(b'blob '+str(len(self.tex)).encode()+b'\0'+self.tex).hexdigest()
        self.pins = patch.multiple(package, SOURCE_SHA256=self.tex_sha,
                                   PDF_SHA256=self.pdf_sha, SOURCE_BLOB=self.blob)
        self.pins.start()
        self.addCleanup(self.pins.stop)
        for name in package.FIXED_FILES:
            self.put(name, b'fixture\n')
        self.put('reference/manuscript/main.tex', self.tex)
        self.put('reference/manuscript/paper.pdf', self.pdf)
        self.put('CyclicBell/Fixture.lean', b'namespace CyclicBell\nend CyclicBell\n')
        self.put('CyclicBell/AxiomAudit.lean', b'import CyclicBell.Fixture\n')
        self.put('validation/AcceptFixture.lean', b'example : True := by trivial\n')
        self.put('validation/RejectFixture.lean', b'example : False := by\n  trivial\n')
        self.put('scripts/check.py', b"runner.run(['lake','env','lean','validation/AcceptFixture.lean'])\n"
                 b"runner.run(['lake','env','lean','validation/RejectFixture.lean'],expect_failure=True)\n")
        self.names = [f'CyclicBell.fixture_{i}' for i in range(package.AXIOM_COUNT)]
        self.axioms = {n: ['propext', 'Classical.choice', 'Quot.sound'] for n in self.names}
        self.write_json('reference/expected_theorems.json', self.names)
        self.write_json('reference/source_inventory.json', {
            'declarations': [{'name': n} for n in self.names],
            'files': {n: {'sha256': package.digest((self.root/n).read_bytes())}
                      for n in ('CyclicBell.lean', 'CyclicBell/Fixture.lean')}})
        self.write_json('reference/manuscript.json', {'source_git_blob_sha1': self.blob,
            'files': {'reference/manuscript/main.tex': self.tex_sha,
                      'reference/manuscript/paper.pdf': self.pdf_sha}})
        self.lock = {'packages': [{'name': 'fixture', 'rev': 'a'*40,
                                 'url': 'https://example.invalid/fixture'}]}
        self.write_json('lake-manifest.json', self.lock)
        self.receipt = {'status': 'passed', 'kernel_checked': True,
            'compiler_commit': package.COMPILER, 'lean_version': 'Lean (version 4.19.0)',
            'clean_project_build_directory': '.lake/build',
            'axiom_report_source': 'fresh clean lake build of CyclicBell.AxiomAudit',
            'standalone_axiom_repeat': False, 'axioms': self.axioms, 'commands': [],
            'manuscript': {'path': 'reference/manuscript/main.tex', 'git_blob_sha1': self.blob,
                           'sha256': self.tex_sha, 'bytes': len(self.tex)}}
        sequence_receipt = dict(self.receipt, _check_source=(self.root/'scripts/check.py').read_text())
        controls = package.validation_registry(self.root)
        sequence = package.expected_commands(sequence_receipt, self.lock, controls)
        for i, (command, cwd, fail) in enumerate(sequence, 1):
            log = ''
            if command == ['lean', '--version']:
                log = self.receipt['lean_version']
            elif command[-1] == '--githash':
                log = package.COMPILER
            elif command == ['git', 'rev-parse', 'HEAD']:
                log = 'a'*40
            elif command == ['lake', 'build']:
                log = ''.join(f"'{n}' depends on axioms: [propext, Classical.choice, Quot.sound]\n" for n in self.names)
            elif fail:
                log = 'validation/RejectFixture.lean:2:2: error: tactic failed\n'
            name = f'{i:03d}.log'
            self.put('verification/recorded/'+name, log.encode())
            self.receipt['commands'].append({'command': command, 'cwd': cwd, 'expected_failure': fail,
                'exit_code': 1 if fail else 0, 'log': name, 'log_sha256': package.digest(log.encode())})
        self.refresh_receipt()

    def put(self, name, data):
        path = self.root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def write_json(self, name, value):
        self.put(name, (json.dumps(value, sort_keys=True)+'\n').encode())

    def refresh_receipt(self):
        self.receipt['protected_source_hashes'] = package.protected_fingerprints(self.root)
        self.save_receipt()

    def save_receipt(self):
        self.write_json('verification/recorded/run.json', self.receipt)

    def test_valid_deterministic_zip_and_manifest(self):
        self.put('verification/runs/transient/private.log', b'not shared')
        self.put('repair_history/private.txt', b'not shared')
        payload = package.collect_payload(self.root)
        out = Path(self.temp.name)/'one.zip'
        first = package.write_archive(payload, out)
        data = out.read_bytes()
        self.assertEqual(first, package.write_archive(payload, out))
        self.assertEqual(data, out.read_bytes())
        self.assertEqual(out.with_name('one.zip.sha256').read_text(), first+'  one.zip\n')
        with zipfile.ZipFile(out) as z:
            self.assertEqual(z.namelist(), sorted(z.namelist()))
            self.assertTrue(all(i.date_time == (1980,1,1,0,0,0) for i in z.infolist()))
            self.assertEqual(len(z.namelist()), len(payload)+1)
            manifest = z.read('lean_formalization/SHA256SUMS').decode().splitlines()
            self.assertEqual(len(manifest), len(payload))
            for line in manifest:
                sha, name = line.split('  ', 1)
                self.assertEqual(package.digest(z.read('lean_formalization/'+name)), sha)
            self.assertFalse(any('transient' in n or 'repair_history' in n for n in z.namelist()))

    def test_missing_required_file(self):
        (self.root/'REVIEWER_GUIDE.md').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing required'):
            package.collect_payload(self.root)

    def test_missing_log(self):
        (self.root/'verification/recorded/001.log').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing required'):
            package.collect_payload(self.root)

    def test_corrupted_log(self):
        self.put('verification/recorded/001.log', b'corrupt')
        with self.assertRaisesRegex(ValueError, 'Corrupt command log'):
            package.collect_payload(self.root)

    def test_stale_receipt(self):
        self.put('CyclicBell/Fixture.lean', b'changed\n')
        with self.assertRaisesRegex(ValueError, 'Stale recorded'):
            package.collect_payload(self.root)

    def test_stale_inventory_even_with_refreshed_receipt(self):
        self.put('CyclicBell/Fixture.lean', b'changed\n')
        self.refresh_receipt()
        with self.assertRaisesRegex(ValueError, 'Stale source inventory'):
            package.collect_payload(self.root)

    def test_symlink_file(self):
        path = self.root/'README.md'
        path.unlink()
        path.symlink_to('COVERAGE.md')
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            package.collect_payload(self.root)

    def test_symlink_directory(self):
        (self.root/'CyclicBell').rename(self.root/'moved')
        (self.root/'CyclicBell').symlink_to('moved', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            package.collect_payload(self.root)

    def test_private_machine_text(self):
        self.put('verification/README.md', ('machine: /'+'Users'+'/private/work\n').encode())
        with self.assertRaisesRegex(ValueError, 'Private machine'):
            package.collect_payload(self.root)

    def test_extra_protected_file(self):
        self.put('scripts/experiment.py', b'print(1)\n')
        self.refresh_receipt()
        with self.assertRaisesRegex(ValueError, 'outside the share allowlist'):
            package.collect_payload(self.root)

    def test_missing_command(self):
        self.receipt['commands'].pop()
        self.save_receipt()
        with self.assertRaisesRegex(ValueError, 'Missing or extra'):
            package.collect_payload(self.root)

    def test_wrong_exit_code(self):
        self.receipt['commands'][0]['exit_code'] = 1
        self.save_receipt()
        with self.assertRaisesRegex(ValueError, 'Unexpected command or exit'):
            package.collect_payload(self.root)

    def test_false_success_flag(self):
        self.receipt['kernel_checked'] = False
        self.save_receipt()
        with self.assertRaisesRegex(ValueError, 'passed kernel-checked'):
            package.collect_payload(self.root)

    def test_omitted_axiom_report(self):
        del self.receipt['axioms'][self.names[0]]
        self.save_receipt()
        with self.assertRaisesRegex(ValueError, 'Recorded axiom inventory'):
            package.collect_payload(self.root)

    def test_extra_axiom(self):
        self.receipt['axioms'][self.names[0]] = ['untrustedAxiom']
        self.save_receipt()
        with self.assertRaisesRegex(ValueError, 'Unapproved recorded axiom'):
            package.collect_payload(self.root)

    def test_build_log_must_contain_actual_axiom_reports(self):
        record = next(r for r in self.receipt['commands'] if r['command'] == ['lake', 'build'])
        self.put('verification/recorded/'+record['log'], b'Build succeeded.\n')
        record['log_sha256'] = package.digest(b'Build succeeded.\n')
        self.save_receipt()
        with self.assertRaisesRegex(ValueError, 'Missing/extra dependency'):
            package.collect_payload(self.root)

    def test_negative_control_must_fail_inside_proof(self):
        record = next(r for r in self.receipt['commands'] if r['expected_failure'])
        log = b'validation/RejectFixture.lean:1:0: error: type mismatch\n'
        self.put('verification/recorded/'+record['log'], log)
        record['log_sha256'] = package.digest(log)
        self.save_receipt()
        with self.assertRaisesRegex(RuntimeError, 'statement or imports'):
            package.collect_payload(self.root)

    def test_manuscript_pin(self):
        self.put('reference/manuscript/main.tex', b'changed manuscript')
        self.refresh_receipt()
        with self.assertRaisesRegex(ValueError, 'Manuscript digest'):
            package.collect_payload(self.root)


    def test_bootstrap_command_contract(self):
        actual = list(self.receipt['commands'])
        bootstrap = [
            ['git', 'init', '--quiet'],
            ['git', 'remote', 'add', 'origin', self.lock['packages'][0]['url']],
            ['git', 'fetch', '--depth=1', 'origin', 'a'*40],
            ['git', 'checkout', '--detach', 'a'*40]]
        actual[2:2] = [{'command': c} for c in bootstrap]
        build = next(i for i, r in enumerate(actual) if r['command'] == ['lake', 'build'])
        actual[build:build] = [
            {'command': ['lake', 'build', 'Cache.Main']},
            {'command': ['lake', 'env', 'lean', '--run', '.lake/packages/mathlib/Cache/Main.lean', 'get']}]

        receipt = dict(self.receipt, commands=actual,
                       _check_source=(self.root/'scripts/check.py').read_text())
        expected = package.expected_commands(receipt, self.lock, package.validation_registry(self.root))
        self.assertEqual([c for c, _, _ in expected], [r['command'] for r in actual])

    def test_missing_axiom_source(self):
        (self.root/'CyclicBell/AxiomAudit.lean').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing required'):
            package.collect_payload(self.root)

    def test_log_path_traversal(self):
        self.receipt['commands'][0]['log'] = '../secret.log'
        self.save_receipt()
        with self.assertRaisesRegex(ValueError, 'Unexpected recorded log path'):
            package.collect_payload(self.root)

    def test_resource_failure_even_with_matching_log_digest(self):
        record = self.receipt['commands'][0]
        log = b'maximum number of heartbeats reached\n'
        self.put('verification/recorded/'+record['log'], log)
        record['log_sha256'] = package.digest(log)
        self.save_receipt()
        with self.assertRaisesRegex(ValueError, 'Resource failure'):
            package.collect_payload(self.root)

    def test_path_traversal(self):
        with self.assertRaisesRegex(ValueError, 'Unsafe archive'):
            package.safe_read(self.root, '../outside')

    def test_output_symlink(self):
        out = Path(self.temp.name)/'out.zip'
        out.symlink_to(self.root/'README.md')
        with self.assertRaisesRegex(ValueError, 'symlinked archive'):
            package.write_archive({'example': b'hello'}, out)


if __name__ == '__main__':
    unittest.main()
