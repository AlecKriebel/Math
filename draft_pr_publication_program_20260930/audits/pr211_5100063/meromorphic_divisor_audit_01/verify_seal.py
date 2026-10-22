#!/usr/bin/env python3
"""Read-only verification of this authored packet and optional retained primaries."""
from pathlib import Path
import hashlib
import json
import sys

b=Path(__file__).resolve().parent

def pin(p):
    data=p.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

seal=json.loads((b/'EXTERNAL_SEAL.json').read_text())
assert pin(b/'AUTHORED_MANIFEST.json')==seal['manifest_pin']
manifest=json.loads((b/'AUTHORED_MANIFEST.json').read_text())
for row in manifest['files']:
    assert '/' not in row['relative_path'], 'Authored selection must contain root files only'
    assert pin(b/row['relative_path'])=={'bytes':row['bytes'],'sha256':row['sha256']}, row
private_count=0
if '--private' in sys.argv:
    private=json.loads((b/'PRIVATE_PRIMARY_MANIFEST.json').read_text())
    for row in private['files']:
        assert row['relative_path'].startswith('private_primary/')
        assert pin(b/row['relative_path'])=={'bytes':row['bytes'],'sha256':row['sha256']}, row
        private_count+=1
print(json.dumps({'authored_files_verified':len(manifest['files']),
                  'private_primary_files_verified':private_count,
                  'manifest_pin':seal['manifest_pin'],'all_passed':True},indent=2))
