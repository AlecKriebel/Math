"""Fresh exact geometry certificates; no candidate supplement imports."""
import sympy as S
from datetime import datetime, timezone

r = S.sqrt(5)
phi = (1+r)/2
c = phi**5
d = 5+2*r
X,Y,T,l,t,z,s,x,eta,xi,u,v,Z,W,jeta = S.symbols('X Y T lambda t z s x eta xi u v Z W jeta')
K = S.QQ.algebraic_field(r)

def canon(e):
    return S.cancel(e, extension=r)

def zero(name,e):
    e = canon(e)
    assert e == 0, (name, e)
    print('EXACT ZERO:', name, flush=True)

def show(name,e):
    print(name, '=', canon(e), flush=True)

print('UTC_START', datetime.now(timezone.utc).isoformat(), flush=True)
print('SYMPY', S.__version__, flush=True)
print('DOMAIN Q(sqrt(5)) in characteristic zero; all identity assertions are symbolic.', flush=True)

Q = X**2+Y**2-T**2
P = 2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*phi*(X**2+Y**2)**2*T-5*phi**3*(X**2+Y**2)*T**3+c*T**5
cyclo = jeta**4+jeta**3+jeta**2+jeta+1
lineprod = S.prod(Z+jeta**(2*j+1)*W-(1+jeta)*jeta**j*T for j in range(5))
cyclophi = 1+jeta+jeta**4
Pzw = Z**5+W**5+5*cyclophi*Z**2*W**2*T-5*cyclophi**3*Z*W*T**3+cyclophi**5*T**5
rem = S.rem(S.Poly(S.expand(lineprod-Pzw),jeta), S.Poly(cyclo,jeta)).as_expr()
assert S.expand(rem) == 0
print('EXACT ZERO: cyclotomic five-line product in Q[Z,W,T,jeta]/Phi5', flush=True)
for j in range(5):
    line = Z+jeta**(2*j+1)*W-(1+jeta)*jeta**j*T
    for k in [j,j+1]:
        ev = line.subs({Z:jeta**k,W:jeta**((5-k)%5),T:1})
        assert S.rem(S.Poly(S.expand(ev),jeta),S.Poly(cyclo,jeta)).as_expr()==0
