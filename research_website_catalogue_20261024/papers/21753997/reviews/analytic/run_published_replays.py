from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, time

root = Path(__file__).resolve().parent
release = root / 'replay-work/v2.0'
scripts = [
    'verify_release_metadata.py',
    'source/verify_v2_claims.py',
    'cleanroom/verify_v1_cleanroom.py',
    'minimality/verify_complexity_arithmetic.py',
    'audit_v2/verify_v2_independent.py',
]
results = []
for script in scripts:
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tic = time.monotonic()
    proc = subprocess.run([sys.executable, str(release / script)],
        cwd=release, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'})
    output = script.replace('/', '__') + '.txt'
    (root / output).write_text(proc.stdout)
    results.append(dict(script=script, script_sha256=hashlib.sha256((release/script).read_bytes()).hexdigest(),
        started_at_utc=started, duration_seconds=round(time.monotonic()-tic,3),
        command=[sys.executable, script], exit_code=proc.returncode, output=output,
        output_sha256=hashlib.sha256(proc.stdout.encode()).hexdigest()))
    (root / 'published-replay-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(script, 'exit', proc.returncode, flush=True)
    if proc.returncode:
        raise SystemExit(proc.returncode)
