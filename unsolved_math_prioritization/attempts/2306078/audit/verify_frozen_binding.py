#!/usr/bin/env python3
"""Read-only exhaustive verification of the frozen package reviewed here."""
import hashlib
import json
from pathlib import Path
import sys

if len(sys.argv)!=2:
    raise SystemExit('Usage: python verify_frozen_binding.py FROZEN_PACKAGE_DIRECTORY')
root=Path(sys.argv[1])
binding=json.loads(Path(__file__).with_name('FROZEN_BINDING.json').read_text())
all_entries=list(root.rglob('*'))
if any(p.is_symlink() for p in all_entries):
    raise SystemExit('Unexpected symbolic link')
actual={p.relative_to(root).as_posix() for p in all_entries if p.is_file()}
expected={row['path'] for row in binding['files']}
if actual!=expected:
    raise SystemExit('File-set mismatch: '+repr(sorted(actual^expected)))
total=0
for row in binding['files']:
    data=(root/row['path']).read_bytes();total+=len(data)
    if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
        raise SystemExit('File mismatch: '+row['path'])
if total!=binding['total_bytes'] or len(actual)!=binding['file_count']:
    raise SystemExit('Aggregate mismatch')
print(json.dumps({'status':'PASS','files_checked':len(actual),'total_bytes':total,'original_manifest_sha256':next(row['sha256'] for row in binding['files'] if row['path']=='MANIFEST.json')}))
