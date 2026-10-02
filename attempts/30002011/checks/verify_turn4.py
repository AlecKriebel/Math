from fractions import Fraction as F
from itertools import product
from math import factorial, comb
from collections import Counter
import json

C=Counter()
def check(k,v):
    assert v,k
    C[k]+=1

def pava(v,w):
    b=[]
    for i,(a,t) in enumerate(zip(v,w)):
        b.append([i,i+1,a*t,t])
        while len(b)>1 and b[-2][2]/b[-2][3]>b[-1][2]/b[-1][3]:
            r=b.pop(); l=b.pop();b.append([l[0],r[1],l[2]+r[2],l[3]+r[3]])
    z=[F(0)]*len(v)
    for i,j,a,t in b:z[i:j]=[a/t]*(j-i)
    return z

samples=[]
for counts in product(range(3),repeat=5):
    if not sum(counts):continue
    xs=[i for i,c in enumerate(counts) if c];w=[F(counts[i]) for i in xs]
    n=sum(counts);m=max(xs);l=min(xs)
    r0=[F((x+1)*(counts[x+1] if x<4 else 0),counts[x]) for x in xs]
    rp=[F(xs[i+1]*counts[xs[i+1]],counts[x]) if i+1<len(xs) else F(0) for i,x in enumerate(xs)]
    d0=pava(r0,w);dp=pava(rp,w)
    check('raw_gap_filled_order',all(a<=b for a,b in zip(r0,rp)))
    check('projected_gap_filled_order',all(0<=a<=b<=m for a,b in zip(d0,dp)))
    missing=sum(F(t*counts[t],n) for t in xs if t>l and counts[t-1]==0)
    md=sum(t*(b-a) for a,b,t in zip(d0,dp,w))/n
    check('exact_projected_missing_bin_mean',md==missing)
    sq=sum(t*(b-a)**2 for a,b,t in zip(d0,dp,w))/n
    check('missing_bin_L2_bound',sq<=m*missing)
    check('projection_preserves_mean',sum(t*a for t,a in zip(w,rp))==sum(t*a for t,a in zip(w,dp)))
    if len(xs)>1 and any(xs[i+1]>xs[i]+1 for i in range(len(xs)-1)) and n<=4:samples.append(counts)

# Actual finite-h source b_h: rational enclosure using alternating exp(-h)
# and a geometric upper bound for the remaining Poisson series.
def exact_enclosure(counts,x,h,J=18):
    n=sum(counts);m=max(i for i,c in enumerate(counts) if c)
    def a(z):
        den=sum(F(c)*h**(z-t)/factorial(z-t) for t,c in enumerate(counts) if c and t<=z)
        num=sum(F(t*c)*h**(z+1-t)/factorial(z+1-t) for t,c in enumerate(counts) if c and t<=z+1)
        return num/den
    s=sum(h**j/F(factorial(j))*a(x+j) for j in range(J+1))
    elo=sum((-h)**j/F(factorial(j)) for j in range(22))
    ehi=sum((-h)**j/F(factorial(j)) for j in range(21))
    tail=F(m*n)*h*h**(J+1)/factorial(J+1)/(1-h/F(J+2))
    return elo*s,ehi*s+tail

for counts in samples[:40]:
    xs=[i for i,c in enumerate(counts) if c];n=sum(counts);m=max(xs)
    for h in (F(1,2),F(1,10),F(1,1000)):
        lower=[];upper=[];plus=[]
        for i,x in enumerate(xs):
            bp=F(xs[i+1]*counts[xs[i+1]],counts[x]) if i+1<len(xs) else F(0)
            lo,hi=exact_enclosure(counts,x,h);eps=m*n*(n+3)*h
            check('finite_h_unprojected_uniform_bound',lo>=bp-eps and hi<=bp+eps)
            lower.append(lo);upper.append(hi);plus.append(bp)
        w=[F(counts[x]) for x in xs];dl=pava(lower,w);du=pava(upper,w);dp=pava(plus,w)
        check('finite_h_projected_uniform_bound',all(a-eps<=b<=c<=a+eps for a,b,c in zip(dp,dl,du)))

for n in range(1,10):
    for pi in range(1,10):
        p=F(pi,10)
        check('binomial_missing_mass_maximum',p*(1-p)**(n-1)<=F(1,n))
        for qi in range(1,10-pi):
            q=F(qi,10)
            lhs=sum(k*comb(n,k)*q**k*(1-p-q)**(n-k) for k in range(n+1))
            check('multinomial_empty_predecessor_identity',lhs==n*q*(1-p)**(n-1))

out={'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
 'scope':'Finite exact PAVA/gap/missing-bin identities and rational enclosures for selected actual positive-h fits. The asymptotic rate uses the written argument and credited Robbins theorem.'}
print(json.dumps(out,indent=2,sort_keys=True))
