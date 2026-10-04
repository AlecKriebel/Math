#!/usr/bin/env python3
"""Independent cyclotomic and local checks, with no candidate routines."""
import sys
import sympy as S
X,Y,T,Z,W,e,r,L,u,v=S.symbols('X Y T Z W e r L u v')
cyclo=e**4+e**3+e**2+e+1
def er(p):
    return S.Poly(S.expand(p),e).rem(S.Poly(cyclo,e)).as_expr().expand()
def rr(p):
    return S.Poly(S.expand(p),r).rem(S.Poly(r*r-5,r)).as_expr().expand()
results=[]
def check(name,p,reducer=rr,expect=True):
    ok=reducer(S.together(p).as_numer_denom()[0])==0
    results.append(ok==expect)
    print(('PASS ' if ok==expect else 'FAIL ')+name+'; vanishes='+str(ok),flush=True)
    if ok!=expect: print(reducer(S.together(p).as_numer_denom()[0]),flush=True)
phie=1+e+e**4
ce=er(phie**5)
side=[Z+e**(2*j+1)*W-(1+e)*e**j*T for j in range(5)]
product=er(S.prod(side))
claimed=Z**5+W**5+5*phie*Z**2*W**2*T-5*phie**3*Z*W*T**3+phie**5*T**5
check('cyclotomic exact side product',product-claimed,er)
check('negative control wrong pentagon scaling',product-2*claimed,er,False)
for j in range(5):
    check('side '+str(j)+' first vertex',side[j].subs({Z:e**j,W:e**(-j),T:1}),er)
    check('side '+str(j)+' next vertex',side[j].subs({Z:e**(j+1),W:e**(-j-1),T:1}),er)
check('cyclotomic real coefficient sqrt relation',(2*phie-1)**2-5,er)
for j in range(5):
    check('rotation cycles side '+str(j),side[j].subs({Z:e*Z,W:W/e},simultaneous=True)-e*side[(j-1)%5],er)
check('regular pentagon rotation preserves equation',product.subs({Z:e*Z,W:W/e},simultaneous=True)-product,er)
phi=(1+r)/2
c=(11+5*r)/2
P=rr(2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*phi*(X*X+Y*Y)**2*T-5*phi**3*(X*X+Y*Y)*T**3+c*T**5)
check('real X,Y conversion',claimed.subs({Z:X+S.I*Y,W:X-S.I*Y})-P.subs(r,2*phie-1),er)
delta=S.symbols('delta')
def rd(p):
    q=S.Poly(S.expand(p),delta).rem(S.Poly(delta*delta-(5+2*r),delta)).as_expr()
    return rr(q)
co=(r-1)/4
si=delta/(2*phi)
check('rotation coefficients cos²+sin²',co*co+si*si-1,rd)
rotP=P.subs({X:co*X-si*Y,Y:si*X+co*Y},simultaneous=True)
check('exact real rotation preserves P',rotP-P,rd)
check('rotation preserves Q',(co*X-si*Y)**2+(si*X+co*Y)**2-X*X-Y*Y,rd)
check('rotation sends O to slope minus-delta',-si/co+delta,rd)
rho=S.symbols('rho')
Ipoly=rr(P.subs({X:rho,Y:1,T:0}))
deriv=S.diff(Ipoly,rho)
gcdI=S.gcd(S.Poly(Ipoly.subs(r,S.sqrt(5)),rho,extension=S.sqrt(5)),S.Poly(deriv.subs(r,S.sqrt(5)),rho,extension=S.sqrt(5)))
print('INFINITY GCD with X derivative',gcdI.as_expr(),flush=True)
assert gcdI.degree()==0
G=rr((P+L*T*(X*X+Y*Y-T*T)**2).subs(T,1))
jet=rr(G.subs({X:1+u,Y:v}))
Lc=-(25+10*r)/4
jetc=rr(jet.subs(L,Lc))
print('FULL CUSP LOCAL EQUATION',jetc,flush=True)
# Solve exact local form because the plane polynomial is even in v.
print('v² coefficient',S.Poly(jetc,v).coeff_monomial(v*v),flush=True)
print('v⁴ coefficient',S.Poly(jetc,v).coeff_monomial(v**4),flush=True)
print('v⁰ coefficient',S.Poly(jetc,v).coeff_monomial(1),flush=True)
check('exact cusp cubic along tangent',S.Poly(jetc,v).coeff_monomial(1)-u**3*(5+S.Rational(25,4)*u+2*u*u))
check('cusp coefficient v² unit',S.Poly(jetc,v).coeff_monomial(v*v).subs(u,0)+25)
print('RESULTS',len(results),'unexpected',sum(not b for b in results),flush=True)
sys.exit(any(not b for b in results))
