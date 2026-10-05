"""Exact Gaussian-rational arithmetic and Newton recurrences (standard library)."""
from dataclasses import dataclass
from fractions import Fraction as F

@dataclass(frozen=True)
class Q:
    re: F = F(0)
    im: F = F(0)
    def __post_init__(self):
        object.__setattr__(self,'re',F(self.re)); object.__setattr__(self,'im',F(self.im))
    @staticmethod
    def co(x): return x if isinstance(x,Q) else Q(x)
    def __add__(self,other):
        z=self.co(other); return Q(self.re+z.re,self.im+z.im)
    __radd__=__add__
    def __neg__(self):return Q(-self.re,-self.im)
    def __sub__(self,other):return self+-self.co(other)
    def __rsub__(self,other):return self.co(other)+-self
    def __mul__(self,other):
        z=self.co(other);return Q(self.re*z.re-self.im*z.im,self.re*z.im+self.im*z.re)
    __rmul__=__mul__
    def __truediv__(self,other):
        z=self.co(other);w=self*z.conj();d=z.norm2();return Q(w.re/d,w.im/d)
    def conj(self):return Q(self.re,-self.im)
    def norm2(self):return self.re*self.re+self.im*self.im
    def __pow__(self,k):
        if k<0: return (Q(1)/self)**(-k)
        r=Q(1);a=self
        while k:
            if k&1:r=r*a
            a=a*a;k//=2
        return r
    def record(self):return [str(self.re),str(self.im)]
    @staticmethod
    def parse(x):return Q(F(x[0]),F(x[1]))

def coeffs_from_sums(s):
    """Coefficients of prod(1-z_i*t), through degree len(s)."""
    a=[Q(1)]
    for j in range(1,len(s)+1):a.append(-sum((s[k-1]*a[j-k] for k in range(1,j+1)),Q())/j)
    return a

def sums_from_coeffs(a):
    s=[]
    for j in range(1,len(a)):
        s.append(-j*a[j]-sum((a[k]*s[j-k-1] for k in range(1,j)),Q()))
    return s

def coeffs_from_roots(z):
    a=[Q(1)]
    for x in z:
        b=a+[Q()]
        for j in range(1,len(b)):b[j]=b[j]-x*a[j-1]
        a=b
    return a

def fixed_root_recurrence(s):
    """Coefficients of exp(sum((1-s_k)t^k/k)), through degree n."""
    b=[Q(1)]
    for j in range(1,len(s)+1):b.append(sum(((1-s[k-1])*b[j-k] for k in range(1,j+1)),Q())/j)
    return b
