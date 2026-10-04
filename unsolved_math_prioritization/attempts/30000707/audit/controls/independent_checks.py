#!/usr/bin/env python3
"""Independent exact audit checks. Not a solution of the open classification."""
from pathlib import Path
import hashlib
import json
import platform
import sympy as sp

HERE = Path(__file__).resolve().parents[1]
checks = []

def check(name, condition, **extra):
    assert condition, name
    checks.append({'name': name, 'pass': True, **extra})

def zero(name, expression):
    value = sp.factor(sp.cancel(expression))
    check(name, value == 0)

# Public projection: historical provenance-only checks are replaced by the public inventory runner.

x, b, k, v, hp, A, B, a, s, j, c, p, q, r, w = sp.symbols('x b k v hp A B a s j c p q r w')
P = lambda y: y**3+p*y**2+q*y+r

# A common affine change of values multiplies each auxiliary by 1/lambda.
lam, y, yy, yp, yyp = sp.symbols('lam y yy yp yyp', nonzero=True)
root = sp.symbols('root0:3')
product = sp.prod(y-t for t in root)
transformed = sp.prod(lam*y+b-(lam*t+b) for t in root)
zero('affine covariance of psi1', lam*yp*(lam*y-lam*yy)/transformed - yp*(y-yy)/(lam*product))

# Keep a free nonzero multiplicative phase in the all-CM exponential form.
d = sp.symbols('d', nonzero=True)
F = b+k*v; G = b+k/v
PC = lambda y: (y-b)*((y-b)**2-k**2)
zero('CM first auxiliary with arbitrary phase', k*hp*v*(F-G)/PC(F)-hp/(k*v))
zero('CM second auxiliary with arbitrary phase', -k*hp/v*(F-G)/PC(G)-hp*v/k)
for eps in (1,-1):
    # h'=-1, k=-epsilon, exp(h)=epsilon/exp(z), with every log branch absorbed.
    zero('CM first function epsilon '+str(eps), F.subs({k:-eps,v:eps/x})-(b-1/x))
    zero('CM second function epsilon '+str(eps), G.subs({k:-eps,v:eps/x})-(b-x))

Fc, Fcp = sp.symbols('Fc Fcp')
Gc = 2*b-Fc
zero('non-omitted infinity gives equal auxiliaries', Fcp*(Fc-Gc)/PC(Fc) - (-Fcp)*(Fc-Gc)/PC(Gc))

# Pole equations and the coefficient Jacobian, independently differentiated.
Fa, Ga, eps = sp.symbols('Fa Ga eps')
lead1 = -A*(A-B)-a*A**3
lead2 = -B*(A-B)-B**3/a
for sign in (1,-1):
    residues = {A: sign-1/a, B: a-sign}
    zero('pole leading equation one sign '+str(sign), lead1.subs(residues))
    zero('pole leading equation two sign '+str(sign), lead2.subs(residues))
    linear1 = j*Fa*(A-B)-A*(Fa-Ga)-3*a*A*A*Fa
    linear2 = j*Ga*(A-B)-B*(Fa-Ga)-3*B*B*Ga/a
    jac = sp.Matrix([linear1,linear2]).jacobian([Fa,Ga]).subs(residues)
    zero('Laurent determinant sign '+str(sign), jac.det()-(a-sign)**4*(j+2)*(j+3)/a**2)

# Differential elimination with a cubic and independent formal jets.
f, df, ddf, E, Qp = sp.symbols('f df ddf E Qp')
g = f-E*P(f)/df
dg = sp.diff(g,f)*df+sp.diff(g,df)*ddf+sp.diff(g,E)*Qp*E
equation = dg*(f-g)-P(g)/E
u = 1/E
scalar = P(f)*ddf-(Qp*P(f)+u*P(f)*sp.diff(P(f),f,2)/2)*df+(u*u-1)*sp.diff(P(f),f)*df**2+(u-u**3)*df**3+P(f)**2
zero('exact scalar equation equivalence multiplier', equation*df**3/(E**2*P(f))-scalar)

