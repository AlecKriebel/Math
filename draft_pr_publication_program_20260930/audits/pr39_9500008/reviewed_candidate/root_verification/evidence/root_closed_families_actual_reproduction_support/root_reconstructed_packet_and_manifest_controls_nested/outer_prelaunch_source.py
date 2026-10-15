#!/usr/bin/env python3
"""Fresh actual root packet/manifest controls with explicit reconstruction labels.

This is retained new replay machinery, never the historical immediate snippet.
The original packet checker and each closed manifest validator run unchanged.
Foreign staged primary PDFs are read-only inputs; only their mutation hash and
result streams enter support, never their copied bodies.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
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
    pins = json.loads(args.pins.read_bytes()); audit = args.repo.resolve()/pins['audit_relative_path']
    output = args.output_directory.resolve(); output.mkdir(parents=True, exist_ok=False)
    sha = lambda data: hashlib.sha256(data).hexdigest()
    load = lambda path: json.loads(path.read_bytes())
    save = lambda path, value: path.write_text(json.dumps(value, indent=2)+'\n')
    runs = []

    def run(label, script, *arguments, expected=0):
        argv = ['/usr/bin/python3', str(script), *map(str, arguments)]
        result = subprocess.run(argv, cwd=args.repo, capture_output=True, timeout=180)
        streams = output/'streams'; streams.mkdir(exist_ok=True)
        for channel in ['stdout', 'stderr']: (streams/(label+'.'+channel)).write_bytes(getattr(result, channel))
        row = {'label': label, 'argv': argv, 'exit_code': result.returncode, 'expected_exit': expected,
               'source_sha256': sha(script.read_bytes()), 'stdout_sha256': sha(result.stdout), 'stderr_sha256': sha(result.stderr),
               'stdout': 'streams/'+label+'.stdout', 'stderr': 'streams/'+label+'.stderr', 'observed_expected': result.returncode == expected}
        runs.append(row); save(output/'CONTROL_RUNS.json', runs)
        assert result.returncode == expected, label
        assert b'ModuleNotFoundError' not in result.stderr, 'Wrong rejection mechanism: '+label
        return result, row

    def writable(path): path.chmod(0o644)

    packet_rows = []
    checker = audit/'primary_scope_family/check_original_packet.py'
    baseline, row = run('packet_baseline', checker)
    assert load(audit/'source_snapshot/source_record.json') == load(audit/'primary_scope_family/raw_source_record.json')
    assert json.loads(baseline.stdout)['passed'] is True
    packet_rows.append({**row, 'control': 'actual_original_baseline'})
    for case in ['source_statement_narrowed', 'source_actual_report_erased', 'budget_six_attempts', 'code_rotation_corrupted']:
        target = output/'packet_cases'/case; shutil.copytree(audit/'source_snapshot', target)
        mutation = {'control': case, 'definition_origin': 'Exact mechanism in closed primary run_negative_controls.py; fresh root implementation.', 'historical_execution_claim': False}
        if case == 'source_statement_narrowed':
            path = target/'source_record.json'; value = load(path); value['statement'] += ' Assume that the stopped pairs are identically distributed.'
            before = path.read_bytes(); writable(path); save(path, value)
        elif case == 'source_actual_report_erased':
            path = target/'prior_report.json'; before = path.read_bytes(); writable(path); save(path, {})
        elif case == 'budget_six_attempts':
            path = target/'turns.json'; before = path.read_bytes(); value = load(path); value['count'] = 6
            value['attempts'] = [{'number': n, 'route': 'extra unsupported route', 'outcome': 'unresolved', 'gap': 'not proved'} for n in range(1,7)]
            writable(path); save(path, value)
            ready = target/'readiness.json'; value = load(ready); value['budget']['used'] = 6; writable(ready); save(ready, value)
        else:
            path = target/'review/independent_checks.py'; before = path.read_bytes()
            assert before.count(b'rot=a+d-e') == 1; writable(path); path.write_bytes(before.replace(b'rot=a+d-e', b'rot=a+d+e', 1))
        mutation.update(mutated_path=path.relative_to(target).as_posix(), before_sha256=sha(before), after_sha256=sha(path.read_bytes()))
        # Actual mutated first-party inputs precede any attempted validation.
        destination = output/'actual_control_inputs/packet'/case/path.relative_to(target); destination.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(path, destination)
        if case == 'budget_six_attempts': shutil.copy2(target/'readiness.json', destination.parent/'readiness.json')
        save(output/'last_control_definition.json', mutation)
        if case == 'code_rotation_corrupted':
            corrupt, code_row = run('packet_actual_corrupt_rotation', path, expected=1)
            assert b'AssertionError: rotation_difference' in corrupt.stderr and not corrupt.stdout
            packet_rows.append({**code_row, 'control': 'actual_corrupt_code_execution', **mutation})
        rejected, row = run('packet_'+case, checker, target, expected=1)
        assert json.loads(rejected.stdout)['passed'] is False
        expected_reason = {'source_statement_narrowed': 'source full record differs', 'source_actual_report_erased': 'prior full report differs',
                           'budget_six_attempts': 'attempt limit exceeded', 'code_rotation_corrupted': 'original byte identity mismatch'}[case]
        assert expected_reason in json.loads(rejected.stdout)['reason'], case
        packet_rows.append({**row, **mutation, 'expected_rejection_reason': expected_reason})
        save(output/'PACKET_CONTROL_RESULTS.json', packet_rows)

    def guard(root, info):
        assert sha((root/info['manifest_name']).read_bytes()) == info['manifest']['sha256'], 'Pinned manifest changed'
        expected = info['members']+info['foreign_members']; names = [x['path'] for x in expected]
        assert len(names) == len(set(names))
        for item in expected:
            name = PurePosixPath(item['path']); assert not name.is_absolute() and '..' not in name.parts and name.as_posix() == item['path']
            path = root/name; assert path.is_file() and not path.is_symlink(), 'Missing/nonregular member'
            data = path.read_bytes(); assert len(data) == item['size'] and sha(data) == item['sha256'], 'Member bytes changed'
        actual = []
        for path in root.rglob('*'):
            rel = path.relative_to(root); assert not path.is_symlink(), 'Symlink rejected'
            if rel.as_posix() == info['manifest_name'] or (info['cache_prefix'] and rel.parts[0] == info['cache_prefix']): continue
            if path.is_file(): actual.append(rel.as_posix())
        assert sorted(actual) == sorted(names), 'Exact root membership changed'

    manifest_rows = []
    for family, info in pins['families'].items():
        source = audit/family
        validator, arguments = {'primary_scope_family': ('check_family_manifest.py', ['verify']),
                                'rotation_concatenation_family': ('manifest.py', ['check']),
                                'uniform_error_scaling_family': ('manifest_integrity.py', [])}[family]
        cases = ['baseline', 'missing', 'extra', 'same_size_hash', 'exclusion_cheat', 'unsafe_path', 'symlink', 'nested_manifest_extra', 'nested_foreign_component_extra']
        if family == 'primary_scope_family': cases.append('foreign_pdf_corrupted')
        for case in cases:
            clone = output/'manifest_cases'/family/case; clone.mkdir(parents=True, exist_ok=False)
            for item in info['members']+info['foreign_members']+[info['manifest']]:
                destination = clone/item['path']; destination.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source/item['path'], destination)
            manifest = clone/info['manifest_name']; old_manifest = manifest.read_bytes(); packet = json.loads(old_manifest)
            victim_name = next(x['path'] for x in info['members'] if x['size'] > 0 and x['path'].endswith('.md'))
            victim = clone/victim_name; before = victim.read_bytes(); changed = []
            definition = {'case': case, 'family': family, 'victim_path': victim_name, 'victim_before_sha256': sha(before),
                          'sealed_manifest_sha256': sha(old_manifest), 'historical_execution_claim': False, 'definition_origin': 'Fresh root exact closed-tree mutation.'}
            if case == 'missing': victim.unlink()
            elif case == 'extra':
                path = clone/'ROOT_UNLISTED_NEGATIVE.txt'; path.write_bytes(b'Actual extra first-party control.\n'); changed.append(path)
            elif case == 'same_size_hash': writable(victim); victim.write_bytes(bytes([before[0]^1])+before[1:]); changed.append(victim)
            elif case in ['exclusion_cheat', 'unsafe_path']:
                if family == 'primary_scope_family':
                    if case == 'exclusion_cheat': packet['self_exclusion_exact_relative_path'] = victim_name
                    else: packet['first_party_members']['../ROOT_UNSAFE_PATH.txt'] = packet['first_party_members'].pop(victim_name)
                elif family == 'rotation_concatenation_family':
                    if case == 'exclusion_cheat': packet['files'] = [x for x in packet['files'] if x['path'] != victim_name]
                    else: packet['files'][0]['path'] = '../ROOT_UNSAFE_PATH.txt'
                else:
                    if case == 'exclusion_cheat': packet['exclude_files'].append(victim_name)
                    else: packet['files'][0]['path'] = '../ROOT_UNSAFE_PATH.txt'
                writable(manifest); save(manifest, packet); changed.append(manifest)
            elif case == 'symlink': victim.unlink(); victim.symlink_to(source/victim_name)
            elif case == 'nested_manifest_extra':
                path = clone/'nested'/info['manifest_name']; path.parent.mkdir(); path.write_bytes(b'Nested same-basename extra control.\n'); changed.append(path)
            elif case == 'nested_foreign_component_extra':
                component = info['cache_prefix'] or 'foreign_sources'
                path = clone/'nested'/component/'ROOT_UNLISTED_NEGATIVE.txt'; path.parent.mkdir(parents=True); path.write_bytes(b'Nested foreign-component extra control.\n'); changed.append(path)
            elif case == 'foreign_pdf_corrupted':
                item = next(x for x in info['foreign_members'] if x['path'].startswith('foreign_sources/') and x['path'].endswith('.pdf'))
                path = clone/item['path']; data = path.read_bytes(); writable(path); path.write_bytes(bytes([data[0]^1])+data[1:])
                definition['foreign_mutation'] = {'path': item['path'], 'before_sha256': sha(data), 'after_sha256': sha(path.read_bytes()), 'bytes': len(data), 'body_retained_in_support': False}
            # No foreign source body enters the first-party control directory.
            for path in changed:
                destination = output/'actual_control_inputs/manifests'/family/case/path.relative_to(clone); destination.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(path, destination)
            save(output/'last_control_definition.json', definition)
            result, row = run('manifest_'+family+'_'+case, clone/validator, *arguments, expected=0 if case == 'baseline' else 1)
            if case == 'baseline':
                assert not result.stderr
                value = json.loads(result.stdout); assert value.get('passed', value.get('verified')) is True
                count = value.get('first_party_members', value.get('recursive_file_count', value.get('files')))
                assert count == info['member_count']
            else:
                if family == 'primary_scope_family':
                    marker = {'same_size_hash': 'Byte seal mismatch:', 'foreign_pdf_corrupted': 'Byte seal mismatch:',
                              'exclusion_cheat': 'Unexpected self exclusion', 'symlink': 'Unexpected symlink:'}.get(case, 'Exact membership mismatch:')
                    rejected = json.loads(result.stdout)
                    assert rejected['passed'] is False and marker in rejected['reason'], (family, case)
                elif family == 'rotation_concatenation_family':
                    marker = 'Unexpected symlink:' if case == 'symlink' else 'Missing, added, or changed first-party files'
                    assert marker.encode() in result.stderr, (family, case)
                else:
                    marker = {'same_size_hash': 'HASH_OR_SIZE_MISMATCH', 'exclusion_cheat': 'EXCLUSION_CHEAT_FILES',
                              'unsafe_path': 'UNSAFE_PATH', 'symlink': 'SYMLINK:'}.get(case, 'CLOSURE_MISSING_OR_EXTRA')
                    assert marker.encode() in result.stderr, (family, case)
                definition['expected_rejection_marker'] = marker
            error = None
            try: guard(clone, info)
            except AssertionError as exc: error = str(exc)
            assert (error is None) == (case == 'baseline'), (family, case)
            definition.update(actual_exit_code=result.returncode, expected_exit_code=0 if case == 'baseline' else 1,
                              strict_root_guard_pass=error is None, strict_root_guard_failure=error,
                              manifest_after_sha256=sha(manifest.read_bytes()), victim_after_sha256=sha(victim.read_bytes()) if victim.is_file() and not victim.is_symlink() else None)
            manifest_rows.append({**row, **definition}); save(output/'MANIFEST_CONTROL_RESULTS.json', manifest_rows)
    save(output/'RECONSTRUCTION_CONTRACT.json', {'status': 'ACTUAL_ROOT_CONTROLS_COMPLETED', 'packet_runs': len(packet_rows), 'manifest_runs': len(manifest_rows),
        'historical_execution_claim': False, 'original_checkers_unchanged': True, 'mutations_execute_actual_rejection_paths': True,
        'foreign_source_bodies_retained_in_support': False, 'new_substantive_attempts': 0, 'scope': 'Finite source/accounting/code and strict manifest controls only; no general proof or new Brownian target attempt.'})
    print(json.dumps({'packet_runs': len(packet_rows), 'manifest_runs': len(manifest_rows), 'actual_root_reconstruction': True, 'historical_execution_claim': False}, indent=2))


if __name__ == '__main__': main()
