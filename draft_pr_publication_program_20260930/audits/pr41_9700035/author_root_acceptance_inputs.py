"""ROOT-only explicit approval inputs following completed personal reviews."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import math
import os
import stat
import subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
H = A / 'acceptance_preparation_family_v2'
PREP = '5f73ee3594751d176ed206ac521558045b0783cfa8b932af1bdde633deacd9aa'
VISITS = 0


def sha(raw): return hashlib.sha256(raw).hexdigest()


def load(p):
    def pairs(items):
        o = {}
        for k, v in items:
            assert k not in o
            o[k] = v
        return o
    o = json.loads(p.read_bytes(), object_pairs_hook=pairs,
                   parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
    def walk(v):
        global VISITS
        VISITS += 1
        if type(v) is dict:
            for x in v.values(): walk(x)
        elif type(v) is list:
            for x in v: walk(x)
        elif type(v) is float: assert math.isfinite(v)
        else: assert type(v) in (str, int, bool, type(None))
    walk(o)
    return o


def pin(p):
    raw = p.read_bytes()
    return {'path': p.relative_to(R).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}


def check(base, row, frozen=False):
    n = PurePosixPath(row['path'])
    assert not n.is_absolute() and n.as_posix() == row['path']
    assert not {'.', '..', '.git', '__pycache__'}.intersection(n.parts)
    p = base / row['path']
    assert p.is_file() and not p.is_symlink() and all(not d.is_symlink() for d in p.parents)
    raw = p.read_bytes(); size = row.get('bytes', row.get('size'))
    assert type(size) is int and size >= 0 and len(raw) == size and sha(raw) == row['sha256']
    if frozen: assert stat.S_IMODE(p.stat().st_mode) == 0o444
    if p.suffix == '.json': load(p)


def closure(base, name, rows, frozen=False, retained_empty=()):
    names = {z['path'] for z in rows}
    assert len(names) == len(rows) and name not in names
    files, dirs = set(), set()
    for p in base.rglob('*'):
        assert not p.is_symlink() and (p.is_file() or p.is_dir())
        (files if p.is_file() else dirs).add(p.relative_to(base).as_posix())
    expected = {p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    assert files == names | {name} and dirs == expected | set(retained_empty)
    for row in rows: check(base, row, frozen)
    if frozen: assert stat.S_IMODE((base / name).stat().st_mode) == 0o444


def dump(name, value):
    p = A / name
    with p.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True); f.write('\n'); f.flush(); os.fsync(f.fileno())
    return p


def main():
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=R).strip() == b'main'
    assert sha((H / 'PREPARATION_MANIFEST.json').read_bytes()) == PREP
    prepared = load(H / 'PREPARATION_MANIFEST.json')
    assert prepared['files_count'] == 32
    closure(H, 'PREPARATION_MANIFEST.json', prepared['files'], True)
    adversary = A / 'acceptance_v2_adversary_family'
    assert sha((adversary / 'FIRST_PARTY_MANIFEST.json').read_bytes()) == 'ebec51d9c41f63b8fadb159e93a85e51709b84dbbdbde4f2fb31b713e0018a32'
    am = load(adversary / 'FIRST_PARTY_MANIFEST.json')
    assert am['files_count'] == 41 and am['mandatory_corrections'] == []
    closure(adversary, 'FIRST_PARTY_MANIFEST.json', am['files'], True, am['intentional_empty_directories'])
    assert {p.relative_to(adversary).as_posix() for p in adversary.rglob('*') if p.is_dir()} == set(am['exact_directories'])
    external = am['individual_external_foreign_dependencies_excluded_from_authored_copy']
    assert len(external) == 1300
    for row in external: check(R, row)
    verdict = load(adversary / 'RESULT.json')
    assert verdict['verdict'] == 'PASS_SOURCE_ONLY_V2_MANDATORY_ADMIN_REPAIRS_ADDRESSED'
    assert verdict['mandatory_corrections'] == [] and verdict['candidate_helpers_imported_compiled_or_executed'] is False
    finite = load(adversary / 'FINITE_SPECIFICATION_RESULT.json')
    assert finite['checks_count'] == len(finite['checks']) == 93
    assert all(type(z['observed_admission']) is bool and z['observed_admission'] is z['expected_admission'] for z in finite['checks'])
    inputs = load(H / 'INPUT_BINDINGS.json')
    for row in inputs['pins'].values(): check(R, row)
    for c in inputs['closures']:
        base = A / c['directory']
        assert sha((base / c['manifest_name']).read_bytes()) == c['manifest_sha256']
        closure(base, c['manifest_name'], c['members'] + c['foreign_members'], c.get('requires_all_members_0444') is True)
    current = A / 'reviewed_candidate'; cm = load(current / 'MANIFEST.json')
    assert sha((current / 'MANIFEST.json').read_bytes()) == '3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'
    assert len(cm['files']) == 547
    closure(current, 'MANIFEST.json', cm['files'], True)
    dependencies = load(current / 'CURRENT_PROOF_DEPENDENCIES.json')
    assert len(dependencies['files']) == 469
    for row in dependencies['files']: check(A, row)
    whole = A / 'whole_current_source_first_family'
    wpin = {k: inputs['whole_observed_only'][k] for k in ['path', 'bytes', 'sha256']}
    check(R, wpin); check(R, inputs['root_whole_observed'])
    wm = load(whole / 'FIRST_PARTY_MANIFEST.json')
    assert len(wm['files']) == 143 and len(wm['foreign_files']) == 17
    closure(whole, 'FIRST_PARTY_MANIFEST.json', wm['files'] + wm['foreign_files'], True)
    # ROOT has personally completed the original/current/whole/source and
    # new independent source-adversary report reviews before this invocation.
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    root = load(H / 'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
    root.update(status='ROOT_APPROVED_CLOSED_WHOLE_EVIDENCE', created_utc=now,
                root_full_current_read_completed=True, root_full_whole_read_completed=True,
                independent_whole_current_pass=True, whole_manifest=wpin,
                root_whole_inspection=inputs['root_whole_observed'])
    root_path = dump('ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json', root)
    refs = [inputs['pins'][n] for n in sorted(inputs['pins'])]
    refs += [wpin, inputs['root_whole_observed'], pin(root_path),
             pin(whole / 'RESULT.json'), pin(whole / 'WHOLE_CURRENT_ADVERSARIAL_REVIEW.md')]
    assert len({row['path'] for row in refs}) == len(refs)
    plan = load(H / 'DRAFT_FINAL_PLAN.json')
    plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION', partial_valid=True,
                preparation_manifest_sha256=PREP, root_bindings=root_path.relative_to(R).as_posix(),
                root_bindings_sha256=sha(root_path.read_bytes()), whole_manifest_sha256=wpin['sha256'],
                root_full_current_read_completed=True, root_full_whole_read_completed=True,
                independent_whole_current_pass=True, immutable_evidence_references=sorted(refs, key=lambda z:z['path']))
    plan_path = dump('ROOT_REVIEWED_FINAL_PLAN.json', plan)
    native = sorted({'draft_pr_publication_program_20260930/inventory.json'} |
                    {'unsolved_math_prioritization/' + n for n in ['QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json', 'queue.py', 'policy.json', 'manifest.json', 'cache/problems.json', 'cache/research_results.json', 'cache/catalog.sqlite', 'review_v2/related_target_groups.json']})
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip()
    fresh = {'approved_by_root': True, 'created_utc': now, 'reason_date_utc': now[:10],
             'reason': 'ROOT inspected completed PR40 acceptance and its exact native mirror, post verification and checkpoint publication; fresh main and thirteen complete worktree files supersede dated preparation observations for PR41 integration.',
             'current_head': head,
             'files': [{**pin(R / n), 'worktree_mode': stat.S_IMODE((R / n).stat().st_mode)} for n in native]}
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip() == head
    fresh_path = dump('ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json', fresh)
    for row in fresh['files']: check(R, row)
    inspection = {'schema': 'pr41-root-reviewed-v2-approval-input-authoring/v1', 'utc': now,
                  'actual_pid': os.getpid(), 'status': 'PASS', 'prepared32': True,
                  'current547': True, 'dependencies469': True, 'whole143_and17': True,
                  'root_bindings': pin(root_path), 'final_plan': pin(plan_path),
                  'fresh_preimage': pin(fresh_path), 'typed_nodes_visited': VISITS,
                  'new_source_adversary_manifest_sha256': 'ebec51d9c41f63b8fadb159e93a85e51709b84dbbdbde4f2fb31b713e0018a32',
                  'entire_new_source_adversary_verdict': verdict,
                  'all93_independent_controls_checked': True,
                  'science_helpers_executed': False, 'native_or_Git_mutations': False}
    dump('ROOT_ACCEPTANCE_INPUT_AUTHORING.json', inspection)
    print(json.dumps(inspection, sort_keys=True))


if __name__ == '__main__': main()
