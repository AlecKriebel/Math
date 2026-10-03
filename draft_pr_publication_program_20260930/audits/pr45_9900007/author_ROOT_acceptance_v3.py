"""ROOT's independent closed SOURCE inspection, followed by explicit reviewed fields.

Run only after personally reading the closed fresh adversary's report and controls.
No prepared production module is imported, compiled or executed here.
"""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, math, os, stat, subprocess, sys

A = Path(__file__).resolve().parent
R = A.parents[2]
S = A / 'acceptance_preparation_family'
F = A / 'acceptance_source_adversary_family'
PREP = '867faf71a96ada5acf2a92539bfdacd3b69bd3a1a1e0cb7e37ea6a106be1958e'

def sha(b): return hashlib.sha256(b).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def parse(b):
    def pairs(items):
        out = {}
        for k, v in items:
            assert k not in out
            out[k] = v
        return out
    out = json.loads(b, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    def finite(o):
        if type(o) is float: assert math.isfinite(o)
        elif type(o) is list:
            for v in o: finite(v)
        elif type(o) is dict:
            for v in o.values(): finite(v)
    finite(out)
    return out
def load(p): return parse(p.read_bytes())
def eq(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys() == b.keys() and all(eq(a[k], b[k]) for k in a)
    if type(a) is list: return len(a) == len(b) and all(eq(x, y) for x, y in zip(a, b))
    return a == b
def safe(base, n):
    assert type(n) is str and n and '\\' not in n and '\0' not in n
    q = PurePosixPath(n)
    assert not q.is_absolute() and q.as_posix() == n and not set(q.parts) & {'.', '..', '.git', '__pycache__'}
    p = base / n
    assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(base.resolve())
    assert all(not t.is_symlink() for t in p.parents)
    return p
def ref(p):
    b = p.read_bytes()
    return {'path': p.relative_to(R).as_posix(), 'bytes': len(b), 'sha256': sha(b)}
def check(base, z):
    assert type(z['bytes']) is int and z['bytes'] >= 0 and type(z['sha256']) is str and len(z['sha256']) == 64
    b = safe(base, z['path']).read_bytes()
    assert len(b) == z['bytes'] and sha(b) == z['sha256'], z['path']
    return b
def dump(n, o):
    with (A / n).open('x') as f:
        json.dump(o, f, indent=2, ensure_ascii=False)
        f.write('\n')
def closure(base, name, pin):
    assert sha(safe(base, name).read_bytes()) == pin
    o = load(base / name)
    assert o['self_excluded'] == [name] and type(o['files_count']) is int and o['files_count'] == len(o['files'])
    rows = o['files']; names = {z['path'] for z in rows}
    assert len(names) == len(rows) and name not in names
    files = set(); dirs = set()
    for p in base.rglob('*'):
        assert not p.is_symlink() and (p.is_file() or p.is_dir())
        n = p.relative_to(base).as_posix()
        if p.is_file():
            files.add(n); assert stat.S_IMODE(p.stat().st_mode) == 0o444, n
        else:
            dirs.add(n)
    assert files == names | {name}
    expected_dirs = {p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    assert dirs == expected_dirs
    for z in rows: check(base, z)
    return o
def clock(v):
    t = dt.datetime.fromisoformat(v)
    assert t.tzinfo is not None
    return t
def complete_capture(p):
    o = load(p); d = p.parent
    assert o['actual_execution'] is True and o['completed'] is True and type(o['exit_code']) is int
    pid = o.get('pid', o.get('child_pid'))
    assert type(pid) is int and pid > 0 and type(o['operator_pid']) is int and o['operator_pid'] > 0
    assert clock(o['started_utc']) <= clock(o['finished_utc']) <= clock(now())
    for k in ['stdout', 'stderr']:
        z = o[k]
        if z['path'].startswith(str(R) + '/'):
            z = dict(z, path=Path(z['path']).relative_to(R).as_posix()); base = R
        elif z['path'].startswith('draft_pr_publication_program_20260930/'): base = R
        elif z['path'].startswith('actual_'): base = F
        else: base = d
        check(base, z)
    pre = load(d / 'PRELAUNCH.json') if (d / 'PRELAUNCH.json').is_file() else o.get('prelaunch')
    if pre is None:
        assert o['argv'][0] == 'git' and o['stdin_supplied'] is False
        z = o['prelaunch_source']
        parents = [cp for cp in S.glob('*ACTUAL_CAPTURE/CAPTURE.json') if load(cp)['pid'] == o['operator_pid']]
        assert len(parents) == 1
        parent = load(parents[0]); captured_source = parents[0].parent / 'PRELAUNCH_SOURCE.py'
        b = captured_source.read_bytes()
        assert len(b) == z['bytes'] and sha(b) == z['sha256']
        assert parent['prelaunch']['argv'][2] == str(R / z['path'])
        assert clock(parent['started_utc']) <= clock(o['started_utc']) <= clock(o['finished_utc']) <= clock(parent['finished_utc'])
        assert o['exit_code'] == 0
        return {'reference': ref(p), 'complete_capture': o,
            'dated_prelaunch_source_reference_verified_against_exact_parent_prelaunch_copy':ref(captured_source),
            'dated_source_reference_not_rebound_to_revised_present_source':True}
    assert type(pre) is dict
    if 'prelaunch' in o: assert eq(pre, o['prelaunch'])
    for n, k in [('PRELAUNCH_SOURCE.py', 'source_sha256'), ('PRELAUNCH_OPERATOR.py', 'operator_sha256')]:
        assert sha(safe(d, n).read_bytes()) == pre[k]
        if k in o: assert o[k] == pre[k]
    assert o['source_unchanged'] is True and o['operator_unchanged'] is True
    return {'reference': ref(p), 'complete_capture': o}

def main():
    assert __debug__ and len(sys.argv) == 2
    prep = closure(S, 'PREPARATION_MANIFEST.json', PREP)
    assert len(prep['files']) == 204
    fm = closure(F, 'SELF_MANIFEST.json', sys.argv[1])
    verdict = load(F / 'VERDICT.json')
    for k, v in {'schema':'pr45-acceptance-source-adversary-verdict/v1', 'verdict':'PASS_SOURCE_ONLY_SCOPED',
                 'preparation_manifest_sha256':PREP, 'mandatory_corrections':[],
                 'production_imported_compiled_executed':False, 'future_acceptance_approved':False}.items():
        assert eq(verdict[k], v), k
    inputs = load(F / 'COMPLETE_READ_INVENTORY.json')
    assert inputs['schema'] == 'pr45-adversary-read-inventory/v1' and inputs['foreign_bodies_copied'] is False
    rows = inputs['files']; names = set(); input_bytes = 0
    for z in rows:
        literal = z['path']; assert type(literal) is str and literal.startswith(str(R) + '/')
        n = Path(literal).relative_to(R).as_posix(); assert n not in names; names.add(n)
        b = check(R, dict(z, path=n)); input_bytes += len(b)
        assert type(z['worktree_mode']) is int and stat.S_IMODE((R/n).stat().st_mode) == z['worktree_mode'], n
    prepared = load(S / 'INPUT_BINDINGS.json')
    for z in list(prepared['pins'].values()) + [prepared[n] for n in ['closed_whole_manifest', 'closed_whole_report',
            'closed_whole_result', 'closed_root_whole_inspection', 'previous_mirror', 'previous_post', 'previous_root_post']]:
        check(R, z)
    actual = [complete_capture(p) for base in [S, F] for p in sorted(base.rglob('CAPTURE.json'))]
    external_close = A / 'acceptance_source_adversary_outer_closure_capture' / 'CAPTURE.json'
    actual.append(complete_capture(external_close))
    own = load(S / 'OWN_CONTROL_RESULTS.json')
    assert own['status'] == 'PASS_PRIVATE_CONTROLS_ONLY' and own['production_imported_compiled_executed'] is False
    assert own['permission_modes_checked'] == 4096 and len(own['negative_controls_rejected']) == 18
    hostile = load(F / 'CONTROL_RESULTS.json')
    assert hostile['status'] == 'PASS_STATIC_OWN_CONTROLS_ONLY' and hostile['production_imported_compiled_executed'] is False
    assert hostile['preparation_manifest_sha256'] == PREP and hostile['preparation_members'] == 204
    assert hostile['candidate_members'] == 497 and hostile['dependencies'] == 416 and hostile['whole_members'] == 1068
    assert hostile['external_inputs'] == 1109 and hostile['all4096_full_modes_checked'] is True
    previous = load(R / prepared['previous_mirror']['path'])
    post = load(R / prepared['previous_post']['path']); rootpost = load(R / prepared['previous_root_post']['path'])
    assert eq(post, load(S/'EXPECTED_PREVIOUS_POST.json')) and eq(rootpost, load(S/'EXPECTED_PREVIOUS_ROOT_POST.json'))
    assert rootpost['schema'] == 'pr44-root-complete-actual-post-inspection/v1' and eq(rootpost['entire_post'], post)
    assert len(previous['entries']) == 34 and post['primary_acceptances'] == 34 and post['targets'] == 35 and post['consumed_substantive_turns'] == 43
    operator = A / 'capture_root_final_operation.py'
    if not operator.exists(): operator.write_bytes((S / operator.name).read_bytes())
    else:
        assert load(A/'root_complete_acceptance_source_inspection_v2_actual_capture/CAPTURE.json')['exit_code'] == 1
        assert safe(A, operator.name).read_bytes() == safe(S, operator.name).read_bytes()
    assert sha(operator.read_bytes()) == '541c4ecf92caf69036adeaf3dbfa2c3e964fd194222ec1bf8100b03394f50a7a'
    inspection = {'schema':'pr45-root-complete-acceptance-source-inspection/v1', 'status':'PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION',
        'utc':now(), 'all_prepared_source_and_controls_fully_read':True, 'exact_preparation_closure_and_full_modes_checked':True,
        'all_individual_source_adversary_inputs_checked':True, 'all_complete_actual_captures_checked':True,
        'complete_VERDICT_object':verdict, 'preparation_manifest_sha256':PREP, 'acceptance_source_manifest':ref(F/'SELF_MANIFEST.json'),
        'acceptance_source_verdict':ref(F/'VERDICT.json'), 'mandatory_corrections':[], 'future_execution_approved':False,
        'preparation_files':204, 'adversary_files':len(fm['files']), 'individual_inputs':len(rows), 'individual_input_bytes':input_bytes,
        'all_complete_source_captures':actual,
        'honest_prior_ROOT_failures_preserved':[ref(A/n/'CAPTURE.json') for n in ['root_complete_acceptance_source_inspection_actual_capture','root_complete_acceptance_source_inspection_v2_actual_capture']], 'original_substantive_attempts':1, 'new_substantive_attempts':0, 'audit_turns':0,
        'full_problem_solved':False, 'ROOT_personal_source_and_adversary_report_reading':'Complete operative sources, closure, source controls and closed adversary report read personally; dated complete observations retained, no administrative future success inferred.'}
    dump('ROOT_SOURCE_ACCEPTANCE_REVIEW.json', inspection)
    bindings = load(S/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
    bindings.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR44_EVIDENCE', created_utc=now(),
        root_full_current_read_completed=True, root_full_whole_read_completed=True, root_acceptance_source_review_completed=True,
        independent_whole_current_pass=True, root_actual_PR44_predecessor_read_completed=True)
    paths = {'whole_manifest':A/'whole_current_source_first_family/MANIFEST.json', 'root_whole_inspection':A/'ROOT_WHOLE_CURRENT_REVIEW.json',
        'root_capture_operator':operator, 'acceptance_source_manifest':F/'SELF_MANIFEST.json', 'acceptance_source_verdict':F/'VERDICT.json',
        'root_source_inspection':A/'ROOT_SOURCE_ACCEPTANCE_REVIEW.json'}
    for k in ['previous_mirror','previous_post','previous_root_post']: paths[k] = R / prepared[k]['path']
    for k, p in paths.items(): bindings[k] = ref(p)
    dump('ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json', bindings)
    refs = list(prepared['pins'].values()) + [ref(A/'reviewed_candidate/MANIFEST.json'), ref(A/'reviewed_candidate/CURRENT_DEPENDENCIES.json'),
        bindings['whole_manifest'], prepared['closed_whole_result'], prepared['closed_whole_report'], bindings['root_whole_inspection'],
        ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')] + [bindings[k] for k in ['previous_mirror','previous_post','previous_root_post',
        'acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']]
    dedup = {}
    for z in refs: assert z['path'] not in dedup or eq(z, dedup[z['path']]); dedup[z['path']] = z
    plan = load(S/'DRAFT_FINAL_PLAN.json')
    plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION', partial_valid=True, preparation_manifest_sha256=PREP,
        whole_manifest_sha256=bindings['whole_manifest']['sha256'], root_bindings=ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')['path'],
        root_bindings_sha256=sha((A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json').read_bytes()), root_full_current_read_completed=True,
        root_full_whole_read_completed=True, root_acceptance_source_review_completed=True, root_actual_PR44_predecessor_read_completed=True,
        independent_whole_current_pass=True, immutable_evidence_references=sorted(dedup.values(), key=lambda z:z['path']))
    dump('ROOT_FINAL_PLAN.json', plan)
    print(json.dumps({'status':'PASS_ROOT_COMPLETE_SOURCE_AND_ACTUAL_PR44_BINDINGS','pid':os.getpid(), 'preparation':204,
        'adversary':len(fm['files']), 'individual_inputs':len(rows), 'actual_captures':len(actual), 'reference_count':len(dedup),
        'future_execution_certified':False}))

if __name__ == '__main__': main()
