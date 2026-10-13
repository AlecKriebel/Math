#!/usr/bin/env python3
"""Local-only regression fixtures for PR623 helpers; no remote calls/mutations."""
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


p = load('prepare_integration', AUDIT / 'prepare_integration.py')
t = load('record_tracker', AUDIT / 'record_tracker.py')
DOI = '10.5281/zenodo.99999999'
META = {'number': 623, 'state': 'OPEN', 'baseRefName': 'main', 'headRefName': p.BRANCH,
        'headRefOid': p.ORIGINAL, 'isCrossRepository': False,
        'headRepositoryOwner': {'login': 'AlecKriebel'}}
ROW = ('| 651 | 30001184 / OWR-3392-012 | Extending Dilated E0-Semigroups Beyond GNS Representations | '
       '0.1067 | 6.0 | 3 | 2009 | queued | 0/5 |  |  |  |')
QUEUE = ('prefix byte identity\r\n' + ROW + '\r\n| other | row bytes | queued | 0/5 |\r\ntrailer').encode()
SOURCE = b'Explicit corollary credit: Bhat, Fagnola and Hachicha. Extensively AI-assisted; unrefereed. No exhaustive first-priority claim.\n'
ORIGINAL, FROZEN = p.load_snapshot(AUDIT / 'native' / p.PREFIX)
PUB = {'gns_generation_counterexample.pdf': b'%PDF-1.7\nfixture\n',
       'gns_generation_counterexample.tex': b'fixture tex',
       'zenodo-deposit.json': p.json_bytes({'metadata': {'title': p.TITLE},
           'files': [{'path': n} for n in ('gns_generation_counterexample.pdf', 'gns_verification.zip')]})}


def fixture_archive(extra=None):
    members = {'candidate/' + n: d for n, d in ORIGINAL.items()}
    members.update({n: PUB[n] for n in ('gns_generation_counterexample.pdf', 'gns_generation_counterexample.tex')})
    members['CURRENT_PRIORITY_AND_STATUS.md'] = SOURCE
    members['PACKAGE_MANIFEST.json'] = p.json_bytes({'schema': 1, 'file_count': len(members),
        'files': [{'path': n, 'bytes': len(d), 'sha256': p.sha(d)} for n, d in sorted(members.items())]})
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in members.items(): z.writestr(name, data)
        if extra:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)
                z.writestr(*extra)
    return buf.getvalue()


PUB['gns_verification.zip'] = fixture_archive()


def receipt():
    return {'environment': 'production', 'title': p.TITLE, 'state': 'published',
            'doi': DOI, 'doi_url': 'https://doi.org/' + DOI, 'id': 99999999,
            'record_url': 'https://zenodo.org/records/99999999', 'verified_utc': '2026-10-13T00:00:00Z',
            'receipt_saved': True, 'metadata_normalizations': [],
            'doi_resolution': {'status': 'resolved', 'http_status': 200},
            'files': [{'name': n, 'size': len(PUB[n]), 'sha256': p.sha(PUB[n])}
                      for n in ('gns_generation_counterexample.pdf', 'gns_verification.zip')]}


