#!/usr/bin/env python3
"""Validate the exact, self-contained release bytes and recompute controls."""
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True


def main():
    base = Path(__file__).resolve().parent
    manifest = json.loads((base / 'MANIFEST.json').read_text())
    expected = {x['path'] for x in manifest['files']} | {'MANIFEST.json'}
    actual = {p.name for p in base.iterdir() if p.is_file()}
    assert actual == expected, (actual - expected, expected - actual)
    assert not any(p.is_dir() for p in base.iterdir()), 'Unexpected subdirectory'
    for item in manifest['files']:
        data = (base / item['path']).read_bytes()
        assert len(data) == item['bytes'], item['path']
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
    import verify
    current = verify.run()
    retained = json.loads((base / 'verification.json').read_text())
    assert current == retained, 'Computed result differs from retained result'
    print(json.dumps({'result': 'PASS', 'manifest_files': len(manifest['files']),
                      'exact_controls': current['result'],
                      'external_inputs_required': False}, sort_keys=True))


if __name__ == '__main__':
    main()
