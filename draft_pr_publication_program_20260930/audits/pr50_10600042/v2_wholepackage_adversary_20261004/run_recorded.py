#!/usr/bin/env python3
"""Execute one actual argv and preserve byte streams, timing, PID and inputs."""
import datetime, hashlib, json, pathlib, subprocess, sys, time

root = pathlib.Path(__file__).resolve().parent
label, cwd, *argv = sys.argv[1:]
out = root / 'private' / 'commands'
out.mkdir(parents=True, exist_ok=True)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.monotonic()
p = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
ended = datetime.datetime.now(datetime.timezone.utc).isoformat()
(out / (label + '.stdout')).write_bytes(stdout)
(out / (label + '.stderr')).write_bytes(stderr)
receipt = {'label': label, 'argv': argv, 'cwd': cwd, 'pid': p.pid,
           'stdin': {'kind': 'DEVNULL', 'body_bytes': 0},
           'start_utc': started, 'end_utc': ended, 'elapsed_seconds': time.monotonic()-t0,
           'exit_code': p.returncode,
           'stdout_bytes': len(stdout), 'stderr_bytes': len(stderr),
           'stdout_sha256': hashlib.sha256(stdout).hexdigest(),
           'stderr_sha256': hashlib.sha256(stderr).hexdigest()}
(out / (label + '.json')).write_text(json.dumps(receipt, indent=2)+'\n')
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
print('\nEXECUTION_RECEIPT='+json.dumps(receipt))
sys.exit(p.returncode)
