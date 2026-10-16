#!/usr/bin/env python3
"""Local PR894 tooling regression audit; fixtures are NOT ACTUAL PAPER.
Run with -I -S -B and --work-dir a fresh outside directory. Never publishes.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import struct
import sys
import zipfile


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--work-dir', type=Path, required=True)
    for name in ('catalog', 'problems', 'reports', 'primary-dir'):
        parser.add_argument('--' + name, type=Path)
    args = parser.parse_args()
    base = Path(__file__).absolute().parent
    spec = importlib.util.spec_from_file_location('publication_portable', base / 'portable.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.isolated()
    m.require(not args.work_dir.exists() and not args.work_dir.is_symlink(), 'fresh audit directory')
    parent = m.selected_root(args.work_dir.absolute().parent)
    work = parent / args.work_dir.name; work.mkdir(mode=0o700)
    package = base / 'verification'
    external_pin = (base / 'PACKAGE_INDEX_SHA256.txt').read_text().strip()
    blobs = m.package_inputs(package, external_pin)
    # Compact fixtures share identical authenticated bytes. Mutations unlink
    # first, so changes cannot alter the cache or another fixture.
    cache = work / '_fixture_blobs'; cache.mkdir()
    def replace_bytes(path, raw):
        path.unlink(); path.write_bytes(raw)
    def compact_materialize(root, values):
        root.mkdir()
        for name, raw in values.items():
            key = m.sha(raw); stored = cache / key
            if not stored.exists(): stored.write_bytes(raw)
            target = root / m.safe_name(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.link(stored, target)
    m.materialize = compact_materialize
    results = []
    started = datetime.now(timezone.utc).isoformat()
    def enc(value): return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()
    def clean(value):
        if isinstance(value, bytes): return m.pin_bytes(value)
        if isinstance(value, dict): return {k: clean(v) for k, v in value.items()}
        if isinstance(value, list): return [clean(v) for v in value]
        return value
    def record(label, outcome, evidence=None):
        row = {'test': label, 'outcome': outcome, 'utc': datetime.now(timezone.utc).isoformat()}
        if evidence is not None: row['evidence'] = clean(evidence)
        results.append(row)
        with (work / 'tests.jsonl').open('ab') as stream:
            stream.write((json.dumps(row, sort_keys=True) + '\n').encode()); stream.flush(); os.fsync(stream.fileno())
        return row
    def check(label, function):
        try:
            evidence = function()
        except Exception as error:
            return record(label, 'FAIL', {'exception_type': type(error).__name__, 'reason': str(error).replace(str(base), '<TOOL_ROOT>').replace(str(work), '<AUDIT_ROOT>')})
        return record(label, 'PASS', evidence)
    def reject(label, function, fragment=None):
        def test():
            try: function()
            except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as error:
                m.require(fragment is None or fragment in str(error), 'unexpected rejection: ' + type(error).__name__ + ': ' + str(error))
                return {'rejected': True, 'exception_type': type(error).__name__}
            raise ValueError('malformed input accepted')
        return check(label, test)
    completed_seen = {}
    for old in (base / 'private_tmp').rglob('*'):
        if old.is_file() and not old.is_symlink() and 'primary' not in old.parts and old.suffix != '.jsonl':
            completed_seen.setdefault((old.stat().st_size, m.sha(old.read_bytes())), old)
    def dedupe_completed():
        # Only called after the invocation has ended and raw streams are durable.
        # Keep byte-identical evidence; no process or result is reconstructed.
        for path in work.rglob('*'):
            if not path.is_file() or path.is_symlink() or path.suffix == '.jsonl': continue
            key = (path.stat().st_size, m.sha(path.read_bytes()))
            prior = completed_seen.get(key)
            if prior is not None and prior.exists() and path.stat().st_ino != prior.stat().st_ino:
                temp = path.with_name(path.name + '.dedup-link')
                os.link(prior, temp); os.replace(temp, path)
            else: completed_seen[key] = path
    count = 0
    def invoke(label, tail, optimize=0, expected_rc=0, environment=None):
        nonlocal count
        count += 1
        command = [sys.executable, '-I', '-S', '-B'] + (['-O'] if optimize else []) + [str(base / 'portable.py'), *map(str, tail)]
        meta, out, err = m.record_process(command, work, work / ('invocation-%02d' % count), 900, environment=environment)
        # Raw invocation evidence is already durable before checking these values.
        dedupe_completed()
        m.require(meta['returncode'] == expected_rc if expected_rc == 0 else meta['returncode'] != 0, 'unexpected invocation rc')
        m.require(not meta['timeout'], 'invocation timeout')
        value = m.strict_json(out) if out.startswith(b'{') else None
        evidence = {'outer_optimize': optimize, 'process': meta}
        if expected_rc == 0:
            m.require(err == b'' and type(value) is dict and value['status'] == 'PASS', 'invocation did not pass cleanly')
            replay = value.get('replay', value.get('portable', value.get('verification', {})).get('replay'))
            if replay is not None:
                evidence['replay_label'] = replay['label']
                evidence['archival_code_executed'] = replay['archival_code_executed']
                if replay['archival_code_executed']:
                    evidence['root_flags'] = replay['launcher']['root_flags']
                    evidence['child_flags'] = [e['measured_flags'] for e in replay['launcher']['events']]
                    evidence['child_processes'] = [e['process'] for e in replay['launcher']['events']]
                    evidence['child_kinds'] = [e['kind'] for e in replay['launcher']['events']]
                    m.require(replay['original_requested_diagnostic_children'] == 2 and replay['extra_control_children'] == 6, 'replay children')
                else:
                    m.require(replay['label'] == 'VERIFY_ONLY_BYTE_AUTHENTICATION_NO_ARCHIVAL_EXECUTION', 'exact verify-only label')
            if 'canonical_pair' in value:
                evidence['canonical_pair'] = value['canonical_pair']; evidence['statement'] = value['statement']
            if 'pdf_validation' in value:
                evidence['pdf_validation'] = value['pdf_validation']; evidence['visual_qa'] = value['visual_qa']
        else:
            evidence['rejected'] = True
        return value, evidence
    def invocation_check(label, tail, **kwargs):
        return check(label, lambda: invoke(label, tail, **kwargs)[1])
    invocation_check('verify-only normal', ['verify', external_pin, '--root', package, '--verify-only'])
    invocation_check('verify-only optimized', ['verify', external_pin, '--root', package, '--verify-only'], optimize=1)
    invocation_check('default replay normal', ['verify', external_pin, '--root', package, '--receipt-dir', work / 'replay-normal'])
    invocation_check('default replay optimized', ['verify', external_pin, '--root', package, '--receipt-dir', work / 'replay-optimized'], optimize=1)
    hostile_folder = work / 'hostile-startup'; hostile_folder.mkdir()
    hostile_marker = hostile_folder / 'HOOK_EXECUTED'
    frozen_output = blobs['source/authored/CHECK_RESULTS.json']
    hook = ('from pathlib import Path\nimport os\nPath(' + repr(str(hostile_marker)) + ').write_bytes(b"HOSTILE_STARTUP_EXECUTED\\n")\nos.write(1,' + repr(frozen_output) + ')\nos._exit(0)\n').encode()
    (hostile_folder / 'sitecustomize.py').write_bytes(hook)
    (hostile_folder / 'usercustomize.py').write_bytes(hook)
    hostile_environment = dict(os.environ)
    hostile_environment.update({'PYTHONPATH': str(hostile_folder), 'PYTHONOPTIMIZE': '2', 'PYTHONSTARTUP': str(hostile_folder / 'sitecustomize.py')})
    def hook_capability():
        meta, stdout, stderr = m.record_process([sys.executable, '-B', str(package / 'source/authored/check_algebra.py')], work, work / 'unisolated-hostile-probe', 120, environment=hostile_environment)
        m.require(meta['returncode'] == 0 and stdout == frozen_output and stderr == b'' and hostile_marker.exists(), 'hostile hook fixture not capable')
        hostile_marker.rename(hostile_folder / 'UNISOLATED_PROBE_EXECUTED')
        return {'process': meta, 'hook_capability_demonstrated': True, 'unisolated_probe_is_not_an_accepted_verification': True}
    check('hostile startup hook capability control', hook_capability)
    for mode in (0, 1):
        def hardened_hostile(mode=mode):
            value, evidence = invoke('hostile replay', ['verify', external_pin, '--root', package, '--receipt-dir', work / ('hostile-replay-%d' % mode)], optimize=mode, environment=hostile_environment)
            replay = value['replay']; events = replay['launcher']['events']
            m.require(not hostile_marker.exists(), 'hostile startup hook executed')
            m.require([e['measured_flags']['optimize'] for e in events[:2]] == [0, 1] and all(e['original_execution_began'] for e in events[:2]), 'original calculations not actually executed at 0/1')
            m.require({'PYTHONPATH', 'PYTHONOPTIMIZE'} <= set(replay['wrapper_process']['removed_environment_keys']), 'startup variables not filtered for archival wrapper')
            evidence['hostile_hook_executed'] = False
            evidence['original_positive_execution_markers'] = [e['original_execution_began'] for e in events[:2]]
            return evidence
        check('hostile PYTHONPATH and PYTHONOPTIMIZE=2 hardened replay mode %d' % mode, hardened_hostile)
    check('hostile hook stayed inactive across hardened runs', lambda: m.require(not hostile_marker.exists(), 'hostile hook marker appeared'))
    builds = []
    for number in (1, 2):
        folder = work / ('build-%d' % number); folder.mkdir()
        path = folder / 'post-lie-verification.zip'; builds.append(path)
        invocation_check('fresh deterministic build %d' % number, ['build', external_pin, path, '--root', package, '--receipt-dir', work / ('replay-build-%d' % number)])
    check('two independent build bytes equal', lambda: m.require(m.read_regular(builds[0]) == m.read_regular(builds[1]), 'build bytes differ'))
    current_blobs = {'verification/' + n: b for n, b in blobs.items()}
    for name in ('portable.py', 'metadata.json', 'zenodo-deposit.json', 'note.tex'):
        current_blobs[name] = blobs[name]
    current_blobs['CURRENT_PUBLICATION.json'] = enc({'schema': m.LAYOUT_SCHEMA, 'problem_id': '30005737', 'portable_prefix': 'verification', 'zip_path': 'post-lie-verification.zip', 'pdf_path': 'post-lie-note.pdf', 'tex_path': 'note.tex'})
    current_blobs['post-lie-note.pdf'] = b'%PDF-1.7\n% NOT ACTUAL PAPER. HEADER-ONLY TOOLING FIXTURE; NOT A VALID PAPER PDF.\n'
    current_blobs['post-lie-verification.zip'] = builds[0].read_bytes()
    def index_current(values):
        return enc({'schema': m.CURRENT_SCHEMA, 'problem_id': '30005737', 'files': [{'path': n, **m.pin_bytes(b)} for n, b in sorted(values.items()) if n != 'CURRENT_PUBLICATION_MANIFEST.json']})
    current_raw = index_current(current_blobs); current_pin = m.sha(current_raw)
    current_blobs['CURRENT_PUBLICATION_MANIFEST.json'] = current_raw
    current = work / 'NOT_ACTUAL_PAPER_current'; m.materialize(current, current_blobs)
    invocation_check('current fixture verify-only header-only explicitly', ['current', current_pin, '--root', current, '--verify-only'])
    invocation_check('current fixture actual default replay', ['current', current_pin, '--root', current, '--receipt-dir', work / 'replay-current'])
    invocation_check('current fixture optimized actual replay', ['current', current_pin, '--root', current, '--receipt-dir', work / 'replay-current-optimized'], optimize=1)
    invocation_check('wrong external package pin', ['verify', '0' * 64, '--root', package, '--verify-only'], expected_rc=1)
    invocation_check('wrong external current pin', ['current', '0' * 64, '--root', current, '--verify-only'], expected_rc=1)
    invocation_check('build inside indexed root rejected before replay', ['build', external_pin, package / 'post-lie-verification.zip', '--root', package, '--receipt-dir', work / 'SHOULD_NOT_EXIST'], expected_rc=1)
    check('inside-output rejection created no receipt directory', lambda: m.require(not (work / 'SHOULD_NOT_EXIST').exists(), 'preflight launched work'))
    invocation_check('build refuses existing output', ['build', external_pin, builds[0], '--root', package, '--receipt-dir', work / 'SHOULD_NOT_EXIST_2'], expected_rc=1)
    check('existing-output rejection created no receipts', lambda: m.require(not (work / 'SHOULD_NOT_EXIST_2').exists(), 'no-overwrite preflight launched work'))
    invocation_check('build cannot request verify-only', ['build', external_pin, work / 'post-lie-verification.zip', '--root', package, '--verify-only'], expected_rc=2)
    def clone_package(label):
        target = work / label; m.materialize(target, blobs); return target
    def reindex(target):
        data = m.strict_json((target / 'package_index.json').read_bytes())
        for row in data['files']:
            row.update(m.pin_bytes((target / row['path']).read_bytes()))
        raw = enc(data); replace_bytes(target / 'package_index.json', raw); return m.sha(raw)
    damaged = clone_package('damaged-original'); cp = damaged / 'source/authored/check_algebra.py'; replace_bytes(cp, cp.read_bytes() + b'\nraise RuntimeError("MUST_NOT_EXECUTE")\n')
    damaged_pin = reindex(damaged)
    invocation_check('externally reindexed corrupt original rejected immutably', ['verify', damaged_pin, '--root', damaged, '--receipt-dir', work / 'CORRUPT_MUST_NOT_EXECUTE'], expected_rc=1)
    check('corrupt original creates no execution receipts', lambda: m.require(not (work / 'CORRUPT_MUST_NOT_EXECUTE').exists(), 'corrupt archival execution began'))
    empty = clone_package('extra-empty-directory'); (empty / 'EMPTY').mkdir()
    invocation_check('unlisted empty directory rejected', ['verify', external_pin, '--root', empty, '--verify-only'], expected_rc=1)
    wrong_type = clone_package('boolean-byte-count'); data = m.strict_json((wrong_type / 'package_index.json').read_bytes()); data['files'][0]['bytes'] = True
    raw = enc(data); replace_bytes(wrong_type / 'package_index.json', raw)
    invocation_check('boolean inventory bytes rejected', ['verify', m.sha(raw), '--root', wrong_type, '--verify-only'], expected_rc=1)
    link = clone_package('symlink-input'); target = link / 'note.tex'; target.unlink(); target.symlink_to(package / 'note.tex')
    invocation_check('symlink input rejected', ['verify', external_pin, '--root', link, '--verify-only'], expected_rc=1)
    alias = work / 'package-link'; alias.symlink_to(package, target_is_directory=True)
    invocation_check('symlink root rejected', ['verify', external_pin, '--root', alias, '--verify-only'], expected_rc=1)
    mismatch = dict(current_blobs); mismatch['note.tex'] += b'% OUTER COPY MISMATCH\n'; raw = index_current(mismatch); mismatch['CURRENT_PUBLICATION_MANIFEST.json'] = raw
    mismatch_root = work / 'current-copy-mismatch'; m.materialize(mismatch_root, mismatch)
    invocation_check('reindexed current TeX mismatch rejected', ['current', m.sha(raw), '--root', mismatch_root, '--verify-only'], expected_rc=1)
    bad_pdf = dict(current_blobs); bad_pdf['post-lie-note.pdf'] = b'NOT PDF'; raw = index_current(bad_pdf); bad_pdf['CURRENT_PUBLICATION_MANIFEST.json'] = raw
    bad_pdf_root = work / 'current-bad-header'; m.materialize(bad_pdf_root, bad_pdf)
    invocation_check('current bad PDF header rejected', ['current', m.sha(raw), '--root', bad_pdf_root, '--verify-only'], expected_rc=1)
    bad_zip = dict(current_blobs); bad_zip['post-lie-verification.zip'] += b'TRAILER'; raw = index_current(bad_zip); bad_zip['CURRENT_PUBLICATION_MANIFEST.json'] = raw
    bad_zip_root = work / 'current-bad-zip'; m.materialize(bad_zip_root, bad_zip)
    invocation_check('reindexed current ZIP trailer rejected', ['current', m.sha(raw), '--root', bad_zip_root, '--verify-only'], expected_rc=1)
    for label, raw in [('duplicate JSON keys', b'{"x":1,"x":2}'), ('NaN JSON', b'{"x":NaN}'), ('positive Infinity JSON', b'{"x":Infinity}'), ('negative Infinity JSON', b'{"x":-Infinity}'), ('overflow JSON float', b'{"x":1e999}')]:
        reject(label, lambda raw=raw: m.strict_json(raw))
    for name in ('../x', '/x', 'a/../b', 'a//b', './x', 'a/./b', 'a\\b', 'a/', 'a:stream', 'a\x00b'):
        reject('unsafe path ' + repr(name), lambda name=name: m.safe_name(name))
    row = lambda name: {'path': name, 'bytes': 0, 'sha256': '0' * 64}
    reject('case-aliased leaf inventory', lambda: m.rows_map([row('A.txt'), row('a.txt')]))
    reject('case-aliased directory inventory', lambda: m.rows_map([row('A/a.txt'), row('a/b.txt')]))
    reject('file directory collision', lambda: m.rows_map([row('a'), row('a/b')]))
    reject('duplicate identical inventory path', lambda: m.rows_map([row('a'), row('a')]))
    reject('unexpected row property', lambda: m.rows_map([{**row('a'), 'extra': 1}]))
    reject('float byte count', lambda: m.rows_map([{**row('a'), 'bytes': 0.0}]))
    reject('uppercase digest rejected', lambda: m.rows_map([{**row('a'), 'sha256': 'A' * 64}]))
    fifo_root = work / 'fifo-tree'; fifo_root.mkdir(); os.mkfifo(fifo_root / 'a')
    reject('FIFO rejected as input tree', lambda: m.closed_tree(fifo_root, {'a'}))
    reject('FIFO bounded read rejects before blocking', lambda: m.read_regular(fifo_root / 'a'))
    expected = {'a.txt': b'hello'}; raw = m.deterministic_zip(expected)
    check('strict raw ZIP positive', lambda: m.zip_payloads(raw, expected, generated=True))
    reject('ZIP trailer', lambda: m.zip_payloads(raw + b'X', expected, generated=True))
    reject('ZIP prefix', lambda: m.zip_payloads(b'X' + raw, expected, generated=True))
    reject('ZIP truncation', lambda: m.zip_payloads(raw[:-1], expected, generated=True))
    wrong_name = bytearray(raw); wrong_name[30] = ord('b')
    reject('ZIP local central filename mismatch', lambda: m.zip_payloads(bytes(wrong_name), expected, generated=True))
    wrong_mode = bytearray(raw); central = struct.unpack_from('<I', raw, len(raw) - 6)[0]; struct.pack_into('<I', wrong_mode, central + 38, (stat.S_IFLNK | 0o777) << 16)
    reject('ZIP symlink mode', lambda: m.zip_payloads(bytes(wrong_mode), expected, generated=True))
    # Insert one byte INSIDE the declared DEFLATE region and update all extents.
    compressed_size = struct.unpack_from('<I', raw, 18)[0]
    suffix = bytearray(raw[:central] + b'X' + raw[central:]); new_central = central + 1
    struct.pack_into('<I', suffix, 18, compressed_size + 1)
    struct.pack_into('<I', suffix, new_central + 20, compressed_size + 1)
    struct.pack_into('<I', suffix, len(suffix) - 6, new_central)
    reject('ZIP declared compressed unused suffix', lambda: m.zip_payloads(bytes(suffix), expected, generated=True), 'raw DEFLATE exact-consumption')
    options = argparse.Namespace(primary_dir=None, catalog=None, problems=None, reports=None)
    for directory in (package, package / 'source', package / 'source/authored', package / 'source/audits', package / 'root_evidence'):
        reject('physical output guard ' + directory.relative_to(base).as_posix(), lambda directory=directory: m.fresh_target(package, blobs, directory / 'post-lie-verification.zip', options, 'post-lie-verification.zip'))
    case_path = package.parent / package.name.swapcase()
    if case_path.exists() and case_path.stat().st_ino == package.stat().st_ino:
        reject('APFS case alias physical output guard', lambda: m.fresh_target(package, blobs, case_path / 'source' / 'post-lie-verification.zip', options, 'post-lie-verification.zip'))
    else:
        record('APFS case alias physical output guard', 'NOT_APPLICABLE', {'reason': 'filesystem is case sensitive'})
    # An in-process trap independently proves the verify-only path calls no replay.
    original_replay = m.replay
    def forbidden(*unused): raise RuntimeError('ARCHIVAL_REPLAY_FORBIDDEN')
    m.replay = forbidden
    verify_options = argparse.Namespace(verify_only=True, receipt_dir=None, primary_dir=None, catalog=None, problems=None, reports=None)
    check('verify-only independent replay trap', lambda: m.verify_result(package, blobs, external_pin, verify_options)['replay'])
    m.replay = original_replay
    values = [args.catalog, args.problems, args.reports]
    if all(v is not None for v in values):
        tail = ['source-only', '--catalog', args.catalog, '--problems', args.problems, '--reports', args.reports]
        if args.primary_dir is not None: tail += ['--primary-dir', args.primary_dir]
        invocation_check('complete native source-only with optional primary', tail)
        seen = []
        old_stream, old_json = m.stream_pin, m.strict_json
        def tracked_stream(path, size, expected):
            result = old_stream(path, size, expected); seen.append('FULL_PIN'); return result
        def tracked_json(raw):
            m.require(seen[:3] == ['FULL_PIN'] * 3 and len(seen) >= 3, 'parsed native data before all complete pins')
            seen.append('PARSE'); return old_json(raw)
        m.stream_pin = tracked_stream; m.strict_json = tracked_json
        check('native all three pins precede first parse independently instrumented', lambda: m.source_only(values)['canonical_pair'])
        m.stream_pin, m.strict_json = old_stream, old_json
    else:
        record('complete native source-only', 'NOT_RUN', {'reason': 'supply all three explicit corpus paths'})
    if args.primary_dir is not None:
        check('optional closed primary set', lambda: m.primary_only(args.primary_dir))
        extra_primary = work / 'primary-extra'; extra_primary.mkdir()
        for name in m.PRIMARY_PINS:
            os.link(args.primary_dir / name, extra_primary / name)
        (extra_primary / 'EXTRA').write_bytes(b'not allowed')
        reject('optional primary unlisted extra rejected', lambda: m.primary_only(extra_primary))
    summary = {'schema': 'post-lie-30005737-tool-regression-v1', 'started_utc': started,
               'ended_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS' if all(r['outcome'] != 'FAIL' for r in results) else 'FAIL',
               'tests': results, 'passed': sum(r['outcome'] == 'PASS' for r in results), 'failed': sum(r['outcome'] == 'FAIL' for r in results),
               'not_run': sum(r['outcome'] in ('NOT_RUN', 'NOT_APPLICABLE') for r in results),
               'tool': m.pin_bytes((base / 'portable.py').read_bytes()), 'package_index_sha256': external_pin,
               'archive': m.pin_bytes(builds[0].read_bytes()), 'current_fixture_manifest_sha256': current_pin,
               'fixture_status': 'NOT ACTUAL PAPER; PDF HEADER ONLY', 'original_effort': '1/5',
               'scope': m.SCOPE, 'raw_process_evidence': 'Retained in the selected private audit directory; paths and raw bodies omitted here.'}
    (work / 'REGRESSION_RESULTS.json').write_bytes(enc(summary))
    print(json.dumps({'status': summary['status'], 'passed': summary['passed'], 'failed': summary['failed'], 'not_run': summary['not_run']}, sort_keys=True))
    return 0 if summary['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
