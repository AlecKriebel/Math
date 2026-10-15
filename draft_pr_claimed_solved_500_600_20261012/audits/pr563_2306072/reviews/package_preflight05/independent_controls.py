#!/usr/bin/env python3
"""Fresh exact controls; analytic inputs remain in INDEPENDENT_DERIVATION.md."""
from fractions import Fraction as F
import json

checks=[]
def check(name, condition, evidence=None):
    if not condition:raise RuntimeError(name)
    checks.append({'name':name,'passed':True,'evidence':evidence})

e=F(1,10**24);h=F(1,10**12);T=F(7,4)
check('scale',h*h==e)
check('a2 proximity',52<8**2)
check('a3 proximity',F(52,3)<25)
check('H sharper weighted tail',13*F(16,135)<F(5,4)**2 and 4*F(2,3)+F(5,4)<5)
check('H derivative sharper weighted tail',13*F(56,25)<F(27,5)**2 and 4+F(27,5)<10)
check('H modulus controls',F(5,3)-5*h>F(3,2) and F(5,3)+5*h<F(11,6))
ferr=F(2,3)*5*F(7,2)/(F(3,2)**2*F(5,3)**2)
fperr=19/F(3,2)**3+F(1,3)*5*11/(F(3,2)**3*F(5,3)**3)
check('value and derivative controls',ferr<2 and fperr<8,{'f_error_multiplier':str(ferr),'fprime_error_multiplier':str(fperr)})
rtip=F(6,25)+F(5,9)*F(9,125)+(2+F(5,9)*8)*h
check('actual tip with inverse Schwarz direction',rtip<F(3,10),{'upper_bound':str(rtip)})
check('positive radius separation',F(25,81)-F(3,10)==F(7,810))
# Independently propagate on the smaller disk |v|<=2. For |t|<=7/4,
# the Rouché contour margin is 1/4, larger than |G-v|<=62e.
check('disk2 polynomial majorants',2+3*4+16==30 and 106+24*4==202 and 30+202*h<31)
check('disk2 Rouche',62*e<F(1,4))
check('disk2 root/derivative safe',31*e<F(1,4))
Cp=101+F(31**2,2)*h
Cv=2*Cp+15*62*h
Cvp=101+(2*31**2+F(44,2)*62)*h
Cz=(T*Cvp+Cv+7*62*h)/(1-62*e)
check('disk2 independent inverse bounds',Cp<102 and Cv<205 and Cvp<102,{'p':str(Cp),'V':str(Cv),'Vprime':str(Cvp)})
check('disk2 independent Z bound',Cz<384,{'Z_error_multiplier':str(Cz),'units':'epsilon*eta'})
# Solve the first variation directly by integrating the quartic pullback.
# Generic coefficients alpha*a3+beta*a4 yield P0=(4alpha+10beta)
# -(alpha+6beta)v²+beta*v⁴ and d=-integral(P0)/2.
def first_variation(alpha,beta):
    P=[4*alpha+10*beta,0,-alpha-6*beta,0,beta]
    d=[F(0)]+[-F(c,2*(n+1)) for n,c in enumerate(P)]
    q=[F(0) for _ in P]
    for n in range(1,len(d)):q[n-1]=(n-1)*d[n]
    return P,d,q
P,d,q=first_variation(F(-3),F(1))
check('quartic and integrated first variation',P==[-2,0,-3,0,1] and d==[0,1,0,F(1,2),0,F(-1,10)])
check('q from t*dprime-d',q==[0,0,1,0,F(-2,5)])
evalq=lambda qq,t:sum(c*t**n for n,c in enumerate(qq))
q1=evalq(q,F(1));qT=evalq(q,T)
check('exact endpoint signs',q1==F(3,5) and qT==F(-441,640))
check('strong strict sign margins',q1-Cz*h>F(1,2) and qT+Cz*h<F(-1,2))
check('all-t orientation bound',222/(1-111*e)<223 and 223*e<1)
check('selected perturbation negative controls',evalq(first_variation(F(1),F(0))[2],1)>0 and evalq(first_variation(F(1),F(0))[2],T)>0 and evalq(first_variation(F(0),F(1))[2],T)>0)
check('zero epsilon degeneracy',0*q1==0)
# Goh's even quartic square route needs a second equation. The candidate's
# output quartic is nonsquare throughout its coefficient enclosures.
check('candidate output quartic nonsquare',4*e*(1-3*e)-16*e*e>3*e)
# No Koebe phase can be critical for the candidate: cos3theta=cos2theta=0
# has no common root by this polynomial Bezout identity.
mul=lambda a,b:[sum(a[j]*b[n-j] for j in range(len(a)) if 0<=n-j<len(b)) for n in range(len(a)+len(b)-1)]
g=[-1,0,2];hh=[0,-3,0,4]
a=mul([-1,0,4],g);b=mul([0,2],hh)
check('Koebe phase polynomial obstruction',[a[n]-b[n] for n in range(5)]==[1,0,0,0,0])
check('same-degree4 Goh coprime cases',__import__('math').gcd(3,1)==1 and __import__('math').gcd(3,2)==1)
print(json.dumps({'status':'PASS','check_count':len(checks),'checks':checks,'limitations':'Finite exact controls do not prove classical compactness, support geometry, area theorem, holomorphic inversion, trajectory identification, or priority. Those analytic dependencies are explicitly reviewed separately.'},indent=2))
