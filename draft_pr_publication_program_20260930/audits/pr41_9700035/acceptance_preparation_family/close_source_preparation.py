#!/usr/bin/env python3
"""Own preparation closure only. Does not import/execute proposed helpers."""
import ast
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path,PurePosixPath

P=Path(__file__).resolve().parent
def parse(b):
 def pairs(rr):
  out={}
  for k,v in rr:
   assert k not in out;out[k]=v
  return out
 def floating(v):
  z=float(v);assert math.isfinite(z);return z
 return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def sha(b):return hashlib.sha256(b).hexdigest()

target=P/'PREPARATION_MANIFEST.json';assert not target.exists() and not target.is_symlink()
files=[];dirs=set()
for q in sorted(P.rglob('*')):
 assert not q.is_symlink()
 if q.is_dir():dirs.add(q.relative_to(P).as_posix());continue
 assert q.is_file();n=q.relative_to(P).as_posix();parts=PurePosixPath(n).parts
 assert not {'.','..','.git','__pycache__'}.intersection(parts)
 b=q.read_bytes()
 if q.suffix=='.json':parse(b)
 if q.suffix=='.py':ast.parse(b)
 files.append({'path':n,'bytes':len(b),'sha256':sha(b)})
assert dirs=={q.as_posix() for n in [z['path'] for z in files] for q in PurePosixPath(n).parents if q.as_posix()!='.'}
assert len(files)==len({z['path'] for z in files})
final=parse((P/'FINAL_STATIC_INSPECTION.json').read_bytes())
assert final['status']=='PASS_OWN_FULL_SOURCE_READ_AND_STATIC_ONLY_CHECK' and final['proposed_helpers_imported_or_executed'] is False and final['future_gate_PASS_claimed'] is False
for z in final['helper_sources']:
 q=P/Path(z['path']).name;b=q.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
capture=parse((P/'final_static_actual_capture/CAPTURE.json').read_bytes());assert type(capture['pid']) is int and capture['pid']==91419 and type(capture['exit_code']) is int and capture['exit_code']==0
assert capture['actual_execution'] is True and capture['completed'] is True and capture['stdin_supplied'] is False
for z in [capture['stdout'],capture['stderr']]:
 b=(P/'final_static_actual_capture'/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
assert sha((P/'final_static_actual_capture/prelaunch_source.py').read_bytes())==capture['source_sha256']
for z in files:(P/z['path']).chmod(0o444)
obj={'schema':'pr41-source-only-acceptance-preparation-strict-closure/v1','status':'CLOSED_SOURCE_ONLY_ACCEPTANCE_PREPARATION','closed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_administrative_closure_pid':os.getpid(),'self_excluded':['PREPARATION_MANIFEST.json'],'files_count':len(files),'files':files,'individual_external_foreign_bindings_in':'INPUT_BINDINGS.json','foreign_prefix_exclusions':[],'all_authored_members_mode':'0444','proposed_helpers_imported_or_executed':False,'native_canonical_Git_index_remote_shared_writes':False,'future_final_reconciliation_integration_native_post_PASS_claimed':False,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'paper_or_new_DOI_or_tracker':False,'source_preparation_completion_estimate_percent':100,'actual_acceptance_execution_estimate_percent':0,'unconditional_discovery_estimate_percent':0,'fresh_independent_source_review_and_ROOT_full_read':'REQUIRED_BEFORE_PROPOSED_EXECUTION'}
with target.open('xb') as stream:
 stream.write((json.dumps(obj,indent=2)+'\n').encode());stream.flush();os.fsync(stream.fileno())
target.chmod(0o444)
for z in files:
 q=P/z['path'];b=q.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'] and q.stat().st_mode&0o777==0o444
assert target.stat().st_mode&0o777==0o444
print(json.dumps({'status':'CLOSED_SOURCE_ONLY_ACCEPTANCE_PREPARATION','administrative_pid':os.getpid(),'files_count':len(files),'manifest_sha256':sha(target.read_bytes()),'helpers':{n:sha((P/n).read_bytes()) for n in ['pr41_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']},'proposed_helpers_imported_or_executed':False,'future_actual_gates':'PENDING'},indent=2))
