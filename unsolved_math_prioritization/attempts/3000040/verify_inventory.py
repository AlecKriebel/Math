"""Fail closed on all non-regular entries before reading any manifest or payload."""
import hashlib,json,os,stat,sys
from pathlib import Path

def inventory(root):
    root=Path(root)
    # lstat root, then recursively lstat every entry; never follow links.
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise ValueError('root is not a real directory')
    files=[]
    def scan(directory):
        for entry in sorted(os.scandir(directory),key=lambda e:e.name):
            mode=entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode): scan(Path(entry.path))
            elif stat.S_ISREG(mode): files.append(Path(entry.path))
            else: raise ValueError('unsafe filesystem entry: '+str(Path(entry.path).relative_to(root)))
    scan(root)
    return files

def verify(root):
    root=Path(root); files=inventory(root) # MUST finish before any reads.
    manifest=json.loads((root/'MANIFEST.json').read_text())
    expected=manifest['files']; actual={str(p.relative_to(root)):p for p in files if p != root/'MANIFEST.json'}
    if set(actual)!=set(expected):raise ValueError('inventory differs from manifest')
    for name,p in actual.items():
        data=p.read_bytes()
        if {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}!=expected[name]:raise ValueError('digest mismatch: '+name)
    return {'verified_files':len(actual),'unsafe_entries_rejected_before_manifest_read':True}
if __name__=='__main__': print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent),sort_keys=True))
