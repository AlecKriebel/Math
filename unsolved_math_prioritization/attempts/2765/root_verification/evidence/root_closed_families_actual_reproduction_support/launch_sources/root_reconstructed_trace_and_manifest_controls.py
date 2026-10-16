#!/usr/bin/env python3
"""Actual root controls for definitions whose original runner was not retained.

This code does not represent itself as the missing historical snippet. It
reconstructs saved trace mutation definitions exactly, checks stored mutant
bytes, and runs fresh closed-manifest mutations against all three families.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--pins', type=Path, required=True)
    parser.add_argument('--output-directory', type=Path, required=True)
    args = parser.parse_args()
    assert not sys.flags.optimize
    pins = json.loads(args.pins.read_bytes())
    audit = args.repo.resolve()/pins['audit_relative_path']
    output = args.output_directory.resolve()
    output.mkdir(parents=True, exist_ok=False)
    sha = lambda data: hashlib.sha256(data).hexdigest()
    load = lambda path: json.loads(path.read_bytes())
    now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    save = lambda path, value: path.write_text(json.dumps(value, indent=2)+'\n')

    def run(label, script, cwd, *arguments):
        start = now()
        command = ['/usr/bin/python3', str(script), *map(str, arguments)]
        process = subprocess.run(command, cwd=cwd, capture_output=True, timeout=120)
        streams = output/'streams'
        streams.mkdir(exist_ok=True)
        for channel in ['stdout', 'stderr']:
            (streams/(label+'.'+channel)).write_bytes(getattr(process, channel))
        return process, {'label': label, 'started_utc': start, 'command': command,
                         'cwd': str(cwd), 'exit_code': process.returncode,
                         'script_sha256': sha(script.read_bytes()),
                         'stdout': 'streams/'+label+'.stdout', 'stdout_sha256': sha(process.stdout),
                         'stderr': 'streams/'+label+'.stderr', 'stderr_sha256': sha(process.stderr)}

    trace = audit/'trace_geometry_family'
    definitions = load(trace/'replay_and_corruption_receipts.json')['runs']
    trace_runs, mutation_mapping = [], []
    for definition in definitions:
        label = definition['label']
        if label == 'geometry_controls':
            script = trace/'geometry_controls.py'
        elif 'mutation_old' not in definition:
            script = trace/'originals'/('verify.py' if label == 'author' else 'independent_checks.py')
        else:
            original = trace/'originals'/('verify.py' if label.startswith('author_') else 'independent_checks.py')
            before = original.read_bytes()
            old, new = definition['mutation_old'].encode(), definition['mutation_new'].encode()
            assert before.count(old) == 1, label
            after = before.replace(old, new)
            script = trace/'mutants'/(label+'.py')
            assert script.read_bytes() == after and sha(after) == definition['script_sha256']
            mutation_mapping.append({'label': label, 'source_path': str(original), 'source_sha256': sha(before),
                                     'exact_old': old.decode(), 'exact_new': new.decode(),
                                     'stored_mutant_path': str(script), 'stored_mutant_sha256': sha(after),
                                     'generated_bytes_equal_stored': True})
        process, row = run(label, script, trace)
        # Match the saved receipt's label/stream interface while the actual
        # capture ledger retains the distinct root execution command and clock.
        row['label'] = label
        if 'mutation_old' in definition:
            assert process.returncode == 1 and not process.stdout
            marker = definition['expected_rejection']
            assert ('AssertionError: '+marker).encode() in process.stderr
            assert b'ModuleNotFoundError' not in process.stderr
            row.update(mutation_old=definition['mutation_old'], mutation_new=definition['mutation_new'],
                       expected_rejection=marker, rejected_as_expected=True)
        else:
            assert process.returncode == 0 and not process.stderr
            expected = (audit/'source_snapshot'/('verification.json' if label == 'author'
                        else 'review/independent_results.json')) if label != 'geometry_controls' else trace/'streams/geometry_controls.stdout'
            assert process.stdout == expected.read_bytes() and json.loads(process.stdout) == load(expected)
            packet = json.loads(process.stdout)
            assert packet['assertions'] == (30 if label == 'author' else 72 if label == 'historical_independent' else 25)
            row['assertions'] = packet['assertions']
            if label != 'geometry_controls':
                row.update(source_equal_bytes=script.read_bytes() == (audit/'source_snapshot'/('verify.py' if label == 'author' else 'review/independent_checks.py')).read_bytes(),
                           expected_receipt=str(expected), receipt_byte_identical=True)
            else:
                row['scope'] = 'independent exact audit controls only'
                # The historical geometry row had no clock/cwd fields.
                row.pop('started_utc'); row.pop('cwd')
        trace_runs.append(row)
        save(output/'trace_replay_receipts.json', {'runtime': '/usr/bin/python3', 'runs': trace_runs})
    save(output/'trace_mutation_source_mapping.json', mutation_mapping)

    manifest_rows = []
    for family, info in pins['families'].items():
        # The baseline clone is the exact sealed tree, before writer replay.
        source = audit/family
        assert len(info['members']) == info['member_count']
        validator = 'verify_family_manifest.py' if family == 'primary_scope_family' else 'verify_manifest.py'
        for case in ['baseline', 'missing', 'extra', 'same_size_hash', 'exclusion_cheat', 'unsafe_path', 'symlink',
                     'nested_manifest_extra', 'nested_ignoredtmp_extra']:
            clone = output/'manifest_cases'/family/case
            clone.mkdir(parents=True, exist_ok=False)
            for member in info['members']+[info['manifest']]:
                target = clone/member['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source/member['path'], target)
            manifest = clone/info['manifest_name']
            old_manifest = manifest.read_bytes()
            packet = json.loads(old_manifest)
            key = 'authored_files' if family == 'current_measure_family' else 'files'
            victim_name = next(x['path'] for x in info['members'] if x['size'] > 0 and x['path'] != validator)
            victim = clone/victim_name
            before = victim.read_bytes()
            mutation = {'case': case, 'family': family, 'sealed_manifest_sha256': sha(old_manifest),
                        'victim_path': victim_name, 'victim_before_sha256': sha(before)}
            if case == 'missing':
                victim.unlink()
            elif case == 'extra':
                (clone/'ROOT_UNLISTED_NEGATIVE.txt').write_bytes(b'Actual extra first-party manifest control.\n')
            elif case == 'same_size_hash':
                victim.write_bytes(bytes([before[0] ^ 1])+before[1:])
                assert victim.stat().st_size == len(before)
            elif case == 'exclusion_cheat':
                if family == 'current_measure_family':
                    packet[key] = [x for x in packet[key] if x['path'] != victim_name]
                else:
                    packet['excluded'].append(victim_name)
                save(manifest, packet)
            elif case == 'unsafe_path':
                packet[key][0]['path'] = '../ROOT_UNSAFE_PATH.txt'
                save(manifest, packet)
            elif case == 'symlink':
                victim.unlink()
                victim.symlink_to(source/victim_name)
            elif case == 'nested_manifest_extra':
                nested = clone/'nested'/info['manifest_name']
                nested.parent.mkdir()
                nested.write_bytes(b'Actual nested same-basename extra-file control.\n')
            elif case == 'nested_ignoredtmp_extra':
                nested = clone/'nested/ignoredtmp/ROOT_UNLISTED_NEGATIVE.txt'
                nested.parent.mkdir(parents=True)
                nested.write_bytes(b'Actual nested ignoredtmp extra-file control.\n')
            # current_measure validator also reads parent/snapshot_manifest.
            shutil.copy2(audit/'snapshot_manifest.json', clone.parent/'snapshot_manifest.json')
            # Bind the actual changed inputs before validation, so a failed
            # outer assertion cannot erase the input that produced its stream.
            for name in [info['manifest_name'], victim_name, 'ROOT_UNLISTED_NEGATIVE.txt',
                         'nested/'+info['manifest_name'], 'nested/ignoredtmp/ROOT_UNLISTED_NEGATIVE.txt']:
                path = clone/name
                if path.is_file() and not path.is_symlink():
                    destination = output/'actual_control_inputs'/family/case/name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, destination)
            save(output/'last_control_definition.json', mutation)
            process, row = run('manifest_'+family+'_'+case, clone/validator, clone)
            passed = case == 'baseline' or (family == 'primary_scope_family' and case in
                                            ['nested_manifest_extra', 'nested_ignoredtmp_extra'])
            assert (process.returncode == 0) == passed
            assert b'ModuleNotFoundError' not in process.stderr
            if passed:
                assert not process.stderr
                if family == 'trace_geometry_family':
                    marker = 'PASS: exact closed coverage, hashes and sizes.'
                    assert process.stdout.decode().strip() == marker
                else:
                    packet_stdout = json.loads(process.stdout)
                    assert packet_stdout['status'] == 'PASS'
                    count_key = 'file_count' if family == 'primary_scope_family' else 'authored_count'
                    assert packet_stdout[count_key] == info['member_count']
                    assert packet_stdout['manifest_sha256'] == info['manifest']['sha256']
                    marker = 'PASS: exact pinned final manifest and member count'
            else:
                assert process.returncode == 1 and process.stderr
                if family == 'primary_scope_family':
                    marker = {'same_size_hash': 'exact SHA256 '+victim_name,
                              'exclusion_cheat': 'strict exclusions', 'symlink': 'file safety'}.get(case, 'complete authored path coverage')
                elif family == 'current_measure_family':
                    marker = 'symlink not allowed:' if case == 'symlink' else 'missing/extra/altered authored files'
                else:
                    marker = {'missing': 'missing_or_nonregular_file', 'same_size_hash': 'hash_mismatch',
                              'exclusion_cheat': 'exclusion_policy', 'unsafe_path': 'unsafe_path',
                              'symlink': 'missing_or_nonregular_file'}.get(case, 'closed_coverage_mismatch')
                assert marker.encode() in process.stderr, 'Wrong rejection mechanism: '+family+' '+case
            # Strong root closure excludes only the exact root manifest and
            # root cache subtree. The closed primary verifier has broader
            # basename/any-component exclusions; preserve that actual limit.
            guard_error = None
            try:
                assert sha(manifest.read_bytes()) == info['manifest']['sha256'], 'Pinned manifest bytes changed'
                listed = packet[key]
                names = [x['path'] for x in listed]
                assert len(names) == len(set(names))
                for item in listed:
                    path = Path(item['path'])
                    assert not path.is_absolute() and '..' not in path.parts
                    target = clone/path
                    assert target.is_file() and not target.is_symlink()
                    data = target.read_bytes()
                    assert len(data) == item.get('size', item.get('bytes')) and sha(data) == item['sha256']
                actual = []
                for path in clone.rglob('*'):
                    name = path.relative_to(clone).as_posix()
                    if name == info['manifest_name'] or path.relative_to(clone).parts[0] == info['cache_prefix']:
                        continue
                    assert not path.is_symlink()
                    if path.is_file():
                        actual.append(name)
                assert sorted(actual) == sorted(names)
            except AssertionError as error:
                guard_error = type(error).__name__+': '+str(error)
            assert (guard_error is None) == (case == 'baseline')
            mutation.update(manifest_after_sha256=sha(manifest.read_bytes()),
                            victim_after_sha256=sha(victim.read_bytes()) if victim.is_file() and not victim.is_symlink() else None,
                            mutation_definition='Exact sealed baseline; apply the named one-file/manifest/path mutation. This root implementation is new, not a preserved historical snippet.',
                            expected_pass=passed, actual_pass=process.returncode == 0,
                            expected_output_marker=marker,
                            strict_root_guard_pass=guard_error is None, strict_root_guard_failure=guard_error,
                            administrative_guard_qualification='Original primary broad exclusion accepts nested manifest/ignoredtmp extras; strict root closure rejects them. No scientific source or closed family is changed.' if passed and case != 'baseline' else None)
            row.update(mutation)
            manifest_rows.append(row)
            save(output/'manifest_reconstruction_receipts.json', manifest_rows)
    save(output/'reconstruction_contract.json', {
        'historical_missing_runner_limit': 'Trace replay/manifest controls were immediate snippets; exact saved mutation definitions and stored sources are replayed. Primary/current manifest mutation runner text is not preserved, so their fresh root controls establish the documented mechanisms only.',
        'trace_source_map': 'trace_mutation_source_mapping.json', 'trace_actual_receipt': 'trace_replay_receipts.json',
        'manifest_actual_receipt': 'manifest_reconstruction_receipts.json',
        'prose_limit': 'False prose packets are executed by the unchanged current_measure helper; finite PASS does not certify their false mathematics. Root proof reading remains separate.',
        'new_substantive_attempts': 0})
    print(json.dumps({'trace_runs': len(trace_runs), 'manifest_runs': len(manifest_rows),
                      'actual_root_reconstruction': True, 'historical_execution_claim': False}, indent=2))


if __name__ == '__main__':
    main()
