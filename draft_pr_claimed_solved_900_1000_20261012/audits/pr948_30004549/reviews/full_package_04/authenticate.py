import pathlib,json,hashlib,subprocess,datetime,tarfile,io,os,sys
R=pathlib.Path('/Users/alec/Documents/Math'); P=R/'draft_pr_claimed_solved_900_1000_20261012'; A=P/'audits/pr948_30004549'; D=A/'preprint'; W=A/'publication/workflow'; O=A/'reviews/full_package_04'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def run(args): return subprocess.run(args,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def authenticate(phase):
 out={'schema':'round04-raw-authentication-v1','phase':phase,'started_utc':now(),'actual_review_started_utc':'2026-10-16T11:18:13+00:00','checks':{},'failures':[]}
 def checked(name,base,mapping,count):
  assert len(mapping)==count,(name,len(mapping))
  observations={}
  for rel,rec in mapping.items():
   p=base/rel; b=p.read_bytes(); obs={'bytes':len(b),'sha256':sha(b)}; assert obs=={'bytes':rec['bytes'],'sha256':rec['sha256']},(name,rel,obs,rec); observations[rel]=obs
  out['checks'][name]={'count':len(observations),'files':observations,'passed':True}
  return observations
 pins={W/'OPERATIONS_INVENTORY.json':'500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002',D/'FREEZE.json':'1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c',W/'MANIFEST.json':'b77fac06fb3cbf3c04b0972d446828642a2b1caeefdaa2a33dc273b8f84cb7d2'}
 for p,h in pins.items(): assert sha(p.read_bytes())==h; out['checks'][str(p.relative_to(R))]={'sha256':h,'passed':True}
 ops=json.loads((W/'OPERATIONS_INVENTORY.json').read_bytes())['files']; out['operations_files']=checked('all_seven_actual_live_operations',R,ops,7); out['all_seven_authenticated_utc']=now()
 f=json.loads((D/'FREEZE.json').read_bytes()); checked('preprint_files',D,f['files'],308); checked('workspace_evidence',R,f['evidence_files'],440); checked('future_helpers',P,f['future_helpers'],6)
 checked('workflow_explicit_payloads',W,json.loads((W/'MANIFEST.json').read_bytes())['files'],357)
 rec=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_bytes()); head=rec['head']; checked('original24_disk',A/'original',rec['files'],24)
 ar=run(['git','-c','tar.umask=0022','archive','--format=tar',head,*rec['files']]); assert ar.returncode==0,ar.stderr.decode(); tf=tarfile.open(fileobj=io.BytesIO(ar.stdout)); members={m.name:m for m in tf.getmembers() if m.isfile()}; assert set(members)==set(rec['files'])
 original={}
 for path,r in rec['files'].items():
  ls=run(['git','ls-tree',head,'--',path]); assert ls.returncode==0; mode,typ,blob_and_path=ls.stdout.decode().strip().split(' ',2); blob=blob_and_path.split('\t')[0]; assert (mode,typ,blob)==('100644','blob',r['git_blob']); b=run(['git','cat-file','blob',blob]); assert b.returncode==0 and sha(b.stdout)==r['sha256'] and len(b.stdout)==r['bytes']; disk=A/'original'/path; assert disk.stat().st_mode&0o777==0o644; m=members[path]; ab=tf.extractfile(m).read(); assert m.mode==0o644 and sha(ab)==r['sha256'] and ab==b.stdout; original[path]={'git_mode':mode,'git_blob':blob,'disk_mode':oct(disk.stat().st_mode&0o777),'archive_mode':oct(m.mode),'bytes':len(ab),'sha256':sha(ab)}
 out['original24']=original; out['archive']={'command':['git','-c','tar.umask=0022','archive','--format=tar',head,'<exact24paths>'],'bytes':len(ar.stdout),'sha256':sha(ar.stdout),'file_count':24}
 seals={'01':'348cf0e067b1a0532cb79172510c247ea3d079dcb315dab899143dc53dca0c66','02':'98af806e47bdbe991ce01f710ea56f76d4c3081fcc2a2a3819362d55564229ea','03':'24dec2ffbce33135e86fa7ef659374c594c54c6d1c2a7eb7f4e722cf21827465'}
 for no,h in seals.items():
  B=A/'reviews'/('full_package_'+no); mb=(B/'MANIFEST.json').read_bytes(); assert sha(mb)==h; mm=json.loads(mb); checked('prior_round_'+no,B,mm['files'],len(mm['files'])); out['checks']['prior_round_'+no]['seal_sha256']=h
 q='query { repository(owner:"AlecKriebel",name:"Math") { pullRequest(number:948) { number state isDraft headRefOid headRefName baseRefName baseRefOid baseRef { name target { oid } } updatedAt url body } } }'
 meta=run(['gh','api','graphql','-f','query='+q]); out['live_metadata_attempt']={'utc':now(),'returncode':meta.returncode,'stdout':meta.stdout.decode(),'stderr':meta.stderr.decode()}; assert meta.returncode==0,meta.stderr.decode(); pr=json.loads(meta.stdout)['data']['repository']['pullRequest']; assert pr['number']==948 and pr['state']=='OPEN' and pr['isDraft'] and pr['baseRefName']=='main' and pr['headRefOid']==head; out['live_metadata']=pr
 queue=run(['git','show',head+':unsolved_math_prioritization/QUEUE.md']); assert queue.returncode==0; rows=[s for s in queue.stdout.decode().splitlines() if '| 30004549 /' in s]; assert len(rows)==1,rows; cells=[s.strip() for s in rows[0].split('|')]; assert 'claimed_solved' in cells and 'claimed_solved'==cells[8],cells; out['literal_queue_row']=rows[0]; out['queue_sha256']=sha(queue.stdout)
 out['before_mathematical_intake']=phase=='START'; out['completed_utc']=now(); out['status']='PASS'; dest=O/('AUTHENTICATION_'+phase+'.json'); tmp=dest.with_suffix('.json.tmp'); tmp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); os.replace(tmp,dest); print(json.dumps({'phase':phase,'status':'PASS','completed_utc':out['completed_utc'],'operations_count':7,'queue':rows[0],'live_head':pr['headRefOid'],'stored_baseRefOid':pr['baseRefOid'],'live_baseRef_target_oid':pr['baseRef']['target']['oid']}))
if __name__=='__main__': authenticate(sys.argv[1])
