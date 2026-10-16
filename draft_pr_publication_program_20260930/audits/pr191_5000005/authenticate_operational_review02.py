"""Authenticate the independent terminal repair verdict; no operational promotion."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent;D=A/'lifecycle_adversary_02'
def require(x,m):
 if not x:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
pins={'FINAL_REPORT.md':'e9632a4ea12b2f372698932b1e23efa87b8bf43a53e07bcb472f7664afa2bf62','FINAL_SEAL.json':'f01338d0004fea82aff08cf93d73f480b4b98b7cbd81e5be43a7509c3cdee7b7','FINAL_MANIFEST.json':'275ea820a75df15bd58ad07cda781cb3189db966adc8975981532fcfac142e72','PUBLIC_SAFE_ALLOWLIST.json':'31cea801f35fff3d7ad5f902f98356055a92a0f6bb025786df669fdc17aa8eba'}
for n,h in pins.items():require(pin(D/n)['sha256']==h,'Terminal identity mismatch '+n)
seal=json.loads((D/'FINAL_SEAL.json').read_text());require(seal['verdict']=='REPAIR_REQUIRED','Unexpected verdict')
manifest=json.loads((D/'FINAL_MANIFEST.json').read_text())['files'];names={x['path'] for x in manifest}|{'FINAL_MANIFEST.json','FINAL_SEAL.json'}
require({p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}==names,'Owned inventory drift')
for x in manifest:require(pin(D/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Owned bytes drift '+x['path'])
for n in names:require(stat.S_IMODE((D/n).stat().st_mode)==0o444 and not (D/n).is_symlink(),'Owned mode/symlink drift '+n)
allow=json.loads((D/'PUBLIC_SAFE_ALLOWLIST.json').read_text())['files'];require(set(allow)<=names and len(set(allow))==len(allow),'Public subset mismatch')
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'PR':191,'status':'ROOT_AUTHENTICATED_NEW_OPERATIONAL_REVIEW02_REPAIR_REQUIRED','Root_read_complete_independent_report':True,'proposal_seal_sha256':'f9aee609fec7ee494dd7bf0dd65ff344ec45d27f1a91b3040179618e7f5bc03a','report':{'path':'lifecycle_adversary_02/FINAL_REPORT.md',**pin(D/'FINAL_REPORT.md')},'seal':{'path':'lifecycle_adversary_02/FINAL_SEAL.json',**pin(D/'FINAL_SEAL.json')},'owned_files_authenticated':len(names),'public_safe_files':len(allow),'all_owned_mode_0444':True,'independent_checks':44,'unsafe_acceptances':4,'required_repairs':['R1 derive and compare full native files; protect every scientific/priority field within factual paths','R2 no live cursor or advancement authority before actual factual acceptance','R3 fresh read-only actual publication/tracker observations plus exact local evidence/proposal bindings at consumption boundaries'],'historical_reviewer_fixture_error_is_not_runtime_finding':True,'repair_generation':'lifecycle_controls_preparation_03','NEW_independent_reviewer':'lifecycle_adversary_03','actual_publication_gate_created':False,'canonical_runtime_installed':False,'actual_published':False,'actual_tracker_updated':False,'actual_original_PR_merged':False,'two_NEW_clean_whole_science_reviews_unchanged':True,'case_percent':77,'fully_completed_count':39,'published_count':23,'goal_complete':False}
p=A/'ROOT_OPERATIONAL_REVIEW02_REPAIR_REQUIRED.json';require(not p.exists(),'Never overwrite authority');p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o444)
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+out['UTC']+' — PR191 workflow77%: Root read full independent02 terminal report and authenticated all'+str(len(names))+' owned files, only'+str(len(allow))+' public-safe. REPAIR_REQUIRED in three categories: scientific fields within factual files; live intake cursor before actual factual acceptance; actual service observations/evidence at downstream publication/tracker consumption. Separate03 repair and NEW03 independently preplanned reviewer; science and exact publication packet unchanged. No publication/tracker/PR/MAIN merge actions or192 intake;39/23 unchanged.\n')
print(json.dumps(out))