print('EXACT ZERO: each line vanishes at its two consecutive unit-circle vertices', flush=True)
zero('real-coordinate expansion', P-(Z**5+W**5+5*phi*Z**2*W**2*T-5*phi**3*Z*W*T**3+c*T**5).subs({Z:X+S.I*Y,W:X-S.I*Y}))
zero('phi cyclotomic quadratic', S.rem(S.Poly(cyclophi**2-cyclophi-1,jeta),S.Poly(cyclo,jeta)).as_expr())
A=10*X+5*phi+l
B=-20*X**3+2*(5*phi+l)*X**2-5*phi**3-2*l
C=2*X**5+(5*phi+l)*X**4-(5*phi**3+2*l)*X**2+c+l
G=A*Y**4+B*Y**2+C
zero('affine quartic equals homogeneous pencil in chart T=1',G-(P+l*T*Q**2).subs(T,1))
h=4*X**2+2*X-1
a=40+20*r+8*l
b=a+5
D=20*X**2-a*X+b
zero('quartic-in-Y squared discriminant', B**2-4*A*C-h**2*D)
zero('conic discriminant', a*a-80*b-64*l*(l+5*r))
Xt=(b-t*t)/(a+4*r*t)
Vt=t+2*r*Xt
zero('parametric conic', Vt**2-D.subs(X,Xt))
zero('conic inverse identity', b-t*t-X*(a+4*r*t)-(D-(t+2*r*X)**2))
Ut=canon((-B.subs(X,Xt)+h.subs(X,Xt)*Vt)/(2*A.subs(X,Xt)))
alpha=1-r/5
gamma=2*r/5
m=5-2*r
F=z**3-((3+r)*l+40+20*r)*z**2+((60+36*r)*l+900+400*r)*z+(48+16*r)*l**2+(500+220*r)*l
Uformula=m*z*z*F/(400*(z+gamma*l)**2*(z+alpha*l))
zero('double-cover Y squared full rational identity',Ut-Uformula.subs(z,t+d))
zero('reverse same conic branch', (2*A.subs(X,Xt)*Ut+B.subs(X,Xt))/h.subs(X,Xt)-Vt)
tforward=(2*A*Y*Y+B)/h-2*r*X
zero('forward/recovered X defining identity',b-tforward*tforward-X*(a+4*r*tforward)+4*A*G/h**2)
a0=m
a1=(-26+10*r)*l-20*r
a2=(42-86*r/5)*l*l+(-100+100*r)*l+500+200*r
a3=(-112+48*r)*l*l*(l+5*r)/5
zero('shifted cubic coefficient identity',m*F.subs(z,s-alpha*l)-(a0*s**3+a1*s**2+a2*s+a3))
Wpoly=xi**3+a2*xi**2+a1*a3*xi+a0*a3*a3
zero('cubic from double-cover', Wpoly.subs(xi,a3/s)-(a3/s)**2*m*F.subs(z,s-alpha*l)/s)
zero('F at branch s zero', F.subs(z,-alpha*l)-(-S.Rational(16,5)+16*r/25)*l*l*(l+5*r))
zero('F discriminant',S.discriminant(F,z)-(24064+10752*r)*l*(l+5*r)**3*(l+c))
zero('W elliptic discriminant',16*S.discriminant(Wpoly,xi)-2**24*(161-72*r)*l**5*(l+5*r)**5*(l+c))
X0=-(5*phi+l)/10
zero('B at only A root',B.subs(X,X0)-l*(l+5*r)*(l+5*(phi+1))/25)
zero('vertical exceptional X0',X0.subs(l,-5*(phi+1))-S.Rational(1,2))
zero('vertical exceptional C',C.subs({X:S.Rational(1,2),l:-5*(phi+1)})+1)
phic=(1-r)/2
Pc=2*(X**5-10*X**3*Y**2+5*X*Y**4)+5*phic*(X**2+Y**2)**2*T-5*phic**3*(X**2+Y**2)*T**3+phic**5*T**5
zero('excluded minus5sqrt5 conjugate line product',P-5*r*T*Q**2-Pc)
Fminus=canon(F.subs(l,-c).subs(z,s-alpha*(-c)))
gcdminus=S.Poly(Fminus,s,domain=K).gcd(S.Poly(S.diff(Fminus,s),s,domain=K)).monic().as_expr()
zero('excluded minus c repeated root gcd',gcdminus-(s-1-3*r/5))
print('EXCLUDED_MINUS_C_SHIFTED_F_FACTORS',S.factor(Fminus,extension=r),flush=True)
show('EXCLUDED_MINUS_C_CONIC_DISCRIMINANT',(a*a-80*b).subs(l,-c))
show('EXCLUDED_MINUS_C_F_AT_S_ZERO',Fminus.subs(s,0))
centerjet=S.Poly(S.expand(G.subs(l,-c)),X,Y,domain=K)
centerq=sum(co*X**ij[0]*Y**ij[1] for ij,co in centerjet.terms() if sum(ij)==2)
zero('center node quadratic form at minus c',centerq-X**2-Y**2)
Gc=G.subs({X:1+u,Y:v})
local=S.Poly(S.expand(Gc),u,v,domain=K.poly_ring(l))
local0=sum(co*u**ij[0]*v**ij[1] for ij,co in local.terms() if sum(ij)<=1)
local2=sum(co*u**ij[0]*v**ij[1] for ij,co in local.terms() if sum(ij)==2)
zero('vertex constant and linear jets',local0)
zero('vertex quadratic jet',local2-((25+10*r+4*l)*u*u-25*v*v))
cusp=-(25+10*r)/4
kernel3=S.Poly(S.expand(Gc.subs({l:cusp,v:0})),u,domain=K).coeff_monomial(u**3)
zero('cusp kernel cubic equals five',kernel3-5)
show('cusp allowed differences', (cusp+c))
Rinf=P.subs(T,0)
zero('infinity restriction',Rinf-2*X*(X**4-10*X**2*Y**2+5*Y**4))
assert S.Poly(Rinf.subs(Y,1),X,domain=K).gcd(S.Poly(S.diff(Rinf.subs(Y,1),X),X,domain=K)).degree()==0
print('EXACT: infinity binary quintic is squarefree, all five points smooth for every lambda',flush=True)
zero('origin X partial ten',S.diff(P+l*T*Q**2,X).subs({X:0,Y:1,T:0})-10)
zero('origin inverse denominator a4rt', (a+4*r*t).subs(t,-alpha*l-d)-4*(3-r)*l)
zero('origin finite X value',Xt.subs(t,-alpha*l-d)-X0)
zero('origin transverse denominator',(-alpha*l+gamma*l)-(gamma-alpha)*l)
beta=(11-5*r)*l/(2*(l+5*r))
k=4*(l+5*r)/r
q=d*k*k
Tb=4*x**3+(beta*beta-6*beta+1)*x*x+2*(beta*beta-beta)*x+beta*beta
zero('actual cubic Tate twist identity',Wpoly.subs(xi,q*(x-beta))-q**3*Tb/4)
show('Tate discriminant pullback',beta**5*(beta*beta-11*beta-1))
show('beta nonsingular factor',beta*beta-11*beta-1)
print('UTC_END', datetime.now(timezone.utc).isoformat(), flush=True)
print('ALL ASSERTIONS ABOVE ARE UNIVERSAL EXACT IDENTITIES, NOT SAMPLE TESTS.',flush=True)
