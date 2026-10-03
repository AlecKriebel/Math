"""ROOT checks the complete actual PR44 freeze, outer child and final inner Git record."""
from pathlib import Path
import datetime as dt,hashlib,json,stat,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];C=A/'reviewed_candidate';sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def ref(p):
 b=p.read_bytes();return {'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b)}
def main():
 assert __debug__; (A/'ROOT_CURRENT_FREEZE_INSPECTION_PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
 m=load(C/'MANIFEST.json');assert len(m['files'])==m['files_count']==430 and m['self_excluded']==['MANIFEST.json']and m['full_problem_solved']is False
 assert {p.relative_to(C).as_posix()for p in C.rglob('*')if p.is_file()}=={z['path']for z in m['files']}|{'MANIFEST.json'}
 for p in C.rglob('*'):assert not p.is_symlink()and(p.is_dir()or(p.is_file()and stat.S_IMODE(p.stat().st_mode)==0o444))
 for z in m['files']:
  b=(C/z['path']).read_bytes();assert type(z['bytes'])is int and len(b)==z['bytes']and sha(b)==z['sha256']
 deps=load(C/'CURRENT_DEPENDENCIES.json');assert (R/deps['anchor_repository_relative']).resolve()==A
 for z in deps['files']:
  p=A/z['path'];assert not p.is_symlink()and all(not q.is_symlink()for q in p.parents);b=p.read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
 fresh=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');assert deps['current_native13']==fresh['files']and deps['current_main_head']==fresh['current_head']
 for z in fresh['files']:
  b=(R/z['path']).read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==fresh['current_head']
 snap=load(A/'snapshot_manifest_v2.json');assert len(snap['files'])==18
 for z in snap['files']:
  b=(A/'source_snapshot_v2'/z['path']).read_bytes();assert (C/'original_archive'/z['path']).read_bytes()==b
 for n in ['OBSTRUCTION.md','verify_group_block.py','group_block_verification.json','source_record.json','source_manifest.json','SOURCES.md','turns.jsonl','review/reviewed_obstruction.md','review/submitted_verifier.py','review/submitted_results.json','review/independent_checks.py','review/independent_results.json']:assert (C/n).read_bytes()==(A/'source_snapshot_v2'/n).read_bytes()
 for n in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']:
  j=load(C/n);assert j['status']=='unsolved'and j['full_problem_solved']is False and j['novelty_claimed']is False and j['original_substantive_attempts']==2 and j['new_substantive_attempts']==0 and j['audit_turns']==0 and j['current_gate']=='PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'
  assert all(j[k]is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict'])
 info=load(C/'CURRENT_EXECUTION_REFERENCE.json');d=A/info['audit_relative_outer_capture'];cap=load(d/'CAPTURE.json')
 assert cap['actual_execution']is True and cap['completed']is True and cap['exit_code']==0 and cap['pid']==64348 and cap['operator_pid']==64347 and cap['builder_unchanged_after_child']is True and cap['operator_unchanged_after_child']is True
 assert {q.name for q in d.iterdir()}=={'CAPTURE.json','OPERATION_PRELAUNCH.json','PRELAUNCH_BUILDER_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'}
 for k in ['stdout','stderr']:
  b=(d/cap[k]['path']).read_bytes();assert len(b)==cap[k]['bytes']and sha(b)==cap[k]['sha256']
 assert sha((d/'PRELAUNCH_BUILDER_SOURCE.py').read_bytes())==cap['builder_sha256']=='09948a4ca10ef5014cdd35ec75ea82bf10887a5fd6ec9400fee0239fcc04983d'
 assert sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==cap['operator_sha256']=='fe0f02ceea16a15895073bda8851a9b67baaf6f02c5da55bfe13a06dc01733ec'
 pre=load(d/'OPERATION_PRELAUNCH.json');assert pre['operator_pid']==cap['operator_pid']and pre['argv']==cap['argv']and sha((d/'OPERATION_PRELAUNCH.json').read_bytes())==info['outer_prelaunch_sha256']
 commands=load(A/info['audit_relative_inner_attempt']/'GIT_COMMANDS.json');assert len(commands)>0
 for cmd in commands:
  assert cmd['actual_execution']is True and cmd['completed']is True and cmd['exit_code']==0 and type(cmd['pid'])is int and cmd['pid']>0 and cmd['argv'][0]=='git'
  assert dt.datetime.fromisoformat(cap['started_utc'])<=dt.datetime.fromisoformat(cmd['started_utc'])<=dt.datetime.fromisoformat(cmd['finished_utc'])<=dt.datetime.fromisoformat(cap['finished_utc'])
  for k in ['stdout','stderr']:
   b=(A/info['audit_relative_inner_attempt']/cmd[k]['path']).read_bytes();assert len(b)==cmd[k]['bytes']and sha(b)==cmd[k]['sha256']
  assert cmd['stderr']['bytes']==0
 patch=load(C/'CURRENT_QUEUE_PATCH.json');queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes();assert sha(queue)==patch['whole_preimage_sha256'];old=patch['row_before'].encode();new=patch['row_prospective'].encode();after=queue.replace(old,new,1)
 assert sha(after)==patch['whole_prospective_sha256']and after.replace(new,old,1)==queue
 assert [i for i,(x,y)in enumerate(zip(old.split(b'|'),new.split(b'|')))if x!=y]==[8,9,11]
 source_m=load(A/'current_source_adversary_family/SELF_MANIFEST.json');assert {q.relative_to(A/'current_source_adversary_family').as_posix()for q in(A/'current_source_adversary_family').rglob('*')if q.is_dir()}==set(source_m['directories'])
 result={'schema':'pr44-root-complete-actual-current-freeze-inspection/v1','status':'PASS','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'current_manifest':ref(C/'MANIFEST.json'),'current_files':430,'complete_dependency_manifest':ref(C/'CURRENT_DEPENDENCIES.json'),'individual_dependencies':len(deps['files']),'original18_and_twelve_science_members_byte_exact':True,'full0444_current_closure':True,'all13_and_actualHEAD_preserved':True,'entire_actual_outer_capture':cap,'actual_final_inner_GIT_COMMANDS':ref(A/info['audit_relative_inner_attempt']/'GIT_COMMANDS.json'),'final_inner_command_count':len(commands),'scope':'UNSOLVED standard conditional partial; both geometric realization gaps; new whole-current gatePENDING; no paper/DOI/tracker/novelty','original_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False}
 with(A/'ROOT_CURRENT_FREEZE_INSPECTION.json').open('x')as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps({'status':'PASS_COMPLETE_CURRENT_FREEZE','current_manifest':result['current_manifest'],'dependencies':len(deps['files']),'commands':len(commands)}))
if __name__=='__main__':main()
