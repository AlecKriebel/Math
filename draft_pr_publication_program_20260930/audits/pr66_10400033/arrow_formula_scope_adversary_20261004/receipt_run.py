#!/usr/bin/env python3
"""Execute one argv and save observed custody for this independent audit."""
import datetime, hashlib, json, os, pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent
private = sys.argv[1] == '--private-output'
offset = 2 if private else 1
name = sys.argv[offset]
argv = sys.argv[offset+1:]
if not argv:
    raise SystemExit('expected receipt name and child argv')
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
start = utc()
proc = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid = proc.pid
stdout, stderr = proc.communicate()
end = utc()
folder = root / 'evidence'
folder.mkdir(exist_ok=True)
output_folder = pathlib.Path('/Users/alec/.cache/codex-pr66-arrow-audit-20261004/receipts') if private else folder
output_folder.mkdir(exist_ok=True)
out = output_folder / (name + '.stdout')
err = output_folder / (name + '.stderr')
out.write_bytes(stdout)
err.write_bytes(stderr)
record = {'argv':argv, 'pid':pid, 'cwd':str(root), 'utc_start':start,
          'utc_end':end, 'exit_code':proc.returncode,
          'stdout':{'path':str(out), 'bytes':len(stdout), 'sha256':hashlib.sha256(stdout).hexdigest()},
          'stderr':{'path':str(err), 'bytes':len(stderr), 'sha256':hashlib.sha256(stderr).hexdigest()}}
(folder / (name + '.json')).write_text(json.dumps(record, indent=2)+'\n')
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
raise SystemExit(proc.returncode)
