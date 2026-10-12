#!/usr/bin/env python3
# Public export: optimization must not disable scientific assertions.
import sys
if sys.flags.optimize:
    raise SystemExit("Verification refuses Python optimization (-O/-OO).")
from datetime import datetime,timezone
print("native_utc",datetime.now(timezone.utc).isoformat())
import sympy as s
print("sympy",s.__version__)
k,L,q=s.symbols("k L q")
def red(expr):
    expr=s.cancel(expr)
    a,b=s.fraction(expr)
    return s.factor(s.rem(s.Poly(a,k),s.Poly(k*k-k-1,k)).as_expr()/s.rem(s.Poly(b,k),s.Poly(k*k-k-1,k)).as_expr())
D=L-5*k; A=5*k**3-2*L; E=L-k**5
G=red((D*q*q+A*q+E)**2-4*q**5)
H,remainder=s.div(G,(q-1)**2,q)
print("quotient_remainder",s.factor(remainder))
assert s.factor(remainder)==0
H=red(H)
print("quotient_cubic",H)
disc=red(s.discriminant(H,q))
print("quotient_cubic_discriminant",s.factor(disc.subs(k,(1+s.sqrt(5))/2),extension=s.sqrt(5)))
print("quotient_cubic_at_vertex_cusp",s.factor(red(H.subs(L,5*k+s.Rational(15,4)))))
print("regular_alternate_line_resultant_parameter",red(5*k+5*(1-k)))
# Check second product-of-lines fibre against the same resultant formula with k replaced by 1-k.
u,v=s.symbols("u v")
F=u**5+v**5-k**5+5*k**3*u*v-5*k*u*u*v*v+L*(u*v-1)**2
Pstar=u**5+v**5-(1-k)**5+5*(1-k)**3*u*v-5*(1-k)*u*u*v*v
print("star_fibre_identity",red(F.subs(L,5*(2*k-1))-Pstar))
assert red(F.subs(L,5*(2*k-1))-Pstar)==0
print("center_fibre",red(F.subs(L,k**5)))
print("PASS: quotient cubic and alternate line fibre identities")
