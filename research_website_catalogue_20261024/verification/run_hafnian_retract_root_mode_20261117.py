from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, subprocess, sys, time

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
E = P / 'verification/hafnian-retract-production-root-executions-20261117'
helper = P / 'verification/hafnian-retract-production-prepare-sol-20261117/release_two.py'
mode = sys.argv[1]
assert mode in ('preflight', 'verify-installed', 'install', 'publish')
assert sha256(helper.read_bytes()).hexdigest() == '6a831b55fbd1d49196619e047e6461d36c9171da94f5ede8d45cdd8148d5b734'
out, err, receipt = [E / (mode + suffix) for suffix in ('.stdout.json', '.stderr.bin', '.execution.json')]
assert E.is_dir() and all(not x.exists() for x in (out, err, receipt))
start = datetime.now(timezone.utc).isoformat()
clock = time.monotonic()
result = subprocess.run([sys.executable, str(helper), '--' + mode], cwd=P,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
elapsed = time.monotonic() - clock
out.write_bytes(result.stdout)
err.write_bytes(result.stderr)
data = dict(mode=mode, argv=[sys.executable, str(helper), '--' + mode],
            started_UTC=start, ended_UTC=datetime.now(timezone.utc).isoformat(),
            elapsed_seconds=elapsed, exit_code=result.returncode,
            stdout_bytes=len(result.stdout), stderr_bytes=len(result.stderr),
            stdout_SHA256=sha256(result.stdout).hexdigest(), stderr_SHA256=sha256(result.stderr).hexdigest(),
            helper_SHA256=sha256(helper.read_bytes()).hexdigest(), automatic_retry=False)
receipt.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data))
if result.returncode:
    print(result.stderr.decode(errors='replace')[-1800:])
    raise SystemExit(result.returncode)
parsed = json.loads(result.stdout)
print(json.dumps({key: parsed[key] for key in ('status', 'preflight_SHA256', 'counts', 'commit', 'tree', 'parent', 'transaction') if key in parsed}))
