#!/usr/bin/env python3
"""Inventory and verify this portable payload using only the standard library."""
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent
FORBIDDEN={'private','private_reading','private_transport','private_upstream','__pycache__','.git'}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory():
    rows=[]
    for path in sorted(BASE.rglob('*')):
        rel=path.relative_to(BASE)
        if path.is_symlink() or set(rel.parts)&FORBIDDEN:
            raise ValueError('Forbidden payload/symlink: '+rel.as_posix())
        if not path.is_file() or rel.as_posix()=='MANIFEST.json':continue
        if path.suffix.lower() in {'.pdf','.html','.htm','.pyc','.png','.jpg','.jpeg'}:
            raise ValueError('Unexpected binary/reading payload: '+rel.as_posix())
        rows.append({'path':rel.as_posix(),'bytes':path.stat().st_size,'sha256':digest(path)})
    return rows

def verify(manifest=None):
    manifest=Path(manifest) if manifest else BASE/'MANIFEST.json'
    data=json.loads(manifest.read_text())
    if data['schema']!='portable-pr210-sha256-v1':raise ValueError('Unknown manifest schema')
    actual=inventory();expected=data['files']
    if actual!=expected:
        a={r['path']:r for r in actual};e={r['path']:r for r in expected}
        bad=[k for k in sorted(set(a)|set(e)) if a.get(k)!=e.get(k)]
        raise ValueError('Integrity/inventory mismatch: '+', '.join(bad))
    return {'file_count':len(actual),'payload_bytes':sum(r['bytes'] for r in actual),'manifest_sha256':digest(manifest)}

if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
