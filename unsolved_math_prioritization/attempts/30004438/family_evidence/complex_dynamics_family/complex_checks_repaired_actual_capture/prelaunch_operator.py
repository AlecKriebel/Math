#!/usr/bin/env python3
"""Capture exact executable source, PID, UTC interval, exit, and full streams."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
script=Path(sys.argv[1]).resolve()
directory=root/sys.argv[2]
directory.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
source=script.read_bytes()
operator=Path(__file__).read_bytes()
(directory/'prelaunch_source.py').write_bytes(source)
(directory/'prelaunch_operator.py').write_bytes(operator)
argv=['/usr/bin/python3','-B',str(script)]
start=utc()
pre={'argv':argv,'cwd':str(root),'operator_pid':os.getpid(),'started_utc':start,
     'source_sha256':sha(source),'operator_sha256':sha(operator),'operator_agent':'/root/pr46_complex_dynamics_adversary'}
(directory/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
with (directory/'stdout.bin').open('wb') as out,(directory/'stderr.bin').open('wb') as err:
    proc=subprocess.Popen(argv,cwd=root,stdout=out,stderr=err)
    pid=proc.pid
    exit_code=proc.wait()
finish=utc()
stdout=(directory/'stdout.bin').read_bytes()
stderr=(directory/'stderr.bin').read_bytes()
receipt={**pre,'actual_pid':pid,'finished_utc':finish,'exit_code':exit_code,
 'complete_streams':True,'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),
 'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),'post_source_sha256':sha(script.read_bytes()),
 'source_unchanged':script.read_bytes()==source}
(directory/'CAPTURE.json').write_text(json.dumps(receipt,indent=2)+'\n')
for file in directory.iterdir():file.chmod(0o444)
print(json.dumps(receipt,indent=2))
sys.exit(exit_code)
