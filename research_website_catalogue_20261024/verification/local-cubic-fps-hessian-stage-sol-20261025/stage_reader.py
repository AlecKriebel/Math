"""Private execution only: missing old site paths resolve read-only to live bytes.

No old asset tree, symlinks or aliases are created. Proposed new files remain
the actual private files; only absent pre-existing paths have fallback reads.
"""
from pathlib import Path
import builtins,io,runpy,subprocess,sys
O=Path(__file__).resolve().parent;S=O/'public';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
rb,rt,st,exists,isfile,isdir,it=Path.read_bytes,Path.read_text,Path.stat,Path.exists,Path.is_file,Path.is_dir,Path.iterdir
real_open=builtins.open;real_output=subprocess.check_output
def physical_exists(p):
 try:st(p);return True
 except (FileNotFoundError,NotADirectoryError):return False
def fallback(p):
 p=Path(p)
 if p.is_absolute() and p.is_relative_to(S) and not physical_exists(p):
  q=LIVE/p.relative_to(S)
  if physical_exists(q):return q
 return p
Path.read_bytes=lambda p:rb(fallback(p))
Path.read_text=lambda p,*a,**k:rt(fallback(p),*a,**k)
Path.stat=lambda p,*a,**k:st(fallback(p),*a,**k)
Path.exists=lambda p:exists(fallback(p))
Path.is_file=lambda p:isfile(fallback(p))
Path.is_dir=lambda p:isdir(fallback(p))
Path.iterdir=lambda p:it(fallback(p))
def opened(file,mode='r',*a,**k):
 if isinstance(file,(str,bytes,Path)):
  if not any(x in mode for x in ['w','a','x','+']):file=fallback(file)
 return real_open(file,mode,*a,**k)
builtins.open=opened
io.open=opened
def output(args,*a,**k):
 if isinstance(args,list):args=[str(fallback(x)) if isinstance(x,(str,Path)) and str(x).startswith(str(S)) else x for x in args]
 return real_output(args,*a,**k)
subprocess.check_output=output
sys.argv=sys.argv[1:];runpy.run_path(sys.argv[0],run_name='__main__')
