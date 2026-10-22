#!/usr/bin/env python3
"""Exact finite regression controls. Does not certify the universal target."""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
import json

@dataclass(frozen=True)
class Q:
    re: F = F(0)
    im: F = F(0)
    def __post_init__(self):
        object.__setattr__(self, 're', F(self.re))
        object.__setattr__(self, 'im', F(self.im))
    def __add__(self, other):
        o = coerce(other); return Q(self.re+o.re, self.im+o.im)
    __radd__ = __add__
    def __neg__(self): return Q(-self.re, -self.im)
    def __sub__(self, o): return self+-coerce(o)
    def __rsub__(self, o): return coerce(o)+-self
    def __mul__(self, other):
        o = coerce(other); return Q(self.re*o.re-self.im*o.im, self.re*o.im+self.im*o.re)
    __rmul__ = __mul__
    def conj(self): return Q(self.re,-self.im)
    def norm(self): return self.re*self.re+self.im*self.im
    def __truediv__(self, o):
        o=coerce(o); d=o.norm()
        if not d: raise ZeroDivisionError
        a=self*o.conj(); return Q(a.re/d,a.im/d)
    def __rtruediv__(self,o): return coerce(o)/self
    def __pow__(self,k):
        if k<0:return (1/self)**(-k)
        out=Q(1)
        for _ in range(k):out=out*self
        return out

def coerce(x): return x if isinstance(x,Q) else Q(x)
def product(xs):
    p=Q(1)
    for x in xs:p=p*x
    return p

def check(ok,message):
    if not ok: raise RuntimeError(message)

def unit(t):
    t=F(t);return Q((1-t*t)/(1+t*t),2*t/(1+t*t))

def blaschke(z,zeros):
    k=product((1-a.conj())/(1-a) for a in zeros)
    return k*z*product((z-a)/(1-a.conj()*z) for a in zeros)

def determinant(matrix):
    a=[[coerce(x) for x in row] for row in matrix]; n=len(a); out=Q(1)
    for i in range(n):
        pivot=next((k for k in range(i,n) if a[k][i]!=Q(0)),None)
        if pivot is None:return Q(0)
        if pivot!=i:a[i],a[pivot]=a[pivot],a[i];out=-out
        v=a[i][i];out=out*v
        for k in range(i+1,n):
            f=a[k][i]/v
            for j in range(i,n):a[k][j]=a[k][j]-f*a[i][j]
    return out

