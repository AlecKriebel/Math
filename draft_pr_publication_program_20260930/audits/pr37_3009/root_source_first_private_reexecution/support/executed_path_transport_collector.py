#!/usr/bin/env python3
"""Root-owned three-closed-family replay collector. Preparation is STATIC ONLY.

Run only after root reads this entire source and README. Every writer helper
runs in a fresh exact private repository hierarchy; retained support contains
first-party streams/receipts, never the corpus, PDFs or private scratch trees.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import traceback

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = AUDIT.parents[2]
PYTHON = '/usr/bin/python3'
CLOCK_KEYS = {'at_utc', 'utc', 'timestamp_utc', 'created_at_utc', 'read_at_utc',
              'start_utc', 'end_utc', 'started_utc', 'ended_utc'}
FAMILIES = ['planar_fixed_continuum_family', 'primary_scope_family',
            'recurrence_orientation_family']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(Path(path).read_bytes())


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def row(path, root):
    data = Path(path).read_bytes()
    return {'path': str(Path(path).relative_to(root)), 'size': len(data), 'sha256': sha(data)}


def require_pin(rec, root):
    path = root / rec['path']
    assert path.is_file() and not path.is_symlink(), path
    assert row(path, root) == rec, 'Pinned bytes changed: '+str(path)


def family_actual(directory, family):
    excluded = {'tmp'} if family != 'primary_scope_family' else {'ignoredtmp', '__pycache__'}
    return sorted(str(p.relative_to(directory)) for p in directory.rglob('*')
                  if p.is_file() and not excluded.intersection(p.relative_to(directory).parts))


def verify_closed(pins, closure):
    """Read-only strict checks, including manifest bytes and dated self receipts."""
    for family, info in pins['families'].items():
        for rec in info['members']+[info['manifest']]:
            require_pin(rec, REPO)
        expected = [str(Path(r['path']).relative_to(AUDIT.relative_to(REPO)/family))
                    for r in info['members']]
        if family != 'recurrence_orientation_family':
            expected.append(Path(info['manifest_path']).name)
        assert family_actual(AUDIT/family, family) == sorted(set(expected))
    c = load(closure)
    assert c.get('family') == 'recurrence_orientation_family'
    records = c['files']
    assert len(records) == 21
    advertised = {str(Path(x['path']).relative_to(AUDIT.relative_to(REPO)/FAMILIES[2])):
                  (x['size'], x['sha256']) for x in pins['families'][FAMILIES[2]]['members']}
    actual = {x['path']: (x.get('size', x.get('bytes')), x['sha256']) for x in records}
    assert len(actual) == len(records) and actual == advertised
    return {'manifest_path': str(closure.relative_to(AUDIT)),
            'sha256': sha(closure.read_bytes()), 'member_count': 21}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hamilton-complete-three-page-proof-read-by-root', action='store_true',
                        help='Root alone attests its actual reading of printed pp522–524.')
    parser.add_argument('--recurrence-closure-manifest', type=Path, required=True)
    parser.add_argument('--root-script-path', type=Path,
                        help='Bind root-owned audit-root reproduce_root_closed_families.py wrapper.')
    parser.add_argument('--root-dated-input-rebase-manifest', type=Path,
                        help='Explicit root-authored current native/inventory preimage rebase; immutable science pins cannot change.')
    parser.add_argument('--output', type=Path, default=AUDIT/'ROOT_THREE_CLOSED_FAMILY_REPLAY.json')
    parser.add_argument('--support-directory', type=Path,
                        default=AUDIT/'root_three_closed_family_replay_support')
    args = parser.parse_args()
    assert sys.flags.optimize == 0 and args.hamilton_complete_three_page_proof_read_by_root
    pins = load(HERE/'INPUT_PINS.json')
    assert pins['repository_root'] == str(REPO)
    # macOS /usr/bin/python3 dispatches to the Xcode interpreter recorded in
    # sys.executable rather than resolving as a filesystem symlink.
    assert Path(sys.executable).resolve() == Path(pins['runtime_actual_executable']).resolve()
    rebase = []
    if args.root_dated_input_rebase_manifest:
        rebase_path = args.root_dated_input_rebase_manifest.resolve()
        assert rebase_path.parent == AUDIT and rebase_path.is_file() and not rebase_path.is_symlink()
        rebase_doc = load(rebase_path)
        assert rebase_doc['approved_by_root'] is True and rebase_doc['reason']
        allowed_rebase = {'draft_pr_publication_program_20260930/inventory.json',
                          str((AUDIT/'ROOT_PARTIAL_SCOPE_CERTIFICATE.md').relative_to(REPO))} | {
            'unsolved_math_prioritization/'+name for name in
            ['QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json']}
        replacements = {r['path']: r for r in rebase_doc['files']}
        assert len(replacements) == len(rebase_doc['files']) and set(replacements) <= allowed_rebase
        for old in pins['inputs']:
            if old['path'] in replacements:
                new = replacements[old['path']]
                require_pin(new, REPO)
                rebase.append({'original_pin': old.copy(), 'root_dated_pin': new.copy()})
                old.update(new)
    root_script = args.root_script_path.resolve() if args.root_script_path else Path(__file__).resolve()
    assert root_script.is_file() and not root_script.is_symlink()
    if args.root_script_path:
        assert root_script.parent == AUDIT and root_script.name == 'reproduce_root_closed_families.py'
    root_script_before = sha(root_script.read_bytes())
    closure = args.recurrence_closure_manifest.resolve()
    assert closure.parent == AUDIT and closure.is_file() and not closure.is_symlink()
    output, support = args.output.resolve(), args.support_directory.resolve()
    assert output.parent == AUDIT and not output.exists()
    assert support.parent == AUDIT and support.name not in FAMILIES and not support.exists()
    own_before = {p.name: sha(p.read_bytes()) for p in [Path(__file__), HERE/'capture_runner.py', HERE/'INPUT_PINS.json']}
    recurrence_info = verify_closed(pins, closure)
    for rec in pins['inputs']:
        require_pin(rec, REPO)
    closed_before = {r['path']: r for f in pins['families'].values()
                     for r in f['members']+[f['manifest']]}
    live_before = {r['path']: r for r in pins['inputs']}
    support.mkdir()
    private = HERE/'tmp'/('root_replay_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    private.mkdir(parents=True, exist_ok=False)
    private_audit = private/AUDIT.relative_to(REPO)
    runs, comparisons, exceptions = [], [], []
    out = {'schema': 1, 'status': 'INCOMPLETE', 'root_script_sha256': own_before[Path(__file__).name],
           'original_substantive_turns': 1, 'turn_limit': 5, 'new_substantive_attempts': 0,
           'hamilton1954_complete_three_page_proof_read_by_root': True,
           'hamilton_read_attestation_origin': 'Explicit root-only command-line flag; preparation made no source-read claim.',
           'closed_family_count': 3, 'actual_outer_program_runs': runs,
           'full_structured_receipt_comparisons': comparisons, 'recorded_expected_differences': exceptions,
           'family_manifests': {f: {'manifest_path': i['manifest_path'],
                                  'sha256': i['manifest']['sha256'], 'member_count': i['member_count']}
                                for f, i in pins['families'].items()},
           'support_directory': str(support.relative_to(AUDIT)),
           'comparison_exclusion_policy': 'Only explicit clock keys and documented absolute path replacements. Runtime trace formatting and dated input changes remain explicit differences, never erased.'}
    out['root_script_sha256'] = root_script_before
    out['executed_collector_sha256'] = own_before[Path(__file__).name]
    out['root_script_path'] = str(root_script.relative_to(AUDIT))
    out['root_dated_input_rebase'] = rebase
    if args.root_dated_input_rebase_manifest:
        out['root_dated_input_rebase_manifest'] = row(rebase_path, AUDIT)
    shutil.copyfile(root_script, support/'executed_root_entrypoint.py')
    git_head = subprocess.run(['/usr/bin/git', 'rev-parse', 'HEAD'], cwd=REPO,
                              capture_output=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
    (support/'live_head_preimage.stdout').write_bytes(git_head.stdout)
    (support/'live_head_preimage.stderr').write_bytes(git_head.stderr)
    assert git_head.returncode == 0 and not git_head.stderr
    live_head = git_head.stdout.decode().strip()
    out['actual_live_git_head_preimage'] = live_head
    out['family_manifests'][FAMILIES[2]] = recurrence_info

    def retain(source, label):
        dst = support/(label+'.json')
        assert not dst.exists()
        shutil.copyfile(source, dst)
        return dst

    def run(label, target, *arguments, instrument=True, env=None):
        argv = [PYTHON, str(target), *map(str, arguments)]
        if instrument:
            argv = [PYTHON, str(HERE/'capture_runner.py'), str(target), str(support/(label+'_nested')), *map(str, arguments)]
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        cp = subprocess.run(argv, cwd=private if private_audit.exists() else REPO,
                            capture_output=True, timeout=600, env=env or os.environ.copy())
        item = {'label': label, 'argv': argv, 'script_sha256': sha(target.read_bytes()),
                'started_utc': started, 'exit_code': cp.returncode,
                'exit': cp.returncode, 'returncode': cp.returncode}
        for name in ['stdout', 'stderr']:
            dst = support/(label+'.'+name)
            dst.write_bytes(getattr(cp, name)); item[name] = row(dst, AUDIT)
        runs.append(item)
        write(support/'outer_runs.json', runs)
        assert cp.returncode == 0, 'Outer program failed; streams retained: '+label
        return cp

    def normalize(value):
        if isinstance(value, dict):
            return {k: normalize(v) for k, v in value.items() if k not in CLOCK_KEYS}
        if isinstance(value, list):
            return [normalize(x) for x in value]
        if isinstance(value, str):
            value = value.replace(str(private), str(REPO))
            value = value.replace(str(REPO), '/Users/alec/Documents/Math')
            value = value.replace(str(Path('/Users/alec/Documents/Math')/'draft_pr_publication_program_20260930/audits/pr37_3009'/FAMILIES[2]/'tmp/replay_env/bin/python'), PYTHON)
            value = value.replace(pins['runtime_actual_executable'], PYTHON)
        return value

    def differences(a, b, at='$'):
        if type(a) != type(b):
            return [{'path': at, 'actual': a, 'saved': b}]
        if isinstance(a, dict):
            if set(a) != set(b):
                return [{'path': at, 'actual_keys': sorted(a), 'saved_keys': sorted(b)}]
            return [d for k in a for d in differences(a[k], b[k], at+'/'+k)]
        if isinstance(a, list):
            if len(a) != len(b):
                return [{'path': at, 'actual_length': len(a), 'saved_length': len(b)}]
            return [d for i in range(len(a)) for d in differences(a[i], b[i], at+'/'+str(i))]
        return [] if a == b else [{'path': at, 'actual': a, 'saved': b}]

    def compare(label, actual, saved, required=True):
        a, b = load(actual), load(saved)
        delta = differences(normalize(a), normalize(b))
        comparisons.append({'label': label, 'actual': row(actual, AUDIT), 'saved': row(saved, AUDIT),
                            'complete_JSON_byte_equal': actual.read_bytes() == saved.read_bytes(),
                            'equal_after_clock_and_path_exclusions': not delta,
                            'differences': delta, 'required_equality': required})
        write(support/'structured_comparisons.json', comparisons)
        if required:
            assert not delta, 'Structured receipt mismatch: '+label
        return delta

    def check_frozen_output(path, expected):
        assert path.read_bytes() == expected.read_bytes()
        assert load(path) == load(expected)
        j = load(path)
        assert j['failed'] == 0 and j['passed'] == len(j['checks'])
        return retain(path, 'generated_'+str(path.relative_to(private_audit)).replace('/', '__').replace('.json', ''))

    try:
        # Safe closed validators FIRST; recurrence writer verifier is intentionally not run live.
        run('live_planar_readonly_manifest', AUDIT/FAMILIES[0]/'verify_manifest.py', instrument=False)
        run('live_primary_readonly_manifest', AUDIT/FAMILIES[1]/'replay_audit.py', '--verify-manifest', instrument=False)
        cp = subprocess.run([PYTHON, '-c', "import sympy; assert sympy.__version__ == '1.14.0'; print(sympy.__version__)"], capture_output=True)
        (support/'runtime.stdout').write_bytes(cp.stdout); (support/'runtime.stderr').write_bytes(cp.stderr)
        assert cp.returncode == 0
        for rec in pins['inputs'] + [r for f in pins['families'].values() for r in f['members']+[f['manifest']]]:
            src, dst = REPO/rec['path'], private/rec['path']
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                shutil.copy2(src, dst)
            require_pin(rec, private)
        # Protect raw cache, native read inputs and administrative input copies.
        # Snapshot files retain their exact original modes: the primary helper
        # copytree preserves them when creating its writable mutation cases.
        for rec in pins['inputs']:
            if 'source_snapshot' not in Path(rec['path']).parts:
                (private/rec['path']).chmod(0o444)
        (private/'.git').symlink_to(REPO/'.git', target_is_directory=True)
        bindir = private/'root_readonly_bin'; bindir.mkdir()
        git = bindir/'git'
        git.write_text('#!/usr/bin/python3\nimport os,sys\nallowed={"ls-tree","cat-file","diff","show","branch","rev-parse","merge-base","check-ignore"}\nassert sys.argv[1] in allowed\nassert sys.argv[1]!="branch" or sys.argv[2:]==["--show-current"]\nos.environ["GIT_OPTIONAL_LOCKS"]="0"\nos.execv("/usr/bin/git",["/usr/bin/git",*sys.argv[1:]])\n')
        git.chmod(0o755)
        metadata = private/'root_historical_pr_metadata_input.json'
        shutil.copy2(private_audit/FAMILIES[1]/'ignoredtmp/current_pr_metadata.json', metadata)
        # The helper writes its own output at this path; the shim's separate
        # pinned readonly input cannot be overwritten by that writer.
        (private_audit/FAMILIES[1]/'ignoredtmp/current_pr_metadata.json').chmod(0o644)
        gh = bindir/'gh'
        gh.write_text('#!/usr/bin/python3\nfrom pathlib import Path\nimport sys\nassert sys.argv[1:]==["api","repos/AlecKriebel/Math/pulls/37"]\nsys.stdout.buffer.write(Path('+repr(str(metadata))+').read_bytes())\n')
        gh.chmod(0o755)
        env = dict(os.environ, PATH=str(bindir)+os.pathsep+os.environ.get('PATH', ''),
                   GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1')
        out['private_input_transport'] = 'Exact hierarchy and source modes; regular readonly raw/SQL/import/native copies; private source snapshot remains writable for copytree mutation cases and is never edited directly; live .git symlink accessed only by allowlisted readonly Git wrapper; gh served pinned historical bytes locally, without network.'
        out['historical_metadata_transport'] = row(metadata, private)

        planar = private_audit/FAMILIES[0]
        run('planar_manifest_controls_private', planar/'verify_manifest.py', env=env)
        run('planar_608_controls', planar/'controls.py', env=env)
        fresh = retain(planar/'control_results.json', 'planar_control_results')
        compare('planar_complete_608_receipt', fresh, AUDIT/FAMILIES[0]/'control_results.json')
        assert load(fresh)['passed'] == len(load(fresh)['checks']) == 608
        assert load(support/'planar_manifest_controls_private.stdout')['passed'] == 9

        primary = private_audit/FAMILIES[1]
        # Manifest controls MUST precede the ordinary writer replay.
        run('primary_six_manifest_controls', primary/'manifest_controls.py', env=env)
        fresh = retain(primary/'MANIFEST_CONTROLS.json', 'primary_manifest_controls')
        delta = compare('primary_dated15_vs_closed17_manifest_controls', fresh, AUDIT/FAMILIES[1]/'MANIFEST_CONTROLS.json', required=False)
        allowed_paths = {'$/tested_manifest_sha256', '$/cases/0/stdout', '$/cases/5/stdout'}
        # Failure tracebacks differ in path length because only their last500 chars are stored.
        tail_paths = {'$/cases/'+str(i)+'/stderr_tail' for i in range(1, 5)}
        assert all(d['path'] in allowed_paths | tail_paths for d in delta)
        old, new = load(AUDIT/FAMILIES[1]/'MANIFEST_CONTROLS.json'), load(fresh)
        manifest_nested = load(support/'primary_six_manifest_controls_nested/nested_runs.json')
        assert len(manifest_nested) == 6
        assert old['tested_manifest_sha256'] == 'd12686d6d900c7587e45706d6301ef695bce9168668b7863d8ba14e10347d4ea'
        assert new['tested_manifest_sha256'] == pins['families'][FAMILIES[1]]['manifest']['sha256']
        for i, case in enumerate(new['cases']):
            assert case['actual_pass'] == case['expected_pass'] == (i in [0, 5])
            if i in [0, 5]:
                assert json.loads(case['stdout'])['files'] == 17
                assert json.loads(old['cases'][i]['stdout'])['files'] == 15
            else:
                assert 'AssertionError: Authored file set or hash mismatch' in case['stderr_tail']
                complete_stderr = Path(manifest_nested[i]['stderr']['path']).read_text()
                # The source receipt kept only last500 chars. Compare that exact
                # interface AFTER complete-stream path replacement, explaining
                # why slicing a longer private path first gives another prefix.
                assert normalize(complete_stderr)[-500:] == normalize(old['cases'][i]['stderr_tail'])
        exceptions.append({'label': 'primary_dated_manifest_control_inputs', 'historical_members': 15,
                           'fresh_closed_members': 17, 'historical_manifest_sha256': old['tested_manifest_sha256'],
                           'fresh_manifest_sha256': new['tested_manifest_sha256'],
                           'precise_differences': delta,
                           'meaning': 'Different sealed inputs; positive file counts/hash differ. Remaining predicates match; intended failure body/exit checked against full captured streams.'})
        run('primary_14_original_code_prose_runs', primary/'replay_audit.py', env=env)
        for name in ['CORPUS_PROVENANCE.json', 'GIT_ACCOUNTING_PROVENANCE.json', 'REPLAY_AND_CORRUPTION_CONTROLS.json']:
            fresh = retain(primary/name, 'primary_'+name[:-5])
            if name == 'GIT_ACCOUNTING_PROVENANCE.json':
                delta = compare('primary_complete_'+name, fresh, AUDIT/FAMILIES[1]/name, required=False)
                current_inventory = load(REPO/'draft_pr_publication_program_20260930/inventory.json')
                selected = [x for x in current_inventory['items'] if x['number'] == 37]
                actual_git = load(fresh)
                saved_git = load(AUDIT/FAMILIES[1]/name)
                assert len(selected) == 1 and actual_git['inventory_item_historical'] == selected
                assert any(x['root_dated_pin']['path'] == 'draft_pr_publication_program_20260930/inventory.json' for x in rebase)
                for key in ['number','headRefOid','headRefName','baseRefName','title','url','isDraft','outcome']:
                    assert selected[0][key] == saved_git['inventory_item_historical'][0][key]
                assert all((d['path'] == '$/current_main_head' and d['actual'] == live_head) or d['path'].startswith('$/inventory_item_historical/0') for d in delta)
                assert load(fresh)['current_main_head'] == live_head
                exceptions.append({'label': 'primary_dated_current_main_head', 'precise_differences': delta,
                                   'actual_preimage': live_head, 'original_base_head_blobs_and_diff_match': True})
            else:
                compare('primary_complete_'+name, fresh, AUDIT/FAMILIES[1]/name)
        ledger = retain(primary/'READ_EXECUTION_LEDGER.json', 'primary_READ_EXECUTION_LEDGER')
        delta = compare('primary_complete_read_execution_ledger', ledger, AUDIT/FAMILIES[1]/'READ_EXECUTION_LEDGER.json', required=False)
        # Hash/length differences caused solely by private absolute paths in failed stderr
        # are accounted for using the full retained stream and full saved stderr below.
        rows = load(ledger)['rows']
        allowed = {'$/rows/'+str(i)+'/'+key for i, r in enumerate(rows)
                   if r.get('returncode') == 1 for key in ['stderr_sha256', 'stderr_bytes']}
        for i, r in enumerate(rows):
            if r.get('argv') == ['git', 'rev-parse', 'HEAD']:
                assert r['stdout_sha256'] == sha((live_head+'\n').encode())
                allowed.add('$/rows/'+str(i)+'/stdout_sha256')
            if r.get('path') in {x['root_dated_pin']['path'] for x in rebase}:
                new = next(x['root_dated_pin'] for x in rebase if x['root_dated_pin']['path'] == r['path'])
                assert r['sha256'] == new['sha256'] and r['bytes'] == new['size']
                allowed.update({'$/rows/'+str(i)+'/sha256', '$/rows/'+str(i)+'/bytes'})
        assert all(d['path'] in allowed for d in delta)
        nested = load(support/'primary_14_original_code_prose_runs_nested/nested_runs.json')
        programs = [r for r in nested if r['argv'][0] == PYTHON]
        assert len(programs) == 14
        cases = load(primary/'REPLAY_AND_CORRUPTION_CONTROLS.json')['cases']
        for c in cases:
            for execution in c['executions']:
                matches = [r for r in programs if str(primary/'ignoredtmp/replays'/c['name']/execution['script']) == r['argv'][1]]
                assert len(matches) == 1
                stream = matches[0]
                assert stream['exit_code'] == execution['returncode']
                if execution['returncode']:
                    assert normalize(Path(stream['stderr']['path']).read_text()) == normalize(execution['stderr_tail'])
                else:
                    receipt = primary/'ignoredtmp/replays'/c['name']/Path(execution['script']).with_name('check_results.json' if execution['script']=='check_controls.py' else 'independent_results.json')
                    check_frozen_output(receipt, private_audit/'source_snapshot'/receipt.name if execution['script']=='check_controls.py' else private_audit/'source_snapshot/independent_review/independent_results.json')
        exceptions.append({'label': 'primary_ledger_failed_stderr_path_hashes', 'precise_differences': delta,
                           'evidence': 'Full captured failed streams agree after private-root path replacement; hash and byte lengths change because the complete paths change.'})

        recurrence = private_audit/FAMILIES[2]
        run('recurrence_independent_controls', recurrence/'check_independent_controls.py', env=env)
        fresh = retain(recurrence/'independent_control_results.json', 'recurrence_independent_control_results')
        compare('recurrence_complete_independent_control_receipt', fresh, AUDIT/FAMILIES[2]/'independent_control_results.json')
        assert load(fresh)['independent_groups_passed'] == 6 and load(fresh)['counter_controls_rejected'] == 11
        run('recurrence_five_original_code_cases', recurrence/'replay_original.py', env=env)
        fresh = retain(recurrence/'original_replay_receipts.json', 'recurrence_original_replay_receipts')
        delta = compare('recurrence_complete_five_case_receipt', fresh, AUDIT/FAMILIES[2]/'original_replay_receipts.json', required=False)
        assert all(d['path'] in {'$/receipts/'+str(i)+'/stderr' for i in range(2, 5)} for d in delta)
        j = load(fresh); assert len(j['receipts']) == 5 and j['all_expected_outcomes']
        saved_recurrence = load(AUDIT/FAMILIES[2]/'original_replay_receipts.json')
        for index, receipt in enumerate(j['receipts']):
            if receipt['expected_failure']:
                assert receipt['return_code'] == 1
                assert receipt['stderr'].splitlines()[-1] == 'AssertionError: '+receipt['expected_failure']
                assert 'ModuleNotFoundError' not in receipt['stderr']
                def traceback_body(text):
                    return '\n'.join(line for line in normalize(text).splitlines()
                                     if not re.fullmatch(r'\s*[~^]+\s*', line))
                assert traceback_body(receipt['stderr']) == traceback_body(saved_recurrence['receipts'][index]['stderr'])
            else:
                assert receipt['return_code'] == 0 and receipt['stderr'] == ''
                assert all(v['structurally_equal'] and v['actual_sha256'] == v['saved_sha256']
                           for v in receipt['saved_result_comparison'].values())
                actual = recurrence/'tmp/original_replay'/receipt['name']/next(iter(receipt['saved_result_comparison']))
                expected = private_audit/'source_snapshot'/('independent_review' if receipt['name']=='historical_independent_baseline' else '')/actual.name
                check_frozen_output(actual, expected)
                expected_stdout = expected.read_bytes() if receipt['name']=='baseline' else (json.dumps({k:v for k,v in load(expected).items() if k!='checks'},indent=2)+'\n').encode()
                assert receipt['stdout'].encode() == expected_stdout
        exceptions.append({'label': 'recurrence_runtime_traceback_formatter', 'precise_differences': delta,
                           'fresh_runtime': PYTHON, 'saved_runtime': load(AUDIT/FAMILIES[2]/'original_replay_receipts.json')['python_executable'],
                           'meaning': 'Complete trace differences retained. Intended AssertionError name, source statement and exit1 checked; formatter underlines are not claimed BYTE identical.'})
        retain(recurrence/'original_replay_attempts.json', 'recurrence_original_replay_attempts')

        # Root original collector has one hardcoded repository path. Preserve the
        # complete first-party revision and exact single path-only edit receipt.
        source = private_audit/'reproduce_root_original.py'
        before = source.read_bytes(); old = b"R=Path('/Users/alec/Documents/Math')"
        assert before.count(old) == 1
        after = before.replace(old, ('R=Path('+repr(str(private))+')').encode())
        revised = private_audit/'root_original_private_path_revision.py'; revised.write_bytes(after)
        shutil.copyfile(revised, support/'root_original_private_path_revision.py')
        write(support/'root_original_path_revision.json', {'original_sha256': sha(before), 'revised_sha256': sha(after),
              'exact_replacement_before': old.decode(), 'exact_replacement_after': ('R=Path('+repr(str(private))+')'),
              'purpose': 'One private repository-root path change; all checking statements unchanged.'})
        for name in ['ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json', 'pinned_problem.json', 'pinned_importer_prior_fallback.json']:
            (private_audit/name).unlink()
        run('root_original_full_integrity_and_replay', revised, env=env)
        fresh = retain(private_audit/'ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json', 'root_original_full_integrity_and_replay')
        delta = compare('root_complete_original_integrity_receipt', fresh, AUDIT/'ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json', required=False)
        rebased_native = {Path(x['root_dated_pin']['path']).name: x['root_dated_pin']['sha256']
                          for x in rebase if Path(x['root_dated_pin']['path']).name in ['QUEUE.md', 'state.json', 'history.jsonl']}
        assert all(d['path'] == '$/live_queue_state_history_unchanged/'+name and d['actual'] == digest
                   for d in delta for name, digest in [(d['path'].split('/')[-1], rebased_native.get(d['path'].split('/')[-1]))])
        exceptions.append({'label': 'root_dated_native_preimage', 'precise_differences': delta,
                           'binding': rebase, 'meaning': 'Explicit root-authorized preimage changes; before/after live hashes remain exact.'})
        assert load(fresh)['actual_original_replays'][1]['checks'] == 8462
        for path in (private_audit/'tmp').rglob('*.json'):
            if path.name in ['check_results.json', 'independent_results.json']:
                expected = private_audit/'source_snapshot'/('independent_review' if path.name=='independent_results.json' else '')/path.name
                check_frozen_output(path, expected)
        out['original_full_integrity_replay'] = load(fresh)
        out['status'] = 'PASS'
    except BaseException as error:
        out['status'] = 'FAIL'
        out['failure'] = {'type': type(error).__name__, 'message': str(error), 'traceback': traceback.format_exc()}
    finally:
        # Always check original self/manifests/authored members AND native live inputs.
        try:
            verify_closed(pins, closure)
            assert sha(closure.read_bytes()) == recurrence_info['sha256']
            if args.root_dated_input_rebase_manifest:
                assert row(rebase_path, AUDIT) == out['root_dated_input_rebase_manifest']
            for rec in live_before.values():
                require_pin(rec, REPO)
            assert own_before == {p.name: sha(p.read_bytes()) for p in [Path(__file__), HERE/'capture_runner.py', HERE/'INPUT_PINS.json']}
            assert sha(root_script.read_bytes()) == root_script_before
            final_head = subprocess.run(['/usr/bin/git', 'rev-parse', 'HEAD'], cwd=REPO,
                                        capture_output=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
            assert final_head.returncode == 0 and final_head.stdout == git_head.stdout and not final_head.stderr
            out['live_git_head_unchanged'] = live_head
            out['authored_members_verified_before_and_after'] = 48
            out['closed_members_and_manifest_self_bytes_unchanged'] = list(closed_before.values())
            out['live_read_inputs_unchanged'] = list(live_before.values())
            out['root_source_and_capture_and_pins_unchanged'] = own_before
        except BaseException as error:
            out['status'] = 'FAIL'
            out['integrity_failure'] = repr(error)
        out['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        # Scratch is deliberately not a retained artifact. Only first-party
        # complete actual streams, full generated JSON and path revision survive.
        shutil.rmtree(private)
        write(output, out)
        support_rows = [row(p, support) for p in sorted(support.rglob('*')) if p.is_file()]
        write(support/'ROOT_SUPPORT_MANIFEST.json', {'self_excluding': True, 'files': support_rows,
              'excluded': ['ROOT_SUPPORT_MANIFEST.json'], 'foreign_corpus_or_PDF_retained': False})
    print(json.dumps({'status': out['status'], 'receipt': str(output), 'support': str(support)}, indent=2))
    if out['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
