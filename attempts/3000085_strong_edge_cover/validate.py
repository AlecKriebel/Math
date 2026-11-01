"""Fail-closed byte inventory and exact normal/optimized replay validation."""
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def fail(message):
    raise RuntimeError(message)

def validate():
    # Preflight every directory entry, including the manifest, before any content read.
    found = set()
    for entry in ROOT.iterdir():
        if not stat.S_ISREG(entry.lstat().st_mode):
            fail('Nonregular entry forbidden: ' + entry.name)
        found.add(entry.name)
    if 'MANIFEST.json' not in found:
        fail('Missing manifest')
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    if set(manifest) != {'schema', 'files'} or manifest['schema'] != 1 or not isinstance(manifest['files'], dict):
        fail('Manifest schema mismatch')
    expected = set(manifest['files']) | {'MANIFEST.json'}
    if found != expected:
        fail('Inventory mismatch')
    for name, info in manifest['files'].items():
        if Path(name).name != name or set(info) != {'bytes', 'sha256'}:
            fail('Manifest entry invalid')
        data = (ROOT / name).read_bytes()
        if type(info['bytes']) is not int or info['bytes'] != len(data) or info['sha256'] != hashlib.sha256(data).hexdigest():
            fail('Payload integrity mismatch: ' + name)
    import runpy
    runpy.run_path(str(ROOT / "transformation_check.py"))["verify"](ROOT)
    for optimized, label in [(False, 'NORMAL'), (True, 'OPTIMIZED')]:
        with tempfile.TemporaryDirectory() as tmp:
            temp = Path(tmp)
            for name in ['regression.py', 'replay_runner.py']:
                shutil.copyfile(ROOT / name, temp / name)
            cmd = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(temp / 'replay_runner.py'), str(temp / 'regression.py')]
            run = subprocess.run(cmd, capture_output=True, cwd=temp, timeout=60)
            if run.returncode != 0:
                fail('Replay failed: ' + label)
            for actual, filename in [(run.stdout, f'REPLAY_{label}.stdout'), (run.stderr, f'REPLAY_{label}.stderr'), ((temp / 'REGRESSION_RESULTS.json').read_bytes(), 'REGRESSION_RESULTS.json')]:
                if actual != (ROOT / filename).read_bytes():
                    fail('Replay output mismatch: ' + filename)
            if run.stdout != (ROOT / 'REGRESSION_RESULTS.json').read_bytes() or run.stderr:
                fail('Regression output contract mismatch')
    print('PASS: exact inventory, hashes, whole-module AST, normal and optimized replay; 65812 families, 64824 covers, 4 finite exceptions.')

if __name__ == '__main__':
    sys.dont_write_bytecode = True
    validate()
