"""Small owned runner; snapshots operator/collector and preserves every full stream."""
import hashlib, json, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
FAMILY = Path(__file__).resolve().parent
PYTHON = '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def main():
    tag, operator_name = sys.argv[1:]
    assert (tag, operator_name) in (('primary_read', 'read_primary_sources.py'),
        ('geometric_controls', 'geometric_controls.py'), ('handoff', 'prepare_handoff.py'))
    folder = FAMILY / 'captures' / tag; folder.mkdir(parents=True, exist_ok=False)
    operator = FAMILY / operator_name
    op = operator.read_bytes(); collector = Path(__file__).read_bytes()
    (folder / 'operator_prelaunch.py').write_bytes(op)
    (folder / 'collector_prelaunch.py').write_bytes(collector)
    started = utc(); argv = [PYTHON, str(operator)]
    with (folder / 'stdout.bin').open('wb') as out, (folder / 'stderr.bin').open('wb') as err:
        child = subprocess.Popen(argv, cwd=FAMILY, stdout=out, stderr=err)
        cap = {'collector_pid': os.getpid(), 'owned_child_pid': child.pid, 'argv': argv,
            'started_utc': started, 'cwd': str(FAMILY), 'operator_prelaunch_sha256': sha(op),
            'collector_prelaunch_sha256': sha(collector), 'ROOT_helpers_executed': False}
        (folder / 'PRELAUNCH.json').write_text(json.dumps(cap, indent=2) + '\n')
        code = child.wait()
    cap.update(ended_utc=utc(), exit_code=code, operator_after_sha256=sha(operator.read_bytes()),
        collector_after_sha256=sha(Path(__file__).read_bytes()))
    for stream in ('stdout', 'stderr'):
        b = (folder / (stream + '.bin')).read_bytes()
        cap[stream + '_bytes'] = len(b); cap[stream + '_sha256'] = sha(b)
    (folder / 'CAPTURE.json').write_text(json.dumps(cap, indent=2) + '\n')
    print(json.dumps(cap, sort_keys=True)); print((folder / 'stdout.bin').read_text())
    sys.exit(code)
if __name__ == '__main__': main()
