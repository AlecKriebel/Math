"""Private runner; only absent old site reads fall through to actual production."""
from pathlib import Path
import builtins, io, runpy, sys
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;P=E.parent.parents[1];S=E/'public';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
sys.path[:0]=[str(E),str(P/'scripts')]
rb,rt,st,ex,fi,di,it=Path.read_bytes,Path.read_text,Path.stat,Path.exists,Path.is_file,Path.is_dir,Path.iterdir
realopen=builtins.open
def physical(p):
    try:st(p);return True
    except (FileNotFoundError,NotADirectoryError):return False
def fallback(p):
    p=Path(p)
    if p.is_absolute() and p.is_relative_to(S) and not physical(p):
        q=LIVE/p.relative_to(S)
        if physical(q):return q
    return p
Path.read_bytes=lambda p:rb(fallback(p))
Path.read_text=lambda p,*a,**k:rt(fallback(p),*a,**k)
Path.stat=lambda p,*a,**k:st(fallback(p),*a,**k)
Path.exists=lambda p:ex(fallback(p))
Path.is_file=lambda p:fi(fallback(p))
Path.is_dir=lambda p:di(fallback(p))
Path.iterdir=lambda p:it(fallback(p))
def opened(file,mode='r',*a,**k):
    if isinstance(file,(str,bytes,Path)):
        if any(x in mode for x in 'wax+'):
            if not Path(file).resolve().is_relative_to(E):raise RuntimeError('write outside resumed stage')
        else:file=fallback(file)
    return realopen(file,mode,*a,**k)
builtins.open=opened;io.open=opened
script=Path(sys.argv[1]).resolve()
if not script.is_relative_to(E):raise RuntimeError('script outside resume')
sys.argv=sys.argv[1:];runpy.run_path(str(script),run_name='__main__')
