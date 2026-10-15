#!/usr/bin/env python3
"""Root actual replay of fully read independent finite controls in new private outputs."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr41_9700035'
O=A/'root_family_controls_actual_reproduction';O.mkdir(exist_ok=False)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def pin(path):
 raw=path.read_bytes();return dict(path=path.relative_to(O).as_posix(),bytes=len(raw),sha256=sha(raw))
def new(path,raw):
 with path.open('xb') as f:f.write(raw)
runs=[]
for label,original,arguments in (
 ('primary_finite',A/'primary_scope_family/finite_controls.py',['--output',str(O/'primary_finite_RESULT.json')]),
 ('network_measure_finite',A/'network_tail_measure_family/network_measure_controls.py',[]),
 ('network_manifest',A/'network_tail_measure_family/check_manifest.py',[str(A/'network_tail_measure_family')])):
 folder=O/label;folder.mkdir();raw=original.read_bytes();source=folder/'prelaunch_source.py';new(source,raw)
 argv=['/usr/bin/python3','-B',str(source),*arguments]
 record=dict(label=label,original_source=str(original.relative_to(R)),source_sha256=sha(raw),argv=argv,cwd=str(folder),started_utc=now(),actual_execution=True,stdin_supplied=False)
 child=subprocess.Popen(argv,cwd=folder,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);record['pid']=child.pid
 out,err=child.communicate(timeout=90)
 new(folder/'stdout.bin',out);new(folder/'stderr.bin',err)
 record.update(finished_utc=now(),completed=True,exit_code=child.returncode,status='PASS' if child.returncode==0 else 'FAIL',stdout=pin(folder/'stdout.bin'),stderr=pin(folder/'stderr.bin'))
 new(folder/'CAPTURE.json',(json.dumps(record,indent=2)+'\n').encode());runs.append(record)
 assert child.returncode==0 and original.read_bytes()==raw
 if label=='primary_finite':
  actual=json.loads((O/'primary_finite_RESULT.json').read_bytes());assert actual['status']=='PASS_INDEPENDENT_FINITE_CONTROLS' and actual['passed']==1326 and len(actual['checks'])==1326 and actual['failed']==0
 elif label=='network_measure_finite':
  actual=json.loads((folder/'NETWORK_MEASURE_CONTROL_RESULTS.json').read_bytes());old=json.loads((A/'network_tail_measure_family/NETWORK_MEASURE_CONTROL_RESULTS.json').read_bytes())
  assert actual==old and actual['checks_passed']==len(actual['checks'])==122
 else:
  actual=json.loads(out);assert actual=={'status':'PASS_EXACT_ROOT_CLOSURE','first_party':115,'foreign_separately_bound':8,'self_only':True}
result=dict(utc=now(),status='PASS',actual_outer_runs=runs,primary_finite_checks=1326,network_measure_checks=122,network_result_whole_saved_actual_equal=True,
 first_party_manifest_check=actual,original_substantive_attempts=2,new_substantive_attempts=0,audit_turns=0,
 scope='Genuine independent finite-control/manifest replays. No SIRSN simulation or universal mathematical proof by computation; original sources unchanged.')
new(O/'ROOT_FAMILY_REPRODUCTION.json',(json.dumps(result,indent=2)+'\n').encode())
files=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
new(O/'MANIFEST.json',(json.dumps(dict(self_excluded=['MANIFEST.json'],files_count=len(files),files=files),indent=2)+'\n').encode())
print(json.dumps(dict(status='PASS',actual_outer_runs=3,primary_finite_checks=1326,network_measure_checks=122,members=len(files),manifest_sha256=sha((O/'MANIFEST.json').read_bytes()))))
