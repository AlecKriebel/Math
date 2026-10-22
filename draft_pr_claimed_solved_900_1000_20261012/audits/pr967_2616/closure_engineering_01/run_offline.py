#!/usr/bin/env python3
"""Launch real independent Python child processes; retain every attempt verbatim."""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,hashlib,json,subprocess
from pathlib import Path
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;P=OWN.parents[2]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def stamp():return datetime.now(timezone.utc).isoformat()
p=argparse.ArgumentParser();p.add_argument('--attempt',required=True);a=p.parse_args()
if not a.attempt.isalnum():raise SystemExit('alphanumeric unique attempt')
core=(P/'close_pr967.py').read_bytes();wrapper=(P/'finalize_pr967_and_gate_next.py').read_bytes();test=(OWN/'test_offline.py').read_bytes()
for name,raw in [('close_pr967.py',core),('finalize_pr967_and_gate_next.py',wrapper),('test_offline.py',test)]:
 path=OWN/(a.attempt+'_'+name)
 with path.open('xb') as stream:stream.write(raw)
summary=[]
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 cmd=[sys.executable,'-I','-S','-B',*flags,str(OWN/'test_offline.py'),'--core-sha256',sha(core),'--wrapper-sha256',sha(wrapper)]
 start=stamp();result=subprocess.run(cmd,cwd=P,capture_output=True,timeout=90)
 for suffix,raw in [('stdout.raw',result.stdout),('stderr.raw',result.stderr)]:
  with (OWN/(a.attempt+'_'+mode+'.'+suffix)).open('xb') as stream:stream.write(raw)
 launch={'argv':cmd,'started_utc':start,'completed_utc':stamp(),'returncode':result.returncode,'source_pins':{'core':sha(core),'wrapper':sha(wrapper),'suite':sha(test)},'stdout':{'bytes':len(result.stdout),'sha256':sha(result.stdout)},'stderr':{'bytes':len(result.stderr),'sha256':sha(result.stderr)},'fixture_only':True,'actual_service_mutations':0}
 with (OWN/(a.attempt+'_'+mode+'.launch.json')).open('x') as stream:json.dump(launch,stream,indent=2);stream.write('\n')
 summary.append({'mode':mode,'returncode':result.returncode,'stderr_tail':result.stderr.decode()[-2200:]})
print(json.dumps(summary,indent=2))
