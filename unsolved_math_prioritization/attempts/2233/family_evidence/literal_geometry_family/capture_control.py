"""Own audit control: capture a child command, its PID, times and unabridged streams."""
import datetime, hashlib, json, pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

name, *command = sys.argv[1:]
directory = ROOT / "controls"
directory.mkdir(exist_ok=True)
started = utc()
clock = time.monotonic()
process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()
(directory / (name + ".stdout.txt")).write_bytes(out)
(directory / (name + ".stderr.txt")).write_bytes(err)
metadata = {"control_name":name,"controller_pid":__import__('os').getpid(),"child_pid":process.pid,
            "command":command,"cwd":str(ROOT),"started_utc":started,"finished_utc":utc(),
            "elapsed_seconds":time.monotonic()-clock,"exit_code":process.returncode,
            "stdout_sha256":hashlib.sha256(out).hexdigest(),"stderr_sha256":hashlib.sha256(err).hexdigest(),
            "controller_sha256":hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
if len(command)>1 and pathlib.Path(command[1]).is_file():
    metadata['child_source_sha256']=hashlib.sha256(pathlib.Path(command[1]).read_bytes()).hexdigest()
(directory / (name + ".metadata.json")).write_text(json.dumps(metadata,indent=2)+"\n")
print(json.dumps(metadata,indent=2))
print(out.decode(errors="replace"))
print(err.decode(errors="replace"),file=sys.stderr)
sys.exit(process.returncode)
