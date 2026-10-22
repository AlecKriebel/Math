"""Exact closed-directory verification: bytes, SHA256, full mode and ns mtime."""
from pathlib import Path
import hashlib,json,stat,sys
SEAL='CLOSED_DIRECTORY_SEAL.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(root,seal):
 if seal.get('exclusion_exact_relative_paths')!=[SEAL]:raise RuntimeError('seal exclusion mismatch')
 rows=seal.get('members');seen=set()
 if not isinstance(rows,list):raise RuntimeError('bad members')
 for row in rows:
  rel=row['path'];p=Path(rel)
  if type(rel) is not str or p.is_absolute() or '..' in p.parts or rel in seen or rel==SEAL:raise RuntimeError('bad/duplicate member')
  seen.add(rel);path=root/rel;st=path.lstat()
  if not stat.S_ISREG(st.st_mode):raise RuntimeError('not regular: '+rel)
  if type(row['bytes']) is not int or st.st_size!=row['bytes']:raise RuntimeError('bytes: '+rel)
  if sha(path)!=row['sha256']:raise RuntimeError('sha256: '+rel)
  if oct(st.st_mode)!=row['mode']:raise RuntimeError('mode: '+rel)
  if type(row['mtime_ns']) is not int or st.st_mtime_ns!=row['mtime_ns']:raise RuntimeError('mtime_ns: '+rel)
 actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() or p.is_symlink()}
 if actual-{SEAL}!=seen:raise RuntimeError('physical membership mismatch')
 return {'status':'PASS','members':len(rows),'member_bytes':sum(x['bytes'] for x in rows),'sha256':sha(root/SEAL) if (root/SEAL).exists() else None,'bytes_mode_nsmtime_all_verified':True}
if __name__=='__main__':
 root=Path(__file__).resolve().parent
 print(json.dumps(validate(root,json.loads((root/SEAL).read_text())),indent=2))
