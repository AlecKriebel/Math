"""One authorized hosting deployment, with exact local preservation checks."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat,subprocess,time
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O=P/'verification/mink-riesz-k3-root-execution-20261117'
R=P/'verification/mink-riesz-k3-live-root-20261117'
sha=lambda b:hashlib.sha256(b).hexdigest()
def file(f):
 return {'bytes':f.stat().st_size,'SHA256':sha(f.read_bytes()),'mode':f'{stat.S_IMODE(f.stat().st_mode):04o}'}
def tree(b):
 d={'root_mode':f'{stat.S_IMODE(b.stat().st_mode):04o}','files':{},'directories':{}}
 for f in sorted(b.rglob('*')):
  assert not f.is_symlink()
  if f.is_file():d['files'][f.relative_to(b).as_posix()]=file(f)
  elif f.is_dir():d['directories'][f.relative_to(b).as_posix()]=f'{stat.S_IMODE(f.stat().st_mode):04o}'
  else:raise AssertionError(f)
 return d
def guards():
 d={'public':tree(W/'public'),'native':{},'hosting':{n:file(W/n) for n in ['firebase.json','.firebaserc']}}
 for name,b in [('M',P.parent),('W',W)]:
  d['native'][name]={'files':{n:file(b/'.git'/n) for n in ['HEAD','index','config']},'loose':tree(b/'.git/refs/heads'),
   'packed_local_heads':[x for x in (b/'.git/packed-refs').read_text().splitlines() if ' refs/heads/' in x]}
 return d
def save(f,d):
 with f.open('x') as out:json.dump(d,out,indent=2);out.write('\n')
def run(label,args):
 cmd=['/opt/homebrew/bin/firebase',*args,'--project','aleckriebel-bd92e','--json','--non-interactive']
 start=datetime.now(timezone.utc);tick=time.monotonic();r=subprocess.run(cmd,cwd=W,capture_output=True)
 for suffix,raw in [('.stdout.bin',r.stdout),('.stderr.bin',r.stderr)]:
  with (O/(label+suffix)).open('xb') as f:f.write(raw)
 save(R/(label+'.execution.json'),{'argv':cmd,'cwd':str(W),'started_UTC':start.isoformat(),'finished_UTC':datetime.now(timezone.utc).isoformat(),'seconds':time.monotonic()-tick,'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'stdout_SHA256':sha(r.stdout),'stderr_SHA256':sha(r.stderr)})
 assert r.returncode==0,label
 d=json.loads(r.stdout);assert d['status']=='success',label
 return d
def live(d):
 cs=[x for x in d['result']['channels'] if x['name']=='projects/aleckriebel-bd92e/sites/aleckriebel-bd92e/channels/live']
 assert len(cs)==1
 v=cs[0]['release']['version'];assert v['status']=='FINALIZED'
 return v
assert not R.exists();R.mkdir()
pub=json.loads((O/'PUBLISH.stdout.bin').read_bytes())
assert pub['commit']=='4cc09d6bbbad61aa11077c5002cf84a1e93b1344'
assert (W/'.git/refs/heads/master').read_text().strip()==pub['commit']
before=guards();save(R/'LOCAL_BEFORE.json',before)
assert len(before['public']['files'])==803 and len(before['public']['directories'])==387 and before['public']['root_mode']=='0750'
assert before['native']['W']['files']['index']==pub['index']
old=live(run('HOSTING_BEFORE',['hosting:channel:list']))
assert old['name']=='projects/aleckriebel-bd92e/sites/aleckriebel-bd92e/versions/9d7f8c6526f4153b'
save(R/'ROOT_DEPLOYMENT_DECISION.json',{'UTC':datetime.now(timezone.utc).isoformat(),'authorization':'Persistent user goal authorizes routine hosting deployment; root adopts this exact scoped15 commit.','commit':pub['commit'],'project':'aleckriebel-bd92e','only_hosting':True,'one_attempt':True,'old_live_version':old['name'],'no_automatic_rollback_or_retry':True,'AA':None,'actual_UI':False})
deployed=run('DEPLOY',['deploy','--only','hosting'])
new=live(run('HOSTING_AFTER',['hosting:channel:list']))
assert new['name']!=old['name']
after=guards();save(R/'LOCAL_AFTER.json',after);assert before==after
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'HOSTING_DEPLOYED_LOCAL_GUARDS_EXACT','commit':pub['commit'],'old_live_version':old['name'],'new_live_version':new['name'],'actual_hosting_fileCount_if_reported':new.get('fileCount'),'optional_metric_not_used_as_certificate':True,'all_native_M_W_controls_localheads_and_public_bytes_modes_exact':True,'deployment_attempts':1,'deployment_exit':0,'HTTP_and_actual_UI_pending':True,'AA':None}
save(R/'DEPLOYMENT_FINAL.json',result);print(json.dumps(result))
