#!/usr/bin/env python3
"""Private review capture; exclusively creates one named capture directory."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, sys

HERE = Path(__file__).resolve().parent
def now(): return datetime.now(timezone.utc).isoformat()
def binding(p):
    p = Path(p); data = p.read_bytes()
    return {'path': str(p), 'mode': format(stat.S_IMODE(p.stat().st_mode),'04o'),
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
name, *argv = sys.argv[1:]
folder = HERE / name
folder.mkdir(exist_ok=False)
source = Path(argv[2]) if len(argv)>2 and argv[1]=='-B' else None
operator = binding(__file__)
(folder/'prelaunch_operator.py').write_bytes(Path(__file__).read_bytes())
pre = {'argv': argv, 'cwd': str(HERE), 'operator_pid': os.getpid(),
       'prepared_utc': now(), 'operator': operator,
       'source': binding(source) if source else None}
if source: (folder/'prelaunch_source.py').write_bytes(source.read_bytes())
(folder/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
started = now()
with (folder/'stdout.bin').open('xb') as out, (folder/'stderr.bin').open('xb') as err:
    child = subprocess.Popen(argv,cwd=HERE,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
    code = child.wait()
record = {'actual_execution': True, 'completed': True, 'started_utc': started,
          'finished_utc': now(), 'argv': argv, 'cwd': str(HERE),
          'operator_pid': os.getpid(), 'child_pid': child.pid, 'exit_code': code,
          'operator_unchanged': operator == binding(__file__),
          'source_unchanged': pre['source'] == (binding(source) if source else None),
          'stdout': binding(folder/'stdout.bin'), 'stderr': binding(folder/'stderr.bin')}
(folder/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
if code or not record['operator_unchanged'] or not record['source_unchanged']: sys.exit(1)
