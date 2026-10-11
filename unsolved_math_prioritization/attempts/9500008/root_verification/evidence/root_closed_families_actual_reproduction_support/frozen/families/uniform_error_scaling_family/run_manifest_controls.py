#!/usr/bin/env python3
"""Execute intact and corrupted tiny fixtures without touching the family seal."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import subprocess
import shutil

root = Path(__file__).resolve().parent
fixture = root/'manifest_control_fixtures'
fixture.mkdir(exist_ok=True)
base = fixture/'baseline'
(base/'nested').mkdir(parents=True, exist_ok=True)
(base/'a.txt').write_text('alpha\n')
(base/'nested/b.txt').write_text('bravo\n')
results = []


def run(name, folder, code, build=False):
    command = ['/usr/bin/python3', str(root/'manifest_integrity.py'), '--root', str(folder)]
    if build:
        command.append('--build')
    result = subprocess.run(command, capture_output=True)
    (root/'streams'/('manifest_'+name+'.stdout')).write_bytes(result.stdout)
    (root/'streams'/('manifest_'+name+'.stderr')).write_bytes(result.stderr)
    row = {'name': name, 'command': command, 'exit_code': result.returncode,
           'expected_exit': code, 'observed_expected': result.returncode == code,
           'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
           'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()}
    results.append(row)
    assert row['observed_expected'], row


run('baseline', base, 0, build=True)
for name in ('missing', 'extra', 'same_size', 'unsafe', 'exclude_cheat'):
    d = fixture/name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(base, d)
    manifest = json.loads((d/'artifact_manifest.json').read_text())
    if name == 'missing':
        (d/'nested/b.txt').unlink()
    elif name == 'extra':
        (d/'new.txt').write_text('extra\n')
    elif name == 'same_size':
        (d/'a.txt').write_text('ALPHA\n')
    elif name == 'unsafe':
        manifest['files'][0]['path'] = '../outside.txt'
    elif name == 'exclude_cheat':
        manifest['exclude_trees'].append('nested')
        manifest['files'] = manifest['files'][:1]
    (d/'artifact_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    run(name, d, 1)
out = {'utc': datetime.now(timezone.utc).isoformat(), 'records': results,
       'scope': 'Baseline passes; missing/extra/same-size corruption/unsafe path/arbitrary exclusion rejected by actual verifier'}
(root/'manifest_control_receipts.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
