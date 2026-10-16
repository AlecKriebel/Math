#!/usr/bin/env python3
"""Supplemental exact arithmetic checks; not a formal proof of analytic inputs."""
from fractions import Fraction as F
import json
E=F(1,10**24); H=F(1,10**12)
checks={}
def ck(name, condition):
    assert condition, name
    checks[name]=True
r=F(2,3); T=F(7,4)
ck('epsilon equals eta squared', E==H*H)
ck('H plus H0 bound used implicitly in proof', F(10,3)+5*H<F(7,2))
ck('H reciprocal cube numerator bound', 4+F(10,3)+F(25,9)<11)
ck('sharp elementary H derivative numerator', 5+F(4,3)*10<F(19))
ck('conformal radius at minus two thirds', (1-r*r)*F(9,125)==F(1,25))
ck('tip bound remains strictly below 3/10', F(7,25)+7*H<F(3,10))
ck('strict gap between trajectory and tip gates', F(25,81)-F(3,10)==F(7,810)>0)
ck('trajectory extends beyond second test point in inverse domain', T<2)
ck('square root disk avoids zero', 111*E<1)
ck('square-root derivative Taylor remainder bounded by 2', F(3,8)**2*F(4,3)**5<4)
ck('polynomial derivative d bound', 1+F(3,2)*9+F(1,2)*81==55)
ck('integrated square root remainder', 3*(161+F(111**2,2)*H)<486)
ck('inversion error strictly below 487', 486+55*333*H<487)
ck('inverse derivative remainder strictly below 162', 161+(2*111**2+F(126,2)*333)*H<162)
ck('Z numerator error constants', 2*(T*162+487)==1541 and 2*7*333==4662)
ck('Z total error strictly below advertised budget', 1541+4662*H<2000)
q=lambda t:t*t-F(2,5)*t**4
ck('first endpoint margin', q(F(1))-2000*H>F(1,2))
ck('second endpoint margin', q(T)+2000*H<-F(1,2))
ck('positive real part margin', 1-2000*E*H>0)
# Supplemental exact constants for the local, eventual-monotonicity crosscheck.
ck('A has modulus less than 3', 2+106*H<3)
D=3*E
ck('a reciprocal square differs from 1 by less than 7 epsilon', D*(2+D)/(1-D)**2<7*E)
ck('B over a squared differs from 3 by less than 25 eta', 24*H/(1-D)**2+21*E<25*H)
ck('near-infinity radial-angle leading coefficient is positive', 3-25*H>0)
print(json.dumps({'status':'passed','checks_passed':len(checks),'checks':checks,'scope':'Supplemental rational margins only; analytic reasoning is in INDEPENDENT_AUDIT.md.'},indent=2))
