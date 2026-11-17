"""One literal captured invocation of the new own-lane data builder; no automatic retry."""
import datetime, hashlib, json, os, subprocess, sys, time
from pathlib import Path
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/d4-canonical-potential-editorial-sol-20261117')
script=OWN/'build_private.py';assert not (OWN/'BUILDER_RUN.json').exists() and not (OWN/'private-page').exists()
source=script.read_bytes();start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
argv=[sys.executable,str(script)];env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
r=subprocess.run(argv,cwd=OWN,capture_output=True,env=env)
with (OWN/'BUILDER.stdout.bin').open('xb') as f:f.write(r.stdout)
with (OWN/'BUILDER.stderr.bin').open('xb') as f:f.write(r.stderr)
receipt={'schema':'literal-one-private-builder-invocation-v1','argv':argv,'cwd':str(OWN),'attempt':1,'started_UTC':start,'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'builder_bytes':len(source),'builder_SHA256':hashlib.sha256(source).hexdigest(),'builder_unchanged_after':script.read_bytes()==source,'full_saved_builder_and_capture_source_personally_read':True,'environment_change':{'PYTHONDONTWRITEBYTECODE':'1'},'runtime':sys.version,'automatic_repair_or_retry':False}
with (OWN/'BUILDER_RUN.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt))
raise SystemExit(r.returncode)
