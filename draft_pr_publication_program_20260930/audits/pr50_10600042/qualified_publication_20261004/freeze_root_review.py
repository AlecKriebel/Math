"""Freeze ROOT's completed semantic adjudication of the authorized PR50 note."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os

Q=Path(__file__).resolve().parent
A=Q.parent
R=A.parents[2]
def binding(p):
    return {'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
pins=json.loads((Q/'QUALIFIED_INPUT_PINS.json').read_bytes())['pins']
for name,pin in pins.items():
    body=(A/'publication_package_v3'/name).read_bytes()
    assert len(body)==pin['bytes'] and hashlib.sha256(body).hexdigest()==pin['sha256']
families=[A/'qualified_round1_adversary_20261004',A/'qualified_round2_adversary_20261004']
v1,v2=[json.loads((p/'VERDICT.json').read_bytes()) for p in families]
assert v1['required_repairs']==[] and v1['status']=='PASS_QUALIFIED_RELEASE_NO_SUBSTANTIVE_ISSUES'
assert v2['required_repairs']==[] and v2['verdict']=='PASS_QUALIFIED_RESEARCH_NOTE_RELEASE'
assert v2['operative_payload_pins']==pins and v2['current_remote_head']=='7260315f8b8b193020c09d4ef6df9d943a3a13ff'
record={'schema':'pr50-qualified-note-root-review-adjudication/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
 'actual_pid':os.getpid(),'reviewed_head':'7260315f8b8b193020c09d4ef6df9d943a3a13ff',
 'ROOT_read_both_final_reports_in_full':True,'ROOT_reconstructed_proof_and_reviewed_sources_in_preceding_audit':True,
 'qualified_release_ready':True,'all_current_substantive_findings_resolved':True,'required_repairs':[],
 'proof_basis':'Universal edge-lifting soundness and completeness relative to explicitly credited established unrestricted Alexander/Markov theorems; finite diagnostics are supplementary.',
 'reviews':[{'report':binding(p/'REPORT.md'),'verdict':binding(p/'VERDICT.json')} for p in families],
 'final_artifacts':[binding(A/'publication_package_v3'/name) for name in pins],
 'authorization':binding(Q/'USER_AUTHORIZATION_AND_PREPARATION.json'),
 'user_exception_priority_unresolved':True,'publication_authorized':True,
 'priority_clearance':False,'historical_priority_certified':False,'present_openness_certified':False,
 'human_peer_review':False,'formal_proof_certification':False,'new_central_proof_attempts':0,
 'publication_performed':False,'tracker_written':False,'PR_merged':False,
 'estimates':{'qualified_review_percent':100,'PR50_workflow_percent':40,'dated_program_completion_percent':3.030303}}
with (Q/'ROOT_REVIEW_ADJUDICATION.json').open('x') as f: json.dump(record,f,indent=2); f.write('\n')
print(json.dumps(record,indent=2))
