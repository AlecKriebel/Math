"""Exact recursive inventory; only the root manifest excludes itself."""
from pathlib import Path, PurePosixPath
import hashlib,json,stat,sys

def safe_name(name):
    if not isinstance(name,str) or not name or '\\' in name or '\x00' in name or ':' in name:
        raise ValueError('Unsafe inventory path')
    path=PurePosixPath(name)
    if path.is_absolute() or any(x in ('','.', '..') for x in name.split('/')):
        raise ValueError('Unsafe inventory path')
    return name

def inventory(root):
    root=Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Invalid inventory root')
    result={}
    def walk(directory):
        for f in sorted(directory.iterdir()):
            name=safe_name(f.relative_to(root).as_posix())
            mode=f.lstat().st_mode
            if stat.S_ISLNK(mode): raise ValueError('Symlink forbidden: '+name)
            if stat.S_ISDIR(mode): walk(f)
            elif stat.S_ISREG(mode):
                if name=='MANIFEST.json': continue
                data=f.read_bytes()
                result[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
            else: raise ValueError('Special file forbidden: '+name)
    walk(root)
    return result

def verify(root):
    root=Path(root)
    manifest=root/'MANIFEST.json'
    if manifest.is_symlink() or not manifest.is_file():raise ValueError('Invalid root manifest')
    raw=json.loads(manifest.read_text())
    if set(raw)!= {'schema','files'} or raw['schema']!=1 or not isinstance(raw['files'],dict):raise ValueError('Bad manifest schema')
    for name,entry in raw['files'].items():
        safe_name(name)
        if name=='MANIFEST.json':raise ValueError('Root manifest cannot inventory itself')
        if not isinstance(entry,dict) or set(entry)!={'bytes','sha256'}:raise ValueError('Bad entry schema')
    actual=inventory(root)
    if actual!=raw['files']:raise ValueError('Recursive inventory mismatch')
    return actual

if __name__=='__main__':
    result=verify(Path(__file__).resolve().parent)
    print('PASS: exact recursive inventory ('+str(len(result))+' files); root manifest alone excluded.')
