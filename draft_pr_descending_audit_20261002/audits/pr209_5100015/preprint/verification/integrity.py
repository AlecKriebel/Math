"""Validate the frozen verification tree without running scientific code."""
from pathlib import Path
import hashlib,json,sys
if not __debug__ or sys.flags.optimize:raise RuntimeError('Optimized Python cannot verify assertions')
ROOT=Path(__file__).resolve().parent
def verify():
 m=ROOT/'MANIFEST.json';data=json.loads(m.read_text());paths=set()
 for row in data['files']:
  rel=Path(row['path']);assert not rel.is_absolute() and '..' not in rel.parts
  p=ROOT/rel;assert p.resolve().is_relative_to(ROOT) and not p.is_symlink() and p.is_file()
  raw=p.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],str(rel)
  assert row['path'] not in paths;paths.add(row['path'])
 actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p!=m}
 assert actual==paths,'Missing or unmanifested file';return len(paths)
if __name__=='__main__':print(json.dumps({'status':'PASS','verified_files':verify()}))
