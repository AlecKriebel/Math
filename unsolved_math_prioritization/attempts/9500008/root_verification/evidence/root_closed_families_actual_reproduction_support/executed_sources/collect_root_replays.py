#!/usr/bin/env python3
"""Root-owned ACTUAL PR39 reproduction. Preparation alone proves no run succeeded.

Read this entire source and the companion sources before root execution.
All writer helpers execute in a private exact hierarchy. Retained support holds
first-party evidence only. Private attempts survive for failure inspection and
are never automatically deleted or used as CURRENT dependency anchors.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import traceback

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = AUDIT.parents[2]
PYTHON = '/usr/bin/python3'
CLOCK_KEYS = {'utc', 'time_utc', 'at', 'started_utc', 'ended_utc'}
NATIVE = 'unsolved_math_prioritization/'
REQUIRED_CURRENT = {NATIVE+name for name in ['QUEUE.md', 'state.json', 'history.jsonl',
    'catalog.json', 'assessments.json', 'queue.py', 'policy.json', 'manifest.json',
    'cache/problems.json', 'cache/research_results.json', 'cache/catalog.sqlite',
    'review_v2/related_target_groups.json']} | {'draft_pr_publication_program_20260930/inventory.json'}
SOURCE_NAMES = ['collect_root_replays.py', 'capture_runner.py', 'inspect_source_native.py',
                'reconstructed_controls.py', 'INPUT_PINS.json', 'README.md', 'RESEARCH_LOG.md',
                'REPLAY_CONTRACT.md', 'ADAPTATION_BASIS.json']
SOURCE_MANIFEST_NAME = 'PREPARATION_MANIFEST.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(Path(path).read_bytes())


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def row(path, root):
    data = Path(path).read_bytes()
    return {'path': Path(path).relative_to(root).as_posix(), 'size': len(data), 'sha256': sha(data)}


def require(record, root):
    name = record['path']
    path = PurePosixPath(name)
    assert name and not path.is_absolute() and '..' not in path.parts and path.as_posix() == name
    target = root/name
    assert target.is_file() and not target.is_symlink(), name
    assert row(target, root) == record, 'Pinned input changed: '+name


def strict_closed(pins, audit):
    summary = {}
    for family, info in pins['families'].items():
        directory = audit/family
        records = info['members']+info['foreign_members']
        for record in records+[info['manifest']]: require(record, directory)
        assert len(info['members']) == info['member_count']
        expected = sorted(record['path'] for record in records)
        assert len(expected) == len(set(expected))
        actual = []
        for path in directory.rglob('*'):
            relative = path.relative_to(directory)
            assert not path.is_symlink(), 'Strict closure rejects symlink: '+str(path)
            if relative.as_posix() == info['manifest_name'] or (info['cache_prefix'] and relative.parts[0] == info['cache_prefix']): continue
            if path.is_file(): actual.append(relative.as_posix())
        assert sorted(actual) == expected, 'Strict root recursive coverage: '+family
        summary[family] = {'manifest_path': str((directory/info['manifest_name']).relative_to(AUDIT)),
            'manifest_sha256': info['manifest']['sha256'], 'member_count': info['member_count'],
            'foreign_member_count': len(info['foreign_members']), 'cache_prefix': info['cache_prefix'],
            'exact_root_manifest_self_exclusion': info['manifest_name'], 'strict_recursive_coverage': True}
    assert sum(x['member_count'] for x in summary.values()) == 732
    assert sum(x['foreign_member_count'] for x in summary.values()) == 40
    return summary


def strict_preparation():
    manifest = HERE/SOURCE_MANIFEST_NAME
    packet = load(manifest)
    assert packet['excluded'] == [SOURCE_MANIFEST_NAME]
    records = packet['files']
    assert sorted(x['path'] for x in records) == sorted(SOURCE_NAMES)
    for record in records: require(record, HERE)
    actual = sorted(path.relative_to(HERE).as_posix() for path in HERE.rglob('*')
                    if path.is_file() and path != manifest)
    assert actual == sorted(SOURCE_NAMES)
    assert not any(path.is_symlink() for path in HERE.rglob('*'))
    return sha(manifest.read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-input-manifest', type=Path, required=True)
    parser.add_argument('--root-script-path', type=Path, required=True)
    parser.add_argument('--root-script-sha256', required=True)
    parser.add_argument('--root-primary-read-ledger', type=Path, required=True)
    parser.add_argument('--root-primary-read-ledger-sha256', required=True)
    parser.add_argument('--output', type=Path, default=AUDIT/'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json')
    parser.add_argument('--support-directory', type=Path, default=AUDIT/'root_closed_families_actual_reproduction_support')
    args = parser.parse_args()
    output, support = args.output.resolve(), args.support_directory.resolve()
    # Destination safety is the only setup outside the protected attempt.
    assert output.parent == AUDIT and support.parent == AUDIT and not output.exists() and not support.exists()
    assert support != HERE and support.name not in ['primary_scope_family', 'rotation_concatenation_family', 'uniform_error_scaling_family', 'root_replay_preparation_family']
    private = private_audit = pins = current = closure_before = preparation_manifest_sha = None
    support_created = output_owned = False
    current_path = root_script = read_ledger = None
    inputs, own, root_bound = [], {}, {}
    runs, administrative_runs, comparisons, exceptions, retention_errors = [], [], [], [], []
    out = {'schema': 1, 'status': 'INCOMPLETE', 'setup_completed': False,
           'actual_outer_program_runs': runs, 'actual_administrative_command_runs': administrative_runs,
           'full_structured_receipt_comparisons': comparisons, 'recorded_qualified_differences': exceptions,
           'retention_errors': retention_errors, 'support_directory': support.relative_to(AUDIT).as_posix(),
           'original_substantive_turns': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0}

    def copy(source, destination):
        destination.parent.mkdir(parents=True, exist_ok=True)
        assert not source.is_symlink()
        shutil.copy2(source, destination)

    def normalize(value):
        if isinstance(value, dict):
            return {key: normalize(item) for key, item in value.items() if key not in CLOCK_KEYS}
        if isinstance(value, list):
            return [normalize(item) for item in value]
        return value.replace(str(private), str(REPO)) if isinstance(value, str) else value

    def differences(actual, saved, at='$'):
        if type(actual) != type(saved):
            return [{'path': at, 'actual': actual, 'saved': saved}]
        if isinstance(actual, dict):
            if set(actual) != set(saved):
                return [{'path': at, 'actual_keys': sorted(actual), 'saved_keys': sorted(saved)}]
            return [item for key in actual for item in differences(actual[key], saved[key], at+'/'+key)]
        if isinstance(actual, list):
            if len(actual) != len(saved):
                return [{'path': at, 'actual_length': len(actual), 'saved_length': len(saved)}]
            return [item for index in range(len(actual)) for item in differences(actual[index], saved[index], at+'/'+str(index))]
        return [] if actual == saved else [{'path': at, 'actual': actual, 'saved': saved}]

    def compare(label, actual, saved, qualified=None):
        delta = differences(normalize(load(actual)), normalize(load(saved)))
        qualified = qualified or {}
        assert all(item['path'] in qualified and item == qualified[item['path']]['difference'] for item in delta), label
        record = {'label': label, 'actual': row(actual, AUDIT), 'saved': row(saved, AUDIT),
                  'complete_JSON_BYTE_equal': actual.read_bytes() == saved.read_bytes(),
                  'equal_after_explicit_clock_and_private_path_exclusions': not delta,
                  'full_JSON_differences': delta, 'precise_qualifications': qualified,
                  'all_remaining_fields_equal': True}
        comparisons.append(record)
        if delta:
            exceptions.append({'label': label, 'full_JSON_differences': delta, 'precise_qualifications': qualified})
        write(support/'structured_comparisons.json', comparisons)
        return delta

    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')

    def failure(error):
        return {'type': type(error).__name__, 'message': str(error),
                'traceback': ''.join(traceback.format_exception(type(error), error, error.__traceback__)),
                'errno': getattr(error, 'errno', None), 'filename': str(error.filename) if getattr(error, 'filename', None) else None}

    def data_bytes(value):
        if value is None: return b''
        if isinstance(value, str): return value.encode()
        return bytes(value)

    def best_effort(stage, action):
        try: return True, action()
        except BaseException as error:
            retention_errors.append({'stage': stage, **failure(error)})
            out['status'] = 'FAIL'
            return False, None

    def write_owned_output():
        nonlocal output_owned
        data = (json.dumps(out, indent=2, ensure_ascii=False)+'\n').encode()
        if output_owned:
            output.write_bytes(data)
        else:
            with output.open('xb') as handle:
                output_owned = True
                handle.write(data)

    def launch_artifact(path, data):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            return row(path, AUDIT)
        except OSError as error:
            retention_errors.append({'stage': 'launch_artifact_primary', 'path': str(path), **failure(error)})
            # If support retention fails, preserve the available bytes in the
            # known private attempt. This is failed-attempt scratch, not support.
            if private is None: raise
            fallback = private/'root_retention_fallback'/path.relative_to(support)
            fallback.parent.mkdir(parents=True, exist_ok=True)
            fallback.write_bytes(data)
            return row(fallback, AUDIT)

    def save_run_ledgers():
        for name, collection in [('outer_runs.json', runs), ('administrative_runs.json', administrative_runs)]:
            launch_artifact(support/name, (json.dumps(collection, indent=2)+'\n').encode())

    def launch(label, command, cwd, script=None, administrative=False, env=None):
        record = {'label': label, 'argv': list(map(str, command)), 'cwd': str(cwd),
                  'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'launch_attempted': False, 'actual_execution': False, 'completed': False,
                  'exit_code': None, 'exit': None, 'returncode': None, 'failure_type': None, 'error': None}
        (administrative_runs if administrative else runs).append(record)
        original_error, original_traceback, process, popen_called = None, None, None, False
        try:
            if script is not None:
                record['script_path'] = str(script)
                record['source_available'] = script.is_file() and not script.is_symlink()
                if record['source_available']:
                    source = script.read_bytes()
                    record['script_sha256'] = sha(source)
                    record['prelaunch_source'] = launch_artifact(support/'launch_sources'/(label+'.py'), source)
            else:
                record['source_not_applicable'] = 'Readonly administrative Git command; collector implementation is retained separately.'
            for channel in ['stdout', 'stderr']:
                record[channel] = launch_artifact(support/(label+'.'+channel), b'')
            record['stdio_capture'] = {'kind': 'prelaunch_empty_placeholder', 'stdout_available': False, 'stderr_available': False}
            save_run_ledgers()
            assert not retention_errors, 'Prelaunch retention failed; do not launch'
            record['launch_attempted'] = True
            save_run_ledgers()
            assert not retention_errors, 'Prelaunch ledger retention failed; do not launch'
            try:
                popen_called = True
                process = subprocess.run(command, cwd=cwd, capture_output=True, timeout=600, env=env or environment)
                record.update(actual_execution=True, completed=True, exit_code=process.returncode,
                              exit=process.returncode, returncode=process.returncode)
                values = {'stdout': process.stdout, 'stderr': process.stderr}
                kind = 'complete_child_streams'
            except subprocess.TimeoutExpired as error:
                original_error, original_traceback = error, error.__traceback__
                record.update(actual_execution=True, completed=False)
                values = {'stdout': error.stdout, 'stderr': error.stderr}
                kind = 'partial_timeout'
            except OSError as error:
                original_error, original_traceback = error, error.__traceback__
                record.update(actual_execution=False, completed=False)
                values = {'stdout': None, 'stderr': None}
                kind = 'no_child_launched'
            if original_error:
                record['failure_type'], record['error'] = type(original_error).__name__, failure(original_error)
            record['stdio_capture'] = {'kind': kind, **{channel+'_available': value is not None for channel, value in values.items()}}
            for channel, value in values.items():
                record[channel] = launch_artifact(support/(label+'.'+channel), data_bytes(value))
        except BaseException as error:
            if not popen_called:
                record['launch_attempted'] = False
                record['failure_stage'] = 'prelaunch_retention'
            if original_error is None:
                original_error, original_traceback = error, error.__traceback__
                record['failure_type'], record['error'] = type(error).__name__, failure(error)
            else:
                retention_errors.append({'stage': 'outer_stream_retention', 'label': label, **failure(error)})
        finally:
            record['ended_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            best_effort('outer_run_ledger_final_'+label, save_run_ledgers)
        if original_error: raise original_error.with_traceback(original_traceback)
        if retention_errors: raise RuntimeError('Launch evidence retention failed; attempted run and available bytes preserved')
        return process

    def run(label, script, *arguments, runtime=PYTHON, instrument=True, expected_exit=0):
        assert private is not None and script.is_relative_to(private), 'Writer execution must stay in the owned private hierarchy'
        command = [runtime, str(script), *map(str, arguments)]
        if instrument:
            command = [runtime, str(HERE/'capture_runner.py'), str(script), str(support/(label+'_nested')), *map(str, arguments)]
        process = launch(label, command, private, script)
        assert process.returncode == expected_exit, 'Actual outer run failed; full streams retained: '+label
        return process

    def retained(source, name):
        destination = support/'actual'/name
        copy(source, destination)
        return destination

    def qualify_streams(actual, saved, actual_streams, saved_streams, collection_key, name_key='label'):
        a, b = load(actual), load(saved)
        qualified = {}
        for index, actual_row in enumerate(a[collection_key]):
            saved_row = b[collection_key][index]
            assert actual_row[name_key] == saved_row[name_key]
            name = actual_row[name_key]
            for channel in ['stdout', 'stderr']:
                actual_data, saved_data = (actual_streams/(name+'.'+channel)).read_bytes(), (saved_streams/(name+'.'+channel)).read_bytes()
                assert normalize(actual_data.decode()) == normalize(saved_data.decode()), name+' '+channel
                actual_retained = retained(actual_streams/(name+'.'+channel), 'full_compared_streams/'+actual.stem+'/'+name+'.'+channel)
                for field, actual_value, saved_value in [(channel+'_sha256', sha(actual_data), sha(saved_data)),
                                                        (channel+'_bytes', len(actual_data), len(saved_data))]:
                    if field in actual_row and actual_value != saved_value:
                        assert actual_row[field] == actual_value and saved_row[field] == saved_value
                        pointer = '$/'+collection_key+'/'+str(index)+'/'+field
                        qualified[pointer] = {'difference': {'path': pointer, 'actual': actual_value, 'saved': saved_value},
                                              'reason': 'Complete actual/saved stream bodies equal after the single explicit private-repository path replacement; raw sizes/hashes remain different.',
                                              'actual_complete_stream': row(actual_retained, AUDIT),
                                              'saved_complete_stream': row(saved_streams/(name+'.'+channel), AUDIT)}
        return qualified

    try:
        support.mkdir()
        support_created = True
        # Retain the reviewed revision before any preflight/private setup can fail.
        for name in SOURCE_NAMES+[SOURCE_MANIFEST_NAME]:
            copy(HERE/name, support/'executed_sources'/name)
        assert not sys.flags.optimize
        sys.dont_write_bytecode = True
        pins = load(HERE/'INPUT_PINS.json')
        assert pins['repository_root'] == str(REPO) and pins['audit_relative_path'] == str(AUDIT.relative_to(REPO))
        current_path, root_script, read_ledger = [path.resolve() for path in
                                               [args.current_input_manifest, args.root_script_path, args.root_primary_read_ledger]]
        for path in [current_path, root_script, read_ledger]:
            assert path.parent == AUDIT and path.is_file() and not path.is_symlink()
        assert len({current_path, root_script, read_ledger}) == 3
        assert root_script.suffix == '.py' and current_path.suffix == read_ledger.suffix == '.json'
        assert read_ledger.name == 'ROOT_PRIMARY_READ_LEDGER.json'
        copy(root_script, support/'executed_sources/root_entrypoint.py')
        for path in [read_ledger, current_path]:
            copy(path, support/'root_prerequisites'/path.name)
        assert sha(root_script.read_bytes()) == args.root_script_sha256
        assert sha(read_ledger.read_bytes()) == args.root_primary_read_ledger_sha256
        # The separate ledger is root's prerequisite. This preparation and this
        # finite reproduction neither infer nor attest actual primary proof reading.
        current = load(current_path)
        assert current['approved_by_root'] is True and current['reason'] and current['current_head']
        inputs = current['files']
        assert {x['path'] for x in inputs} == REQUIRED_CURRENT and len(inputs) == len(REQUIRED_CURRENT)
        for record in inputs:
            require(record, REPO)
        assert current['runtimes']['system_python'] == PYTHON
        default_runtime = current['runtimes']['historical_default_failure_python']
        assert default_runtime == load(AUDIT/'primary_scope_family/default_python_failure.json')['stdout'].splitlines()[0]
        assert default_runtime == '/opt/homebrew/opt/python@3.14/bin/python3.14'
        assert Path(default_runtime).is_file()
        assert not (REPO/(NATIVE+'cache/catalog.sqlite-wal')).exists()
        assert not (REPO/(NATIVE+'cache/catalog.sqlite-shm')).exists()
        for record in [pins['snapshot_manifest'], pins['diff'], *pins.get('auxiliary', [])]:
            require(record, AUDIT)
        for record in pins['snapshot_files']:
            require({'path': record['path'], 'size': record['size'], 'sha256': record['sha256']}, AUDIT/'source_snapshot')
        closure_before = strict_closed(pins, AUDIT)
        preparation_manifest_sha = strict_preparation()
        own = {name: sha((HERE/name).read_bytes()) for name in SOURCE_NAMES}
        root_bound = {str(path): sha(path.read_bytes()) for path in [root_script, read_ledger, current_path]}
        out.update({'schema': 1, 'status': 'INCOMPLETE', 'head': pins['head'], 'base': pins['base'],
               'exact_original_file_count': 16, 'changed_diff_path_count': 17, 'closed_family_count': 3,
               'original_substantive_turns': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0,
               'root_script_path': root_script.relative_to(AUDIT).as_posix(), 'root_script_sha256': args.root_script_sha256,
               'executed_collector_path': Path(__file__).relative_to(AUDIT).as_posix(), 'executed_collector_sha256': own['collect_root_replays.py'],
               'root_primary_read_ledger': row(read_ledger, AUDIT), 'root_primary_read_attestation_by_preparer': False,
               'current_input_manifest': row(current_path, AUDIT), 'root_current_preimage_reason': current['reason'],
               'family_manifests': closure_before, 'actual_outer_program_runs': runs,
               'full_structured_receipt_comparisons': comparisons, 'recorded_qualified_differences': exceptions,
               'support_directory': support.relative_to(AUDIT).as_posix(),
               'scope': 'Actual original and closed-family diagnostic/provenance reproduction only. Mathematical/source-scope and publication verdict remain root responsibilities.'})
        assert support.name not in pins['families']
        copy(root_script, support/'executed_sources/root_entrypoint.py')
        for path in [read_ledger, current_path]:
            copy(path, support/'root_prerequisites'/path.name)
        (AUDIT/'tmp').mkdir(exist_ok=True)
        private = Path(tempfile.mkdtemp(prefix='root_pr39_actual_', dir=AUDIT/'tmp'))
        private_audit = private/pins['audit_relative_path']
        out['setup_completed'] = True
        for record in [pins['snapshot_manifest'], pins['diff'], *pins.get('auxiliary', [])]:
            copy(AUDIT/record['path'], private_audit/record['path'])
            copy(AUDIT/record['path'], support/'frozen/original'/record['path'])
        for record in pins['snapshot_files']:
            copy(AUDIT/'source_snapshot'/record['path'], private_audit/'source_snapshot'/record['path'])
            (private_audit/'source_snapshot'/record['path']).chmod(0o444)
            copy(AUDIT/'source_snapshot'/record['path'], support/'frozen/original/source_snapshot'/record['path'])
        for family, info in pins['families'].items():
            for record in info['members']+[info['manifest']]:
                copy(AUDIT/family/record['path'], private_audit/family/record['path'])
                copy(AUDIT/family/record['path'], support/'frozen/families'/family/record['path'])
            for record in info['foreign_members']:
                copy(AUDIT/family/record['path'], private_audit/family/record['path'])
                (private_audit/family/record['path']).chmod(0o444)
        for record in inputs:
            copy(REPO/record['path'], private/record['path'])
            require(record, private)
            (private/record['path']).chmod(0o444)
            if not record['path'].startswith(NATIVE+'cache/'):
                copy(REPO/record['path'], support/'native_preimages'/record['path'])
        (private/'.git').symlink_to(REPO/'.git', target_is_directory=True)
        bindir = private/'root_readonly_bin'; bindir.mkdir()
        git = bindir/'git'
        git.write_text('#!/usr/bin/python3\nimport os,sys\nallowed={"ls-tree","cat-file","diff","show","rev-parse","branch","hash-object"}\nassert sys.argv[1] in allowed\nassert sys.argv[1]!="branch" or sys.argv[2:]==["--show-current"]\nassert sys.argv[1]!="hash-object" or sys.argv[2:]==["--stdin"]\nos.environ["GIT_OPTIONAL_LOCKS"]="0"\nos.execv("/usr/bin/git",["/usr/bin/git",*sys.argv[1:]])\n')
        git.chmod(0o755)
        environment['PATH'] = str(bindir)+os.pathsep+os.environ.get('PATH', '')
        head_process = launch('current_head_preimage_readonly_git', ['git', 'rev-parse', 'HEAD'], private, administrative=True)
        (support/'current_head.stdout').write_bytes(head_process.stdout); (support/'current_head.stderr').write_bytes(head_process.stderr)
        assert head_process.returncode == 0 and not head_process.stderr and head_process.stdout.decode().strip() == current['current_head']
        out['current_head'] = current['current_head']
        out['current_head_qualification'] = {'historical_snapshot_main_at_start': load(AUDIT/'snapshot_manifest.json')['main_at_start'],
                                             'current_preimage_head': current['current_head'], 'reason': current['reason']}
        for name in ['inspect_source_native.py', 'reconstructed_controls.py']:
            copy(HERE/name, private/'root_tools'/name)
        run('source_native_full_provenance', private/'root_tools/inspect_source_native.py', '--repo', private,
            '--pins', HERE/'INPUT_PINS.json', '--output', private_audit/'ROOT_SOURCE_NATIVE_REPRODUCTION.json')
        provenance_file = retained(private_audit/'ROOT_SOURCE_NATIVE_REPRODUCTION.json', 'ROOT_SOURCE_NATIVE_REPRODUCTION.json')
        out['source_native_inspection_receipt'] = row(provenance_file, AUDIT)
        out['provenance'] = load(provenance_file)
        out['original_runtime_python'] = PYTHON
        out['original_runtime_python_version'] = out['provenance']['runtime_python_version']
        original_replays = []
        original_specs = [('author', 'verify.py', 'verification.json', 'verification.json', 520),
                          ('old_submitted', 'review/submitted_verify.py', 'review/submitted_results.json', 'verification.json', 520),
                          ('old_independent', 'review/independent_checks.py', 'review/independent_results.json', 'independent_results.json', 899)]
        for label, program, expected, generated_name, byte_count in original_specs:
            directory = private_audit/'ROOT_ORIGINAL_RUNS'/label; directory.mkdir(parents=True, exist_ok=False)
            script = directory/Path(program).name
            copy(private_audit/'source_snapshot'/program, script); script.chmod(0o444)
            before = script.read_bytes()
            process = run('root_original_'+label, script)
            frozen = (AUDIT/'source_snapshot'/expected).read_bytes()
            generated = directory/generated_name
            assert len(frozen) == byte_count and not process.stderr
            assert process.stdout == frozen and json.loads(process.stdout) == json.loads(frozen)
            assert generated.is_file() and generated.read_bytes() == frozen and load(generated) == json.loads(frozen)
            packet = load(generated)
            if label == 'old_independent':
                assert packet['named_checks_passed'] == 12 and packet['failed'] == 0 and packet['path_configurations'] == 144
                assert packet['rotation_grid_equalities'] == 2256 and packet['randomized_zero_duration_prefix_laws'] == 16 and packet['sympy_version'] == '1.14.0'
            else:
                assert packet['passed'] is True and packet['finite_configurations'] == 12288 and packet['uniform_four_step_prefix_checks'] == 48
            assert script.read_bytes() == before
            actual_generated = retained(generated, 'original_replays/'+label+'/'+generated_name)
            original_replays.append({'label': label, 'program': program, 'program_sha256': sha(before), 'exit_code': 0,
                'whole_stdout_BYTE_equal': True, 'whole_stdout_JSON_equal': True, 'stdout_bytes': len(frozen), 'stdout_sha256': sha(frozen),
                'actual_stdout': runs[-1]['stdout'], 'actual_stderr': runs[-1]['stderr'], 'expected_receipt': row(AUDIT/'source_snapshot'/expected, AUDIT),
                'generated_receipt': row(actual_generated, AUDIT), 'generated_receipt_sha256': sha(actual_generated.read_bytes()),
                'generated_complete_receipt_BYTE_equal': True, 'generated_complete_receipt_JSON_equal': True,
                'generated_receipt_behavior': 'The unchanged original program itself writes this complete JSON file in a fresh private directory; actual file bytes and stdout are retained separately.',
                'complete_actual_result': packet})
        out['original_replays'] = original_replays
        out['original_runtime_sympy_version'] = '1.14.0'
        # Reproduce the real missing-SymPy failure with the original independent
        # script, retaining the failure rather than installing or substituting.
        runtime_probe = private/'root_tools/runtime_probe.py'
        runtime_probe.write_text('import json,sys\nprint(json.dumps({"executable":sys.executable,"version":sys.version,"version_info":list(sys.version_info)},indent=2))\n')
        runtime_probe.chmod(0o444)
        runtime_process = run('root_default_python314_runtime', runtime_probe, runtime=default_runtime)
        runtime_result = json.loads(runtime_process.stdout)
        assert runtime_result['executable'] == default_runtime and runtime_result['version_info'][:2] == [3,14] and not runtime_process.stderr
        out['default_python314_runtime'] = runtime_result
        default_dir = private_audit/'ROOT_ORIGINAL_RUNS/default_missing_sympy'; default_dir.mkdir()
        default_script = default_dir/'independent_checks.py'; copy(private_audit/'source_snapshot/review/independent_checks.py', default_script); default_script.chmod(0o444)
        failed = run('root_default_python314_missing_sympy', default_script, runtime=default_runtime, instrument=False, expected_exit=1)
        assert not failed.stdout and b"ModuleNotFoundError: No module named 'sympy'" in failed.stderr
        assert not (default_dir/'independent_results.json').exists()
        out['default_python314_actual_failure'] = {'runtime': default_runtime, 'source_sha256': sha(default_script.read_bytes()),
            'exit_code': 1, 'actual_stdout': runs[-1]['stdout'], 'actual_stderr': runs[-1]['stderr'], 'generated_result_absent': True,
            'qualification': 'Fresh actual original independent-script failure under the historical default interpreter; not a claim to replay the earlier -c probe byte-for-byte.'}
        out['default_python314_missing_sympy_failure_retained'] = True
        manifest_specs = {'primary_scope_family': ('check_family_manifest.py', ['verify']),
                          'rotation_concatenation_family': ('manifest.py', ['check']),
                          'uniform_error_scaling_family': ('manifest_integrity.py', ['--no-digest'])}
        for family, (validator, arguments) in manifest_specs.items():
            process = run(family+'_pristine_manifest', private_audit/family/validator, *arguments)
            value = json.loads(process.stdout); assert value.get('passed', value.get('verified')) is True
            count = value.get('first_party_members', value.get('recursive_file_count', value.get('files')))
            assert count == pins['families'][family]['member_count'] and not process.stderr
            if family == 'uniform_error_scaling_family':
                assert process.stdout == (AUDIT/family/'streams/final_manifest.stdout').read_bytes()
        controls = private_audit/'ROOT_RECONSTRUCTED_CONTROLS'
        run('root_reconstructed_packet_and_manifest_controls', private/'root_tools/reconstructed_controls.py',
            '--repo', private, '--pins', HERE/'INPUT_PINS.json', '--output-directory', controls)
        packet_controls = load(controls/'PACKET_CONTROL_RESULTS.json'); manifest_controls = load(controls/'MANIFEST_CONTROL_RESULTS.json')
        assert len(packet_controls) == 6 and len(manifest_controls) == 28
        assert all(x['observed_expected'] for x in packet_controls+manifest_controls)
        assert all(x['strict_root_guard_pass'] == (x['case'] == 'baseline') for x in manifest_controls)
        out['real_packet_controls'] = packet_controls
        out['real_manifest_controls'] = manifest_controls
        out['nested_manifest_and_foreign_component_extras_rejected_by_original_and_strict_root_guards'] = True
        primary = private_audit/'primary_scope_family'
        process = run('primary_source_qualifications', primary/'check_source_qualifications.py')
        result = retained(primary/'SOURCE_QUALIFICATION_RESULTS.json', 'primary_scope_family/SOURCE_QUALIFICATION_RESULTS.json')
        expected = AUDIT/'primary_scope_family/SOURCE_QUALIFICATION_RESULTS.json'
        assert result.read_bytes() == expected.read_bytes() and load(result) == load(expected) and process.stdout == expected.read_bytes() and not process.stderr
        compare('primary_source_qualifications_whole_JSON', result, expected)
        out['source_qualification_proof_limit'] = 'Actual exact finite sign/initial-boundary/radical checks reproduce the sealed qualification receipt. Root primary proof reading and the scientific certificate remain separate prerequisites.'
        rotation = private_audit/'rotation_concatenation_family'
        process = run('rotation_exact_falsification_controls', rotation/'falsification_controls.py')
        result = retained(rotation/'falsification_results.json', 'rotation_concatenation_family/falsification_results.json')
        expected = AUDIT/'rotation_concatenation_family/falsification_results.json'
        assert result.read_bytes() == expected.read_bytes() and load(result) == load(expected) and process.stdout == expected.read_bytes() and not process.stderr
        compare('rotation_exact_falsification_controls_whole_JSON', result, expected)
        uniform = private_audit/'uniform_error_scaling_family'
        process = run('uniform_exact_controls', uniform/'audit_controls.py', '--candidate', uniform/'frozen_original/PARTIAL.md', '--out', uniform/'exact_control_results.json')
        result = retained(uniform/'exact_control_results.json', 'uniform_error_scaling_family/exact_control_results.json')
        expected = AUDIT/'uniform_error_scaling_family/exact_control_results.json'
        assert result.read_bytes() == expected.read_bytes() and load(result) == load(expected) and process.stdout == expected.read_bytes() and not process.stderr
        compare('uniform_exact_controls_whole_JSON', result, expected)
        # Historical outputs are already retained in frozen/families. Only the
        # private copied mutation destinations are cleared for fresh real writes.
        historical_mutations = uniform/'executed_mutations'
        out['private_historical_output_reset'] = {'path': str(historical_mutations), 'purpose': 'Permit unchanged writer to create fresh actual mutation files; all historical closed inputs are retained before this private-only removal.'}
        shutil.rmtree(historical_mutations)
        process = run('uniform_actual_eight_prose_and_two_code_controls', uniform/'run_adversarial_controls.py')
        result = retained(uniform/'adversarial_execution_receipts.json', 'uniform_error_scaling_family/adversarial_execution_receipts.json')
        expected = AUDIT/'uniform_error_scaling_family/adversarial_execution_receipts.json'
        packet = load(result); assert len(packet['records']) == 11 and all(x['observed_expected'] for x in packet['records'])
        assert packet['records'][0]['exit_code'] == 0 and all(x['exit_code'] == 1 for x in packet['records'][1:])
        qualified = qualify_streams(result, expected, uniform/'streams', AUDIT/'uniform_error_scaling_family/streams', 'records', name_key='name')
        compare('uniform_full_actual_adversarial_receipt', result, expected, qualified)
        assert json.loads(process.stdout) == packet and not process.stderr
        out['real_uniform_prose_and_code_control_count'] = 10
        out['scientific_certificate'] = row(AUDIT/'ROOT_PARTIAL_SCOPE_CERTIFICATE.md', AUDIT)
        out['primary_proof_qualifications'] = row(AUDIT/'ROOT_PRIMARY_PROOF_QUALIFICATIONS.md', AUDIT)
        out['scientific_status'] = 'UNSOLVED; valid scoped coupling/scaling partial. No finite random Brownian origin established; no novelty claim.'
        out['full_problem_solved'] = False
        out['status'] = 'PASS'
    except BaseException as error:
        out['status'] = 'FAIL'
        out['failure'] = failure(error)
    finally:
        def finalize_available_evidence():
            assert support_created, 'This attempt does not own the support destination'
            # Each secondary retention operation is isolated. It must never replace
            # the original setup/launch/helper failure or trigger private cleanup.
            for name in SOURCE_NAMES+[SOURCE_MANIFEST_NAME]:
                source = HERE/name
                if source.is_file() and not source.is_symlink():
                    best_effort('available_revision_source_'+name, lambda source=source: copy(source, support/'executed_sources'/source.name))
            for source in [root_script, read_ledger, current_path]:
                if source is not None and source.parent == AUDIT and source.is_file() and not source.is_symlink():
                    best_effort('available_root_prerequisite_'+source.name, lambda source=source: copy(source, support/'available_root_prerequisites'/source.name))
            directories = []
            if private_audit is not None and pins is not None:
                for family in pins['families']:
                    directories.append((private_audit/family, 'final_partial_or_complete/'+family, family))
                directories.append((private_audit/'ROOT_RECONSTRUCTED_CONTROLS', 'final_partial_or_complete/reconstructed_controls', 'controls'))
                directories.append((private_audit/'ROOT_ORIGINAL_RUNS', 'final_partial_or_complete/original_runs', 'originals'))
                source = private_audit/'ROOT_SOURCE_NATIVE_REPRODUCTION.json'
                if source.is_file(): best_effort('available_source_native_receipt', lambda: retained(source, 'final_partial_or_complete/ROOT_SOURCE_NATIVE_REPRODUCTION.json'))
            if private is not None:
                directories.extend([(private/'root_tools', 'final_partial_or_complete/root_tools', 'tools'),
                                    (private/'root_retention_fallback', 'failed_retention_fallback', 'fallback')])
            for directory, destination, kind in directories:
                ok, paths = best_effort('available_tree_inventory_'+destination, lambda directory=directory: list(directory.rglob('*')) if directory.exists() else [])
                if not ok: continue
                for source in paths:
                    relative = source.relative_to(directory)
                    foreign = kind in pins['families'] and (relative.as_posix() in {x['path'] for x in pins['families'][kind]['foreign_members']} or (pins['families'][kind]['cache_prefix'] and relative.parts[0] == pins['families'][kind]['cache_prefix']))
                    excluded = {'__pycache__', 'manifest_cases', 'packet_cases'}.intersection(relative.parts)
                    if source.is_file() and not source.is_symlink() and not foreign and not excluded:
                        best_effort('available_file_'+destination+'/'+relative.as_posix(),
                                    lambda source=source, name=destination+'/'+relative.as_posix(): retained(source, name))
            if out['setup_completed']:
                try:
                    closure_after = strict_closed(pins, AUDIT)
                    assert closure_after == closure_before
                    for record in inputs: require(record, REPO)
                    assert own == {name: sha((HERE/name).read_bytes()) for name in SOURCE_NAMES}
                    assert strict_preparation() == preparation_manifest_sha
                    assert root_bound == {str(path): sha(path.read_bytes()) for path in [root_script, read_ledger, current_path]}
                    final_head = launch('current_head_final_readonly_git', ['/usr/bin/git', 'rev-parse', 'HEAD'], REPO,
                                        administrative=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
                    assert final_head.returncode == 0 and not final_head.stderr and final_head.stdout.decode().strip() == current['current_head']
                    for record in [pins['snapshot_manifest'], pins['diff'], *pins.get('auxiliary', [])]: require(record, AUDIT)
                    for record in pins['snapshot_files']:
                        require({'path': record['path'], 'size': record['size'], 'sha256': record['sha256']}, AUDIT/'source_snapshot')
                    out['authored_members_verified_before_and_after'] = 732
                    out['strict_root_closure_before_and_after'] = {'before': closure_before, 'after': closure_after, 'equal': True}
                    out['strict_root_exact_recursive_closure_verified'] = True
                    out['native_full_file_preimages_before_and_after'] = inputs
                    out['current_head_unchanged'] = current['current_head']
                    out['root_and_preparation_sources_unchanged'] = own
                    out['preparation_manifest_sha256_before_and_after'] = preparation_manifest_sha
                except BaseException as error:
                    out['status'] = 'FAIL'
                    out['integrity_failure'] = failure(error)
            else:
                out['integrity_check_not_run_reason'] = 'Preflight/private setup did not complete; no before/after success is fabricated.'
            nested = []
            ok, ledgers = best_effort('nested_ledger_inventory', lambda: sorted(support.glob('*_nested/nested_runs.json')))
            for path in ledgers or []:
                ok, records = best_effort('nested_ledger_read_'+str(path), lambda path=path: load(path))
                if ok:
                    nested.extend({'outer_label': path.parent.name[:-7], 'nested_index': index, **item} for index, item in enumerate(records))
            out['actual_nested_program_runs'] = nested
            out['comparison_exclusion_policy'] = {'clock_keys': sorted(CLOCK_KEYS),
                'single_private_path_prefix': {'actual': str(private) if private is not None else None, 'saved': str(REPO)},
                'qualified_differences_remain_in_full_JSON': True, 'broad_runtime_or_native_ignoring': False}
            out['private_attempt_preserved'] = private is not None and private.exists()
            out['private_attempt_locator'] = {'audit_tmp_directory_name': private.name if private is not None else None,
                'meaning': 'Administrative scratch locator only, never a CURRENT dependency anchor or retained support artifact.',
                'cleanup_policy': 'No automatic deletion. Root may clean only after independently inspecting complete retained evidence. Failed retention keeps all available private evidence.'}
            out['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            if retention_errors: out['status'] = 'FAIL'
    
            def publish_retained_receipt():
                write_owned_output()
                records = []
                for path in sorted(support.rglob('*')):
                    assert not path.is_symlink(), 'No retained support symlinks'
                    if path.is_file() and path.relative_to(support).as_posix() != 'ROOT_SUPPORT_MANIFEST.json':
                        records.append(row(path, support))
                packet = {'schema': 1, 'status': out['status'], 'self_excluding': True,
                    'excluded': ['ROOT_SUPPORT_MANIFEST.json'], 'files': records,
                    'path_base': 'support_directory', 'support_directory': support.relative_to(AUDIT).as_posix(),
                    'root_reproduction_receipt': row(output, AUDIT), 'root_reproduction_receipt_sha256': sha(output.read_bytes()),
                    'foreign_corpus_SQL_PDF_OCR_cache_or_private_scratch_retained': False}
                write(support/'ROOT_SUPPORT_MANIFEST.json', packet)
                for record in records: require(record, support)
                actual = sorted(path.relative_to(support).as_posix() for path in support.rglob('*')
                                if path.is_file() and path.relative_to(support).as_posix() != 'ROOT_SUPPORT_MANIFEST.json')
                assert actual == sorted(record['path'] for record in records)
                assert packet['root_reproduction_receipt_sha256'] == sha(output.read_bytes())
            ok, unused = best_effort('final_receipt_and_strict_support_manifest', publish_retained_receipt)
            if not ok:
                # Retry only failure reporting, never a scientific program. Keep
                # the private attempt even if the report itself remains unwritable.
                ok, unused = best_effort('failure_receipt_and_support_manifest_retry', publish_retained_receipt)
            if not ok and private is not None:
                best_effort('private_finalization_failure_receipt', lambda: write(private/'ROOT_FINALIZATION_FAILURE.json', out))
            if out['status'] != 'PASS':
                print(json.dumps({'status': 'FAIL', 'original_failure': out.get('failure'),
                    'integrity_failure': out.get('integrity_failure'), 'retention_errors': retention_errors,
                    'private_attempt_locator': out['private_attempt_locator']}), file=sys.stderr)
        try:
            finalize_available_evidence()
        except BaseException as error:
            # This outer guard also covers unexpected filesystem/metadata
            # errors in the finalizer itself, without replacing a prior failure.
            out['status'] = 'FAIL'
            out['unexpected_finalization_failure'] = failure(error)
            retention_errors.append({'stage': 'unexpected_finalization_failure', **failure(error)})
            out['private_attempt_preserved'] = private is not None
            out['private_attempt_locator'] = {'audit_tmp_directory_name': private.name if private is not None else None,
                'meaning': 'Administrative scratch locator only; never a CURRENT dependency anchor.',
                'cleanup_policy': 'No automatic deletion; failed finalization keeps the private attempt.'}
            out['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            best_effort('emergency_failure_receipt', write_owned_output)
            if private is not None:
                best_effort('emergency_private_failure_receipt', lambda: write(private/'ROOT_FINALIZATION_FAILURE.json', out))
            print(json.dumps({'status': 'FAIL', 'original_failure': out.get('failure'),
                'unexpected_finalization_failure': out['unexpected_finalization_failure'],
                'retention_errors': retention_errors, 'private_attempt_locator': out['private_attempt_locator']}), file=sys.stderr)
    print(json.dumps({'status': out['status'], 'receipt': str(output) if output_owned else None,
                      'support': str(support), 'private_attempt_preserved': out['private_attempt_preserved']}, indent=2))
    if out['status'] != 'PASS': raise SystemExit(1)


if __name__ == '__main__':
    main()
