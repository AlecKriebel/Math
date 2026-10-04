"""Exact checks for the old explicit family. Standard library only; no numeric orbits."""
from math import comb
from pathlib import Path
import json,datetime,hashlib
D=Path(__file__).resolve().parent

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def sub(a,b):return add(a,neg(b))
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return (a[0],-a[1])
def power(a,n):
 r=(1,0)
 for _ in range(n):r=mul(r,a)
 return r
Z=(0,0); ONE=(1,0); I=(0,1)
P={'1':(ONE,ONE),'-1':(neg(ONE),ONE),'0':(Z,ONE),'infinity':(ONE,Z),'i':(I,ONE),'-i':(neg(I),ONE)}
def eq(a,b):return mul(a[0],b[1])==mul(a[1],b[0])
def f(p,d,coefficient=I):
 X,Y=p;return mul(coefficient,power(sub(X,Y),d)),power(add(X,Y),d)
def t(p):return neg(p[1]),p[0]
def c(p):return conj(p[0]),conj(p[1])
def a(p):return t(c(p))
def poly_prod(p,q):
 out=[Z]*(len(p)+len(q)-1)
 for j,x in enumerate(p):
  for k,y in enumerate(q):out[j+k]=add(out[j+k],mul(x,y))
 return out

def poly_sub(p,q):
 return [sub(p[j] if j<len(p) else Z,q[j] if j<len(q) else Z) for j in range(max(len(p),len(q)))]
def derivative(p):return [mul((j,0),p[j]) for j in range(1,len(p))]
def binom_poly(n,sgn):return [(comb(n,j)*(sgn**(n-j)),0) for j in range(n+1)]
def w_check(d,coefficient=I):
 F=[mul(coefficient,x) for x in binom_poly(d,-1)];G=binom_poly(d,1)
 actual=poly_sub(poly_prod(derivative(F),G),poly_prod(F,derivative(G)))
 expected=[mul(mul((2*d,0),coefficient),x) for x in poly_prod(binom_poly(d-1,-1),binom_poly(d-1,1))]
 while actual and actual[-1]==Z:actual.pop()
 return actual==expected,actual

def named(q):
 found=[name for name,p in P.items() if eq(q,p)]
 if len(found)!=1:raise ValueError(f'Not exactly one known point: {q}, {found}')
 return found[0]
rows=[]
for d in [3,5,7,9,11,13,15]:
 expected={'1':'0','0':'-i','-1':'infinity','infinity':'i','i':'1' if d%4==3 else '-1','-i':'-1' if d%4==3 else '1'}
 mapping={name:named(f(p,d)) for name,p in P.items()}
 if mapping!=expected:raise AssertionError((d,mapping,expected))
 wronskian_ok,W=w_check(d)
 if not wronskian_ok:raise AssertionError(('W',d))
 # Finite set contains both critical points and each lies on a cycle; closure is exact.
 periods={}
 for critical in ['1','-1']:
  q=expected[critical];steps=1
  while q!=critical and steps<=6:q=expected[q];steps+=1
  if q!=critical:raise AssertionError(('critical_not_periodic',d))
  periods[critical]=steps
 # Compare rational identities by exact coefficients in homogeneous forms.
 # T f T has coordinates -(-X+Y)^d, i(-Y-X)^d; bar(f) has -i(X-Y)^d,(X+Y)^d.
 # Their cross difference is identically zero precisely when d is odd.
 # direct symbolic factor check below independent of this rearrangement
 FT=[neg(x) for x in binom_poly(d,-1)] # -G(T(X,Y)) = -(X-Y)^d
 GT=[mul(I,(((-1)**d)*x[0],0)) for x in binom_poly(d,1)] # F(T)=i(-X-Y)^d
 Fc=[mul(neg(I),x) for x in binom_poly(d,-1)];Gc=binom_poly(d,1)
 cross=poly_sub(poly_prod(FT,Gc),poly_prod(Fc,GT))
 if any(x!=Z for x in cross):raise AssertionError(('T_conjugation_identity',d))
 for name,p in P.items():
  if not eq(f(a(p),d),a(f(p,d))):raise AssertionError(('A_commuting',d,name))
 if eq(t(f(P['infinity'],d)),f(t(P['infinity']),d)):raise AssertionError(('T_should_fail',d))
 rows.append({'d':d,'map':mapping,'critical_periods':periods,'postcritical_count':6,'wronskian_degree':len(W)-1,'exact_wronskian_verified':True,'conjugation_identity_polynomial_verified':True,'A_commutes_on_S':True,'T_holomorphic_fails_at_infinity':True})
controls=[]
# Even-degree mutation must fail the odd-degree conjugation/descent certificate.
for d in [2,4,6]:
 if any(not eq(f(a(p),d),a(f(p,d))) for p in P.values()):
  controls.append({'name':f'even_degree_{d}','certificate_rejected':True,'reason':'A commuting identity fails (at critical orbit data).','T_is_holomorphic_automorphism_on_S':all(eq(f(t(p),d),t(f(p,d))) for p in P.values())})
 else:raise AssertionError(('even_mutant_survived',d))
# Removing i makes the map real, so the fixed-point-free obstruction must not pass.
if all(eq(f(c(p),3,ONE),c(f(p,3,ONE))) for p in P.values()) and all(eq(f(t(p),3,ONE),t(f(p,3,ONE))) for p in P.values()):
 controls.append({'name':'real_coefficient_mutation','certificate_rejected':True,'reason':'complex conjugation itself commutes and T is a nontrivial holomorphic automorphism, so the pseudo-real certificate fails.','real_positive_control':True})
else:raise AssertionError('real control failed')
# Wrongly assert critically fixed instead of PCF: rejection on an actual critical point.
if not eq(f(P['1'],3),P['1']):controls.append({'name':'critically_fixed_claim_mutation','certificate_rejected':True,'reason':'1 maps to 0, so old cubic is PCF but is not critically fixed.'})
else:raise AssertionError('critically-fixed mutant survived')
# Corrupt the cubic orbit row and reject against actual evaluation.
mutated={'1':'0','0':'-i','-1':'infinity','infinity':'i','i':'-1','-i':'-1'}
actual={name:named(f(p,3)) for name,p in P.items()}
if actual!=mutated:controls.append({'name':'orbit_endpoint_mutation','certificate_rejected':True,'first_bad_key':next(k for k in actual if actual[k]!=mutated[k])})
else:raise AssertionError('orbit mutant survived')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','method':'exact Gaussian-integer homogeneous evaluation and exact integer polynomial identities; no floating point','degrees_checked':rows,'actual_controls':controls,'all_controls_rejected':all(x['certificate_rejected'] for x in controls),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limitations':'Finite checks corroborate the displayed proof. All odd degrees are proved by the two residue classes modulo4 in the proof; no finite-degree sweep substitutes for it. All no-real-model steps are proved in prose.'}
(D/'SILVERMAN_EXACT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
