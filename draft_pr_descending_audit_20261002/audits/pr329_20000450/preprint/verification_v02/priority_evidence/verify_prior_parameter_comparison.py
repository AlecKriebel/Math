"""Portable exact Verdure/Morton/Fisher/candidate convention comparison.

Standard library only; rational functions over Q(sqrt(5)). No private sources,
network, source-reading claims, earlier-application or priority certification.
"""
from fractions import Fraction as F
import json
import sys

if sys.flags.optimize:
    raise RuntimeError('Run without -O: exact comparisons require assertions enabled.')

class Q5:
    def __init__(self,a=0,b=0):self.a,self.b=F(a),F(b)
    @staticmethod
    def coerce(v):return v if isinstance(v,Q5) else Q5(v)
    def __add__(self,v):
        v=self.coerce(v);return Q5(self.a+v.a,self.b+v.b)
    __radd__=__add__
    def __neg__(self):return Q5(-self.a,-self.b)
    def __sub__(self,v):return self+-self.coerce(v)
    def __mul__(self,v):
        v=self.coerce(v);return Q5(self.a*v.a+5*self.b*v.b,self.a*v.b+self.b*v.a)
    __rmul__=__mul__
    def __bool__(self):return bool(self.a or self.b)

def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]:p.pop()
    return p

def padd(p,q):
    return trim([(p[i] if i<len(p) else Q5())+(q[i] if i<len(q) else Q5()) for i in range(max(len(p),len(q)))])

def pneg(p):return [-v for v in p]

def pmul(p,q):
    o=[Q5() for _ in range(len(p)+len(q)-1)]
    for i,a in enumerate(p):
        for j,b in enumerate(q):o[i+j]=o[i+j]+a*b
    return trim(o)

class R:
    def __init__(self,v=0,n=None,d=None):
        self.n=trim(n) if n is not None else [Q5.coerce(v)]
        self.d=trim(d) if d is not None else [Q5(1)]
        assert any(self.d),'zero polynomial denominator'
    @staticmethod
    def coerce(v):return v if isinstance(v,R) else R(v)
    def __add__(self,v):
        v=self.coerce(v);return R(n=padd(pmul(self.n,v.d),pmul(v.n,self.d)),d=pmul(self.d,v.d))
    __radd__=__add__
    def __neg__(self):return R(n=pneg(self.n),d=self.d)
    def __sub__(self,v):return self+-self.coerce(v)
    def __rsub__(self,v):return self.coerce(v)+-self
    def __mul__(self,v):
        v=self.coerce(v);return R(n=pmul(self.n,v.n),d=pmul(self.d,v.d))
    __rmul__=__mul__
    def __truediv__(self,v):
        v=self.coerce(v);return R(n=pmul(self.n,v.d),d=pmul(self.d,v.n))
    def __rtruediv__(self,v):return self.coerce(v)/self
    def __pow__(self,k):
        if k<0:return (1/self)**(-k)
        out=R(1)
        while k:
            if k%2:out=out*self
            self=self*self;k//=2
        return out

checks=[]
def equal(name,a,z=0):
    a=R.coerce(a);z=R.coerce(z)
    diff=padd(pmul(a.n,z.d),pneg(pmul(z.n,a.d)))
    assert not any(diff),name
    checks.append(name)

r=R(Q5(0,1));l=R(n=[Q5(),Q5(1)])
phi=(1+r)/2;c=(11+5*r)/2
beta=(11-5*r)*l/(2*(l+5*r))
epsilon=(r-1)/2;epsilon_bar=(-r-1)/2
equal('epsilon=phi^-1',epsilon,1/phi)
equal('epsilon_bar=-phi',epsilon_bar,-phi)
b=-beta
for name,a,z in [('a1',1+b,1-beta),('a2',b,-beta),('a3',b,-beta)]:
    equal('Morton/candidate '+name,a,z)
u5=(2*b+11+5*r)/(-2*b-11+5*r)
equal('Morton u^5 becomes phi^5(lambda+phi^5)',u5,c*(l+c))
equal('Morton equation(2.1) recovers b=-beta',
      (epsilon**5*c*(l+c)+epsilon_bar**5)/(c*(l+c)+1),-beta)
iota=lambda v:(c*v+1)/(v-c)
equal('candidate full-level Kummer value',iota(beta),-1/(l+c))
equal('Morton/candidate Kummer classes differ by phi^5 and inversion',u5,-c/iota(beta))
# Verdure Theorem 5 p84: choose zeta+zeta^-1=(sqrt(5)-1)/2.
alpha5=8+5*(r-1)/2;beta5=3-5*(r-1)/2
equal('Verdure alpha5=phi^5',alpha5,c)
equal('Verdure beta5=-phi^-5',beta5,-1/c)
verdure5=(beta-alpha5)/(beta-beta5)
equal('Verdure radical equals -phi^5(lambda+phi^5)',verdure5,-c*(l+c))
equal('Verdure/Morton radical ratio=-1=(-1)^5',verdure5/u5,-1)
f=l**4+3*l**3+4*l*l+2*l+1;g=l**4-2*l**3+4*l*l-3*l+1
eps=lambda v:(phi*v+1)/(v-phi)
equal('Fisher full-level coordinate identity',iota(eps(l)**5),l*f/g)
# Independent transcription: Morton section2 p5 D5, candidate TURN_1(20).
z=l;b=-z
mc=[5,5+25*b+5*b*b,1+38*b+44*b*b+7*b**3+b**4,
 9*b+127*b*b+26*b**3+3*b**4-b**5,
 36*b*b+248*b**3+19*b**4-3*b**5+b**6,
 84*b**3+322*b**4+71*b**5+3*b**6-b**7,
 126*b**4+293*b**5+94*b**6+12*b**7+b**8,
 125*b**5+180*b**6+50*b**7+5*b**8,
 80*b**6+65*b**7+10*b**8,30*b**7+10*b**8,5*b**8]
cc=[5,5*(z*z-5*z+1),z**4-7*z**3+44*z*z-38*z+1,
 z*(z**4+3*z**3-26*z*z+127*z-9),z*z*(z**4+3*z**3+19*z*z-248*z+36),
 z**3*(z**4+3*z**3-71*z*z+322*z-84),z**4*(z**4-12*z**3+94*z*z-293*z+126),
 5*z**5*(z**3-10*z*z+36*z-25),5*z**6*(2*z*z-13*z+16),10*z**7*(z-3),5*z**8]
for i,(a,v) in enumerate(zip(mc,cc)):
    equal('D5/R_beta coefficient x^'+str(10-i),a,v)
print(json.dumps({'result':'PASS','exact_comparisons':len(checks),'checks':checks,
 'bridge':'Verdure t=candidate beta, fifth-root=-phi theta; Morton b=-beta, u=phi theta; theta^5=lambda+phi^5',
 'scope':'symbolic convention/formula comparison; no claim of earlier explicit pentagonal application or first priority'},indent=2))
