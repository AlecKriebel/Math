#!/usr/bin/env python3
"""Independent exact controls for analytic bridges; imports only our own checker."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,permutations
from hashlib import sha256
import sympy as s
import json
import independent_cover as C
n=0;groups={}
def ck(t,g):
 global n
 assert bool(t),g
 n+=1;groups[g]=groups.get(g,0)+1
root=Path(__file__).resolve().parent
rt=s.sqrt(3);a=(2-rt)/4;b=(2*rt-3)/4
star=[s.Rational(1,4),a,a,b,a,b,b,3*a];alpha=(3-rt)/6;theta=(3-rt)/2
for x in range(8):
 k=x.bit_count();actual=(1-alpha)*theta**k*(1-theta)**(3-k)+(alpha if x==0 else 0)
 ck(s.simplify(actual-star[x])==0,'exact star membership')
 ck(star[x]>0,'strict star positivity')
ck(s.simplify(sum(star)-1)==0,'star mass')
rows=[]
for x in range(8):
 for y in range(x+1,8):
  if x&y!=x and x&y!=y:
   row=[0]*8
   for i,d in [(x&y,1),(x|y,1),(x,-1),(y,-1)]:row[i]+=d
   rows.append(row)
   ck(s.simplify(star[x&y]*star[x|y]-star[x]*star[y])>=0,'nine necessary inequalities')
active=[]
for x,y in [(3,5),(3,6),(5,6)]:
 row=[0]*8
 for i,d in [(x&y,1),(x|y,1),(x,-1),(y,-1)]:row[i]+=d
 active.append(row)
 ck(s.simplify(star[x&y]*star[x|y]-star[x]*star[y])==0,'active face exactness')
for x in range(8):ck(s.simplify(star[x]-(s.Rational(1,4) if x.bit_count()%2==0 else 0)-a*sum(r[x] for r in active))==0,'convex gradient multipliers')
for flip in range(8):
 even=flip if flip.bit_count()%2==0 else flip^7
 ck(even.bit_count()%2==0,'even orientation representative')
for x,y in product(range(8),repeat=2):
 ck(((x^7)&(y^7))==((x|y)^7) and ((x^7)|(y^7))==((x&y)^7),'global complement cone symmetry')
# Every support pattern, with two distinct positive weight assignments.
channel_cases=0
for mask in range(1,256):
 for recipe in [0,1]:
  raw=[(1+(i%3 if recipe else 0)) if mask>>i&1 else 0 for i in range(8)]
  p=[Q(x,sum(raw)) for x in raw]
  for bit in [1,2,4]:
   for swap in [0,1]:
    indexes=[x for x in range(8) if bool(x&bit)==bool(swap)]
    S0={x for x in indexes if p[x]};S1={x for x in indexes if p[x^bit]}
    if not S0 or not S1 or not S0<=S1:continue
    tau=min(p[x^bit]/p[x] for x in S0);r=p.copy()
    for x in indexes:r[x]=(1+tau)*p[x];r[x^bit]=p[x^bit]-tau*p[x]
    ck(tau>0 and min(r)>=0 and sum(r)==1,'channel reversed law')
    ck(sum(x>0 for x in r)<sum(x>0 for x in p),'strict support decrease')
    for x in indexes:ck(r[x]/(1+tau)==p[x] and r[x^bit]+tau*r[x]/(1+tau)==p[x^bit],'channel reconstruction')
    channel_cases+=1
# Ordered-simplex coverage for all integer four-tuples in a bounded grid.
for w in product(range(4),repeat=4):
 if not sum(w):continue
 order=sorted(range(4),key=lambda i:-w[i]);p=[Q(x,sum(w)) for x in w]
 ordered=[p[i] for i in order]+[Q(0)]
 coeff=[(j+1)*(ordered[j]-ordered[j+1]) for j in range(4)]
 ck(min(coeff)>=0 and sum(coeff)==1,'ordered root barycentric weights')
 recon=[sum((coeff[j]/(j+1) for j in range(4) if i in order[:j+1]),Q(0)) for i in range(4)]
 ck(recon==p,'ordered root continuous coverage identity')
# Bisection coverage for arbitrary barycentric vectors in small rational controls.
for dim in range(2,7):
 for weights in product([1,2],repeat=dim):
  w=[Q(x,sum(weights)) for x in weights]
  for i in range(dim):
   j=(i+1)%dim;small,big=(i,j) if w[i]<=w[j] else (j,i)
   child=w.copy();child[small]=2*w[small];child[big]=w[big]-w[small]
   recon=child.copy();recon[small]=child[small]/2;recon[big]+=child[small]/2
   ck(min(child)>=0 and sum(child)==1 and recon==w,'edge bisection coverage identity')
# An independent high-accuracy rational log enclosure, with no fixed-point recurrence.
def rational_log2():
 lo=sum((Q(2,(2*j+1)*3**(2*j+1)) for j in range(80)),Q(0))
 return lo,lo+Q(9,4*161*3**161)
L2,H2=rational_log2()
for den in range(3,15):
 for num in range(1,den//2+1):
  x=Q(num,den);low=sum(((-1)**(j+1)*x**j/j for j in range(1,161)),Q(0));high=low+x**161/161
  for k in [-5,-1,0,1,5]:
   value=(1+x)*(Q(2)**k);lo,hi=C.logs(value)
   tl,th=(low+k*L2,high+k*H2) if k>=0 else (low+k*H2,high+k*L2)
   ck(Q(lo,C.BASE)<=tl<=th<=Q(hi,C.BASE),'independent log containment')
result={'verdict':'PASS','assertions':n,'groups':groups,'channel_cases':channel_cases,'artifact_sha256':sha256((root/'author_replay/SOURCE_APPLICATION.md').read_bytes()).hexdigest(),'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact lower certificate, support reduction, continuous-cover identities and independent log containment. The universal claims are audited analytically in REVIEW.md.'}
(root/'independent_analytic_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
