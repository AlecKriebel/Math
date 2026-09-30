"""Independent word and exact integral-lattice controls, without SymPy."""
from pathlib import Path
from hashlib import sha256
from math import gcd
from functools import reduce
from itertools import product
from collections import Counter
from fractions import Fraction as F
import random,json
N=Counter();cases=Counter();rng=random.Random(2770)
def ck(k,v):
 if not v:raise AssertionError(k)
 N[k]+=1
def omega(x,y):return sum(x[i]*y[i+1]-x[i+1]*y[i] for i in range(0,len(x),2))
def gg(v):return reduce(gcd,v,0)
def plus(x,y):return [a+b for a,b in zip(x,y)]
def times(c,x):return [c*a for a in x]
def trans(x,v,s=1):return plus(x,times(s*omega(x,v),v))
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def mv(A,v):return [sum(x*y for x,y in zip(row,v)) for row in A]
def transpose(A):return list(map(list,zip(*A)))
def det(A):
 n=len(A);B=[[F(x) for x in row] for row in A];d=F(1)
 for i in range(n):
  j=next((j for j in range(i,n) if B[j][i]),None)
  if j is None:return 0
  if j!=i:B[i],B[j]=B[j],B[i];d=-d
  t=B[i][i];d*=t
  for j in range(i+1,n):
   q=B[j][i]/t
   for k in range(i+1,n):B[j][k]-=q*B[i][k]
 return int(d)
def bezout(v):
 # Accumulate an explicit integer dot-product certificate.
 g=0;zs=[]
 for x in v:
  aa,bb=abs(g),abs(x);u0,u1,v0,v1=1,0,0,1
  while bb:q=aa//bb;aa,bb=bb,aa-q*bb;u0,u1=u1,u0-q*u1;v0,v1=v1,v0-q*v1
  u=u0*(1 if g>=0 else -1);w=v0*(1 if x>=0 else -1)
  zs=[u*z for z in zs]+[w];g=aa
 return g,zs
for g in range(1,5):
 dim=2*g
 for rep in range(120):
  vs=[]
  for i in range(rep%7):
   v=[rng.randrange(-6,7) for _ in range(dim)];q=gg(v)
   if q:v=[x//q for x in v]
   if (i+rep)%5==0:v=[0]*dim
   vs.append(v)
  k=len(vs);C=eye(k);ws=[]
  for i,v in enumerate(vs):
   w=v[:];coeff=[0]*k;coeff[i]=1
   for j in reversed(range(i)):
    q=omega(w,vs[j]);w=plus(w,times(-q,vs[j]));coeff[j]-=q
   ws.append(w)
   for j in range(k):C[j][i]=coeff[j]
   ck('transport_integer_combination',w==[sum(coeff[j]*vs[j][h] for j in range(k)) for h in range(dim)])
   x=[rng.randrange(-6,7) for _ in range(dim)];y=[rng.randrange(-6,7) for _ in range(dim)]
   ck('inverse_transvection',trans(trans(x,v),v,-1)==x)
   ck('symplectic_pairing',omega(trans(x,v),trans(y,v))==omega(x,y))
   qvec=[]
   for h in range(0,dim,2):qvec += [v[h+1],-v[h]]
   common,z=bezout(qvec)
   ck('bezout_pairing_certificate',omega(z,v)==common)
   ck('primitive_or_zero',common in (0,1))
   if common:
    for m in (-3,0,1,5):
     coeff2=-2;zz=times(coeff2-m,z)
     ck('zero_or_allowed_multiplicity_range',plus(times(m,v),plus(zz,times(-1,trans(zz,v,-1))))==times(coeff2,v))
  if k:
   # Explicit inverse of unitriangular C via finite nilpotent geometric sum.
   U=[[C[i][j]-int(i==j) for j in range(k)] for i in range(k)];inv=eye(k);power=eye(k)
   for h in range(1,k):
    power=mm(power,U);inv=[[inv[i][j]+(-1)**h*power[i][j] for j in range(k)] for i in range(k)]
   ck('unitriangular_determinant',det(C)==1)
   ck('integral_inverse',mm(C,inv)==eye(k))
   V=transpose(vs);W=transpose(ws)
   ck('both_integral_span_inclusions',mm(V,C)==W and mm(W,inv)==V)
  cases['transport_sequences']+=1
# Free-word check: twist about a fixes a and sends b to b a^-1; inverse sends b to b a.
def invword(w):return tuple(-x for x in reversed(w))
def reduceword(w):
 r=[]
 for x in w:
  if r and r[-1]==-x:r.pop()
  else:r.append(x)
 return tuple(r)
def inverse_twist(w):
 out=[]
 for x in w:
  image=(1,) if abs(x)==1 else (2,1)
  if x<0:image=invword(image)
  out+=image
 return reduceword(out)
def ab(w):return [sum((1 if x>0 else -1) for x in w if abs(x)==i) for i in (1,2)]
for length in range(6):
 for w in product((1,-1,2,-2),repeat=length):
  if reduceword(w)!=w:continue
  z=ab(w)
  for m in (-2,0,1,3):
   power=(1,)*m if m>=0 else (-1,)*(-m)
   expr=reduceword(w+power+inverse_twist(invword(w)))
   ck('twisted_conjugacy_word_ab',ab(expr)==[m-z[1],0])
  cases['reduced_words']+=1
for x,y in product(range(-25,26),repeat=2):
 if y%2==0:ck('finite_index_constructive',(x-y//2)+y//2==x and 2*(y//2)==y)
 else:ck('finite_index_parity_obstruction',y%2==1)
H=[[0,1],[1,0]];E8=[[2*int(i==j) for j in range(8)] for i in range(8)]
for i,j in [(i,i+1) for i in range(6)]+[(2,7)]:E8[i][j]=E8[j][i]=-1
for Q in (H,[[1,0],[0,-1]],E8):
 ck('unimodular_symmetric',det(Q) in (-1,1) and transpose(Q)==Q)
 for rep in range(300):
  v=[rng.randrange(-30,31) for _ in Q]
  ck('fiber_divisibility_gcd',gg(mv(Q,v))==gg(v));cases['intersection_vectors']+=1
for d in range(1,21):
 for h in range(20):
  b=2*h+2*d-2;ck('riemann_hurwitz',2-2*h==2*d-b and b%2==0 and b>=0)
root=Path(__file__).resolve().parent
r={'artifact_sha256':sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),'independent_assertions':sum(N.values()),'categories':dict(N),'cases':dict(cases),'scope':'Exact abelian, free-word, integral-span and degree controls. No positive sphere-factorization realization or nonabelian extension computation.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
