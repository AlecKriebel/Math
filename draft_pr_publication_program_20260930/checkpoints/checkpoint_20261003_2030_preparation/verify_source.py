"""Actual readonly administrative observation; production sources receive AST checks only."""
import ast, os
from common import *
def main():
    need(__debug__,'No optimized SOURCE checks')
    scope=load(N/'SCOPE_PREVERIFICATION.json');fixed=verify_fixed_scope(scope)
    for q in N.glob('*.py'):ast.parse(q.read_bytes(),filename=q.name)
    need(len(scope['completed_fixed_families'])==6 and len(scope['actual_ROOT_CAP4_sets'])==16,'Literal whole-family/CAP selection')
    own=sorted(fixed|set(scope['new_preparation_source_paths'])|set(scope['runtime_stamped_log_paths']))
    need(not set(own)&set(scope['forbidden_native_paths']) and all('\0' not in n and '\n' not in n for n in own),'Exact literal owned path domain')
    c=Commands(N/'source_verification_git_commands',operator_role='SOURCE_PREPARER_READONLY')
    head,gitdir,index=repository_gate(c);before=protection(c,own,index);count=len(c.records)
    try:c.git(['read-tree',head],index=N/'NEVER_CREATED_PRIVATE_INDEX')
    except RuntimeError:pass
    else:raise RuntimeError('Readonly SOURCE role allowed mutation')
    need(len(c.records)==count and not (N/'NEVER_CREATED_PRIVATE_INDEX').exists(),'Negative control launched no child/index')
    need(debug_flag_bits(b'x\0  ctime: 0:0\n  mtime: 0:0\n  dev: 1\tino: 1\n  uid: 1\tgid: 1\n  size: 0\tflags: 8000\n')=={b'x':0x8000},'Full integer index flags retained')
    for bad in [b'x',b'x\0junk',b'x\0  ctime: 0:0\n']:
        try:debug_flag_bits(bad)
        except RuntimeError:pass
        else:raise RuntimeError('Malformed flags accepted')
    repository_gate(c,head);after=protection(c,own,index);same_protection(before,after);verify_fixed_scope(scope)
    record=dict(schema='checkpoint2030-preparer-readonly-verification/v1',status='PASS_READONLY_SOURCE_CHECKS',
      actual_pid=os.getpid(),utc=now(),exact_preverification_scope=plain_ref(N/'SCOPE_PREVERIFICATION.json'),fixed_files=len(fixed),
      directories=len(scope['fixed_directories']),main_head=head,foreign_before=before,foreign_after=after,complete_readonly_commands=c.records,
      foreign_staged_count=len(before['foreign_staged']),foreign_dirty_body_count=len(before['foreign_dirty_worktree']),syntax_only_production_helpers=True,
      production_helpers_executed=False,actual_negative_controls=5,all_integer_index_flag_bits_bound=True,full_permission_bits_bound=True,
      ROOT_execution_or_approval=False,stage_commit_push_performed=False,
      temporal_limit='Only this actual before/after window is certified; earlier uncaptured status observation and future external activity are not certified unchanged.')
    exclusive(N/'SOURCE_VERIFICATION.json',encoded(record))
    print(encoded(dict(status=record['status'],actual_pid=os.getpid(),verification=plain_ref(N/'SOURCE_VERIFICATION.json'),
      readonly_commands=len(c.records),main_head=head,foreign_staged=record['foreign_staged_count'],foreign_dirty=record['foreign_dirty_body_count'])).decode(),end='')
if __name__=='__main__':main()
