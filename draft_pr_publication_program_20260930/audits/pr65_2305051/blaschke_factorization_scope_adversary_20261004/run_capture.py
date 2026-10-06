from pathlib import Path
import datetime,json,subprocess,sys,hashlib
BASE=Path(__file__).resolve().parent
label=sys.argv[1]
args=sys.argv[2:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run(args,cwd="/Users/alec/Documents/Math",capture_output=True)
out=BASE/"commands"/(label+".stdout")
err=BASE/"commands"/(label+".stderr")
out.write_bytes(p.stdout);err.write_bytes(p.stderr)
record={"label":label,"argv":args,"cwd":"/Users/alec/Documents/Math","started_utc":start,"ended_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"returncode":p.returncode,"stdout_path":str(out.relative_to(BASE)),"stderr_path":str(err.relative_to(BASE)),"stdout_sha256":hashlib.sha256(p.stdout).hexdigest(),"stderr_sha256":hashlib.sha256(p.stderr).hexdigest()}
with (BASE/"ACTUAL_COMMANDS.jsonl").open("a") as f:f.write(json.dumps(record)+"\n")
sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr)
sys.exit(p.returncode)
