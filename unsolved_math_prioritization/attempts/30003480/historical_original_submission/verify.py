from fractions import Fraction as F
from itertools import product
from math import comb
from functools import reduce
from pathlib import Path
from hashlib import sha256
import json
checks=0;sections={}
def ck(v,s):
 global checks
 assert v,s
 checks+=1;sections[s]=sections.get(s,0)+1
support=[(0,0,0),(0,1,1),(1,0,1),(1,1,0)]
for a,b in product(support,repeat=2):
 if a!=b:ck(sum(x!=y for x,y in zip(a,b))!=1,'parity off-diagonal zero')
realizations=0
for nums in product(range(11),repeat=3):
 t=[F(i,20) for i in nums]
 if any(t[i]>sum(t)-t[i] for i in range(3)):continue
 w=[1-sum(t)/2]+[(sum(t)-2*x)/2 for x in t]
 ck(sum(w)==1 and min(w)>=0,'real realization weights')
 for i in range(3):
  p=sum(w[j] for j,bits in enumerate(support) if bits[i])
  ck(p==t[i],'real marginal eigenvalues');ck(p*(1-p)==t[i]*(1-t[i]),'real Gram determinants')
 realizations+=1
boundary=0
for b,c in product([F(i,40) for i in range(1,20)],repeat=2):
 if b+c>=F(1,2):continue
 t=[b+c,b,c];d=[x*(1-x) for x in t]
 diffs=[sum(d)-2*x for x in d]
 ck(diffs==[2*b*c,2*c*(1-b-c),2*b*(1-b-c)],'true boundary inside hull')
 ck(min(diffs)>0 and min(d)>0 and max(d)<F(1,4),'true boundary inside hull')
 for sign in [-1,1]:
  eps=min(b,c,F(1,2)-b-c)/10;z=[b+c+sign*eps,b,c]
  ck((z[0]>z[1]+z[2])==(sign>0),'boundary crossing triangle')
 boundary+=1
interior=0
for i,j in product(range(1,12),repeat=2):
 k=24-i-j
 if not 0<k<12:continue
 t=[F(i,24),F(j,24),F(k,24)];d=[x*(1-x) for x in t]
 ck(sum(t)==1,'conjugate plane interior')
 for u in range(3):
  v,w=[z for z in range(3) if z!=u]
  ck(t[u]<t[v]+t[w],'conjugate plane interior')
  ck(sum(d)-2*d[u]==2*t[v]*t[w]>0,'conjugate plane inside hull')
 interior+=1
# Exact polynomial coefficient check t^a(1-t)^a invariant under t->1-t.
for a in range(41):
 coef=[0]*(2*a+1)
 for k in range(a+1):coef[a+k]=(-1)**k*comb(a,k)
 transformed=[sum(coef[k]*comb(k,j)*(-1)**j for k in range(j,len(coef))) for j in range(len(coef))]
 for p,q in zip(coef,transformed):ck(p==q,'pullback polynomial involution')
# Monotonicity sign in equation5 is exact from ordered positive radicands.
for den in [20,40]:
 for ai in range(2,den//4):
  for aj in range(1,ai):
   di,dj=F(ai,den),F(aj,den)
   for sn in range(1,21):
    s=F(sn,20)
    if s*s>4*di:ck(0<s*s-4*di<s*s-4*dj,'ball-ratio derivative sign')
# Positive rational source-polynomial counterexample.
roots=[F(49,100),F(36,100),F(36,100),F(1,100)];d=[x*x for x in roots]
q1=reduce(lambda x,y:x*y,[sum(d)-2*x for x in d],F(1))
q2=reduce(lambda x,y:x*y,[sum(e*x for e,x in zip(signs,roots)) for signs in product([-1,1],repeat=4)],F(1))/2
ck(q1==F(168760917,305175781250),'proposed polynomial exact counterexample')
ck(q2==F(23632249608,2384185791015625),'proposed polynomial exact counterexample')
ck(q1-q2==F(2589624828909,4768371582031250)>0,'proposed polynomial exact counterexample')
ck(all(0<x<F(1,4) for x in d),'positive counterexample domain');ck(all(sum(d)-2*x>0 for x in d),'positive counterexample hull')
ck(d[0]>F(2,5)*(1-F(2,5)),'spectral inequality violation')
ck(d[1]==d[2]<F(1,6)*(1-F(1,6)),'spectral inequality violation')
ck(d[3]<F(1,100)*(1-F(1,100)),'spectral inequality violation')
ck(F(1,3)+F(1,100)<F(2,5),'spectral inequality violation')
# Exact tensor-product slice controls, actual flattening matrices.
def gram(T,n):
 out=[]
 for i in range(n):
  pairs={}
  for bits,a in T.items():
   rest=bits[:i]+bits[i+1:];pairs.setdefault(rest,[F(0),F(0)])[bits[i]]=a
  aa=sum(x*x for x,y in pairs.values());bb=sum(y*y for x,y in pairs.values());ab=sum(x*y for x,y in pairs.values())
  out.append(aa*bb-ab*ab)
 return out
for seed in range(100):
 T={bits:F(((seed+3)*(j+5)+j*j)%5-2,10) for j,bits in enumerate(product(range(2),repeat=3))}
 old=gram(T,3);norm=sum(a*a for a in T.values());ck(norm<=1,'slice norms')
 for n in [4,5,6]:
  T={bits+(b,):a*u for bits,a in T.items() for b,u in enumerate([F(3,5),F(4,5)])}
  ck(sum(a*a for a in T.values())==norm,'slice norms')
  ck(gram(T,n)==old+[F(0)]*(n-3),'rank-one slice Gram preservation')
# Printed three-factor display check at GHZ, using its exact determinants.
g=[F(1,4)]*3;Q1=reduce(lambda a,b:a*b,[sum(g)-2*x for x in g],F(1));Q2=reduce(lambda a,b:a*b,[sum(F(e,2) for e in signs) for signs in product([-1,1],repeat=3)],F(1))/2
ck(Q1==F(1,64) and Q2==F(9,512),'printed display GHZ check');ck(F(1,4)>F(3,16),'printed display GHZ check')
receipt={'artifact_sha256':sha256(Path('COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'assertions':checks,'sections':sections,'real_three_factor_realizations':realizations,'boundary_samples':boundary,'interior_conjugate_samples':interior,'Q1_minus_Q2':str(q1-q2),'scope':'Exact supporting controls. Nonexistence of every polynomial follows from the written multiplicity argument, not finite sampling.'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
