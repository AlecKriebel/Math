#!/usr/bin/env python3
"""Exact Fraction/Gaussian-rational checks, requiring only Python stdlib."""
from fractions import Fraction as F
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass(frozen=True)
class Q:
    re: F = F(0)
    im: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))
    def __add__(self, b):
        b = q(b); return Q(self.re+b.re, self.im+b.im)
    __radd__ = __add__
    def __neg__(self): return Q(-self.re, -self.im)
    def __sub__(self, b): return self + -q(b)
    def __rsub__(self, b): return q(b) + -self
    def __mul__(self, b):
        if hasattr(b,'d') or hasattr(b,'num'): return NotImplemented
        b=q(b); return Q(self.re*b.re-self.im*b.im,self.re*b.im+self.im*b.re)
    __rmul__ = __mul__
    def __truediv__(self, b):
        b=q(b); n=b.re*b.re+b.im*b.im
        return self*b.conj()*Q(1/n)
    def __rtruediv__(self,b): return q(b)/self
    def __pow__(self,n):
        if n<0:return (1/self)**(-n)
        out=Q(1)
        for _ in range(n):out=out*self
        return out
    def conj(self):return Q(self.re,-self.im)
    def norm2(self):return self.re*self.re+self.im*self.im
    def show(self):return {'re':str(self.re),'im':str(self.im)}

def q(a): return a if isinstance(a,Q) else Q(a)
I=Q(0,1)
N=7
ZERO=(0,)*N
names=['z','x','y','a2','a3','a4','eps']

class P:
    def __init__(self,d):self.d={k:q(v) for k,v in d.items() if q(v)!=Q()}
    def __add__(self,b):
        b=p(b);d=dict(self.d)
        for k,v in b.d.items():d[k]=d.get(k,Q())+v
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.d.items()})
    def __sub__(self,b):return self+-p(b)
    def __rsub__(self,b):return p(b)+-self
    def __mul__(self,b):
        b=p(b);d={}
        for k,v in self.d.items():
            for l,w in b.d.items():
                m=tuple(a+c for a,c in zip(k,l));d[m]=d.get(m,Q())+v*w
        return P(d)
    __rmul__=__mul__
    def __pow__(self,n):
        out=p(1)
        for _ in range(n):out=out*self
        return out
    def diff(self,j=0):
        out={}
        for k,v in self.d.items():
            if k[j]:
                l=list(k);l[j]-=1;out[tuple(l)]=v*k[j]
        return P(out)
    def coef(self,j,n):
        out={}
        for k,v in self.d.items():
            if k[j]==n:
                l=list(k);l[j]=0;out[tuple(l)]=v
        return P(out)
    def val(self,values):
        out=Q()
        for k,v in self.d.items():
            term=v
            for j,exp in enumerate(k):term=term*q(values[j])**exp
            out+=term
        return out

def p(v):return v if isinstance(v,P) else P({ZERO:q(v)})
def var(j):
    k=list(ZERO);k[j]=1;return P({tuple(k):Q(1)})

class R:
    def __init__(self,num,den=1):self.num=p(num);self.den=p(den)
    def __add__(self,b):
        b=r(b);return R(self.num*b.den+b.num*self.den,self.den*b.den)
    __radd__=__add__
    def __neg__(self):return R(-self.num,self.den)
    def __sub__(self,b):return self+-r(b)
    def __rsub__(self,b):return r(b)+-self
    def __mul__(self,b):
        b=r(b);return R(self.num*b.num,self.den*b.den)
    __rmul__=__mul__
    def __truediv__(self,b):
        b=r(b);return R(self.num*b.den,self.den*b.num)
    def __rtruediv__(self,b):return r(b)/self
    def __pow__(self,n):
        if n<0:return R(self.den,self.num)**(-n)
        return R(self.num**n,self.den**n)
    def diff(self):return R(self.num.diff()*self.den-self.num*self.den.diff(),self.den**2)
    def val(self,values):return self.num.val(values)/self.den.val(values)
    def conj(self):return R(P({k:v.conj() for k,v in self.num.d.items()}),P({k:v.conj() for k,v in self.den.d.items()}))

def r(v):return v if isinstance(v,R) else R(v)
def eq(a,b):
    a=r(a);b=r(b)
    return not (a.num*b.den-b.num*a.den).d
