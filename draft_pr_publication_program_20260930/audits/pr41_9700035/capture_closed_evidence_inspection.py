"""Root actual inspection launch; preserve all actual child evidence."""
import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path

A = Path(__file__).resolve().parent
O = A/'root_closed_evidence_inspection_actual_capture'
O.mkdir(exist_ok=False)
source = A/'inspect_closed_evidence.py'
raw = source.read_bytes()
(O/'prelaunch_source.py').write_bytes(raw)
argv = ['/usr/bin/python3','-B',str(source)]
row = dict(argv=argv,cwd=str(A),source_sha256=hashlib.sha256(raw).hexdigest(),
           started_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
           stdin_supplied=False,actual_execution=False,completed=False)
child = None; out = err = b''
try:
    child = subprocess.Popen(argv,cwd=A,stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    row.update(pid=child.pid,actual_execution=True)
    try:
        out,err = child.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        child.kill(); out,err = child.communicate(); row['timed_out'] = True
    row.update(completed=True,exit_code=child.returncode)
except OSError as error:
    row.update(pid=None,exit_code=None,launch_error=str(error))
finally:
    row['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    for channel,b in [('stdout',out),('stderr',err)]:
        p = O/(channel+'.bin'); p.write_bytes(b)
        row[channel] = dict(path=p.name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    row['status'] = 'PASS' if row.get('exit_code') == 0 and not row.get('timed_out') else 'FAIL'
    (O/'CAPTURE.json').write_text(json.dumps(row,indent=2)+'\n')
assert row['status'] == 'PASS' and source.read_bytes() == raw
assert json.loads(out)['status'] == 'PASS'
print(json.dumps(row))
