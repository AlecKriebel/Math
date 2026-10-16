"""Exact actual-generator controls for the local all-load Poisson corrector."""
from fractions import Fraction as F
from collections import Counter
import json
C=Counter()
def ck(v,k):
    assert v,k
    C[k]+=1
def ceil(v):return -((-v.numerator)//v.denominator)
def transitions(s,la):
    a,b,x,y=s;D=x+y+1
    return [((1,0,0,0),la/2),((0,1,0,0),la/2),((-1,0,1,0),F(a*(x+1),D)),((0,-1,0,1),F(b*(y+1),D)),((0,0,-1,0),F(x*(y+1),D)),((0,0,0,-1),F(y*(x+1),D))]
def gen(s,la,h):return sum(r*(h(tuple(t+v for t,v in zip(s,d)))-h(s)) for d,r in transitions(s,la) if r)
reports=[]
for la in [F(1,2),F(1),F(2),F(5),F(10)]:
    ga=(la+1)/(la+2);R=1
    def mean(R):return sum(k*ga**k for k in range(R+1))/sum(ga**k for k in range(R+1))
    while mean(R)<=la:R+=1
    mu=mean(R);eps=mu+F(1,2)-la
    ds=[sum(ga**j*(j-mu) for j in range(k+1))/(ga**(k+1)*(k+1)) for k in range(R)]
    gs=[-sum(ds[k:]) for k in range(R)]+[F(0)]
    g=lambda k:gs[k] if k<R else F(0)
    for k in range(R+1):
        q=(ga*(k+1)*(g(k+1)-g(k)) if k<R else 0)+(k*(g(k-1)-g(k)) if k else 0)
        ck(q==k-mu,'finite_Poisson_equation_including_cap')
        ck(g(k)>=0,'nonnegative_corrector')
        if k<R:
            ck(g(k+1)<g(k),'strict_decrease_below_cap')
            ck(ga**k*ga*(k+1)==ga**(k+1)*(k+1),'finite_detailed_balance')
    ck(mu>la and eps>F(1,2),'strict_all_load_margin')
    for y in range(R+3):
        for x in [y+1,2*(y+1),10*(y+1)]:
            D=x+y+1
            for b in [ceil(ga*D),ceil(ga*D)+3,3*ceil(ga*D)]:
                for a in [0,1,10]:
                    state=(a,b,x,y);h=lambda s:sum(s)+g(s[3])
                    ck(F(x,D)>=F(1,2) and F(b,D)>=ga,'majority_sector_membership')
                    ck(gen(state,la,h)<=-eps,'actual_generator_local_negative_drift')
    K=4*la+6;v=(K-1)/(K+1)
    for y in range(15):
        for x in [ceil(K*(y+1)),2*ceil(K*(y+1))]:
            D=x+y+1;b=ceil(ga*D)-1
            for a in [0,7]:
                s=(a,b,x,y);Z=lambda s:s[0]+s[2]-s[1]-s[3]
                ck(b<ga*D and x>=K*(y+1),'biased_sector_membership')
                ck(Z(s)>0 and Z(s)>=a+(1-ga)*x/2,'positive_stopped_imbalance')
                ck(gen(s,la,Z)<=-v,'uniform_exit_drift')
    for m in [ceil(la+1),2*ceil(la+1),10*ceil(la+1)]:
        ck(F(m,m+1)>=ga,'quadratic_obstruction_ray_now_covered')
    reports.append({'lambda':str(la),'R':R,'gamma':str(ga),'margin':str(eps)})
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'parameter_examples':reports,'scope':'Finite exact Poisson-equation and actual six-rate generator checks. Global positive recurrence at lambda>=2 is not claimed.'},sort_keys=True,indent=2))
