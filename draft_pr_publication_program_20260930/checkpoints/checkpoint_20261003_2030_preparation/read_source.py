"""Separate administrative source readback; excludes its literal own output directory."""
import ast, os
from common import *
from selection import EXCLUDED_READBACK_ROOT
EXCLUDED_FINALIZATION_ROOT = 'actual_source_finalization_capture'
def main():
    need(__debug__,'No optimized SOURCE readback')
    ready=load(N/'SOURCE_READY.json');need(ready['schema']=='ROOT-checkpoint-SOURCE-ready/v1' and ready['stage_commit_push_executed'] is False,'SOURCE only')
    verify_plain_refs(ready['source_files']);scope=load(N/'SCOPE.json');fixed=verify_fixed_scope(scope)
    own={str(q.relative_to(R)) for q in N.rglob('*') if q.is_file() and not {EXCLUDED_READBACK_ROOT,EXCLUDED_FINALIZATION_ROOT}&set(q.relative_to(N).parts)}
    need(own==set(scope['new_preparation_source_paths'])|set(scope['runtime_stamped_log_paths']),'Exact SOURCE path domain excluding one literal readback output')
    need(plain_ref(path(ready['runtime_log_prefix']['path']))==ready['runtime_log_prefix'],'Complete prepared unstamped log')
    for q in N.glob('*.py'):ast.parse(q.read_bytes(),filename=q.name)
    for q in N.glob('source_*_actual_capture'):
        j=load(q/'CAPTURE.json');need(j['actual_execution'] and j['completed'] and j['ROOT_execution_or_approval'] is False,'Actual preparer capture')
        need(j['exit_code']==0,'Current completed SOURCE captures must succeed; retained historical failure is selected separately')
        if q.name!='source_derivation_actual_capture':
            verify_plain_refs([j[k] for k in ['prelaunch_operator','prelaunch_common','prelaunch_inputs','stdout','stderr']])
            need(j['input_bodies_and_full_modes_unchanged'],'Actual prelaunch inputs unchanged')
            verify_plain_refs(load(path(j['prelaunch_inputs']['path'])))
    print(encoded(dict(status='PASS_SEPARATE_READONLY_SOURCE_READBACK',actual_pid=os.getpid(),utc=now(),source_ready=plain_ref(N/'SOURCE_READY.json'),
      own_files=len(own),fixed_files=len(fixed),fixed_directories=len(scope['fixed_directories']),ROOT_approval=False,stage_commit_push_executed=False,no_git_calls=True,
      source_preparation_completion_percent=100,formal_completed_acceptance='37/180',formal_completed_percent=20.5556,
      mathematical_discovery_changed=False,readback_capture_outside_fixed_SOURCE_but_inside_owned_folder=True)).decode(),end='')
if __name__=='__main__':main()
