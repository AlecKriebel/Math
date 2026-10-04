"""SOURCE ONLY. ROOT launches this closure child under an external actual capture.

This handwritten V2 administrative closer imports no proposed production source.
Rejected V1 and the actually completed adverse review remain preserved history.
It closes this preparation only and grants no future ROOT/acceptance authority.
"""
from pathlib import Path, PurePosixPath
import argparse, ctypes, datetime as dt, hashlib, json, math, os, re, stat

H = Path(__file__).resolve().parent
A = H.parent
R = A.parents[2]
C = A / 'reviewed_candidate'
W = A / 'current_whole_adversary_family'
NAME = 'PREPARATION_MANIFEST.json'
CURRENT = '66239699390b279235c4064208e63134049a5804884818de9176d377476a189d'
WHOLE = 'be3fa099c6a080d5f9cddcf42f39ac51b51c8f89cd76d09fb5d360a99d1990e2'
ROOT_WHOLE = 'ed0cc07fd852881a0b9a9893e6c2ec7f25e6e6d2f3d1bfb26bfa88a7a0b17b54'
V1_SHA = 'd97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab'
IMMUTABLE = {'SOURCE_STATUS.md', 'independent_review/independent_checks.py',
 'independent_review/independent_results.json', 'provenance.json',
 'source_record.json', 'turns.json', 'verification.json', 'verify.py'}
ADMIN = {'status.json', 'readiness.json', 'independent_review/verdict.json',
 'independent_review/review_summary.json'}
PRODUCTION = ['pr46_guards.py', 'seal_final_evidence.py',
 'capture_root_final_operation.py', 'integrate_reviewed_partial.py',
 'state_mirror_reconciliation.py', 'verify_post_acceptance.py']

def need(ok, message):
    if not ok: raise ValueError(message)

def sha(raw): return hashlib.sha256(raw).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def same(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b

def parse(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'Duplicate JSON key')
            out[key] = value
        return out
    def floating(value):
        value = float(value)
        need(math.isfinite(value), 'Nonfinite JSON value')
        return value
    return json.loads(raw, object_pairs_hook=pairs, parse_float=floating,
      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))

def relative(value):
    need(type(value) is str and value and value != '.' and '\\' not in value
      and '\0' not in value, 'Invalid relative path')
    path = PurePosixPath(value)
    need(not path.is_absolute() and path.as_posix() == value
      and not {'.', '..', '.git', '__pycache__'}.intersection(path.parts),
      'Noncanonical relative path')
    return path

