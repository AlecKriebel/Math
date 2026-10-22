"""Complete cold own evidence reconstruction and readback, without providers."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parent
if sys.flags.optimize or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):raise RuntimeError('Use optimize0 -I -S -B')
if(ROOT/'MANIFEST.json').exists():raise RuntimeError('Cannot write into a sealed packet')
q=ROOT/'verify_custody17.py';body=q.read_bytes();ns={'__file__':str(q),'__name__':'cold_complete_custody'}
exec(compile(body,str(q),'exec',dont_inherit=True,optimize=0),ns)
result=ns['verify']();result['controller_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
out=ROOT/'private/COLD_CUSTODY_REPLAY.json'
with out.open('x')as h:h.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
