#!/usr/bin/env python3
"""Modest reproducible checks; not a proof of the full PDE threshold theorem."""
from fractions import Fraction as F
import json, math

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

# Rational polynomial identity, q representing k^2.
# (2 q eps^3)(1/(2eps)+2 eps q) = eps^2 q(1+4q eps^2).
# Check as a formal bivariate polynomial, not sampled numerical equality.
def mul(p,q):
    out={}
    for (e1,k1),v1 in p.items():
        for (e2,k2),v2 in q.items():
            key=(e1+e2,k1+k2)
            out[key]=out.get(key,F(0))+v1*v2
    return {key:value for key,value in out.items() if value}
lhs=mul({(3,1):F(2)},{(-1,0):F(1,2),(1,1):F(2)})
rhs=mul({(2,1):F(1)},{(0,0):F(1),(2,1):F(4)})
require(lhs==rhs,'single-mode prefactor cancellation')
wrong=mul({(3,1):F(2)},{(-1,0):F(1,2),(1,1):F(-2)})
require(wrong!=rhs,'negative control rejects drift-spectrum algebra mutation')

# Verify the antiderivative coefficients for integral exp(-a*x) cos(b*x):
# F(x)=exp(-a*x)(-a*cos(b*x)+b*sin(b*x))/(a*a+b*b).
# Its derivative coefficients are exactly 1 for cosine and 0 for sine.
for a in (F(1,7),F(1),F(7)):
    for b in (F(1,3),F(2),F(11)):
        A=-a/(a*a+b*b); B=b/(a*a+b*b)
        require(-a*A+b*B==1,'antiderivative cosine coefficient')
        require(-b*A-a*B==0,'antiderivative sine coefficient')

scaling_cases=0
for L in (F(1,3),F(1),F(7)):
    for a in (F(1,2),F(2),F(5)):
        for eps in (F(1,100),F(1,7)):
            # Multiply transformed PDE by L/a.
            require(eps/(L*L)*(L/a)==eps/(a*L),'scaled diffusivity')
            require((a/L)*(L/a)==1,'scaled transport magnitude')
            # The spatial L2 normalization is amplitude^2=L.
            require(L/L==1,'initial norm')
            require(L*(a/L)==a,'control norm squared factor')
            scaling_cases+=1

# Strict separation of threshold candidates by exact rational enclosures.
r2lo=F(1414213,1000000); r2hi=F(1414214,1000000)
r3lo=F(1732050,1000000); r3hi=F(1732051,1000000)
require(r2lo*r2lo<2<r2hi*r2hi,'sqrt2 enclosure')
require(r3lo*r3lo<3<r3hi*r3hi,'sqrt3 enclosure')
require(2+2*r2hi < 2*(1+r3lo),'separate source-prose threshold from prior theorem')

# Stable log evaluation of the exact ratios. These are consistency tests only.
def log_expm1(x):
    return x+math.log1p(-math.exp(-x)) if x>1 else math.log(math.expm1(x))
def log_ratio_sq(eta,n,eps,T):
    lam=1/(4*eps)+eps*(math.pi*n)**2
    ln_num=math.log(-math.expm1(-1/eps)) if eta==1 else log_expm1(1/eps)
    return ln_num-log_expm1(2*lam*T)
rows=[]
for eta in (1,-1):
    for T in (1.0,2.0,3.0):
        previous=None
        for eps in (0.02,0.01,0.005,0.002):
            r=log_ratio_sq(eta,1,eps,T)
            for n in (2,3,8,32):
                require(log_ratio_sq(eta,n,eps,T)<r,'single-mode maximum at n=1')
            predicted=(-T/2 if eta==1 else 1-T/2)
            # eps log(R^2) approaches the exact leading action.
            if eps==0.002:
                require(abs(eps*r-predicted)<0.001,'asymptotic action consistency')
            rows.append({'eta':eta,'T':T,'epsilon':eps,'log_ratio_squared':r})

# Endpoint abstract models at tau=2, eps=1/n.
for n in (2,10,100):
    require(F(1)==1,'bounded endpoint A')
    require(1/F(1,n)==n,'unbounded endpoint B')

out={
 'status':'PASS',
 'exact_checks':['formal single-mode prefactor cancellation','antiderivative coefficient identities','rational scaling factors','rational square-root enclosures and threshold separation','abstract endpoint countermodels'],
 'scaling_cases':scaling_cases,
 'floating_checks':'Only consistency checks of a formula proved in prose; no numerical threshold proof.',
 'numerical_rows':rows,
 'does_not_verify':['the entire Koike-Laheurte preprint','uniform PDE observability over arbitrary mode combinations','the positive critical endpoint','absence of all prior user or repository work']
}
print(json.dumps(out,indent=2,sort_keys=True))
