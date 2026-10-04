#!/usr/bin/env python3
"""Root actual child capture and independent fresh native-input checks for PR39."""
import argparse
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr39_9500008'
S=A/'acceptance_preparation_family'
PREP='f66df61cb4b57ae63cc007fed3c4dabf9e67e027f1d428d4e0ffbc75a6332fca'
GUARD='35922e8739cdfce8f93929bc78c18e464fa529e82f2481b9f2a2e9ac474aaf6d'
SOURCE_HASHES={'seal_final_evidence.py':'d1ee189304b48f1b21b54b3adcd82e22fce6a8d03d0df663dfde10bc3081df8b',
 'integrate_reviewed_partial.py':'42be7ce20e4231a83b72a01c01b01c28f8790a09f54ee4783b7734440661612a',
 'state_mirror_reconciliation.py':'0958f01368a3e41bcf56098bc28c66ad8d4e70c69a8a46e78877b035f5a53e9d',
 'verify_post_acceptance.py':'a072de3cacdeedc6ac546b7023baf5ffb6e2474200a5d5abe4c5ba21a60fc1e7'}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def fresh_inputs():
 names=[x['path'] for x in json.loads((A/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes())['files']]
 assert len(names)==13 and len(set(names))==13
 return [dict(path=n,bytes=len((R/n).read_bytes()),sha256=sha((R/n).read_bytes())) for n in names]
def write_new(path,data):
 with path.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('phase',choices=['final','preflight','overlay','prepush','finalize','mirror','post'])
parser.add_argument('--reviewed-plan-sha256')
parser.add_argument('--reviewed-gate-arguments-sha256')
args=parser.parse_args();phase=args.phase
assert subprocess.check_output(['git','branch','--show-current'],cwd=R).strip()==b'main'
assert sha((S/'PREPARATION_MANIFEST.json').read_bytes())==PREP
assert sha((S/'pr39_guards.py').read_bytes())==GUARD
filename={'final':'seal_final_evidence.py','mirror':'state_mirror_reconciliation.py','post':'verify_post_acceptance.py'}.get(phase,'integrate_reviewed_partial.py')
source=S/filename;raw=source.read_bytes();assert sha(raw)==SOURCE_HASHES[filename]
argv=['/usr/bin/python3','-B',str(source)]
if phase=='final':
 plan=A/'ROOT_REVIEWED_FINAL_PLAN.json'
 assert args.reviewed_plan_sha256 and sha(plan.read_bytes())==args.reviewed_plan_sha256
 argv+=['--execute','--preparation-manifest-sha256',PREP,'--plan',str(plan.relative_to(R)),'--plan-sha256',args.reviewed_plan_sha256]
else:
 gatepath=A/'ROOT_REVIEWED_GATE_ARGUMENTS.json'
 assert args.reviewed_gate_arguments_sha256 and sha(gatepath.read_bytes())==args.reviewed_gate_arguments_sha256
 gates=json.loads(gatepath.read_bytes())
 if phase not in ('mirror','post'):argv.append(phase)
 argv+=['--execute']
 for key,value in gates['explicit_arguments'].items():argv+=['--'+key,value]
 if phase in ('preflight','overlay'):
  review=A/('ROOT_FRESH_MAIN_PREIMAGES.json' if phase=='preflight' else 'ROOT_AUTOMATIC_MERGE_INSPECTION.json')
  reviewed=json.loads(review.read_bytes())
  queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes()
  assert sha(queue)==reviewed['whole_queue_sha256']
  argv+=['--'+('fresh-queue' if phase=='preflight' else 'merge-queue')+'-preimage-sha256',sha(queue)]
before=fresh_inputs();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
if phase=='preflight':
 reviewed=json.loads((A/'ROOT_FRESH_MAIN_PREIMAGES.json').read_bytes())
 assert before==reviewed['files'] and head==reviewed['head']
destination=A/('root_final_reconciliation_actual_capture' if phase=='final' else 'root_integration_'+phase+'_actual_capture')
assert not destination.exists() and not destination.is_symlink()
stage=A/(destination.name+'.stage.'+now().replace(':','-'));stage.mkdir(mode=0o700)
write_new(stage/'prelaunch_source.py',raw)
if phase!='final':write_new(stage/'prelaunch_guards.py',(S/'pr39_guards.py').read_bytes())
record=dict(schema='pr39-root-genuine-child-and-native13-capture/v1',phase=phase,
 source_sha256=sha(raw),guards_sha256=GUARD,argv=argv,cwd=str(A),started_utc=now(),
 actual_execution=True,stdin_supplied=False,head_before=head,fresh_native13_before=before)
child=subprocess.Popen(argv,cwd=A,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
record['pid']=child.pid
try:
 out,err=child.communicate(timeout=180)
 timeout=False
except subprocess.TimeoutExpired:
 child.kill();out,err=child.communicate();timeout=True
write_new(stage/'stdout.bin',out);write_new(stage/'stderr.bin',err)
after=fresh_inputs();afterhead=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
changes={a['path'] for a,b in zip(before,after) if a!=b}
allowed={'overlay':{'unsolved_math_prioritization/QUEUE.md'},'finalize':{'draft_pr_publication_program_20260930/inventory.json'},
 'mirror':{'unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}}.get(phase,set())
native_ok=changes<=allowed and afterhead==head
record.update(finished_utc=now(),completed=True,exit_code=child.returncode,timed_out=timeout,
 status='PASS' if child.returncode==0 and native_ok and not timeout else 'FAIL',
 stdout=dict(path='stdout.bin',bytes=len(out),sha256=sha(out)),stderr=dict(path='stderr.bin',bytes=len(err),sha256=sha(err)),
 fresh_native13_after=after,actual_changed_native_inputs=sorted(changes),allowed_changed_native_inputs=sorted(allowed),
 independent_native13_and_HEAD_checks_pass=native_ok,head_after=afterhead)
write_new(stage/'CAPTURE.json',(json.dumps(record,indent=2)+'\n').encode())
lib=ctypes.CDLL(None,use_errno=True);rename=lib.renamex_np
rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
if rename(os.fsencode(stage),os.fsencode(destination),0x4)!=0:
 code=ctypes.get_errno();raise OSError(code,os.strerror(code),str(destination))
print(json.dumps(dict(phase=phase,status=record['status'],pid=child.pid,exit_code=child.returncode,
 capture_sha256=sha((destination/'CAPTURE.json').read_bytes()),stdout=out.decode(),stderr=err.decode(),native13_ok=native_ok)))
sys.exit(0 if record['status']=='PASS' else 1)
