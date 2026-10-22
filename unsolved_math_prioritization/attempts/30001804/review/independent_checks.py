"""Independent finite-ring and signed group-ring controls; no surface relations computed."""
from itertools import product
from pathlib import Path
from math import gcd
import json,hashlib
P=Path(__file__).parent;count=0;families={}
def ck(b,label):
 global count
 assert b,label
 count+=1;families[label]=families.get(label,0)+1
R=list(product(range(3),repeat=4));zero=(0,0,0,0);I=(1,0,0,1);A=(0,0,1,0);B=(0,1,0,0)
def add(x,y):return tuple((a+b)%3 for a,b in zip(x,y))
def neg(x):return tuple(-a%3 for a in x)
def mul(x,y):return ((x[0]*y[0]+x[1]*y[2])%3,(x[0]*y[1]+x[1]*y[3])%3,(x[2]*y[0]+x[3]*y[2])%3,(x[2]*y[1]+x[3]*y[3])%3)
def vec(x,v):return ((x[0]*v[0]+x[1]*v[1])%3,(x[2]*v[0]+x[3]*v[1])%3)
ann1={x for x in R if vec(x,(1,0))==(0,0)}
N={(add(mul(x,B),neg(mul(y,A))),y) for x,y in product(R,repeat=2)}
direct={(x,y) for x,y in product(R,repeat=2) if add(x,mul(y,A)) in ann1}
ck(N==direct and len(N)==729,'M2F3 relation module')
for x,y in product(R,repeat=2):
 ck(((x,y) in N)==(add(x,mul(y,A)) in ann1),'M2F3 kernel equality')
for z in R:
 for x,y in [(I,A),(B,I),(A,B),(zero,I)]:
  ck(add(mul(z,x),mul(mul(z,y),A))==mul(z,add(x,mul(y,A))),'M2F3 left linearity')
# Arbitrary generator c=A e0, with class the second standard vector.
a0=B;a1=I;c=(A,zero)
Tc=add(mul(c[0],a0),mul(c[1],a1));consistency=add(I,neg(Tc))
images={add(mul(x,a0),mul(y,a1)) for x,y in N}
J={mul(x,consistency) for x in R};ann2={x for x in R if vec(x,(0,1))==(0,0)}
ck(images==J==ann2,'arbitrary representative ideal')
for r in R:
 ck((r in J)==(vec(r,(0,1))==(0,0)),'arbitrary representative annihilator')
# Integer countercontrol where the consistency relation is essential.
ck(gcd(6,-8)==2 and 6!=2,'essential consistency term over integers')
# Noncommutative integral S3 group-ring orientation/stabilizer control.
G=list(__import__('itertools').permutations(range(3)));e=(0,1,2);h=(1,0,2);a=(1,2,0)
def comp(p,q):return tuple(p[q[i]] for i in range(3))
def inv(p):return tuple(p.index(i) for i in range(3))
k=comp(comp(inv(a),h),a)
def radd(x,y):
 z=dict(x)
 for g,v in y.items():z[g]=z.get(g,0)+v
 return {g:v for g,v in z.items() if v}
def rmul(x,y):
 z={}
 for g,b in x.items():
  for q,c in y.items():
   p=comp(g,q);z[p]=z.get(p,0)+b*c
 return {g:v for g,v in z.items() if v}
# Normal form in the induced left module R/R(1-epsilon*k), indexed by right cosets.
reps=sorted({min(g,comp(g,k)) for g in G})
def nf(x,eps):
 out=[0]*len(reps)
 for g,c in x.items():
  rep=min(g,comp(g,k));sign=1 if g==rep else eps
  out[reps.index(rep)]+=c*sign
 return tuple(out)
for eps in [-1,1]:
 base={e:1,k:-eps};stab={e:1,h:-eps}
 right=rmul(stab,{a:1});wrong=rmul({a:1},stab)
 ck(right==rmul({a:1},base),'signed stabilizer conjugation')
 ck(nf(right,eps)==(0,0,0),'signed stabilizer correct order')
 ck(nf(wrong,eps)!=(0,0,0),'signed stabilizer reversed order fails')
 for g in G:
  ck(nf(rmul({g:1},base),eps)==(0,0,0),'left ideal normal form')
sha=hashlib.sha256((P/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest()
assert sha=='5dfdb8485eb030b05ce81b69268d75625e2633e0888c3d3117172e475d759d40'
r={'status':'pass','assertions':count,'families':families,'reviewed_artifact_sha256':sha,'scope':'Exact noncommutative kernel and signed-stabilizer diagnostics; no mapping-class relation list or general-genus computation.'}
(P/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
