"""Replay unchanged finite controls; these do not prove the PDE theorem."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, sys
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_descending_audit_20261002/audits/pr302_30003508'
P=A/'root_priority_controls_replay_private'
assert sys.flags.optimize==0
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(path):
 p=Path(path);b=p.read_bytes()
 return dict(path=str(p),resolved_path=str(p.resolve()),bytes=len(b),sha256=sha(b),mode=oct(stat.S_IMODE(p.stat().st_mode)))
def main():
 P.mkdir(exist_ok=False);captures=[];source=pin(__file__)
 cases=[('mechanism',A/'priority_mechanism_adversary_01/priority_controls.py',A/'priority_mechanism_adversary_01/CONTROL_RESULTS.json'),
        ('auxiliary',A/'classical_reduction_adversary_01/controls.py',A/'classical_reduction_adversary_01/CONTROL_RESULTS.json')]
 for label,original,baseline in cases:
  folder=P/label;folder.mkdir();copy=folder/original.name;copy.write_bytes(original.read_bytes())
  assert copy.read_bytes()==original.read_bytes()
  argv=[str(R/'.venv/bin/python'),'-E','-B',str(copy)]
  capture=dict(label=label,launcher_actual_pid=os.getpid(),launcher_argv=sys.argv,actual_argv=argv,cwd=str(folder),
   started_utc=utc(),original_source=pin(original),executed_source=pin(copy),reference_output=pin(baseline),
   child_executable=pin((R/'.venv/bin/python').resolve()),driver_source=source)
  (folder/'request.json').write_text(json.dumps(capture,indent=2)+'\n')
  with (folder/'stdout.bin').open('wb') as out,(folder/'stderr.bin').open('wb') as err:
   process=subprocess.Popen(argv,cwd=folder,stdout=out,stderr=err);capture['actual_child_pid']=process.pid;code=process.wait()
  capture.update(completed_utc=utc(),exit_code=code,stdout=pin(folder/'stdout.bin'),stderr=pin(folder/'stderr.bin'),source_after=pin(copy))
  (folder/'execution.json').write_text(json.dumps(capture,indent=2)+'\n')
  assert code==0 and (folder/'stderr.bin').read_bytes()==b'',capture
  actual=json.loads((folder/'CONTROL_RESULTS.json').read_text());old=json.loads(baseline.read_text())
  if label=='mechanism':
   assert actual['assertions']==old['assertions']==49 and actual['checks']==old['checks']
   assert actual['status']==old['status'] and actual['optimized']==0 and actual['actual_self_pid']==process.pid
   assert actual['cwd']==str(folder) and actual['sympy']=='1.14.0'
   for row in actual['loaded_modules']:
    got=pin(row['path']);assert (got['bytes'],got['sha256'])==(row['bytes'],row['sha256'])
   claim='49 exact mechanism controls and complete scientific check names reproduced; dynamic PID/time/runtime/module fields are not byte-identical portability assertions'
  else:
   assert {k:v for k,v in actual.items() if k!='completed_utc'}=={k:v for k,v in old.items() if k!='completed_utc'}
   assert actual['checks_passed'] is True and actual['mathematical_proof_dependency'] is False
   claim='Every finite mathematical stress-control value reproduced; only the actual completion time differs'
  captures.append(dict(native=capture,output=pin(folder/'CONTROL_RESULTS.json'),comparison=claim))
 result=dict(status='PASS_ROOT_FRESH_FINITE_PRIORITY_CONTROL_REPRODUCTION',UTC=utc(),actual_driver_pid=os.getpid(),
  argv=sys.argv,cwd=os.getcwd(),driver_source=source,captures=captures,unchanged_original_sources=True,
  all_actual_children_exit0_empty_stderr=True,optimization_disabled=True,
  limits='Finite algebra/dependence/bias/abstract-operator stress checks; not proof of the infinite PDE/statistical theorem or historical absence.')
 (A/'ROOT_PRIORITY_CONTROL_REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(status=result['status'],children=[c['native']['actual_child_pid'] for c in captures],count=len(captures))))
if __name__=='__main__':main()
