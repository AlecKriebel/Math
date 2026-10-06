#!/usr/bin/python3
"""Strict closed coverage. Exclude only this manifest itself and tmp/ foreign/raw scratch."""
import pathlib,json,hashlib,sys
root=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
manifest=root/'authored_manifest.json'
try:
    data=json.loads(manifest.read_text())
    assert data['excluded']==['authored_manifest.json','tmp/'],'exclusion_policy'
    entries=data['files'];listed=[]
    for entry in entries:
        name=entry['path'];p=pathlib.PurePosixPath(name)
        assert name and not p.is_absolute() and '..' not in p.parts and str(p)==name,'unsafe_path'
        assert name!='authored_manifest.json' and p.parts[0]!='tmp','excluded_path_listed'
        assert name not in listed,'duplicate_path'
        listed.append(name)
        target=root/name
        assert target.is_file() and not target.is_symlink(),'missing_or_nonregular_file'
        content=target.read_bytes()
        assert len(content)==entry['bytes'],'size_mismatch'
        assert hashlib.sha256(content).hexdigest()==entry['sha256'],'hash_mismatch'
    actual=[]
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix()
        if rel=='authored_manifest.json' or rel.startswith('tmp/'):continue
        assert not p.is_symlink(),'symlink_not_allowed'
        if p.is_file():actual.append(rel)
    assert sorted(actual)==sorted(listed),'closed_coverage_mismatch'
    print('PASS: exact closed coverage, hashes and sizes.')
except Exception as e:
    print('FAIL: '+str(e),file=sys.stderr)
    sys.exit(1)
