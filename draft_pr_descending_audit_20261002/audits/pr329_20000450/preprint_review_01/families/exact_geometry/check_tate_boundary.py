#!/usr/bin/env python3
import sys
import sympy as S
r,L,x,y,B=S.symbols('r L x y B')
def red(p):return S.Poly(S.expand(p),r).rem(S.Poly(r*r-5,r)).as_expr()
def zero(p):return red(S.together(p).as_numer_denom()[0])==0
checks=[]
def check(name,p,expected=True):
    ok=zero(p);checks.append(ok==expected);print(('PASS ' if ok==expected else 'FAIL ')+name+'; vanishes='+str(ok),flush=True)
c=(11+5*r)/2;d=5+2*r
beta=(11-5*r)*L/(2*(L+5*r));k=4*(L+5*r)/r;q=d*k*k
deltaW=2**24*(161-72*r)*L**5*(L+5*r)**5*(L+c)
check('exact discriminant under Tate scaling',deltaW-q**6*beta**5*(beta*beta-11*beta-1))
print('TATE SECOND FACTOR numerator',S.factor(red(S.together(beta*beta-11*beta-1).as_numer_denom()[0]),extension=S.sqrt(5)),flush=True)
D=y*y+(1-B)*x*y-B*y-x**3+B*x*x
check('horizontal tangent third intersection',D.subs(y,0)+x*x*(x-B))
check('chord P0 to 2P0 has third intersection 2P0',D.subs(y,B*x)+x*(x-B)**2)
check('negation of (B,0) has ordinate B²',-(1-B)*B+B-B*B)
coeffs=[5*B**8,10*B**7*(B-3),5*B**6*(2*B*B-13*B+16),5*B**5*(B**3-10*B*B+36*B-25),B**4*(B**4-12*B**3+94*B*B-293*B+126),B**3*(B**4+3*B**3-71*B*B+322*B-84),B*B*(B**4+3*B**3+19*B*B-248*B+36),B*(B**4+3*B**3-26*B*B+127*B-9),B**4-7*B**3+44*B*B-38*B+1,5*(B*B-5*B+1),5]
R=sum(cj*x**j for j,cj in enumerate(coeffs))
check('residual at zero excludes inverse chart pole',R.subs(x,0)-5*B**8)
check('residual at beta excludes inverse chart pole',R.subs(x,B)-5*B**12)
check('negative control incorrect residual beta exponent',R.subs(x,B)-5*B**11,False)
print('RESULTS',len(checks),'unexpected',sum(not a for a in checks),flush=True)
sys.exit(any(not a for a in checks))
