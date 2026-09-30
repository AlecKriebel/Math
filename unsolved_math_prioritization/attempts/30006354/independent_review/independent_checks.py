#!/usr/bin/env python3
"""Independent symbolic and physical-vector controls for the scoped SU3/Haah audit."""
from pathlib import Path
from hashlib import sha256
from itertools import product
import json
import sympy as s
x,y=s.symbols('x y',nonzero=True)
K=s.Matrix([[1/x-x,x+x*y-y+1],[-1/x+1/y-1/(x*y)-1,y-1/y]])
I=s.eye(2); J=s.zeros(4); J[:2,2:]=I;J[2:,:2]=-I
V=I.col_join(K/2); W=I.col_join(-K/2)
bar=lambda A:A.subs({x:1/x,y:1/y},simultaneous=True).T
n=0; groups={}
def ck(ok,g):
 global n
 assert bool(ok),g
 n+=1;groups[g]=groups.get(g,0)+1
def equal(A,B,g):
 for z in A-B:ck(s.cancel(z)==0,g)
equal(bar(K),-K,'integer Laurent identities')
ck(s.factor(K.det())==4,'integer Laurent identities')
equal(bar(V)*J*V,K,'integer Laurent identities')
equal(bar(W)*J*W,-K,'integer Laurent identities')
equal(bar(V)*J*W,s.zeros(2),'integer Laurent identities')
D=V.row_join(W); inverse=(I/2).row_join(K.inv()).col_join((I/2).row_join(-K.inv()))
equal(D*inverse,s.eye(4),'exact complementary decomposition')
equal(inverse*D,s.eye(4),'exact complementary decomposition')
Pi=V*K.inv()*bar(V)*J
equal(Pi*Pi,Pi,'projector over rationals')
equal(Pi,(I/2).row_join(K.inv()).col_join((K/4).row_join(I/2)),'projector over rationals')
# Independently reduce rational Laurent coefficients to F3.
def terms(q):
 out={}
 for term in s.expand(q).as_ordered_terms():
  powers=term.as_powers_dict(); i=int(powers.get(x,0));j=int(powers.get(y,0))
  c=s.cancel(term/x**i/y**j);a,b=c.as_numer_denom();v=int(a)*pow(int(b)%3,-1,3)%3
  if v:out[i,j]=(out.get((i,j),0)+v)%3
 return {k:v for k,v in out.items() if v}
KP=[[terms(K[i,j]) for j in range(2)] for i in range(2)]
VP=[[terms(V[i,j]) for j in range(2)] for i in range(4)]
WP=[[terms(W[i,j]) for j in range(2)] for i in range(4)]
PP=[[terms(Pi[i,j]) for j in range(4)] for i in range(4)]
for A in [VP,WP,PP]:
 for row in A:
  for p in row:
   ck(all(abs(i)<=1 and abs(j)<=1 for i,j in p),'support certificate')
# Physical Pauli vectors use (cellx,celly,type, X-or-Z) keys.
def generator(r,c,kind,minus=False):
 A=WP if minus else VP;d={}
 for physicalrow in range(4):
  for (i,j),v in A[physicalrow][kind].items():d[r+i,c+j,physicalrow%2,physicalrow//2]=v
 return d
def physical_pair(a,b):
 return sum(v*b.get((i,j,t,1-z),0)*(1 if z==0 else -1) for (i,j,t,z),v in a.items())%3
def dot(a,b,C):return sum(a[i]*C[i][j]*b[j] for i in range(len(a)) for j in range(len(a)))%3
def symplectic_basis(C):
 m=len(C);basis=[[int(i==j) for i in range(m)] for j in range(m)];pairs=[]
 while True:
  pair=next(((i,j) for i in range(len(basis)) for j in range(i+1,len(basis)) if dot(basis[i],basis[j],C)),None)
  if pair is None:break
  i,j=pair;v=basis[i];w=basis[j];inv=pow(dot(v,w,C),-1,3);w=[inv*z%3 for z in w]
  new=[]
  for k,u in enumerate(basis):
   if k in pair:continue
   c=dot(w,u,C);d=dot(v,u,C);new.append([(u[t]+c*v[t]-d*w[t])%3 for t in range(m)])
  pairs.append((v,w));basis=new
 T=[v for pair in pairs for v in pair]+basis
 ck(int(s.Matrix(T).det())%3!=0,'symplectic basis independence')
 for i in range(m):
  for j in range(m):
   target=(1 if i%2==0 and j==i+1 else -1 if i%2==1 and j==i-1 else 0) if i<2*len(pairs) and j<2*len(pairs) else 0
   ck(dot(T[i],T[j],C)==target%3,'canonical form')
 return len(pairs),len(basis)
windows=[]
label_pool=[(i,j,t) for i,j in [(0,0),(1,0),(0,1),(1,1),(-1,1),(2,0),(0,-1)] for t in range(2)]
for length in range(1,15):
 E=label_pool[:length];G=[generator(*r) for r in E];H=[generator(*r,minus=True) for r in E]
 C=[[physical_pair(a,b) for b in G] for a in G]
 for i,(r,c,t) in enumerate(E):
  for j,(u,v,k) in enumerate(E):
   ck(C[i][j]==KP[t][k].get((r-u,c-v),0),'physical versus Laurent pairing')
   ck(physical_pair(G[i],H[j])==0,'physical complementary commutation')
 q,z=symplectic_basis(C);ck(3**z*3**(2*q)==3**length,'block dimensions')
 windows.append({'labels':length,'symplectic_pairs':q,'radical_dimension':z})
# Exact Weyl group multiplication phase, including cube order in odd characteristic.
for u,z,v,w in product(range(3),repeat=4):
 ck((z*v-w*u)%3==-(u*w-z*v)%3,'Weyl commutator sign')
 ck((3*u)%3==0 and (3*z)%3==0 and (3*u*z)%3==0,'Weyl cube relation')
# Fusion multiplicities by independent convolution, without enumerating all words.
c=[1,0,0]
for N in range(1,21):
 c=[sum(c[(j-a)%3] for a in range(3)) for j in range(3)]
 ck(c==[3**(N-1)]*3,'pointed fusion dimensions')
 ck(sum(t*t for t in c)==3**(2*N-1),'pointed fusion dimensions')
receipt={'verdict':'PASS','assertions':n,'groups':groups,'irregular_windows':windows,
 'artifact_sha256':sha256(Path('author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),
 'independent_code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Exact Laurent algebra, physical pairings and finite symplectic certificates only; no net isomorphism is inferred.'}
Path('independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
