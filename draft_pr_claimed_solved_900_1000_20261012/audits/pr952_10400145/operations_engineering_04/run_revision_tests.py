#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,sys
OWN=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--stem',required=True);p.add_argument('--installed',action='store_true');p.add_argument('--proposal-sha256');p.add_argument('--suites',nargs='+',default=['finalization','operations','source_gate','native_recovery']);a=p.parse_args()
need=lambda ok,msg:None if ok else (_ for _ in ()).throw(RuntimeError(msg))
need(a.stem.replace('_','').isalnum(),'safe output stem')
sha=lambda b:hashlib.sha256(b).hexdigest()
proposal=(OWN/'PROPOSED_accept_pr952.py').read_bytes();pin=sha(proposal);need(a.proposal_sha256 is None or a.proposal_sha256==pin,'external requested proposal pin')
core=OWN.parents[2]/'accept_pr952.py';need(sha(core.read_bytes())==(pin if a.installed else '888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8'),'current core unchanged')
suites={'finalization':('test_finalization_logs_recovery.py','--proposal-sha256'),'operations':('test_operations_proposal.py','--core-sha256'),'source_gate':('test_source_gate_proposal.py','--core-sha256'),'native_recovery':('test_native_recovery_proposal.py','--proposal-sha256')}
for suite in a.suites:
 script,arg=suites[suite];source=(OWN/script).read_bytes()
 snapshot=OWN/(a.stem+'_'+suite+'.TEST_SOURCE.py');snapshot.write_bytes(source) if not snapshot.exists() else need(snapshot.read_bytes()==source,'test source immutable')
 for mode,flag,opt in [('normal',[],0),('O',['-O'],1),('OO',['-OO'],2)]:
  prefix=OWN/(a.stem+'_'+suite+'_'+mode);paths=[Path(str(prefix)+ext) for ext in ['.stdout.json','.stderr.txt','.launch.json']];need(not any(path.exists() for path in paths),'never overwrite actual test history')
  command=[sys.executable,'-I','-S','-B',*flag,str(OWN/script),arg,pin,*(['--installed'] if a.installed else [])]
  start=datetime.datetime.now(datetime.timezone.utc).isoformat();result=subprocess.run(command,cwd=OWN,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat()
  paths[0].write_bytes(result.stdout);paths[1].write_bytes(result.stderr)
  launch={'started_utc':start,'completed_utc':end,'command':command,'returncode':result.returncode,'proposal_sha256':pin,'test_source_sha256':sha(source),'test_source_snapshot':snapshot.name,'stdout_sha256':sha(result.stdout),'stderr_sha256':sha(result.stderr),'outer_mode':mode,'requested_compile_optimization':opt,'installed':a.installed,'real_service_or_Git_calls':0}
  paths[2].write_text(json.dumps(launch,indent=2)+'\n')
  parsed=json.loads(result.stdout) if result.returncode==0 else {}
  print(json.dumps({'suite':suite,'mode':mode,'returncode':result.returncode,'event_count':parsed.get('event_count'),'stderr':result.stderr.decode()[-1600:] if result.returncode else '', 'proposal_sha256':pin}),flush=True)
need(sha(core.read_bytes())==(pin if a.installed else '888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8'),'current core unchanged after tests')
