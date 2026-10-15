#!/usr/bin/env python3
import datetime,hashlib,json,platform,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
label,cwd=sys.argv[1:3]
command=sys.argv[3:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(command,cwd=cwd,capture_output=True)
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
(HERE/'journals').mkdir(exist_ok=True)
outputs={}
for kind,data in [('stdout',r.stdout),('stderr',r.stderr)]:
 p=HERE/'journals'/f'{label}.{kind}.txt';p.write_bytes(data)
 outputs[kind]={'relative_path':str(p.relative_to(HERE)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
record={'label':label,'command':command,'cwd':str(Path(cwd).resolve()),'started_utc':start,'completed_utc':end,
        'returncode':r.returncode,'outputs':outputs,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'environment':{'python_executable':sys.executable,'python_version':sys.version,'platform':platform.platform()}}
(HERE/'journals'/f'{label}.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,sort_keys=True))
