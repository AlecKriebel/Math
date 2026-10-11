from __future__ import annotations

import json
import sympy as sp

z = sp.Symbol('z')


def seed(d):
    q = sp.prod(z-j for j in range(1, d))
    p = sp.expand(2*z*q - sum(sp.div(q,z-j)[0] for j in range(1,d)))
    return p, sp.expand(q)


def compose(p, q, a, b, d):
    pp = sp.Poly(p,z)
    qq = sp.Poly(q,z)
    newp = sp.expand(sum(coeff*a**k*b**(d-k) for (k,),coeff in pp.terms()))
    newq = sp.expand(sum(coeff*a**k*b**(d-k) for (k,),coeff in qq.terms()))
    h = sp.gcd(newp,newq)
    return sp.cancel(newp/h), sp.cancel(newq/h)


results=[]
for d,nmax in [(2,5),(3,3),(4,2),(5,2)]:
    p,q=seed(d)
    assert sp.degree(p,z)==d and sp.degree(q,z)==d-1
    assert sp.gcd(p,q)==1
    residues=[sp.cancel(p.subs(z,j)/sp.diff(q,z).subs(z,j)) for j in range(1,d)]
    assert all(r==-1 for r in residues)
    a,b=z,sp.Integer(1)
    for n in range(1,nmax+1):
        a,b=compose(p,q,a,b,d)
        fixed=sp.Poly(sp.expand(a-z*b),z)
        degree=int(fixed.degree())
        assert int(sp.degree(a,z))==d**n
        assert int(sp.degree(b,z))==d**n-1
        assert degree==d**n
        assert sp.gcd(a,b)==1
        assert sp.degree(sp.gcd(fixed.as_expr(),fixed.diff().as_expr()),z)==0
        real_count=int(fixed.count_roots(-sp.oo,sp.oo))
        assert real_count==degree
        results.append({'d':d,'iterate':n,'map_degree':int(sp.degree(a,z)),
                        'finite_fixed_degree':degree,'real_finite_fixed_count':real_count,
                        'infinity_fixed':True,'coprime':True,'fixed_roots_simple':True})

# Exact projective conjugation that moves the attracting point away from infinity.
# T(z)=z/(1-rz); F=T^-1 f T. Thus F fixes z=1/r.
r=sp.Rational(1,7)
for d in [2,3,4]:
    p,q=seed(d)
    t=z/(1-r*z)
    g=sp.cancel((p/q).subs(z,t))
    F=sp.cancel(g/(1+r*g))
    a,b=sp.fraction(F)
    assert sp.degree(a,z)==d and sp.degree(b,z)==d
    assert sp.gcd(a,b)==1
    assert sp.cancel(F.subs(z,1/r))==1/r
    multiplier=sp.cancel(sp.diff(F,z).subs(z,1/r))
    assert multiplier==sp.Rational(1,2)
    fixed=sp.Poly(a-z*b,z)
    assert fixed.degree()==d+1
    assert fixed.count_roots(-sp.oo,sp.oo)==d+1
    results.append({'d':d,'projective_conjugacy_r':str(r),
                    'numerator_degree':int(sp.degree(a,z)),
                    'denominator_degree':int(sp.degree(b,z)),
                    'real_fixed_count':d+1,'attracting_fixed_point':str(1/r),
                    'attracting_multiplier':str(multiplier)})

print(json.dumps({'scope':'independent exact symbolic finite checks; all-period proof is analytic',
                  'sympy_version':sp.__version__,'checks':results},indent=2))
