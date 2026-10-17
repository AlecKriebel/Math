#!/usr/bin/env python3
"""Read-only authenticate all supplied package and explicit external inputs."""
import datetime,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
A=R.parents[1]
F=R/'INPUT_FREEZE.json'
assert hashlib.sha256(F.read_bytes()).hexdigest()=='af36cb683bccbd9d368c6eb617094f8e2955c9dcbdba42640d63f70c1b7ee42b'
f=json.loads(F.read_text()); results=[]
for group in ('files','external_readonly_inputs'):
 for e in f[group]:
  p=Path(e['path']);p=p if p.is_absolute() else A/p
  b=p.read_bytes();s=hashlib.sha256(b).hexdigest()
  results.append({'group':group,'path':e['path'],'bytes':len(b),'sha256':s,'ok':len(b)==e['bytes'] and s==e['sha256']})
out={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_freeze_sha256':hashlib.sha256(F.read_bytes()).hexdigest(),'file_count':len(f['files']),'external_count':len(f['external_readonly_inputs']),'ok':all(x['ok'] for x in results),'results':results}
print(json.dumps(out,indent=2));raise SystemExit(0 if out['ok'] else 1)
