import datetime
import json
import os
import pathlib
import signal
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
process = subprocess.Popen(sys.argv[2:], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           start_new_session=True, cwd=root)
timed_out = False
try:
    stdout, stderr = process.communicate(timeout=45)
except subprocess.TimeoutExpired:
    timed_out = True
    os.killpg(process.pid, signal.SIGTERM)
    try:
        stdout, stderr = process.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate(timeout=2)
try:
    os.killpg(process.pid, 0)
    empty = False
except ProcessLookupError:
    empty = True
record = dict(start_utc=start, end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              argv=sys.argv[2:], pid=process.pid, exit_code=process.returncode,
              timed_out=timed_out, reaped=process.poll() is not None, process_group_empty=empty,
              stdout=stdout.decode(), stderr=stderr.decode())
(root / (sys.argv[1] + '.json')).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
if timed_out or not empty or process.returncode:
    raise SystemExit(1)
