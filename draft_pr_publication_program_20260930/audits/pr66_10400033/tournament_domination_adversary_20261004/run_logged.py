#!/usr/bin/env python3
"""Execute one child command and preserve exact bounded execution receipts."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--name', required=True)
p.add_argument('--cwd', default=str(root))
p.add_argument('--timeout', type=float, default=120)
p.add_argument('argv', nargs=argparse.REMAINDER)
a = p.parse_args()
if a.argv and a.argv[0] == '--':
    a.argv = a.argv[1:]
if not a.argv:
    p.error('child argv required')
receipts = root / 'commands'
receipts.mkdir(exist_ok=True)
utc = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
start = utc()
child = subprocess.Popen(a.argv, cwd=a.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
timed_out = False
try:
    stdout, stderr = child.communicate(timeout=a.timeout)
except subprocess.TimeoutExpired:
    timed_out = True
    child.kill()
    stdout, stderr = child.communicate()
end = utc()
for key, b in [('stdout', stdout), ('stderr', stderr)]:
    (receipts / (a.name + '.' + key)).write_bytes(b)
r = {'name':a.name, 'argv':a.argv, 'pid':child.pid, 'cwd':a.cwd,
     'start_utc':start, 'end_utc':end, 'exit':child.returncode,
     'timed_out':timed_out, 'stdout_path':'commands/'+a.name+'.stdout',
     'stderr_path':'commands/'+a.name+'.stderr',
     'stdout_bytes':len(stdout), 'stderr_bytes':len(stderr),
     'stdout_sha256':hashlib.sha256(stdout).hexdigest(),
     'stderr_sha256':hashlib.sha256(stderr).hexdigest()}
with (root/'ACTUAL_COMMANDS.jsonl').open('a') as f:
    f.write(json.dumps(r, sort_keys=True)+'\n')
print(json.dumps(r, sort_keys=True))
sys.stdout.flush()
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
sys.exit(child.returncode)
