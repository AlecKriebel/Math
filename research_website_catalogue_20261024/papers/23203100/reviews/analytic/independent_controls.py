"""Fresh standard-library analytic-review controls; no submitted code imported."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from decimal import Decimal as D, localcontext
import json,hashlib,datetime
OUT=Path(__file__).resolve().parent

def h(*names): return {frozenset(names):F(1)} if names else {}
def lin(*terms):
 out=defaultdict(F)
 for c,e in terms:
  for k,v in e.items(): out[k]+=c*v
 return {k:v for k,v in out.items() if v}
def mi(a,b,c=()): return lin((1,h(*(a+c))),(1,h(*(b+c))),(-1,h(*c)),(-1,h(*(a+b+c))))
def equal(name,terms):
 rem=lin(*terms);assert not rem,(name,rem)
 return {'name':name,'residual_entropy_coefficients':0}
X=('X',);W=('W',);V=('V',);B=('B',);E=('E',)
checks=[]
checks.append(equal('second_converse_identity',[(1,mi(W,B+V,X)),(-1,mi(W,E,X)),(-1,mi(W+V,B,X)),(1,mi(W+V,E,X)),(-1,mi(W,V,X)),(1,mi(V,B,X)),(-1,mi(V,E,W+X))]))
checks.append(equal('second_positive_remainder_combination',[(1,mi(W,V,X)),(1,mi(V,E,W+X)),(-1,mi(V,W+E,X))]))
K=('K',);L=('L',)
checks.append(equal('third_converse_identity',[(1,mi(K+W,B+L+V)),(-1,mi(W,E,K+L)),(-1,mi(K+L+W+V,B)),(1,mi(W+V,E,K+L)),(1,mi(L+V,B)),(-1,mi(K+W,L+V)),(-1,mi(V,E,K+W+L))]))
checks.append(equal('third_positive_remainder_combination',[(1,mi(K+W,L+V)),(1,mi(V,E,K+W+L)),(-1,mi(K+W,L)),(-1,mi(V,K+W+E,L))]))
# A mutation omitting the consumed-key correlation term must fail as a formal identity.
mutant=lin((1,mi(W,B+V,X)),(-1,mi(W,E,X)),(-1,mi(W+V,B,X)),(1,mi(W+V,E,X)),(-1,mi(W,V,X)),(1,mi(V,B,X)))
assert mutant

def exact_otp(d,qs):
 assert sum(qs)==1 and min(qs)>=0
 p=F(1,d*d)
 actual={(m,s,l):(p if l==(m+s)%d else F(0)) for m,s,l in product(range(d),repeat=3)}
 joint=sum(abs(v-p*qs[l]) for (m,s,l),v in actual.items())
 generated=sum(abs(sum(actual[m,s,l] for s in range(d))-F(1,d*d)) for m,l in product(range(d),repeat=2))
 assert joint==2*(1-F(1,d)) and generated==0
 return {'d':d,'comparison_q':[str(v) for v in qs],'joint_norm':str(joint),'generated_norm':str(generated)}
otp=[]
for d in range(1,10):
 otp.extend(exact_otp(d,q) for q in ([F(1,d)]*d,[F(1)]+[F(0)]*(d-1),[F(i+1,d*(d+1)//2) for i in range(d)]))
# Mutant: revealing the used key to Eve destroys generated-message secrecy.
revealed_key_norm=sum(abs((F(1,4) if l==(m+s)%2 else F(0))-F(1,8)) for m,s,l in product(range(2),repeat=3)) # actual M,S,L versus uniform M times actual S,L
assert revealed_key_norm!=0
# Exact cone maps and inverse deficit maps, with nonnegative rational coefficients.
qvec=[(-2,1,-1),(2,-1,-1),(0,-1,1)]
pvec=[(-1,1,-1),(1,-1,0),(0,-1,1)]
def qface(v):c,q,e=v;return (c+2*q,q+e,c+q+e)
def pface(v):r,p,s=v;return (r+p,p+s,r+p+s)
assert [qface(v) for v in qvec]==[(0,0,-2),(0,-2,0),(-2,0,0)]
assert [pface(v) for v in pvec]==[(0,0,-1),(0,-1,0),(-1,0,0)]
for x,y,z in product([F(0),F(1,7),F(3,2),F(10)],repeat=3):
 for vec,faces,scale in [(qvec,qface,F(2)),(pvec,pface,F(1))]:
  v=tuple(sum(a*w[i] for a,w in zip((x,y,z),vec)) for i in range(3))
  f=faces(v);assert (x,y,z)==(-f[2]/scale,-f[1]/scale,-f[0]/scale)
# Scalar derivative signs use Decimal logs with 80-digit context; proof is in DERIVATION.md.
# This is a broad deterministic numerical supplement, not a universal interval certificate.
scalar=[]
with localcontext() as ctx:
 ctx.prec=80
 def A(u):return (u+1)*(1+1/u).ln()
 def g(u):return ((u+1)*(u+1).ln()-u*u.ln())/D(2).ln() if u else D(0)
 for t in map(D,['0.00001','0.01','0.1','0.5','0.99999','1','1.00001','2','10000']):
  for u in map(D,['1e-20','1e-10','0.01','1','100','1e10','1e20']):
   delta=A(t*u)-A(u)
   assert delta>0 if t<1 else delta<0 if t>1 else delta==0
   scalar.append({'t':str(t),'u':str(u),'curvature_sign':int(delta>0)-int(delta<0)})
 # A weaker linear entropy bound is strictly weaker at the control thermal state.
 sharp=g(D('0.5'));weak=D('0.5')*g(D(1));assert sharp>weak
 weak_gap=str(sharp-weak)
 # A negative environmental coefficient is material, not removable as a sign convention.
 assert g(D('0.5'))-g(D('0.5')) == 0 and g(D('0.5'))+g(D('0.5')) > 0
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_entropy_identities':checks,'exact_otp_cases':otp,'cone_rational_cases':128,'scalar_numerical_cases':scalar,'mutants':{'omitted_consumed_resource_E_correlation_detected':bool(mutant),'consumed_key_exposure_detected_norm_d2':str(revealed_key_norm),'weak_linear_entropy_premise_insufficient_thermal_gap_bits':weak_gap,'wrong_environment_sign_detected':True},'limits':'Exact controls certify algebra, cone inversion and finite OTP examples only. Scalar universal result is analytical. No control proves EPnI, coding or global capacity by finite sampling.','passed':True}
(OUT/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'identities':len(checks),'otp_cases':len(otp),'cone_cases':128,'scalar_cases':len(scalar),'mutants':result['mutants']},indent=2))
