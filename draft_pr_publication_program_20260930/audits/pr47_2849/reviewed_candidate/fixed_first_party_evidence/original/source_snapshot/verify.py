"""Exact diagnostics only; this does not compute instanton Floer homology."""
import itertools,json,math
from pathlib import Path
import sympy as s
checks=[]
def check(label,v):
    assert bool(v),label
    checks.append(label)
t=s.symbols('t');D=t*t-t+1
check('trefoil Alexander polynomial is Phi_6',s.expand(D-s.cyclotomic_poly(6,t))==0)
check('unmodified sixth-root test fails',s.degree(s.gcd(D,t**6-1),t)==2)
check('squared sixth-root test succeeds',s.gcd(D.subs(t,t*t),t**6-1)==1)
check('third-root test succeeds',s.gcd(D,t**3-1)==1)
check('torus Alexander formula reduces correctly',s.cancel(((t**6-1)*(t-1))/((t**2-1)*(t**3-1)))==D)
# The cellular chain complex for the lower link T^2 has ranks (1,2,1)
# and zero cellular boundaries. The cone relative punctured cone is shifted
# reduced homology. Geometry identifying the lower link is proved in the text.
local={0:0,1:0,2:2,3:1,4:0}
check('local critical rank three',sum(local.values())==3)
check('local Euler characteristic one',sum((-1)**k*v for k,v in local.items())==1)
u,v,w,z=s.symbols('u v w z',real=True);x=u*u+v*v;y=w*w+z*z;f=(x-y)*(x-2*y)
g=[s.diff(f,a) for a in (u,v,w,z)]
expected=[2*u*(2*x-3*y),2*v*(2*x-3*y),2*w*(-3*x+4*y),2*z*(-3*x+4*y)]
for i in range(4):check('exact gradient coordinate '+str(i),s.expand(g[i]-expected[i])==0)
check('zero Hessian at origin',s.hessian(f,(u,v,w,z)).subs({u:0,v:0,w:0,z:0})==s.zeros(4))
check('mixed critical equations invertible',s.Matrix([[2,-3],[-3,4]]).det()==-1)
# Rational rotations independently in both complex coordinates give exact symmetry checks.
for a,b in [(s.Rational(3,5),s.Rational(4,5)),(s.Rational(5,13),s.Rational(12,13)),(0,1)]:
    rotated=f.subs({u:a*u-b*v,v:b*u+a*v,w:a*w-b*z,z:b*w+a*z}, simultaneous=True)
    check('circle invariance at '+str((a,b)),s.expand(rotated-f)==0)
q=s.symbols('q',real=True)
check('lower link polynomial',s.expand(f.subs({u:s.sqrt(q),v:0,w:s.sqrt(1-q),z:0})-(2*q-1)*(3*q-2))==0)
check('lower link roots',s.solve((2*q-1)*(3*q-2),q)==[s.Rational(1,2),s.Rational(2,3)])
for a in range(1,13):
 for b in range(1,9):
    chars=list(itertools.product(range(a),range(b)));seen=set();central=0;spheres=0
    for c in chars:
      if c in seen:continue
      inv=((-c[0])%a,(-c[1])%b);seen.update((c,inv))
      if c==inv:central+=1
      else:spheres+=1
    check('abelian orbit count '+str((a,b)),central+2*spheres==a*b and central==math.gcd(a,2)*math.gcd(b,2))
out={'passed':True,'assertions':len(checks),'scope':'Exact polynomial, circle-symmetry, lower-link cellular-homology arithmetic, and finite-character-orbit diagnostics. No 3-manifold Floer computation or proof of KP-3.51.','local_critical_groups':local,'trefoil_gcd_unsquared':str(s.gcd(D,t**6-1)),'trefoil_gcd_squared':str(s.gcd(D.subs(t,t*t),t**6-1)),'checks':checks}
p=Path(__file__).with_name('verification.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
