from fractions import Fraction as F
from itertools import product
from math import comb
from collections import Counter
import json

C=Counter()
def check(k,b):
    assert b,k
    C[k]+=1

def dist(y,a):
    out=[]
    for u in product(*(range(v+1) for v in y)):
        p=F(1)
        for v,w in zip(y,u):p*=comb(v,w)*a**w*(1-a)**(v-w)
        out.append((u,p))
    return out

def fits(y,kind):
    n=len(y); m=max(y)
    if kind==0:return [F(0)]*n
    if kind==1:return [F(v,2) for v in y]
    if kind==2:return [F(sum(y),n)]*n
    return [F(m if (sum(y)+i)%2 else 0) for i in range(n)]

def mean2(v):return sum(x*x for x in v)/len(v)

for n in (1,2,3):
    for y in product(range(3),repeat=n):
        S=sum(y);m=max(y)
        for a in (F(1,3),F(2,3),F(9,10)):
            d=dist(y,a)
            check('thinning_probability',sum(p for u,p in d)==1)
            q0=1-a**S
            q1=1-a**(S-1) if S else F(0)
            if S:
                dm=[(u,p/q0) for u,p in d if u!=y]
                check('conditional_nonzero_deletion',sum(p for u,p in dm)==1)
            for kind in range(4):
                fy=fits(y,kind); A=mean2(fy)
                c=sum(p*mean2(fits(u,kind)) for u,p in d)
                raw=sum(p*(mean2(fits(u,kind))-2*a/((1-a)*n)*sum((y[i]-u[i])*fits(u,kind)[i] for i in range(n))) for u,p in d)
                c1=A;anchor=A;ex1=F(0);ex2=F(0)
                bounds=[]
                for i in range(n):
                    if not y[i]:continue
                    z=tuple(v-(j==i) for j,v in enumerate(y)); fz=fits(z,kind)[i]
                    dz=dist(z,a)
                    bz=sum(p*fits(u,kind)[i] for u,p in dz)
                    c-=2*a*y[i]*bz/n
                    c1-=2*F(y[i],n)*fz
                    anchor-=2*a*F(y[i],n)*fz
                    if q1:
                        dmz=[(u,p/q1) for u,p in dz if u!=z]
                        check('conditional_delete_one',sum(p for u,p in dmz)==1)
                        ex2+=F(y[i],S)*sum(p*(fits(u,kind)[i]-fz) for u,p in dmz)
                        bounds.extend(abs(fits(u,kind)[i]-fz)<=m for u,p in dmz)
                if S:ex1=sum(p*(mean2(fits(u,kind))-A) for u,p in dm)
                expectedX=q0*ex1-2*a*q1*F(S,n)*ex2
                L=q0*m*m+2*a*q1*F(S*m,n)
                D=(1-a)*(m*m*S+2*F(m*S*S,n))
                check('centered_binomial_identity',c==raw)
                check('anchored_score_unbiased',anchor+expectedX==c)
                check('correction_range_expectation',abs(expectedX)<=L)
                check('rare_deletion_range_bound',L<=D)
                check('uniform_score_Hudson_bound',abs(c-c1)<=D)
                check('sample_component_envelopes',all(bounds))
                if S:
                    for u,p in dm:
                        check('square_correction_range',abs(mean2(fits(u,kind))-A)<=m*m)

# Conditional rare deletions can be sampled by total then hypergeometric allocation.
for y in ((1,2),(2,2),(1,1,2)):
    S=sum(y)
    for a in (F(1,4),F(3,4),F(99,100)):
        q=1-a**S
        for u,p in dist(y,a):
            if u==y:continue
            d=tuple(v-w for v,w in zip(y,u));D=sum(d)
            ptot=F(comb(S,D))*(1-a)**D*a**(S-D)/q
            ph=F(1,comb(S,D))
            for v,w in zip(y,d):ph*=comb(v,w)
            check('truncated_total_hypergeometric_sampling',ptot*ph==p/q)

# Actual n=1 family: h=0 and h=log 2 correspond exactly to c=0 and c=1/2.
for a in (F(1,2),F(2,3),F(9,10),F(99,100)):
    y=(2,); d=dist(y,a)
    score=[]
    for c in (F(0),F(1,2)):
        score.append(sum(p*(c*u[0]-a*(2-u[0])/(1-a))**2 for u,p in d))
    check('actual_exact_average_selects_log2',score[1]<score[0])
    check('actual_no_deletion_selects_zero',F(0)**2<(F(1,2)*2)**2)
    for B in range(1,6):
        check('actual_no_deletion_probability',a**(2*B)==(a*a)**B)

out={'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
     'scope':'Finite exact decomposition, envelopes, conditional sampling laws, and actual n=1 source-family countercontrol. No full adaptive-regret theorem is inferred.'}
print(json.dumps(out,indent=2,sort_keys=True))
