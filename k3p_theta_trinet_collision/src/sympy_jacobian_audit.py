#!/usr/bin/env python3
"""Optional independent SymPy reconstruction of the selected Jacobian determinant.

This optional audit requires SymPy and is not used by the dependency-free verifier.
"""
import sympy as sp
from itertools import product
h=sp.symbols('h')
# variables
rxC,rxG,rxT = sp.symbols('rxC rxG rxT')
uG=sp.symbols('uG')
pr2C,pr2G,qr2C,qr2G,pr3C,pr3G,qr3C,qr3G=sp.symbols('pr2C pr2G qr2C qr2G pr3C pr3G qr3C qr3G')
yT,zT,d3=sp.symbols('yT zT d3')
cols=[rxC,rxG,rxT,uG,pr2C,pr2G,qr2C,qr2G,pr3C,pr3G,qr3C,qr3G,yT,zT,d3]
# group indices 0 A,1 C,2 G,3 T; xor
K=[1,sp.Rational(1,2),sp.Rational(1,2),sp.Rational(1,2)]
RX=[1,rxC,rxG,rxT]
RU=K
U=[1,h/3,uG,sp.Rational(1,3)]
V=[1,h,h/3,sp.Rational(1,3)]
PR2=[1,pr2C,pr2G,sp.Rational(3,10)]
QR2=[1,qr2C,qr2G,sp.Rational(3,10)]
PR3=[1,pr3C,pr3G,sp.Rational(3,10)]
QR3=[1,qr3C,qr3G,sp.Rational(3,10)]
Y=[1,sp.Rational(1,2),sp.Rational(1,2),yT]
Z=[1,sp.Rational(1,2),sp.Rational(1,2),zT]
d2=sp.Rational(1,2)

def core(y,z):
    x=y^z
    return (
        d2*d3 * PR2[y]*PR3[z]*U[x]
        + d2*(1-d3) * PR2[y]*QR3[z]*U[y]*V[z]
        + (1-d2)*d3 * QR2[y]*PR3[z]*U[z]*V[y]
        + (1-d2)*(1-d3) * QR2[y]*QR3[z]*V[x]
    )

def q(x,y,z):
    if x^y^z: return sp.Integer(0)
    return RX[x]*RU[x]*Y[y]*Z[z]*core(y,z)

subs={
 rxC:sp.Rational(1,2), rxG:sp.Rational(1,2), rxT:sp.Rational(1,2),
 uG:h,
 pr2C:3*h**2/4,pr2G:sp.Rational(1,4),
 qr2C:sp.Rational(1,4),qr2G:3*h**2/4,
 pr3C:3*h**2/4,pr3G:sp.Rational(1,4),
 qr3C:sp.Rational(1,4),qr3G:3*h**2/4,
 yT:sp.Rational(1,2),zT:sp.Rational(1,2),d3:sp.Rational(1,2)
}
# row lex x,y,z
rows=[(x,y,z) for x,y,z in product(range(4),repeat=3) if x^y^z==0 and (x,y,z)!=(0,0,0)]
print('rows',rows)
J=sp.Matrix([[sp.diff(q(*r),c).subs(subs) for c in cols] for r in rows])
print('computing det...')
det=sp.factor(J.det(method='domain-ge'))
print('raw factor=',det)
# reduce h^4=1/5
num,den=sp.fraction(det)
rem=sp.rem(sp.Poly(num,h,domain=sp.QQ),sp.Poly(5*h**4-1,h,domain=sp.QQ)).as_expr()/den
rem=sp.factor(rem)
print('reduced=',rem)
candidate=h*(10*h**2+1)/(2**61*3**4*5**14)
print('candidate=',candidate)
print('ratio reduced=',sp.factor(sp.rem(sp.Poly(sp.together(rem/candidate).as_numer_denom()[0],h,domain=sp.QQ),sp.Poly(5*h**4-1,h,domain=sp.QQ)).as_expr()/sp.together(rem/candidate).as_numer_denom()[1]))
# direct difference modulo
expr=sp.together(rem-candidate)
n,d=expr.as_numer_denom(); print('diff rem',sp.rem(sp.Poly(n,h,domain=sp.QQ),sp.Poly(5*h**4-1,h,domain=sp.QQ)).as_expr())
print('numeric det',sp.N(rem.subs(h,5**(-sp.Rational(1,4))),30))
print('candidate numeric',sp.N(candidate.subs(h,5**(-sp.Rational(1,4))),30))
