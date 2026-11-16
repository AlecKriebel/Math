"""One ordinary unchanged native route; custody and literal process capture only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
import subprocess
import sys
import time

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'papers/23174156/sources'
O = P / 'papers/23174156/reviews/adversarial-sol'
R = O / 'native-run'
PROGRAM = S / 'published-source/container-001/tree/verification/verify.py'
MANUSCRIPT = PROGRAM.parent.parent / 'pr95_note.tex'
EXPECTED_MANIFEST = 'fdff8a4219c2b4b72f7395079fab6945ab2736784c712a359015c08ff40a35dc'
EXPECTED_FINAL = '153bc99484999f9e5bca8623ee88e9935cf2c42557626112161f8f372a5a4827'

def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data),
            'SHA256': hashlib.sha256(data).hexdigest(),
            'mode': oct(stat.S_IMODE(path.stat().st_mode))}

def guard():
    m = pin(S / 'SOURCE_MANIFEST.json')
    f = pin(S / 'SOURCE_FINAL.json')
    if m['SHA256'] != EXPECTED_MANIFEST or f['SHA256'] != EXPECTED_FINAL:
        raise RuntimeError('Source terminal controls differ')
    manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_text())
    expected = {x['path']: x for x in manifest['files']}
    expected['SOURCE_MANIFEST.json'] = m
    expected['SOURCE_FINAL.json'] = f
    actual_files = sorted(str(x.relative_to(S)) for x in S.rglob('*') if x.is_file())
    actual_dirs = sorted(str(x.relative_to(S)) for x in S.rglob('*') if x.is_dir())
    if actual_files != sorted(expected):
        raise RuntimeError('Source file extent differs')
    if actual_dirs != sorted(x['path'] for x in manifest['directories']):
        raise RuntimeError('Source directory extent differs')
    for rel, item in expected.items():
        path = S / rel
        if path.is_symlink() or not path.is_file():
            raise RuntimeError('Unexpected source node: ' + rel)
        p = pin(path)
        if any(p[k] != item[k] for k in ['bytes', 'SHA256', 'mode']):
            raise RuntimeError('Source bytes/mode differ: ' + rel)
    for item in manifest['directories']:
        path = S / item['path']
        if path.is_symlink() or oct(stat.S_IMODE(path.stat().st_mode)) != item['mode']:
            raise RuntimeError('Source directory mode differs: ' + item['path'])
    return {'files': len(actual_files), 'child_directories': len(actual_dirs),
            'manifest': m, 'final': f, 'all_bytes_modes_and_extent_match': True}

if R.exists():
    raise RuntimeError('Refusing a second native invocation or nonempty run namespace')
before = guard()
program_pin, input_pin = pin(PROGRAM), pin(MANUSCRIPT)
R.mkdir()
argv = [sys.executable, str(PROGRAM)]
start = datetime.now(timezone.utc).isoformat()
t0 = time.monotonic()
with (R / 'stdout.txt').open('wb') as out, (R / 'stderr.txt').open('wb') as err:
    proc = subprocess.run(argv, cwd=R, stdout=out, stderr=err, check=False)
elapsed = time.monotonic() - t0
after = guard()
receipt = {'schema': 'single-ordinary-native-receipt-v1', 'UTC_start': start,
           'UTC_end': datetime.now(timezone.utc).isoformat(), 'argv': argv,
           'cwd': str(R), 'exit_code': proc.returncode, 'elapsed_seconds': elapsed,
           'python_version': sys.version, 'environment': 'inherited existing environment unchanged',
           'optimized_or_false_target_or_runner': False,
           'program': program_pin, 'only_local_input': input_pin,
           'source_guard_before': before, 'source_guard_after': after,
           'streams': [pin(R / 'stdout.txt'), pin(R / 'stderr.txt')],
           'artifacts': [pin(x) for x in sorted(R.iterdir()) if x.name not in ['stdout.txt', 'stderr.txt']],
           'finite_diagnostic_not_universal_proof': True}
(R / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'exit_code': proc.returncode, 'elapsed_seconds': elapsed,
                  'source_files_unchanged': after['files'], 'receipt': pin(R / 'RECEIPT.json')}))
