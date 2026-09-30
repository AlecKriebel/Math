from pathlib import Path
from math import gcd
from functools import reduce
from itertools import product
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form
import random,json,hashlib
rng=random.Random(222);checks=0;sequences=0
def ck(t):
 global checks
 assert t;checks+=1
def gg(v):return reduce(gcd,(abs(int(x)) for x in v),0)
for g in range(1,4):
 d=2*g;J=s.zeros(d)
 for i in range(g):J[2*i,2*i+1]=1;J[2*i+1,2*i]=-1
 for rep in range(100):
  V=[];W=[];Pinv=s.eye(d)
  for k in range(1+rep%6):
   if k==rep%7 and rep%4==0:v=s.zeros(d,1)
   else:
    vals=[rng.randrange(-3,4) for _ in range(d)];vals[rep%d]=1;v=s.Matrix(vals)
   ck(gg(v) in (0,1));T=s.eye(d)+v*(J*v).T;Ti=s.eye(d)-v*(J*v).T
   ck(T*Ti==s.eye(d));ck(T.T*J*T==J)
   z=s.Matrix([rng.randrange(-4,5) for _ in range(d)])
   for m in (0,1,2,-3):ck(m*v+(s.eye(d)-Ti)*z==(m+(z.T*J*v)[0])*v)
   V.append(v);W.append(Pinv*v)
   ck(hermite_normal_form(s.Matrix.hstack(*V))==hermite_normal_form(s.Matrix.hstack(*W)))
   Pinv=Pinv*Ti
  sequences+=1
# The primitive-slope example has an exact parity obstruction.
A=s.Matrix([[1,1],[0,2]]);ck(abs(A.det())==2)
for x,y in product(range(-20,21),repeat=2):
 ck((y%2==0)==(s.Rational(y,2).q==1 and (s.Rational(x)-s.Rational(y,2)).q==1))
for d in range(1,7):
 for rep in range(100):
  U=s.eye(d)
  if d>1:
   for k in range(10):
    i,j=rng.sample(range(d),2);a=rng.randrange(-3,4);U[i,:]=U[i,:]+a*U[j,:]
  Q=U.T*s.diag(*[(-1)**i for i in range(d)])*U
  v=s.Matrix([rng.randrange(-12,13) for _ in range(d)])
  ck(abs(Q.det())==1);ck(gg(Q*v)==gg(v))
r={'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'exact_assertions':checks,'transvection_sequences':sequences,'scope':'Exact integral homology/lattice identities; no nonabelian lift or positive sphere-factorization realization.','dependency':'sympy'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
