#!/usr/bin/env python3
"""Local nonproduction capture; never writes outside this audit family."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
def digest(b): return hashlib.sha256(b).hexdigest()
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
    name = sys.argv[1]
    source = HERE / sys.argv[2]
    folder = HERE / 'captures' / name
    folder.mkdir()
    src = source.read_bytes()
    operator = pathlib.Path(__file__).read_bytes()
    (folder / 'source_prelaunch.py').write_bytes(src)
    (folder / 'operator_prelaunch.py').write_bytes(operator)
    argv = ['/usr/bin/python3', '-B', str(source)]
    with (folder / 'stdout.bin').open('wb') as out, (folder / 'stderr.bin').open('wb') as err:
        started = utc()
        child = subprocess.Popen(argv, cwd=str(HERE), stdout=out, stderr=err)
        pid = child.pid
        exit_code = child.wait()
        ended = utc()
    stdout = (folder / 'stdout.bin').read_bytes()
    stderr = (folder / 'stderr.bin').read_bytes()
    record = {'schema': 'pr52-independent-jet-child-capture/v1',
              'operator_pid': __import__('os').getpid(), 'child_pid': pid,
              'argv': argv, 'cwd': str(HERE), 'started_utc': started, 'ended_utc': ended,
              'exit_code': exit_code, 'source_sha256': digest(src), 'source_bytes': len(src),
              'source_unchanged_after': source.read_bytes() == src,
              'operator_sha256': digest(operator),
              'stdout_bytes': len(stdout), 'stdout_sha256': digest(stdout),
              'stderr_bytes': len(stderr), 'stderr_sha256': digest(stderr)}
    (folder / 'CAPTURE.json').write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
    print(json.dumps(record, sort_keys=True))
    sys.exit(exit_code)
if __name__ == '__main__': main()
