from pathlib import Path
import sys, json, subprocess, time, datetime, hashlib
base=Path(__file__).resolve().parent
name=sys.argv[1]
argv=sys.argv[2:]
out=base/"process_evidence"/name
out.mkdir(parents=True,exist_ok=False)
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
t=time.monotonic()
p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd="/Users/alec/Documents/Math")
meta={"argv":argv,"cwd":"/Users/alec/Documents/Math","actual_child_pid":p.pid,"start_utc":start}
(out/"launch.json").write_text(json.dumps(meta,indent=2)+"\n")
stdout,stderr=p.communicate()
(out/"stdout.bin").write_bytes(stdout)
(out/"stderr.bin").write_bytes(stderr)
meta.update({"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"exit_code":p.returncode,"elapsed_seconds":time.monotonic()-t,"stdout_bytes":len(stdout),"stderr_bytes":len(stderr),"stdout_sha256":hashlib.sha256(stdout).hexdigest(),"stderr_sha256":hashlib.sha256(stderr).hexdigest()})
(out/"process.json").write_text(json.dumps(meta,indent=2)+"\n")
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
print("\nCAPTURE_METADATA "+json.dumps(meta),file=sys.stderr)
sys.exit(p.returncode)
