"""Full checker execution with owned, copied-byte, read-only input interception."""
from pathlib import Path
import json,runpy,sys
control=json.loads(Path(sys.argv[1]).read_text())
source=Path(control['path']).resolve();replacement=Path(control['bytes_file']).read_bytes()
original_bytes=Path.read_bytes;original_text=Path.read_text
def read_bytes(p):return replacement if p.resolve()==source else original_bytes(p)
def read_text(p,*a,**kw):
 if p.resolve()==source:return replacement.decode(kw.get('encoding') or (a[0] if a else None) or 'utf-8')
 return original_text(p,*a,**kw)
Path.read_bytes=read_bytes;Path.read_text=read_text
sys.argv=sys.argv[2:]
runpy.run_path(sys.argv[0],run_name='__main__')
