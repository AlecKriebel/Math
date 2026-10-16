#!/usr/bin/env python3
"""Run the small support checker with complete first-party reproducibility evidence.
Creates only ./verification_run next to this script; refuses to overwrite a run.
SPDX-License-Identifier: MIT
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, platform, subprocess, sys

base = Path(__file__).absolute().parent
source = base / 'verify_even_calculus.py'
folder = base / 'verification_run'
folder.mkdir(exist_ok=False)

def stamp(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()
def ref(path):
    data = path.read_bytes()
    return {'path': path.name, 'bytes': len(data), 'sha256': sha(data)}

(folder/'prelaunch_checker.py').write_bytes(source.read_bytes())
(folder/'prelaunch_runner.py').write_bytes(Path(__file__).read_bytes())
argv = [sys.executable, '-B', str(source)]
pre = {'schema':'even-calculus-diagnostic-prelaunch/v1','prepared_utc':stamp(),
       'operator_pid':os.getpid(),'argv':argv,'cwd':str(base),
       'source':ref(source),'operator':ref(Path(__file__)),
       'python':sys.version,'platform':platform.platform()}
(folder/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
started = stamp()
with (folder/'stdout.bin').open('xb') as out, (folder/'stderr.bin').open('xb') as err:
    child = subprocess.Popen(argv,cwd=base,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
    code = child.wait()
finished = stamp()
record = {'schema':'even-calculus-diagnostic-actual-capture/v1','actual_execution':True,
          'completed':True,'operator_pid':os.getpid(),'child_pid':child.pid,
          'argv':argv,'cwd':str(base),'started_utc':started,'finished_utc':finished,
          'exit_code':code,'stdin_supplied':False,'source_unchanged':ref(source)==pre['source'],
          'operator_unchanged':ref(Path(__file__))==pre['operator'],
          'stdout':ref(folder/'stdout.bin'),'stderr':ref(folder/'stderr.bin')}
(folder/'CAPTURE.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
if code != 0 or not record['source_unchanged'] or not record['operator_unchanged']:
    raise SystemExit('Diagnostic run failed or source changed; inspect retained complete streams.')
