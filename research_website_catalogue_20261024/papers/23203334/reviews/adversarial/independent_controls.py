#!/usr/bin/env python3
"""Independent exact forward differentiation and finite algebra controls.

No imports from the supplied certificates. No PDE theorem certification.
"""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import random, json, hashlib, datetime

counts=Counter()
def check(ok,label):
    counts[label]+=1
    if not ok: raise ValueError(label)

class Jet:
    def __init__(self,v,d=0): self.v,self.d=F(v),F(d)
    @staticmethod
    def cast(x): return x if isinstance(x,Jet) else Jet(x)
    def __add__(self,x):
        x=Jet.cast(x);return Jet(self.v+x.v,self.d+x.d)
    __radd__=__add__
    def __neg__(self):return Jet(-self.v,-self.d)
    def __sub__(self,x):return self+-Jet.cast(x)
    def __rsub__(self,x):return Jet.cast(x)+-self
    def __mul__(self,x):
        x=Jet.cast(x);return Jet(self.v*x.v,self.d*x.v+self.v*x.d)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=Jet.cast(x);return Jet(self.v/x.v,(self.d*x.v-self.v*x.d)/(x.v*x.v))
    def __rtruediv__(self,x):return Jet.cast(x)/self

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def add(*vs):return [sum(z) for z in zip(*vs)]
def scale(x,v):return [x*y for y in v]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def velocity(w):
    w=list(map(F,w));s=dot(w,w)
    if s==1:raise ValueError('singular velocity parameter')
    return scale(2/(1+s),w),(1+s)/abs(1-s)
def sphere(x,y):
    x,y=F(x),F(y);h=1+x*x+y*y
    return [2*x/h,2*y/h,(1-x*x-y*y)/h]
def acceleration(u,q,e,m,E,B):
    force=add(E,cross(u,B))
    return scale(e/(m*q),add(force,scale(-dot(u,force),u)))
def det(a):
    a=[list(map(F,row)) for row in a];out=F(1)
    for i in range(len(a)):
        j=next((j for j in range(i,len(a)) if a[j][i]),None)
        if j is None:return F(0)
        if j!=i:a[i],a[j]=a[j],a[i];out=-out
        pivot=a[i][i];out*=pivot
        for j in range(i+1,len(a)):
            z=a[j][i]/pivot
            for k in range(i+1,len(a)):a[j][k]-=z*a[i][k]
    return out

def pair(n,a,u,A,b,r):
    d,D,eta=1-dot(n,u),1-dot(n,a),1-dot(a,u)
    check(d>0 and D>0,'positive_retarded_deficits')
    tp=d/D;rp=tp-1
    np=scale(1/r,add(scale(tp,add(a,scale(-1,n))),n,scale(-1,u)))
    check(dot(n,np)==0,'exact_tangent_cone_derivative')
    nj=[Jet(x,y) for x,y in zip(n,np)]
    aj=[Jet(x,tp*y) for x,y in zip(a,A)]
    uj=[Jet(x,y) for x,y in zip(u,b)]
    rj=Jet(r,rp)
    dj,Dj,etaj=1-dot(nj,uj),1-dot(nj,aj),1-dot(aj,uj)
    kj=add(uj,scale(-etaj/Dj,nj))
    primitive=scale(1/(rj*dj),kj)
    k=[z.v for z in kj]
    residual=add(scale(eta/(r*r*D*D),add(scale((1-dot(a,a))/D,n),scale(-1,a))),
                 scale(dot(A,k)/(r*D*D),n))
    rhs=add([-z.d for z in primitive],residual)
    electric=add(scale((1-dot(u,u))/(r*r*d*d*d),add(n,scale(-1,u))),
                 scale(1/(r*d*d*d),add(scale(dot(n,b),add(n,scale(-1,u))),scale(-d,b))))
    force=add(electric,cross(a,cross(n,electric)))
    lhs=scale(tp,force)
    check(lhs==rhs,'exact_pair_identity_arbitrary_cone_direction')
    return lhs,rhs

