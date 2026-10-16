import argparse, datetime, hashlib, json, pathlib, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument('label')
p.add_argument('--body')
p.add_argument('argv', nargs=argparse.REMAINDER)
a = p.parse_args()
argv = a.argv[1:] if a.argv and a.argv[0] == '--' else a.argv
root = pathlib.Path(__file__).resolve().parent
out = root / 'native' / a.label
out.mkdir(parents=True, exist_ok=True)
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
body = pathlib.Path(a.body).resolve() if a.body else None
meta = {'argv': argv, 'cwd': str(root), 'started_utc': now(),
        'capture_script_sha256': hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
        'body_path': str(body) if body else None,
        'body_sha256': hashlib.sha256(body.read_bytes()).hexdigest() if body else None}
proc = subprocess.run(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
meta.update(ended_utc=now(), exit_code=proc.returncode,
            stdout_sha256=hashlib.sha256(proc.stdout).hexdigest(),
            stderr_sha256=hashlib.sha256(proc.stderr).hexdigest())
(out / 'stdout.bin').write_bytes(proc.stdout)
(out / 'stderr.bin').write_bytes(proc.stderr)
(out / 'execution.json').write_text(json.dumps(meta, indent=2) + '\n')
print(json.dumps(meta, indent=2))
print('--- FULL STDOUT ---')
sys.stdout.flush()
sys.stdout.buffer.write(proc.stdout)
print('\n--- FULL STDERR ---')
sys.stdout.flush()
sys.stdout.buffer.write(proc.stderr)
sys.exit(proc.returncode)
