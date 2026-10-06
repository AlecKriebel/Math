"""Run an argv vector and retain genuine subprocess custody, including failures."""
import datetime, hashlib, json, os, pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent
label = sys.argv[1]
argv = sys.argv[2:]
if not argv or not label.replace('_','').replace('-','').isalnum():
    raise SystemExit('usage: run_capture.py LABEL executable [arguments]')
out = root / 'process_evidence' / label
out.mkdir(parents=True, exist_ok=False)
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
start = utc()
record = dict(recorder_pid=os.getpid(), argv=argv, cwd=os.getcwd(), started_utc=start,
              recorder_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
              optimization_flags=[], provenance='PID from subprocess.Popen, bytes from communicate')
try:
    proc = subprocess.Popen(argv, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    record['actual_child_pid'] = proc.pid
    stdout, stderr = proc.communicate()
    record['exit_code'] = proc.returncode
except OSError as exc:
    record.update(actual_child_pid=None, exit_code=None, spawn_error=repr(exc))
    stdout, stderr = b'', repr(exc).encode()
record['finished_utc'] = utc()
for name, data in [('stdout.bin',stdout),('stderr.bin',stderr)]:
    (out/name).write_bytes(data)
    record[name] = {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(out/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
print(json.dumps({'capture':str(out),'actual_child_pid':record['actual_child_pid'],'exit_code':record['exit_code']}))
raise SystemExit(record['exit_code'] if record['exit_code'] is not None else 127)
