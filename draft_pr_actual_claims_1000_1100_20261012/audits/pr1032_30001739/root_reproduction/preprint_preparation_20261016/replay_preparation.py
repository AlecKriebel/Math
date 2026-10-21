from pathlib import Path
import sys,json,hashlib,subprocess,datetime,tempfile,zipfile,shutil
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'preprint_v1_0';F=A/'preparation/unknown_priority_20261016'
def need(c,s):
 if not c:raise RuntimeError(s)
def load(p):return json.loads(p.read_text())
def identity(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def match(p,r):need(identity(p)=={k:r[k]for k in ['bytes','sha256']},'Pin mismatch '+str(p))
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
original=load(F/'ORIGINAL_INPUT_PINS.json')['files']
for r in original:match(A/r['path'],r)
for parent in [P,F]:
 for r in load(parent/'PREPARATION_SEAL.json')['files']:match(parent/r['path'],r)
match(A/'publication/zenodo-deposit.json',load(P/'PREPARATION_SEAL.json')['native_manifest'])
copies=load(P/'kit/COPY_MAP.json')
for r in copies:
 match(A/r['original_relative_to_audit'],r);match(P/'kit'/r['copy_relative_to_kit'],r)
meta=load(P/'.zenodo.json');need(meta==load(P/'kit/.zenodo.json')==load(P/'zenodo-deposit.json')['metadata']==load(A/'publication/zenodo-deposit.json')['metadata'],'Bibliographic objects differ')
for n in ['paper.pdf','paper.tex']:need((P/n).read_bytes()==(P/'kit'/n).read_bytes(),'Kit paper copy')
cmds=[]
def run(argv):
 p=subprocess.run(list(map(str,argv)),cwd=R,capture_output=True,text=True);cmds.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':list(map(str,argv)),'cwd':str(R),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});save(R/'ROOT_ACTUAL_COMMANDS.json',cmds);need(p.returncode==0,'Command failed '+str(argv));return p
tmp=Path(tempfile.mkdtemp(prefix='ROOT1032-prep-',dir='/private/tmp'));C=tmp/'clean';C.mkdir();raw=P/'pr1032_supportkit_v1.0.zip'
try:
 with zipfile.ZipFile(raw)as z:z.extractall(C)
 results=[]
 for py in ['/opt/homebrew/bin/python3.11','/opt/homebrew/bin/python3.14']:
  for flags in [[],['-O']]:
   p=run([py,'-B',*flags,C/'scripts/verify_kit.py','--archive',raw]);results.append(json.loads(p.stdout))
 need(all(r==results[0]for r in results),'Complete cross-runtime/outer-mode JSON differs')
 rebuilt=tmp/'rebuilt.zip';run(['/opt/homebrew/bin/python3.14','-B',C/'scripts/build_archive.py',rebuilt]);need(rebuilt.read_bytes()==raw.read_bytes(),'Actual deterministic builder differs')
 run(['/opt/homebrew/bin/python3.14','-B',A.parents[2]/'zenodo_deposit_tool/zenodo.py','check',A/'publication/zenodo-deposit.json'])
finally:
 save(R/'OWN_PREP_REPLAY_CLEANUP.json',{'records':[{'path':str(p),**identity(p)}for p in sorted(tmp.rglob('*'))if p.is_file()],'scope':'Only newly owned unsealed ROOT clean extraction/rebuild; no earlier pinned or original byte retired.'});shutil.rmtree(tmp)
for r in original:match(A/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_PREPARATION_WITH_OPEN_SUPPORT_P3_PENDING_COMPLETE_REVIEW_REPAIR_LOOP','head':'810d52306312623ecfe01ecbc5f5f0dd360972c3','original_files_rehashed':len(original),'preprint_seal_files':len(load(P/'PREPARATION_SEAL.json')['files']),'preparation_evidence_seal_files':len(load(F/'PREPARATION_SEAL.json')['files']),'copy_pairs':len(copies),'ROOT_entire_paper_preparation_report_READMEs_verifier_builder_source_credit_ledger_metadata_and_citation_read':True,'ROOT_all9_rendered_pages_actually_viewed':True,'actual_ROOT_fresh_commands':cmds,'full_verifier_JSON_cross_installed311_314_normal_optimized_equal':True,'mathematical_acceptance':'Scoped accepted proof remains conditional on explicit published dependencies; no new primary whole-body read or priority certificate claimed in this preparation adoption.','known_actionable_support_finding':'ROOT1032-P3-BUILD-01: natural relative TARGET can write inside frozen exact-allowlist kit; independently reproduced in own disposable copy. Repair new revision then new complete reviews required.','additional_lifecycle_framing_assessment_pending':'Intended permanent metadata should not retain undated current preparation readiness/deposit assertions after publication; first complete reviewer assessing.','priority_Luo_Zha_overlap':'UNKNOWN; human expressly accepts nonblocking unknown, no further access request','publication_ready':False,'fresh_complete_whole_package_reviews':0,'minimum_fresh_complete_whole_package_reviews':2,'first_complete_review_active':True,'paper':identity(P/'paper.pdf'),'archive':identity(raw),'new_compile_claimed':False,'inspection_helper_failure_disclosed':'Initial schema inventory helper treated list COPY_MAP as dict and raised AttributeError before any reproduction; corrected list adapter, no candidate finding.'}
save(A/'ROOT_PREPRINT_PREPARATION_REVIEW_20261016.json',record);print(json.dumps({'status':record['status'],'actual_commands':len(cmds),'original_files':len(original),'copy_pairs':len(copies)}))
