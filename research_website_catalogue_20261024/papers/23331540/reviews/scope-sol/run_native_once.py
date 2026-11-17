#!/usr/bin/env python3
"""Single owned-copy invocation with exact source guards and literal streams."""
from pathlib import Path
import datetime
import hashlib
import json
import stat
import subprocess
import sys

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parents[1] / 'sources'
NATIVE = SOURCE / 'published-source/container-001/tree/full_stress_stratifications_v1/checks/check_collision_witness.py'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def snapshot():
    files, directories = [], []
    for path in sorted(SOURCE.rglob('*')):
        mode = path.lstat().st_mode
        rel = path.relative_to(SOURCE).as_posix()
        if stat.S_ISREG(mode):
            body = path.read_bytes()
            files.append({'path': rel, 'bytes': len(body),
                          'SHA256': hashlib.sha256(body).hexdigest(),
                          'mode': oct(stat.S_IMODE(mode))})
        elif stat.S_ISDIR(mode):
            directories.append({'path': rel, 'mode': oct(stat.S_IMODE(mode))})
        else:
            raise RuntimeError('special source object: ' + rel)
    return {'root_mode': oct(stat.S_IMODE(SOURCE.stat().st_mode)),
            'files': files, 'directories': directories}

def write_json(name, value):
    (OWN / name).write_text(json.dumps(value, indent=2) + '\n')

before = snapshot()
baseline = json.loads((OWN / 'SOURCE_CUSTODY.json').read_text())
if any(before[key] != baseline[key] for key in ('root_mode', 'files', 'directories')):
    raise RuntimeError('source differs from source-only custody')
write_json('NATIVE_SOURCE_BEFORE.json', before)
route = OWN / 'native-route'
route.mkdir(exist_ok=False)
script = route / NATIVE.name
script.write_bytes(NATIVE.read_bytes())
script.chmod(stat.S_IMODE(NATIVE.stat().st_mode))
command = [sys.executable, '-I', '-B', str(script)]
invocation = {'started_UTC': utc(), 'command': command, 'cwd': str(route),
              'source_script': str(NATIVE), 'source_script_bytes': NATIVE.stat().st_size,
              'source_script_SHA256': hashlib.sha256(NATIVE.read_bytes()).hexdigest(),
              'relocated_copy_byte_identical': script.read_bytes() == NATIVE.read_bytes(),
              'entire_source_body_inputs_expected_safety_personally_read': True,
              'ordinary_native_invocations': 1, 'optimized_or_retry_invocations': 0}
write_json('NATIVE_INVOCATION.json', invocation)
result = subprocess.run(command, cwd=route, capture_output=True)
(OWN / 'native.stdout.json').write_bytes(result.stdout)
(OWN / 'native.stderr.txt').write_bytes(result.stderr)
after = snapshot()
write_json('NATIVE_SOURCE_AFTER.json', after)
receipt = dict(invocation, finished_UTC=utc(), exit_code=result.returncode,
               stdout={'path': 'native.stdout.json', 'bytes': len(result.stdout),
                       'SHA256': hashlib.sha256(result.stdout).hexdigest()},
               stderr={'path': 'native.stderr.txt', 'bytes': len(result.stderr),
                       'SHA256': hashlib.sha256(result.stderr).hexdigest()},
               source_unchanged=before == after,
               source_extent={'files': len(after['files']), 'child_directories': len(after['directories'])})
write_json('NATIVE_RECEIPT.json', receipt)
print(json.dumps(receipt, indent=2))
raise SystemExit(0 if result.returncode == 0 and before == after else 1)
