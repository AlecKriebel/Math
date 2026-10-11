"""Actual preparer capture for allowlisted SOURCE operations; never ROOT execution."""
import argparse
import subprocess
import sys
from common import N, R, plain_ref, exclusive, encoded, now, need, digest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('operator', choices=['build_scope.py','verify_source.py','read_source.py'])
    ap.add_argument('capture_name')
    args = ap.parse_args()
    need(args.capture_name.startswith('source_') and args.capture_name.replace('_','').isalnum(), 'Literal own SOURCE capture name')
    q = N / args.capture_name
    if args.operator == 'read_source.py':
        need(args.capture_name == 'source_frozen_readback_actual_capture', 'One separate literal SOURCE readback capture')
        q = N.parent / 'checkpoint_20261003_1530_preparation_readback_actual_capture'
    q.mkdir(exist_ok=False)
    operator = N / args.operator
    pre = q / 'prelaunch_operator.py'
    exclusive(pre, operator.read_bytes())
    common_pre = q / 'prelaunch_common.py'
    exclusive(common_pre, (N/'common.py').read_bytes())
    argv = [sys.executable, '-B', str(operator)]
    started = now()
    child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    finished = now()
    exclusive(q/'stdout.bin', out)
    exclusive(q/'stderr.bin', err)
    cap = dict(schema='checkpoint-preparer-actual-SOURCE-capture/v1', operator_role='SOURCE_PREPARER', actual_execution=True,
               argv=argv, cwd=str(R), pid=child.pid, started_utc=started, finished_utc=finished, completed=True, exit_code=child.returncode,
               prelaunch_operator=plain_ref(pre), prelaunch_common=plain_ref(common_pre), stdout=plain_ref(q/'stdout.bin'), stderr=plain_ref(q/'stderr.bin'),
               operator_unchanged=digest(operator.read_bytes())==digest(pre.read_bytes()), common_unchanged=digest((N/'common.py').read_bytes())==digest(common_pre.read_bytes()),
               ROOT_execution_or_approval=False, native_or_Git_mutations_authorized=False)
    exclusive(q/'CAPTURE.json', encoded(cap))
    print(encoded(cap).decode(), end='')
    need(child.returncode == 0, 'Actual SOURCE child failed; all streams retained')


if __name__ == '__main__':
    main()
