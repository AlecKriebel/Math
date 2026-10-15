"""Preparation-only actual subprocess recorder, not a portable theorem program."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
sys.dont_write_bytecode = True
base = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base/'publicfiles/support'))
from safe_output import write_new, json_bytes
label = sys.argv[1]
command = sys.argv[2:]
if not label.replace('_','').isalnum() or not command:
    raise ValueError('Supply a unique simple label and exact argv')
records = base/'private/actual_runs'
records.mkdir(exist_ok=True)
if any((records/(label+suffix)).exists() for suffix in ['.json','.stdout.txt','.stderr.txt']):
    raise ValueError('Never overwrite a previous actual-run record')
start = dt.datetime.now(dt.timezone.utc).isoformat()
tick = time.monotonic()
proc = subprocess.Popen(command, cwd=base, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = proc.communicate()
def sha(data): return hashlib.sha256(data).hexdigest()
r = dict(label=label, command=command, cwd=str(base), pid=proc.pid,
         started_utc=start, finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
         wall_seconds=time.monotonic()-tick, exit_code=proc.returncode,
         stdout_sha256=sha(out), stderr_sha256=sha(err),
         stdout_bytes=len(out), stderr_bytes=len(err),
         input_source_hashes={str(Path(c).relative_to(base)):sha(Path(c).read_bytes())
                             for c in command if Path(c).is_file()
                             and base in Path(c).absolute().parents})
write_new(records/(label+'.stdout.txt'), out)
write_new(records/(label+'.stderr.txt'), err)
write_new(records/(label+'.json'), json_bytes(r))
print(json.dumps(r, indent=2))
if proc.returncode:
    print(err.decode(errors='replace'), file=sys.stderr)
raise SystemExit(proc.returncode)