def polymul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def main():
    counts={}
    families=[[],[Q(0)],[Q(F(1,2))],[Q(F(1,2)),Q(F(-1,2))],
      [Q(0,F(1,2)),Q(0,F(-1,2))],
      [Q(F(1,2)),Q(F(-1,2)),Q(0,F(1,2)),Q(0,F(-1,2))],
      [Q(F(1,3),F(1,4)),Q(F(-1,5),F(1,7)),Q(0)],
      [Q(0),Q(0),Q(0)], [Q(F(2,3))]*5]
    points=[unit(F(i,7)) for i in range(-10,11)]+[Q(-1)]
    count=0;newton=0
    for zeros in families:
        m=len(zeros)
        check(blaschke(Q(1),zeros)==Q(1),'boundary marking')
        check(blaschke(Q(0),zeros)==Q(0),'interior marking')
        for z in points:
            val=blaschke(z,zeros)
            check(val.norm()==1,'circle preservation')
            ld=Q(1)+sum(z*(1-a.norm())/((z-a)*(1-a.conj()*z)) for a in zeros)
            pois=F(1)+sum((1-a.norm())/(z-a).norm() for a in zeros)
            check(ld==Q(pois),'logarithmic derivative/Poisson identity')
            check(pois>1 if m else pois==1,'strict expansion exact degree condition')
            count+=1
        e=[Q(1)]+[sum(product(c) for c in combinations(zeros,k)) for k in range(1,m+1)]
        s=[Q(0)]+[sum(a**k for a in zeros) for k in range(1,m+1)]
        for k in range(1,m+1):
            check(k*e[k]==sum((-1)**(j-1)*e[k-j]*s[j] for j in range(1,k+1)),'Newton identity')
            newton+=1
        check(all(v==Q(0) for v in s[1:])==all(a==Q(0) for a in zeros),'finite moment witness')
    counts['boundary_point_checks']=count
    counts['newton_identity_checks']=newton
    zs=[Q(F(1,2)),Q(F(-1,2))]
    check(sum(zs)==Q(0) and sum(z**2 for z in zs)!=Q(0),'first moment negative control')
    counts['first_moment_false_inference_rejected']=True
    # Exact quadratic multipliers and homogeneous resultant obstruction.
    quad=0
    for alpha in [Q(0),Q(F(1,2)),Q(0,F(1,3)),Q(F(-1,3),F(1,5))]:
        for beta in points+[Q(0),Q(F(1,3))]:
            check((alpha*beta).norm()<1,'no cancellation for fixed interior alpha')
            check(1-alpha*beta != Q(0),'resultant factor')
            resultant=determinant([[1,beta,0,0],[0,1,beta,0],[0,alpha,1,0],[0,0,alpha,1]])
            check(resultant==1-alpha*beta,'homogeneous Sylvester determinant')
            # R(z)/z at zero = beta.  In w=1/z, 1/R(1/w)=w(w+alpha)/(1+beta*w).
            check((Q(0)+beta)/(1+alpha*Q(0))==beta,'zero multiplier')
            check((Q(0)+alpha)/(1+beta*Q(0))==alpha,'infinity multiplier')
            quad+=1
    counts['quadratic_parameter_checks']=quad
    check(1-Q(1)*Q(1)==Q(0),'excluded alpha beta=1 cancellation')
    counts['excluded_quadratic_cancellation_detected']=True
    # Homogeneous formula and exact radial-rate identity.
    hole=0
    for n in range(3,13):
        for c in [F(1,2),F(1),F(2),F(3)]:
            for eps in [F(1,10),F(1,100),F(1,1000)]:
                r,s=1-eps,1-c*eps
                check(0<r<1 and 0<s<1,'admissible radial approach')
                L=n-2+(1+r)/(1-r)+(1+s)/(1-s)
                check(eps*L==2+2/c+(n-4)*eps,'exact scaled angular derivative')
                monomial=[F(0)]*(n-2)+[F(1)]
                numerator=polymul(monomial,polymul([r,F(1)],[s,F(1)]))
                denominator=polymul([F(1),r],[F(1),s])
                check(numerator[-3:]==[r*s,r+s,F(1)],'numerator coefficient formula')
                check(denominator==[F(1),r+s,r*s],'denominator coefficient formula')
                limnum=polymul(monomial,polymul([F(1),F(1)],[F(1),F(1)]))
                common=[F(1),F(2),F(1)]
                check(limnum==[F(0)]*(n-2)+common,'double hole factor and reduced degree')
                hole+=1
    counts['hole_rate_checks']=hole
    check(2+2/F(1)!=2+2/F(2),'rate constants distinct')
    counts['rate_distinction_checked']=True
    # Finite graph models of the two different topological failure directions.
    def fibers(R,axis):
        out={}
        for p in R:out.setdefault(p[axis],set()).add(p[1-axis])
        return out
    diag={(0,0),(1,1),(2,2)}
    split={(0,0),(1,1),(1,2)}
    merge={(0,0),(1,1),(2,1)}
    check(all(len(x)==1 for a in (0,1) for x in fibers(diag,a).values()),'diagonal projections')
    check(max(map(len,fibers(split,0).values()))==2,'split direction')
    check(max(map(len,fibers(merge,1).values()))==2,'merge direction')
    counts['finite_relation_controls']=3
    counts['universal_analytic_proofs_machine_certified']=False
    counts['actual_mating_boundary_witness_constructed']=False
    counts['original_target_solved']=False
    print(json.dumps(counts,indent=2,sort_keys=True))
if __name__=='__main__': main()
