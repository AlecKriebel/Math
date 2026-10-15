#!/usr/bin/env python3
"""Verify this shard's authored seal, independently of external source paths."""
from pathlib import Path
import hashlib
import json


def main():
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / 'AUTHORED_SEAL.json').read_text())
    results = []
    for expected in manifest['files']:
        path = here / expected['path']
        if path.parent != here:
            raise AssertionError('Manifest entry is not an immediate authored file')
        data = path.read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest()
        ok = len(data) == expected['bytes'] and actual_hash == expected['sha256']
        results.append({'path': expected['path'], 'passed': ok,
                        'bytes': len(data), 'sha256': actual_hash})
    ok = all(row['passed'] for row in results)
    output = {'status': 'passed' if ok else 'failed',
              'files_checked': len(results), 'files': results,
              'scope': 'Authored shard files only; frozen historical source and manuscript hashes are preserved as records, not compared with a subsequently changed package.'}
    print(json.dumps(output, indent=2, sort_keys=True))
    if not ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
