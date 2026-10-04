#!/usr/bin/env python3
# Public export: optimization must not disable scientific assertions.
import sys
if sys.flags.optimize:
    raise SystemExit("Verification refuses Python optimization (-O/-OO).")
from datetime import datetime, timezone
print("native_utc", datetime.now(timezone.utc).isoformat())
import sympy as s
print("sympy", s.__version__)
u,v,k,t,L,q,z,a,b=s.symbols("u v k t L q z a b")
def red(expr):
    num,den=s.fraction(s.cancel(expr))
    num=s.rem(s.Poly(num,k),s.Poly(k*k-k-1,k)).as_expr()
    den=s.rem(s.Poly(den,k),s.Poly(k*k-k-1,k)).as_expr()
    return s.factor(num/den)
P=s.resultant(t**5-1,v*t*t-k*t+u,t).expand()
print("pentagon_side_resultant",P)
assert s.expand(P-(u**5+v**5-k**5+5*k**3*u*v-5*k*u**2*v**2))==0
print("circle_restriction", red(P.subs(v,1/u)))
F=u**5+v**5-k**5+5*k**3*u*v-5*k*u**2*v**2+L*(u*v-1)**2
# At a vertex, use u=u0(1+a),v=v0(1+b),u0^5=v0^5=-1,u0v0=1.
local=-(1+a)**5-(1+b)**5-k**5+5*k**3*(1+a)*(1+b)-5*k*((1+a)*(1+b))**2+L*((1+a)*(1+b)-1)**2
local=s.Poly(s.expand(local),a,b)
parts={j:red(sum(c*a**i[0]*b**i[1] for i,c in local.terms() if sum(i)==j)) for j in range(6)}
print("vertex_local_parts",parts)
assert parts[0]==parts[1]==0
Q=parts[2]
disc=red(s.Poly(Q,a,b).coeff_monomial(a*b)**2-4*s.Poly(Q,a,b).coeff_monomial(a*a)*s.Poly(Q,a,b).coeff_monomial(b*b))
print("vertex_node_discriminant",disc)
D=L-5*k; A=5*k**3-2*L; E=L-k**5
sing=red(D*q*q+3*A*q+5*E)
print("nonzero_singular_radial_condition",sing)
q2=5*E/D
obstruction=red((2*D*q2+A)**2-25*q2**3)
print("additional_nonzero_singular_obstruction",obstruction)
print("obstruction_radical_factored",s.factor(obstruction.subs(k,(1+s.sqrt(5))/2),extension=s.sqrt(5)))
print("origin_on_curve",red(F.subs({u:0,v:0})))
print("origin_quadratic_at_center_parameter",red((5*k**3-2*L).subs(L,k**5)))
Lnode=5*k+s.Rational(15,4)
print("nodeexception_tangent_quadratic",red(Q.subs(L,Lnode)))
print("nodeexception_tangent_restriction",red(local.as_expr().subs({b:a,L:Lnode})))
print("nodeexception_whole_quintic_factor",s.factor(F.subs({L:Lnode,k:(1+s.sqrt(5))/2}),extension=s.sqrt(5)))
print("zero_parameter_factor_structure", "original product of five side lines by resultant")
print("infinity_restriction",u**5+v**5)
print("infinity_gradient",5*u**4,5*v**4)
print("PASS: resultant and vertex singularity identities")
