#!/usr/bin/env python3
"""Capture real launches, unabridged streams, and source custody in this effort."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

here=Path(__file__).resolve().parent
source=here/'independent_checks.py'
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
commands=[('ordinary',[sys.executable,'-B',str(source)],0),
          ('negative',[sys.executable,'-B',str(source),'--negative-control'],1),
          ('optimized',[sys.executable,'-B','-O',str(source)],1),
          ('double_optimized',[sys.executable,'-B','-OO',str(source)],1)]
for name,argv,expected in commands:
    folder=here/(name+'_actual_capture');folder.mkdir(exist_ok=True)
    before=source.read_bytes();sha=hashlib.sha256(before).hexdigest()
    (folder/'PRELAUNCH_SOURCE.py').write_bytes(before)
    start=stamp();p=subprocess.Popen(argv,cwd=here,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    (folder/'stdout.bin').write_bytes(out);(folder/'stderr.bin').write_bytes(err)
    record={'argv':argv,'cwd':str(here),'launcher_pid':os.getpid(),'actual_child_pid':p.pid,'start_utc':start,'end_utc':stamp(),'exit_code':p.returncode,'expected_exit_code':expected,'before_sha256':sha,'after_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest(),'stdout_bytes':len(out),'stderr_bytes':len(err)}
    (folder/'CAPTURE.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    if p.returncode!=expected or record['before_sha256']!=record['after_sha256']:
        raise RuntimeError('Unexpected control outcome: '+name)
    print(name+': expected exit '+str(p.returncode)+'; PID '+str(p.pid)+'; streams retained')
