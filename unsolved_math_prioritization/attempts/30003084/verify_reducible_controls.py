"""Own exact controls for reducible-cubic residual laws and bounded witnesses."""
import sympy as s
from itertools import combinations,product
from collections import Counter
import json
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
alpha,beta,gamma,delta,eps,phi,t=s.symbols('alpha beta gamma delta eps phi t')
def Q(x,y,z):return s.expand(alpha*x*x+beta*y*y+gamma*z*z+delta*x*y+eps*x*z+phi*y*z)
# Triangle: products of roots on three carriers multiply to one.
Ps=[s.Poly(Q(0,1,t),t),s.Poly(Q(t,0,1),t),s.Poly(Q(1,t,0),t)]
ck(s.simplify(s.prod(p.nth(0)/p.nth(2) for p in Ps))==1,'triangle_product')
Ps=[s.Poly(Q(0,1,-t),t),s.Poly(Q(1,0,-t),t),s.Poly(Q(1,1,t),t)]
ck(s.simplify(sum(-p.nth(1)/p.nth(2) for p in Ps))==0,'concurrent_sum')
P=s.Poly(s.expand(t*t*Q(t,1/t,1)),t);L=s.Poly(Q(t,1,0),t)
ck(s.simplify(P.nth(0)/P.nth(4)-L.nth(0)/L.nth(2))==0,'secant_product')
P=s.Poly(Q(t,t*t,1),t);L=s.Poly(Q(1,t,0),t)
ck(s.simplify(-P.nth(3)/P.nth(4)+L.nth(1)/L.nth(2))==0,'tangent_sum')
q,F,G,S,T,d,e,f,K=s.symbols('q F G S T d e f K',nonzero=True)
expr=lambda x:q*x*(F-S-x)-K*(G-T-1/x)
ck(s.simplify(expr(d)-expr(e)-(d-e)*(q*(F-S-d-e)-K/(d*e)))==0,'two_deletion_subtraction')
val=lambda x,y:x+y+K/(q*x*y)
ck(s.factor(val(d,e)-val(d,f))==(e-f)*(q*d*e*f-K)/(q*d*e*f),'two_deletion_four_value_obstruction')
for m in range(3,41):
 pairs={ (a+b)%m for a in range(m) for b in range(m) if a!=b}
 ck(pairs==set(range(m)),'distinct_pair_products_exhaust_cyclic_group')
 for target in range(m):
  found=next(((a,b,c,d) for a in range(m) for b in range(m) if a!=b for c in range(m) for d in range(m) if c!=d and (a+b+c+d)%m==target),None)
  ck(found is not None,'coset_double_pair_tangency')
# Fixed explicit component configurations. Search stops at the first verified
# five-point conic; no sampling result is used in the universal proof.
def normalize(p):
 p=tuple(map(s.Rational,p));v=next(x for x in p if x);return tuple(x/v for x in p)
def witness(name,pts):
 pts=list(dict.fromkeys(normalize(p) for p in pts));V=s.Matrix([[x*x,y*y,z*z,x*y,x*z,y*z] for x,y,z in pts])
 ck(V.rank()==6,'nonconic_configuration')
 for ids in combinations(range(len(pts)),5):
  M=V[list(ids),:]
  if M.rank()!=5:continue
  z=M.nullspace()[0];sup=[i for i in range(len(pts)) if (V[i,:]*z)[0]==0]
  if len(sup)==5:
   ck(set(sup)==set(ids),'ordinary_witness_support')
   return {'name':name,'points':[[str(x) for x in p] for p in pts],'indices':sup,'conic_coefficients':[str(x) for x in z]}
 raise AssertionError(name)
configs=[]
configs.append(witness('triangle_with_vertices',[(0,1,a) for a in [1,2,3,4]]+[(b,0,1) for b in [1,2,3]]+[(1,c,0) for c in [1,2,3]]+[(1,0,0),(0,1,0),(0,0,1)]))
configs.append(witness('triangle_singleton_branches',[(0,1,a) for a in range(1,9)]+[(1,0,1),(1,1,0),(1,0,0)]))
configs.append(witness('concurrent_with_vertex',[(0,1,-a) for a in [0,1,2,3]]+[(1,0,-b) for b in [0,1,2,3]]+[(1,1,c) for c in [0,1,2]]+[(0,0,1)]))
configs.append(witness('secant_conic_and_line',[(t,s.Rational(1,t),1) for t in range(1,7)]+[(u,1,0) for u in range(1,5)]+[(1,0,0),(0,1,0)]))
configs.append(witness('tangent_conic_and_line',[(t,t*t,1) for t in range(6)]+[(1,u,0) for u in range(5)]+[(0,1,0)]))
configs.append(witness('large_line',[(t,0,1) for t in range(8)]+[(0,1,1),(1,1,1),(0,2,1),(2,3,1)]))
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'fixed_witnesses':configs,'scope':'Symbolic residual laws, finite cyclic controls, and six explicit rational configurations; no general configuration census.'},indent=2,sort_keys=True))
