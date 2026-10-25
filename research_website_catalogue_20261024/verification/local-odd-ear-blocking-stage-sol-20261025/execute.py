"""Execute one owned private program; conventional Python writes stay here."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import builtins,io,runpy
O=Path(__file__).resolve().parent
P=O.parents[1]
script=Path(sys.argv[1]).resolve()
if not script.is_relative_to(O):raise RuntimeError('execution outside private stage')
sys.path[:0]=[str(O),str(P/'scripts')]
real_open=builtins.open
def guarded_open(file,mode='r',*args,**kwargs):
    if isinstance(file,(str,bytes,Path)) and any(x in mode for x in 'wax+'):
        if not Path(file).resolve().is_relative_to(O):raise RuntimeError('write outside private stage:'+str(file))
    return real_open(file,mode,*args,**kwargs)
builtins.open=guarded_open
io.open=guarded_open
sys.argv=sys.argv[1:]
runpy.run_path(str(script),run_name='__main__')
