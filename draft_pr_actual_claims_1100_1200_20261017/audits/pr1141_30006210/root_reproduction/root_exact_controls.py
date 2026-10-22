#!/usr/bin/env python3
"""Root's exact rational controls; supplementary to the universal proof, no dependencies."""
from fractions import Fraction as F
from itertools import product
import argparse, json, random

def require(ok, message):
    if not ok: raise ValueError(message)

def poly_value(cs, x):
    return sum((c * (-1 if (mask & x).bit_count() % 2 else 1) for mask,c in enumerate(cs)), F(0))

def tree(rng, free, level=0):
    if not free or (level and rng.randrange(4)==0): return rng.randrange(2)
    i=rng.choice(free); rem=[j for j in free if j!=i]
    return (i,tree(rng,rem,level+1),tree(rng,rem,level+1))

def run(t,x):
    queried=[]
    while isinstance(t,tuple):
        i,a,b=t; require(i not in queried,'repeat query'); queried.append(i); t=b if x>>i&1 else a
    return t,queried

def main(mutant):
    rng=random.Random(114130006210); counts={'rational_covariance_cases':0,'square_coordinate_cases':0,'chebyshev_endpoint_cases':0,'full_norm_and_endpoint_cases':0}
    for n in range(1,6):
        size=1<<n
        for k in range(40):
            t=tree(rng,list(range(n)))
            hs=[run(t,x) for x in range(size)]; h=[v[0] for v in hs]
            r=[F(sum(i in v[1] for v in hs),size) for i in range(n)]
            u=[F(rng.randrange(-200,201),rng.randrange(1,18)) for x in range(size)]
            if k==0:
                t=(0,0,1); hs=[run(t,x) for x in range(size)]; h=[v[0] for v in hs]
                r=[F(int(i==0)) for i in range(n)]; u=[F(x&1) for x in range(size)]
            cov=abs(sum((F(h[x])*u[x] for x in range(size)),F(0))/size-F(sum(h),size)*sum(u,F(0))/size)
            aa=[sum((abs(u[x]-u[x^(1<<i)]) for x in range(size)),F(0))/(2*size) for i in range(n)]
            factor=F(1,4) if mutant=='covariance-quarter' else F(1,2)
            require(cov<=factor*sum((r[i]*aa[i] for i in range(n)),F(0)),'sharp adaptive covariance coefficient')
            counts['rational_covariance_cases']+=1
            cs=[F(rng.randrange(-9,10),rng.randrange(1,12)) if j.bit_count()<=2 else F(0) for j in range(size)]
            if k==0: cs=[F(int(j in [0,1])) for j in range(size)]
            norm=sum((c*c for c in cs),F(0)); require(norm>0,'nonzero polynomial')
            av=[poly_value(cs,x) for x in range(size)]
            require(sum((v*v for v in av),F(0))/size==norm,'full Parseval norm')
            for i in range(n):
                rho=sum((cs[j]*cs[j] for j in range(size) if j>>i&1),F(0))/norm
                A=sum((abs(av[x]**2-av[x^(1<<i)]**2) for x in range(size)),F(0))/(2*size*norm)
                constant=F(1) if mutant=='square-one' else F(4)
                require(A*A<=constant*rho*(1-rho),'square influence Cauchy constant')
                bcs=[((av[x]+av[x^(1<<i)])/2,(av[x]-av[x^(1<<i)])/2) for x in range(size)]
                require(A==2*sum((abs(b*c) for b,c in bcs),F(0))/(size*norm),'direct b+x_i*c square formula')
                counts['square_coordinate_cases']+=1
    # Independent coefficient recurrence gives endpoint equality in Markov after t -> 2t-1.
    prev=[F(1)]; cur=[F(0),F(1)]
    for m in range(1,25):
        if m==1: coeff=cur
        else:
            nxt=[F(0)]*(len(cur)+1)
            for j,c in enumerate(cur): nxt[j+1]+=2*c
            for j,c in enumerate(prev): nxt[j]-=c
            prev,cur=cur,nxt; coeff=cur
        deriv=sum((j*c for j,c in enumerate(coeff)),F(0))
        require(deriv==m*m,'Chebyshev endpoint derivative')
        bound=m*m if mutant=='markov-no-rescale' else 2*m*m
        require(2*deriv<=bound,'rescaled Markov factor two')
        counts['chebyshev_endpoint_cases']+=1
    # At all dimensions, the two affine supports partition the cube and relative influence is 1/2.
    for n in range(1,7):
        a=[F(0)]*(1<<n); a[0]=a[1]=1
        b=a.copy(); b[1]=-1
        norm=sum((v*v for v in a),F(0))
        denominator=norm-a[0]**2 if mutant=='variance-denominator' else norm
        rho=a[1]**2/denominator
        require(rho==F(1,2),'constant belongs to denominator')
        require(all(poly_value(a,x)*poly_value(b,x)==0 for x in range(1<<n)),'affine disjoint supports')
        old_sufficient = rho <= F(1,2) if mutant=='old-inclusive-endpoint' else rho < F(1,2)
        require(not old_sufficient,'strict old threshold endpoint counterexample')
        require(F(1,4096)<F(1,1024)<rho,'safe new constant ordering')
        counts['full_norm_and_endpoint_cases']+=1
    print(json.dumps({'status':'PASS','arithmetic':'exact fractions and integers','seed':114130006210,'counts':counts,'interpretation':'Finite controls supplement the universal argument; they are not an exhaustive verification at arbitrary dimension.'},indent=2,sort_keys=True))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--mutant',choices=['covariance-quarter','square-one','markov-no-rescale','variance-denominator','old-inclusive-endpoint']); a=ap.parse_args(); main(a.mutant)
