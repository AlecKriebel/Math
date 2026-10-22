"""Verify exact portable payload hashes, including both compressed certificates."""
from pathlib import Path
import hashlib, json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'PUBLIC_MANIFEST.json').read_text())
for name, info in manifest['files'].items():
    data = (root / name).read_bytes()
    if len(data) != info['bytes'] or hashlib.sha256(data).hexdigest() != info['sha256']:
        raise ValueError('payload mismatch: ' + name)
author = json.loads((root / 'FINAL_AUDIT_MANIFEST.json').read_text())
for name, info in author['files'].items():
    data = (root / name).read_bytes()
    if len(data) != info['bytes'] or hashlib.sha256(data).hexdigest() != info['sha256']:
        raise ValueError('frozen author mismatch: ' + name)
print(json.dumps({'public_files_verified': len(manifest['files']),
                  'frozen_author_payloads_verified': len(author['files']),
                  'full_original_solved': False, 'author_turns_used': 5,
                  'verified': True}, indent=2))
