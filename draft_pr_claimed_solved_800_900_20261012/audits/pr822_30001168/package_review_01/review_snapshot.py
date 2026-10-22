#!/usr/bin/env python3
"""Read-only snapshot of exact review inputs; writes only the review receipt."""
from pathlib import Path
import datetime
import hashlib
import json

A = Path(__file__).resolve().parents[1]
R = A / 'package_review_01'
T = A.parents[1] / 'work/pr822_revision_r1'
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
seal = json.loads((A / 'PACKAGE_SEAL_R1.json').read_text())
core = []
for row in seal['core_files']:
    p = A / 'preprint' / row['path']
    b = p.read_bytes()
    got = {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
    got['matches_seal'] = got['bytes'] == row['bytes'] and got['sha256'] == row['sha256']
    core.append(got)
outer = [{'relative_path': p.relative_to(T).as_posix(), 'bytes': p.stat().st_size,
          'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
         for p in sorted(T.rglob('*')) if p.is_file()]
refs = []
for name in ['PACKAGE_SEAL_R1.json', 'LOCAL_PR_ASSEMBLY_R1.json',
             'PREPARED_PR_MAPPING_R1.json', 'SOURCE_MANIFEST.json']:
    p = A / name
    b = p.read_bytes()
    refs.append({'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()})
output = {'timestamp_utc': now, 'core': core, 'bindings': refs,
          'assembly_root': str(T), 'assembly_files': outer}
target = R / ('INPUT_HASHES_AFTER.json' if (R / 'INPUT_HASHES.json').exists() else 'INPUT_HASHES.json')
target.write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps({'timestamp_utc': now, 'core_matches': all(x['matches_seal'] for x in core),
                  'assembly_files': len(outer), 'receipt': target.name}))
