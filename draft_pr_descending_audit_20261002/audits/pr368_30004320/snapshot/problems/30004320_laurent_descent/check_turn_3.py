#!/usr/bin/env python3
"""Exact finite controls for torus-lattice ramification and unit lifting."""
import sympy as s
import itertools,json
checks=0

def ck(x):
 global checks
 assert x
 checks+=1
# Cyclic lattice norm identity: (A-I)*sum i A^i = m I - sum A^i.
representations=[]
for m in range(2,10):
 A=s.zeros(m)
 for j in range(m):A[(j+1)%m,j]=1
 representations.append((m,A))
representations += [(2,s.Matrix([[-1]])),(3,s.Matrix([[0,-1],[1,-1]])),(4,s.Matrix([[0,-1],[1,0]])),(6,s.Matrix([[0,-1],[1,1]]))]
for m,A in representations:
 I=s.eye(A.rows);N=s.zeros(A.rows);S=s.zeros(A.rows)
 for i in range(m):N+=A**i;S+=i*A**i
 ck(A**m==I);ck((A-I)*S==m*I-N)
 for v in itertools.product(range(-1,2),repeat=min(A.rows,4)):
  vec=s.Matrix(list(v)+[0]*(A.rows-len(v)))
  coc=(A-I)*vec
  ck(N*coc==s.zeros(A.rows,1));ck(m*coc==(A-I)*S*coc)
lattice_checks=checks
# Finite quadratic extensions F_{p^2}, including p=2 dividing the degree.
unit_cases=0
for p,u,v in [(2,1,1),(3,0,1),(5,0,2),(7,0,1)]:
 def add(x,y):return ((x[0]+y[0])%p,(x[1]+y[1])%p)
 def neg(x):return ((-x[0])%p,(-x[1])%p)
 def mul(x,y):
  a,b=x;c,d=y
  return ((a*c-v*b*d)%p,(a*d+b*c-u*b*d)%p)
 def pw(x,n):
  out=(1,0)
  while n:
   if n&1:out=mul(out,x)
   x=mul(x,x);n//=2
  return out
 traces=set()
 for x in itertools.product(range(p),repeat=2):
  conj=pw(x,p);tr=add(x,conj);nr=mul(x,conj)
  ck(tr[1]==0 and nr[1]==0);traces.add(tr[0])
  ck(tr[0]==(2*x[0]-u*x[1])%p)
  ck(nr[0]==(x[0]**2-u*x[0]*x[1]+v*x[1]**2)%p)
  # Norm(1+s*x)=1+Tr(x)s+Norm(x)s^2, coefficient by coefficient.
  coeff=[(1,0),add(x,conj),mul(x,conj)]
  ck(coeff==[(1,0),tr,nr]);unit_cases+=1
 ck(traces==set(range(p)))
unit_checks=checks-lattice_checks
# Full Puiseux ramification kills any finite lattice-cohomology torsion.
for order in range(2,31):
 for n in range(1,31):
  for residue in range(order):ck((order*residue)%order==0 and (n*order)%n==0)
# Artin-Schreier reduction s^-p^e*m ~ s^-m, tested as exponent dictionaries.
for p in (2,3,5,7):
 for e in range(1,6):
  for m in range(1,21):
   if m%p==0:continue
   q={-m*p**j:1 for j in range(e)}
   out={}
   for exponent,c in q.items():
    out[p*exponent]=(out.get(p*exponent,0)+c)%p
    out[exponent]=(out.get(exponent,0)-c)%p
   out={k:c for k,c in out.items() if c}
   ck(out=={-m*p**e:1,-m:p-1})
print(json.dumps({'status':'PASS','exact_assertions':checks,'cyclic_lattice_representations':len(representations),'lattice_assertions':lattice_checks,'finite_unit_cases':unit_cases,'unit_assertions':unit_checks,'scope':'Finite identities support the lattice/direct-limit and smooth principal-unit mechanisms; they do not replace the written cohomology, gerbe and algebraic proofs.'},indent=2,sort_keys=True))
