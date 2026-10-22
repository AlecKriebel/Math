#!/usr/bin/env python3
"""Exercise read-only full generator after authorized installation; outputs own only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent;A=P/'audits/pr952_10400145'
PIN='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec';READY='14bd1137e83f974e7dbf8153614533d72b5fe93d6382cea33e220580e396d603';AUTH='88c70b6d71f2674fa5593a70c2924a949408fadd6b36f731127db1aaef469063';PROTOCOL='20c8a041b9eb7e5d3b23c7c15ec603526c6bd9516c43ef890539e827ed515ad3'
def need(ok,m):
 if not ok:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(path):
 b=path.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def new(path,raw):
 with path.open('xb') as stream:stream.write(raw)
need(pin(P/'accept_pr952.py')['sha256']==PIN and pin(A/'ROOT_OPERATIONS04_INSTALLATION_AUTHORIZATION.json')['sha256']==AUTH and pin(A/'FULL_REVIEW_PROTOCOL.md')['sha256']==PROTOCOL,'external installed/auth/protocol pins')
extras=[A/'ROOT_OPERATIONS04_INSTALLATION_AUTHORIZATION.json',A/'ROOT_FULL02_PROCESS_UPDATE.json',OWN/'INSTALL_ACTION_RECEIPT.json']
extras+=sorted(path for path in (A/'root_operations04_revised_probe').iterdir() if path.is_file())
arguments=[]
for path in extras:arguments+=['--extra-evidence',path.relative_to(ROOT).as_posix(),pin(path)['sha256']]
source=OWN/'integration_inputs.py';results=[]
for mode,flag,opt in [('normal',[],0),('O',['-O'],1),('OO',['-OO'],2)]:
 command=[sys.executable,'-I','-S','-B',*flag,str(source),'--proposal-sha256',PIN,'--own-readiness-sha256',READY,*arguments]
 start=datetime.now(timezone.utc).isoformat();result=subprocess.run(command,cwd=OWN,capture_output=True);end=datetime.now(timezone.utc).isoformat();prefix=OWN/('GENERATOR_FULL_INSTALLED_'+mode)
 new(Path(str(prefix)+'.stdout.json'),result.stdout);new(Path(str(prefix)+'.stderr.txt'),result.stderr)
 receipt={'started_utc':start,'completed_utc':end,'command':command,'returncode':result.returncode,'outer_optimization':opt,'generator_sha256':pin(source)['sha256'],'installed_core_sha256':PIN,'proposal_readiness_sha256':READY,'root_authorization_sha256':AUTH,'stdout':{'bytes':len(result.stdout),'sha256':sha(result.stdout)},'stderr':{'bytes':len(result.stderr),'sha256':sha(result.stderr)},'output_only_own_engineering_folder':True,'adopted_into_W_or_D':False,'service_or_Git_calls':0}
 new(Path(str(prefix)+'.launch.json'),(json.dumps(receipt,indent=2)+'\n').encode())
 if result.returncode!=0:print(result.stderr.decode(),file=sys.stderr);raise RuntimeError('actual full generator failed; retained launch/raw failure')
 out=json.loads(result.stdout);freeze=json.loads(out['freeze_json']);inv=json.loads(out['operations_inventory_json']);settings=out['settings'];need(settings['candidate_revision']==4 and len(settings['review_manifest_specs'])==2 and settings['review_manifest_specs'][0].startswith('01:') and settings['review_manifest_specs'][1].startswith('02:'),'both adverse numbered reviews preserved')
 need(freeze['evidence_files'][(A/'FULL_REVIEW_PROTOCOL.md').relative_to(ROOT).as_posix()]['sha256']==PROTOCOL,'fresh protocol not pinned')
 need(inv['files'][(P/'accept_pr952.py').relative_to(ROOT).as_posix()]['sha256']==PIN and len(inv['files'])==7,'actual installed seven-file inventory')
 need(settings['freeze_sha256']==sha(out['freeze_json'].encode()) and settings['operations_inventory_sha256']==sha(out['operations_inventory_json'].encode()),'exact serialized generator pins')
 results.append({'mode':mode,'status':'PASS_READONLY_FULL_GENERATION_NOT_ADOPTED','candidate_payloads':len(freeze['files']),'frozen_evidence_files':len(freeze['evidence_files']),'prior_issue_ids':settings['prior_review_issue_ids'],'operations_inventory_sha256':settings['operations_inventory_sha256'],'generated_freeze_sha256':settings['freeze_sha256'],'stdout':receipt['stdout']})
 if mode=='normal':
  new(OWN/'GENERATED_OPERATIONS_INVENTORY.json',out['operations_inventory_json'].encode());new(OWN/'GENERATED_CANDIDATE04_FREEZE_NOT_ADOPTED.json',out['freeze_json'].encode());new(OWN/'GENERATED_CANDIDATE04_SETTINGS_NOT_ADOPTED.json',(json.dumps(settings,indent=2)+'\n').encode())
new(OWN/'FULL_GENERATOR_VALIDATION.json',(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_READONLY_FULL_PATH_AFTER_AUTHORIZED_INSTALLATION','results':results,'writes_only_new_own_engineering_files':True,'adoption_or_acceptance_authority':False},indent=2)+'\n').encode())
print(json.dumps({'status':'PASS','modes':len(results),'seven_file_operations_inventory_sha256':results[0]['operations_inventory_sha256'],'no_workflow_or_freeze_adoption':True}))
