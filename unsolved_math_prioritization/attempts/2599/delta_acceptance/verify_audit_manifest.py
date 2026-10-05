#!/usr/bin/env python3
"""Strict audit payload allowlist and file integrity verifier."""
import hashlib,json,pathlib,sys

def verify(root):
    root=pathlib.Path(root).resolve()
    manifest_path=root/'AUDIT_MANIFEST.json'
    assert manifest_path.is_file() and not manifest_path.is_symlink()
    manifest=json.loads(manifest_path.read_text())
    names=set()
    for record in manifest['files']:
        name=record['name']
        assert name not in names and pathlib.PurePosixPath(name).name==name
        names.add(name)
        p=root/name
        assert p.is_file() and not p.is_symlink()
        data=p.read_bytes()
        assert len(data)==record['bytes'],name
        assert hashlib.sha256(data).hexdigest()==record['sha256'],name
    assert {p.name for p in root.iterdir()}==names|{'AUDIT_MANIFEST.json'}
    return {'status':'PASS','files':len(names)+1,'source_material_excluded':True}

if __name__=='__main__':
    print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else pathlib.Path(__file__).parent),sort_keys=True))
