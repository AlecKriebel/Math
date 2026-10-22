import sys, os, json, hashlib, subprocess, datetime, zipfile, io, tempfile, shutil, stat
from pathlib import Path
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parents[1]; F=A/'finalization/terminal_admin_after_whole05_20261016'; P=A/'NEWpreprint_v1_0'
O=A/'root_reproduction/terminal_after_whole05_20261016'; O.mkdir(exist_ok=False)
ZIP='PR1071_preprint_v1_0_support.zip'
def need(c,s):
 if not c:raise RuntimeError(s)
def load(p):return json.loads(p.read_text())
def ident(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def pinmatch(p,r,physical=False):
 need(ident(p)=={k:r[k] for k in ['bytes','sha256']},'Identity '+str(p))
 if physical:need(stat.S_IMODE(p.stat().st_mode)==r['mode'] and p.stat().st_nlink==r['nlink'],'Physical '+str(p))
seal=load(F/'SEAL.json')
for k in ['output_pins','current_audit_pins','current_candidate_pins','operative_diff','report']:pinmatch(F/seal[k]['path'],seal[k])
for name,root in [('OUTPUT_PINS.json',F),('CURRENT_AUDIT_PINS.json',A),('CURRENT_CANDIDATE_PINS.json',P)]:
 d=load(F/name)
 for r in d['records']:pinmatch(root/r['path'],r,True)
 for r in d['symlink_fixtures']:
  q=root/r['path'];need(q.is_symlink() and os.readlink(q)==r['target'],'Fixture link')
captured=A.parents[1]/'ROOT_PR1071_CAPTURED_TERMINAL_VALIDATION_20261016.stdout'
need(load(captured)['status']=='PASS' and load(captured)['current_audit_regular_files']==2004,'Actual captured validation receipt')
save(O/'CAPTURED_STAGE_VALIDATION_RECEIPT.json',{'argv':['python3','-B','finalization/terminal_admin_after_whole05_20261016/validate_terminal.py'],'cwd':str(A),'observed_exit_code':0,'stdout':str(captured),'stdout_identity':ident(captured),'stderr':str(captured.with_suffix('.stderr')),'scope':'ROOT actually executed the unmodified sealed checker before adding this helper or new ROOT audit files. Subsequent own records do not change that captured-stage result.'})
before=(F/'before/NEWpreprint_v1_0/scripts/verify_package.py').read_text();current=(P/'scripts/verify_package.py').read_text();anchor="    for r in json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']:"
need(current==before.replace(anchor,(F/'verifier_insertion.txt').read_text()+'\n'+anchor),'Complete current verifier diff is precisely reviewed insertion')
receipts=[]
def run(argv,expected=0):
 env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.run(list(map(str,argv)),cwd=O,env=env,capture_output=True,text=True)
 receipts.append({'utc':start,'argv':list(map(str,argv)),'cwd':str(O),'returncode':p.returncode,'expected_exit':expected,'stdout':p.stdout,'stderr':p.stderr});save(O/'ACTUAL_COMMANDS.json',receipts)
 need(p.returncode==expected,'Command failed '+str(argv));return p
# Execute the exact custody source with only its seven output writes redirected.
# Its source, __file__, input roots and every byte-reading/checking expression stay intact.
redirect=O/'custody';redirect.mkdir()
runner=O/'custody_read_only_replay.py'
runner.write_text('from pathlib import Path\nimport json\nF=Path('+repr(str(F))+')\nO=Path('+repr(str(redirect))+')\noriginal=Path.write_text\ndef redirected(self,*a,**kw):\n if self.is_relative_to(F):\n  target=O/self.relative_to(F);target.parent.mkdir(parents=True,exist_ok=True);return original(target,*a,**kw)\n raise RuntimeError("Unexpected custody output "+str(self))\nPath.write_text=redirected\np=F/"custody.py"\nexec(compile(p.read_text(),str(p),"exec"),{"__file__":str(p),"__name__":"__main__"})\n')
py='/opt/homebrew/bin/python3.14';run([py,'-B',runner])
actual=load(redirect/'CUSTODY_FULL_REPLAY.json');old=load(F/'CUSTODY_FULL_REPLAY.json')
need({k:v for k,v in actual.items() if k!='utc'}=={k:v for k,v in old.items() if k!='utc'},'Complete 29619 custody JSON differs')
for name in ['TERMINAL_BASELINE_RECONCILIATION.json','HISTORICAL_STAGE_RESOLUTION.json','PRIOR_LATER_PIN_RESOLUTION.json','LATEST_STAGE_PIN_RESOLUTION.json','NEW_STAGE_PIN_RESOLUTION.json','FULL_SOURCE_POINTER_RESOLUTION.json']:
 need(load(redirect/name)==load(F/name),'Full structured custody replay '+name)
raw=(P/ZIP).read_bytes();need(actual['closed_zip']['members']==225,'Closed225')
tmp=Path(tempfile.mkdtemp(prefix='ROOT1071final-',dir='/private/tmp'));C=tmp/'MixedPackage';C.mkdir()
try:
 with zipfile.ZipFile(io.BytesIO(raw)) as z:z.extractall(C)
 results={}
 for tag,python in [('311','/opt/homebrew/bin/python3.11'),('314',py)]:
  vals=[]
  for flags in [[],['-O']]:
   label=tag+('-O' if flags else '-normal')
   run([python,'-B',*flags,P/'scripts/verify_package.py','--require-bindings'])
   run([python,'-B',*flags,C/'scripts/verify_package.py'])
   out=tmp/(label+'-check');run([python,'-B',*flags,C/'scripts/check.py','--out',out])
   for inner in ['normal','optimized']:
    d=load(out/inner/'FINITE_CHECKS.json');vals.append({k:v for k,v in d.items() if k!='utc'})
   rebuilt=tmp/(label+'.zip');run([python,'-B',*flags,C/'scripts/build_archive.py','--out',rebuilt]);need(rebuilt.read_bytes()==raw,'Actual complete rebuild')
  need(all(v==vals[0] for v in vals),'Full same-runtime normal/O inner/outer JSON')
  results[tag]={'full_JSON_same_runtime_four_results_equal':True,'results':vals[0]}
 save(O/'FULL_MATH_RUNTIME_REPLAY.json',results)
 alias=C.with_name(C.name.swapcase());need(alias.samefile(C),'Physical case alias required')
 for script,output in [(C/'scripts/build_archive.py',alias/'never.zip'),(alias/'scripts/build_archive.py',C/'never.zip')]:
  r=run([py,'-B','-O',script,'--out',output],1);need('outside all frozen package descendants' in r.stderr,'Case guard diagnostic')
 status=C/'TERMINAL_AFTER_WHOLE05_STATUS.json';manifest=C/'PACKAGE_MANIFEST.json';sb=status.read_bytes();mb=manifest.read_bytes()
 d=load(status);d['fresh_whole_package_reviews_completed']=4;save(status,d)
 m=load(manifest)
 for r in m['members']:r.update(ident(C/r['path']))
 save(manifest,m)
 fault=tmp/'coherent-fault.zip'
 with zipfile.ZipFile(fault,'w',compression=0,allowZip64=False) as z:
  for n in sorted([r['path'] for r in m['members']]+['PACKAGE_MANIFEST.json']):
   i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,(C/n).read_bytes())
 b=load(P/'UPLOAD_BINDINGS.json');b['archive'].update(ident(fault));b['manifest_sha256']=ident(manifest)['sha256'];binding=tmp/'fault-binding.json';save(binding,b)
 for flags in [[],['-O']]:
  r=run([py,'-B',*flags,C/'scripts/verify_package.py','--require-bindings','--bindings',binding,'--archive',fault],1)
  need('Current terminal five-review/zero-finding accounting drift.' in r.stderr,'Semantic guard rather than stale hash')
 status.write_bytes(sb);manifest.write_bytes(mb);run([py,'-B',C/'scripts/verify_package.py'])
 run([py,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',A/'publication/zenodo-deposit.json'])
finally:
 save(O/'OWN_EXTERNAL_CLEANUP.json',{'scope':'Only new unsealed ROOT extraction/rebuild/fault derivatives. Every regular file identity captured before removal; original canonical, earlier stage outputs and source bodies untouched.','records':[{'path':str(q),**ident(q)} for q in sorted(tmp.rglob('*')) if q.is_file()]});shutil.rmtree(tmp)
for r in load(F/'OUTPUT_PINS.json')['records']:pinmatch(F/r['path'],r,True)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_TERMINAL_AFTER_WHOLE05_LOCALLY_READY_ORDERED_SERVICES_HELD','ROOT_full_current_prose_status_terminal_report_verifier_insertion_custody_and_controls_source_read':True,'entire_current_verifier_equals_reviewed_before_plus_exact_insertion':True,'actual_captured_stage_checker_passed_before_new_ROOT_audit_files':True,'captured_stage_receipt':str((O/'CAPTURED_STAGE_VALIDATION_RECEIPT.json').relative_to(A)),'terminal_outputs':994,'terminal_links':3,'captured_audit':2004,'candidate':381,'terminal_baseline':1978,'terminal_before':8,'terminal_protected':1970,'complete_custody':actual,'full_structured_custody_sources_and_each_identity_event_equal_to_sealed_agent_execution':True,'actual_ROOT_commands':receipts,'whole_reviews_completed':5,'minimum_whole_reviews':2,'latest_whole05_complete_zero_and_ROOT_adopted':True,'new_complete_whole_review_currently_required':False,'all_actionable_findings_resolved':True,'publication_ready':True,'issues_resolved':True,'published':False,'services_held_after_pr':1032,'scope':'Each fixed H in (1/4,1), T>0, integer n>=1, every L2 estimator from both uniform grids, independent standard equal-H components and canonical iterated integral. Brownian optimum/smooth rate prior. Full novelty/priority/worldwide current openness UNKNOWN; attributed note, extensive AI and unrefereed.','historical_preservation':'Earlier internal pending/readiness fields, false global-order raw claims, original failures and seals retain exact dated meanings. Current external ROOT seal supplies final adoption; unchanged qualification explicitly describes939 altered order positions and all4346 byte identities.','actual_prior_failure_scope':'Two bounded custody harness schema/locator errors corrected;323 recorded children=46successes+276intended rejections+1unexpected harness failure, plus separately disclosed direct-tool schema failure. Earlier whole05 ENOSPC child exit UNKNOWN remains UNKNOWN.','no_new_compile_render_claim':True,'paper':ident(P/'paper.pdf'),'tex':ident(P/'paper.tex'),'support_archive':ident(P/ZIP)}
save(A/'ROOT_TERMINAL_AFTER_WHOLE05_REVIEW_20261016.json',record)
files=[A/'ROOT_TERMINAL_AFTER_WHOLE05_REVIEW_20261016.json',F/'SEAL.json',F/'OUTPUT_PINS.json',F/'FINAL_VERIFICATION.json',F/'COMPLETE_OPERATIVE_CHANGES.patch',P/'paper.pdf',P/'paper.tex',P/ZIP,P/'UPLOAD_BINDINGS.json',A/'publication/zenodo-deposit.json']
integrity={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authority':'Current external ROOT final seal. All older internal pending/readiness fields and seals remain exact dated history.','entries':[{'path':str(p.relative_to(A)),**ident(p)} for p in files],'publication_ready':True,'issues_resolved':True,'published':False,'services_held_after_pr':1032};save(A/'CURRENT_FINAL_INTEGRITY_20261016.json',integrity)
save(A/'CURRENT_FINAL_SEAL_20261016.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_CURRENT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','integrity':ident(A/'CURRENT_FINAL_INTEGRITY_20261016.json'),'root_terminal_adoption':ident(A/'ROOT_TERMINAL_AFTER_WHOLE05_REVIEW_20261016.json'),'whole_reviews_completed':5,'minimum_whole_reviews':2,'actionable_issues':0,'publication_ready':True,'issues_resolved':True,'published':False,'services_held_after_pr':1032,'paper':ident(P/'paper.pdf'),'support_archive':ident(P/ZIP),'priority_novelty_worldwide_openness':'UNKNOWN'})
print(json.dumps({'status':'PASS_ROOT_CURRENT_FINAL_SEALED_READY_UNPUBLISHED_HOLD1032','commands':len(receipts),'archive':ident(P/ZIP)}))
