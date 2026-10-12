"""Publish only own fixed SOURCE handoff; do not execute ROOT helpers or change historical modes."""
import ast, os, sys
from common import *
from selection import EXCLUDED_READBACK_ROOT
EXCLUDED_FINALIZATION_ROOT = 'actual_source_finalization_capture'
def main():
    need(__debug__,'No optimized SOURCE checks')
    scope=load(N/'SCOPE.json');fixed=verify_fixed_scope(scope);prior=load(N/'SCOPE_PREVERIFICATION.json')
    need(scope['fixed_files']==prior['fixed_files'] and scope['fixed_directories']==prior['fixed_directories'],'Selected evidence unchanged since actual verifier')
    check=load(N/'SOURCE_VERIFICATION.json');need(check['status']=='PASS_READONLY_SOURCE_CHECKS','Actual administrative consistency recorded')
    for q in N.glob('*.py'):ast.parse(q.read_bytes(),filename=q.name)
    for q in N.glob('source_*_actual_capture'):
        j=load(q/'CAPTURE.json');need(j['actual_execution'] and j['completed'] and j['ROOT_execution_or_approval'] is False,'Actual complete preparer capture')
        need(j['exit_code']==0,'Current completed SOURCE captures must succeed; retained historical failure is selected separately')
        if q.name=='source_derivation_actual_capture':
            for k in ['prelaunch_operator','prelaunch_controller','stdout','stderr']:
                z=j[k];a=plain_ref(N/z['path']);need({k:a[k] for k in ['bytes','sha256','full_mode']}=={k:z[k] for k in ['bytes','sha256','full_mode']},'Actual derivation capture body/mode')
        else:
            verify_plain_refs([j[k] for k in ['prelaunch_operator','prelaunch_common','prelaunch_inputs','stdout','stderr']])
            need(j['input_bodies_and_full_modes_unchanged'],'Actual prelaunch inputs unchanged through child')
            verify_plain_refs(load(path(j['prelaunch_inputs']['path'])))
    rows=[plain_ref(q) for q in sorted(N.rglob('*')) if q.is_file() and q.name not in ['RESEARCH_LOG.md','SOURCE_READY.json']
          and not {EXCLUDED_READBACK_ROOT,EXCLUDED_FINALIZATION_ROOT}&set(q.relative_to(N).parts)]
    current={z['path'] for z in rows}|{str((N/n).relative_to(R)) for n in ['RESEARCH_LOG.md','SOURCE_READY.json']}
    need(current==set(scope['new_preparation_source_paths'])|set(scope['runtime_stamped_log_paths']),'Exact prepared SOURCE path domain')
    completion=now();oldlog=plain_ref(N/'RESEARCH_LOG.md')
    line='\n'+completion+' — SOURCE conditions verified by actual own finalizer'+str(os.getpid())+'; checkpoint preparation100% at this SOURCE_READY handoff, separate readback still pending. Formal completed program37/180 (20.56%); mathematical/discovery progress unchanged; proposed production helpers remain unexecuted.\n'
    with (N/'RESEARCH_LOG.md').open('ab') as f:f.write(line.encode());f.flush();os.fsync(f.fileno())
    ready=dict(schema='ROOT-checkpoint-SOURCE-ready/v1',actual_preparation_writer_pid=os.getpid(),argv=sys.argv,prepared_utc=completion,
      exact_scope=plain_ref(N/'SCOPE.json'),source_files=rows,source_ready_literal_self_exclusion=str((N/'SOURCE_READY.json').relative_to(R)),
      runtime_log_prefix=plain_ref(N/'RESEARCH_LOG.md'),log_prefix_before_actual_preparer_completion=oldlog,
      dedicated_runtime_log_only=True,fixed_selected_files=len(fixed),
      fixed_selected_directories=len(scope['fixed_directories']),selected_fixed_bytes=sum(v['bytes'] for v in scope['fixed_files']),
      whole_fixed_families_selected=6,actual_ROOT_CAP4_sets=16,completed_rollback_quarantine_files=13,storage_readback_packet_files=13,
      formal_accepted_inventory='37/180',formal_accepted_percent=20.5556,selected_rollback_does_not_complete_native_acceptance=True,
      source_preparation_completion_percent=100,mathematical_discovery_changed=False,source_readonly_verifier_pid=check['actual_pid'],
      verification_dated_not_future_protection_guarantee=True,production_helpers_are_unexecuted=['stage_checkpoint.py','commit_checkpoint.py'],
      stage_commit_push_executed=False,remote_push_helper_supplied=False,ROOT_review_of_this_SOURCE_claimed=False,
      separate_source_readback_not_yet_claimed=True,excluded_own_future_readback_output=str((N/EXCLUDED_READBACK_ROOT).relative_to(R)),
      excluded_own_finalization_capture_output=str((N/EXCLUDED_FINALIZATION_ROOT).relative_to(R)),
      source_file_modes_bound_not_chmod_frozen=True,native_acceptance_changed=False,mathematical_acceptance_or_paper_publication_DOI=False,
      old1915_source_and_actual_receipts_unchanged=True,historical_FAILED80414_and80480_unchanged_already_checkpointed=True,
      remaining_gap='ROOT personal full source/scope review and fresh actual stage/commit/push gates after recovery; this SOURCE preparation adds no acceptance or discovery.')
    exclusive(N/'SOURCE_READY.json',encoded(ready))
    print(encoded(dict(status='SOURCE_READY_UNEXECUTED_ROOT_HANDOFF',actual_writer_pid=os.getpid(),ready=plain_ref(N/'SOURCE_READY.json'),
      fixed_files=len(fixed),own_source_files=len(rows)+2,selected_bytes=ready['selected_fixed_bytes'])).decode(),end='')
if __name__=='__main__':main()