def read(path, row=None, mode=None):
    path = Path(path)
    need(path.is_absolute(), 'Absolute read path required')
    need(not path.is_symlink() and stat.S_ISREG(path.lstat().st_mode)
      and all(not p.is_symlink() for p in path.parents), 'Unsafe regular input')
    raw = path.read_bytes()
    if row is not None:
        need(type(row['bytes']) is int and row['bytes'] >= 0
          and len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Bound body differs')
    if mode is not None:
        need(type(mode) is int and stat.S_IMODE(path.stat().st_mode) == mode,
          'Full permission mode differs')
    return raw

def tree(base):
    need(base.is_dir() and not base.is_symlink()
      and all(not p.is_symlink() for p in base.parents), 'Unsafe corpus root')
    files, directories, folded = {}, set(), set()
    for path in sorted(base.rglob('*')):
        name = path.relative_to(base).as_posix()
        relative(name)
        need(name.casefold() not in folded, 'Case-alias duplicate')
        folded.add(name.casefold())
        mode = path.lstat().st_mode
        need(not path.is_symlink(), 'Symlink member')
        if stat.S_ISDIR(mode): directories.add(name)
        else:
            need(stat.S_ISREG(mode), 'FIFO/special member')
            files[name] = path
    implied = {p.as_posix() for n in files for p in PurePosixPath(n).parents
      if p.as_posix() != '.'}
    need(directories == implied, 'Extra empty directory or incomplete topology')
    return files, directories

def closed(base, name, count, digest):
    raw = read(base / name, mode=0o444)
    need(sha(raw) == digest, 'Fixed closed manifest differs')
    obj = parse(raw)
    need(type(obj['files_count']) is int and obj['files_count'] == count
      and same(obj['self_excluded'], [name]), 'Closed manifest count/self differs')
    rows = obj['files']
    need(type(rows) is list and len(rows) == count
      and len({z['path'] for z in rows}) == count, 'Duplicate/incorrect closed rows')
    files, dirs = tree(base)
    need(set(files) == {z['path'] for z in rows} | {name}, 'Exact closure membership differs')
    for row in rows:
        relative(row['path'])
        read(base / row['path'], row, 0o444)
    return obj, dirs

def capture(directory, expected_exit):
    obj = parse(read(directory / 'CAPTURE.json'))
    pre = parse(read(directory / 'PRELAUNCH.json'))
    need(obj['actual_execution'] is True and obj['completed'] is True
      and type(obj['pid']) is int and obj['pid'] > 0
      and type(obj['operator_pid']) is int and obj['operator_pid'] > 0
      and type(obj['exit_code']) is int and obj['exit_code'] == expected_exit
      and obj['source_unchanged'] is True, 'Own actual capture differs')
    need(dt.datetime.fromisoformat(pre['created_utc']) <=
      dt.datetime.fromisoformat(obj['started_utc']) <=
      dt.datetime.fromisoformat(obj['finished_utc']), 'Capture chronology differs')
    need(sha(read(directory / 'PRELAUNCH_SOURCE.py')) == pre['source_sha256'],
      'Captured source differs')
    if 'prelaunch' in obj:
        need(same(obj['prelaunch'], pre) and obj['operator_unchanged'] is True
          and sha(read(directory / 'PRELAUNCH_OPERATOR.py')) == pre['operator_sha256']
          and obj['status'] == ('PASS' if expected_exit == 0 else 'FAIL'),
          'Complete operation capture differs')
    else:
        need(obj['argv'] == pre['argv'] and obj['cwd'] == pre['cwd']
          and obj['source_sha256'] == pre['source_sha256'], 'Git capture prelaunch differs')
    for channel in ['stdout', 'stderr']:
        need(obj[channel]['path'] == channel + '.bin', 'Literal full stream required')
        read(directory / obj[channel]['path'], obj[channel])
    return obj

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-source-report-sha256', required=True)
    parser.add_argument('--expected-controls-sha256', required=True)
    args = parser.parse_args()
    need(__debug__ and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0'),
      'Optimization prohibited')
    need(re.fullmatch('[0-9a-f]{64}', args.expected_source_report_sha256),
      'Explicit report SHA256 required')
    need(re.fullmatch('[0-9a-f]{64}', args.expected_controls_sha256), 'Explicit completed controls SHA256 required')
    need(not (H / NAME).exists() and not (H / NAME).is_symlink(), 'Already closed')
    need(sha(read(H / 'FINAL_SOURCE_REPORT.md')) == args.expected_source_report_sha256,
      'Source report differs')
    rejected, unused_dirs = closed(A/'acceptance_preparation_family', NAME, 166, V1_SHA)
    need(same(rejected, parse(read(H/'EXPECTED_REJECTED_V1_MANIFEST.json'))), 'Entire rejected V1 source differs')
    repair = parse(read(H/'SOURCE_REPAIR_BINDINGS.json'))
    need(repair['status']=='COMPLETED_REJECTED_V1_ADVERSE_BINDINGS'
      and repair['closed_adverse_binding_completed'] is True
      and repair['superseded_v1_manifest_sha256']==V1_SHA
      and repair['future_acceptance_approved'] is False
      and repair['production_imported_compiled_executed'] is False, 'Completed actual adverse bindings required')
    for row in repair['complete_first_party_refs']:
        relative(row['path']);read(R/row['path'],row,row['full_mode'])
    ap=R/repair['closed_adverse_manifest']['path']
    need(ap.parent==A/'acceptance_source_adversary_family', 'Exact rejected adverse family')
    am=parse(read(ap,repair['closed_adverse_manifest'],0o444))
    closed(ap.parent,ap.name,am['files_count'],repair['closed_adverse_manifest']['sha256'])
    need(same(am,parse(read(H/'EXPECTED_REJECTED_V1_ADVERSE_MANIFEST.json'))), 'Entire closed adverse manifest differs')
    av=parse(read(R/repair['closed_adverse_verdict']['path'],repair['closed_adverse_verdict'],0o444))
    need(same(av,parse(read(H/'EXPECTED_REJECTED_V1_ADVERSE_VERDICT.json')))
      and av['mandatory_corrections'] and 'S1' in json.dumps(av['mandatory_corrections'])
      and av['production_imported_compiled_executed'] is False
      and av['future_acceptance_approved'] is False, 'Actual final adverse verdict differs')
    ar=parse(read(R/repair['root_complete_adverse_inspection']['path'],repair['root_complete_adverse_inspection']))
    need(same(ar,parse(read(H/'EXPECTED_ROOT_REJECTED_V1_INSPECTION.json')))
      and same(ar['complete_VERDICT_object'],av), 'Entire genuine ROOT adverse read differs')
    candidate, cdirs = closed(C, 'MANIFEST.json', 946, CURRENT)
    whole, wdirs = closed(W, 'MANIFEST.json', 245, WHOLE)
    need(len(cdirs) == 142 and len(wdirs) == 49, 'Fixed directory count differs')
    need(same(whole, parse(read(H / 'EXPECTED_WHOLE_MANIFEST.json'))),
      'Entire whole manifest differs')
    inputs = parse(read(H / 'INPUT_BINDINGS.json'))
    need(inputs['whole_binding_completed'] is True and inputs['external_input_count'] == 1877
      and inputs['closed_whole_manifest']['sha256'] == WHOLE
      and inputs['closed_root_whole_inspection']['sha256'] == ROOT_WHOLE,
      'Actual completed whole binding differs')
    root = parse(read(A / 'ROOT_WHOLE_CURRENT_REVIEW.json',
      inputs['closed_root_whole_inspection']))
    need(same(root, parse(read(H / 'EXPECTED_ROOT_WHOLE_REVIEW.json')))
      and root['schema'] == 'pr46-root-complete-closed-whole-inspection/v1',
      'Entire genuine ROOT whole inspection differs')
    verdict = parse(read(W / 'VERDICT.json', inputs['closed_whole_result'], 0o444))
    need(same(verdict, parse(read(H / 'EXPECTED_WHOLE_VERDICT.json')))
      and verdict['verdict'] == 'PASS_EXACT_CURRENT_KNOWN_RESULT_NO_MANDATORY_CORRECTION'
      and verdict['mandatory_corrections'] == [], 'Whole verdict differs')
    need(same(parse(read(W / 'READBACK_RESULT.json', inputs['closed_whole_external_inventory'], 0o444)),
      parse(read(H / 'EXPECTED_EXTERNAL_INPUT_INVENTORY.json'))), 'Full readback differs')
    external = inputs['external_input_rows']
    need(len(external) == 1877 and len({z['path'] for z in external}) == 1877,
      'External input membership differs')
    for row in external: read(Path(row['path']), row, row['full_mode'])
    for row in inputs['pins'].values():
        relative(row['path']); read(R / row['path'], row)
    for key in ['previous_mirror', 'previous_post', 'previous_root_post']:
        row = inputs[key]; relative(row['path']); read(R / row['path'], row)
    post = parse(read(R / inputs['previous_post']['path']))
    rootpost = parse(read(R / inputs['previous_root_post']['path']))
    need(same(post, rootpost['entire_post']) and rootpost['completed_primary_prs'] == 35,
      'Entire actual PR45 predecessor post differs')
    deps = parse(read(C / 'CURRENT_DEPENDENCIES.json'))
    need(same(deps, parse(read(H / 'EXPECTED_CURRENT_DEPENDENCIES.json')))
      and len(deps['files']) == 826, 'Whole current dependencies differ')
    for row in deps['files']:
        relative(row['path']); read(A / row['path'], row)
    # Dated native4/main observations never authorize a future acceptance.
    native4 = {'draft_pr_publication_program_20260930/inventory.json',
      'unsolved_math_prioritization/QUEUE.md', 'unsolved_math_prioritization/state.json',
      'unsolved_math_prioritization/history.jsonl'}
    need(len(deps['current_native13']) == 13, 'Current dependency native count differs')
    for row in deps['current_native13']:
        if row['path'] not in native4: read(R / row['path'], row, row['full_mode'])
    freeze = parse(read(A / 'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json'))
    need(same(freeze, parse(read(H / 'EXPECTED_ROOT_CURRENT_FREEZE.json')))
      and freeze['frozen_inner_prefix_commands'] == 43
      and freeze['final_original_inner_commands'] == 45, 'Dated 43/45 inner records differ')
    for row in freeze['complete_stream_members']:
        relative(row['path']); read(A / row['path'], row)
    snapshot = parse(read(A / 'snapshot_manifest.json'))
    need(len(snapshot['files']) == 13, 'Original snapshot count differs')
    for row in snapshot['files']:
        relative(row['relative_path'])
        raw = read(A / 'source_snapshot' / row['relative_path'], row, 0o444)
        need(raw == read(C / 'original_archive' / row['relative_path']), 'Original13 archive differs')
    for name in IMMUTABLE:
        need(read(C / name) == read(A / 'source_snapshot' / name), 'Literal operative original differs')
    admin = parse(read(H / 'EXPECTED_CURRENT_ADMIN.json'))
    for name in ADMIN:
        need(same(parse(read(C / name)), admin), 'Entire current administration differs')
    need(same(parse(read(C / 'turns.json')), parse(read(H / 'EXPECTED_ORIGINAL_LEDGER.json'))),
      'Literal complete object ledger differs')
    for name in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json', 'DRAFT_FINAL_PLAN.json']:
        obj = parse(read(H / name))
        for key, value in obj.items():
            if key.startswith('root_') and key.endswith('_completed'):
                need(value is False, 'Fabricated future ROOT completion')
        need(obj['independent_whole_current_pass'] is False, 'Fabricated future whole approval')
        for key in ['created_utc', 'acceptance_source_manifest', 'acceptance_source_verdict',
          'root_source_inspection', 'root_bindings', 'root_bindings_sha256',
          'preparation_manifest_sha256', 'whole_manifest_sha256']:
            if key in obj: need(obj[key] is None, 'Fabricated future authority binding')
    scope = parse(read(H / 'SCIENTIFIC_SCOPE.json'))
    need(scope['full_problem_solved'] is True and scope['project_solved'] is False
      and scope['campaign_new_discovery'] is False and scope['novelty_claimed'] is False
      and scope['source_publication_kind'] == '2020 preprint'
      and scope['original_substantive_attempts'] == 0
      and scope['original_source_verification_responses'] == 1
      and scope['new_substantive_attempts'] == 0 and scope['audit_turns'] == 0
      and scope['paper_or_new_doi_or_tracker'] is False, 'Scientific scope differs')
    status = parse(read(H / 'SOURCE_STATUS.json'))
    need(status['status'] == 'READY_SOURCE_ONLY_CLOSURE'
      and status['future_acceptance_approved'] is False
      and status['production_imported_compiled_executed'] is False, 'Source status differs')
    actuals=sorted(H.glob('*_ACTUAL_CAPTURE/CAPTURE.json'))
    need(len(actuals)>=5, 'Complete own authoring/repair/binding/closure-source/controls captures required')
    captures={p.parent.name:capture(p.parent,parse(read(p))['exit_code']) for p in actuals}
    selected=status['private_controls_capture']
    need(selected in captures, 'Exact successful private controls capture required')
    control=captures[selected]
    need(control['exit_code']==0 and control['status']=='PASS'
      and control['prelaunch']['source_sha256']==sha(read(H/'independent_controls_v2.py'))
      and control['prelaunch']['operator_sha256']==sha(read(H/'capture_owned_operation.py')),
      'Completed successful current V2 controls source/operator identity differs')
    raw_result=read(H/'OWN_CONTROL_RESULTS.json')
    need(sha(raw_result)==args.expected_controls_sha256, 'Complete actual V2 controls pin differs')
    result=parse(raw_result)
    need(result['schema']=='pr46-acceptance-source-v2-private-controls/v1'
      and result['status']=='PASS_PRIVATE_SOURCE_ONLY_S1_REPAIR_CONTROLS'
      and type(result['assertions']) is int and result['assertions']>50
      and len(result['checks'])==result['assertions']
      and all(z['passed'] is True for z in result['checks'])
      and result['actual_pid']==control['pid']
      and result['new_S1_boundary_rejection_before_mutation'] is True
      and result['no_whole_program_exclusion'] is True
      and result['unrelated_paths_preserved'] is True
      and result['owned_log_full_prefix_append_mode_verified'] is True
      and result['production_imported_compiled_executed'] is False
      and result['future_acceptance_approved'] is False
      and same(result['native13_before'],result['native13_after']),
      'Complete actual handwritten V2 source-only control evidence differs')
    need(dt.datetime.fromisoformat(control['started_utc'])<=
      dt.datetime.fromisoformat(result['utc'])<=dt.datetime.fromisoformat(control['finished_utc']),
      'Actual V2 control chronology differs')
    failure=result['private_V1_failure_reproduction']
    need(failure['actual_model_pid']==control['pid'] and failure['reproduced_S1'] is True
      and failure['production_executed'] is False
      and failure['logical_path']=='draft_pr_publication_program_20260930/RESEARCH_LOG.md',
      'Actual private V1 failure reproduction differs')
    ownership=parse(read(H/'OWNERSHIP_WRITE_INVENTORY.json'))
    need(ownership['additional_owned_tracked_body_paths']==['draft_pr_publication_program_20260930/RESEARCH_LOG.md']
      and ownership['complete_program_exclusion'] is False
      and ownership['canonical_overlay_payload_count']==955
      and ownership['accepted_payload_count']==957, 'Exact narrow S1 ownership scope differs')
    post=parse(read(H/'ROOT_POST_CONTRACT.json'))
    need(len(post['required_ROOT_complete_keyset'])==22
      and len(set(post['required_ROOT_complete_keyset']))==22
      and post['required_completed_values']['owned_operational_log_appends_exact'] is True,
      'Exact revised complete ROOT post contract differs')
    for name in PRODUCTION:
        path = str(H / name)
        rows = [z for z in result['complete_input_reads'] if z['path'] == path]
        need(rows and all(sha(read(H / name)) == z['sha256'] for z in rows),
          'Proposed source differs after actual source-only controls')
    files, dirs = tree(H)
    need(NAME not in files and not any(n.startswith('.PREPARATION_MANIFEST.') for n in files),
      'Existing closure or staging member')
    payload = []
    for name, path in sorted(files.items()):
        raw = read(path)
        if name.endswith('.json'): parse(raw)
        payload.append({'path':name, 'bytes':len(raw), 'sha256':sha(raw)})
    manifest = {'schema':'pr46-acceptance-source-closure/v1',
      'status':'CLOSED_SOURCE_ONLY', 'utc':now(), 'self_excluded':[NAME],
      'files_count':len(payload), 'files':payload, 'source_only':True,
      'proposed_helpers_imported_compiled_executed':False,
      'future_acceptance_or_ROOT_approval_claimed':False}
    body = (json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()
    # Recheck the exact own corpus before freezing; closure captures remain external.
    for row in payload: read(H / row['path'], row)
    again, again_dirs = tree(H)
    need(set(again) == set(files) and again_dirs == dirs, 'Own corpus changed during read')
    for path in files.values(): path.chmod(0o444)
    stage = H / '.PREPARATION_MANIFEST.staging'
    with stage.open('xb') as stream:
        stream.write(body); stream.flush(); os.fsync(stream.fileno())
    stage.chmod(0o444)
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renamex_np
    rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(os.fsencode(stage), os.fsencode(H / NAME), 4) != 0:
        error = ctypes.get_errno(); stage.unlink(); raise OSError(error, os.strerror(error))
    need(read(H / NAME, mode=0o444) == body, 'Actual closed manifest differs')
    final_files, final_dirs = tree(H)
    need(set(final_files) == set(files) | {NAME} and final_dirs == dirs,
      'Final self-only membership differs')
    for row in payload: read(H / row['path'], row, 0o444)
    print(json.dumps({'status':'CLOSED_SOURCE_ONLY', 'actual_closing_pid':os.getpid(),
      'manifest_sha256':sha(body), 'payload_files':len(payload), 'relative_directories':len(dirs),
      'source_report_sha256':args.expected_source_report_sha256,
      'actual_controls_sha256':args.expected_controls_sha256,
      'proposed_helpers_imported_compiled_executed':False,
      'future_acceptance_or_ROOT_approval_claimed':False}, sort_keys=True))

if __name__ == '__main__': main()
