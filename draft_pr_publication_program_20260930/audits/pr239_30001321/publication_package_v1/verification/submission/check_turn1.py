"""Exact finite RWRE controls for the turn-1 partial theorem.

Enumerates independent environments, without simulation. Does not certify
the asymptotic estimates or the unresolved superpolynomial-tail target.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict,Counter
from math import comb
import json
import sympy as sp
counts=Counter()
def ck(x,label):
    assert x,label
    counts[label]+=1
def annealed(t,q):
    return {2*j-t:F(comb(t,j))*q**j*(1-q)**(t-j) for j in range(t+1)}
for values,probs in [((F(1,4),F(3,4)),(F(1,2),F(1,2))),((F(1,5),F(2,5)),(F(1,3),F(2,3)))]:
    q=sum(v*w for v,w in zip(values,probs));a=q*(1-q)
    delta=sum(w*v*(1-v) for v,w in zip(values,probs));sigma=a-delta
    chain={0:F(1)};g=[]
    for n in range(31):
        g.append(chain.get(0,F(0)))
        nxt=defaultdict(F)
        for d,w in chain.items():
            step=delta if d==0 else a
            nxt[d-1]+=w*step;nxt[d+1]+=w*step;nxt[d]+=w*(1-2*step)
        chain=nxt
    z=sp.symbols('z');aa=sp.Rational(a.numerator,a.denominator);dd=sp.Rational(delta.numerator,delta.denominator)
    G=1/((1-dd/aa)*(1-z)+(dd/aa)*sp.sqrt((1-z)*(1-(1-4*aa)*z)))
    series=sp.series(G,z,0,31).removeO().expand()
    for n in range(31):ck(series.coeff(z,n)==sp.Rational(g[n].numerator,g[n].denominator),'return_generating_coefficients')
    for n in range(30):ck(g[n+1]<=g[n],'return_probability_monotonicity')
    for N in range(1,5):
        sites=[(s,x) for s in range(N) for x in range(-s,s+1,2)]
        profiles=[defaultdict(F) for _ in range(N)]
        outcomes=[];total=F(0)
        for bits in product((0,1),repeat=len(sites)):
            env=dict(zip(sites,(values[b] for b in bits)))
            weight=F(1)
            for b in bits:weight*=probs[b]
            total+=weight;mu={0:F(1)}
            for s in range(N):
                for x,w in mu.items():profiles[s][x]+=weight*w*w
                nxt=defaultdict(F)
                for x,w in mu.items():
                    p=env[s,x];nxt[x+1]+=w*p;nxt[x-1]+=w*(1-p)
                mu=nxt
            outcomes.append((weight,dict(mu)))
        ck(total==1,'environment_normalization')
        for s in range(N):ck(sum(profiles[s].values())==g[s],'replica_overlap_identity')
        avg=annealed(N,q)
        for x,p in avg.items():ck(sum(w*mu.get(x,F(0)) for w,mu in outcomes)==p,'annealed_endpoint_law')
        means=[(w,sum(x*p for x,p in mu.items())) for w,mu in outcomes]
        expected_mean=N*(2*q-1)
        ck(sum(w*(m-expected_mean)**2 for w,m in means)==4*sigma*sum(g[:N]),'quenched_mean_variance')
        for M in range(1,6):
            for shift in range(M):
                labels=sorted({(x-shift)//M for x in avg})
                for label in labels:
                    def inside(x):return (x-shift)//M==label
                    amass=sum(p for x,p in avg.items() if inside(x))
                    var=sum(w*(sum(p for x,p in mu.items() if inside(x))-amass)**2 for w,mu in outcomes)
                    predicted=F(0)
                    for s in range(N):
                        kernel=annealed(N-s-1,q)
                        for x,second in profiles[s].items():
                            grad=sum(p*(int(inside(x+1+y))-int(inside(x-1+y))) for y,p in kernel.items())
                            predicted+=sigma*second*grad*grad
                    ck(var==predicted,'interval_layer_martingale_variance')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'families':dict(sorted(counts.items())),'sympy_version':sp.__version__,'scope':'Finite exact identity controls only; no superpolynomial tail conclusion.'},indent=2,sort_keys=True))
