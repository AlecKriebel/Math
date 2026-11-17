#!/usr/bin/env python3
"""One unchanged owned-copy pointwise check, with complete source guards."""
from pathlib import Path
import datetime
import hashlib
import json
import stat
import subprocess
import sys

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parents[1] / 'sources'
PROGRAM = SOURCE / 'published-source/container-001/tree/radial_statistical_counterexample/verification/verify_exact.py'

def snapshot():
    files, directories = [], []
    for path in sorted(SOURCE.rglob('*')):
        kind = path.lstat().st_mode
        rel = path.relative_to(SOURCE).as_posix()
        if stat.S_ISREG(kind):
            data = path.read_bytes()
            files.append({'path': rel, 'bytes': len(data),
                          'SHA256': hashlib.sha256(data).hexdigest(),
                          'mode': oct(stat.S_IMODE(kind))})
        elif stat.S_ISDIR(kind):
            directories.append({'path': rel, 'mode': oct(stat.S_IMODE(kind))})
        else:
            raise RuntimeError('special source object: ' + rel)
    return {'root_mode': oct(stat.S_IMODE(SOURCE.stat().st_mode)),
            'files': files, 'directories': directories}

def save(name, value):
    (OWN / name).write_text(json.dumps(value, indent=2) + '\n')

before = snapshot()
baseline = json.loads((OWN / 'SOURCE_CUSTODY.json').read_text())
if any(before[key] != baseline[key] for key in ('root_mode', 'files', 'directories')):
    raise RuntimeError('source changed since source-only INITIAL')
save('NATIVE_SOURCE_BEFORE.json', before)
route = OWN / 'native-route'
route.mkdir(exist_ok=False)
copy = route / PROGRAM.name
copy.write_bytes(PROGRAM.read_bytes())
copy.chmod(stat.S_IMODE(PROGRAM.stat().st_mode))
command = [sys.executable, '-I', '-B', str(copy)]
invocation = {'started_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'command': command, 'cwd': str(route),
              'source_program': str(PROGRAM), 'source_bytes': PROGRAM.stat().st_size,
              'source_SHA256': hashlib.sha256(PROGRAM.read_bytes()).hexdigest(),
              'copy_byte_identical': copy.read_bytes() == PROGRAM.read_bytes(),
              'entire_actual_code_inputs_expected_safety_read': True,
              'ordinary_native_invocations': 1, 'retry_or_optimized_invocations': 0}
save('NATIVE_INVOCATION.json', invocation)
process = subprocess.run(command, cwd=route, capture_output=True)
(OWN / 'native.stdout.txt').write_bytes(process.stdout)
(OWN / 'native.stderr.txt').write_bytes(process.stderr)
after = snapshot()
save('NATIVE_SOURCE_AFTER.json', after)
receipt = dict(invocation, finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               exit_code=process.returncode, source_unchanged=before == after,
               source_extent={'files': len(after['files']), 'child_directories': len(after['directories'])},
               stdout={'path': 'native.stdout.txt', 'bytes': len(process.stdout),
                       'SHA256': hashlib.sha256(process.stdout).hexdigest()},
               stderr={'path': 'native.stderr.txt', 'bytes': len(process.stderr),
                       'SHA256': hashlib.sha256(process.stderr).hexdigest()})
save('NATIVE_RECEIPT.json', receipt)
print(json.dumps(receipt, indent=2))
raise SystemExit(0 if process.returncode == 0 and before == after else 1)
