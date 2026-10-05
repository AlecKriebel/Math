"""Small reviewer-only native recorder; no production operator is imported."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat, subprocess
O = Path(__file__).resolve().parent
Q = O / 'native_run_001'
Q.mkdir(exist_ok=False)
sha = lambda b: hashlib.sha256(b).hexdigest()
pin = lambda p: dict(path=str(p), bytes=len(p.read_bytes()), sha256=sha(p.read_bytes()), mode=stat.S_IMODE(p.stat().st_mode))
argv = ['/opt/homebrew/bin/python3', '-E', '-B', str(O / 'review_packet.py')]
spec = dict(argv=argv, cwd=str(O), started_utc=datetime.now(timezone.utc).isoformat(),
            programs=[pin(O / 'review_packet.py'), pin(Path(__file__)), pin(Path(argv[0]).resolve())],
            no_production_command=True)
(Q / 'execution_spec.json').write_text(json.dumps(spec, indent=2) + '\n')
p = subprocess.Popen(argv, cwd=O, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(Q / 'started.json').write_text(json.dumps(dict(**spec, actual_PID=p.pid), indent=2) + '\n')
out, err = p.communicate(timeout=55)
for k, b in [('stdout', out), ('stderr', err)]:
    (Q / (k + '.bin')).write_bytes(b)
receipt = dict(**spec, actual_PID=p.pid, ended_utc=datetime.now(timezone.utc).isoformat(), exit_code=p.returncode,
               stdout_bytes=len(out), stdout_sha256=sha(out), stderr_bytes=len(err), stderr_sha256=sha(err))
(Q / 'execution.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
print(out.decode())
print(err.decode())
raise SystemExit(p.returncode)
