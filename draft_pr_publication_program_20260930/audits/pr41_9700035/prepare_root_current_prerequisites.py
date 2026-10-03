"""ROOT-owned completed-read prerequisites, with genuine fresh native hashes."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
A=Path(__file__).resolve().parent;R=A.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def new(p,obj):
 with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
ledger=read(A/'ROOT_PRIMARY_READ_LEDGER.json')
assert ledger['reading_completed'] is True and all(v is True for v in ledger['root_flags'].values())
assert ledger['scope_certificate_sha256']==sha(A/'ROOT_PARTIAL_SCOPE_CERTIFICATE.md')
assert read(A/'ROOT_CLOSED_FAMILY_INSPECTION.json')['status']=='PASS'
root=read(A/'root_original_actual_reproduction/ROOT_REPRODUCTION.json')
assert root['status']=='PASS' and root['full_problem_solved'] is False
assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R).strip()
files=[]
for old in root['input_preimages']:
 p=R/old['path'];assert p.is_file() and not p.is_symlink()
 row=dict(path=old['path'],bytes=p.stat().st_size,sha256=sha(p));assert row==old
 files.append(row)
assert len(files)==13 and len({z['path'] for z in files})==13
assert '9700035' not in read(R/'unsolved_math_prioritization/state.json')
assert not any(str(json.loads(b)['id'])=='9700035' for b in (R/'unsolved_math_prioritization/history.jsonl').read_bytes().splitlines())
now=dt.datetime.now(dt.timezone.utc).isoformat()
pre=dict(schema='pr41-root-approved-fresh-current-inputs/v1',created_utc=now,
 approved_by_root=True,current_head=head,dated_actual_replay_head=root['head_before'],files=files,
 reason='Root reviewed all thirteen current native inputs after publishing the independent mathematical and closed-evidence checkpoint. Every complete file remains byte-identical to the dated genuine original replay; the separately approved current Git head includes only owned audit-publication progress. The selected target still has no native state or history event. Current freeze may now use these exact fresh preimages without transferring an old whole-packet verdict.')
new(A/'ROOT_CURRENT_INPUT_PREIMAGES.json',pre)
card=dict(schema='pr41-root-scientific-scope-before-new-current-freeze/v1',utc=now,
 status='UNSOLVED',partial_valid=True,full_problem_solved=False,novelty_claimed=False,
 original_substantive_attempts=2,turn_limit=5,new_substantive_attempts=0,audit_turns=0,
 current_model=None,current_reasoning_effort=None,current_deadline_utc=None,current_verdict=None,
 new_whole_current_gate='PENDING',root_flags=ledger['root_flags'],
 scope_certificate_sha256=sha(A/'ROOT_PARTIAL_SCOPE_CERTIFICATE.md'),
 read_ledger_sha256=sha(A/'ROOT_PRIMARY_READ_LEDGER.json'),
 proof_qualifications_sha256=sha(A/'primary_scope_family/SOURCE_PROOF_QUALIFICATIONS.md'),
 actual_replay_receipt_sha256=sha(A/'root_original_actual_reproduction/ROOT_REPRODUCTION.json'),
 actual_replay_manifest_sha256=sha(A/'root_original_actual_reproduction/MANIFEST.json'),
 actual_family_replay_manifest_sha256=sha(A/'root_family_controls_actual_reproduction/MANIFEST.json'),
 current_input_manifest_sha256=sha(A/'ROOT_CURRENT_INPUT_PREIMAGES.json'),
 paper_or_new_doi_or_tracker=False,human_peer_review_asserted=False,
 strongest_verified='Interior expected-length law/full lower bound unconditional; full law conditional on t^4 P(D>t)->0.',
 exact_remaining_gap='Expected full exterior route-union length o(k) under ordinary SIRSN axioms.',
 workflow_completion_estimate_percent=75,full_resolution_completion_estimate_percent=0,
 scope='Completed root mathematical/primary/retained-evidence reading. Current freeze, fresh whole verdict and actual integration are pending.')
new(A/'ROOT_SCIENCE_CARD.json',card)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==head
for z in files:assert (R/z['path']).stat().st_size==z['bytes'] and sha(R/z['path'])==z['sha256']
print(json.dumps(dict(status='GENUINE_ROOT_PREREQUISITES_RECORDED',head=head,
 current_manifest_sha256=sha(A/'ROOT_CURRENT_INPUT_PREIMAGES.json'),science_card_sha256=sha(A/'ROOT_SCIENCE_CARD.json'))))
