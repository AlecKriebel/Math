#!/usr/bin/env python3
"""Bounded exact diagnostic checks, not a global classification certificate."""
import json
from pathlib import Path
import sympy as s

checks=[]
def eq(label, actual, expected=0):
    residual=s.factor(s.cancel(actual-expected))
    assert residual==0, (label,str(residual))
    checks.append({'name':label,'passed':True})
def yes(label, value):
    assert bool(value),label
    checks.append({'name':label,'passed':True})
def mutant(label, residual):
    yes('negative control: '+label,s.factor(s.cancel(residual))!=0)

t,u,v,z=s.symbols('t u v z')
a,b,c,alpha,beta,r,k=s.symbols('a b c alpha beta r k', nonzero=True)
P=lambda w:w*(w*w-1)
D=lambda x:s.factor(t*s.diff(x,t))

# Local finite and pole leading terms, monomial models, bounded p,q.
# Limit after removal of the predicted t power tests the coefficient only.
local_count=0
for p in range(1,7):
    for q in range(1,7):
        F=2*t**p; G=3*t**q
        E=s.diff(F,t)*s.diff(G,t)*(F-G)**2/(P(F)*P(G))
        expected=(p*q*4 if p<q else p*q*9 if q<p else p*p)
        eq(f'finite local p={p} q={q}',s.limit(E/t**(2*min(p,q)-2),t,0),expected)
        F=2/t**p;G=3/t**q
        E=s.diff(F,t)*s.diff(G,t)*(F-G)**2/(P(F)*P(G))
        expected=(s.Rational(p*q,4) if p<q else s.Rational(p*q,9) if q<p else s.Rational(p*p,36))
        eq(f'pole local p={p} q={q}',s.limit(E/t**(2*min(p,q)-2),t,0),expected)
        Up=s.diff(F,t)*(F-G)/P(F)
        Uexpected=s.Rational(3*p,4) if p<q else -s.Rational(p,2) if p>q else s.Rational(p,4)
        eq(f'U pole coefficient p={p} q={q}',s.limit(Up/t**(2*p-max(p,q)-1),t,0),Uexpected)
        local_count+=1
# Matched leading coefficients force extra zero order.
F=t;G=t+t*t
E=s.diff(F,t)*s.diff(G,t)*(F-G)**2/(P(F)*P(G))
eq('finite cancellation psi has order 2',s.limit(E/t**2,t,0),1)
F=1/t;G=1/t+1
E=s.diff(F,t)*s.diff(G,t)*(F-G)**2/(P(F)*P(G))
eq('pole cancellation psi has order 2',s.limit(E/t**2,t,0),1)

# Transform factors with symbolic ordinary-coordinate derivatives canceled.
x,y=s.symbols('x y')
Po=lambda w:(w-a)*(w-b)*(w-c)
T=lambda w:alpha*w+beta
Pn=lambda w:(w-T(a))*(w-T(b))*(w-T(c))
ratio=s.diff(T(x),x)*s.diff(T(y),y)*(T(x)-T(y))**2*Po(x)*Po(y)/(Pn(T(x))*Pn(T(y))*(x-y)**2)
eq('affine target scaling',ratio,alpha**-2)
T=lambda w:1/(w-a)
Pn=lambda w:w*(w-1/(b-a))*(w-1/(c-a))
ratio=s.diff(T(x),x)*s.diff(T(y),y)*(T(x)-T(y))**2*Po(x)*Po(y)/(Pn(T(x))*Pn(T(y))*(x-y)**2)
eq('inversion at shared root',ratio,(a-b)**2*(a-c)**2)

# Nevanlinna pair exp(z), exp(-z), calculated with t=exp(z).
F=t;G=1/t
U=s.factor(D(F)*(F-G)/P(F));V=s.factor(D(G)*(F-G)/P(G))
eq('CM example U',U,1/t);eq('CM example V',V,t);eq('CM example psi',U*V,1)
mutant('nonaffine precomposition preserves normalization',4*z*z-1)
mutant('forgotten derivative scaling in affine target map',s.Rational(1,4)-1)

# Gundersen exact fibers and normalization.
R=(t+1)/(t-1)**2;S=(t+1)**2/(8*(t-1))
Pg=lambda w:w*(w-1)*(w+s.Rational(1,8))
eq('Gundersen R-1',R-1,-t*(t-3)/(t-1)**2)
eq('Gundersen R+1/8',R+s.Rational(1,8),(t+3)**2/(8*(t-1)**2))
eq('Gundersen S-1',S-1,(t-3)**2/(8*(t-1)))
eq('Gundersen S+1/8',S+s.Rational(1,8),t*(t+3)/(8*(t-1)))
Ug=s.factor(D(R)*(R-S)/Pg(R));Vg=s.factor(D(S)*(R-S)/Pg(S))
eq('Gundersen U',Ug,1-t);eq('Gundersen V',Vg,8/(1-t));eq('Gundersen psi',Ug*Vg,8)
eq('Gundersen normalized psi',Ug*Vg/8,1)
mutant('unscaled Gundersen has psi=1',Ug*Vg-1)
mutant('Gundersen derivative omitted',D(R)*D(S)*(R-S)**2/(Pg(R)*Pg(S))/D(S)-8)
Sbad=(t+1)**2/(7*(t-1))
mutant('Gundersen denominator 7 shares value 1 at t=3',Sbad.subs(t,3)-1)

