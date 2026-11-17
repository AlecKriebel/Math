"""Distinct passive closure after the successful deployment's storage error."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
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
def save(name,d):
 with (R/name).open('x') as f:json.dump(d,f,indent=2);f.write('\n')
assert (R/'LOCAL_AFTER.json').read_bytes()==b''
assert not (R/'DEPLOYMENT_FINAL.json').exists()
failure={'UTC':datetime.now(timezone.utc).isoformat(),'original_script':'verification/deploy_three_pages_root_once_20261117.py',
 'original_script_exit':1,'failure_stage':'After successful Firebase DEPLOY0 and HOSTING_AFTER0, saving LOCAL_AFTER.json failed with OSError [Errno28] No space left on device at source line55/save line27.',
 'literal_failed_file_preserved':'LOCAL_AFTER.json, zero bytes','original_native_cli_deployment_attempts':1,
 'root_disposition':'Separate passive complete local guard comparison and metadata closure only; no import/rerun of deployment script, no Firebase/network/Git action or redeployment.',
 'source_and_all_paper_files_not_repaired':True}
save('ORIGINAL_POSTSAVE_STORAGE_FAILURE.json',failure)
before=json.loads((R/'LOCAL_BEFORE.json').read_bytes());after=guards()
save('LOCAL_AFTER_CONTINUATION.json',after)
assert before==after,'Actual local preservation mismatch; retain all observations and stop'
deploy=json.loads((R/'DEPLOY.execution.json').read_bytes());observed=json.loads((R/'HOSTING_AFTER.execution.json').read_bytes())
assert deploy['exit_code']==observed['exit_code']==0
response=json.loads((O/'HOSTING_AFTER.stdout.bin').read_bytes())
live=[x for x in response['result']['channels'] if x['name'].endswith('/channels/live')]
assert len(live)==1
version=live[0]['release']['version'];assert version['status']=='FINALIZED'
assert version['name']=='projects/aleckriebel-bd92e/sites/aleckriebel-bd92e/versions/245aaf213f501c8a'
assert (W/'.git/refs/heads/master').read_text().strip()=='4cc09d6bbbad61aa11077c5002cf84a1e93b1344'
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'HOSTING_DEPLOYED_LOCAL_GUARDS_EXACT',
 'commit':'4cc09d6bbbad61aa11077c5002cf84a1e93b1344','old_live_version':'projects/aleckriebel-bd92e/sites/aleckriebel-bd92e/versions/9d7f8c6526f4153b',
 'new_live_version':version['name'],'actual_hosting_fileCount_if_reported':version.get('fileCount'),
 'deployment_attempts':1,'deployment_exit':0,'original_postcondition_script_exit':1,
 'separate_passive_closure':'Complete native M/W controls, local heads, hosting config and whole803file387dir public tree equal the actual predeployment observation.',
 'all_native_M_W_controls_localheads_and_public_bytes_modes_exact':True,
 'original_failure_and_empty_partial_file_retained':True,'redeployment_or_network_Git_actions_in_closure':0,
 'completed_prior_HTTPS_checks':'verification/sheet-three-pages-deployed143-20261117/LIVE_HASH_READS.json',
 'actual_UI':False,'AA':None,'goal_active_incomplete':True}
save('DEPLOYMENT_FINAL.json',result);print(json.dumps(result))
