#!/usr/bin/env python3
"""Own status and closure only; no proposed helper imported/compiled/executed."""
import ast
import datetime as dt
import hashlib
import json
import math
import os
import stat
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent;A=P.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def parse(b):
 def pairs(rr):
  o={}
  for k,v in rr:
   assert k not in o;o[k]=v
  return o
 def floating(v):
  x=float(v);assert math.isfinite(x);return x
 return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def put(n,v):
 q=P/n;assert not q.exists();q.write_text(json.dumps(v,indent=2)+'\n')
check=parse((P/'FINAL_STATIC_INSPECTION.json').read_bytes());assert check['status']=='PASS_OWN_FULL_BYTE_READ_AND_STATIC_V2_SOURCE_INSPECTION' and check['actual_pid']==18492
assert check['candidate_helpers_imported_compiled_or_executed'] is False and check['future_runtime_PASS_claimed'] is False and check['private_specification_controls']==39
for name,pid in [('source_revision_actual_capture',12550),('private_inspection_actual_capture',18492)]:
 root=P/name;c=parse((root/'CAPTURE.json').read_bytes());assert type(c['pid']) is int and c['pid']==pid and type(c['exit_code']) is int and c['exit_code']==0
 assert c['actual_execution'] is True and c['completed'] is True and c['stdin_supplied'] is False and c['source_after_unchanged'] is True
 for z in [c['stdout'],c['stderr']]:
  b=(root/z['path']).read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
 assert sha((root/'prelaunch_source.py').read_bytes())==c['source_sha256']
for root,name,pin in [(A/'acceptance_preparation_family','PREPARATION_MANIFEST.json','6e8d07a73f68177ae3b7f446a1416ae39eabd560352fd7685464bcb129d0bcdc'),(A/'acceptance_static_adversary_family','FIRST_PARTY_MANIFEST.json','31c82a50855cf621859d6bfa182541ec07d77a3727d621ce4adc99597620c6c0')]:
 assert sha((root/name).read_bytes())==pin and stat.S_IMODE((root/name).stat().st_mode)==0o444
 m=parse((root/name).read_bytes());assert len(m['files'])==35
 for z in m['files']:
  q=root/z['path'];b=q.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444
for z in check['final_helper_sources']:
 q=P/Path(z['path']).name;b=q.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256']
now=dt.datetime.now(dt.timezone.utc).isoformat()
put('REPAIR_RESULT.json',{'schema':'pr41-source-only-v2-mandatory-administrative-repair-proposal/v1','utc':now,'status':'SOURCE_ONLY_S1_S2_S3_REPAIRS_PREPARED_PENDING_NEW_ADVERSARY','mandatory_findings_addressed':['S1','S2','S3'],'proof_or_current547_math_changed':False,'old_preparation_and_adversary_preserved':True,'final_sources':check['final_helper_sources'],'own_static_and_private_model_inspection_pid':18492,'private_specification_controls':39,'own_failed_V2_captured_runs':[],'candidate_helpers_imported_compiled_or_executed':False,'native_canonical_Git_index_remote_shared_writes':False,'future_runtime_PASS_claimed':False,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'novelty_claimed':False,'paper_or_new_DOI_or_tracker':False,'source_preparation_completion_estimate_percent':100,'actual_acceptance_execution_estimate_percent':0,'unconditional_discovery_estimate_percent':0,'next_required':'New different independent V2 source adversary and actual ROOT full read before approved future runtime bindings/execution.'})
put('SOURCE_STATUS.json',{'status':'SOURCE_ONLY_V2_SELF_REVIEW_COMPLETE_PENDING_NEW_INDEPENDENT_REVIEW_AND_ROOT_EXECUTION','utc':now,'source_preparation_completion_estimate_percent':100,'actual_acceptance_execution_estimate_percent':0,'unconditional_discovery_estimate_percent':0,'candidate_helpers_imported_compiled_or_executed':False,'future_runtime_PASS_claimed':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'full_problem_solved':False,'novelty_claimed':False,'paper_or_new_DOI_or_tracker':False})
target=P/'PREPARATION_MANIFEST.json';assert not target.exists() and not target.is_symlink();files=[];dirs=set()
for q in sorted(P.rglob('*')):
 assert not q.is_symlink()
 if q.is_dir():dirs.add(q.relative_to(P).as_posix());continue
 assert q.is_file();n=q.relative_to(P).as_posix();assert not {'.','..','.git','__pycache__'}.intersection(PurePosixPath(n).parts)
 b=q.read_bytes();assert len(b)<100*1024*1024
 if q.suffix=='.json':parse(b)
 if q.suffix=='.py':ast.parse(b)
 files.append({'path':n,'bytes':len(b),'sha256':sha(b)})
assert len(files)==len({z['path'] for z in files})
assert dirs=={q.as_posix() for n in [z['path'] for z in files] for q in PurePosixPath(n).parents if q.as_posix()!='.'}
for z in files:(P/z['path']).chmod(0o444)
manifest={'schema':'pr41-v2-source-only-acceptance-preparation-strict-closure/v1','status':'CLOSED_SOURCE_ONLY_ACCEPTANCE_PREPARATION_V2','closed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_administrative_closure_pid':os.getpid(),'self_excluded':['PREPARATION_MANIFEST.json'],'files_count':len(files),'files':files,'exact_directories':sorted(dirs),'all_authored_files_mode':'0444_STAT_S_IMODE','previous_preparation_manifest_sha256':'6e8d07a73f68177ae3b7f446a1416ae39eabd560352fd7685464bcb129d0bcdc','independent_adversary_manifest_sha256':'31c82a50855cf621859d6bfa182541ec07d77a3727d621ce4adc99597620c6c0','individual_external_bindings_in':'INPUT_BINDINGS.json','foreign_prefix_exclusions':[],'candidate_helpers_imported_compiled_or_executed':False,'native_canonical_Git_index_remote_shared_writes':False,'future_actual_PASS_claimed':False,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'novelty_claimed':False,'paper_or_new_DOI_or_tracker':False,'source_preparation_completion_estimate_percent':100,'actual_acceptance_execution_estimate_percent':0,'unconditional_discovery_estimate_percent':0,'new_different_adversary_and_ROOT_full_read':'REQUIRED_BEFORE_PROPOSED_EXECUTION'}
with target.open('xb') as stream:stream.write((json.dumps(manifest,indent=2)+'\n').encode());stream.flush();os.fsync(stream.fileno())
target.chmod(0o444)
for z in files:
 q=P/z['path'];b=q.read_bytes();assert len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444
assert stat.S_IMODE(target.stat().st_mode)==0o444
print(json.dumps({'status':'CLOSED_SOURCE_ONLY_ACCEPTANCE_PREPARATION_V2','administrative_pid':os.getpid(),'manifest_sha256':sha(target.read_bytes()),'files_count':len(files),'largest_authored_file_bytes':max(z['bytes'] for z in files),'final_source_sha256':{n:sha((P/n).read_bytes()) for n in ['pr41_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']},'candidate_helpers_imported_compiled_or_executed':False,'future_actual_gates':'PENDING'},indent=2))
