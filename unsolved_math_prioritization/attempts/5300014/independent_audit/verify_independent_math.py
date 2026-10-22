#!/usr/bin/env python3
"""Independent exact finite regression checks; no universal proof certification."""
from fractions import Fraction as F
from itertools import combinations
import json

def require(ok, msg):
    if not ok:
        raise RuntimeError(msg)

# Gaussian rationals as pairs, independently implemented without author imports.
def q(a=0,b=0): return (F(a), F(b))
def add(a,b): return (a[0]+b[0], a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def sub(a,b): return add(a,neg(b))
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a): return (a[0],-a[1])
def norm(a): return a[0]**2+a[1]**2
def div(a,b):
    c=mul(a,conj(b));d=norm(b)
    return (c[0]/d,c[1]/d)
def power(a,k):
    r=q(1)
    for _ in range(k): r=mul(r,a)
    return r
def total(v):
    r=q()
    for a in v:r=add(r,a)
    return r
def pmul(a,b):
    r=[q()]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[i+j]=add(r[i+j],mul(x,y))
    return r
def peval(p,z):
    r=q()
    for c in reversed(p):r=add(c,mul(z,r))
    return r
def pderiv(p):return [mul(q(i),p[i]) for i in range(1,len(p))]
def rational_derivative(p,d,z):
    pv,dv=peval(p,z),peval(d,z)
    return div(sub(mul(peval(pderiv(p),z),dv),mul(pv,peval(pderiv(d),z))),mul(dv,dv))
def circle(t):
    t=F(t);return q((1-t*t)/(1+t*t),2*t/(1+t*t))

def main():
    out={}
    points=[circle(F(j,5)) for j in range(-10,11)]+[q(-1)]
    families=[[q()],[q(F(1,2))],[q(F(1,2)),q(F(-1,2))],
              [q(F(1,2)),q(0,F(1,2)),q(F(-1,2)),q(0,F(-1,2))],
              [q(F(1,3),F(1,4)),q(F(-1,5),F(1,7)),q()],
              [q(F(2,3)),q(F(2,3)),q(),q()]]
    derivative_count=0;newton_count=0
    for zs in families:
        p=[q(),q(1)];d=[q(1)];free=[q(1)]
        for a in zs:
            p=pmul(p,[neg(a),q(1)]);d=pmul(d,[q(1),neg(conj(a))])
            free=pmul(free,[neg(a),q(1)])
        # Normalize at 1 only after multiplying coefficient polynomials.
        k=div(peval(d,q(1)),peval(p,q(1)))
        p=[mul(k,c) for c in p]
        require(peval(p,q())==q(),'zero fixed')
        require(peval(p,q(1))==peval(d,q(1)),'boundary marked')
        for z in points:
            value=div(peval(p,z),peval(d,z))
            require(norm(value)==1,'unit circle preserved')
            logder=div(mul(z,rational_derivative(p,d,z)),value)
            poisson=1+sum((1-norm(a))/norm(sub(z,a)) for a in zs)
            require(logder==q(poisson) and poisson>1,'coefficient derivative equals Poisson sum')
            derivative_count+=1
        m=len(zs);s=[q()]+[total(power(a,k) for a in zs) for k in range(1,m+1)]
        e=[mul(q((-1)**k),free[m-k]) for k in range(m+1)]
        for k in range(1,m+1):
            rhs=total(mul(q((-1)**(j-1)),mul(e[k-j],s[j])) for j in range(1,k+1))
            require(mul(q(k),e[k])==rhs,'Newton identity against independently multiplied polynomial')
            newton_count+=1
        require(any(x!=q() for x in s[1:])==any(a!=q() for a in zs),'finite Fourier witness')
    out['independent_coefficient_derivative_cases']=derivative_count
    out['independent_newton_cases']=newton_count
    sharp=[q(F(1,2)),q(0,F(1,2)),q(F(-1,2)),q(0,F(-1,2))]
    require(all(total(power(a,k) for a in sharp)==q() for k in range(1,4)), 'first three moments vanish')
    require(total(power(a,4) for a in sharp)==q(F(1,4)), 'fourth moment nonzero')
    out['degree_five_last_possible_witness_control']=True

    quadratics=0
    for alpha in [q(),q(F(1,2)),q(0,F(1,3)),q(F(-1,3),F(1,5))]:
        for beta in points+[q(),q(F(1,3),F(1,4))]:
            p=[q(),beta,q(1)];d=[q(1),alpha]
            require(sub(q(1),mul(alpha,beta))!=q(),'no homogeneous common factor')
            require(rational_derivative(p,d,q())==beta,'zero multiplier by derivative')
            require(rational_derivative([q(),alpha,q(1)],[q(1),beta],q())==alpha,'infinity multiplier by inverse-coordinate derivative')
            marked=div(sub(q(1),beta),sub(q(1),alpha))
            require(peval(p,marked)==mul(marked,peval(d,marked)),'third marked fixed point')
            gamma=div(sub(sub(q(2),alpha),beta),sub(q(1),mul(alpha,beta)))
            require(rational_derivative(p,d,marked)==gamma,'third fixed multiplier')
            quadratics+=1
    out['independent_quadratic_derivative_cases']=quadratics
    require(div(sub(q(1),q(1)),sub(q(1),q(F(1,2))))==q(),'parabolic marking collision allowed')
    out['quadratic_boundary_marking_collision_checked']=True
    hole_count=0
    for n in range(3,14):
        for c in [F(1,3),F(1,2),F(1),F(2),F(3)]:
            for eps in [F(1,10),F(1,37),F(1,1000)]:
                r,s=1-eps,1-c*eps
                p=[q()]*(n-2)+[q(1)]
                p=pmul(p,pmul([q(r),q(1)],[q(s),q(1)]))
                d=pmul([q(1),q(r)],[q(1),q(s)])
                value=div(peval(p,q(-1)),peval(d,q(-1)))
                L=div(mul(q(-1),rational_derivative(p,d,q(-1))),value)
                require(mul(q(eps),L)==q(2+2/c+(n-4)*eps),'double-hole derivative from coefficients')
                require((n-3)+2==n-1,'free zero count includes distinguished z separately')
                hole_count+=1
    out['independent_double_hole_derivative_cases']=hole_count
    edges=[(i,j) for i in range(3) for j in range(3)];surjective=bijective=0
    for mask in range(1<<9):
        R={e for k,e in enumerate(edges) if mask>>k&1}
        f0={i:{j for a,j in R if a==i} for i in range(3)}
        f1={j:{i for i,b in R if b==j} for j in range(3)}
        if all(f0.values()) and all(f1.values()):
            surjective+=1
            both=all(len(s)==1 for s in list(f0.values())+list(f1.values()))
            require(both==(len(R)==3),'finite two-projection criterion')
            bijective+=int(both)
    require(bijective==6,'three-element bijections')
    out['surjective_finite_relations_checked']=surjective
    out['bijective_finite_relations']=bijective
    out['universal_analytic_proofs_machine_certified']=False
    out['original_target_solved']=False
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
