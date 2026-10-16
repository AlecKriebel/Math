"""Authenticate the terminal independent04 findings, never promotion authority."""
from pathlib import Path
import datetime, hashlib, json, stat
A=Path(__file__).resolve().parent
D=A/'lifecycle_adversary_04'
def require(ok, message):
    if not ok: raise RuntimeError(message)
def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(p, expected):
    require(pin(p)=={k:expected[k] for k in ('bytes','sha256')},'Binding drift: '+str(p))
require(pin(D/'FINAL_SEAL.json')['sha256']=='4c51609ee21a2fe4264af87e9027083fe7c41bec79023bdd3e0b01f6f1a6a10d','Seal drift')
seal=json.loads((D/'FINAL_SEAL.json').read_text())
require(seal['verdict']=='REPAIR_REQUIRED' and seal['summary']['checks']==78 and seal['summary']['unexpected_acceptances']==12,'Wrong terminal findings')
for name, expected in seal['files'].items(): check(D/name,expected)
manifest=json.loads((D/'REVIEW_MANIFEST.json').read_text())
for name, expected in manifest['deliverables'].items(): check(D/name,expected)
for name, expected in manifest['frozen_inputs'].items(): check(D/name,expected)
allow=json.loads((D/'PUBLIC_SAFE_ALLOWLIST.json').read_text())['files']
require(set(allow)==set(seal['files'])|{'FINAL_SEAL.json'},'Allowlist mismatch')
for name in allow:
    p=D/name
    require(not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o444,'Unsafe owned mode/path: '+name)
stamp=datetime.datetime.now(datetime.UTC).isoformat()
out={'UTC':stamp,'PR':191,'status':'ROOT_AUTHENTICATED_NEW_OPERATIONAL_REVIEW04_REPAIR_REQUIRED',
     'report':{'path':'lifecycle_adversary_04/FINAL_REPORT.md',**pin(D/'FINAL_REPORT.md')},
     'seal':{'path':'lifecycle_adversary_04/FINAL_SEAL.json',**pin(D/'FINAL_SEAL.json')},
     'proposal_seal':{'path':'lifecycle_controls_preparation_04/FINAL_SEAL.json',**pin(A/'lifecycle_controls_preparation_04/FINAL_SEAL.json')},
     'public_safe_owned_files_authenticated':len(allow),'Root_read_full_report':True,
     'independent_probes':78,'behaved_as_required':66,'unsafe_acceptances':12,
     'required_repairs':seal['required_repairs'],'separate_repair_generation':'lifecycle_controls_preparation_05',
     'NEW_independent_review_plan_already_sealed':'lifecycle_adversary_05',
     'earlier_handoffs_frozen_unused_without_promotion_authority':True,
     'two_clean_NEW_science_reviews_unchanged':True,'canonical_runtime_installed':False,
     'actual_operational_clearance_or_publication_gate_created':False,
     'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,
     'case_percent':79,'fully_completed_count':39,'published_count':23,'goal_complete':False}
p=A/'ROOT_OPERATIONAL_REVIEW04_REPAIR_REQUIRED.json'
with p.open('x') as f: f.write(json.dumps(out,indent=2)+'\n')
p.chmod(0o444)
case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text())
case.update(UTC=stamp,status='SCIENTIFIC_PACKAGE_READY_REPAIRING_FOURTH_OPERATIONAL_REVIEW_FINDINGS',case_percent=79,
            publication_ready=False,operational_lifecycle_audit_active=True,operational_required_repairs=seal['required_repairs'],
            operational_review04_Root_authentication=p.name,operational_review04_report='lifecycle_adversary_04/FINAL_REPORT.md',
            remaining_required_steps='Independently validate exact QUEUE postimages and programme dates; new05 adversarial review, actual Zenodo DOI/tracker/original-head MAIN merge and full factual acceptance before192.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+stamp+' — PR191 workflow79%: Root read the full terminal NEW independent04 report and authenticated14 safe sealed files plus all frozen inputs.78 checks gave66 expected outcomes and12 unsafe acceptances in two families: QUEUE contents and programme JSON factual dates. Revision05 will repair these at consumption boundaries; a distinct reviewer05 sealed its plan before implementation. Scientific v4 proof, package v1 and both clean whole-science reviews remain unchanged. No canonical runtime, Root publication gate, actual publication/DOI/tracker/PR change/merge or192 intake.39 completed/23 published.\n')
print(json.dumps(out))
