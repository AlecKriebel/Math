#!/usr/bin/env python3
"""Optional independent SymPy reconstruction of the fixed-output IFT tangent identity.

This optional audit requires SymPy and is not used by the dependency-free verifier.
"""
import sympy as sp
from itertools import product
h=sp.symbols('h')
# pivot variables
rxC,rxG,rxT = sp.symbols('rxC rxG rxT')
uG=sp.symbols('uG')
pr2C,pr2G,qr2C,qr2G,pr3C,pr3G,qr3C,qr3G=sp.symbols('pr2C pr2G qr2C qr2G pr3C pr3G qr3C qr3G')
yT,zT,d3=sp.symbols('yT zT d3')
pivots=[rxC,rxG,rxT,uG,pr2C,pr2G,qr2C,qr2G,pr3C,pr3G,qr3C,qr3G,yT,zT,d3]
uC,vG=sp.symbols('uC vG')
K=[1,sp.Rational(1,2),sp.Rational(1,2),sp.Rational(1,2)]
RX=[1,rxC,rxG,rxT]; RU=K
U=[1,uC,uG,sp.Rational(1,3)]
V=[1,h,vG,sp.Rational(1,3)]
PR2=[1,pr2C,pr2G,sp.Rational(3,10)]
QR2=[1,qr2C,qr2G,sp.Rational(3,10)]
PR3=[1,pr3C,pr3G,sp.Rational(3,10)]
QR3=[1,qr3C,qr3G,sp.Rational(3,10)]
Y=[1,sp.Rational(1,2),sp.Rational(1,2),yT]
Z=[1,sp.Rational(1,2),sp.Rational(1,2),zT]
d2=sp.Rational(1,2)
def core(y,z):
 x=y^z
 return d2*d3*PR2[y]*PR3[z]*U[x] + d2*(1-d3)*PR2[y]*QR3[z]*U[y]*V[z] + (1-d2)*d3*QR2[y]*PR3[z]*U[z]*V[y]+(1-d2)*(1-d3)*QR2[y]*QR3[z]*V[x]
def q(x,y,z):
 return RX[x]*RU[x]*Y[y]*Z[z]*core(y,z) if not (x^y^z) else sp.Integer(0)
subs={rxC:sp.Rational(1,2),rxG:sp.Rational(1,2),rxT:sp.Rational(1,2),uC:h/3,uG:h,vG:h/3,
pr2C:3*h**2/4,pr2G:sp.Rational(1,4),qr2C:sp.Rational(1,4),qr2G:3*h**2/4,
pr3C:3*h**2/4,pr3G:sp.Rational(1,4),qr3C:sp.Rational(1,4),qr3G:3*h**2/4,
yT:sp.Rational(1,2),zT:sp.Rational(1,2),d3:sp.Rational(1,2)}
rows=[r for r in product(range(4),repeat=3) if (r[0]^r[1]^r[2])==0 and r!=(0,0,0)]
F=sp.Matrix([q(*r) for r in rows])
J=F.jacobian(pivots).subs(subs)
g=(F.diff(uC)+F.diff(vG)).subs(subs)
print('solving')
v=J.inv()*g # p' = - v
pprime=[-sp.factor(x) for x in v]
mod=sp.Poly(5*h**4-1,h,domain=sp.QQ)
def reduce_rat(expr):
 expr=sp.cancel(expr)
 num,den=sp.fraction(expr)
 # Need reduce rational function in number field. use invert den modulo polynomial.
 pn=sp.Poly(num,h,domain=sp.QQ)
 pd=sp.Poly(den,h,domain=sp.QQ)
 inv=sp.invert(pd,mod)
 rem=(pn*inv).rem(mod)
 return sp.factor(rem.as_expr())
for name,expr in zip([str(x) for x in pivots],pprime):
 red=reduce_rat(expr)
 print(name,'=',red)
print('uG target diff=',sp.factor(reduce_rat(pprime[3]-6/(1+10*h**2))))
# verify J pprime + g =0 mod
res=J*sp.Matrix(pprime)+g
print('max residual nonzero?')
for i,e in enumerate(res):
 r=reduce_rat(e)
 if r!=0: print(i,r)
# Derivative margins all edges maybe print relevant
u_margin_der=1-sp.Rational(1,3)*pprime[3]
print('U sat margin deriv',reduce_rat(u_margin_der))
print('V sat margin deriv',1)
