#!/usr/bin/env python3
"""Verify the explicit public artifact whitelist, not any private sources."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
if __name__ == '__main__':
    manifest = json.loads((HERE/'PUBLIC_MANIFEST.json').read_text())
    for item in manifest['public_files']:
        p = HERE/item['path']
        assert p.resolve().is_relative_to(HERE)
        assert 'private_sources' not in p.parts
        assert p.suffix not in {'.pdf', '.png', '.jpg', '.jpeg'}
        b = p.read_bytes()
        assert len(b) == item['bytes'], item['path']
        assert hashlib.sha256(b).hexdigest() == item['sha256'], item['path']
    print(json.dumps({'status': 'pass',
                      'public_artifacts_verified': len(manifest['public_files']),
                      'private_sources_included': False}, indent=2, sort_keys=True))
