"""Capture the sole private builder attempt literally; stop on any failure."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,time
A=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/binary-gram-locus-editorial-sol-20261117')
assert not (A/'BUILDER_RUN.json').exists()
argv=[sys.executable,str(A/'build_private.py')]
start=datetime.now(timezone.utc).isoformat();t=time.monotonic()
r=subprocess.run(argv,cwd=A,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
elapsed=time.monotonic()-t
(A/'BUILDER.stdout.bin').write_bytes(r.stdout);(A/'BUILDER.stderr.bin').write_bytes(r.stderr)
receipt={'start_UTC':start,'end_UTC':datetime.now(timezone.utc).isoformat(),'argv':argv,'cwd':str(A),
    'elapsed_seconds':elapsed,'exit':r.returncode,'attempts':1,'repairs_retries':0,
    'stdout_bytes':len(r.stdout),'stdout_SHA256':hashlib.sha256(r.stdout).hexdigest(),
    'stderr_bytes':len(r.stderr),'stderr_SHA256':hashlib.sha256(r.stderr).hexdigest(),'scope':'private editorial builder only'}
(A/'BUILDER_RUN.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
if r.returncode:sys.exit(r.returncode)
