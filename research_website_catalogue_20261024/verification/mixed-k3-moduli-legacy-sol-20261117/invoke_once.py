"""Literal capture of one fully read passive identity auditor invocation."""
import datetime, hashlib, json, subprocess, sys, time
from pathlib import Path
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mixed-k3-moduli-legacy-sol-20261117')
assert not (OWN/'EXECUTION.json').exists()
raw=(OWN/'audit_identity.py').read_bytes();argv=[sys.executable,'-B',str(OWN/'audit_identity.py')]
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with (OWN/'AUDIT.stdout.txt').open('xb') as out,(OWN/'AUDIT.stderr.txt').open('xb') as err:r=subprocess.run(argv,cwd=OWN,stdout=out,stderr=err,check=False)
record=dict(argv=argv,cwd=str(OWN),started_UTC=started,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,exit_code=r.returncode,stdout_bytes=(OWN/'AUDIT.stdout.txt').stat().st_size,stderr_bytes=(OWN/'AUDIT.stderr.txt').stat().st_size,fully_read_saved_auditor_SHA256=hashlib.sha256(raw).hexdigest(),auditor_bytes=len(raw),auditor_lines=len(raw.splitlines()),personal_full_source_read_before_one_invocation=True,attempt=1)
with (OWN/'EXECUTION.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record));raise SystemExit(r.returncode)
