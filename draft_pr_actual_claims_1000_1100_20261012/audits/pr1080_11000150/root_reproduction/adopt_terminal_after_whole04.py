import sys,os,json,hashlib,subprocess,datetime,zipfile,io,tempfile,shutil
from pathlib import Path
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parents[1];R=A/'finalization/terminal_admin_after_whole04_20261016';D=A/'preprint_v1_0';K=D/'verification_kit';O=A/'root_reproduction/terminal_after_whole04_20261016';O.mkdir(exist_ok=True)
def need(c,s):
 if not c:raise RuntimeError(s)
def load(p):return json.loads(p.read_text())
def identity(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def match(p,r):return identity(p)=={k:r[k] for k in ['bytes','sha256']}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
seal=load(R/'SEAL.json');need(match(R/'OUTPUT_PINS.json',seal['output_inventory']),'terminal seal')
for r in load(R/'OUTPUT_PINS.json')['files']:need(match(R/r['path'],r),'terminal output')
for r in load(R/'CURRENT_INPUT_PINS.json')['files']:need(match(A/r['path'],r),'captured898 input')
summary=load(R/'FINAL_VERIFICATION.json');need(summary['current_canonical_files']==898 and summary['changed_files']==9 and summary['protected_files']==856,'current898 counts')
save(O/'CAPTURED898_ROOT_CHECK_RECEIPT.json',{'argv':['python3','-B','finalization/terminal_admin_after_whole04_20261016/verify_terminal.py','--check'],'cwd':str(A),'observed_exit_code':0,'observed_stdout_JSON_compared_to':str(R/'FINAL_VERIFICATION.json'),'result_identity':identity(R/'FINAL_VERIFICATION.json'),'scope':'ROOT read entire verifier source then actually ran the unmodified sealed --check successfully BEFORE adding this helper or other new ROOT records under A. Tool exec session83364 returned exit0 and full matching JSON. Raw process stdout was displayed by the tool, not separately captured into a local raw-stream file. Later root files do not alter its captured898-stage contract.'})
def closed(root):
 names=load(root/'ALLOWLIST.json')['members'];need(len(names)==299,'allowlist299');buf=io.BytesIO()
 with zipfile.ZipFile(buf,'w',compression=0) as z:
  for n in names:
   i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,(root/n).read_bytes())
 return buf.getvalue()
