#!/usr/bin/env python3
"""Exact supplemental algebra checks; not a PDE solver or formal proof verifier."""
import json
import sympy as s

checks=[]
def zero(name, expression):
    value=s.factor(s.simplify(expression))
    if value != 0:
        raise RuntimeError(f'{name}: nonzero residual {value}')
    checks.append(name)
def truth(name, condition):
    if condition is not True and condition != s.true:
        raise RuntimeError(f'{name}: condition failed: {condition}')
    checks.append(name)

c,lam,q,p,eps,b,rc,rp=s.symbols('c lam q p eps b rc rp', positive=True)
logH=q*s.log(c)+(1-q)*s.log(lam-q*c)
g=q*(lam-c)/(c*(lam-q*c))
zero('logarithmic derivative',s.diff(logH,c)-g)
zero('critical first derivative',g.subs(c,lam))
zero('critical curvature',s.diff(g,c).subs(c,lam)+q/(lam**2*(1-q)))
leading=eps*p*c*(c-lam/q)*b
zero('leading invariant cancellation',g*leading-p*eps*b*(c-lam))
zero('perturbed invariant identity',g*(leading+rc)-p*eps*b*(c-lam+rp)-(g*rc-p*eps*b*rp))
zero('threshold monotonicity',s.diff(s.log(lam)+(1-q)*(s.log(1-q)-s.log(lam-q)),lam)-q*(lam-1)/(lam*(lam-q)))
zero('tail-square coefficient',(p*s.Rational(1,2))/(q/(2*lam**2*(1-q)))-p*lam**2*(1-q)/q)
zero('invariant-square coefficient',1/(q/(2*lam**2*(1-q)))-2*lam**2*(1-q)/q)
L=s.symbols('L', positive=True)
for m in (2,3,4):
    qm=s.Rational(5-m,m+3);pm=s.Rational(4,m+3)
    alpha=s.Rational(2,m-1)-s.Rational(1,2)
    beta=s.Rational(1,m-1)-s.Rational(1,2)
    zero(f'm={m} alpha identity',alpha-qm/(1-qm))
    zero(f'm={m} threshold exponent',pm/(1-qm)-s.Rational(2,m-1))
    zero(f'm={m} signed-integral exponent',beta-s.Rational(3-m,2*(m-1)))
    f=c**alpha*(lam-qm*c)
    zero(f'm={m} energy derivative',s.diff(f,c)-alpha*c**(alpha-1)*(lam-c))
    zero(f'm={m} energy curvature',s.diff(f,c,2).subs(c,lam)+alpha*lam**(alpha-1))
    K=s.Rational(m-1,m+3)*c*L;N=s.Rational(2*(m+1),m+3)*c*L
    zero(f'm={m} first Pohozaev',K+c*L-N)
    zero(f'm={m} second Pohozaev',K/2-c*L/2+N/(m+1))
    zero(f'm={m} soliton energy',K/2+lam*L/2-N/(m+1)-(lam-qm*c)*L/2)
    z=s.symbols('z',real=True);k=s.Rational(m-1,2)
    zero(f'm={m} Q equation after division by Q',s.tanh(z)**2-k/s.cosh(z)**2-1+s.Rational(m+1,2)/s.cosh(z)**2)

# Exact polynomial forms obtained by positive integer powers; no root-selection by numerics.
P2=lambda x:x**5-100*(x-s.Rational(3,5))**2
P3=lambda x:x**3-(3*x-1)**2
P4=lambda x:6**6*x**7-16*(7*x-1)**6
truth('quadratic threshold bracket lower',P2(s.Rational(63,100))>0)
truth('quadratic threshold bracket upper',P2(s.Rational(64,100))<0)
truth('cubic threshold bracket lower',P3(s.Rational(42,100))>0)
truth('cubic threshold bracket upper',P3(s.Rational(43,100))<0)
zero('quartic exact threshold',P4(s.Rational(1,4)))
truth('quartic threshold interval',s.Rational(1,7)<s.Rational(1,4)<1)
zero('quartic signed-integral cancellation',2**s.Rational(-1,3)*(s.Rational(1,4))**s.Rational(-1,6)-1)
zero('quartic energy endpoint',(s.Rational(1,4))**7*6**6-16*(7*s.Rational(1,4)-1)**6)

# Verify that deliberately wrong mathematical identities are detected.
mutations={
    'wrong invariant drift sign':g*(leading+rc)-p*eps*b*(c-lam+rp)-(g*rc+p*eps*b*rp),
    'wrong curvature sign':s.diff(g,c).subs(c,lam)-q/(lam**2*(1-q)),
    'quartic false signed integral mismatch':2**s.Rational(-1,3)*(s.Rational(1,4))**s.Rational(-1,6),
}
rejected=[]
for name,residual in mutations.items():
    try:zero('MUTATION '+name,residual)
    except RuntimeError:rejected.append(name)
    else:raise RuntimeError(f'Mutation survived: {name}')
print(json.dumps({'status':'PASS','exact_checks':len(checks),'checks':checks,'mathematical_mutations_rejected':rejected,'scope':'Exact algebra only; no PDE asymptotic, existence, literature-completeness, or formal-proof certification.'},indent=2,sort_keys=True))
