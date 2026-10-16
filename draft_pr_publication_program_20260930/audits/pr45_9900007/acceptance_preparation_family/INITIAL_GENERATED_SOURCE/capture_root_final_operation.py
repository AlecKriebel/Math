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
    native_paths = [{'path': 'draft_pr_publication_program_20260930/inventory.json', 'bytes': 102519, 'sha256': '7b0943c70b844b309d28043ab4a003e6b19b23627a5d9796cfb00cfcdaa10fe8'}, {'path': 'unsolved_math_prioritization/QUEUE.md', 'bytes': 381277, 'sha256': 'e49757e24fe539df372c40e8f2318d144a59640ee6c26bdaf20cedc906b7d658'}, {'path': 'unsolved_math_prioritization/assessments.json', 'bytes': 19027333, 'sha256': '4abae2bb6bd53eef5e25f29e20813378fa7154473321b3adb627e20eebe64cdb'}, {'path': 'unsolved_math_prioritization/cache/catalog.sqlite', 'bytes': 157691904, 'sha256': 'c02b1c81e0b46f918407ae6d7e46b0ce0130d19e50043e23b8f6ef29f22ab457'}, {'path': 'unsolved_math_prioritization/cache/problems.json', 'bytes': 68931837, 'sha256': '04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'}, {'path': 'unsolved_math_prioritization/cache/research_results.json', 'bytes': 80334822, 'sha256': '8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'}, {'path': 'unsolved_math_prioritization/catalog.json', 'bytes': 21735099, 'sha256': '891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'}, {'path': 'unsolved_math_prioritization/history.jsonl', 'bytes': 82306, 'sha256': '343cef452b7d0c6104e714208a5af8f73d5f02676a4e5d5102787d9606505137'}, {'path': 'unsolved_math_prioritization/manifest.json', 'bytes': 486, 'sha256': '3e025cee22128443584ddc22e095e44600a006699d0d62488793d881e62be208'}, {'path': 'unsolved_math_prioritization/policy.json', 'bytes': 1257, 'sha256': '72f21e70ee41a7e9164b648cf46ac0f282a5f2ed065456816dbcd8dfc95dfac7'}, {'path': 'unsolved_math_prioritization/queue.py', 'bytes': 25994, 'sha256': 'f72aee023f837bad092da58531c2cc069ce2cf094e835d090221107d20f07ab2'}, {'path': 'unsolved_math_prioritization/review_v2/related_target_groups.json', 'bytes': 1146, 'sha256': 'fb32ad69080193e1e9b7feac1f00c739483c0e97a7a6ac9deca188438f1e2cf8'}, {'path': 'unsolved_math_prioritization/state.json', 'bytes': 94347, 'sha256': '1c619e760a420ca952bf0c3a44170972628a6a7995308b2ea431db390d876c35'}]
    native_paths=[z['path'] for z in native_paths]
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
