#!/usr/bin/env python3
"""Exact checks for the uniform Turn 5 tangent and arithmetic reductions."""
from pathlib import Path
from itertools import combinations
import json
import sympy as sp
x=sp.Symbol('x')
checks=[]
family_counts=[]
for L in range(1,8):
    k=4*L+2;mid=2*L+1;count=0
    for mask in range(1,1<<L):
        chosen=[a for a in range(1,L+1) if mask>>(a-1)&1]
        A=max(chosen)
        S=sorted({mid}|{j for a in chosen for j in (4*a,4*(L-a)+2)})
        if L%2:
            f=x**(2*L+1)-x**(2*L-A+1)-1
            U=x**L-x**(L-A)
            assert f.subs(x,1)<0<f.subs(x,2)
        else:
            f=x**(2*L+1)+x**A-1
            U=x**L
            assert f.subs(x,0)<0<f.subs(x,1)
        def base(n):return 0 if n%4 in [0,1] else 1
        def w(n):
            q,r=divmod(n,4)
            return 0 if r in [0,2] else (U*x**q if r==1 else -x**q)
        for n in range(4):
            eligible=[j for j in S if base(n+j)==1]
            assert eligible and max(base(n+j) for j in S)==1
            assert base(n+k)==1-base(n)
            # At a maximal base coordinate, tangent values are zero or -x^q.
            assert all((n+j)%4 in [0,2,3] for j in eligible)
            zero=[j for j in eligible if (n+j)%4 in [0,2]]
            if zero:win=zero[0]
            elif L%2:win=min(eligible,key=lambda j:(n+j)//4) # x>1
            else:win=max(eligible,key=lambda j:(n+j)//4)     # 0<x<1
            residual=sp.rem(sp.expand(w(n+k)-(w(n+win)-w(n))),f,x)
            assert residual==0,(L,A,S,n,residual)
        assert any(w(j)!=0 for j in range(k))
        assert all(sp.expand(w(j+4)-x*w(j))==0 for j in range(k))
        count+=1
    family_counts.append({'L':L,'order':k,'support_patterns_checked':count,
                          'constant_statuses':[False,True],
                          'multiplier':'greater than 1' if L%2 else 'between 0 and 1'})
checks.append({'name':'uniform_tangent_formula_consistency','results':family_counts,'passed':True,
               'scope':'Exact checks in several orders; the document proves the family for all L.'})

# Cyclotomic norm-polynomial identity, in abstract symbols.
B,R,N,M,t=sp.symbols('B R N M t')
minimal=t*t+N*M*t-M
product=(B-t*R)*(B+(N*M+t)*R)
expected=B*B+N*M*B*R-M*R*R
assert sp.rem(sp.expand(product-expected),minimal,t)==0
checks.append({'name':'quadratic_norm_polynomial_identity','passed':True})

# Classical rationally scaled examples are retained.
z=sp.Symbol('z')
examples=[]
for ell in range(1,5):
    for name,k,R,N in [('five_period',2*ell,z**ell,1),
                       ('eight_period',3*ell,z**ell+z**(2*ell),2)]:
        B=z**k+1;Q=sp.Poly(B*B+N*B*R-R*R,z)
        factors=sp.factor_list(Q.as_expr(),z)[1]
        assert all(sp.Poly(p,z).is_cyclotomic for p,e in factors)
        r=ell;m_r=1
        assert r*m_r*N<=k-1
        examples.append({'family':name,'dilation':ell,'norm_factors':[(str(p),e) for p,e in factors]})
checks.append({'name':'classical_arithmetic_controls','results':examples,'passed':True})

# An adversarial larger-support candidate passes the coarse arithmetic bounds
# but is rejected by a second-power trace at the negative fixed point.
k=8;weights={1:1,4:2,7:1};N=sum(weights.values());M=1;r=min(weights)
assert N==4 and r*weights[r]*N*M<=k-1
assert sum(v for j,v in weights.items() if j%2)==sum(v for j,v in weights.items() if j%2==0)
tau=sp.sqrt(5)-2;c0=1-N*tau;d=N*M+tau
assert sp.simplify(c0*(9+4*sp.sqrt(5)))==1
assert sp.simplify(d-(2+sp.sqrt(5)))==0
P=z**k+1+d*sum(m*z**j for j,m in weights.items())
# Newton's second power sum is d^2 since the next leading coefficient vanishes.
assert sp.Poly(P,z).nth(k-1)==d and sp.Poly(P,z).nth(k-2)==0
assert sp.simplify(d*d-8)==1+4*sp.sqrt(5)
checks.append({'name':'arithmetic_bounds_are_not_sufficient','order':8,'weights':weights,
               'scaled_constant':'1','negative_fixed_point_second_power_sum':str(sp.expand(d*d)),
               'strictly_exceeds_dimension':True,'passed':True})

result={'all_passed':True,'sympy_version':sp.__version__,'checks':checks,
        'scope':'General proofs plus exact consistency and adversarial checks. No finite search is used as an all-order classification.'}
Path(__file__).with_name('turn05_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_passed':True,'tangent_support_patterns':sum(r['support_patterns_checked'] for r in family_counts),
                  'orders_checked':[r['order'] for r in family_counts],'checks':len(checks)},indent=2))
