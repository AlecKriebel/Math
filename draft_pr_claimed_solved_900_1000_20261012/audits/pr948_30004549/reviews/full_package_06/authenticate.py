from pathlib import Path
import json,hashlib,os,subprocess,sys,zipfile,io,datetime,traceback
P=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012'); A=P/'audits/pr948_30004549';D=A/'preprint';W=A/'publication/workflow';R=A/'reviews/full_package_06';ROOT=P.parent
IP='500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002'; FP='1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c'; MP='a25e28435f84374bf6e6705c9e5bc91952236d9f5fc5dc48e05ad29d62956b23'; WP='b77fac06fb3cbf3c04b0972d446828642a2b1caeefdaa2a33dc273b8f84cb7d2'; PP='dfb4a95b998f4b200ba8755fefe104126383667ee6ea927d338d144d396a2535';CP='0ccccc9cc49cadf489248f2a56d275625a033289ec5361212e35b6d9b9052827'
PRIOR=['348cf0e067b1a0532cb79172510c247ea3d079dcb315dab899143dc53dca0c66','98af806e47bdbe991ce01f710ea56f76d4c3081fcc2a2a3819362d55564229ea','24dec2ffbce33135e86fa7ef659374c594c54c6d1c2a7eb7f4e722cf21827465','5b91834665d27c0cb2ff7bbe9bd5296fcc133e825759c6e348d52d282fc62af2','4952eee8ff51c9d553121f66ccc907e4cc89eaa4b3bfbf36454e7a6e0ec9d15f']
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(path,z):
 b=(json.dumps(z,indent=2,sort_keys=True)+'\n').encode();f=open(path,'wb');f.write(b);f.flush();os.fsync(f.fileno());f.close();assert path.read_bytes()==b
 return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def h(path,pin=None):
 b=path.read_bytes();v={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};assert path.is_file() and not path.is_symlink();assert pin is None or v['sha256']==pin;return v
raw=(P/'accept_pr948.py').read_bytes();assert hashlib.sha256(raw).hexdigest()=='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823'
ns={'__name__':'_review_inert_','__file__':str(P/'accept_pr948.py')};exec(compile(raw,str(P/'accept_pr948.py'),'exec'),ns)
def map_check(base,records):
 out={}
 for name,pin in records.items():
  assert ns['safe'](name); b=ns['read_regular'](base/name,pin=pin);out[name]=ns['fingerprint'](b)
 return out
def authenticate(label):
 start=utc();out={'status':'INCOMPLETE','full_started_utc':start,'original_pr_head':ns['HEAD'],'freeze_sha256':FP,'package_manifest_sha256':MP}
 try:
  ctx=ns['capture_inventory'](IP);out['live_operations']={k:ns['fingerprint'](v) for k,v in ctx['captured'].items()};assert len(out['live_operations'])==7
  f=ns['freeze_check']((D/'FREEZE.json').read_bytes(),FP,ctx,base=D);out['candidate_files']=f['files'];out['evidence_files']=map_check(ROOT,f['evidence_files']);out['future_helpers']=f['future_helpers']
  out['workflow_manifest']=h(W/'MANIFEST.json',WP);out['workflow_files']=map_check(W,json.loads((W/'MANIFEST.json').read_bytes())['files']);assert len(out['workflow_files'])==357
  out['contract']=h(W/'CONTRACT.json',CP)
  B=D/'reviewed_candidates/candidate01';out['preservation_manifest']=h(B/'PRESERVATION.json',PP);out['preserved_candidate_files']=map_check(B,json.loads((B/'PRESERVATION.json').read_bytes())['files']);assert len(out['preserved_candidate_files'])==353
  old=json.loads((B/'FREEZE.json').read_bytes());ns['freeze_check']((B/'FREEZE.json').read_bytes(),h(B/'FREEZE.json')['sha256'],ctx,base=B,historical=True);out['historical_evidence_files']=map_check(B/'evidence',old['evidence_files']);out['historical_freeze_check']=True
  originals=ns['original_check']();out['originals']={}
  with zipfile.ZipFile(D/ns['ZIP']) as z:
   for name,pin in originals.items():
    info=z.getinfo('original/'+name);b=z.read(info);assert ns['fingerprint'](b)=={k:pin[k] for k in ('bytes','sha256')};assert info.external_attr>>16==0o100644;out['originals'][name]={**pin,'archive_mode':'100644','disk_and_archive_match':True}
  out['prior_review_seals']={}
  for i,pin in enumerate(PRIOR,1):
   B=A/f'reviews/full_package_{i:02d}';m=B/'MANIFEST.json';mh=h(m,pin);records=json.loads(m.read_bytes())['files'];out['prior_review_seals'][B.name]={'manifest':mh,'payloads':map_check(B,records)}
  q='query { repository(owner:"AlecKriebel",name:"Math") { pullRequest(number:948) { number state isDraft headRefOid baseRefName baseRefOid baseRef { target { oid } } } } }'
  p=subprocess.run(['gh','api','graphql','-f','query='+q],cwd=ROOT,capture_output=True,text=True,timeout=90)
  out['live_pr_read']={'utc':utc(),'command':['gh','api','graphql','-f','query='+q],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr};assert p.returncode==0
  pr=json.loads(p.stdout)['data']['repository']['pullRequest'];assert pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==ns['HEAD'] and pr['baseRefName']=='main' and len(pr['baseRef']['target']['oid'])==40
  out['status']='PASS';out['utc']=utc();out['full_completed_utc']=out['utc'];save(R/f'AUTHENTICATION_{label}.json',out);again=json.loads((R/f'AUTHENTICATION_{label}.json').read_bytes());assert again==out
  print(json.dumps({'label':label,'status':'PASS','utc':out['utc'],'live_operations':len(out['live_operations']),'files':len(f['files']),'evidence':len(out['evidence_files']),'workflow':len(out['workflow_files']),'preservation':len(out['preserved_candidate_files']),'originals':len(out['originals']),'priorseals':len(out['prior_review_seals']),'sha256':h(R/f'AUTHENTICATION_{label}.json')['sha256']}))
  return out
 except Exception as e:
  out.update(status='FAIL',utc=utc(),error=repr(e),traceback=traceback.format_exc());save(R/f'AUTHENTICATION_{label}_ATTEMPT_01_FAILURE.json',out);raise
if __name__=='__main__':authenticate(sys.argv[1])
