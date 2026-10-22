"""Strict recursive inventory verification. The manifest hash is externally pinned."""
import hashlib,json,os
from pathlib import Path,PurePosixPath

def require(ok,message):
    if not ok:raise RuntimeError(message)

def verify(root):
    root=Path(root)
    require(not root.is_symlink(),'root symlink')
    manifest=root/'MANIFEST.json'
    require(manifest.is_file() and not manifest.is_symlink(),'manifest type')
    data=json.loads(manifest.read_text())
    require(set(data)=={'schema','files'} and data['schema']==1,'manifest schema')
    expected={}; dirs=set()
    for row in data['files']:
        require(set(row)=={'path','bytes','sha256'},'entry schema')
        name=row['path']; p=PurePosixPath(name)
        require(isinstance(name,str) and name and not p.is_absolute() and str(p)==name and '\\' not in name and all(x not in ('','..','.') for x in name.split('/')),'unsafe path')
        require(p.name!='MANIFEST.json','nested or self manifest')
        require(name not in expected,'duplicate entry')
        require(type(row['bytes']) is int and row['bytes']>=0,'byte count')
        require(isinstance(row['sha256'],str) and len(row['sha256'])==64 and all(c in '0123456789abcdef' for c in row['sha256']),'hash format')
        expected[name]=row
        dirs.update(str(x) for x in p.parents if str(x)!='.')
    found=set(); found_dirs=set()
    for base,ds,fs in os.walk(root,followlinks=False):
        for name in ds+fs:
            p=Path(base)/name; rel=p.relative_to(root).as_posix()
            require(not p.is_symlink(),'symlink '+rel)
            if p.is_dir():found_dirs.add(rel);continue
            require(p.is_file(),'nonregular '+rel)
            if rel=='MANIFEST.json':continue
            require(p.name!='MANIFEST.json','nested manifest')
            require(rel in expected,'unlisted '+rel)
            raw=p.read_bytes(); row=expected[rel]
            require(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'content mismatch '+rel)
            found.add(rel)
    require(found==set(expected),'missing inventory member')
    require(found_dirs==dirs,'unexpected or missing directory')
    return {'status':'PASS','files':len(found)}
if __name__=='__main__':print(json.dumps(verify(Path(__file__).parent),sort_keys=True))
