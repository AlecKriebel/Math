"""Capture exactly one explicitly selected helper invocation and retain all streams."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,time
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
O=P/'verification/mink-riesz-k3-root-execution-20261117'
H=P/'verification/mink-riesz-k3-production-prepare-v2-sol-20261117/release_three.py'
assert len(sys.argv)==2 and sys.argv[1] in {'preflight','install','verify-installed','publish'}
m=sys.argv[1];label=m.upper().replace('-','_')
assert hashlib.sha256(H.read_bytes()).hexdigest()=='83c48bca3761c9fbd49d8b29c42a113e10eebfa58b9793bad84c25644b48b3f9'
assert (O/(label+'.authority.json')).is_file()
assert not any((O/(label+s)).exists() for s in ['.stdout.bin','.stderr.bin','.execution.json'])
cmd=['/opt/homebrew/opt/python@3.14/bin/python3.14','-B',str(H),'--'+m]
start=datetime.now(timezone.utc);tick=time.monotonic()
r=subprocess.run(cmd,cwd=P,capture_output=True)
finish=datetime.now(timezone.utc)
for suffix,raw in [('.stdout.bin',r.stdout),('.stderr.bin',r.stderr)]:
 with (O/(label+suffix)).open('xb') as f:f.write(raw)
d={'argv':cmd,'cwd':str(P),'started_UTC':start.isoformat(),'finished_UTC':finish.isoformat(),
 'seconds':time.monotonic()-tick,'exit_code':r.returncode,'attempt':1,
 'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),
 'stdout_SHA256':hashlib.sha256(r.stdout).hexdigest(),'stderr_SHA256':hashlib.sha256(r.stderr).hexdigest()}
with (O/(label+'.execution.json')).open('x') as f:json.dump(d,f,indent=2);f.write('\n')
print(json.dumps(d))
raise SystemExit(r.returncode)
