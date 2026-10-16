#!/usr/bin/env python3
"""Root-owned ACTUAL PR38 reproduction. Preparation alone proves no run succeeded.

Read this entire source and the companion sources before root execution.
All writer helpers execute in a private exact hierarchy. Complete first-party
inputs/results/streams survive; corpus, SQL, foreign sources and scratch do not.
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
                'reconstructed_controls.py', 'INPUT_PINS.json', 'README.md', 'RESEARCH_LOG.md']


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
        for record in info['members']+[info['manifest']]:
            require(record, directory)
        assert len(info['members']) == info['member_count']
        expected = sorted(record['path'] for record in info['members'])
        assert len(expected) == len(set(expected))
        actual = []
        for path in directory.rglob('*'):
            relative = path.relative_to(directory)
            if relative.as_posix() == info['manifest_name'] or relative.parts[0] == info['cache_prefix']:
                continue
            assert not path.is_symlink(), 'Strict closure rejects symlink: '+str(path)
            if path.is_file():
                actual.append(relative.as_posix())
        assert sorted(actual) == expected, 'Strict root recursive coverage: '+family
        summary[family] = {'manifest_path': str((directory/info['manifest_name']).relative_to(AUDIT)),
                           'manifest_sha256': info['manifest']['sha256'], 'member_count': len(expected),
                           'exclusions': [info['manifest_name'], info['cache_prefix']+'/'],
                           'strict_recursive_coverage': True}
    assert sum(x['member_count'] for x in summary.values()) == 169
    return summary


def strict_preparation():
    manifest = HERE/'PREPARATION_MANIFEST.json'
    packet = load(manifest)
    assert packet['excluded'] == ['PREPARATION_MANIFEST.json']
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
    assert not sys.flags.optimize
    sys.dont_write_bytecode = True
    pins = load(HERE/'INPUT_PINS.json')
    assert pins['repository_root'] == str(REPO) and pins['audit_relative_path'] == str(AUDIT.relative_to(REPO))
    current_path, root_script, read_ledger = [path.resolve() for path in
                                           [args.current_input_manifest, args.root_script_path, args.root_primary_read_ledger]]
    for path in [current_path, root_script, read_ledger]:
        assert path.parent == AUDIT and path.is_file() and not path.is_symlink()
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
    assert default_runtime == load(AUDIT/'primary_scope_family/ORIGINAL_VERIFY_EXECUTION.json')[0]['runtime_path']
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
    output, support = args.output.resolve(), args.support_directory.resolve()
    assert output.parent == AUDIT and support.parent == AUDIT and not output.exists() and not support.exists()
    assert support.name not in pins['families'] and support != HERE
    support.mkdir()
    (AUDIT/'tmp').mkdir(exist_ok=True)
    private = Path(tempfile.mkdtemp(prefix='root_pr38_actual_', dir=AUDIT/'tmp'))
    private_audit = private/pins['audit_relative_path']
    runs, comparisons, exceptions = [], [], []
    out = {'schema': 1, 'status': 'INCOMPLETE', 'head': pins['head'], 'base': pins['base'],
           'exact_original_file_count': 16, 'changed_diff_path_count': 17, 'closed_family_count': 3,
           'original_substantive_turns': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0,
           'root_script_path': root_script.relative_to(AUDIT).as_posix(), 'root_script_sha256': args.root_script_sha256,
           'executed_collector_path': Path(__file__).relative_to(AUDIT).as_posix(), 'executed_collector_sha256': own['collect_root_replays.py'],
           'root_primary_read_ledger': row(read_ledger, AUDIT), 'root_primary_read_attestation_by_preparer': False,
           'current_input_manifest': row(current_path, AUDIT), 'root_current_preimage_reason': current['reason'],
           'family_manifests': closure_before, 'actual_outer_program_runs': runs,
           'full_structured_receipt_comparisons': comparisons, 'recorded_qualified_differences': exceptions,
           'support_directory': support.relative_to(AUDIT).as_posix(),
           'scope': 'Actual original and closed-family diagnostic/provenance reproduction only. Mathematical/source-scope and publication verdict remain root responsibilities.'}

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

    def run(label, script, *arguments, runtime=PYTHON, instrument=True):
        command = [runtime, str(script), *map(str, arguments)]
        if instrument:
            command = [runtime, str(HERE/'capture_runner.py'), str(script), str(support/(label+'_nested')), *map(str, arguments)]
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        process = subprocess.run(command, cwd=private, capture_output=True, timeout=600, env=environment)
        record = {'label': label, 'argv': command, 'cwd': str(private), 'script_sha256': sha(script.read_bytes()),
                  'started_utc': started, 'exit_code': process.returncode, 'exit': process.returncode, 'returncode': process.returncode}
        for channel in ['stdout', 'stderr']:
            path = support/(label+'.'+channel)
            path.write_bytes(getattr(process, channel))
            record[channel] = row(path, AUDIT)
        runs.append(record)
        write(support/'outer_runs.json', runs)
        assert process.returncode == 0, 'Actual outer run failed; full streams retained: '+label
        return process

    def retained(source, name):
        destination = support/'actual'/name
        copy(source, destination)
        return destination

    def qualify_streams(actual, saved, actual_streams, saved_streams, collection_key):
        a, b = load(actual), load(saved)
        qualified = {}
        for index, actual_row in enumerate(a[collection_key]):
            saved_row = b[collection_key][index]
            assert actual_row['label'] == saved_row['label']
            name = actual_row['label']
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
        for name in SOURCE_NAMES:
            copy(HERE/name, support/'executed_sources'/name)
        copy(HERE/'PREPARATION_MANIFEST.json', support/'executed_sources/PREPARATION_MANIFEST.json')
        copy(root_script, support/'executed_sources/root_entrypoint.py')
        for path in [read_ledger, current_path]:
            copy(path, support/'root_prerequisites'/path.name)
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
        head_process = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=private, capture_output=True, env=environment)
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
        for program, expected, assertions in [('verify.py', 'verification.json', 30),
                                              ('review/independent_checks.py', 'review/independent_results.json', 72)]:
            script = private_audit/'source_snapshot'/program
            before = script.read_bytes()
            process = run('root_original_'+str(assertions), script, instrument=False)
            frozen = (AUDIT/'source_snapshot'/expected).read_bytes()
            assert not process.stderr and process.stdout == frozen and json.loads(process.stdout) == json.loads(frozen)
            packet = json.loads(process.stdout)
            assert packet['status'] == 'PASS' and packet['sympy_version'] == '1.14.0' and packet['assertions'] == assertions
            assert sum(packet['checks'].values()) == assertions and script.read_bytes() == before
            generated = support/'actual'/('root_original_'+str(assertions)+'_stdout_materialized.json')
            generated.parent.mkdir(parents=True, exist_ok=True)
            generated.write_bytes(process.stdout)
            original_replays.append({'program': program, 'program_sha256': sha(before), 'exit_code': 0,
                                     'whole_stdout_BYTE_equal': True, 'whole_stdout_JSON_equal': True,
                                     'stdout_bytes': len(frozen), 'stdout_sha256': sha(frozen), 'assertions': assertions,
                                     'actual_stdout': runs[-1]['stdout'], 'actual_stderr': runs[-1]['stderr'],
                                     'generated_receipt': row(generated, AUDIT), 'generated_receipt_sha256': sha(generated.read_bytes()),
                                     'generated_complete_receipt_BYTE_equal': generated.read_bytes() == frozen,
                                     'generated_complete_receipt_JSON_equal': load(generated) == json.loads(frozen),
                                     'generated_receipt_behavior': 'Collector materializes complete actual stdout as a checkable JSON artifact. The unchanged original program itself writes no result file.'})
        out['original_replays'] = original_replays
        out['original_runtime_sympy_version'] = '1.14.0'
        for family in pins['families']:
            validator = 'verify_family_manifest.py' if family == 'primary_scope_family' else 'verify_manifest.py'
            run(family+'_pristine_manifest', private_audit/family/validator)
        controls = private_audit/'ROOT_RECONSTRUCTED_CONTROLS'
        run('root_reconstructed_trace_and_manifest_controls', private/'root_tools/reconstructed_controls.py',
            '--repo', private, '--pins', HERE/'INPUT_PINS.json', '--output-directory', controls)
        for path in controls.rglob('*'):
            if path.is_file() and not path.is_symlink() and 'manifest_cases' not in path.relative_to(controls).parts:
                retained(path, 'reconstructed_controls/'+path.relative_to(controls).as_posix())
        # Preserve actual mutated manifest/victim/extra bytes; unchanged clone
        # files are bound by the frozen family input, not retained as scratch.
        manifest_rows = load(controls/'manifest_reconstruction_receipts.json')
        for item in manifest_rows:
            clone = controls/'manifest_cases'/item['family']/item['case']
            wanted = [pins['families'][item['family']]['manifest_name'], item['victim_path'],
                      'ROOT_UNLISTED_NEGATIVE.txt', 'nested/'+pins['families'][item['family']]['manifest_name'],
                      'nested/ignoredtmp/ROOT_UNLISTED_NEGATIVE.txt']
            for name in wanted:
                path = clone/name
                if path.is_file() and not path.is_symlink():
                    retained(path, 'reconstructed_controls/mutated_inputs/'+item['family']+'/'+item['case']+'/'+name)
        out['administrative_guard_findings'] = [item for item in manifest_rows if item['family'] == 'primary_scope_family'
                                                and item['case'] in ['nested_manifest_extra', 'nested_ignoredtmp_extra']]
        assert len(out['administrative_guard_findings']) == 2 and all(item['actual_pass'] and not item['strict_root_guard_pass'] for item in out['administrative_guard_findings'])
        out['primary_nested_manifest_exploit_rejected_by_strict_root'] = True
        trace_actual = support/'actual/reconstructed_controls/trace_replay_receipts.json'
        trace_saved = AUDIT/'trace_geometry_family/replay_and_corruption_receipts.json'
        qualified = qualify_streams(trace_actual, trace_saved, support/'actual/reconstructed_controls/streams',
                                    AUDIT/'trace_geometry_family/streams', 'runs')
        compare('trace_complete_eight_run_receipt', trace_actual, trace_saved, qualified)
        primary = private_audit/'primary_scope_family'
        for label, code, result, runtime in [('primary_author_and_runtime_controls', 'run_original_verify.py', 'ORIGINAL_VERIFY_EXECUTION.json', default_runtime),
                                             ('primary_independent_controls', 'run_original_review_helper.py', 'ORIGINAL_REVIEW_HELPER_EXECUTION.json', PYTHON),
                                             ('primary_source_accounting_controls', 'check_source_and_budget.py', 'SOURCE_ACCOUNTING_CONTROL_RESULTS.json', PYTHON)]:
            run(label, primary/code, runtime=runtime)
            actual = retained(primary/result, 'primary_scope_family/'+result)
            compare(label+'_whole_JSON', actual, AUDIT/'primary_scope_family'/result)
            if result == 'ORIGINAL_VERIFY_EXECUTION.json':
                default_failure = load(actual)[0]
                assert default_failure['case'] == 'default_runtime_initial' and default_failure['exit_code'] == 1
                assert default_failure['stdout'] == '' and "ModuleNotFoundError: No module named 'sympy'" in default_failure['stderr']
                assert default_failure['exact_original_bytes'] and default_failure['runtime_version'].startswith('3.14.')
                out['default_python314_missing_sympy_failure_retained'] = True
                out['default_python314_actual_failure'] = {'actual_receipt': row(actual, AUDIT), 'case_index': 0,
                                                         'runtime_path': default_failure['runtime_path'],
                                                         'source_sha256': default_failure['source_sha256'], 'exit_code': 1}
        metadata_code = primary/'read_historical_metadata.py'
        before = metadata_code.read_bytes(); old = b"root=Path('/Users/alec/Documents/Math')"
        replacement = ('root=Path('+repr(str(private))+')').encode()
        assert before.count(old) == 1
        metadata_code.write_bytes(before.replace(old, replacement))
        retained(metadata_code, 'source_revisions/read_historical_metadata.py')
        write(support/'actual/source_revisions/metadata_path_revision.json', {'original_sha256': sha(before), 'revised_sha256': sha(metadata_code.read_bytes()),
              'exact_old': old.decode(), 'exact_new': replacement.decode(), 'purpose': 'Only absolute repository-root transport; all read/selection/hash predicates unchanged.'})
        run('primary_frozen_current_native_metadata', metadata_code)
        metadata_actual = retained(primary/'POST_SEAL_HISTORY_METADATA.json', 'primary_scope_family/POST_SEAL_HISTORY_METADATA.json')
        metadata_saved = AUDIT/'primary_scope_family/POST_SEAL_HISTORY_METADATA.json'
        actual = load(metadata_actual)
        by_path = {record['path']: record for record in inputs}
        for name in ['state.json', 'assessments.json', 'catalog.json']:
            assert actual[name]['bytes'] == by_path[NATIVE+name]['size'] and actual[name]['sha256'] == by_path[NATIVE+name]['sha256']
        assert actual['state.json']['target'] is None and actual['history_target']['events'] == []
        assert actual['catalog.json']['target'] == [out['provenance']['current_native_target']['catalog']]
        assert actual['history_target']['sha256'] == by_path[NATIVE+'history.jsonl']['sha256']
        assert actual['related_target_groups']['sha256'] == by_path[NATIVE+'review_v2/related_target_groups.json']['sha256']
        assert actual['related_target_groups']['target_mentions'] == []
        inventory = load(private/'draft_pr_publication_program_20260930/inventory.json')
        selected = []
        def select(value):
            if isinstance(value, dict):
                if any(str(value.get(key)) == '38' for key in ['number', 'pr_number', 'pr']):
                    selected.append(value); return
                for item in value.values(): select(item)
            elif isinstance(value, list):
                for item in value: select(item)
        select(inventory)
        assert actual['inventory_entry'] == selected and len(selected) == 1 and selected[0]['headRefOid'] == pins['head']
        delta = differences(normalize(actual), normalize(load(metadata_saved)))
        allowed_prefixes = ['$/state.json/', '$/assessments.json/', '$/catalog.json/', '$/history_target/', '$/related_target_groups/', '$/inventory_entry/']
        qualified = {}
        for item in delta:
            assert any(item['path'].startswith(prefix) for prefix in allowed_prefixes)
            qualified[item['path']] = {'difference': item, 'reason': 'Explicit root-approved dated current preimage; full actual structures/hashes checked against exact frozen native/inventory copies. No field is erased.',
                                       'current_input_manifest': out['current_input_manifest'], 'root_reason': current['reason']}
        compare('primary_full_dated_current_metadata', metadata_actual, metadata_saved, qualified)
        measure = private_audit/'current_measure_family'
        run('current_measure_original_code_and_prose_controls', measure/'replay_and_controls.py')
        for name in ['replay_inputs.json', 'replay_results.json']:
            actual = retained(measure/name, 'current_measure_family/'+name)
            qualified = qualify_streams(actual, AUDIT/'current_measure_family'/name, measure/'streams',
                                        AUDIT/'current_measure_family/streams', 'negative_controls') if name == 'replay_results.json' else {}
            compare('current_measure_whole_'+name, actual, AUDIT/'current_measure_family'/name, qualified)
        for family in ['primary_scope_family', 'current_measure_family']:
            for path in (private_audit/family).rglob('*'):
                relative = path.relative_to(private_audit/family)
                if path.is_file() and not path.is_symlink() and not {'tmp', 'ignoredtmp', '__pycache__'}.intersection(relative.parts):
                    retained(path, family+'/complete_post_replay/'+relative.as_posix())
        for subtree in ['ignoredtmp/verify_runs', 'ignoredtmp/review_runs']:
            for path in (primary/subtree).rglob('*'):
                if path.is_file() and not path.is_symlink():
                    retained(path, 'primary_scope_family/actual_case_inputs/'+path.relative_to(primary).as_posix())
        out['status'] = 'PASS'
    except BaseException as error:
        out['status'] = 'FAIL'
        out['failure'] = {'type': type(error).__name__, 'message': str(error), 'traceback': traceback.format_exc()}
    finally:
        # A failed helper's partial first-party outputs and exact source inputs
        # survive too. Foreign/cache trees and manifest-case clone trees never
        # become retention evidence; their actual changed inputs were saved
        # before each run by reconstructed_controls.py.
        for family in pins['families']:
            directory = private_audit/family
            if directory.exists():
                for path in directory.rglob('*'):
                    relative = path.relative_to(directory)
                    allowed_case = family == 'primary_scope_family' and relative.as_posix().startswith(('ignoredtmp/verify_runs/', 'ignoredtmp/review_runs/'))
                    if path.is_file() and not path.is_symlink() and (allowed_case or not {'tmp', 'ignoredtmp', '__pycache__'}.intersection(relative.parts)):
                        retained(path, 'final_partial_or_complete/'+family+'/'+relative.as_posix())
        controls_directory = private_audit/'ROOT_RECONSTRUCTED_CONTROLS'
        if controls_directory.exists():
            for path in controls_directory.rglob('*'):
                relative = path.relative_to(controls_directory)
                if path.is_file() and not path.is_symlink() and 'manifest_cases' not in relative.parts:
                    retained(path, 'final_partial_or_complete/reconstructed_controls/'+relative.as_posix())
        try:
            closure_after = strict_closed(pins, AUDIT)
            assert closure_after == closure_before
            for record in inputs: require(record, REPO)
            assert own == {name: sha((HERE/name).read_bytes()) for name in SOURCE_NAMES}
            assert strict_preparation() == preparation_manifest_sha
            assert root_bound == {str(path): sha(path.read_bytes()) for path in [root_script, read_ledger, current_path]}
            final_head = subprocess.run(['/usr/bin/git', 'rev-parse', 'HEAD'], cwd=REPO, capture_output=True,
                                        env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
            assert final_head.returncode == 0 and not final_head.stderr and final_head.stdout.decode().strip() == current['current_head']
            for record in [pins['snapshot_manifest'], pins['diff'], *pins.get('auxiliary', [])]: require(record, AUDIT)
            for record in pins['snapshot_files']:
                require({'path': record['path'], 'size': record['size'], 'sha256': record['sha256']}, AUDIT/'source_snapshot')
            out['authored_members_verified_before_and_after'] = 169
            out['strict_root_closure_before_and_after'] = {'before': closure_before, 'after': closure_after, 'equal': True}
            out['strict_root_exact_recursive_closure_verified'] = True
            out['native_full_file_preimages_before_and_after'] = inputs
            out['current_head_unchanged'] = current['current_head']
            out['root_and_preparation_sources_unchanged'] = own
            out['preparation_manifest_sha256_before_and_after'] = preparation_manifest_sha
        except BaseException as error:
            out['status'] = 'FAIL'; out['integrity_failure'] = traceback.format_exc()
        nested = []
        for path in sorted(support.glob('*_nested/nested_runs.json')):
            for index, item in enumerate(load(path)):
                nested.append({'outer_label': path.parent.name[:-7], 'nested_index': index, **item})
        out['actual_nested_program_runs'] = nested
        out['comparison_exclusion_policy'] = {'clock_keys': sorted(CLOCK_KEYS), 'single_private_path_prefix': {'actual': str(private), 'saved': str(REPO)},
                                               'qualified_differences_remain_in_full_JSON': True, 'broad_runtime_or_native_ignoring': False}
        out['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        shutil.rmtree(private)
        write(output, out)
        support_rows = [row(path, support) for path in sorted(support.rglob('*')) if path.is_file()]
        write(support/'ROOT_SUPPORT_MANIFEST.json', {'schema': 1, 'status': out['status'], 'self_excluding': True,
              'excluded': ['ROOT_SUPPORT_MANIFEST.json'], 'files': support_rows,
              'path_base': 'support_directory', 'support_directory': support.relative_to(AUDIT).as_posix(),
              'root_reproduction_receipt': row(output, AUDIT), 'root_reproduction_receipt_sha256': sha(output.read_bytes()),
              'foreign_corpus_SQL_PDF_OCR_cache_or_private_scratch_retained': False})
    print(json.dumps({'status': out['status'], 'receipt': str(output), 'support': str(support)}, indent=2))
    if out['status'] != 'PASS': raise SystemExit(1)


if __name__ == '__main__':
    main()
