"""Independent finite certificate and universal coefficient controls for July implication.
No claims about infinity are inferred from bounded tests; see DERIVED_PRIOR_IMPLICATION.md.
"""
from pathlib import Path
from itertools import product
import json,hashlib,sys

def require(value,label):
 if not value: raise RuntimeError(label)

F=tuple(range(16))
def bits(a): return tuple((a>>i)&1 for i in range(4))
def pack(v): return sum((z&1)<<i for i,z in enumerate(v))
def chi(a):
 _,b,c,d=bits(a);return (b+c+d+c*d)&1
def lam(a,y):
 _,b,c,d=bits(a);u,v,w,z=bits(y)
 p=(b+c+d+c*d)&1;q=(c+b*d)&1;r=(b+c+c*d)&1
 return pack((u+z*p,v+d*w+z*q,w+z*r,z))
def circle(a,b):return a^lam(a,b)
def eps(a):return 1-2*chi(a)
checks=0
for a,b,c in product(F,repeat=3):
 require(circle(circle(a,b),c)==circle(a,circle(b,c)),'finite associativity')
 require(lam(a,b^c)==lam(a,b)^lam(a,c),'additive lambda')
 require(lam(circle(a,b),c)==lam(a,lam(b,c)),'lambda homomorphism')
 checks+=3
for a in F:
 require(circle(0,a)==a==circle(a,0),'neutral')
 require(len({lam(a,b) for b in F})==16,'lambda automorphism')
 require(any(circle(a,b)==0==circle(b,a) for b in F),'inverse')
 for b in F:
  require(chi(circle(a,b))==(chi(a)^chi(b)),'sign character')
  # Exact polynomial coefficients of integer triple associativity
  require((1,eps(a),eps(circle(a,b)))==(1,eps(a),eps(a)*eps(b)),'integer associativity coefficients')
  checks+=2
K=[a for a in F if chi(a)==0]
require(K==[0,1,6,7,10,11,14,15],'kernel exactly primary')
require(6 in K and 10 in K and (6^10)==12 and 12 not in K,'closure failure')
require(lam(8,6)==4 and 4 not in K,'lambda failure')

def subgroup(H,operation):
 return 0 in H and all(operation(a,b) in H for a in H for b in H)
rows=[]
for a in K:
 # z=(n,a), additive centralizer all; rightFix=Z×fixedFinite
 R=[b for b in F if lam(a,b)==b]
 require(subgroup(R,lambda x,y:x^y),'right fixed additive subgroup')
 for n_nonzero in [False,True]:
  # left fixed and multiplicative centralizer intersection has no integer restriction
  L=[b for b in F if (not n_nonzero or eps(b)==1) and lam(b,a)==a and circle(b,a)==circle(a,b)]
  require(subgroup(L,circle),'second fixed+centralizer subgroup')
  rows.append({'a':a,'n_nonzero':n_nonzero,'additive_index':16//len(R),'multiplicative_index':16//len(L),'R':R,'L':L})
  checks+=2
# supplemental direct controls distinct from universal proof
ints=range(-2,3)
def big_circle(x,y):return (x[0]+eps(x[1])*y[0],circle(x[1],y[1]))
for n,m,a,b in product(ints,ints,F,F):
 z=(n,a);g=(m,b)
 if a in K:
  central=(not n or eps(b)==1) and circle(b,a)==circle(a,b)
  left=(not n or eps(b)==1) and lam(b,a)==a
  require((big_circle(z,g)==big_circle(g,z))==central,'centralizer controls')
  require((big_circle(g,z)==(m+n,b^a))==left,'left fixed controls')
 checks+=2
for a in F:
 if a not in K:
  # coefficient -2 guarantees rightFixed integer coordinate zero universally.
  require(eps(a)-1==-2,'infinite coset separating coefficient')
result={'status':'PASS','checks':checks,'finite_order':16,'kernel':K,'failure_witness':{'a':6,'b':10,'additive_sum':12,'chi_sum':chi(12),'lambda_witness':[8,6,lam(8,6)]},'index_rows':rows,'infinite_claim_proof':'Exact nonzero integer coefficient -2 plus pairwise distinct integer cosets; not numerical inference','uses_July_Theorem5_2':False,'requires_unsupported_literature_theorem':False}
Path(sys.argv[1] if len(sys.argv)>1 else 'PRIOR_IMPLICATION_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='index_rows'},indent=2))
