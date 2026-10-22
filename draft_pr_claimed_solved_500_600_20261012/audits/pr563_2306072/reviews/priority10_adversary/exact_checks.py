"""Independent finite algebra controls. Does not certify extremality or priority."""
from dataclasses import dataclass
from fractions import Fraction as F
import json
from pathlib import Path

@dataclass(frozen=True)
class G:
    re: F = F(0)
    im: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))
    @staticmethod
    def of(x):
        return x if isinstance(x, G) else G(x)
    def __add__(self, other):
        b=G.of(other)
        return G(self.re+b.re, self.im+b.im)
    __radd__=__add__
    def __neg__(self):
        return G(-self.re,-self.im)
    def __sub__(self, other):
        return self+-G.of(other)
    def __rsub__(self, other):
        return G.of(other)+-self
    def __mul__(self, other):
        b=G.of(other)
        return G(self.re*b.re-self.im*b.im,self.re*b.im+self.im*b.re)
    __rmul__=__mul__
    def __truediv__(self, other):
        b=G.of(other)
        n=b.re*b.re+b.im*b.im
        return self*G(b.re/n,-b.im/n)
    def __pow__(self, n):
        assert n>=0
        result=G(1)
        for _ in range(n):
            result=result*self
        return result

def padd(a,b):
    return [G.of(a[j] if j<len(a) else 0)+G.of(b[j] if j<len(b) else 0)
            for j in range(max(len(a),len(b)))]
def pmul(a,b):
    out=[G() for _ in range(len(a)+len(b)-1)]
    for j,x in enumerate(a):
        for k,y in enumerate(b):
            out[j+k]=out[j+k]+G.of(x)*G.of(y)
    return out
def pscale(a,b):
    return [G.of(x)*b for x in a]
def pdiff(a):
    return [j*G.of(a[j]) for j in range(1,len(a))]
def peval(a,x):
    out=G()
    for y in a[::-1]:
        out=out*x+y
    return out

checks=[]
def check(name, test, details=None):
    if not test:
        raise AssertionError(name)
    checks.append({'name':name,'pass':True,'details':details})

epsilon=F(1,10**24)
eta=F(1,10**12)
T=F(7,4)
check('epsilon is eta squared',epsilon==eta**2)
q=lambda t:t*t-F(2,5)*t**4
check('q(1)',q(F(1))==F(3,5))
check('q(T)',q(T)==-F(441,640))
check('positive sign margin',q(F(1))-2000*eta>F(1,2))
check('negative sign margin',q(T)+2000*eta<-F(1,2))
check('actual tip below 3/10',F(7,25)+7*eta<F(3,10))
check('witness above tip with gap',F(25,81)-F(3,10)==F(7,810))
check('V witness radius control',T+333*epsilon<F(9,5))
check('orientation control',(222*epsilon)/(1-111*epsilon)<223*epsilon<1)
check('sqrt quadratic cost',(F(111**2,2))*eta<1)
check('inverse quadratic cost',18315*eta<1)
check('derivative quadratic cost',45621*eta<1)
check('Z error absorption',1541*epsilon*eta+4662*epsilon**2<2000*epsilon*eta)
check('Q numerator dominance for quarter radius',32*epsilon<1-3*epsilon)
check('nonzero quadratic discriminant margin',28*epsilon**2<4*epsilon)
check('Koebe nonrationality obstruction margin',1-12*eta>0)

# Direct coefficient extraction in several exact Gaussian-rational instances.
# The generic coefficient formulas are proved by formal expansion in REPORT.md.
for j,(a2,a3,a4,w) in enumerate([
    (G(2),G(3),G(4),G(-2,1)),
    (G(F(3,2),F(1,7)),G(F(2,3),F(-3,5)),G(F(8,9),F(1,11)),G(F(7,4),F(-2,3))),
    (G(-1,1),G(2,-3),G(4,5),G(-2,-1)),
]):
    f=[G(0),G(1),a2,a3,a4]
    f2=pmul(f,f);f3=pmul(f2,f);f4=pmul(f3,f)
    s=padd(padd(pscale(f2,-G(1)/w),pscale(f3,-G(1)/(w**2))),pscale(f4,-G(1)/(w**3)))
    check(f'coefficient z2 instance {j}',s[2]==-G(1)/w)
    check(f'coefficient z3 instance {j}',s[3]==-2*a2/w-G(1)/(w**2))
    check(f'coefficient z4 instance {j}',s[4]==-(2*a3+a2**2)/w-3*a2/(w**2)-G(1)/(w**3))
    ie=G(0,epsilon)
    expected=-(G(1)+ie*(2*a3+a2**2-6*a2))/w-ie*(3*a2-3)/(w**2)-ie/(w**3)
    check(f'candidate Phi instance {j}',s[2]+ie*(s[4]-3*s[3])==expected)

# Correct tangent quotient: g=tau*w, w'= (tau*g'-g)/tau^2.
# Exact diagnostic is auxiliary algebra only, without a support assertion.
tau=F(1,2)
g=[G(1),G(0,1),G(1)]
gv=peval(g,tau);gp=peval(pdiff(g),tau);gpp=peval(pdiff(pdiff(g)),tau)
correct=tau*gpp/(tau*gp-gv)-G(2)/tau
wp=G(1)-G(1)/(tau**2)
wpp=G(2)/(tau**3)
check('correct quotient identity at diagnostic',correct==wpp/wp)
check('printed g double-prime over g prime discrepancy',(gpp/gp).im==-1 and correct.im==0)

# Exact independent verification of priority08's later-read polynomial witness.
# The missing local case itself was derived before priority08 was read.
P=padd([G(0,1)],pmul([G(1),G(-2),G(1)],[G(0,-1),G(2,F(3,2)),G(-1,F(-1,2))]))
Pd=pdiff(P);Pdd=pdiff(Pd)
check('ZM P simple zero at origin',peval(P,G(0))==G(0) and peval(Pd,G(0))!=G(0))
check('ZM nonzero level equal at omega and u0',peval(P,G(1))==peval(P,G(2))==G(0,1))
check('ZM u0 derivative nonzero',peval(Pd,G(2))==G(-2,F(-1,2)))
check('ZM double level-value zero at omega',peval(Pd,G(1))==G(0) and peval(Pdd,G(1))==G(2))
alpha=F(1);m=0;k=2
check('ZM two compatible local orders',m*alpha+2*(alpha-1)==0 and k*alpha+2*(alpha-1)==2)

# Outward half-lines: phi is constant, theta'=-y/D, beta'=y/D.
for y in [F(-1),F(0),F(1)]:
    x=F(2);s=F(3,7);w=G(x+s,y)
    theta=(G(1)/w).im
    D=(x+s)**2+y*y
    check(f'halfline theta derivative y={y}',theta==-y/D)
    check(f'halfline radial derivative y={y}',-theta==y/D)

# Origin composition retains a nonzero highest fourth coefficient.
phi=[G(0),G(F(2,3)),G(F(1,7),F(1,11)),G(F(-2,5)),G(F(1,13))]
phi2=pmul(phi,phi);phi3=pmul(phi2,phi);phi4=pmul(phi3,phi)
check('composition fourth coefficient',G(0,epsilon)*phi4[4]==G(0,epsilon)*phi[1]**4!=G(0))

record={'scope':'Finite exact controls supplement the written proof; no classical theorem, actual extremality, universal priority, or package acceptance certification.',
        'arithmetic':'Python standard-library rational Gaussian pairs',
        'count':len(checks),'all_pass':True,'checks':checks}
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'count':len(checks),'all_pass':True}))
