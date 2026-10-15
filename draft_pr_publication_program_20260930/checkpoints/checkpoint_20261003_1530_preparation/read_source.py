"""Separate SOURCE readback: no Git calls, log stamp or production execution."""
import ast
import os
from common import *


def main():
    ready = load(N/'SOURCE_READY.json')
    need(ready['schema']=='ROOT-checkpoint-SOURCE-ready/v1' and ready['stage_commit_push_executed'] is False, 'Unexecuted SOURCE status')
    verify_plain_refs(ready['source_files'])
    scope = load(N/'SCOPE.json')
    fixed = verify_fixed_scope(scope)
    own = {str(q.relative_to(R)) for q in N.rglob('*') if q.is_file()}
    expected = set(scope['new_preparation_source_paths']) | set(scope['runtime_stamped_log_paths'])
    need(own==expected, 'Exact own fixed file domain; readback capture is separate')
    prefix = ready['runtime_log_prefix']
    need(plain_ref(path(prefix['path']))==prefix, 'Prepared log unchanged and no invented ROOT stamp')
    for q in N.glob('*.py'):
        ast.parse(q.read_bytes(), filename=q.name)
    for q in N.glob('source_*_actual_capture'):
        cap = load(q/'CAPTURE.json')
        need(cap['actual_execution'] and cap['completed'] and cap['ROOT_execution_or_approval'] is False, 'Truthful preparer CAP')
        verify_plain_refs([cap[k] for k in ['prelaunch_operator','prelaunch_common','stdout','stderr']])
    result = dict(status='PASS_SEPARATE_READONLY_SOURCE_READBACK', actual_pid=os.getpid(), utc=now(), source_ready=plain_ref(N/'SOURCE_READY.json'),
                  own_files=len(own), fixed_files=len(fixed), fixed_directories=len(scope['fixed_directories']),
                  own_bytes=sum(q.stat().st_size for q in N.rglob('*') if q.is_file()),
                  ROOT_approval=False, stage_commit_push_executed=False, no_git_calls=True)
    print(encoded(result).decode(),end='')


if __name__=='__main__':
    main()
