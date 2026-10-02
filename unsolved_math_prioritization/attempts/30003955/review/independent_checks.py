"""Independent exact algebra/Euler diagnostics, not a geometric proof engine."""
from itertools import permutations,product
from functools import reduce
from math import gcd,factorial
from pathlib import Path
import json,hashlib
assertions=0
def check(x):
 global assertions
 assertions+=1
 assert x

def mul(a,b):return tuple(a[b[j]] for j in range(len(a)))
def inv(a):return tuple(a.index(j) for j in range(len(a)))
def closure(gens,n):
 ans={tuple(range(n))}
 while True:
  new=ans|{mul(a,b) for a in ans for b in gens}
  if new==ans:return frozenset(ans)
  ans=new

def orbit_parts(H,points,action):
 rem=set(points);out=[]
 while rem:
  x=next(iter(rem));orb={action(h,x) for h in H};check(orb<=rem)
  rem-=orb;out.append(len(orb))
 return sorted(out)
counts=[]
for n in (3,4):
 G=frozenset(permutations(range(n)));I=tuple(range(n));subs={frozenset([I])};todo=list(subs)
 while todo:
  H=todo.pop()
  for g in G-H:
   K=closure(list(H)+[g],n)
   if K not in subs:subs.add(K);todo.append(K)
 for H in subs:
  regular=orbit_parts(H,G,mul);natural=orbit_parts(H,range(n),lambda h,x:h[x])
  check(regular==[len(H)]*(len(G)//len(H)))
  check((len(regular)>1)==(H!=G))
  check(sum(natural)==n)
 counts.append({'degree':n,'subgroups':len(subs)})
# Rebuild the S3 surface relation and pants image independently.
r=(1,2,0);t=(1,0,2);I=(0,1,2)
def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
check(mul(comm(r,t),comm(inv(r),t))==I)
H=closure([r,mul(mul(t,inv(r)),inv(t))],3)
check(len(H)==3)
check(orbit_parts(H,range(3),lambda h,x:h[x])==[3])
check(orbit_parts(H,list(permutations(range(3))),mul)==[3,3])
# Primitive integral lift of every nonzero small finite-field character.
characters=0
for g,p in [(2,2),(2,3),(2,5),(3,2)]:
 for c in product(range(p),repeat=2*g):
  if not any(c):continue
  j=next(j for j,a in enumerate(c) if a);scale=pow(c[j],-1,p)
  lift=tuple(scale*a%p for a in c)
  check(lift[j]==1 and reduce(gcd,lift)==1)
  check(all((v-scale*a)%p==0 for a,v in zip(c,lift)))
  # Jv=lift, where J has blocks [[0,1],[-1,0]].
  v=tuple(z for k in range(g) for z in (-lift[2*k+1],lift[2*k]))
  check(all(v[2*k+1]==lift[2*k] and -v[2*k]==lift[2*k+1] for k in range(g)))
  check(sum(lift[k]*v[k] for k in range(2*g))==0)
  characters+=1
# Pigeonhole alternatives and primitive difference classes; exhaustive small colors.
pigeon=0
for m in range(2,7):
 for vals in product(range(m),repeat=m):
  if 0 in vals:check(True)
  else:check(len(set(vals))<m)
  pigeon+=1
 for j in range(m):
  for k in range(j):
   v=[int(i==j)-int(i==k) for i in range(m)]
   check(any(v) and reduce(gcd,v)==1)
# Euler/gluing checks only; embeddedness/essentiality are proved in REVIEW.md.
def chi(g,b):return 2-2*g-b
topology=[]
for g in range(4,31):
 check(chi(1,1)+chi(1,1)-1==chi(2,1))
 check(chi(2,1)==chi(0,5))
 check(chi(0,5)==chi(0,3)+chi(0,4))
 check(chi(0,3)==chi(1,1))
 check(chi(2,1)+chi(g-2,1)==chi(g,0))
 check(g-2>0 and g-1>0)
 topology.append(g)
source=Path(__file__).with_name('reviewed_partial.md')
out={'all_passed':True,'assertions':assertions,'subgroup_enumerations':counts,'primitive_lift_characters':characters,'pigeonhole_tuples':pigeon,'genus_controls':topology,'scope':'Exact algebra and Euler diagnostics. Surface embeddedness/essentiality relies on the independent written geometric audit.','reviewed_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
