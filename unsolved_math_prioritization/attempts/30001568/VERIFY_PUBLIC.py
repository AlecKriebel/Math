#!/usr/bin/env python3
"""Portable byte-integrity verification; this is not proof verification."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parent
def verify():
    manifest=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
    for relative,meta in manifest['files'].items():
        data=(ROOT/relative).read_bytes()
        assert len(data)==meta['bytes'],relative
        assert hashlib.sha256(data).hexdigest()==meta['sha256'],relative
    projection=json.loads((ROOT/'PUBLIC_PROJECTION.json').read_text())
    for meta in projection['byte_identical_public_files']:
        data=(ROOT/meta['public_path']).read_bytes()
        assert len(data)==meta['bytes'] and hashlib.sha256(data).hexdigest()==meta['sha256'],meta['public_path']
    return {'public_files_verified':len(manifest['files']),'byte_identical_projected_files':len(projection['byte_identical_public_files']),'mathematics_verified_by_this_script':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
