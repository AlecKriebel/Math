#!/usr/bin/env python3
"""Local-only round2 F1/F2 controls plus the original operational regression suite."""
import contextlib
import datetime
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
fixture = AUDIT / 'reviews/operations_01/check_helpers.py'
ns = {'__name__': 'operation_fixture', '__file__': str(fixture)}
exec(compile(fixture.read_bytes(), str(fixture), 'exec'), ns)
p, t = ns['p'], ns['t']
DOI, META, QUEUE = ns['DOI'], ns['META'], ns['QUEUE']
PUB, SOURCE, ORIGINAL, FROZEN = ns['PUB'], ns['SOURCE'], ns['ORIGINAL'], ns['FROZEN']
EVIDENCE = {}


def populate(root):
    publication = root / 'publication'
    publication.mkdir()
    for name, data in PUB.items():
        (publication / name).write_bytes(data)
    source = publication / 'CURRENT_PRIORITY_AND_STATUS.md'
    source.write_bytes(SOURCE)
    captured = p.json_bytes(ns['receipt']())
    rp, ip = root / 'ZENODO_PUBLICATION_RECEIPT.json', root / 'ZENODO_POST_PUBLICATION_INSPECTION.json'
    rp.write_bytes(captured)
    ip.write_bytes(captured)
    return publication, source, rp, ip, captured


