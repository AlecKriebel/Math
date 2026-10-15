"""Root completed source review and actual final plan; imports no candidate."""
import ast
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr40_2814'
S=A/'acceptance_execution_preparation_family/integration_source_revision_v2'
def H(b):return hashlib.sha256(b).hexdigest()
def J(p):return json.loads(p.read_bytes())
def row(p):
    b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=H(b))
def member(root,z):
    n=z['path'];assert not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts
    p=root/n;assert p.is_file() and not p.is_symlink()
    b=p.read_bytes();assert type(z.get('bytes',z.get('size'))) is int and len(b)==z.get('bytes',z.get('size')) and H(b)==z['sha256'];return b
def closure(p,pin):
    assert H(p.read_bytes())==pin;m=J(p);names={p.name}
    for z in m['files']:
        assert z['path'] not in names;names.add(z['path']);member(p.parent,z)
    actual={q.relative_to(p.parent).as_posix() for q in p.parent.rglob('*') if q.is_file()}
    assert actual==names
    dirs={q.relative_to(p.parent).as_posix() for q in p.parent.rglob('*') if q.is_dir()}
    expected=set(m.get('directories',[t.as_posix() for n in names for t in PurePosixPath(n).parents if t.as_posix()!='.']))
    assert dirs==expected
    return m
prep='e5f0ce1f9cbc890767ef8131ac760d39562c9fba0faf41df208c3d0ebb3832ba'
closure(S/'PREPARATION_MANIFEST.json',prep)
closure(A/'root_runner_preparation_family/MANIFEST.json','aa58d2e3a9f470c6ce8d2781e47c72605de8338ee6766bb390a7f57ab7f42d50')
F=A/'acceptance_v2_publication_adversary_family'
closure(F/'FIRST_PARTY_MANIFEST.json','0fe8459862fa6f651482ad967179ddd4c13b8801356c1123167ffa74c4718fa8')
assessment=J(F/'ASSESSMENT.json')
sources=[]
for n in ['pr40_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:
    b=(S/n).read_bytes();ast.parse(b);sources.append(dict(**row(S/n),lines=len(b.splitlines())))
assert sum(z['lines'] for z in sources)==696
w=A/'execute_root_acceptance_revised.py';assert H(w.read_bytes())=='f00d8be3926b02d10f46a351802688a87f107d406c842317f51a5674248d4215'
assert w.read_bytes()==(A/'root_runner_preparation_family/WRAPPER_SOURCE.py.txt').read_bytes();ast.parse(w.read_bytes())
draft=J(S/'DRAFT_FINAL_PLAN.json')
for z in draft['immutable_evidence_references']:member(R,z)
for filename,field in [('REVISION_BINDINGS.json','immutable_revision_inputs'),('PREDECESSOR_REVISION_BINDINGS.json','immutable_refs')]:
    for z in J(S/filename)[field]:member(R,z)
C=A/'reviewed_candidate';cm=J(C/'MANIFEST.json');assert len(cm['files'])==239
for z in cm['files']:member(C,z);assert stat.S_IMODE((C/z['path']).stat().st_mode)==0o444
for z in J(C/'CURRENT_PROOF_DEPENDENCIES.json')['files']:member(A,z)
whole=J(A/'ROOT_WHOLE_CURRENT_REVIEW.json')
record=dict(schema='pr40-root-complete-v2-wrapper-and-source-review/v1',status='PASS',utc=dt.datetime.now(dt.timezone.utc).isoformat(),root_full_current_read_completed=True,root_full_whole_read_completed=True,root_full_all_five_helper_sources_read=True,root_full_wrapper_source_read=True,source_lines=696,wrapper_lines=len(w.read_bytes().splitlines()),source_pins=sources,wrapper=row(w),full_contract_scope_draft_input_revision_predecessor_bindings_read=True,new_source_adversary_manifest=row(F/'FIRST_PARTY_MANIFEST.json'),entire_new_source_adversary_assessment=assessment,entire_prior_whole_root_review=whole,source_only_review_does_not_claim_future_execution=True,original0of5=True,new_substantive_attempts=0,audit_turns=0,full_problem_solved=False,partial_valid=True,mandatory_corrections=[],S7_qualification='Earlier qualified static PASS missed ignoredcache3 Git absence. Separate closed v2 checks exactly three absent Git cache entries with full live bytes, tracked10 at preflight and tracked9 at accepted tree with queue separately verified. Original science and closed prior reviews remain exact.')
with (A/'ROOT_REVISED_ACCEPTANCE_SOURCE_REVIEW.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
plan=dict(draft);plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',root_full_current_read_completed=True,root_full_whole_read_completed=True,independent_whole_current_pass=True,preparation_manifest_sha256=prep)
with (A/'ROOT_REVIEWED_FINAL_PLAN.json').open('x') as f:json.dump(plan,f,indent=2);f.write('\n')
print(json.dumps(dict(status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',plan_sha256=H((A/'ROOT_REVIEWED_FINAL_PLAN.json').read_bytes()),source_review_sha256=H((A/'ROOT_REVISED_ACCEPTANCE_SOURCE_REVIEW.json').read_bytes()))))
