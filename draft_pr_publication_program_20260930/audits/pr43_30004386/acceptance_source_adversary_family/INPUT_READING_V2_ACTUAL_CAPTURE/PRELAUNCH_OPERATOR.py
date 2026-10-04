"""Actual capture of independent authored review programs, never proposed code."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

H = Path(__file__).resolve().parent
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(x): return hashlib.sha256(x).hexdigest()
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0')
    name, script = sys.argv[1:3]
    assert name and '/' not in name and name not in ('.', '..')
    p = Path(script)
    assert p.parent == H and p.is_file() and not p.is_symlink()
    source = p.read_bytes()
    d = H / name
    d.mkdir(mode=0o700)
    (d/'PRELAUNCH_SOURCE.py').write_bytes(source)
    (d/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
    argv = ['/usr/bin/python3', '-B', str(p), *sys.argv[3:]]
    record = {'schema':'PR43_NEW_ACCEPTANCE_SOURCE_ADVERSARY_ACTUAL_CAPTURE_v1',
              'argv':argv,'cwd':str(H),'started_utc':now(),'actual_execution':False,
              'completed':False,'pid':None,'prelaunch_source_sha256':sha(source),
              'stdin_supplied':False,'proposed_code_executed':False}
    proc = subprocess.Popen(argv, cwd=H, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env=dict(os.environ, PYTHONOPTIMIZE='0', PYTHONDONTWRITEBYTECODE='1'))
    record.update(actual_execution=True, pid=proc.pid)
    out, err = proc.communicate()
    record.update(completed=True,exit_code=proc.returncode,finished_utc=now(),
                  source_unchanged=p.read_bytes()==source)
    for channel, raw in [('stdout',out),('stderr',err)]:
        with (d/(channel+'.bin')).open('xb') as f:
            f.write(raw);f.flush();os.fsync(f.fileno())
        record[channel]={'path':channel+'.bin','bytes':len(raw),'sha256':sha(raw)}
    with (d/'CAPTURE.json').open('x') as f:
        json.dump(record,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(record,indent=2))
    return proc.returncode
if __name__=='__main__':sys.exit(main())
