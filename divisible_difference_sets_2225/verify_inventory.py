"""Verify exact recursive regular-file inventory; refuse symbolic links."""
import hashlib,json
from pathlib import Path

def verify(root):
 entries=json.loads((root/'INVENTORY.json').read_text())['files']
 expected={row['path']:row for row in entries}
 if len(expected)!=len(entries):raise RuntimeError('duplicate inventory entry')
 actual={}
 for p in root.rglob('*'):
  if p.is_symlink():raise RuntimeError('symlink rejected')
  if p.is_file() and p.relative_to(root).as_posix()!='INVENTORY.json':actual[p.relative_to(root).as_posix()]=p
 if set(actual)!=set(expected):raise RuntimeError('recursive inventory mismatch')
 for name,p in actual.items():
  b=p.read_bytes();row=expected[name]
  if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise RuntimeError('content mismatch: '+name)
 print(json.dumps({'passed':True,'files':len(actual)},sort_keys=True))
if __name__=='__main__':verify(Path(__file__).parent)
