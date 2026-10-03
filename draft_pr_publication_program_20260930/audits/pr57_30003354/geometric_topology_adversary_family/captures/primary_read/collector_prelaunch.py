"""Own/capture one explicitly named family operator. No ROOT helpers are executed."""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'


def utc(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()


def main():
    tag, name = sys.argv[1:]
    assert tag in ('primary_read', 'geometric_controls', 'handoff_preparation')
    assert name in ('read_primary_sources.py', 'geometric_controls.py', 'prepare_handoff.py')
    capture = ROOT / 'captures' / tag
    capture.mkdir(parents=True, exist_ok=False)
    operator = ROOT / name
    source = operator.read_bytes(); collector = Path(__file__).read_bytes()
    (capture / 'operator_prelaunch.py').write_bytes(source)
    (capture / 'collector_prelaunch.py').write_bytes(collector)
    argv = [PYTHON, str(operator)]; started = utc()
    with (capture / 'stdout.bin').open('wb') as stdout, (capture / 'stderr.bin').open('wb') as stderr:
        child = subprocess.Popen(argv, cwd=ROOT, stdout=stdout, stderr=stderr)
        metadata = {'collector_pid': os.getpid(), 'owned_child_pid': child.pid,
                    'started_utc': started, 'argv': argv, 'cwd': str(ROOT),
                    'operator_sha256_prelaunch': sha(source), 'collector_sha256_prelaunch': sha(collector),
                    'root_helpers_executed': False, 'root_closed': False}
        (capture / 'PRELAUNCH.json').write_text(json.dumps(metadata, indent=2) + '\n')
        code = child.wait()
    metadata.update(ended_utc=utc(), exit_code=code, operator_sha256_after=sha(operator.read_bytes()),
                    collector_sha256_after=sha(Path(__file__).read_bytes()))
    for stream in ('stdout', 'stderr'):
        data = (capture / (stream + '.bin')).read_bytes()
        metadata[stream + '_bytes'] = len(data); metadata[stream + '_sha256'] = sha(data)
    (capture / 'CAPTURE.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, indent=2, sort_keys=True)); print((capture / 'stdout.bin').read_text())
    sys.exit(code)


if __name__ == '__main__': main()