def main():
    rng=random.Random(23203334)
    masses=[F(1,10000),F(1,2),F(1),F(7),F(10000)]
    charges=[F(-7),F(-1),F(0),F(1),F(3)]
    samples=[]
    for i in range(600):
        n=sphere(F(rng.randrange(-5,6),3),F(rng.randrange(-5,6),3))
        w1=[F(rng.randrange(-4,5),7) for _ in range(3)]
        w2=[F(rng.randrange(-4,5),7) for _ in range(3)]
        a,qa=velocity(w1);u,qb=velocity(w2)
        if i%10==0:a,qa=velocity([F(999999,1000000),0,0])
        if i%11==0:u,qb=velocity([0,F(-99999,100000),0])
        ma,mb=rng.choice(masses),rng.choice(masses)
        ea,eb=rng.choice(charges),rng.choice(charges)
        E=[F(rng.randrange(-9,10),3) for _ in range(3)]
        B=[F(rng.randrange(-9,10),5) for _ in range(3)]
        A=acceleration(a,qa,ea,ma,E,B)
        b=acceleration(u,qb,eb,mb,E,B)
        r=F(1,1000000) if i%7==0 else F(rng.randrange(1,50),11)
        lhs,rhs=pair(n,a,u,A,b,r)
        cab=ea*eb/ma
        check(scale(cab,lhs)==scale(cab,rhs),'signed_unequal_mass_pair_identity')
        check(ma*(ea/ma)==ea,'mass_weighted_energy_work')
        check(cab*(eb/mb)==ea*eb*eb/(ma*mb),'source_acceleration_coefficient')
        check(ma**3*(F(1,ma)**3)==1,'number_density_jacobian')
        flux=(dot(E,E)+dot(B,B))/2-dot(n,cross(E,B))
        good=add(E,cross(n,B))
        check(flux==(dot(good,good)+dot(n,B)**2)/2,'exact_positive_electromagnetic_cone_flux')
        qvec=add(E,cross(u,B));vp=scale(eb/mb,qvec)
        v6=u+vp;n6=n+[F(0)]*3
        rankone=[[F(i==j)-v6[i]*n6[j] for j in range(6)] for i in range(6)]
        check(det(rankone)==1-dot(n,u),'exact_retarded_rank_one_jacobian')
        derivative=[[(F(i==j)-u[i]*u[j])/qb for j in range(3)] for i in range(3)]
        trace=F(0)
        for j in range(3):trace+=cross([derivative[i][j] for i in range(3)],B)[j]
        check(trace==0,'exact_phase_force_divergence')
        if ea==0:check(A==[0,0,0] and cab==0,'neutral_receiver_control')
        if eb==0:check(b==[0,0,0] and cab==0,'neutral_source_control')
    # Wrong formula controls: a zero-acceleration pair still has transport force.
    lhs,_=pair([F(0),F(0),F(1)],[F(0)]*3,[F(0)]*3,[F(0)]*3,[F(0)]*3,F(1))
    check(lhs==[0,0,1],'negative_control_omitted_transport_term')
    check(F(2)*F(-3)/F(5)!= (F(2)/F(5))*(F(-3)/F(7)),
          'negative_control_wrong_pair_mass_factor')
    check((F(1),F(-1))!=(F(1),F(1)),'negative_control_false_common_aggregate_force')
    # Exact closure constants. Each square root is rational by construction.
    eta=F(1,1024)
    for C in [F(1,7),F(1),F(9),F(1000),F(10**9)]:
        M=max(F(32),8*C);rootA=16*(C+M);A=rootA*rootA
        check(A>=max(1,16*C*M,256*C*C),'closure_parameter_order')
        coeff1=C+M/16
        coeff2=C*(M+rootA)+2*A*eta
        check(coeff1<=M/2 and coeff2<=A/2,'closure_strict_improvement')
        for L in [F(1),F(10),F(10000)]:
            floor=min(F(1,(4096*M)**2),F(1)/(4*1024**2*A*L))
            # Below this floor neither summand can supply one quarter of q.
            check(1024**2*M*M*floor<F(1,16) and 1024**2*A*L*floor<=F(1,4),
                  'doubling_harmonic_floor')
        samples.append({'C':str(C),'M':str(M),'A':str(A)})
    # Claimed exact exponent margin checked independently from the two inequalities.
    beta=F(29,25);eps=F(1,1000)
    upper=(beta/2-F(1,3)+(F(8,3)+beta/2)*eps)/(F(1,3)+beta/4)
    check(F(62,125)-upper==F(8889,93500),'exact_selected_exponent_contradiction_margin')
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
            'assertions':sum(counts.values()),'families':dict(counts),'assembled_pair_inputs':600,
            'closure_samples':samples,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limits':'Finite exact rational and forward-differentiation controls; no supplied checker imports. These do not certify dyadic occupation estimates, PDE existence, formalization or priority.'}
    Path(__file__).with_name('independent_controls_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','assertions':result['assertions'],'families':len(counts)}))

if __name__=='__main__':main()
