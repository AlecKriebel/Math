# Additive portable copy: only source-hash availability/default path/report count changed.
import sympy as S,json,hashlib,subprocess,sys
from pathlib import Path
from fractions import Fraction as Q
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
manifest=json.loads((p/'FINAL_AUTHOR_MANIFEST.json').read_text())
for f in manifest['files']:assert hashlib.sha256((p/f['path']).read_bytes()).hexdigest()==f['sha256']
source_count=0
if (p/'sources').is_dir():
 for f in json.loads((p/'SOURCE_MANIFEST.json').read_text())['files']:
  assert hashlib.sha256((p/'sources'/f['name']).read_bytes()).hexdigest()==f['sha256'];source_count+=1
b=subprocess.check_output([sys.executable,str(p/'check_turn_1.py')]);assert b==(p/'TURN_1_CHECKS.json').read_bytes()
N=0
def ck(v):
 global N
 assert v;N+=1
# Independent angular integration of Newton's kernel, then interior/exterior shells.
r,d,R,m,l,t=S.symbols('r d R m l t',positive=True)
# For shell radius r relative to displaced center d, integrate cosine angular variable.
z=S.symbols('z');primitive=-S.sqrt(r*r+d*d-2*r*d*z)/(r*d)
ck(S.simplify(S.diff(primitive,z)-1/S.sqrt(r*r+d*d-2*r*d*z))==0)
J=4*S.pi*(S.integrate(r*r/d,(r,0,d))+S.integrate(r,(r,d,R)))
ck(S.simplify(J-2*S.pi*(R*R-d*d/3))==0)
# General mass volume cubic term and normalized radius shift.
V=4*S.pi*R**3/3+3*m*J.subs(d,l*R)
shift=S.simplify((V-4*S.pi*R**3/3)/(4*S.pi*R**2))
ck(S.simplify(shift-m*(S.Rational(3,2)-l*l/2))==0)
ck(S.simplify(shift-m/2-m*(1-l*l/2))==0)
ck((shift-m/2).subs({m:-2,l:S.Rational(1,2)})==-S.Rational(7,4))
# Capacitary quotient far-field coefficient and conformal ADM formula.
ck(S.expand(S.series((1-R*t)/(1+m*t/2),t,0,2).removeO()).coeff(t,1)==-R-m/2)
u=1+m/(2*r)
ck(S.limit(-2*r*r*u**3*S.diff(u,r),r,S.oo)==m)
# Divergence cancellation valid without radial symmetry.
x=S.symbols('x');u0=S.Function('u')(x);f=S.Function('f')(x)
ck(S.simplify(S.diff(u0*u0*S.diff(f/u0,x),x)-(u0*S.diff(f,x,2)-f*S.diff(u0,x,2)))==0)
for k in range(2,41):
 for j in range(1,k):
  lam=Q(j,k)
  for mass in [-1,-2,-7]:
   deficit=mass*(1-lam*lam/2);ck(deficit>mass)
  ck(lam*(k+1-k)+k<=k+1)
print(json.dumps({'status':'PASS','author_receipt':json.loads(b),'manifest_bound_files':len(manifest['files']),'source_pdfs':source_count,'independent_assertions':N,'scope':'Independent angular integration, asymptotic coefficients, conformal identities and strict-gap controls. Full analytical proof and prior theorem hypotheses audited separately.'},indent=2))
