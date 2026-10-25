"""Alter only bytes returned by one owned read map; original files stay intact."""
from pathlib import Path
import base64,json,runpy,sys
all_cases=json.loads(Path(sys.argv[1]).read_text());case=all_cases[int(sys.argv[2])]
overrides={Path(k).resolve():base64.b64decode(v) for k,v in case['overrides'].items()}
rb,rt=Path.read_bytes,Path.read_text
def read_bytes(p):return overrides[p.resolve()] if p.resolve() in overrides else rb(p)
def read_text(p,*a,**kw):
 if p.resolve() in overrides:return overrides[p.resolve()].decode(kw.get('encoding') or (a[0] if a else None) or 'utf-8')
 return rt(p,*a,**kw)
Path.read_bytes=read_bytes;Path.read_text=read_text
sys.argv=sys.argv[3:];runpy.run_path(sys.argv[0],run_name='__main__')
