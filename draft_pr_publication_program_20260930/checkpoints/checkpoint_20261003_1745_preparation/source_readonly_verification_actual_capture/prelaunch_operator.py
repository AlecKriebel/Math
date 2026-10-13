"""Own read-only SOURCE verification; never execute stage/commit sources."""
import ast
import os
from common import *


def main():
    need(__debug__, 'No optimized SOURCE checks')
    scope = load(N/'SCOPE_PREVERIFICATION.json')
    fixed = verify_fixed_scope(scope)
    for q in N.glob('*.py'):
        ast.parse(q.read_bytes(), filename=q.name)
    need(scope['runtime_stamped_log_paths'] == [str((N/'RESEARCH_LOG.md').relative_to(R))], 'Dedicated own log only')
    need(len(scope['completed_fixed_families']) == 20, 'Exact whole-family selection')
    need(len(scope['actual_ROOT_CAP4_sets']) == 52, 'Exact genuine completed ROOT operations')
    own = sorted(fixed | set(scope['new_preparation_source_paths']) | set(scope['runtime_stamped_log_paths']))
    need(not set(own) & set(scope['forbidden_native_paths']), 'No native/shared log staging')
    need(all('\0' not in n and '\n' not in n for n in own), 'Literal owned NUL scope')
    c = Commands(N/'source_verification_git_commands', operator_role='SOURCE_PREPARER_READONLY')
    head, gitdir, index = repository_gate(c)
    before = protection(c, own, index)
    count = len(c.records)
    try:
        c.git(['read-tree',head], index=N/'NEVER_CREATED_PRIVATE_INDEX')
    except RuntimeError:
        pass
    else:
        raise RuntimeError('SOURCE role allowed mutation')
    need(len(c.records) == count and not (N/'NEVER_CREATED_PRIVATE_INDEX').exists(), 'No negative-control child/index created')
    need(debug_flag_bits(b'x\0  ctime: 0:0\n  mtime: 0:0\n  dev: 1\tino: 1\n  uid: 1\tgid: 1\n  size: 0\tflags: 8000\n') == {b'x':0x8000}, 'Integer flag bits are retained')
    for bad in [b'x', b'x\0junk', b'x\0  ctime: 0:0\n']:
        try:
            debug_flag_bits(bad)
        except RuntimeError:
            pass
        else:
            raise RuntimeError('Malformed flags accepted')
    repository_gate(c, head)
    after = protection(c, own, index)
    same_protection(before, after)
    verify_fixed_scope(scope)
    result = dict(schema='checkpoint1745-preparer-readonly-verification/v1', status='PASS_READONLY_SOURCE_CHECKS',
                  actual_pid=os.getpid(), utc=now(), exact_preverification_scope=plain_ref(N/'SCOPE_PREVERIFICATION.json'),
                  fixed_files=len(fixed), directories=len(scope['fixed_directories']), main_head=head,
                  foreign_before=before, foreign_after=after, complete_readonly_commands=c.records,
                  foreign_staged_count=len(before['foreign_staged']), foreign_dirty_body_count=len(before['foreign_dirty_worktree']),
                  syntax_only_helpers=True, production_helpers_executed=False, all_integer_index_flag_bits_bound=True,
                  full_permission_bits_bound=True, conversion_configuration_bound=True,
                  actual_negative_controls=5, ROOT_execution_or_approval=False, stage_commit_push_performed=False)
    exclusive(N/'SOURCE_VERIFICATION.json', encoded(result))
    print(encoded(dict(status=result['status'], actual_pid=os.getpid(), verification=plain_ref(N/'SOURCE_VERIFICATION.json'),
                       readonly_commands=len(c.records), foreign_staged_count=result['foreign_staged_count'],
                       foreign_dirty_body_count=result['foreign_dirty_body_count'], main_head=head)).decode(), end='')


if __name__ == '__main__':
    main()
