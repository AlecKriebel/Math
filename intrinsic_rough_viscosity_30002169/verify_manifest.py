"""Validate exact inventory and hashes; this is integrity checking, not authentication."""
import hashlib,json,pathlib

def require(ok,why):
    if not ok:raise RuntimeError(why)
def main():
    root=pathlib.Path(__file__).resolve().parent
    manifest=json.loads((root/'MANIFEST.json').read_text()); expected={}
    for entry in manifest['files']:
        name=entry['path']; rel=pathlib.PurePosixPath(name)
        require(not rel.is_absolute() and '..' not in rel.parts and name not in expected and name!='MANIFEST.json','Invalid manifest path')
        expected[name]=entry
    actual=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'Symlink forbidden')
        if p.is_file() and p.relative_to(root).as_posix()!='MANIFEST.json':actual.add(p.relative_to(root).as_posix())
    require(actual==set(expected),'Inventory mismatch')
    for name,entry in expected.items():
        data=(root/name).read_bytes()
        require(len(data)==entry['bytes'],'Byte-count mismatch: '+name)
        require(hashlib.sha256(data).hexdigest()==entry['sha256'],'SHA-256 mismatch: '+name)
    require(len(expected)==manifest['file_count_excluding_manifest'],'Manifest count mismatch')
    require(sum(e['bytes'] for e in expected.values())==manifest['total_bytes_excluding_manifest'],'Manifest total mismatch')
    provenance=json.loads((root/'PROVENANCE.json').read_text())
    for entry in provenance['copies']:
        require(expected[entry['file']]['sha256']==entry['package_sha256'],'Frozen provenance mismatch')
    print(json.dumps({'status':'PASS','verified_files':len(expected),'verified_bytes':manifest['total_bytes_excluding_manifest']},indent=2))
if __name__=='__main__':main()
