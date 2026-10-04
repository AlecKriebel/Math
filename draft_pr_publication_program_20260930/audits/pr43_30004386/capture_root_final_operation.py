"""Capture a genuinely launched ROOT-reviewed audit-local administrative script."""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import traceback

A = Path(__file__).resolve().parent
R = A.parents[2]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('capture_name')
    parser.add_argument('script')
    parser.add_argument('script_sha256')
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0')
    assert args.capture_name and '/' not in args.capture_name and args.capture_name not in ('.', '..')
    script = Path(args.script)
    assert script.is_absolute() and script.is_file() and not script.is_symlink()
    assert script.parent in (A, A / 'acceptance_preparation_family')
    source = script.read_bytes()
    assert sha(source) == args.script_sha256
    dest = A / args.capture_name
    dest.mkdir(mode=0o700)
    (dest / 'PRELAUNCH_SOURCE.py').write_bytes(source)
    (dest / 'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
    records = []
    def git(*tail):
        assert tail in [('branch', '--show-current'), ('rev-parse', 'HEAD')]
        rec = {'argv': ['git', *tail], 'cwd': str(R),
               'started_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
        proc = subprocess.Popen(rec['argv'], cwd=R, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
        out, err = proc.communicate()
        rec.update(pid=proc.pid, actual_execution=True, completed=True,
                   exit_code=proc.returncode, stdout=out.decode(), stderr=err.decode(),
                   finished_utc=dt.datetime.now(dt.timezone.utc).isoformat())
        records.append(rec)
        assert proc.returncode == 0
        return out.decode().strip()
    native_record_raw = (A / 'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes()
    assert sha(native_record_raw) == '5e28953d65bf1490bc6519c55e8c27972b6bcbd788e20280c149bf688b24f011'
    native_record = json.loads(native_record_raw)
    assert native_record['schema'] == 'PR43_ROOT_FRESH13_INPUT_PREIMAGES_v1'
    native_paths = [row['path'] for row in native_record['files']]
    assert len(native_paths) == len(set(native_paths)) == 13
    assert all(type(name) is str for name in native_paths)
    def native():
        rows = []
        for name in native_paths:
            path = R / name
            assert path.is_file() and not path.is_symlink()
            raw = path.read_bytes()
            rows.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
        return rows
    assert git('branch', '--show-current') == 'main'
    before_head, before_files = git('rev-parse', 'HEAD'), native()
    tail = args.arguments[1:] if args.arguments[:1] == ['--'] else args.arguments
    argv = ['/usr/bin/python3', '-B', str(script), *tail]
    rec = {'schema': 'ROOT_actual_audit_administrative_capture_v1', 'argv': argv,
           'cwd': str(A), 'actual_execution': False, 'completed': False, 'pid': None,
           'source_sha256': sha(source), 'stdin_supplied': False,
           'native13_before': before_files, 'main_head_before': before_head,
           'started_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
    out, err = b'', b''
    try:
        proc = subprocess.Popen(argv, cwd=A, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        rec.update(pid=proc.pid, actual_execution=True)
        out, err = proc.communicate()
        rec.update(completed=True, exit_code=proc.returncode)
    except BaseException:
        rec['operator_error'] = traceback.format_exc()
    rec['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    rec.update(source_unchanged=script.read_bytes() == source,
               main_head_after=git('rev-parse', 'HEAD'), native13_after=native())
    for channel, raw in [('stdout', out), ('stderr', err)]:
        name = channel + '.bin'
        with (dest / name).open('xb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        rec[channel] = {'path': name, 'bytes': len(raw), 'sha256': sha(raw)}
    rec['readonly_git_queries'] = records
    good = (rec['completed'] is True and rec.get('exit_code') == 0 and
            rec['source_unchanged'] is True and rec['main_head_after'] == before_head and
            rec['native13_after'] == before_files and 'operator_error' not in rec)
    rec['status'] = 'PASS' if good else 'FAIL'
    with (dest / 'CAPTURE.json').open('x') as f:
        json.dump(rec, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
    print(json.dumps({k:v for k,v in rec.items() if k not in ('native13_before','native13_after','readonly_git_queries')}, indent=2))
    return 0 if good else 1


if __name__ == '__main__':
    sys.exit(main())