# Degree-two ansatz elimination; equations use only necessary fibers.
Ra=alpha*(t-r)/(t-1)**2;Sa=beta*(t-r)**2/(t-1)
eq('degree-two R derivative',s.diff(Ra,t),alpha*(-t+2*r-1)/(t-1)**3)
eq('degree-two S derivative',s.diff(Sa,t),beta*(t-r)*(t+r-2)/(t-1)**2)
p1=s.factor(s.together((Ra.subs(t,2-r)-Ra.subs(t,0))/alpha))
p2=s.factor(s.together((Sa.subs(t,2*r-1)-Sa.subs(t,0))/beta))
eq('first ansatz condition',p1,(r*r-r-2)/(r-1))
eq('second ansatz condition',p2,(2*r*r+r-1)/2)
eq('common ansatz polynomial gcd',s.gcd(r*r-r-2,2*r*r+r-1),r+1)
eq('ansatz equality alpha beta',Ra.subs({t:-3,r:-1})-Sa.subs({t:-3,r:-1}),beta-alpha/8)
mutant('extraneous first-condition root r=2 passes second',(2*r*r+r-1).subs(r,2))
mutant('extraneous second-condition root r=1/2 passes first',(r*r-r-2).subs(r,s.Rational(1,2)))

# Exact arithmetic in C(u,v)/(v^2-12u(u+1)(u+4)).
Q=12*u*(u+1)*(u+4)
def canon(expr):
    n,d=s.fraction(s.cancel(expr))
    n=s.rem(n,v*v-Q,v);d=s.rem(d,v*v-Q,v)
    dc=d.subs(v,-v)
    n=s.rem(s.expand(n*dc),v*v-Q,v)
    d=s.rem(s.expand(d*dc),v*v-Q,v)
    return s.cancel(n/d)
def ED(expr):return canon(s.diff(expr,u)*v+s.diff(expr,v)*s.diff(Q,u)/2)
F=u*v/(8*s.sqrt(3)*(u+1));G=(u+4)*v/(8*s.sqrt(3)*(u+1)**2)
eq('elliptic vector field respects curve',canon(2*v*(s.diff(Q,u)/2)-s.diff(Q,u)*v))
eq('Reinders F squared fiber',canon(F*F-1),(u-2)*(u+2)**3/(16*(u+1)))
eq('Reinders G squared fiber',canon(G*G-1),(u-2)**3*(u+2)/(16*(u+1)**3))
eq('Reinders sign ratio at u=2',canon(G/F).subs(u,2),1)
eq('Reinders sign ratio at u=-2',canon(G/F).subs(u,-2),1)
Ue=canon(ED(F)*(F-G)/P(F));Ve=canon(ED(G)*(F-G)/P(G))
eq('Reinders U',Ue,12*s.sqrt(3)/(u+1))
eq('Reinders V',Ve,4*s.sqrt(3)*(u+1))
eq('Reinders psi',canon(Ue*Ve),144)
eq('Reinders normalized psi',canon(Ue*Ve)/144,1)
mutant('unscaled Reinders has psi=1',canon(Ue*Ve)-1)
mutant('wrong Reinders scale z/6',canon(Ue*Ve)/36-1)
# Pole and zero local orders use u uniformizers at curve branch points.
for name,us,vs,p,q in [('zero u=0',t*t,t,3,1),('zero u=-4',-4+t*t,t,1,3),('pole u=-1',-1+t*t,t,-1,-3),('pole infinity',1/t**2,1/t**3,-3,-1)]:
    for label,expr,expected in [('F',F,p),('G',G,q)]:
        substituted=expr.subs({u:us,v:vs}, simultaneous=True)
        order=substituted.as_leading_term(t).as_powers_dict().get(t,s.Integer(0))
        eq('Reinders local order '+label+' '+name,order,expected)

# Degree / ramification bookkeeping: formulas, not an existence search.
d,e0,ei,n=s.symbols('d e0 ei n')
eq('sphere ramification yields n=2d',(4*d-e0-ei-2*d)+(e0+ei-2),2*d-2)
eq('torus fiber/ramification count',4*d-2*d,2*d)
eq('torus maximal multiplicity sum',8*d-2*d,6*d)
mutant('elliptic uniform multiplicity 2 fits balance',2*2*d-6*d)
mutant('elliptic uniform multiplicity 4 fits balance',4*2*d-6*d)
# Local ODE check at a regular point. This does not certify continuation.
eq('local ODE initial derivative',P(s.Integer(2))*P(s.Integer(3))/(2-3)**2,144)
eq('local ODE initial psi',144*(2-3)**2/(P(s.Integer(2))*P(s.Integer(3))),1)
# Shrinking scale is an exact chain-rule identity, not a numerical convergence test.
rho=s.symbols('rho')
fp,gp,delta,pf,pg=s.symbols('fp gp delta pf pg',nonzero=True)
eq('shrinking rescaling factor',(rho*fp)*(rho*gp)*delta**2/(pf*pg),rho**2*fp*gp*delta**2/(pf*pg))
eq('shrinking constant limit',s.limit(rho**2,rho,0),0)
mutant('shrinking scale preserves psi=1',rho**2-1)

receipt={'schema':1,'problem_id':30000706,'claim':'bounded exact diagnostic controls only','passed':len(checks),'failed':0,
'limits':{'local_multiplicity_p_max':6,'local_multiplicity_q_max':6,'local_pairs':local_count,'search':'no unbounded search; no exhaustive global classification','arithmetic':'exact symbolic; no floating-point tolerance','external_theorems_not_verified':['Picard','Riemann-Hurwitz','Gundersen 2CM+2IM']},'checks':checks}
text=json.dumps(receipt,indent=2,sort_keys=True)+'\n'
Path(__file__).with_name('CONTROL_RESULTS.json').write_text(text)
print(json.dumps({'passed':len(checks),'failed':0,'local_pairs':local_count,'sympy':s.__version__},sort_keys=True))
