#!/usr/bin/env python3
"""Exact Gaussian-rational controls for the authored identities.

Uses only the standard library. Finite evaluations are regression controls;
the universal arguments and identities are proved in PROOF_PARTIALS.md.
"""
from dataclasses import dataclass
from fractions import Fraction as F
import json
from pathlib import Path

@dataclass(frozen=True)
class Q:
    re: F = F(0)
    im: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))
    @staticmethod
    def coerce(x): return x if isinstance(x,Q) else Q(x)
    def __add__(self,x):
        x=Q.coerce(x);return Q(self.re+x.re,self.im+x.im)
    __radd__=__add__
    def __neg__(self):return Q(-self.re,-self.im)
    def __sub__(self,x):return self+-Q.coerce(x)
    def __rsub__(self,x):return Q.coerce(x)+-self
    def __mul__(self,x):
        x=Q.coerce(x);return Q(self.re*x.re-self.im*x.im,self.re*x.im+self.im*x.re)
    __rmul__=__mul__
    def conj(self):return Q(self.re,-self.im)
    def norm2(self):return self.re*self.re+self.im*self.im
    def __truediv__(self,x):
        x=Q.coerce(x);n=x.norm2()
        if n==0:raise ZeroDivisionError()
        v=self*x.conj();return Q(v.re/n,v.im/n)
    def __rtruediv__(self,x):return Q.coerce(x)/self
    def __pow__(self,n):
        if n<0:return (1/self)**(-n)
        out=Q(1)
        for _ in range(n):out=out*self
        return out

def pk(z,sgn=1):return (4*sgn+2*z)/(1-z*z)
def ph(z):return 2*z/(1+z*z)+4*z/(1-z*z)
def A(P,z):return (1-z.norm2())*P(z)-2*z.conj()

def require(ok,what):
    if not ok:raise RuntimeError(what)

counts={}
def check(label,ok):
    require(ok,label);counts[label]=counts.get(label,0)+1

for ix in range(-8,9):
 for iy in range(-8,9):
  z=Q(F(ix,10),F(iy,10))
  if z.norm2()>=1:continue
  delta2=z.im*z.im/(1-z*z).norm2()
  for sign in [-1,1]:
   check('koebe_squared_deficit', A(lambda w:pk(w,sign),z).norm2()==16-48*delta2)
  check('delta_domain',delta2>=0 and delta2<F(1,4))
  check('delta_denominator_identity',(1-z*z).norm2()==(1-z.norm2())**2+4*z.im*z.im)
  if iy==0:
   check('real_koebe_positive',A(pk,z)==Q(4))
   check('real_koebe_negative',A(lambda w:pk(w,-1),z)==Q(-4))
  for aa in [F(-3,5),F(0),F(2,5)]:
   phi=(z+aa)/(1+aa*z)
   dphi=(1-aa*aa)/(1+aa*z)**2
   pphi=-2*aa/(1+aa*z)
   for P in [pk,ph]:
    left=(1-z.norm2())*(P(phi)*dphi+pphi)-2*z.conj()
    right=(1+aa*z.conj())/(1+aa*z)*A(P,phi)
    check('real_automorphism_covariance',left==right)
   check('delta_invariance',phi.im*phi.im/(1-phi*phi).norm2()==delta2)

for num in range(1,20):
 t=F(num,20);z=Q(0,t)
 check('two_slit_imaginary_identity',A(ph,z)==Q(0,8*t/(1+t*t)))
check('half_imaginary_koebe',A(pk,Q(0,F(1,2))).norm2()==F(208,25))
check('half_imaginary_two_slit',A(ph,Q(0,F(1,2))).norm2()==F(256,25))
check('koebe_not_sole_extremizer',F(256,25)>F(208,25))

# Exact Q(sqrt(2)) arithmetic for z^2=-3+2sqrt(2).
def pairadd(a,b):return (a[0]+b[0],a[1]+b[1])
def pairmul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
u=(-3,2)
numerator=pairadd(pairadd(pairmul(u,u),(6*u[0],6*u[1])),(1,0))
check('convex_hull_derivative_zero',numerator==(0,0))
# 1<sqrt(2)<3/2, so 0<sqrt(2)-1<1/2; q' has an interior zero.
check('convex_hull_zero_inside_disk',1<2<F(9,4))

# Deliberately false identities must be rejected, proving controls distinguish constants.
z=Q(F(1,3),F(1,4));d2=z.im*z.im/(1-z*z).norm2()
check('negative_control_47_rejected',A(pk,z).norm2()!=16-47*d2)
check('negative_control_uniform_gap_rejected',A(pk,Q(F(1,2))).norm2()>F(399,100)**2)
check('negative_control_wrong_covariance_phase_rejected',((1+F(2,5)*z)/(1+F(2,5)*z.conj())) != ((1+F(2,5)*z.conj())/(1+F(2,5)*z)))

result={'status':'PASS','arithmetic':'exact rational and quadratic-field arithmetic','checks':sum(counts.values()),'by_family':counts,'limits':'Finite regression controls supplement the written proofs; not a proof search or certified ODE computation.'}
if __name__=='__main__':print(json.dumps(result,indent=2,sort_keys=True))
