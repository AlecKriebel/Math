import sympy as S
from datetime import datetime,timezone
r=S.sqrt(5);phi=(1+r)/2;c=phi**5;d=5+2*r
L,z,x=S.symbols('L z x')
def zero(name,e):
    assert S.cancel(e,extension=r)==0,(name,e)
    print('EXACT ZERO:',name,flush=True)
print('UTC_START',datetime.now(timezone.utc).isoformat(),flush=True)
alpha=1-r/5;gamma=2*r/5
a=40+20*r+8*L;b=a+5;t=z-d
X=(b-t*t)/(a+4*r*t)
A=10*X+5*phi+L;h=4*X*X+2*X-1
zero('denominator unification',a+4*r*t-4*r*(z+gamma*L))
zero('simplified X(z)',X-(-z*z+2*d*z+8*L)/(4*r*(z+gamma*L)))
print('A in z factored',S.factor(A,extension=r),flush=True)
print('h in z factored',S.factor(h,extension=r),flush=True)
F=z**3-((3+r)*L+40+20*r)*z*z+((60+36*r)*L+900+400*r)*z+(48+16*r)*L*L+(500+220*r)*L
zero('F at vertex factor',F.subs(z,0)-16*(3+r)*L*(L+(25+10*r)/4))
beta=(11-5*r)*L/(2*(L+5*r))
zero('beta equals negative c reciprocal parameter',beta+L/(c*(L+5*r)))
zero('Tate nonsingular exact factor',beta*beta-11*beta-1+125*(L+c)/(c*(L+5*r)**2))
zero('Tate elliptic discriminant factor',beta**5*(beta*beta-11*beta-1)-125*L**5*(L+c)/(c**6*(L+5*r)**7))
q=d*(4*(L+5*r)/r)**2
a3=(-112+48*r)*L*L*(L+5*r)/5
st=a3/(q*(x-beta));zt=st-alpha*L
zero('torsion inverse transverse divisor identity',zt+gamma*L-(gamma-alpha)*L*x/(x-beta))
zero('torsion inverse X denominator identity',a+4*r*(zt-d)-4*r*(zt+gamma*L))
print('UTC_END',datetime.now(timezone.utc).isoformat(),flush=True)
