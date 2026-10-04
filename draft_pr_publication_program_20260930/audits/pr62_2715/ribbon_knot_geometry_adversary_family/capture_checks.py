#!/usr/bin/env python3
"""Capture true child PIDs, UTC, prelaunch code pins and full byte streams."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys

BASE = Path(__file__).resolve().parent
ORIGINAL = BASE.parent/'original_preparation_family'/'original'
def utc(): return datetime.now(timezone.utc).isoformat()
def pin(path):
    st=path.lstat()
    return {"path":str(path),"bytes":st.st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"full_mode_07777":format(st.st_mode&0o7777,'04o'),"nlink":st.st_nlink}

jobs = [
    ('submitted_default',[sys.executable,str(ORIGINAL/'verify.py')],[ORIGINAL/'verify.py',ORIGINAL/'OBSTRUCTION.md']),
    ('independent_default',[sys.executable,str(BASE/'independent_controls.py')],[BASE/'independent_controls.py']),
    ('independent_optimized_refusal',[sys.executable,'-O',str(BASE/'independent_controls.py')],[BASE/'independent_controls.py']),
]
summaries=[]
for name,argv,inputs in jobs:
    dest=BASE/'captures'/name
    dest.mkdir(parents=True,exist_ok=False)
    prelaunch={"utc":utc(),"controller_pid":os.getpid(),"argv":argv,"cwd":str(BASE),"inputs":[pin(p) for p in inputs],"controller":pin(Path(__file__))}
    (dest/'PRELAUNCH.json').write_text(json.dumps(prelaunch,indent=2,sort_keys=True)+'\n')
    started=utc()
    child=subprocess.Popen(argv,cwd=BASE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr=child.communicate()
    ended=utc()
    (dest/'stdout.bin').write_bytes(stdout)
    (dest/'stderr.bin').write_bytes(stderr)
    capture={"schema":"pr62-geometry-actual-capture/v1","name":name,"actual_controller_pid":os.getpid(),"actual_child_pid":child.pid,"started_utc":started,"ended_utc":ended,"exit_code":child.returncode,"argv":argv,"prelaunch":pin(dest/'PRELAUNCH.json'),"stdout":pin(dest/'stdout.bin'),"stderr":pin(dest/'stderr.bin'),"inputs_unchanged":[pin(p)==pre for p,pre in zip(inputs,prelaunch['inputs'])]}
    (dest/'CAPTURE.json').write_text(json.dumps(capture,indent=2,sort_keys=True)+'\n')
    summaries.append(capture)
print(json.dumps({"controller_pid":os.getpid(),"captures":summaries},indent=2,sort_keys=True))