def must(name,condition,detail=None):
    assert condition,name
    checks.append({'name':name,'passed':True,'detail':detail})

checks=[]
z,x,y,a2,a3,a4,eps=[var(j) for j in range(N)]
k=R(z,(1-z)**2)
pk=R(z-(x+y)*z**2*F(1,2),(1-y*z)**2)
must('Pearce derivative, polynomial identity',eq(pk.diff(),R(1-x*z,(1-y*z)**3)))
h=R(-x,1-x*z)+R(3*y,1-y*z)
must('Pearce logarithmic derivative, polynomial identity',eq(pk.diff().diff()/pk.diff(),h))
sp=h.diff()-h*h*F(1,2)
sp_expected=R(-(x-y)**2*F(3,2),(1-x*z)**2*(1-y*z)**2)
must('Pearce Schwarzian, polynomial identity',eq(sp,sp_expected))
hk=R(1,1+z)+R(3,1-z)
sk=hk.diff()-hk*hk*F(1,2)
must('Koebe Schwarzian, polynomial identity',eq(sk,R(-6,(1-z*z)**2)))

# Exact coefficient extraction through degree four, with independent symbols.
f=z+a2*z**2+a3*z**3+a4*z**4
must('coefficient f^2 at 2',eq((f*f).coef(0,2),1))
must('coefficient f^2 at 3',eq((f*f).coef(0,3),2*a2))
must('coefficient f^2 at 4',eq((f*f).coef(0,4),2*a3+a2*a2))
must('coefficient f^3 at 3',eq((f**3).coef(0,3),1))
must('coefficient f^3 at 4',eq((f**3).coef(0,4),3*a2))
must('coefficient f^4 at 4',eq((f**4).coef(0,4),1))
A=2*a3+a2*a2-6*a2;B=3*a2-3
phi=R(-1,x)+I*R(eps)*(-R(2*a3+a2*a2,x)-R(3*a2,x*x)-R(1,x**3)+3*R(2*a2,x)+R(3,x*x))
must('degree-four functional produces candidate Phi',eq(phi,-R(1+I*eps*A,x)-R(I*eps*B,x*x)-R(I*eps,x**3)))

# General corrected identity for w=g/z. The source's g''/g' fails even on an
# exact Laurent half-line, without implying this auxiliary curve is a support.
g=r(1)+I*r(z)+r(z*z);w=g/r(z)
corrected=r(z)*g.diff().diff()/(r(z)*g.diff()-g)-2/r(z)
must('corrected tangent-at-infinity identity',eq(w.diff().diff()/w.diff(),corrected))
point=[F(1,2)]+[0]*6
actual=(w.diff().diff()/w.diff()).val(point)
printed=(g.diff().diff()/g.diff()).val(point)
must('printed 2007 formula has exact mismatch',actual.im==0 and printed.im==-1,{'actual':actual.show(),'printed':printed.show(),'tau':'1/2'})

# Exact Gaussian-rational evaluation of r Z_rtheta / Z, using logarithmic
# derivatives; no square roots, finite differences or floating point.
pearce_x=Q(F(-7,25),F(24,25));pearce_y=pearce_x.conj()
must('Pearce specialization unit parameters',pearce_x.norm2()==1 and pearce_y.norm2()==1)
test_functions=[('identity',r(z)),('Koebe',k),('Pearce',pk),('univalent small quadratic',r(z+z*z*F(1,10)))]
for fn,rf in test_functions:
    for zz in [Q(F(3,10),F(2,5)),Q(F(1,6),F(1,7))]:
        values=[zz,pearce_x,pearce_y,0,0,0,0]
        f0=rf.val(values);f1=rf.diff().val(values);f2=rf.diff().diff().val(values);f3=rf.diff().diff().diff().val(values)
        den=1+f0.norm2();NN=zz*f1*f0.conj();hh=zz*f2/f1
        aa=2*NN.re/den-1-hh.re
        bb=-2*NN.im/den+hh.im
        TD=-2*NN.im
        TN=I*(NN+zz*zz*f2*f0.conj()-zz.norm2()*f1.norm2())
        hp=(f3*f1-f2*f2)/(f1*f1)
        TA=2*TN.re/den-2*NN.re*TD/(den*den)+(hh+zz*zz*hp).im
        lhs=TA+aa*bb
        rhs=(zz*zz*(f3/f1-F(3,2)*(f2/f1)**2)).im
        must('spherical/Schwarzian exact identity '+fn+' at '+str(zz.show()),lhs==rhs,{'lhs':str(lhs),'rhs':str(rhs)})

