#!/usr/bin/env python3
"""Independent first-read algebra checks; no candidate supplement code is used.

Standard-library exact sparse polynomials over Q(sqrt(5)); two indeterminates.
These are selected falsification checks, not a full manuscript verification.
"""
from fractions import Fraction as F

class Q5:
    def __init__(self, a=0, b=0):
        if isinstance(a,Q5): self.a,self.b=a.a,a.b
        else: self.a,self.b=F(a),F(b)
    def __add__(self,o):
        o=Q5(o); return Q5(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return Q5(-self.a,-self.b)
    def __sub__(self,o): return self+-Q5(o)
    def __rsub__(self,o): return Q5(o)+-self
    def __mul__(self,o):
        if isinstance(o,Poly): return o*self
        o=Q5(o); return Q5(self.a*o.a+5*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def inverse(self):
        norm=self.a*self.a-5*self.b*self.b
        if not norm: raise ZeroDivisionError
        return Q5(self.a/norm,-self.b/norm)
    def __truediv__(self,o): return self*Q5(o).inverse()
    def __pow__(self,n):
        if n<0: return self.inverse()**(-n)
        v=Q5(1)
        for _ in range(n): v=v*self
        return v
    def __bool__(self): return bool(self.a or self.b)
    def __eq__(self,o):
        o=Q5(o); return self.a==o.a and self.b==o.b
    def __repr__(self): return f"({self.a})+({self.b})*sqrt5"

class Poly:
    def __init__(self,o=0):
        if isinstance(o,Poly): self.d=dict(o.d)
        elif isinstance(o,dict): self.d={k:Q5(v) for k,v in o.items() if Q5(v)}
        else: self.d={(0,0):Q5(o)} if Q5(o) else {}
    def __add__(self,o):
        o=Poly(o); d=dict(self.d)
        for k,v in o.d.items(): d[k]=d.get(k,Q5())+v
        return Poly(d)
    __radd__=__add__
    def __neg__(self): return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,o): return self+-Poly(o)
    def __rsub__(self,o): return Poly(o)+-self
    def __mul__(self,o):
        o=Poly(o); d={}
        for (i,j),a in self.d.items():
            for (k,l),b in o.d.items():
                e=(i+k,j+l); d[e]=d.get(e,Q5())+a*b
        return Poly(d)
    __rmul__=__mul__
    def __pow__(self,n):
        if n<0: raise ValueError
        v=Poly(1)
        for _ in range(n): v=v*self
        return v
    def subs(self,i,value):
        value=Poly(value); out=Poly()
        for exponent,coeff in self.d.items():
            keep=list(exponent); keep[i]=0
            out=out+Poly({tuple(keep):coeff})*value**exponent[i]
        return out
    def coefficient(self,i,j): return self.d.get((i,j),Q5())
    def __bool__(self): return bool(self.d)

def zero(name,p):
    if p:
        print("FAIL",name,repr(p.d)); raise SystemExit(1)
    print("EXACT_ZERO",name)

r=Q5(0,1); phi=(1+r)/2; c=phi**5; d=5+2*r
la=Poly({(1,0):1}); x=Poly({(0,1):1})
A=10*x+5*phi+la
B=-20*x**3+2*(5*phi+la)*x**2-5*phi**3-2*la
C=2*x**5+(5*phi+la)*x**4-(5*phi**3+2*la)*x**2+c+la
h=4*x**2+2*x-1; a=40+20*r+8*la; b=a+5
zero("quartic_discriminant_factor",B**2-4*A*C-h**2*(20*x**2-a*x+b))
zero("conic_discriminant",a**2-80*b-64*la*(la+5*r))
x0=-(5*phi+la)*Q5(F(1,10))
zero("vertical_component_B",B.subs(1,x0)-la*(la+5*r)*(la+5*(phi+1))*Q5(F(1,25)))
zero("vertical_component_C_exception",C.subs(1,Q5(F(1,2))).subs(0,-5*(phi+1))+1)

alpha=1-r/5; gamma=2*r/5; m=5-2*r
fc2=-((3+r)*la+40+20*r)
fc1=(60+36*r)*la+900+400*r
fc0=(48+16*r)*la**2+(500+220*r)*la
fz=x**3+fc2*x**2+fc1*x+fc0
zero("F_at_negative_alpha_lambda",fz.subs(1,-alpha*la)-(-Q5(F(16,5))+Q5(F(16,25))*r)*la**2*(la+5*r))
discF=fc2**2*fc1**2-4*fc1**3-4*fc2**3*fc0-27*fc0**2+18*fc2*fc1*fc0
zero("F_discriminant",discF-(24064+10752*r)*la*(la+5*r)**3*(la+c))
a0=m; a1=(-26+10*r)*la-20*r
a2=(42-Q5(F(86,5))*r)*la**2+(-100+100*r)*la+500+200*r
a3=(-112+48*r)*la**2*(la+5*r)*Q5(F(1,5))
zero("shifted_F_cubic_coefficients",m*fz.subs(1,x-alpha*la)-(a0*x**3+a1*x**2+a2*x+a3))
bc=a1*a3; cc=a0*a3**2
discW=16*(a2**2*bc**2-4*bc**3-4*a2**3*cc-27*cc**2+18*a2*bc*cc)
zero("cubic_discriminant",discW-2**24*(161-72*r)*la**5*(la+5*r)**5*(la+c))

N=(11-5*r)*la; D=2*(la+5*r)
k=(la+5*r)*Q5(4)/r; q=d*k**2
xi_num=q*(D*x-N)
Tnum=4*D**2*x**3+(N**2-6*N*D+D**2)*x**2+2*(N**2-N*D)*x+N**2
zero("Tate_twist_cleared_denominators",4*(xi_num**3+a2*xi_num**2*D+a1*a3*xi_num*D**2+a0*a3**2*D**3)-q**3*D*Tnum)
zero("iota_beta",(c*N+D)*(la+c)+(N-c*D))
zero("Morton_radical",(-2*N+(11+5*r)*D)-c*(la+c)*(2*N+(-11+5*r)*D))
zero("Verdure_radical",(N-c*D)+c*(la+c)*(N+c**(-1)*D))

tau=x
f=tau**4+3*tau**3+4*tau**2+2*tau+1
g=tau**4-2*tau**3+4*tau**2-3*tau+1
top=phi*tau+1; bot=tau-phi
zero("Fisher_cover_fraction_identity",tau*f*(top**5-c*bot**5)-g*(c*top**5+bot**5))

# A fresh ring interpretation: first variable beta, second variable x.
be=la
b2=be**2-6*be+1; b4=be**2-be; b6=be**2; b8=-be**3
T=4*x**3+b2*x**2+2*b4*x+b6
psi3=3*x**4+b2*x**3+3*b4*x**2+3*b6*x+b8
H6=2*x**6+b2*x**5+5*b4*x**4+10*b6*x**3+10*b8*x**2+(b2*b8-b4*b6)*x+b4*b8-b6**2
coeff=[5*be**8,10*be**7*(be-3),5*be**6*(2*be**2-13*be+16),
       5*be**5*(be**3-10*be**2+36*be-25),
       be**4*(be**4-12*be**3+94*be**2-293*be+126),
       be**3*(be**4+3*be**3-71*be**2+322*be-84),
       be**2*(be**4+3*be**3+19*be**2-248*be+36),
       be*(be**4+3*be**3-26*be**2+127*be-9),
       be**4-7*be**3+44*be**2-38*be+1,5*(be**2-5*be+1),Poly(5)]
R=sum((co*x**j for j,co in enumerate(coeff)),Poly())
zero("all_residual_coefficients",T**2*H6-psi3**3-x*(x-be)*R)
zero("residual_at_zero",R.subs(1,0)-5*be**8)
zero("residual_at_beta",R.subs(1,be)-5*be**12)

# At the unit-circle vertex (1,0), check the cusp's first nonzero jet.
u=la; v=x; xx=1+u
P=2*(xx**5-10*xx**3*v**2+5*xx*v**4)+5*phi*(xx**2+v**2)**2-5*phi**3*(xx**2+v**2)+c
Q=xx**2+v**2-1
lc=-(25+10*r)/4
G=P+lc*Q**2
assert all(not G.coefficient(i,j) for i,j in [(0,0),(1,0),(0,1),(2,0),(1,1)])
assert G.coefficient(0,2)==-25 and G.coefficient(3,0)==5
print("EXACT_CUSP_JET vertex=(1,0) tangent=-25*v^2, kernel-cubic=5*u^3")
print("LIMITATION selected algebraic identities only; no source theorem, resultants, full normalization, all-fiber field proof, priority, or package verification certified")
