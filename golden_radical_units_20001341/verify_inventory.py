"""Strict recursive inventory verification; only root INVENTORY.json is excluded."""
from pathlib import Path
import hashlib,json,os,stat

def inventory(root):
 root=Path(root); result=[]
 if root.is_symlink() or not root.is_dir():raise RuntimeError('unsafe root')
 for parent,dirs,files in os.walk(root,followlinks=False):
  for name in dirs+files:
   f=Path(parent)/name; rel=f.relative_to(root).as_posix()
   if f.is_symlink():raise RuntimeError('symlink prohibited: '+rel)
   if any(c in rel for c in ['\\','\x00','\n','\r']) or any(z in ['', '.', '..'] for z in rel.split('/')):raise RuntimeError('unsafe path: '+repr(rel))
   mode=f.stat().st_mode
   if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):raise RuntimeError('nonregular entry: '+rel)
   if stat.S_ISREG(mode) and rel!='INVENTORY.json':result.append({'path':rel,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 return sorted(result,key=lambda r:r['path'])

if __name__=='__main__':
 root=Path(__file__).resolve().parent;expected=json.loads((root/'INVENTORY.json').read_text())
 if inventory(root)!=expected['files']:raise RuntimeError('recursive inventory mismatch')
 print(json.dumps({'status':'PASS','files':len(expected['files']),'recursive':True,'root_manifest_only_exclusion':True},indent=2))
