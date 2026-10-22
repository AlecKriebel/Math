"""Read-only recursive exact-byte inventory validation; safe under python -O."""
from pathlib import Path
import hashlib,json,sys,stat

def verify(root):
 root=Path(root)
 if root.is_symlink():raise RuntimeError('Symlink root forbidden')
 if not root.is_dir():raise RuntimeError('Root must be a directory')
 paths=list(root.rglob('*'))
 if any(x.is_symlink() for x in paths):raise RuntimeError('Symlink entry forbidden')
 for x in paths:
  mode=x.lstat().st_mode
  if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):raise RuntimeError('Unsupported filesystem entry: '+x.relative_to(root).as_posix())
 manifest=json.loads((root/'MANIFEST.json').read_text())
 entries=manifest['files']
 names=[x['path'] for x in entries]
 if len(names)!=len(set(names)):raise RuntimeError('Duplicate manifest entry')
 actual={x.relative_to(root).as_posix() for x in paths if x.is_file() and x.relative_to(root).as_posix()!='MANIFEST.json'}
 if set(names)!=actual:raise RuntimeError('Recursive inventory mismatch')
 for item in entries:
  name=item['path']
  if Path(name).is_absolute() or '..' in Path(name).parts:raise RuntimeError('Unsafe manifest path')
  b=(root/name).read_bytes()
  if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=item['sha256']:raise RuntimeError('Byte/hash mismatch: '+name)
 return {'result':'PASS','files':len(entries),'recursive':True,'symlinks':'forbidden'}
if __name__=='__main__':print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent),sort_keys=True))
