"""Finalize only own SOURCE handoff after real complete collection/checks."""
import ast
import os
import sys
from common import *


def main():
    need(__debug__, 'No optimized SOURCE freeze')
    scope = load(N/'SCOPE.json')
    fixed = verify_fixed_scope(scope)
    for q in N.glob('*.py'):
        ast.parse(q.read_bytes(), filename=q.name)
    check = load(N/'SOURCE_VERIFICATION.json')
    need(check['status'] == 'PASS_READONLY_SOURCE_CHECKS', 'Actual earlier read-only Git/full-mode verification')
    prior = load(N/'SCOPE_PREVERIFICATION.json')
    need(scope['fixed_files'] == prior['fixed_files'] and scope['fixed_directories'] == prior['fixed_directories'], 'Whole verified selected evidence unchanged')
    for q in N.glob('source_*_actual_capture'):
        cap = load(q/'CAPTURE.json')
        need(cap['actual_execution'] and cap['completed'] and cap['exit_code'] == 0 and cap['ROOT_execution_or_approval'] is False, 'All complete SOURCE captures successful')
        verify_plain_refs([cap[k] for k in ['prelaunch_operator','prelaunch_common','stdout','stderr']])
    files = [plain_ref(q) for q in sorted(N.rglob('*')) if q.is_file() and q.name not in ['RESEARCH_LOG.md','SOURCE_READY.json']]
    current = {z['path'] for z in files} | {str((N/n).relative_to(R)) for n in ['RESEARCH_LOG.md','SOURCE_READY.json']}
    need(current == set(scope['new_preparation_source_paths']) | set(scope['runtime_stamped_log_paths']), 'Exact completed own SOURCE file domain')
    ready = dict(schema='ROOT-checkpoint-SOURCE-ready/v1', actual_preparation_writer_pid=os.getpid(),
                 argv=sys.argv, prepared_utc=now(), exact_scope=plain_ref(N/'SCOPE.json'),
                 source_files=files, source_ready_literal_self_exclusion=str((N/'SOURCE_READY.json').relative_to(R)),
                 runtime_log_prefix=plain_ref(N/'RESEARCH_LOG.md'), dedicated_runtime_log_only=True,
                 fixed_selected_files=len(fixed), fixed_selected_directories=len(scope['fixed_directories']),
                 selected_fixed_bytes=sum(v['bytes'] for v in scope['fixed_files']),
                 whole_fixed_families_selected=20, actual_ROOT_CAP4_sets=52,
                 formal_accepted_inventory='37/180', formal_accepted_percent=20.5556,
                 source_preparation_completion_percent=100, new_mathematical_discovery_percent=0,
                 source_readonly_verifier_pid=check['actual_pid'], verification_dated_not_future_protection_guarantee=True,
                 production_helpers_are_unexecuted=['stage_checkpoint.py','commit_checkpoint.py'],
                 stage_commit_push_executed=False, remote_push_helper_supplied=False,
                 ROOT_review_of_this_SOURCE_claimed=False, separate_readback_future_not_claimed=True,
                 mathematical_acceptance_or_paper_publication_DOI=False, native_acceptance_changed=False,
                 historical_failed_storage_and_V5_author_runs_preserved=True,
                 old1530_source_history_unchanged=True,
                 remaining_gap='ROOT personal whole SOURCE/scope review and fresh actual stage/commit/push gates; prior/source custody is not native acceptance.')
    exclusive(N/'SOURCE_READY.json', encoded(ready))
    print(encoded(dict(status='SOURCE_READY_UNEXECUTED_ROOT_HANDOFF', actual_writer_pid=os.getpid(),
                       ready=plain_ref(N/'SOURCE_READY.json'), fixed_files=len(fixed),
                       own_source_files=len(files)+2, selected_bytes=ready['selected_fixed_bytes'])).decode(), end='')


if __name__ == '__main__':
    main()