e=F(1,10**24);eta=F(1,10**12)
qt=lambda t:t*t-F(2,5)*t**4
must('candidate reversal exact q(1)',qt(F(1))==F(3,5))
must('candidate reversal exact q(7/4)',qt(F(7,4))==F(-441,640))
must('candidate sign error margin',2000*eta<F(1,10))
must('candidate actual tip/segment radius gap',F(25,81)-F(3,10)==F(7,810))
must('candidate |A|<3, |B|<4 from stated uniform bounds',106*eta<1 and 24*eta<1)
must('candidate Q has no zeros for |w|>=1/4',32*e<1-3*e,{'reason':'|b|/r+|c|/r^2 <= 32 eps < |a| for r>=1/4'})
must('candidate two numerator zeros simple',16*e*e<4*e*(1-3*e),{'reason':'|b|^2<4|a c| implies b^2-4ac !=0; c !=0'})
must('candidate Schwarzian constant nonzero',1-61*eta>F(1,2),{'bound':'|a3-a2^2| > 1-61 eta > 1/2 > 3-2sqrt(2)'})
VV=r(z)+r(I*eps)*(r(z)+r(z**3)*F(1,2)-r(z**5)*F(1,10))
WW=-1/(VV**2);ZZ=r(z)*VV.diff()/VV
must('candidate exact angle ratio algebra',eq(WW.diff()/WW,-2*ZZ/r(z)) and eq(-WW.diff()/WW,2*ZZ/r(z)))

# Diagnostic of a geometric inference, NOT an actual support-point example.
# Conjugation here treats z as a real parameter s.
delta=F(1,1000)
aux=-r(z)+r(I*delta)*(1-1/(5*r(z)))
imag=lambda rr:(rr-rr.conj())/r(2*I)
aux_theta=imag(aux.diff()/aux)
aux_phi=imag(aux.diff().diff()/aux.diff())
aux_theta_expected=delta*(1-2/(5*r(z)))/(r(z*z)+delta*delta*(1-1/(5*r(z)))**2)
aux_phi_expected=(2*delta/(5*r(z**3)))/(1+delta*delta/(25*r(z**4)))
must('2005 geometric-proof diagnostic polar identity',eq(aux_theta,aux_theta_expected),{'scope':'auxiliary analytic arc; no support certificate'})
must('2005 geometric-proof diagnostic tangent identity',eq(aux_phi,aux_phi_expected),{'scope':'auxiliary analytic arc; no support certificate; derivative positive for s>=1/4'})
must('auxiliary one wiggle no waver exact samples',aux_theta.val([F(1,4)]+[0]*6).re<0 and aux_theta.val([F(2,5)]+[0]*6).re==0 and aux_theta.val([F(1)]+[0]*6).re>0)

# A tangent waver need not spoil either target angle. Prescribe the exact
# radial angle beta=atan(delta/(1+r^2)), strictly positive and decreasing.
# The associated polar derivative is theta_r=delta/[r(1+r^2)]>0.
theta_r=delta/(r(z)*(1+r(z*z)))
beta_r=-2*delta*r(z)/((1+r(z*z))**2+delta*delta)
phi_r=theta_r+beta_r
phi_expected=delta*(1-r(z**4)+delta*delta)/(r(z)*(1+r(z*z))*((1+r(z*z))**2+delta*delta))
must('tangent-waver insufficient for either target: exact derivative identity',eq(phi_r,phi_expected),{'scope':'auxiliary analytic radial prescription; beta positive decreasing, theta increasing; no support certificate'})
must('tangent-waver insufficiency exact signs',phi_r.val([F(1,2)]+[0]*6).re>0 and phi_r.val([F(2)]+[0]*6).re<0)

out={'arithmetic':'exact fractions and Gaussian rationals; generic identities by polynomial cross multiplication','count':len(checks),'all_passed':all(c['passed'] for c in checks),'checks':checks}
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_passed':out['all_passed']}))
