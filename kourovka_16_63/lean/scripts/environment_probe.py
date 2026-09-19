#!/usr/bin/env python3
"""Record actual availability; never infer a successful Lean run from source files."""
import json, platform, shutil, socket, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
result={'platform':platform.platform(),'machine':platform.machine(),'python':sys.version,
        'executables':{},'dns':{},'commands':[],'lean_compiled':False}
for cmd in ['lean','lake','elan','git','g++']:
    result['executables'][cmd]=shutil.which(cmd)
for host in ['github.com','zenodo.org','pypi.org']:
    try: result['dns'][host]={'addresses':sorted({a[4][0] for a in socket.getaddrinfo(host,443)})}
    except OSError as ex: result['dns'][host]={'error':str(ex)}
for cmd in [['lean','--version'],['lake','--version'],['g++','--version']]:
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
        result['commands'].append({'argv':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    except (OSError,subprocess.TimeoutExpired) as ex:
        result['commands'].append({'argv':cmd,'error':str(ex)})
(root/'logs/environment_probe.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
