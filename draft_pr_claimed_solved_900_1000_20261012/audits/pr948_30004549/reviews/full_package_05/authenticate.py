import datetime,hashlib,io,json,os,pathlib,stat,subprocess,sys,tarfile
R=pathlib.Path('/Users/alec/Documents/Math'); P=R/'draft_pr_claimed_solved_900_1000_20261012'; A=P/'audits/pr948_30004549'; D=A/'preprint'; W=A/'publication/workflow'; O=A/'reviews/full_package_05'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rec(p):
 b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def atomic(p,obj):
 q=p.with_name(p.name+'.new'); data=(json.dumps(obj,indent=2,sort_keys=True)+'\n').encode(); fd=os.open(q,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
 with os.fdopen(fd,'wb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
 os.replace(q,p)
def mapped(base,m):
 out={}
 for k,v in m.items():
  q=base/k; x=rec(q); assert x=={'bytes':v['bytes'],'sha256':v['sha256']},str(q); out[k]=x
 return out
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
def authenticate(phase):
 out={'schema':'pr948-independent-live-auth-v1','reviewer_agent_id':'/root/pr948_full_package_05','pr':948,'problem_id':'30004549','phase':phase,'actual_started_utc':now(),'failures':[]}
 try:
  pins={'FREEZE.json':(D/'FREEZE.json','1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c'),'OPERATIONS_INVENTORY.json':(W/'OPERATIONS_INVENTORY.json','500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002'),'workflow_MANIFEST.json':(W/'MANIFEST.json','b77fac06fb3cbf3c04b0972d446828642a2b1caeefdaa2a33dc273b8f84cb7d2'),'PRESERVATION.json':(D/'reviewed_candidates/candidate01/PRESERVATION.json','dfb4a95b998f4b200ba8755fefe104126383667ee6ea927d338d144d396a2535')}
  out['pins']={}
  for k,(p,h) in pins.items():
   v=rec(p); assert v['sha256']==h,k; out['pins'][k]=v
  f=json.loads((D/'FREEZE.json').read_bytes()); inv=json.loads((W/'OPERATIONS_INVENTORY.json').read_bytes())
  out['operations_files']=mapped(R,inv['files']); assert len(out['operations_files'])==7
  out['operations_checked_utc']=now()
  out['files']=mapped(D,f['files']); assert len(out['files'])==308
  out['evidence_files']=mapped(R,f['evidence_files']); assert len(out['evidence_files'])==440
  out['future_helpers']=mapped(P,f['future_helpers']); assert len(out['future_helpers'])==6
  wm=json.loads((W/'MANIFEST.json').read_bytes()); out['workflow_files']=mapped(W,wm['files']); assert len(out['workflow_files'])==357
  hist=D/'reviewed_candidates/candidate01'; out['historical_preservation_files']=mapped(hist,json.loads((hist/'PRESERVATION.json').read_bytes())['files']); assert len(out['historical_preservation_files'])==353
  out['previous_reviews']={}
  seals=['348cf0e067b1a0532cb79172510c247ea3d079dcb315dab899143dc53dca0c66','98af806e47bdbe991ce01f710ea56f76d4c3081fcc2a2a3819362d55564229ea','24dec2ffbce33135e86fa7ef659374c594c54c6d1c2a7eb7f4e722cf21827465','5b91834665d27c0cb2ff7bbe9bd5296fcc133e825759c6e348d52d282fc62af2']
  for i,h in enumerate(seals,1):
   q=A/'reviews'/('full_package_%02d'%i); v=rec(q/'MANIFEST.json'); assert v['sha256']==h; m=json.loads((q/'MANIFEST.json').read_bytes()); out['previous_reviews'][q.name]={'manifest':v,'files':mapped(q,m['files'])}
  originals=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_bytes()); head=originals['head']; out['original_files']={}
  archive=git('-c','tar.umask=0022','archive','--format=tar',head,*originals['files'])
  with tarfile.open(fileobj=io.BytesIO(archive)) as t:
   for k,v in originals['files'].items():
    tree=git('ls-tree',head,'--',k).decode().split(); assert tree[:3]==['100644','blob',v['git_blob']],k
    blob=git('cat-file','blob',v['git_blob']); br={'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest()}; assert br=={'bytes':v['bytes'],'sha256':v['sha256']}
    disk=A/'original'/k; assert rec(disk)==br and stat.S_IMODE(disk.stat().st_mode)==0o644
    member=t.getmember(k); tb=t.extractfile(member).read(); assert member.mode==0o644 and tb==blob and member.isfile()
    out['original_files'][k]={**br,'git_blob':v['git_blob'],'git_mode':'100644','disk_mode':'0644','archive_mode':'100644'}
  assert len(out['original_files'])==24
  out['branch']=git('branch','--show-current').decode().strip(); assert out['branch']=='main'
  out['immutable_local_head']=git('rev-parse','HEAD').decode().strip()
  queue=git('show',head+':unsolved_math_prioritization/QUEUE.md').decode(); rows=[s for s in queue.splitlines() if '30004549' in s]; assert len(rows)==1 and 'claimed_solved' in rows[0] and '4/5' in rows[0]; out['immutable_queue_row']=rows[0]
  query='query { repository(owner:"AlecKriebel",name:"Math") { pullRequest(number:948) { number state isDraft headRefOid headRefName baseRefName baseRefOid baseRef { name target { oid } } updatedAt url body } } }'
  cp=subprocess.run(['gh','api','graphql','-f','query='+query],cwd=R,capture_output=True,text=True)
  out['metadata_check_utc']=now(); out['graphql_exit']=cp.returncode; out['graphql_stderr']=cp.stderr; assert cp.returncode==0,cp.stderr
  raw=json.loads(cp.stdout); pr=raw['data']['repository']['pullRequest']; out['graphql_raw']=raw
  assert pr['number']==948 and pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==head and pr['baseRefName']=='main'; assert pr['baseRef']['name']=='main' and len(pr['baseRef']['target']['oid'])==40
  out['actual_pr_body_sha256']=hashlib.sha256(pr['body'].encode()).hexdigest(); out['associated_base_oid']=pr['baseRefOid']; out['live_base_target_oid']=pr['baseRef']['target']['oid']
  out['historical_native_count']='UNKNOWN'; out['historical_native_total']='UNKNOWN'; out['new_author_proof_responses']=0
  out['actual_completed_utc']=now(); out['status']='PASS'
 except BaseException as e:
  out['failures'].append({'utc':now(),'type':type(e).__name__,'message':str(e)}); out['actual_completed_utc']=now(); out['status']='FAIL'
 atomic(O/('AUTHENTICATION_'+phase+'.json'),out)
 print(json.dumps({'phase':phase,'status':out['status'],'actual_started_utc':out['actual_started_utc'],'actual_completed_utc':out['actual_completed_utc'],'failures':out['failures'],'operations_count':len(out.get('operations_files',{}))}))
 if out['status']!='PASS': sys.exit(1)
 return out
if __name__=='__main__': authenticate(sys.argv[1])
