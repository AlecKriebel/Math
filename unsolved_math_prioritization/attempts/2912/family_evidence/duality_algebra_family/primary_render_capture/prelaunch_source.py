#!/usr/bin/env python3
"""Render just the relevant primary pages; image files remain foreign inputs."""
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess
root=Path(__file__).resolve().parent
jobs=[('lomonaco1981',25,27),('hillman_v3',290,292)]
records=[]
for name,first,last in jobs:
    argv=['/opt/homebrew/bin/pdftoppm','-f',str(first),'-l',str(last),'-r','100','-png',
          str(root/'foreign_primary'/(name+'.pdf')),str(root/'foreign_primary'/(name+'_page'))]
    before=datetime.now(timezone.utc).isoformat()
    child=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr=child.communicate()
    after=datetime.now(timezone.utc).isoformat()
    records.append({'argv':argv,'child_pid':child.pid,'before_utc':before,'after_utc':after,
                    'exit_code':child.returncode,'stdout_bytes':len(stdout),
                    'stderr':stderr.decode(errors='replace')})
    (root/'PRIMARY_RENDER.json').write_text(json.dumps(records,indent=2)+'\n')
    if child.returncode: raise RuntimeError('Primary page rendering failed')
print(json.dumps(records,indent=2))
