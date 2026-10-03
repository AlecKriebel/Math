#!/usr/bin/env python3
"""Prelaunch operator for this family's own controls. Preserve full byte streams."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys
base=Path(__file__).resolve().parent
run=base/'independent_controls_run1'
run.mkdir(exist_ok=False)
program=base/'independent_controls.py'
argv=[sys.executable,str(program)]
def utc():return datetime.now(timezone.utc).isoformat()
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
pre={'phase':'prelaunch','utc':utc(),'operator_pid':os.getpid(),'operator_argv':sys.argv,'operator_cwd':os.getcwd(),'child_argv':argv,'child_cwd':str(base),'program_sha256':digest(program),'operator_sha256':digest(Path(__file__))}
(run/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
start=utc()
with (run/'stdout.bin').open('wb') as out,(run/'stderr.bin').open('wb') as err:
    process=subprocess.Popen(argv,cwd=base,stdout=out,stderr=err)
    child_pid=process.pid
    (run/'LAUNCH.json').write_text(json.dumps({'utc':utc(),'child_pid':child_pid,'operator_pid':os.getpid(),'argv':argv,'cwd':str(base)},indent=2)+'\n')
    code=process.wait()
receipt={'started_utc':start,'ended_utc':utc(),'operator_pid':os.getpid(),'child_pid':child_pid,'argv':argv,'cwd':str(base),'exit_code':code,'prelaunch_sha256':digest(run/'PRELAUNCH.json'),'launch_sha256':digest(run/'LAUNCH.json'),'stdout_bytes':(run/'stdout.bin').stat().st_size,'stdout_sha256':digest(run/'stdout.bin'),'stderr_bytes':(run/'stderr.bin').stat().st_size,'stderr_sha256':digest(run/'stderr.bin'),'program_sha256_after':digest(program),'operator_sha256_after':digest(Path(__file__))}
(run/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
sys.exit(code)
