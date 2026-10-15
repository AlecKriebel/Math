"""Actual prelaunch-bound capture of our bounded diagnostic only."""
import datetime, hashlib, json, os, pathlib, subprocess, sys
base = pathlib.Path(__file__).resolve().parent
out = base / "controls_actual"
out.mkdir(mode=0o755)
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(b):
    return hashlib.sha256(b).hexdigest()
def put(name, value):
    (out/name).write_text(json.dumps(value, indent=2)+"\n")
source = (base/"controls.py").read_bytes()
operator = pathlib.Path(__file__).read_bytes()
(out/"controls_prelaunch.py").write_bytes(source)
(out/"operator_prelaunch.py").write_bytes(operator)
argv = ["/usr/bin/python3", "-B", str(out/"controls_prelaunch.py")]
pre = {"operator_pid":os.getpid(), "operator_argv":sys.argv,
       "prelaunch_utc":now(), "argv":argv, "cwd":str(base),
       "source_sha256":digest(source), "source_bytes":len(source),
       "operator_sha256":digest(operator), "operator_bytes":len(operator),
       "execution_scope":"our bounded diagnostics; no author/reviewer program or theorem reproduction"}
put("PRELAUNCH.json", pre)
started = now()
child = subprocess.Popen(argv, cwd=str(base), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = child.communicate()
ended = now()
(out/"stdout.bin").write_bytes(stdout)
(out/"stderr.bin").write_bytes(stderr)
put("CAPTURE.json", dict(pre, child_pid=child.pid, started_utc=started,
    ended_utc=ended, exit_code=child.returncode,
    stdout_bytes=len(stdout), stdout_sha256=digest(stdout),
    stderr_bytes=len(stderr), stderr_sha256=digest(stderr),
    execution_source_mode=oct((out/"controls_prelaunch.py").stat().st_mode&0o7777),
    source_after_sha256=digest((out/"controls_prelaunch.py").read_bytes()),
    source_preserved=(out/"controls_prelaunch.py").read_bytes()==source))
print(json.dumps({"operator_pid":os.getpid(), "child_pid":child.pid,
    "started_utc":started, "ended_utc":ended, "exit_code":child.returncode,
    "stdout":stdout.decode(), "stderr":stderr.decode()}, indent=2))
sys.exit(child.returncode)