# Recompute endpoint-normalized degree-two equations without importing original controls.
for sign in (1,-1):
    R = -1/x+(sign*c-1)/(x-c)
    S = -x+B+(c*c-sign*c)/(x-c)
    rn, rd = sp.fraction(sp.together(R))
    sn, sd = sp.fraction(sp.together(S))
    zero('nonzero endpoint numerator R at zero sign '+str(sign), rn.subs(x,0)-c)
    zero('R residue numerator at c sign '+str(sign), rn.subs(x,c)-c*(sign*c-1))
    zero('S residue numerator at c sign '+str(sign), sn.subs(x,c)-c*(c-sign))
    # Generic fibers have two distinct points: these discriminants are nonzero polynomials in w.
    dr = sp.Poly(sp.discriminant(rn-w*rd,x),w)
    ds = sp.Poly(sp.discriminant(sn-w*sd,x),w)
    check('R generic degree-two fiber sign '+str(sign), dr.degree() == 2 and sp.factor(dr.LC()-c*c) == 0)
    check('S generic degree-two fiber sign '+str(sign), ds.degree() == 2 and ds.LC() == 1)

R = -1/x+(c-1)/(x-c)
S = -x+B+(c*c-c)/(x-c)
PP = lambda y: y**3+p*y*y+q*y
n1 = sp.Poly(sp.cancel((sp.diff(R,x)*(R-S)-PP(R))*x*x*(x-c)**2),x)
n2 = sp.Poly(sp.cancel((x*x*sp.diff(S,x)*(R-S)-PP(S))*(x-c)**2),x)
zero('second numerator fixes p', n2.LC()+2*B+p)
special = [sp.factor(t.subs({p:-2*B,q:-2,c:2})) for t in [n1.nth(1),n1.nth(0)]]
check('exceptional c=2 ideal is inconsistent', sp.groebner(special,B).polys[0].as_expr() == 1)
ordinary = [sp.factor(t.subs({p:-2*B,q:-1})) for t in n1.all_coeffs()]
reduced = [sp.factor(t.subs(B,-c-1+2/c)) for t in ordinary]
nonzero = [t for t in reduced if t != 0]
gcd = sp.Poly(sp.fraction(nonzero[0])[0],c)
for t in nonzero[1:]:
    gcd = sp.gcd(gcd,sp.Poly(sp.fraction(t)[0],c))
check('ordinary branch only degenerate c=1 survives N1', sp.factor(gcd.monic().as_expr()-(c-1)) == 0)
for sign in (1,-1):
    rr = -1/x+(sign*c-1)/(x-c)
    ss = -x+B+(c*c-sign*c)/(x-c)
    zero('removed-pole R sign '+str(sign), rr.subs(c,sign)+1/x)
    zero('removed-pole S sign '+str(sign), ss.subs({c:sign,B:0})+x)

# The exact preprint test, including its actual nested sector exponents.
F = (x+1)/2; G = (1/x+1)/2
PP = lambda y: y*(y-1)*(y-sp.Rational(1,2))
zero('preprint Phi is exp(-2z)', sp.diff(F,x)*PP(G)/(sp.diff(G,x)*PP(F))-1/x**2)
epsilon = sp.pi/12
outer_width = sp.pi-4*epsilon
outer_omega = sp.pi/outer_width
epsilon0 = epsilon/outer_omega
inner_width = outer_width-2*epsilon0
zero('actual outer angular exponent',outer_omega-sp.Rational(3,2))
zero('actual inner angular exponent',sp.pi/inner_width-sp.Rational(9,5))
check('outer and inner leading scales exceed order one', outer_omega>1 and sp.pi/inner_width>1)

result = {'status':'PASS','check_count':len(checks),'python':platform.python_version(),
          'sympy':sp.__version__,'checks':checks,
          'scope':'Public projection of the same 36 independent exact identity checks; historical provenance-only checks are excluded. The analytic claims are audited in AUDIT.md; no full classification, global existence, novelty, or theorem-falsity certificate.'}
(HERE/'controls'/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','check_count','python','sympy']}))
