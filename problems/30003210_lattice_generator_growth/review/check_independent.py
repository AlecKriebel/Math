from pathlib import Path
from fractions import Fraction as F
from itertools import permutations
import json,hashlib
p=Path('/workspace/shared/math-30003210');n=0
for name in ['FINAL_AUTHOR_MANIFEST.json','SOURCE_HASHES.json','ADDITIONAL_SOURCE_HASHES.json']:
 for file,h in json.loads((p/name).read_text()).items():assert hashlib.sha256((p/file).read_bytes()).hexdigest()==h;n+=1
# Exact valuation inequalities valid also at ramified rational valuations s>=1.
for den in range(1,25):
 for num in range(den,5*den):
  v=F(num,den);assert 1+2*v>1+v and 3*v>1+v;n+=1
for a in range(1,31):
 critical=F(a,a+1)
 assert a*(1-critical)-critical==0;n+=1
 for step in range(1,20):
  alpha=critical+(1-critical)*F(step,20)
  assert a*(1-alpha)-alpha<0;n+=1
# Compute A5, commutator-supported normal closure and class-size simplicity control.
def mul(p,q):return tuple(p[q[i]] for i in range(5))
def inv(p):return tuple(p.index(i) for i in range(5))
G=[p for p in permutations(range(5)) if sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0]
e=tuple(range(5));x=(1,2,0,3,4)
classes={frozenset(mul(mul(g,a),inv(g)) for g in G) for a in G}
assert sorted(map(len,classes))==[1,12,12,15,20];n+=1
comm={mul(mul(mul(x,g),inv(x)),inv(g)) for g in G}
normal={mul(mul(g,c),inv(g)) for c in comm for g in G}
H={e};stack=[e]
while stack:
 a=stack.pop()
 for c in normal:
  b=mul(a,c)
  if b not in H:H.add(b);stack.append(b)
assert len(H)==60;n+=1
print(json.dumps({'status':'PASS','independent_assertions':n,'scope':'integrity, valuation inequalities, transfer exponents and finite group diagnostic; cited lattice theorems are not recomputed'},indent=2))
