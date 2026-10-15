"""Authenticate the independent05 terminal counterexamples, not promotion."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent;D=A/'lifecycle_adversary_05'
def require(x,m):
 if not x:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(p,x):require(pin(p)=={k:x[k] for k in ['bytes','sha256']},'Binding drift '+str(p))
require(pin(D/'FINAL_SEAL.json')['sha256']=='5d126b1fea471c05fd53c76974331651be1b2b9300220440b2a0a79139be9d50','Seal drift')
seal=json.loads((D/'FINAL_SEAL.json').read_text());require(seal['verdict']=='REPAIR_REQUIRED' and seal['independent_expectations']==113 and seal['wrongly_accepted_negative_mutations']==10,'Terminal finding drift')
for k in ['report','bindings','manifest','results','safe_allowlist']:x=seal[k];check(D/x['path'],x)
manifest=json.loads((D/'MANIFEST.json').read_text())
for x in manifest['files']:check(D/x['path'],x)
allow=json.loads((D/'PUBLIC_SAFE_ALLOWLIST.json').read_text())['files'];require(set(allow)=={x['path'] for x in manifest['files']}|{'MANIFEST.json','FINAL_SEAL.json'},'Safe scope mismatch')
for n in allow:require(not (D/n).is_symlink() and stat.S_IMODE((D/n).stat().st_mode)==0o444,'Owned mode drift '+n)
inputs=json.loads((D/'INPUT_BINDINGS.json').read_text())
for n,x in inputs['source_files'].items():check(A/'lifecycle_controls_preparation_05'/n,x)
for k in ['paired_Root_handoff','dated_carry_forward_seed','preimplementation_plan']:x=inputs[k];check(D/x['path'],x)
stamp=datetime.datetime.now(datetime.UTC).isoformat()
out={'UTC':stamp,'PR':191,'status':'ROOT_AUTHENTICATED_NEW_OPERATIONAL_REVIEW05_REPAIR_REQUIRED','report':{'path':'lifecycle_adversary_05/FINAL_REPORT.md',**pin(D/'FINAL_REPORT.md')},'seal':{'path':'lifecycle_adversary_05/FINAL_SEAL.json',**pin(D/'FINAL_SEAL.json')},'proposal_seal':{'path':'lifecycle_controls_preparation_05/FINAL_SEAL.json',**pin(A/'lifecycle_controls_preparation_05/FINAL_SEAL.json')},'public_safe_owned_files_authenticated':len(allow),'Root_read_full_report':True,'independent_probes':113,'behaved_as_required':103,'unsafe_acceptances':10,'required_repairs':seal['required_issues'],'separate_repair_generation':'lifecycle_controls_preparation_06','NEW_independent_review_plan_already_sealed':'lifecycle_adversary_06','procedural_deviation_disclosed':seal['procedural_deviation'],'two_clean_NEW_science_reviews_unchanged':True,'canonical_runtime_installed':False,'actual_operational_clearance_or_publication_gate_created':False,'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'case_percent':79,'fully_completed_count':39,'published_count':23,'goal_complete':False}
p=A/'ROOT_OPERATIONAL_REVIEW05_REPAIR_REQUIRED.json'
with p.open('x') as f:f.write(json.dumps(out,indent=2)+'\n')
p.chmod(0o444)
case=json.loads((A/'CURRENT_CASE_STATUS.json').read_text());case.update(UTC=stamp,status='SCIENTIFIC_PACKAGE_READY_REPAIRING_FIFTH_OPERATIONAL_REVIEW_FINDINGS',case_percent=79,publication_ready=False,operational_lifecycle_audit_active=True,operational_required_repairs=seal['required_issues'],operational_review05_Root_authentication=p.name,operational_review05_report='lifecycle_adversary_05/FINAL_REPORT.md',remaining_required_steps='Exact complete case/programme/log derivations from approved baselines, NEW06 audit; actual Zenodo DOI/tracker/original-head MAIN merge and full factual acceptance before192.')
(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(case,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+' — PR191 workflow79%: Root read full terminal independent05 REPAIR_REQUIRED report and authenticated24 safe0444 artifacts plus all source/handoff inputs.113 expectations:103 matched,10 wrong acceptances in two families (current completion/intake aliases and newly generated Root case-log claims). Existing QUEUE/date repairs, full positive flow and immutable stale retry verified. Separate06 implements full pure programme/case/log postimages; distinct reviewer06 plan sealed before code. Prior historical Root prose stays trusted; arbitrary current factual claims do not. Empty-marker procedural deviation is explicitly disclosed in the review. Science proof/package/two clean reviews unchanged. No canonical runtime/gate/publication/DOI/tracker/PR mutation/merge/192 intake;39/23 unchanged.\n')
print(json.dumps(out))
