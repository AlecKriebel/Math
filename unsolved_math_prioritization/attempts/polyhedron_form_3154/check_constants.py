#!/usr/bin/env python3
"""Authored checks. Binomial weights are asymptotic proxies, NOT exact map counts."""
import json, math
from fractions import Fraction
from pathlib import Path
import sympy as s

a=s.symbols('a', positive=True)
I=(3*a-1)*s.log(3*a-1)+(2-3*a)*s.log(2-3*a)-a*s.log(a)-(1-a)*s.log(1-a)
expected=2/(a*(1-a)*(3*a-1)*(2-3*a))
assert s.simplify(s.diff(I,a,2)-expected)==0
coeff={str(k):str(s.simplify(s.diff(I,a,k).subs(a,s.Rational(1,2))/s.factorial(k))) for k in (0,1,2,3,4,5,6)}
assert coeff=={'0':'0','1':'0','2':'16','3':'0','4':'320/3','5':'0','6':'23296/15'}
G=((3*a-1)*(2-3*a))**s.Rational(5,2)/(a**4*(1-a)**4)
assert G.subs(a,s.Rational(1,2))==8

def logchoose(n,k):
    return math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1)
def check(e):
    rows=[]
    for i in range(3,e-2):
        j=e-i
        if j+3>2*i or i+3>2*j: continue
        w=logchoose(2*i,j+3)+logchoose(2*j,i+3)-math.log(4*3**5*i*j*e)
        rows.append((i-e/2,w))
    mx=max(w for x,w in rows)
    total=sum(math.exp(w-mx) for x,w in rows)
    logtotal=mx+math.log(total)
    ps=[(x,math.exp(w-mx)/total) for x,w in rows]
    v=sum(p*x*x for x,p in ps)
    fourth=sum(p*x**4 for x,p in ps)
    normalizer=e*math.log(4)-math.log(486*math.sqrt(math.pi))-3.5*math.log(e)
    cum=0.; ks=0.
    for x,p in ps:
        phi=.5*(1+math.erf(x/math.sqrt(e/16)))
        ks=max(ks,abs(cum-phi),abs(cum+p-phi)); cum+=p
    return {'edges':e,'proxy_total_over_asymptotic':math.exp(logtotal-normalizer),'proxy_variance_over_e':v/e,'proxy_standardized_fourth_moment':fourth/(e/32)**2,'proxy_KS_distance_to_target_Gaussian':ks}
results={'scope':'Algebra and asymptotic proxy checks, not proof by computation and not exact polyhedron enumeration.','symbolic_Taylor_coefficients':coeff,'proxy_checks':[check(e) for e in (100,101,500,501,2000,2001,10000,10001)]}
# Exact rational arithmetic for shifted-binomial proxy verifies parity symmetry.
for e in (30,31,60,61):
    weights={i:Fraction(math.comb(2*i,e-i+3)*math.comb(2*(e-i),i+3),4*3**5*i*(e-i)*e) for i in range(3,e-2) if e-i+3<=2*i and i+3<=2*(e-i)}
    assert all(w==weights[e-i] for i,w in weights.items())
    assert sum((Fraction(i)-Fraction(e,2))*w for i,w in weights.items())==0
results['exact_rational_proxy_symmetry_checks']='PASS for e=30,31,60,61'
Path(__file__).with_name('check_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
