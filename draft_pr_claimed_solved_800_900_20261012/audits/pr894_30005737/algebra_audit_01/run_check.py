import sys,subprocess,datetime,hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
n=sys.argv[1];args=sys.argv[2:]
t0=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(args,capture_output=True)
t1=datetime.datetime.now(datetime.timezone.utc).isoformat()
out=r.stdout+r.stderr
p.joinpath("checks",n+".out").write_bytes(out)
m={"check":n,"argv":args,"start_utc":t0,"end_utc":t1,"returncode":r.returncode,"stdout_bytes":len(r.stdout),"stderr_bytes":len(r.stderr),"combined_sha256":hashlib.sha256(out).hexdigest()}
p.joinpath("checks",n+".json").write_text(json.dumps(m,indent=2)+"\n")
print(json.dumps(m));sys.stdout.buffer.write(out)
sys.exit(r.returncode)
