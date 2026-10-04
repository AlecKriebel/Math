"""Capture actual subprocess outputs in this namespace. Caller supplies argv."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,sys,re
N=Path(__file__).resolve().parent
tag=sys.argv[1];assert re.fullmatch('[a-z0-9_]+',tag)
R=N/'private_evidence'/tag;R.mkdir(parents=True,exist_ok=False)
argv=sys.argv[2:];assert argv
start=datetime.now(timezone.utc).isoformat();p=subprocess.run(argv,capture_output=True,cwd=N);end=datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
(R/'stdout').write_bytes(p.stdout);(R/'stderr').write_bytes(p.stderr)
r={'kind':'genuine_native_subprocess_execution_receipt','argv':argv,'cwd':str(N),'started_utc':start,'finished_utc':end,'actual_exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
(R/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
if p.stderr:print(p.stderr.decode(errors='replace'),file=sys.stderr)
if p.returncode:sys.exit(p.returncode)
