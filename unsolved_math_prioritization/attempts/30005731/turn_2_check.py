"""Own exact algebraic controls for the conditional visible-prefix theorem."""
import json
import sympy as s
r,p,q,a,b,sigma=s.symbols('r p q a b sigma',real=True)
F=s.sqrt(r*r+p*p)
E=s.simplify(s.diff(F,r)-s.diff(s.diff(F,p),r)*p-s.diff(s.diff(F,p),p)*q)
assert s.simplify(E-r*(r*r+2*p*p-r*q)/F**3)==0
# Differentiate P*eta + integral E*eta: it is precisely F_r*eta+F_p*eta'.
P=s.diff(F,p)
assert s.simplify((s.diff(P,r)*p+s.diff(P,p)*q)*a+P*b+E*a-(s.diff(F,r)*a+s.diff(F,p)*b))==0
th=s.symbols('theta',real=True)
x=r*s.cos(th);y=r*s.sin(th)
D=lambda f:s.diff(f,th)+s.diff(f,r)*p+s.diff(f,p)*q
assert s.simplify(D(x)*D(D(y))-D(y)*D(D(x))-(r*r+2*p*p-r*q))==0
# The inactive straight-arc family and active logarithmic-spiral family are sanity checks only.
k=s.symbols('k',positive=True)
assert s.simplify((r*r+2*p*p-r*q).subs({p:r*k,q:r*k*k})-r*r*(1+k*k))==0
count=4
for R in range(1,8):
 for V in range(1,8):
  Q=s.Rational(R*R+2*V*V,R)+1
  ee=E.subs({r:R,p:V,q:Q})
  assert ee<0
  assert P.subs({r:R,p:V})<1
  count+=2
result={'status':'PASS','exact_assertions':count,'scope':'Conditional C2 strictly outward radially visible prefix length minimization. No winding-splice or global optimality claim.','core_identity':'dG/depsilon=(sigma-P)*eta-integral(E*eta); E<0 and eta>=0 imply every budget improves.'}
print(json.dumps(result,indent=2))
