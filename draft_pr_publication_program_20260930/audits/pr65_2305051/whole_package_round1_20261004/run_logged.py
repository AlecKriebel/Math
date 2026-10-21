from pathlib import Path
from datetime import datetime,timezone
import sys,subprocess,hashlib,json,os
root=Path(__file__).resolve().parent
label=sys.argv[1]
argv=sys.argv[2:]
out=root/"execution"/label
out.mkdir(parents=True,exist_ok=False)
now=lambda:datetime.now(timezone.utc).isoformat()
start=now()
proc=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=root)
spawn=now()
stdout,stderr=proc.communicate()
end=now()
(out/"stdout.bin").write_bytes(stdout)
(out/"stderr.bin").write_bytes(stderr)
r={"argv":argv,"cwd":str(root),"declared_utc":start,"child_pid":proc.pid,"spawn_observed_utc":spawn,"completed_utc":end,"exit_code":proc.returncode,"stdout_bytes":len(stdout),"stderr_bytes":len(stderr),"stdout_sha256":hashlib.sha256(stdout).hexdigest(),"stderr_sha256":hashlib.sha256(stderr).hexdigest()}
(out/"record.json").write_text(json.dumps(r,indent=2)+"\n")
print(json.dumps(r,indent=2))
print(stdout.decode("utf-8",errors="replace"))
print(stderr.decode("utf-8",errors="replace"),file=sys.stderr)
sys.exit(proc.returncode)
