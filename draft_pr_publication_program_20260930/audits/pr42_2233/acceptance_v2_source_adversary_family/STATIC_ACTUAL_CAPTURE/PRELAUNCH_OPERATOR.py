"""Actual capture of this family's own handwritten read-only control only."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
H = Path(__file__).resolve().parent
def sha(raw): return hashlib.sha256(raw).hexdigest()
def stamp(): return dt.datetime.now(dt.timezone.utc).isoformat()
name, source_name = sys.argv[1:]
assert name == 'STATIC_ACTUAL_CAPTURE' and source_name == 'independent_static_controls.py'
source = H / source_name
raw = source.read_bytes()
dest = H / name
dest.mkdir(mode=0o700)
(dest/'PRELAUNCH_SOURCE.py').write_bytes(raw)
(dest/'PRELAUNCH_OPERATOR.py').write_bytes(Path(__file__).read_bytes())
argv = [sys.executable, '-B', str(source)]
start = stamp()
proc = subprocess.Popen(argv, cwd=H, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = proc.communicate()
finish = stamp()
rec = {'schema':'PR42_V2_NEW_ADVERSARY_OWN_ACTUAL_CAPTURE_v1', 'actual_execution':True,
       'completed':True, 'pid':proc.pid, 'parent_pid':os.getpid(), 'argv':argv,
       'cwd':str(H), 'started_utc':start, 'finished_utc':finish,
       'exit_code':proc.returncode, 'stdin_supplied':False, 'source_sha256':sha(raw),
       'source_unchanged':source.read_bytes()==raw,
       'proposed_native_candidate_helpers_imported_compiled_executed':False}
for name, body in [('stdout',out),('stderr',err)]:
    path=name+'.bin'
    with (dest/path).open('xb') as stream:
        stream.write(body);stream.flush();os.fsync(stream.fileno())
    rec[name]={'path':path,'bytes':len(body),'sha256':sha(body)}
rec['status']='PASS' if proc.returncode==0 and rec['source_unchanged'] else 'FAIL'
with (dest/'CAPTURE.json').open('x') as stream:
    json.dump(rec,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
print(json.dumps(rec))
sys.exit(0 if rec['status']=='PASS' else 1)
