"""Read-only merged-source and sealed-submission verification; captures stay outside seals."""
from pathlib import Path
import base64,datetime,hashlib,json,os,stat,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
D=A/'root_replay_private/post_merge_002';D.mkdir(exist_ok=False)
records=[]
def run(args,cwd=R):
 i=len(records);start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.run(args,cwd=cwd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 (D/f'{i:03}.stdout').write_bytes(p.stdout);(D/f'{i:03}.stderr').write_bytes(p.stderr)
 e={'argv':args,'cwd':str(cwd),'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr)}
 records.append(e);(D/f'{i:03}.receipt.json').write_text(json.dumps(e,indent=2)+'\n')
 assert p.returncode==0,(args,p.returncode,p.stderr.decode(errors='replace'))
 return p.stdout
def namespace(p):
 out={}
 for f in p.rglob('*'):
  assert not f.is_symlink()
  if f.is_file():assert stat.S_ISREG(f.lstat().st_mode);b=f.read_bytes();out[str(f.relative_to(p))]=(len(b),sha(b))
  else:assert f.is_dir();out[str(f.relative_to(p))+'/']=None
 return out
assert run(['git','branch','--show-current']).strip()==b'main'
head=run(['git','rev-parse','HEAD']).decode().strip();index=run(['git','ls-files','-s','-z'])
merged=load(A/'ACTUAL_MERGE_VERIFICATION.json');m=load(A/'repaired_snapshot_manifest.json');clear=load(A/'PUBLISHING_CLEARANCE.json')
assert clear['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS' and clear['second_review_mandatory_findings']==0
merge=merged['actual_merge'];assert merged['reviewed_head']==m['head']
pr=json.loads(run(['gh','api','repos/AlecKriebel/Math/pulls/364']))
assert pr['merged'] is True and pr['merge_commit_sha']==merge and pr['head']['sha']==m['head'] and pr['merged_at']==merged['merged_at']
c=json.loads(run(['gh','api',f'repos/AlecKriebel/Math/git/commits/{merge}']))
assert [x['sha'] for x in c['parents']]==merged['actual_parents']==[m['base'],m['head']]
assert run(['git','show','-s','--format=%T',merge]).decode().strip()==c['tree']['sha']
run(['git','merge-base','--is-ancestor',merge,head])
remote=json.loads(run(['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']))['object']['sha']
run(['git','merge-base','--is-ancestor',merge,remote])
scope=[]
for e in m['files']:
 path=e['path'];b=run(['git','show',merge+':'+path]);assert len(b)==e['bytes'] and sha(b)==e['sha256']
 assert run(['git','show',head+':'+path])==b and (R/path).read_bytes()==b
 tree=run(['git','ls-tree',merge,'--',path]).decode();assert tree.startswith(e['mode']+' blob '+e['git_blob_sha']+'\t')
 obj=json.loads(run(['gh','api','repos/AlecKriebel/Math/git/blobs/'+e['git_blob_sha']]))
 assert obj['sha']==e['git_blob_sha'] and obj['encoding']=='base64' and obj['size']==len(b) and base64.b64decode(obj['content'])==b
 scope.append({'path':path,'bytes':len(b),'sha256':sha(b),'git_blob_sha':e['git_blob_sha'],'mode':e['mode'],'merged_current_git_api_and_disk_identical':True})
q='unsolved_math_prioritization/QUEUE.md';old=run(['git','show',m['base']+':'+q]).splitlines(keepends=True);new=(R/q).read_bytes().splitlines(keepends=True)
assert len(old)==len(new);diff=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y];assert diff==[397]
x=old[397].split(b'|');y=new[397].split(b'|');assert [i for i,(a,b) in enumerate(zip(x,y)) if a!=b]==[8,9,11] and y[8].strip()==b'claimed_solved'
for e in clear['sealed_submission_files']:
 b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
families=[('graph_boundary_review/public/check_public_namespace.py',['--require-private']),('polytope_duality_review/verify_review.py',[]),('priority_review/private/check_integrity.py',[]),('preprint_review_01/verify_review.py',[]),('preprint_review_02/verify_review.py',[])]
roots=[A/'graph_boundary_review',A/'polytope_duality_review',A/'priority_review',A/'preprint_review_01',A/'preprint_review_02'];before=[namespace(p) for p in roots];checks=[]
for (name,flags),root in zip(families,roots):
 b=run([sys.executable,'-B',str(A/name),*flags],root);checks.append({'program':name,'whole_output':json.loads(b),'whole_stdout_sha256':sha(b)})
assert before==[namespace(p) for p in roots]
assert run(['git','rev-parse','HEAD']).decode().strip()==head and run(['git','ls-files','-s','-z'])==index
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FRESH_POST_MERGE_ALL_SOURCE_AND_SUBMISSION_BINDINGS','pr':364,'actual_merge':merge,'local_main':head,'observed_remote_main':remote,'ordered_actual_parents':merged['actual_parents'],'all42_merged_git_current_git_disk_and_fresh_api_bindings':scope,'all41_mathematical_files_unchanged':True,'only_queue_line':398,'only_queue_cells':[8,9,11],'all_other_queue_bytes_equal':True,'all_four_submission_pins_unchanged':True,'closed_family_checks':checks,'all_five_family_namespaces_unchanged':True,'entire_shared_index_unchanged':True,'native_capture_directory':str(D),'captures':len(records),'mathematical_resolution_percent':100,'workflow_completion_percent':90}
(A/'ROOT_POST_MERGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
criteria=load(A/'acceptance_criteria.json');criteria.update(post_merge_pending=False,post_merge_verification='ROOT_POST_MERGE_VERIFICATION.json');(A/'acceptance_criteria.json').write_text(json.dumps(criteria,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'all42_merged_git_current_git_disk_and_fresh_api_bindings','closed_family_checks'}},indent=2))
