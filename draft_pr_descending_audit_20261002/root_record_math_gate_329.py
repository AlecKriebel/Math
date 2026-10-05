"""Record the root-adjudicated mathematical gate, leaving publication gates open."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
P=Path(__file__).resolve().parent; A=P/'audits/pr329_20000450'
utc=datetime.now(timezone.utc).isoformat(); sha=lambda b:hashlib.sha256(b).hexdigest()
assert not (A/'ROOT_MATHEMATICAL_GATE.json').exists()
pins={}
for name,st in [('GEOMETRY','PASS_ROOT_EXTERNALLY_CLOSED_GEOMETRY_FAMILY_ONLY'),
 ('DIVISION','PASS_ROOT_EXTERNALLY_CLOSED_DIVISION_FAMILY_ONLY'),
 ('ARITHMETIC','PASS_ROOT_EXTERNALLY_CLOSED_ARITHMETIC_FAMILY_ONLY')]:
    f=A/f'ROOT_{name}_CLOSURE.json'; b=f.read_bytes(); j=json.loads(b); assert j['status']==st
    pins[name]=dict(path=f.name,bytes=len(b),sha256=sha(b),utc=j['utc'])
b=(A/'ROOT_MATHEMATICAL_REVIEW.md').read_bytes()
j=dict(utc=utc,status='PASS_ROOT_FULL_MATHEMATICAL_GATE_PR329',original_head='96395a4f506af6a6045e3cd59afcba2db6b7e2e7',
    report=dict(path='ROOT_MATHEMATICAL_REVIEW.md',bytes=len(b),sha256=sha(b)),
    independent_family_closures=pins,mathematical_verification_percent=100,workflow_percent=40,
    exact_remaining_mathematical_gap='None identified within the explicitly normalized characteristic-zero regular-pentagon claim.',
    priority_complete=False,preprint_ready=False,merge_authorized_by_this_gate=False,publication_ready=False,
    original_author_turn_count='1/5',priority_stage_two_may_now_start=True,persistent_goal_complete=False)
(A/'ROOT_MATHEMATICAL_GATE.json').write_text(json.dumps(j,indent=2)+'\n')
s=json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_bytes())
s.update(utc=utc,descending_active_pr=329,descending_329_mathematical_verification_percent=100,
    descending_329_workflow_percent=40,descending_329_mathematical_verification_complete=True,
    descending_final_acceptance_preparing=False,descending_git_checkpoint_preparing=False)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_bytes())
item=next(x for x in inv['items'] if x['number']==329)
item.update(mathematical_verification_percent=100,audit_workflow_percent=40,
    mathematical_gate='PASS_ROOT_FULL_MATHEMATICAL_GATE_PR329',priority_complete=False,
    preprint_ready=False,original_author_turn_count='1/5')
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
entry=f'\n{utc} — PR329 full mathematical gate PASS:100% mathematics,40% workflow. Root externally closed all3 independent mechanism families and whole stable namespaces, fully read final proofs and scientific streams, and actually reproduced current computations, complete native evidence verifiers and meaningful mutants. Original22-file submission/21 attempt files and1/5 history unchanged. Fixed-generator Kummer inverse-class precision is required in the current paper. No mathematical gap identified in the explicitly normalized regular-pentagon family. Priority stage2 now released; preprint, fresh full-package review loops, merge, Zenodo and tracker remain pending. No first-priority/current-openness claim, publication clearance or persistent-goal completion.\n'
for p in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write(entry)
print(json.dumps(j,indent=2))
