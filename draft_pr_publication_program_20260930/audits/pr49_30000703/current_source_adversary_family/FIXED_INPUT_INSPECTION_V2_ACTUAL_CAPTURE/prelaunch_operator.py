"""Capture actual PR49 current SOURCE adversarial operations and complete streams."""
from pathlib import Path
import argparse, datetime as dt, hashlib, json, os, subprocess, sys, traceback

A = Path(__file__).resolve().parent
R = Path('/Users/alec/Documents/Math')

def sha(body):
    return hashlib.sha256(body).hexdigest()

def write(path, body):
    with path.open('xb') as stream:
        stream.write(body)
        stream.flush()
        os.fsync(stream.fileno())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target-source')
    parser.add_argument('--expected-exit', type=int, default=0)
    parser.add_argument('capture_name')
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    assert args.capture_name not in ('.', '..') and '/' not in args.capture_name
    argv = args.argv[1:] if args.argv and args.argv[0] == '--' else args.argv
    assert argv and all(type(item) is str for item in argv)
    directory = A / args.capture_name
    directory.mkdir(mode=0o700)
    source = Path(__file__).read_bytes()
    write(directory / 'prelaunch_operator.py', source)
    target = None
    target_path = None
    if args.target_source is not None:
        target_path = Path(args.target_source).resolve()
        assert A in target_path.parents and target_path.is_file() and not target_path.is_symlink()
        target = target_path.read_bytes()
        write(directory / 'prelaunch_target.py', target)
    record = dict(schema='pr49-current-source-adversary-actual-command/v1', argv=argv, cwd=str(R), operator_pid=os.getpid(), started_utc=dt.datetime.now(dt.timezone.utc).isoformat(), actual_execution=False, pid=None, completed=False, exit_code=None, expected_exit=args.expected_exit, stdin_supplied=False, operator_sha256=sha(source), target_source=None, target_unchanged=None)
    if target is not None:
        record['target_source'] = dict(path=str(target_path), bytes=len(target), sha256=sha(target))
    write(directory / 'PRELAUNCH.json', (json.dumps(record, indent=2, sort_keys=True) + '\n').encode())
    out, err = b'', b''
    try:
        child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        record.update(actual_execution=True, pid=child.pid)
        out, err = child.communicate()
        record.update(completed=True, exit_code=child.returncode)
    except BaseException:
        record['operator_error'] = traceback.format_exc()
    record['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    for name, body in [('stdout', out), ('stderr', err)]:
        write(directory / (name + '.bin'), body)
        record[name] = dict(path=name + '.bin', bytes=len(body), sha256=sha(body))
    record['operator_unchanged'] = Path(__file__).read_bytes() == source
    if target is not None:
        record['target_unchanged'] = target_path.read_bytes() == target
    ok = record['actual_execution'] is True and record['completed'] is True and record['exit_code'] == args.expected_exit and record['operator_unchanged'] is True and (target is None or record['target_unchanged'] is True) and 'operator_error' not in record
    record['capture_status'] = 'EXPECTED_ACTUAL_EXIT_COMPLETE' if ok else 'UNEXPECTED_OR_INCOMPLETE_ACTUAL_EXIT'
    write(directory / 'CAPTURE.json', (json.dumps(record, indent=2, sort_keys=True) + '\n').encode())
    for path in directory.iterdir():
        assert path.is_file() and not path.is_symlink()
        os.chmod(path, 0o444)
    print(json.dumps(record, sort_keys=True))
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
