#!/usr/bin/env python3
"""Bounded exact regression controls, NOT an analytic/formal proof checker."""
from fractions import Fraction as Q
import json

class C:
    def __init__(self, re=0, im=0):
        if isinstance(re, C): self.re, self.im = re.re, re.im
        else: self.re, self.im = Q(re), Q(im)
    def __add__(self, y):
        y=C(y); return C(self.re+y.re,self.im+y.im)
    __radd__=__add__
    def __neg__(self): return C(-self.re,-self.im)
    def __sub__(self,y): return self+-C(y)
    def __rsub__(self,y): return C(y)+-self
    def __mul__(self,y):
        y=C(y); return C(self.re*y.re-self.im*y.im,self.re*y.im+self.im*y.re)
    __rmul__=__mul__
    def conj(self): return C(self.re,-self.im)
    def norm2(self): return self.re*self.re+self.im*self.im
    def __truediv__(self,y):
        y=C(y); n=y.norm2()
        if not n: raise ZeroDivisionError
        v=self*y.conj();return C(v.re/n,v.im/n)
    def __rtruediv__(self,y): return C(y)/self
    def __pow__(self,n):
        if n<0:return (1/self)**(-n)
        a=C(1)
        for _ in range(n):a=a*self
        return a
    def __eq__(self,y):
        y=C(y);return self.re==y.re and self.im==y.im
    def out(self):return {'real':str(self.re),'imag':str(self.im)}

counts={}
def check(category, condition):
    if not condition: raise AssertionError(category)
    counts[category]=counts.get(category,0)+1

q=C(Q(1,3),-Q(1,6)); w=1-q**3
r=Q(399,400); alpha=C(Q(8,9),Q(4,9)); beta=w/r**3
lam=Q(3,5)
check('certificate',q*q==C(Q(1,12),-Q(1,9)))
check('certificate',q**3==C(Q(1,108),-Q(11,216)))
check('certificate',w==C(Q(107,108),Q(11,216)))
check('certificate',alpha.norm2()==Q(80,81))
check('certificate',w.norm2()==Q(45917,46656))
check('certificate',r**6-w.norm2()==Q(2785244627851129,2985984000000000000))
check('certificate',0<r<1 and 0<lam<1)
check('certificate',beta.norm2()==Q(2938688000000000000,2941473244627851129))
check('certificate',0<alpha.norm2()<1 and 0<beta.norm2()<1)
check('certificate',q.re>0 and q.im<0 and 3*q.im**2<q.re**2)
check('certificate',alpha.norm2()<Q(179,180)**2)
check('certificate',beta.norm2()<Q(9999,10000)**2)
check('certificate',lam*Q(179,180)+(1-lam)==Q(299,300))
D=lam*(1-alpha*r*r)+(1-lam)*q*q
N=lam*(1+alpha*r*r)+(1-lam)*(2/q-q*q)
check('certificate',D==C(184794,-557603)/1800000)
check('certificate',N==C(5431206,2285603)/1800000)
check('certificate',D.norm2()>0)
R=N/D
check('certificate',R==C(-54160961609,690164496000)/69013985609)
check('certificate',R.re<0)

# Check the derived real quadratic identity at 21 prescribed rational weights.
# This is a bounded algebraic control, not a search or an infinite proof.
for j in range(21):
 t=Q(j,20);dt=t*(1-alpha*r*r)+(1-t)*q*q
 nt=t*(1+alpha*r*r)+(1-t)*(2/q-q*q)
 poly=Q(15391097599,25920000000)*t*t-Q(17772056000,25920000000)*t+Q(2956000000,25920000000)
 check('weight_identity',(nt*dt.conj()).re==poly)

# Compare direct signed-binomial recursion and absolute-value telescoping.
a=Q(2,3);signed=Q(2,3);partial=Q(0)
for n in range(1,65):
 check('binomial_controls',a==abs(signed) and a>0)
 anext=a*Q(3*n-2,3*n+3)
 check('binomial_controls',Q(3*n,2)*a-Q(3*(n+1),2)*anext==a)
 partial+=a
 check('binomial_controls',partial==1-Q(3*(n+1),2)*anext and partial<=1)
 signed=signed*(Q(2,3)-n)/(n+1);a=anext

# Exact right-half-plane identities on a bounded Gaussian-rational grid.
for u0 in range(-4,5):
 for v0 in range(-4,5):
  u=C(Q(u0,5),Q(v0,5))
  if u.norm2()<1:
   check('mobius_controls',((1+u)/(1-u)).re==(1-u.norm2())/(1-u).norm2()>0)

# Four fixed exterior pairs and inverse powers 1..32.
pairs=[(C(2),C(3)),(C(0,2),C(-2)),(C(Q(3,2),1),C(2,-1)),(C(1,1),C(-1,1))]
for z,v in pairs:
 check('lipschitz_pair_domains',z.norm2()>=1 and v.norm2()>=1)
 for n in range(1,33):
  check('inverse_power_controls',(z**(-n)-v**(-n)).norm2()<=n*n*(z-v).norm2())

# Deliberately wrong hypotheses/conclusions must be rejected.
check('negative_controls',not R.re>=0)
check('negative_controls',not (w/Q(99,100)**3).norm2()<1)
check('negative_controls',not q**3==q.conj()**3)
check('negative_controls',not R==C(-54160961608,690164496000)/69013985609)
for t in (Q(0),Q(1)):
 dt=t*(1-alpha*r*r)+(1-t)*q*q
 nt=t*(1+alpha*r*r)+(1-t)*(2/q-q*q)
 check('negative_controls',not (nt/dt).re<0)

print(json.dumps({'result':'PASS','counts':counts,'total_checks':sum(counts.values()),
 'certificate':{'q':q.out(),'w':w.out(),'beta':beta.out(),'D':D.out(),'N':N.out(),'P_H_z0':R.out()},
 'limits':['Exact finite arithmetic only; no floating-point sampling.',
 '64 binomial indices, 21 prescribed weights, a 9-by-9 grid filtered by norm < 1, four pairs with powers 1..32.',
 'Does not certify general analyticity, convergence, topology, convexity or all Lean dependencies.',
 'No parameter search, exhaustive search, Lean build, or new discovery claim.']},indent=2,sort_keys=True))
