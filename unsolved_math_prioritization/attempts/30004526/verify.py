from itertools import product,combinations_with_replacement
from pathlib import Path
from hashlib import sha256
import sympy as s,json
count=0;groups={}
def ck(v,g):
 global count
 assert bool(v),g
 count+=1;groups[g]=groups.get(g,0)+1
# Combinatorial identity is independent of geometric realizability of H.
for j in range(3,8):
 for interior in product(range(1,5),repeat=j-1):
  H=(1,)+interior+(1,);P=[sum(h>=t for h in H) for t in range(1,max(H)+1)]
  ck(sum(max(p-j+2,0) for p in P)==min(interior)+2,'conjugate rank identity')
# Differential inverse-system ranks over Q, with all partials represented exactly.
x,y,z,u,v,w=s.symbols('X Y Z U V W');V=(x,y,z,u,v,w)
def partials(F):
 seen={s.expand(F)};queue=list(seen)
 while queue:
  q=queue.pop()
  for a in V:
   p=s.expand(s.diff(q,a))
   if p!=0 and p not in seen:seen.add(p);queue.append(p)
 return list(seen)
def rank(polys):
 ps=[s.Poly(p,V) for p in polys if p!=0]
 if not ps:return 0
 mons=sorted(set().union(*(set(p.monoms()) for p in ps)))
 return s.Matrix([[p.coeff_monomial(m) for p in ps] for m in mons]).rank()
def apply(F,c,quadratic):
 out=sum(a*s.diff(F,b) for a,b in zip(c,V))
 for i,j,a in quadratic:out+=a*s.diff(F,V[i],V[j])
 return s.expand(out)
def hilbert(F,j):
 cur=[F];dims=[]
 for k in range(j+2):
  dims.append(rank(cur));cur=[s.diff(p,a) for p in cur for a in V if s.diff(p,a)!=0]
  # m^k image includes all higher partials.
  if cur:cur=list(set(q for p in cur for q in partials(p)))
 return [dims[i]-dims[i+1] for i in range(j+1)]
G3=x*u*u+y*u*v+z*v*v;G4=x*u**3+y*u*u*v+z*v**3
# Homogeneous Hilbert functions using exact-order derivative dimensions.
for G,j,expected in [(G3,3,[1,5,5,1]),(G4,4,[1,5,6,5,1])]:
 vals=[]
 for k in range(j+1):
  ds=[s.diff(G,*[V[i] for i in inds]) if inds else G for inds in combinations_with_replacement(range(6),k)]
  vals.append(rank(ds))
 ck(vals==expected,'homogeneous apolar Hilbert function')
 Hess=s.hessian(G,V);ck(Hess[:3,:3]==s.zeros(3),'Perazzo zero block');ck(Hess.subs(dict.fromkeys(V,1)).rank()==4,'Perazzo generic Hessian witness')
# Cases include lower-degree and extra-variable terms, and nonlinear ell.
cases=[(G3+w*w,3),(G3+x*x+y*w+w*w,3),(x**3+y**3+z**3+w*w,3),(G4,4),(G4+x**3+y*y*w+w*w,4),(G4+(x+y+z+w)**3+u*w,4)]
records=[]
for idx,(F,j) in enumerate(cases):
 G=s.Poly(F,V).homogeneous_component(j).as_expr() if hasattr(s.Poly(F,V),'homogeneous_component') else s.Add(*[term for term in s.expand(F).as_ordered_terms() if s.Poly(term,V).total_degree()==j])
 M=partials(F);length=rank(M)
 for c in [(1,1,1,1,1,1),(1,2,3,2,1,1)]:
  for nonlinear in [[],[(0,0,1),(3,4,-1)]]:
   q=F;ranks=[length]
   for k in range(1,j+2):q=apply(q,c,nonlinear);ranks.append(rank(partials(q)) if q!=0 else 0)
   ck(ranks[j]==1 and ranks[j+1]==0,'nonzero top power')
   d=s.hessian(G,V).subs(dict(zip(V,c))).rank()
   ck(ranks[j-2]==d+2,'nonlinear top-Hessian rank formula')
   ck(all(ranks[k]>=ranks[k+1] for k in range(j+1)),'nilpotent rank monotonicity')
   if j==3:ck(ranks[2:]==[2,1,0],'cubic higher powers')
   records.append({'case':idx,'linear_part':c,'nonlinear_terms':nonlinear,'ranks':ranks,'hessian_rank':d})
# Exact cubic H(1,6,5,1) example, including lower-order W².
ck(rank(partials(G3+w*w))==13,'cubic extended length')
# Coefficientwise rank-two block obstruction needs only linear algebra; deterministic controls.
for a,b,c,d,e,f in product(range(-1,2),repeat=6):
 C=s.Matrix([[a,b],[c,d],[e,f]]);D=s.Matrix([[1,2],[2,3]])
 H=s.zeros(5);H[:3,3:]=C;H[3:,:3]=C.T;H[3:,3:]=D
 ck(H.rank()<=4,'zero-block Hessian obstruction')
receipt={'verdict':'PASS','assertions':count,'groups':groups,'inverse_system_controls':records,'artifact_sha256':sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'sympy_version':s.__version__,'scope':'Exact rational finite diagnostics; no claim that tested Hilbert sequences are all realizable or that finite examples solve the general local question.'}
Path('verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='inverse_system_controls'}))
