"""Independently bind and replay all closed actual post-merge evidence."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import gzip,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];F=A/'post_merge_review';V=A/'root_postmerge_replay_private_03';V.mkdir(exist_ok=True)
FRESH_MAIN='6c120b2c88436b2e3f23e63861ece85db8d95eef';ACTUAL='a7931795d85cd86c414200c5828d175046f707d5'
sha=lambda b:hashlib.sha256(b).hexdigest();checks=[];fresh=[]
def ck(v,n):
 checks.append({'name':n,'passed':bool(v)});assert v,n
def normalize_repos(old,new):
 changes=[]
 for side in ['head','base']:
  a,b=old[side]['repo'],new[side]['repo'];ck(a['full_name']==b['full_name']=='AlecKriebel/Math','repository identity')
  ck(a['open_issues']==a['open_issues_count'] and b['open_issues']==b['open_issues_count'],'coherent repository issue counts')
  for key in ['open_issues','open_issues_count','pushed_at','updated_at']:
   if a[key]==b[key]:continue
   if key in {'pushed_at','updated_at'}:
    ck(isinstance(a[key],str) and isinstance(b[key],str),'repository timestamp type');datetime.fromisoformat(a[key].replace('Z','+00:00'));datetime.fromisoformat(b[key].replace('Z','+00:00'))
   else:ck(type(a[key]) is int and type(b[key]) is int and a[key]>=0 and b[key]>=0,'repository count type')
   changes.append({'path':side+'.repo.'+key,'previous':a[key],'current':b[key]});b[key]=a[key]
 return changes
raw=(F/'PUBLIC_MANIFEST.json').read_bytes();mf=json.loads(raw);seal=json.loads((F/'FINAL_SEAL.json').read_bytes())
ck(seal['status']=='PASS' and seal['manifest_sha256']==sha(raw),'actual closed manifest seal')
ck(seal['verifier_code_sha256']==sha((F/'verify_post_merge.py').read_bytes()),'closed verifier code pin')
actual_names={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file() and not set(p.relative_to(F).parts)&{'private','__pycache__'} and p.relative_to(F).as_posix() not in {'PUBLIC_MANIFEST.json','FINAL_SEAL.json'}}
ck(len(mf['files'])==seal['public_files'] and actual_names=={e['path'] for e in mf['files']},'entire public inventory')
for e in mf['files']:
 q=PurePosixPath(e['path']);ck(not q.is_absolute() and '..' not in q.parts,'safe closed path')
 p=F/q;b=p.read_bytes();ck(not p.is_symlink() and len(b)==e['bytes'] and sha(b)==e['sha256'],'every whole closed file '+e['path'])
o=json.loads((F/'ACTUAL_POST_MERGE_RECEIPT.json').read_bytes())
ck(o['actual_merge']=='a7931795d85cd86c414200c5828d175046f707d5' and o['actual_parents']==['04c40062219cc9fa20834d98db2b270fdad1a848','7821af7ddd84a4b3bb3168a11246f4b49ab0c5e8'],'actual literal merge parents')
ck(o['actual_tree']=='194ef7dbd1f1a0d050400e68a61c6d166a54ef6e' and o['remote_state']=='CLOSED and merged','actual literal tree/state')
ck(len(o['commands'])==88 and len({e['label'] for e in o['commands']})==88,'all88 commands')
for i,c in enumerate(o['commands']):
 old={}
 for stream in ['stdout','stderr']:
  stored=(F/c[stream+'_path']).read_bytes();ck(sha(stored)==c[stream+'_stored_sha256'],'stored capture '+c['label']+'/'+stream)
  b=gzip.decompress(stored) if c['compressed'] else stored;ck(len(b)==c[stream+'_bytes'] and sha(b)==c[stream+'_sha256'],'whole logical capture '+c['label']+'/'+stream);old[stream]=b
 ck(c['exit']==0 and not old['stderr'],'original exit/stderr '+c['label']);start=datetime.now(timezone.utc).isoformat();z=subprocess.run(c['argv'],cwd=R,capture_output=True);end=datetime.now(timezone.utc).isoformat()
 streams={}
 for stream,b in [('stdout',z.stdout),('stderr',z.stderr)]:
  p=V/(str(i)+'_'+c['label']+'.'+stream+'.gz');p.write_bytes(gzip.compress(b,mtime=0));ck(gzip.decompress(p.read_bytes())==b,'fresh lossless whole stream '+c['label']+'/'+stream)
  streams[stream]={'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b),'stored_bytes':p.stat().st_size,'stored_sha256':sha(p.read_bytes())}
 entry={'label':c['label'],'argv':c['argv'],'start_utc':start,'end_utc':end,'exit':z.returncode,'only_repository_metadata_changes':[],**streams};fresh.append(entry)
 (A/'root_postmerge_replay_progress.json').write_text(json.dumps({'completed_executions':fresh,'checks':checks,'status':'IN_PROGRESS_NO_FINAL_PASS'},indent=2)+'\n')
 ck(z.returncode==0 and z.stderr==old['stderr'],'fresh complete exit/stderr '+c['label']);changes=[]
 if c['label'] in {'main_start','checkout_start','local_main_end'}:
  ck(old['stdout'].decode().strip()==ACTUAL and z.stdout.decode().strip()==FRESH_MAIN,'historical and refreshed literal local main '+c['label']);changes=[{'scope':'main ref after independently attributable descendant checkpoint','historical':ACTUAL,'current':FRESH_MAIN}]
 elif c['label'] in {'remote_main_start','remote_main_end'}:
  ck(old['stdout'].decode().split()==[ACTUAL,'refs/heads/main'] and z.stdout.decode().split()==[FRESH_MAIN,'refs/heads/main'],'historical and refreshed literal remote main '+c['label']);changes=[{'scope':'main ref after independently attributable descendant checkpoint','historical':ACTUAL,'current':FRESH_MAIN}]
 elif c['label'] in {'raw_api_main_start','raw_api_main_end'}:
  a=json.loads(old['stdout']);b=json.loads(z.stdout);ck(a['object']['sha']==ACTUAL and b['object']['sha']==FRESH_MAIN,'historical/fresh whole main API SHA')
  ck(a['object']['url']=='https://api.github.com/repos/AlecKriebel/Math/git/commits/'+ACTUAL and b['object']['url']=='https://api.github.com/repos/AlecKriebel/Math/git/commits/'+FRESH_MAIN,'historical/fresh whole main API commit URL')
  changes=[{'path':'object.sha','previous':a['object']['sha'],'current':b['object']['sha']},{'path':'object.url','previous':a['object']['url'],'current':b['object']['url']}];b['object']=a['object'];ck(a==b,'entire main API except two enumerated descendant SHA/URL leaves')
 elif z.stdout!=old['stdout'] and c['argv'][:2]==['gh','api'] and c['argv'][-1]=='repos/AlecKriebel/Math/pulls/366':
  a=json.loads(old['stdout']);b=json.loads(z.stdout);changes=normalize_repos(a,b);ck(a==b,'entire actual PR object except enumerated repository leaves')
 else:ck(z.stdout==old['stdout'],'every fresh stdout byte '+c['label'])
 entry['only_repository_metadata_changes']=changes
extra=[]
def current_run(label,argv):
 z=subprocess.run(argv,cwd=R,capture_output=True);streams={}
 for stream,b in [('stdout',z.stdout),('stderr',z.stderr)]:
  p=V/('current_'+label+'.'+stream+'.gz');p.write_bytes(gzip.compress(b,mtime=0));ck(gzip.decompress(p.read_bytes())==b,'full fresh current lossless '+label+'/'+stream);streams[stream]={'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b),'stored_sha256':sha(p.read_bytes())}
 extra.append({'label':label,'argv':argv,'exit':z.returncode,**streams});ck(z.returncode==0 and not z.stderr,'current exit/stderr '+label);return z.stdout
ck(current_run('current_main',['git','rev-parse','HEAD']).decode().strip()==FRESH_MAIN,'fresh end main stable')
current_run('actual_ancestor',['git','merge-base','--is-ancestor',ACTUAL,FRESH_MAIN])
ck(current_run('descendant_parents',['git','show','-s','--format=%P',FRESH_MAIN]).decode().split()==[ACTUAL],'attributable single-parent checkpoint')
expected={e['path'] for e in o['whole_file_receipts']}
changed=set(current_run('all_descendant_changed_paths',['git','diff','--name-only',ACTUAL,FRESH_MAIN]).decode().splitlines())
ck(not changed&expected and not any(p.startswith('unsolved_math_prioritization/attempts/2303016/') for p in changed),'every descendant changed path excludes target and QUEUE')
for e in o['whole_file_receipts']:
 b=current_run('blob_'+str(len(extra)),['git','show',FRESH_MAIN+':'+e['path']]);ck(len(b)==e['bytes'] and sha(b)==e['sha256'] and b==(R/e['path']).read_bytes(),'whole fresh current HEAD/worktree file '+e['path'])
ck(current_run('end_main',['git','rev-parse','HEAD']).decode().strip()==FRESH_MAIN,'current local main stable after every file')
ck(current_run('end_remote',['git','ls-remote','origin','refs/heads/main']).decode().split()==[FRESH_MAIN,'refs/heads/main'],'current remote main stable after every file')
z=subprocess.run(['python3',str(F/'verify_post_merge.py')],cwd=R,capture_output=True)
(A/'root_postmerge_closed_verifier.stdout').write_bytes(z.stdout);(A/'root_postmerge_closed_verifier.stderr').write_bytes(z.stderr)
ck(z.returncode==0 and z.stdout==(F/'closure.stdout').read_bytes() and z.stderr==(F/'closure.stderr').read_bytes()==b'','full readonly closed semantic verification')
ck(o['original_target_files_unchanged']==21 and o['nested_binding_count']==48 and o['remote_contents_fetched']==43,'all reviewed mathematics unchanged')
ck(o['queue']['lines']==1966 and o['queue']['line']==406 and o['queue']['changed_cells']==[8,9] and o['queue']['all_other_bytes_equal'],'whole queue contract')
clarification=json.loads((F/'QUEUE_NEGATIVE_CLARIFICATION.json').read_bytes())
ck(clarification['rejected_wrong_target_turn'] and clarification['changed_physical_line']==406 and clarification['changed_pipe_cell']==9,'literal target-row negative, original label honestly clarified')
ck(sha((F/'PUBLIC_MANIFEST.json').read_bytes())==sha(raw),'closed post evidence not mutated')
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ENTIRE_POSTMERGE_EVIDENCE_AND_REEXECUTION','manifest_sha256':sha(raw),'manifest_files':len(mf['files']),'seal_sha256':sha((F/'FINAL_SEAL.json').read_bytes()),'post_receipt_sha256':sha((F/'ACTUAL_POST_MERGE_RECEIPT.json').read_bytes()),'actual_merge':o['actual_merge'],'actual_parents':o['actual_parents'],'actual_tree':o['actual_tree'],'checks':checks,'check_count':len(checks),'all88_command_reexecutions':fresh,'refreshed_main':FRESH_MAIN,'extra_current_commands':extra,'normalization_policy':'Enumerated typed head/base repository count/timestamp leaves, plus explicit main SHA/URL/ref observations after independently verified single-parent checkpoint. Every other object field and non-ref stdout exact; every22 scoped current HEAD/worktree file and complete descendant changed-path set independently checked. Original failed stale comparison preserved.','closed_verifier_exit':z.returncode,'closed_verifier_stdout_sha256':sha(z.stdout),'closed_verifier_stderr_sha256':sha(z.stderr),'program_sha256':sha(Path(__file__).read_bytes()),'post_merge_review_percent':100,'credited_method_percent':100,'new_theorem_percent':0}
(A/'root_postmerge_verification_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','check_count','manifest_sha256','manifest_files','actual_merge']},indent=2))
