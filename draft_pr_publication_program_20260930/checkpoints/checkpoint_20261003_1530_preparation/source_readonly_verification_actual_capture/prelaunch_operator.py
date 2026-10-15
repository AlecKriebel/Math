"""Own read-only SOURCE verification; production stage/commit code is never run."""
import ast
import os
import stat
from common import *


def main():
    scope = load(N/'SCOPE.json')
    fixed = verify_fixed_scope(scope)
    for name in ['common.py','stage_checkpoint.py','commit_checkpoint.py','build_scope.py','capture_source.py', 'verify_source.py']:
        ast.parse((N/name).read_bytes(), filename=name)
    need(scope['runtime_stamped_log_paths'] == [str((N/'RESEARCH_LOG.md').relative_to(R))], 'Dedicated log only')
    need(len(scope['closed_families']) == 5 and scope['externally_validated_geometry']['files'] == 70, 'Exact closure model')
    need(len(scope['actual_A45_CAP4_sets']) == 16, 'Exact actualROOT operations')
    own = sorted(fixed | set(scope['new_preparation_source_paths']) | set(scope['runtime_stamped_log_paths']))
    need(not set(own) & set(scope['forbidden_native_paths']), 'Native excluded')
    need(all('\0' not in v and '\n' not in v for v in own), 'Literal scope NUL encoding')
    c = Commands(N/'source_verification_git_commands', operator_role='SOURCE_PREPARER_READONLY')
    head, gitdir, real_index = repository_gate(c)
    before = protection(c, own, real_index)
    # Read-only negative control: a write-capable command must be rejected
    # before launching any child, even with a private index supplied.
    count = len(c.records)
    try:
        c.git(['read-tree',head], index=N/'NEVER_CREATED_PRIVATE_INDEX')
    except RuntimeError:
        pass
    else:
        raise RuntimeError('Read-only role unexpectedly allowed a write')
    need(len(c.records)==count and not (N/'NEVER_CREATED_PRIVATE_INDEX').exists(), 'Write negative control did not launch')
    need(debug_flag_bits(b'x\0  ctime: 0:0\n  mtime: 0:0\n  dev: 1\tino: 1\n  uid: 1\tgid: 1\n  size: 0\tflags: 8000\n') == {b'x':0x8000}, 'Integer flags preserved')
    for invalid in [b'x', b'x\0junk', b'x\0  ctime: 0:0\n']:
        try:
            debug_flag_bits(invalid)
        except RuntimeError:
            pass
        else:
            raise RuntimeError('Malformed integer flag control accepted')
    # The protection walk binds all foreign staged entries and full regular or
    # symlink worktree bodies/modes without copying their bodies.
    repository_gate(c,head)
    after = protection(c, own, real_index)
    same_protection(before,after)
    verify_fixed_scope(scope)
    result = dict(schema='checkpoint1530-preparer-readonly-verification/v1', status='PASS_READONLY_SOURCE_CHECKS', actual_pid=os.getpid(), utc=now(),
                  exact_scope=plain_ref(N/'SCOPE.json'), fixed_files=len(fixed), directories=len(scope['fixed_directories']),
                  syntax_only_helpers=True, production_helpers_executed=False, main_head=head,
                  foreign_before=before, foreign_after=after, complete_readonly_commands=c.records,
                  foreign_staged_count=len(before['foreign_staged']), foreign_dirty_body_count=len(before['foreign_dirty_worktree']),
                  all_integer_index_flag_bits_bound=True, full_permission_bits_bound=True, conversion_configuration_bound=True,
                  actual_negative_controls=5, ROOT_execution_or_approval=False, stage_commit_push_performed=False)
    exclusive(N/'SOURCE_VERIFICATION.json',encoded(result))
    print(encoded(dict(status=result['status'], actual_pid=os.getpid(), verification=plain_ref(N/'SOURCE_VERIFICATION.json'),
                       readonly_commands=len(c.records), foreign_staged_count=result['foreign_staged_count'], foreign_dirty_body_count=result['foreign_dirty_body_count'], main_head=head)).decode(),end='')


if __name__ == '__main__':
    main()
