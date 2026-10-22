"""Settle full diffs, inventories and a noncircular local repair seal."""
import difflib,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'NEWpreprint_v1_0';Z='PR1071_preprint_v1_0_support.zip'
def now():return datetime.now(timezone.utc).isoformat()
def read(p):return json.loads(p.read_text())
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(p,n):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return {'path':str(n),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
def write(n,o):(D/n).write_text(json.dumps(o,indent=2)+'\n')
need(not (D/'SEAL.json').exists(),'Already sealed')
custody=read(D/'CUSTODY_SUMMARY.json');controls=read(D/'CONTROL_SUMMARY.json');need(custody['status']==controls['status']=='PASS','Required validation missing')
need(custody['authorized_existing_changes']==8 and custody['protected_unchanged']==979 and controls['semantic_rejections']==124,'Unexpected validated counts')
inventory=read(D/'CHANGE_INVENTORY.json');need(len(inventory['all_new_paths_outside_effort'])==17,'New paths outside narrow scope')
patch=[]
for r in inventory['authorized_existing_changes']:
 if r['path'].endswith('.zip'):continue
 before=A/r['before_snapshot'];after=A/r['path']
 patch.extend(difflib.unified_diff(before.read_text().splitlines(keepends=True),after.read_text().splitlines(keepends=True),fromfile='before/'+r['path'],tofile='after/'+r['path']))
for r in inventory['all_new_paths_outside_effort']:
 path=A/r['path'];need(path.is_relative_to(P),'Unexpected new external path')
 patch.extend(difflib.unified_diff([],path.read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/'+r['path']))
(D/'COMPLETE_OPERATIVE_CHANGES.patch').write_text(''.join(patch))
tool=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
write('NATIVE_LOCAL_DISPATCH_RECHECK.json',{'utc':now(),'source':pin(tool,str(tool)),'read_scope':'run() lines402-426; check dispatch returns local manifest/hash summary before local_state, token, client and remote branches.','actual_native_LOCAL_commands':4,'native_manifest':pin(A/'publication/zenodo-deposit.json','publication/zenodo-deposit.json'),'no_service_action':True})
# Last actual canonical verifier execution; all candidate writes have already settled.
argv=['/opt/homebrew/bin/python3.14','-B','-O',str(P/'scripts/verify_package.py')]
r=subprocess.run(argv,cwd=D,capture_output=True,text=True);write('FINAL_CANONICAL_VERIFY.json',{'utc':now(),'argv':argv,'cwd':str(D),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});need(r.returncode==0 and r.stderr=='','Final canonical verifier failed')
candidate=[pin(p,p.relative_to(P)) for p in sorted(P.rglob('*')) if p.is_file() and not p.is_symlink()]
audit=[pin(p,p.relative_to(A)) for p in sorted(A.rglob('*')) if p.is_file() and not p.is_symlink() and D not in p.parents]
need(len(candidate)==355 and len(audit)==1004,'Final candidate/audit regular-file counts')
write('CURRENT_CANDIDATE_PINS.json',{'utc':now(),'records':candidate})
write('CURRENT_AUDIT_PINS.json',{'utc':now(),'records':audit})
archive=pin(P/Z,Z);old=pin(D/'before/NEWpreprint_v1_0'/Z,'before/NEWpreprint_v1_0/'+Z)
need(old['sha256']=='11a16cbe77cc084cf1ac50f4396159ad7ddd3b301a888adbf5b38613d771dbeb' and old['bytes']==1773348,'Original archive not retained')
summary={'utc':now(),'status':'PASS_BOUNDED_WHOLE04_P3_01_EXPLICIT_CURRENT_QUALIFICATION','finding':'WHOLE04-P3-01','archive':archive,'before_archive':old,'ZIP_members':199,'manifest_members':198,'candidate_regular_files':len(candidate),'audit_regular_files_outside_effort':len(audit),'custody':custody,'controls':controls,'actual_source_creation_failure_retained':True,'old_sealed_reports_raw_false_claims_and_statuses_unchanged':True,'mathematical_PDF_TeX_native_metadata_path_policy_and_runtime_sources_unchanged':True,'whole_reviews_completed':4,'minimum_whole_reviews_required':2,'latest_complete_review_findings':{'P0':0,'P1':0,'P2':0,'P3':1},'new_complete_whole05_required':True,'new_complete_whole05_completed':False,'root_repair_adoption_required':True,'root_terminal_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'bounded_repair_completion_percent':100,'no_Git_service_outreach_or_subagents':True}
write('FINAL_VERIFICATION.json',summary)
with (D/'RESEARCH_LOG.md').open('a') as f:
 f.write('\n'+now()+' — 100% of bounded WHOLE04-P3-01 repair: current explicit two-block/global-order correction is complete. All4346 historical rows/11480 locator fields,3158 prior later pins,3637 latest stage pins,153 exact copies and74 omissions pass;987 entry baseline files resolve to8 before/current changes and979 protected bytes.156 actual subprocesses match, including124 coherently rehashed semantic rejections, four unchanged checker wrappers, four native LOCAL checks and four byte-exact rebuilds on installed3.11/3.14 normal/-O. Final canonical -O verify passes. All writes now settle into per-file outputs/seal. Old claims/seals preserved, original ZIP durable, no deletions/Git/services/outreach/subagents. Root adoption then fresh whole05 and terminal adoption remain required; readiness/resolved/published=false, hold1032.\n')
outputs=[pin(p,p.relative_to(D)) for p in sorted(D.rglob('*')) if p.is_file() and not p.is_symlink() and p.name not in {'OUTPUT_PINS.json','SEAL.json'}]
write('OUTPUT_PINS.json',{'utc':now(),'scope':'Every settled regular effort file except this output-pin manifest and terminal noncircular seal. Includes all exact before bytes and every full code/prose/row-level receipt.','records':outputs})
seal={'utc':now(),'status':'SEALED_BOUNDED_LOCAL_HISTORY_ORDER_CORRECTION_PENDING_ROOT_AND_NEW_COMPLETE_WHOLE05','output_pins':pin(D/'OUTPUT_PINS.json','OUTPUT_PINS.json'),'settled_output_files':len(outputs),'candidate_pins':pin(D/'CURRENT_CANDIDATE_PINS.json','CURRENT_CANDIDATE_PINS.json'),'audit_pins':pin(D/'CURRENT_AUDIT_PINS.json','CURRENT_AUDIT_PINS.json'),'full_operative_diff':pin(D/'COMPLETE_OPERATIVE_CHANGES.patch','COMPLETE_OPERATIVE_CHANGES.patch'),'archive':archive,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'no_complete_review_self_claimed':True}
write('SEAL.json',seal)
print(json.dumps(seal,indent=2))
