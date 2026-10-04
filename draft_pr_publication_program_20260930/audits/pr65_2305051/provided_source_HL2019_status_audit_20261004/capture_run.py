#!/usr/bin/env python3
"""Record actual child execution; preserve full streams only in private cache."""
import datetime, hashlib, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
PRIVATE = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/status_family_20261004')
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='microseconds')
def sha(path):
    p = pathlib.Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else {'error': 'file_missing'}

spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
name = spec['name']
cwd = spec.get('cwd', str(ROOT))
started = utc()
p = subprocess.Popen(spec['argv'], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid = p.pid
out, err = p.communicate()
ended = utc()
PRIVATE.mkdir(parents=True, exist_ok=True)
stdout = PRIVATE / (name + '.stdout')
stderr = PRIVATE / (name + '.stderr')
stdout.write_bytes(out)
stderr.write_bytes(err)
receipt = {
    'name': name, 'recorder_pid': os.getpid(), 'child_pid': pid,
    'argv': spec['argv'], 'cwd': cwd, 'started_utc': started,
    'ended_utc': ended, 'exit_code': p.returncode,
    'stdout_private_path': str(stdout), 'stdout_sha256': sha(stdout),
    'stderr_private_path': str(stderr), 'stderr_sha256': sha(stderr),
    'source_sha256': {str(x): sha(x) for x in spec.get('sources', [])},
}
(ROOT / (name + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
if spec.get('emit_stdout', False):
    print(out.decode('utf-8', errors='replace'))
if err:
    print(err.decode('utf-8', errors='replace'), file=sys.stderr)
sys.exit(p.returncode)