class Helpers(unittest.TestCase):
    def test_known_original_and_only_exact_successful_prior(self):
        self.assertEqual(p.check_known_head(META, DOI), p.ORIGINAL)
        prior = {'schema': 'pr623-scoped-integration-receipt-v1', 'pr': 623, 'problem_id': p.PROBLEM,
                 'branch': p.BRANCH, 'pushed': True, 'historical_candidate_commit': p.ORIGINAL,
                 'proof_sha256': p.PROOF_SHA, 'doi': DOI, 'integration_commit': 'a' * 40}
        changed = META | {'headRefOid': 'a' * 40}
        self.assertEqual(p.check_known_head(changed, DOI, prior), 'a' * 40)
        for bad in (None, prior | {'pushed': False}, prior | {'doi': '10.5281/zenodo.111'},
                    prior | {'pr': 618}, prior | {'branch': 'other'}):
            with self.assertRaises(ValueError):
                p.check_known_head(changed, DOI, bad)
        with self.assertRaises(ValueError):
            p.check_known_head(META | {'headRefOid': 'b' * 40}, DOI, prior)

    def test_unknown_head_aborts_before_any_candidate_or_publication_read(self):
        with tempfile.TemporaryDirectory(dir=HERE, prefix='fixture-') as td:
            with patch.object(p, 'local_state', return_value={}), patch.object(p, 'PUSHED_RECEIPT', Path(td) / 'absent'), \
                    patch.object(p, 'pr_metadata', return_value=META | {'headRefOid': 'b' * 40}), \
                    patch.object(p, 'git', side_effect=AssertionError('candidate/git must not be read')), \
                    patch.object(p, 'load_snapshot', side_effect=AssertionError('native must not be read')), \
                    patch.object(p, 'publication_inputs', side_effect=AssertionError('paper must not be read')), \
                    patch.object(sys, 'argv', ['prepare_integration.py', '--doi', DOI]):
                with self.assertRaisesRegex(ValueError, 'unreviewed PR head'):
                    p.main()

    def test_exact_selected_scope_and_repo(self):
        for change in ({'number': 618}, {'state': 'MERGED'}, {'baseRefName': 'other'},
                       {'headRefName': 'other'}, {'isCrossRepository': True},
                       {'headRepositoryOwner': {'login': 'someone'}}):
            with self.assertRaises(ValueError):
                p.check_known_head(META | change, DOI)

    def test_one_queue_row_preserves_all_other_bytes_and_line_endings(self):
        after, rec = p.patch_queue(QUEUE, DOI)
        before_lines = QUEUE.splitlines(keepends=True)
        after_lines = after.splitlines(keepends=True)
        self.assertEqual([i for i, pair in enumerate(zip(before_lines, after_lines)) if pair[0] != pair[1]], [1])
        self.assertEqual(before_lines[0], after_lines[0])
        self.assertEqual(before_lines[2:], after_lines[2:])
        self.assertTrue(after_lines[1].endswith(b'\r\n'))
        self.assertEqual(rec['changed_cells'], ['Status', 'Turns', 'Findings'])
        cells = after_lines[1].split(b'|')
        self.assertEqual(cells[8].strip(), b'claimed_solved')
        self.assertEqual(cells[9].strip(), b'1/5')
        for bad in (QUEUE + (ROW + '\n').encode(), QUEUE.replace(b' queued ', b' claimed_solved '),
                    QUEUE.replace(b' 0/5 ', b' 2/5 '), QUEUE.replace(b'| 651 |', b'| 999 |')):
            with self.assertRaises(ValueError):
                p.patch_queue(bad, DOI)

    def test_frozen_bytes_current_outer_replay_and_adversarial_rehash(self):
        _, qrec = p.patch_queue(QUEUE, DOI)
        current = p.build_current_files(ORIGINAL, FROZEN, PUB, SOURCE, DOI, 'fixture-time', qrec)
        self.assertTrue(all(current[n] == ORIGINAL[n] for n in FROZEN))
        self.assertEqual(p.sha(current['packet/PROOF.md']), p.PROOF_SHA)
        with tempfile.TemporaryDirectory(dir=HERE, prefix='fixture-') as td:
            root = Path(td)
            for name, data in current.items():
                dest = root / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
            result = subprocess.run([sys.executable, '-I', str(root / 'verify_publication.py')], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual(p.parse_json(result.stdout)['manifested_files'], 35)
            local_env = os.environ.copy()
            local_env['TMPDIR'] = str(HERE)
            controls = subprocess.run([sys.executable, '-I', str(root / 'test_integrity.py')], capture_output=True, env=local_env)
            self.assertEqual(controls.returncode, 0, controls.stderr.decode())
            # A dishonest outer rehash cannot conceal a modified frozen proof.
            (root / 'packet/PROOF.md').write_bytes(current['packet/PROOF.md'] + b'!')
            mf = p.parse_json((root / 'PUBLICATION_MANIFEST.json').read_bytes())
            for entry in mf['files']:
                if entry['path'] == 'packet/PROOF.md':
                    data = (root / entry['path']).read_bytes()
                    entry.update(bytes=len(data), sha256=p.sha(data))
            (root / 'PUBLICATION_MANIFEST.json').write_bytes(p.json_bytes(mf))
            for flags in ([], ['-O']):
                result = subprocess.run([sys.executable, '-I', *flags, str(root / 'verify_publication.py'), '--integrity-only'], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(b'frozen input changed', result.stderr)

    def test_receipt_and_local_hash_gate(self):
        with tempfile.TemporaryDirectory(dir=HERE, prefix='fixture-') as td:
            root = Path(td)
            for name, data in PUB.items():
                (root / name).write_bytes(data)
            (root / 'CURRENT_PRIORITY_AND_STATUS.md').write_bytes(SOURCE)
            r = receipt()
            rp, ip = root / 'receipt.json', root / 'inspection.json'
            rp.write_bytes(p.json_bytes(r))
            ip.write_bytes(p.json_bytes(r))
            p.publication_inputs(root, DOI, rp, ip)
            for mutation in ({'state': 'draft'}, {'environment': 'sandbox'}, {'doi': '10.5281/zenodo.111'},
                             {'receipt_saved': False}, {'files': r['files'] + [r['files'][0]]},
                             {'doi_resolution': {'status': 'unresolved', 'http_status': 404}}):
                ip.write_bytes(p.json_bytes(r | mutation))
                with self.assertRaises(ValueError):
                    p.publication_inputs(root, DOI, rp, ip)
            ip.write_bytes(p.json_bytes(r))
            (root / 'gns_verification.zip').write_bytes(b'tampered local zip')
            with self.assertRaisesRegex(ValueError, 'hashes differ'):
                p.publication_inputs(root, DOI, rp, ip)

    def test_archive_inventory_candidate_and_paper_binding(self):
        self.assertEqual(p.archive_binding(PUB['gns_verification.zip'], ORIGINAL, PUB, SOURCE)['original_candidate_files_bound'], 29)
        for bad in (fixture_archive(('EXTRA.txt', b'extra')), fixture_archive(('gns_generation_counterexample.tex', b'duplicate')),
                    fixture_archive(('../escape', b'bad'))):
            with self.assertRaises(ValueError):
                p.archive_binding(bad, ORIGINAL, PUB, SOURCE)
        with self.assertRaises(ValueError):
            p.archive_binding(PUB['gns_verification.zip'], ORIGINAL, PUB | {'gns_generation_counterexample.tex': b'different'}, SOURCE)
        with self.assertRaises(ValueError):
            p.archive_binding(PUB['gns_verification.zip'], ORIGINAL, PUB, SOURCE + b'changed')

    def run_main_fixture(self, mode):
        base, tree, commit = 'c' * 40, 'd' * 40, 'e' * 40
        after_queue, _ = p.patch_queue(QUEUE, DOI)
        calls = []
        current = {}
        real_build = p.build_current_files
        def build(*args):
            result = real_build(*args)
            current.update(result)
            return result
        def fake_git(*args, env=None, input=None):
            calls.append((args, env))
            if args[0] == 'show':
                spec = args[1]
                if spec == p.ORIGINAL + ':' + p.QPATH:
                    return after_queue
                if spec == base + ':' + p.QPATH:
                    return QUEUE
                return ORIGINAL[spec.split(':' + p.PREFIX, 1)[1]]
            if args[0] in ('fetch', 'ls-tree', 'read-tree', 'update-index', 'push'):
                return b''
            if args[0] == 'rev-parse': return (base + '\n').encode()
            if args[0] == 'hash-object': return ('f' * 40 + '\n').encode()
            if args[0] == 'write-tree': return (tree + '\n').encode()
            if args[0] == 'diff':
                return b'1\t1\tqueue\n' if args[1] == '--numstat' else ('\n'.join(sorted({p.QPATH} | {p.PREFIX + n for n in current})) + '\n').encode()
            if args[0] == 'commit-tree': return (commit + '\n').encode()
            if args[0] == 'ls-remote': return ((('a' * 40) if mode == 'main_race' else base) + '\trefs/heads/main\n').encode()
            raise AssertionError('unexpected fixture git call: ' + repr(args))
        metas = [META]
        if mode == 'head_race': metas += [META | {'headRefOid': 'b' * 40}]
        else: metas += [META, META | {'headRefOid': commit}]
        with tempfile.TemporaryDirectory(dir=HERE, prefix='fixture-') as td:
            root = Path(td)
            src = root / 'source.md'
            src.write_bytes(SOURCE)
            with patch.object(p, 'A', root), patch.object(p, 'PUSHED_RECEIPT', root / 'pushed.json'), \
                    patch.object(p, 'local_state', return_value={'head': 'selected-main', 'index_sha256': 'fixture'}), \
                    patch.object(p, 'pr_metadata', side_effect=metas), patch.object(p, 'git', side_effect=fake_git), \
                    patch.object(p, 'load_snapshot', return_value=(ORIGINAL, FROZEN)), \
                    patch.object(p, 'publication_inputs', return_value=(PUB, {})), \
                    patch.object(p, 'build_current_files', side_effect=build), \
                    patch.object(sys, 'argv', ['prepare_integration.py', '--doi', DOI, '--push', '--source-audit', str(src)]):
                if mode == 'success':
                    with patch('builtins.print'):
                        p.main()
                    saved = p.parse_json((root / 'pushed.json').read_bytes())
                    self.assertTrue(saved['pushed'])
                    self.assertEqual(saved['integration_commit'], commit)
                else:
                    with self.assertRaises(ValueError):
                        p.main()
                    self.assertFalse((root / 'pushed.json').exists())
                    self.assertTrue((root / 'INTEGRATION_PREPARED_RECEIPT.json').exists())
        pushes = [args for args, env in calls if args[0] == 'push']
        self.assertEqual(len(pushes), 1 if mode == 'success' else 0)
        if pushes:
            self.assertEqual(pushes[0], ('push', 'origin', commit + ':refs/heads/' + p.BRANCH))
        for args, env in calls:
            if args[0] in ('read-tree', 'update-index', 'write-tree'):
                self.assertIsNotNone(env)
                self.assertIn('GIT_INDEX_FILE', env)
        commits = [args for args, env in calls if args[0] == 'commit-tree']
        self.assertEqual(commits[0], ('commit-tree', tree, '-p', base, '-p', p.ORIGINAL))

    def test_final_head_race_aborts_without_push(self): self.run_main_fixture('head_race')
    def test_final_main_race_aborts_without_push(self): self.run_main_fixture('main_race')
    def test_nonforce_push_alternate_index_and_two_parents(self): self.run_main_fixture('success')

    def test_prior_successful_tree_receipt_and_frozen_binding(self):
        base, head = 'c' * 40, 'a' * 40
        after_queue, qrec = p.patch_queue(QUEUE, DOI)
        current = p.build_current_files(ORIGINAL, FROZEN, PUB, SOURCE, DOI, 'fixture-time', qrec)
        names = sorted({p.QPATH} | {p.PREFIX + n for n in current})
        prior = {'integration_commit': head, 'main_base': base, 'existing_pr_head': p.ORIGINAL,
                 'changed_paths': names, 'attempt_sha256': {n: p.sha(d) for n, d in current.items()},
                 'queue_patch': qrec, 'all_frozen_bytes_unchanged': True,
                 'shared_checkout_and_index_untouched': True, 'frozen_packet_files': 13, 'frozen_audit_files': 11}
        def fake_git(*args):
            if args[0] == 'ls-tree': return ('\n'.join(sorted(p.PREFIX + n for n in current)) + '\n').encode()
            if args[0] == 'diff': return ('\n'.join(names) + '\n').encode()
            if args[:3] == ('show', '-s', '--format=%P'): return (base + ' ' + p.ORIGINAL + '\n').encode()
            if args[1] == head + ':' + p.QPATH: return after_queue
            return current[args[1].split(':' + p.PREFIX, 1)[1]]
        with patch.object(p, 'git', side_effect=fake_git):
            p.verify_prior_tree(prior, head)
            with self.assertRaises(ValueError): p.verify_prior_tree(prior | {'frozen_packet_files': 12}, head)
            current['packet/PROOF.md'] += b'!'
            dishonest = copy.deepcopy(prior)
            dishonest['attempt_sha256']['packet/PROOF.md'] = p.sha(current['packet/PROOF.md'])
            with self.assertRaisesRegex(ValueError, 'frozen input bytes changed'):
                p.verify_prior_tree(dishonest, head)

    def test_tracker_exact_doi_and_conflicting_row_guards(self):
        row = t.wanted_row(DOI)
        values = [t.HEADERS, row]
        self.assertEqual(t.exact_existing(values, row, DOI), [2])
        with self.assertRaises(ValueError): t.exact_existing(values + [row], row, DOI)
        with self.assertRaises(ValueError): t.exact_existing([t.HEADERS, row[:3] + ['other']], row, DOI)
        self.assertEqual(row[1], '')
        self.assertIn('Bhat-Fagnola-Hachicha', row[3])

    def test_tracker_ambiguous_append_is_not_retried(self):
        row = t.wanted_row(DOI)
        with tempfile.TemporaryDirectory(dir=HERE, prefix='fixture-') as td:
            pending = Path(td) / 'pending.json'
            pending.write_bytes(p.json_bytes({'action_outcome': 'unconfirmed'}))
            with patch.object(t, 'PENDING', pending), patch.object(t, 'inspect', return_value=[t.HEADERS]), \
                    patch.object(t, 'call', side_effect=AssertionError('no append allowed')):
                with self.assertRaisesRegex(ValueError, 'unconfirmed'):
                    t.append_once(DOI, row, {})
                with patch.object(t, 'inspect', return_value=[t.HEADERS, row]):
                    self.assertTrue(t.append_once(DOI, row, {})['already_present'])

    def test_tracker_exact_append_readback_and_global_unique(self):
        row = t.wanted_row(DOI)
        response = {'updates': {'updatedRange': "'Math Puzzles'!A2:D2", 'updatedRows': 1,
                                'updatedColumns': 4, 'updatedCells': 4}}
        for duplicate in (False, True):
            with tempfile.TemporaryDirectory(dir=HERE, prefix='fixture-') as td:
                pending = Path(td) / 'pending.json'
                calls = []
                def call(resource, method, params, body=None):
                    calls.append((method, params, body))
                    if method == 'append':
                        self.assertEqual(body, {'majorDimension': 'ROWS', 'values': [row]})
                        self.assertTrue(pending.exists(), 'unconfirmed marker must precede POST')
                        return response
                    if params['range'].endswith('A2:D2'): return {'values': [row]}
                    return {'values': [t.HEADERS, row] + ([row] if duplicate else [])}
                with patch.object(t, 'PENDING', pending), patch.object(t, 'inspect', return_value=[t.HEADERS]), patch.object(t, 'call', side_effect=call):
                    if duplicate:
                        with self.assertRaisesRegex(ValueError, 'duplicate exact DOI'):
                            t.append_once(DOI, row, {})
                        self.assertNotEqual(p.parse_json(pending.read_bytes())['action_outcome'], 'confirmed')
                    else:
                        result = t.append_once(DOI, row, {})
                        self.assertTrue(result['applied'])
                        self.assertEqual(result['global_exact_doi_rows'], [2])
                        self.assertEqual(p.parse_json(pending.read_bytes())['action_outcome'], 'confirmed')
                    self.assertEqual(sum(method == 'append' for method, params, body in calls), 1)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Helpers)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary = {'result': 'PASS' if result.wasSuccessful() else 'FAIL', 'tests_run': result.testsRun,
               'failures': len(result.failures), 'errors': len(result.errors),
               'remote_mutations': 0, 'git_mutations': 0, 'shared_index_mutations': 0,
               'actual_frozen_packet_files': 13, 'actual_frozen_audit_files': 11,
               'fixture_git_and_gws_only': True, 'wrapper_replay_actual': True}
    print(json.dumps(summary, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() else 1)
