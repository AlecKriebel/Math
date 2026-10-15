#!/usr/bin/env python3
"""Seal or independently verify every authored file in this bounded audit."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json

ROOT = Path(__file__).resolve().parent
CONTROLS = {'MANIFEST.json', 'MANIFEST_CHECKS.json'}


def inner_files():
    return sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
                  if p.is_file() and '.cache' not in p.relative_to(ROOT).parts
                  and '__pycache__' not in p.relative_to(ROOT).parts)


def record(name):
    data = (ROOT / name).read_bytes()
    return {'path': name, 'bytes': len(data), 'sha256': sha256(data).hexdigest()}


parser = argparse.ArgumentParser()
parser.add_argument('--write', action='store_true', help='Create/refresh the authored manifest before verification.')
args = parser.parse_args()
if args.write:
    names = sorted(set(inner_files()) | CONTROLS)
    manifest = {'schema': 'authored-file-seal-v1', 'created_utc': datetime.now(timezone.utc).isoformat(),
                'all_inner_authored_files': names,
                'files': [record(n) for n in names if n not in CONTROLS],
                'self_referential_controls': sorted(CONTROLS),
                'ignored_raw_directories': ['.cache', '__pycache__'],
                'scope': 'Authored integrity only, including .gitignore; raw copyrighted sources/OCR/renderings are excluded.'}
    (ROOT / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')

manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
actual = sorted(set(inner_files()) | {'MANIFEST_CHECKS.json'})
missing = sorted(set(manifest['all_inner_authored_files']) - set(actual))
extra = sorted(set(actual) - set(manifest['all_inner_authored_files']))
bad = []
for item in manifest['files']:
    path = ROOT / item['path']
    if not path.is_file() or record(item['path']) != item:
        bad.append(item['path'])
checks = {'verified_utc': datetime.now(timezone.utc).isoformat(),
          'passed': not missing and not extra and not bad,
          'missing': missing, 'extra': extra, 'hash_mismatches': bad,
          'hashed_authored_files': len(manifest['files']),
          'all_inner_authored_files': len(manifest['all_inner_authored_files']),
          'gitignore_included': any(i['path'] == '.gitignore' for i in manifest['files']),
          'control_files_present': all((ROOT/n).is_file() for n in CONTROLS if n != 'MANIFEST_CHECKS.json')}
(ROOT / 'MANIFEST_CHECKS.json').write_text(json.dumps(checks, indent=2)+'\n')
checks['control_files_present'] = all((ROOT/n).is_file() for n in CONTROLS)
assert checks['passed'] and checks['gitignore_included'] and checks['control_files_present'], checks
print(json.dumps(checks, indent=2))
