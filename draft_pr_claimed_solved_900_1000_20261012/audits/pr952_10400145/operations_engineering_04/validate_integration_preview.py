from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
OWN=Path(__file__).resolve().parent
PIN='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec'
sha=lambda b:hashlib.sha256(b).hexdigest()
if sha((OWN/'PROPOSED_accept_pr952.py').read_bytes())!=PIN:raise RuntimeError('external proposal pin')
source=OWN/'integration_inputs.py';events=[]
for mode,flags,opt in [('normal',[],0),('O',['-O'],1),('OO',['-OO'],2)]:
 for label,args,expected in [('preview',['--operations-only','--proposal-preview'],0),('bad_external_pin',['--operations-only','--proposal-preview'],1),('uninstalled_full',[],1),('forbidden_full_preview',['--proposal-preview'],1)]:
  command=[sys.executable,'-I','-S','-B',*flags,str(source),'--proposal-sha256',('0'*64 if label=='bad_external_pin' else PIN),*args];start=datetime.now(timezone.utc).isoformat();result=subprocess.run(command,cwd=OWN,capture_output=True);end=datetime.now(timezone.utc).isoformat();prefix=OWN/('GENERATOR_'+label+'_'+mode)
  for suffix,data in [('.stdout.json',result.stdout),('.stderr.txt',result.stderr)]:
   with Path(str(prefix)+suffix).open('xb') as stream:stream.write(data)
  launch={'started_utc':start,'completed_utc':end,'command':command,'returncode':result.returncode,'expected_returncode':expected,'outer_optimization':opt,'source_sha256':sha(source.read_bytes()),'proposal_sha256':PIN,'stdout_sha256':sha(result.stdout),'stderr_sha256':sha(result.stderr),'services_or_writes_by_generator':0}
  with Path(str(prefix)+'.launch.json').open('x') as stream:json.dump(launch,stream,indent=2);stream.write('\n')
  if result.returncode!=expected:raise RuntimeError('unexpected generator result '+label)
  if expected==0:
   doc=json.loads(result.stdout);inv=json.loads(doc['operations_inventory_json'])
   if not(doc['proposal_preview_only'] is True and doc['installed_actual_core'] is False and sha(doc['operations_inventory_json'].encode())==doc['operations_inventory_sha256'] and len(inv['files'])==7):raise RuntimeError('preview schema')
  events.append({'mode':mode,'test':label,'status':'PASS' if expected==0 else 'REJECTED_EXPECTED'})
(OWN/'GENERATOR_VALIDATION.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'events':events,'event_count':len(events),'status':'PASS_OPERATIONS_PREVIEW_AND_UNINSTALLED_GUARDS_ONLY','full_after_installation_path_executed':False,'acceptance_authority':False},indent=2)+'\n')
print(json.dumps({'status':'PASS','event_count':len(events)}))
