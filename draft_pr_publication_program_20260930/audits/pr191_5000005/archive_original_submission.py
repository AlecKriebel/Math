"""Authenticate immutable PR191 native artifacts; no mathematical opinion or writes remotely."""
from pathlib import Path
import base64,datetime,hashlib,importlib.util,json,stat
A=Path(__file__).resolve().parent;P=A.parent.parent;HEAD='a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe';NATIVE='unsolved_math_prioritization/attempts/5000005'
s=importlib.util.spec_from_file_location('native190',P/'audits/pr190_5000007/prepare_final_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.m.TREE_CACHE_PATH=A/'ARCHIVE_IMMUTABLE_TREE_CACHE.json'
def require(x,msg):
 if not x:raise RuntimeError(msg)
t=datetime.datetime.now(datetime.UTC).isoformat();pr=m.api('pulls/191');require(pr['head']['sha']==HEAD and pr['state']=='open' and pr['draft'] and not pr['merged'],'Original191 head/state changed')
intake=json.loads((P/'status_intakes_after_pr190/PR191_ORIGINAL_STATUS_INTAKE.json').read_text());require(intake['original_head']==HEAD and intake['original_QUEUE_status']=='claimed_solved','Not eligible original head')
root=m.api('git/commits/'+HEAD)['tree']['sha'];node=m.lookup(root,NATIVE);require(node is not None and node[1]=='tree','Original attempt tree absent');files=[]
def walk(tree,relative=''):
 for name,item in sorted(m.lookup.__globals__['directory'](tree).items()):
  require('/' not in name and name not in ['.','..'],'Unsafe Git name');mode,kind,sha=item;n=relative+name
  if kind=='tree':walk(sha,n+'/');continue
  require(kind=='blob' and mode in ['100644','100755'],'Unsupported original type/mode '+n)
  b=m.api('git/blobs/'+sha);require(b['encoding']=='base64','Unexpected blob encoding');data=base64.b64decode(b['content']);require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==sha,'Original Gitblob mismatch')
  p=A/'original_submission/files'/NATIVE/n;require(not p.exists(),'Do not overwrite original');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(0o444);files.append({'path':NATIVE+'/'+n,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob':sha,'git_mode':mode,'actual_local_mode':'0444'})
walk(node[2]);require(files,'Empty original submission')
manifest={'UTC':t,'PR':191,'original_head':HEAD,'original_commit_tree':root,'original_native_tree':node[2],'original_QUEUE_status':'claimed_solved','original_effort':intake['original_effort'],'files':files,'all_blob_SHA1_and_SHA256_authenticated':True,'actual_all_local_files_0444':True,'mathematical_review_performed':False,'priority_review_performed':False};(A/'ORIGINAL_FILE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');(A/'ORIGINAL_FILE_MANIFEST.json').chmod(0o444)
status={'UTC':t,'PR':191,'problem_id':5000005,'original_head':HEAD,'original_QUEUE_status':'claimed_solved','original_effort':intake['original_effort'],'status':'IMMUTABLE_ELIGIBLE_ORIGINAL_ARCHIVED_SCIENCE_UNREVIEWED','case_percent':5,'mathematical_clearance':False,'priority_clearance':False,'publication_ready':False,'completed':39,'published':23,'goal_complete':False,'remaining_required_steps':'Exact original-source scope, independent mathematical falsification/reproduction/repair, deep priority if valid, complete publication/review loop, exact Zenodo/tracker/original-head merge and factual acceptance.'};(A/'CURRENT_CASE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
(A/'RESEARCH_LOG.md').write_text('# PR191 /5000005 research log\n\n'+t+' — Workflow5%: original claimed_solved head '+HEAD+' and effort2/5 preserved. All'+str(len(files))+' original native artifacts authenticated by Git blob SHA1/SHA256, protected0444. Status-only eligibility accepted; no mathematical/priority/publication clearance or prior-review opinion adopted. PR190 factual completion39completed/23published accepted; broadergoalactive.\n')
print(json.dumps({'status':status['status'],'original_files':len(files),'files':[x['path'].removeprefix(NATIVE+'/') for x in files],'remote_mutations':0}))
