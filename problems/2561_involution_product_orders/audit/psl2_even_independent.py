from pathlib import Path
"""Independently enumerate SL2(8) and compute the class on nine projective points."""
from itertools import product
from collections import Counter
import importlib.util,json
root=str(Path(__file__).resolve().parent.parent/'checks')+'/'
spec=importlib.util.spec_from_file_location('release',root+'colored_involutions.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def mul(a,b):
 # Polynomial convolution followed by long-division modulo X^3+X+1.
 raw=0
 for i in range(3):
  for j in range(3):
   if (a>>i)&1 and (b>>j)&1:raw^=1<<(i+j)
 for d in range(4,2,-1):
  if raw>>d&1:raw^=0b1011<<(d-3)
 return raw
inv={a:next(b for b in range(1,8) if mul(a,b)==1) for a in range(1,8)}
def action(m):
 a,b,c,d=m;out=[]
 for x in range(8):
  num=mul(a,x)^b;den=mul(c,x)^d;out.append(mul(num,inv[den]) if den else 8)
 out.append(mul(a,inv[c]) if c else 8)
 return tuple(out)
G={action(m) for m in product(range(8),repeat=4) if mul(m[0],m[3])^mul(m[1],m[2])==1}
identity=tuple(range(9));D=sorted(g for g in G if g!=identity and all(g[g[i]]==i for i in range(9)))
assert len(G)==504 and len(D)==63
trans={action((1^mul(a,b),mul(a,a),mul(b,b),1^mul(a,b))) for a,b in product(range(8),repeat=2) if a or b}
assert trans==set(D)
M,C=r.tables(D);z=r.solve(M,C);assert z['group_order']==1512 and z['stabilizer_size']==24
out={'whole_group_order':len(G),'all_involutions':len(D),'all_transvections_equal_full_class':True,'independent_nine_point_search':z}
print(out);json.dump(out,open(Path(__file__).resolve().parent/'psl2_even_independent_results.json','w'),indent=2)