class RepairControls(ns['Helpers']):
    def test_exact_integer_schema_controls(self):
        with zipfile.ZipFile(io.BytesIO(PUB['gns_verification.zip'])) as archive:
            members = {name: archive.read(name) for name in archive.namelist()}
        results = []
        cases = [('integer_one', 1, True), ('boolean_true', True, False),
                 ('boolean_false', False, False), ('decimal_one', 1.0, False),
                 ('unsupported_zero', 0, False), ('unsupported_negative', -1, False),
                 ('unsupported_two', 2, False)]
        for label, schema, accept in cases:
            with self.subTest(case=label):
                changed = dict(members)
                manifest = p.parse_json(changed['PACKAGE_MANIFEST.json'])
                manifest['schema'] = schema
                changed['PACKAGE_MANIFEST.json'] = p.json_bytes(manifest)
                output = io.BytesIO()
                with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                    for name, data in changed.items(): archive.writestr(name, data)
                if accept:
                    p.archive_binding(output.getvalue(), ORIGINAL, PUB, SOURCE)
                else:
                    with self.assertRaisesRegex(ValueError, 'package manifest schema'):
                        p.archive_binding(output.getvalue(), ORIGINAL, PUB, SOURCE)
                results.append({'case': label, 'schema': schema, 'python_type': type(schema).__name__,
                                'outcome': 'ACCEPT' if accept else 'REJECT'})
        EVIDENCE['schema_controls'] = results

    def test_each_receipt_is_captured_validated_and_hashed_once(self):
        results = []
        for which in ('publication', 'inspection'):
            with self.subTest(receipt=which), tempfile.TemporaryDirectory(dir=HERE, prefix='receipt-capture-') as td:
                publication, source, rp, ip, captured = populate(Path(td))
                target = rp if which == 'publication' else ip
                invalid = p.json_bytes(ns['receipt']() | {'title': 'INVALID CHANGED RECEIPT'})
                real_read = p.regular_bytes
                counts = {}
                def capture_then_mutate(path):
                    counts[path] = counts.get(path, 0) + 1
                    data = real_read(path)
                    if path == target and counts[path] == 1:
                        target.write_bytes(invalid)
                    return data
                with patch.object(p, 'regular_bytes', side_effect=capture_then_mutate):
                    files, notice, validation = p.publication_inputs(
                        publication, DOI, rp, ip, source, ORIGINAL)
                self.assertEqual(files, PUB)
                self.assertEqual(notice, SOURCE)
                self.assertEqual(counts[rp], 1)
                self.assertEqual(counts[ip], 1)
                self.assertEqual(counts[source], 1)
                key = which + '_receipt_sha256'
                self.assertEqual(validation[key], p.sha(captured))
                self.assertNotEqual(validation[key], p.sha(invalid))
                self.assertEqual(target.read_bytes(), invalid)
                with self.assertRaisesRegex(ValueError, 'not confirmed production publication'):
                    p.publication_inputs(publication, DOI, rp, ip, source, ORIGINAL)
                results.append({'receipt': which, 'path_read_count': counts[target],
                                'both_receipts_captured_once': True,
                                'validated_receipt_sha256': p.sha(captured),
                                'mutated_wrong_title_sha256': p.sha(invalid),
                                'returned_hash_binds_validated_bytes': True,
                                'fresh_changed_receipt': 'REJECT'})
        EVIDENCE['receipt_capture_controls'] = results

    def test_full_main_uses_archive_validated_notice_after_disk_mutation(self):
        base, tree, commit = 'c' * 40, 'd' * 40, 'e' * 40
        after, _ = p.patch_queue(QUEUE, DOI)
        current, calls, counts = {}, [], {}
        real_build, real_inputs, real_read = p.build_current_files, p.publication_inputs, p.regular_bytes
        changed_source = SOURCE + b'Changed disk notice after successful archive validation.\n'
        with tempfile.TemporaryDirectory(dir=HERE, prefix='notice-capture-') as td:
            root = Path(td)
            publication, source, rp, ip, captured = populate(root)
            def capture(path):
                counts[path] = counts.get(path, 0) + 1
                return real_read(path)
            def inputs(*args, **kwargs):
                snapshot = real_inputs(*args, **kwargs)
                source.write_bytes(changed_source)
                return snapshot
            def build(*args):
                answer = real_build(*args)
                current.update(answer)
                return answer
            def git(*args, env=None, input=None):
                calls.append(args)
                if args[0] == 'show':
                    if args[1] == p.ORIGINAL + ':' + p.QPATH: return after
                    if args[1] == base + ':' + p.QPATH: return QUEUE
                    return ORIGINAL[args[1].split(':' + p.PREFIX, 1)[1]]
                if args[0] in ('fetch', 'ls-tree', 'read-tree', 'update-index'): return b''
                if args[0] == 'rev-parse': return (base + '\n').encode()
                if args[0] == 'hash-object': return ('f' * 40 + '\n').encode()
                if args[0] == 'write-tree': return (tree + '\n').encode()
                if args[0] == 'diff':
                    return b'1\t1\tqueue\n' if args[1] == '--numstat' else ('\n'.join(sorted({p.QPATH} | {p.PREFIX + n for n in current})) + '\n').encode()
                if args[0] == 'commit-tree': return (commit + '\n').encode()
                raise AssertionError('unexpected mocked Git call: ' + repr(args))
            with patch.object(p, 'A', root), patch.object(p, 'PUSHED_RECEIPT', root / 'absent'), \
                    patch.object(p, 'local_state', return_value={'head': 'main', 'index_sha256': 'unchanged'}), \
                    patch.object(p, 'pr_metadata', return_value=META), patch.object(p, 'git', side_effect=git), \
                    patch.object(p, 'load_snapshot', return_value=(ORIGINAL, FROZEN)), \
                    patch.object(p, 'regular_bytes', side_effect=capture), \
                    patch.object(p, 'publication_inputs', side_effect=inputs), \
                    patch.object(p, 'build_current_files', side_effect=build), \
                    patch.object(sys, 'argv', ['helper', '--doi', DOI, '--source-audit', str(source)]), \
                    contextlib.redirect_stdout(io.StringIO()):
                p.main()
            saved = p.parse_json((root / 'INTEGRATION_PREPARED_RECEIPT.json').read_bytes())
            self.assertEqual(source.read_bytes(), changed_source)
            self.assertEqual(counts[source], 1)
            self.assertEqual(counts[rp], 1)
            self.assertEqual(counts[ip], 1)
            self.assertTrue(current['CURRENT_SOURCE_AUDIT.md'].endswith(SOURCE))
            self.assertNotIn(b'Changed disk notice', current['CURRENT_SOURCE_AUDIT.md'])
            self.assertEqual(saved['publication_validation']['current_source_notice_sha256'], p.sha(SOURCE))
            self.assertEqual(saved['current_attempt_replay']['integrity'], 'PASS')
            self.assertTrue(all(current[n] == ORIGINAL[n] for n in FROZEN))
            self.assertFalse(any(args[0] == 'push' for args in calls))
            with self.assertRaisesRegex(ValueError, 'source notice differs'):
                real_inputs(publication, DOI, rp, ip, source, ORIGINAL)
            EVIDENCE['full_main_notice_capture'] = {
                'source_path_read_count': counts[source], 'installed_notice_is_validated_capture': True,
                'changed_disk_notice_installed': False, 'wrapper_replay': 'PASS',
                'validated_and_installed_notice_sha256': p.sha(SOURCE),
                'changed_disk_notice_sha256': p.sha(changed_source),
                'fresh_changed_notice': 'REJECT', 'real_remote_git_calls': 0,
                'frozen_packet_audit_unchanged': True}

    def test_tracker_consumes_new_snapshot_contract_without_notice_reread(self):
        validation = {'current_source_notice_sha256': p.sha(SOURCE)}
        with tempfile.TemporaryDirectory(dir=HERE, prefix='tracker-capture-') as td:
            root = Path(td)
            with patch.object(t, 'A', root), \
                    patch.object(t, 'publication_inputs', return_value=(PUB, SOURCE, validation)) as inputs, \
                    patch.object(t, 'inspect', return_value=[t.HEADERS]), \
                    patch.object(t, 'regular_bytes', side_effect=AssertionError('snapshot must not be reread')), \
                    patch.object(t, 'call', side_effect=AssertionError('no live GWS operation')), \
                    patch.object(sys, 'argv', ['tracker', '--doi', DOI]), \
                    contextlib.redirect_stdout(io.StringIO()):
                t.main()
            inputs.assert_called_once()
            ready = p.parse_json((root / 'TRACKER_ROW_READY.json').read_bytes())
            self.assertEqual(ready['publication_validation'], validation)
            self.assertFalse(ready['applied'])
            EVIDENCE['tracker_snapshot_contract'] = {'snapshot_calls': 1, 'notice_rereads': 0,
                                                      'live_gws_calls': 0, 'row_preparation': 'PASS'}


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RepairControls)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary = {'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'result': 'PASS' if result.wasSuccessful() else 'FAIL',
               'python_optimization': sys.flags.optimize, 'tests_run': result.testsRun,
               'failures': len(result.failures), 'errors': len(result.errors), 'controls': EVIDENCE,
               'remote_mutations': 0, 'git_mutations': 0, 'shared_index_mutations': 0,
               'artifact_scope': 'operations_02 disposable fixtures; native29 read only',
               'actual_rebuilt_publication_hashes_are_final': False}
    print(json.dumps(summary, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() else 1)
