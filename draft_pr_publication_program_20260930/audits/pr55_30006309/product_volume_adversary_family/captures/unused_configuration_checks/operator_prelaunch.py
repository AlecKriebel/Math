"""Capture only this family's exact named command, inputs and prelaunch sources."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/alec/Documents/Math')

def row(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
            'mode': oct(p.stat().st_mode & 0o777)}

def main():
    name, script = sys.argv[1:]
    assert name in ('independent_product_controls', 'primary_source_checks', 'in_depth_negative_controls', 'independent_custody_checks', 'unused_configuration_checks')
    p = (HERE / script).resolve()
    assert p.parent == HERE and p.is_file() and not p.is_symlink()
    dest = HERE / 'captures' / name
    dest.mkdir(parents=True, exist_ok=False)
    (dest / 'operator_prelaunch.py').write_bytes(Path(__file__).read_bytes())
    (dest / 'source_prelaunch.py').write_bytes(p.read_bytes())
    inp = {'script': row(p), 'input': 'Deterministic literals in this captured source; network primary retrieval only when primary_source_checks is named.',
           'stdin': 'DEVNULL', 'expected_exit_code': 0}
    (dest / 'INPUT.json').write_text(json.dumps(inp, indent=2) + '\n')
    argv = ['/usr/bin/python3', '-B', str(p)]
    rec = {'schema': 'independent-adversary-command-capture/v1', 'argv': argv,
           'cwd': str(ROOT), 'started_utc': datetime.now(timezone.utc).isoformat(),
           'actual_execution': False, 'pid': None, 'completed': False, 'exit_code': None,
           'source_prelaunch': row(dest / 'source_prelaunch.py'),
           'operator_prelaunch': row(dest / 'operator_prelaunch.py'), 'input_prelaunch': row(dest / 'INPUT.json')}
    child = subprocess.Popen(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rec.update(actual_execution=True, pid=child.pid)
    out, err = child.communicate()
    rec.update(completed=True, exit_code=child.returncode, finished_utc=datetime.now(timezone.utc).isoformat())
    for fname, b in (('stdout.bin', out), ('stderr.bin', err)):
        with (dest / fname).open('xb') as f:
            f.write(b); f.flush(); os.fsync(f.fileno())
        rec[fname[:-4]] = row(dest / fname)
    rec['source_unchanged'] = p.read_bytes() == (dest / 'source_prelaunch.py').read_bytes()
    rec['operator_unchanged'] = Path(__file__).read_bytes() == (dest / 'operator_prelaunch.py').read_bytes()
    rec['status'] = 'PASS' if child.returncode == 0 and rec['source_unchanged'] and rec['operator_unchanged'] else 'FAIL'
    (dest / 'CAPTURE.json').write_text(json.dumps(rec, indent=2) + '\n')
    print(json.dumps(rec, sort_keys=True))
    return 0 if rec['status'] == 'PASS' else 1

if __name__ == '__main__':
    sys.exit(main())
