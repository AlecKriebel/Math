"""Capture the sole authorized private preparation attempt; preserve literal failures."""
import datetime, hashlib, json, os, subprocess, sys, time
from pathlib import Path

OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mixed-k3-moduli-editorial-sol-20261117')
assert not (OWN/'EXECUTION.json').exists()
source=(OWN/'prepare.py').read_bytes()
argv=[sys.executable,'-B',str(OWN/'prepare.py')]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
t=time.monotonic()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
with (OWN/'PREPARE.stdout.txt').open('xb') as out,(OWN/'PREPARE.stderr.txt').open('xb') as err:
    result=subprocess.run(argv,cwd=OWN,env=env,stdout=out,stderr=err,check=False)
record=dict(schema='one-private-preparation-attempt-v1',argv=argv,cwd=str(OWN),started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,exit_code=result.returncode,stdout_bytes=(OWN/'PREPARE.stdout.txt').stat().st_size,stderr_bytes=(OWN/'PREPARE.stderr.txt').stat().st_size,builder_bytes=len(source),builder_SHA256=hashlib.sha256(source).hexdigest(),builder_lines=len(source.splitlines()),whole_saved_builder_personally_read_before_invocation=True,attempt=1,no_source_or_old_helper_execution=True)
with (OWN/'EXECUTION.json').open('x') as f:
    json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record))
raise SystemExit(result.returncode)
