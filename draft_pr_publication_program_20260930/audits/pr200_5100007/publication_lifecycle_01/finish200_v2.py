"""Preserve frozen lifecycle logic; add the explicit tracker scope clarification to public custody."""
from pathlib import Path
import importlib.util,sys
A=Path(__file__).resolve().parent.parent
s=importlib.util.spec_from_file_location('frozen_lifecycle200',A/'publication_lifecycle_01/finish200.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def load():
 c,h,rv,n=v.load();original=n.construct
 def construct(stage,f):
  out=original(stage,f)
  for rel in ['publication_operations_01/update_tracker_v2.py','publication_operations_01/TRACKER_SCOPE_CLARIFICATION.json','publication_lifecycle_01/finish200_v2.py']:
   p=A/rel
   assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444
   out[v.CASE+rel]=p.read_bytes()
  return out
 n.construct=construct
 return c,h,rv,n
if __name__=='__main__':
 assert sys.dont_write_bytecode
 if sys.argv[1]=='pointer':v.record_pointer(sys.argv[2],sys.argv[3])
 else:
  c,h,rv,n=load();v.run(c,h,rv,n,sys.argv[1],sys.argv[2],sys.argv[3])