raw=(D/'verification_kit.zip').read_bytes();need(closed(K)==raw,'independent closed ZIP')
src=(A/'newreviews/package_04/fullmath.py').read_text().replace('HERE=Path(__file__).resolve().parent','HERE=Path('+repr(str(O))+')').replace("KIT=HERE.parents[1]/'preprint_v1_0/verification_kit'","KIT=Path("+repr(str(K))+")")
(O/'fullmath_replay.py').write_text(src)
receipts=[]
def run(argv,ok=True):
 e=os.environ.copy();e['PYTHONDONTWRITEBYTECODE']='1';p=subprocess.run(argv,cwd=O,env=e,capture_output=True,text=True);receipts.append({'argv':argv,'cwd':str(O),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expected_success':ok});save(O/'ACTUAL_COMMANDS.json',receipts);need((p.returncode==0)==ok,'actual command failed '+str(argv));return p
py='/opt/homebrew/bin/python3.14';tmp=Path(tempfile.mkdtemp(prefix='root1080-terminal-',dir='/private/tmp'));C=tmp/'verification_kit'
try:
 with zipfile.ZipFile(io.BytesIO(raw)) as z:z.extractall(tmp)
 for flags in [[],['-O']]:
  run([py,'-B',*flags,str(K/'verify.py'),'--require-binding'])
  run([py,'-B',*flags,str(C/'verify.py')])
  run([py,'-B',*flags,str(O/'fullmath_replay.py')]);name='FULL_MATHEMATICAL_OUTPUT_COMPARISON_O.json' if flags else 'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json';need(load(O/name)==load(R/name),'complete math JSON')
  rebuilt=tmp/('optimized.zip' if flags else 'normal.zip');run([py,'-B',*flags,str(C/'build_archive.py'),'--output',str(rebuilt)]);need(rebuilt.read_bytes()==raw,'actual rebuild')
  alias=C.with_name(C.name.swapcase());need(alias.samefile(C),'case alias available')
  run([py,'-B',*flags,str(C/'build_archive.py'),'--output',str(alias/'never-output.zip')],False)
  run([py,'-B',*flags,str(alias/'build_archive.py'),'--output',str(C/'never-output.zip')],False)
 # Semantic count corruption with fresh manifest hashes, using no outer binding.
 status=C/'CURRENT_TERMINAL_AFTER_WHOLE04.json';man=C/'MANIFEST.json';sb=status.read_bytes();mb=man.read_bytes();s=load(status);s['whole_reviews_completed']=3;status.write_text(json.dumps(s));m=load(man)
 for r in m['files']:
  if r['path']=='CURRENT_TERMINAL_AFTER_WHOLE04.json':r.update(identity(status))
 man.write_text(json.dumps(m))
 for flags in [[],['-O']]:
  p=run([py,'-B',*flags,str(C/'verify.py')],False);need('current terminal complete review count' in p.stderr,'semantic guard rather than stale hash')
 status.write_bytes(sb);man.write_bytes(mb)
 run([py,'-B',str(C/'verify.py')])
 run([py,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',str(D/'deposit_metadata.json')])
finally:
 save(O/'OWN_EXTERNAL_CLEANUP.json',{'entries':[{'path':str(p),**identity(p)} for p in sorted(tmp.rglob('*')) if p.is_file()],'scope':'Only newly created unsealed ROOT extraction/rebuild derivatives. Every file identity before removal; canonical and earlier artifacts untouched.'});shutil.rmtree(tmp)
for r in load(R/'OUTPUT_PINS.json')['files']:need(match(R/r['path'],r),'postrun terminal output')
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_TERMINAL_AFTER_WHOLE04_LOCALLY_READY_ORDERED_SERVICES_HELD','ROOT_full_REPORT_current_both_READMEs_current_verifier_new_current_status_and_entire_terminal_custody_verifier_source_read':True,'captured898_unmodified_sealed_checker_actually_passed_before_new_ROOT_files':True,'captured898_root_check_receipt':str((O/'CAPTURED898_ROOT_CHECK_RECEIPT.json').relative_to(A)),'counts':{'baseline':865,'changed':9,'protected':856,'new_canonical':33,'captured_canonical':898,'terminal_outputs':75,'copies':207,'prior_copy_prefix':181,'history':4731,'prior_history_prefix':4666,'exact_history':3257,'individual_history_omissions':1474,'old_relocations':9,'new_relocations':0,'old_structured_pointers':117,'new_before_pointer_resolutions':65,'selected_authored_evidence':18,'review04_decisions':52,'new_individual_source_body_omissions':8,'closed_zip_members':299},'actual_root_commands':receipts,'complete_mathematical_JSON_normal_optimized_equals_adopted_whole04':True,'paper':identity(D/'preprint.pdf'),'tex':identity(D/'preprint.tex'),'support_archive':identity(D/'verification_kit.zip'),'whole_reviews_completed':4,'minimum_whole_reviews':2,'latest_complete_whole04_zero_and_root_adopted':True,'new_complete_review_currently_required':False,'all_actionable_findings_resolved':True,'publication_ready':True,'issues_resolved':True,'published':False,'services_held_after_pr':1032,'scope':'Finite attained fixed-genus maximum and finite simultaneous-conjugacy classes under essential positive factors and geometric intersection<=1; separately printed restricted arbitrary-length clause negative; higher-genus exact maxima/classification bundle PARTIAL. Priority/novelty/worldwide openness UNKNOWN.','historical_preservation':'All old statuses/seals/archives/pins remain exact dated history. Current external final seal supplies ROOT final adoption without overwriting internal pending flags.','actual_interruptions':'Initial partial ZIP ENOSPC with exact own partial hash before removal; first own-copy compression receipt could not persist, disclosed; final31 commands contain26 completed before interruption +one failed explicit ENOSPC+four resumed completed. Local resume inventory-exclusion harness error before remaining commands retained/corrected. Older erasing-fault cause UNESTABLISHED; ROOT older attempt02 UNCONFIRMED.','storage_only':'Fifteen newly owned before/extraction copies transparently compressed with bytes/mode/mtime/nlink1/no canonical aliases exact, estimated24,260,608 physical bytes saved. Twenty-two own new full-math fixtures retired only after identity ledger. No deeper filesystem cause inferred.','no_new_math_PDF_TeX_pathguard_native_metadata_compile_render_or_service_change':True}
save(A/'ROOT_TERMINAL_AFTER_WHOLE04_REVIEW_20261016.json',record)
files=[A/'ROOT_TERMINAL_AFTER_WHOLE04_REVIEW_20261016.json',R/'SEAL.json',R/'OUTPUT_PINS.json',R/'FINAL_VERIFICATION.json',R/'COMPLETE_CODE_PROSE_DIFF.patch',D/'preprint.pdf',D/'preprint.tex',D/'verification_kit.zip',D/'EXTERNAL_BINDING.json',D/'deposit_metadata.json']
integrity={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current_authority':'External ROOT current final seal; earlier internal pending fields remain exact dated administrative history.','entries':[{'path':str(p.relative_to(A)),**identity(p)} for p in files],'all75_terminal_outputs_and898_current_and865_baseline_resolutions_checked':True,'publication_ready':True,'issues_resolved':True,'published':False,'services_held_after_pr':1032};save(A/'CURRENT_FINAL_INTEGRITY_20261016.json',integrity)
save(A/'CURRENT_FINAL_SEAL_20261016.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_CURRENT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR','integrity':identity(A/'CURRENT_FINAL_INTEGRITY_20261016.json'),'root_terminal_adoption':identity(A/'ROOT_TERMINAL_AFTER_WHOLE04_REVIEW_20261016.json'),'whole_reviews_completed':4,'minimum_whole_reviews':2,'actionable_issues':0,'publication_ready':True,'issues_resolved':True,'published':False,'services_held_after_pr':1032,'paper':identity(D/'preprint.pdf'),'support_archive':identity(D/'verification_kit.zip'),'higher_genus_exact_maximum_classification_bundle':'PARTIAL','priority_novelty_worldwide_openness':'UNKNOWN'})
print(json.dumps({'status':'PASS_ROOT_CURRENT_FINAL_SEALED_READY_UNPUBLISHED_HOLD1032','commands':len(receipts),'archive':identity(D/'verification_kit.zip')}))
