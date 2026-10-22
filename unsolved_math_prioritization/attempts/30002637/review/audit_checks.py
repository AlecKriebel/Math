#!/usr/bin/env python3
"""Independent formal checks for the frozen audit; not a geometric proof."""
import json, sympy as S
x, l, n = S.symbols('x l n', nonzero=True)
m2,m3,m4,z=S.symbols('m2 m3 m4 z')
tests={}
def ck(name,a,b=0):
    assert S.factor(S.together(a-b))==0, name
    tests[name]='PASS'
# Independent general-coefficient checks, beyond simply rerunning the supplied script.
k=x*(x-2*l)/(2*(x-l))
ck('General lambda gradient correction', x-x*x/(2*(x-l)),k)
ck('General lambda Hessian gauge cancellation',(l-x/2)*x*(x-l)+k*(l-x)**2)
ck('General lambda Ricci projection cancellation',l*(l*S.Symbol('r'))-(l*S.Symbol('r'))**2/S.Symbol('r'))
ck('Gradient correction operator division',x*(x-2*l)/(x-l),x-l-l*l/(x-l))
# Turn 3 conformal diagonal reduced using its own k-spectrum and moment identities.
turn3=2*m3-S.Rational(2,3)*m4+S.Rational(1,8)*(S.Rational(8,3)*m4-(m4-m2*m2)-z)-(2*m2-m3)**2/(n-2*m2)
turn2=2*m3-S.Rational(1,8)*(S.Rational(11,3)*m4-m2*m2+z)-(2*m2-m3)**2/(n-2*m2)
ck('Turn 3 conformal diagonal equals Turn 2 formula',turn3,turn2)
# Mixed leading term, using E(u^2 |Ric|^2)=3E(u^2 R)-E(SR).
p,q=S.symbols('p q')
ck('Mixed Ricci-conformal leading term',(3*p-q)-p,2*p-q)
# Direct weighted product expansion of the ground state transformation.
a,b,c=S.symbols('a b c') # a=|grad U|^2,b=<WU,U>,c=Delta_f r/r
ck('Bundle zeroth order term',S.Rational(1,2)*(2-2*b+a)-1,S.Rational(1,2)*a-b)
# Min-max separation and stability implication with all norms retained.
g,v,aa,kap=S.symbols('G V a kappa')
ck('Projected Rayleigh lower bound',aa*(g+v)-kap*g,aa*v+(aa-kap)*g)
print(json.dumps({'independent_formal_checks':tests,'count':len(tests),'scope':'Formal identities only. The analytic and geometric audit is written separately.'},indent=2))
