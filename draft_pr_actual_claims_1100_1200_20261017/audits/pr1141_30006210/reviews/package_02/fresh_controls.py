#!/usr/bin/env python3
"""Fresh exact finite controls; independent of distributed checker imports.

Construct the actual maximum-monomial separator on rational disjoint tables,
then examine every pre-query and terminal cylinder of each constructed tree.
Finite stress tests do not replace the universal argument.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse, hashlib, json, random, sys

def require(ok, message):
    if not ok: raise RuntimeError(message)

def coefficients(table):
    a=list(table); n=len(a).bit_length()-1
    for i in range(n):
        for j in range(len(a)):
            if j&(1<<i): a[j]-=a[j^(1<<i)]
    return a

def degree(table):
    return max((j.bit_count() for j,c in enumerate(coefficients(table)) if c), default=-1)

def submasks(m):
    return [s for s in range(m+1) if s&~m==0]

def restrict(table, free, queried, answer):
    rest=[i for i in free if i not in queried]
    original={i:k for k,i in enumerate(free)}
    result=[]
    for z in range(1<<len(rest)):
        x=sum(((answer>>k)&1)<<original[i] for k,i in enumerate(queried))
        x+=sum(((z>>k)&1)<<original[i] for k,i in enumerate(rest))
        result.append(table[x])
    return tuple(result),rest

def separator(p,q,free,counts):
    require(all(a*b==0 for a,b in zip(p,q)), 'separator disjointness lost')
    if not any(p): return 0
    if not any(q): return 1
    dp,dq=degree(p),degree(q); D=max(dp,dq)
    require(min(dp,dq)>=1,'nonzero constant cannot have a disjoint partner')
    s=[a*a-b*b for a,b in zip(p,q)]
    z=max(range(len(s)),key=lambda j:abs(s[j]))
    chosen=q if s[z]>0 else p
    cc=coefficients(chosen); k=degree(chosen)
    top=[m for m,c in enumerate(cc) if c and m.bit_count()==k]
    union=0; family=[]
    for m in top:
        if not union&m: family.append(m);union|=m
    require(all(m&union for m in top),'top family is not maximal')
    blocks=[]
    for m in family:
        witness=next((e for e in submasks(m) if e and chosen[z^e]),None)
        require(witness is not None,'top monomial has no nonempty block witness')
        blocks.append(witness)
    sign=1 if s[z]>0 else -1
    R=[]
    for y in range(1<<len(blocks)):
        flip=0
        for j,e in enumerate(blocks):
            if y>>j&1: flip|=e
        R.append(sign*s[z^flip]/abs(s[z]))
    require(R[0]==1 and max(map(abs,R))<=1,'block normalization')
    require(all(R[1<<j]<0 for j in range(len(blocks))),'block sign switch')
    cr=coefficients(R); m=degree(R)
    derivative=sum(cr[1<<j] for j in range(len(blocks)))
    require(m<=2*D and len(blocks)<=abs(derivative)<=2*m*m,'Markov Bernoulli interface')
    for t in (Q(1,11),Q(2,7),Q(1,2),Q(10,11)):
        value=sum(c*t**j.bit_count() for j,c in enumerate(cr))
        moment=sum(v*t**j.bit_count()*(1-t)**(len(blocks)-j.bit_count()) for j,v in enumerate(R))
        require(value==moment and abs(value)<=1,'Bernoulli moment identity')
        counts['block_moment_checks']+=1
    query=[free[i] for i in range(len(free)) if union>>i&1]
    require(len(query)<=8*D**3,'query batch bound')
    counts['separator_stages']+=1
    counts['selected_blocks']+=len(blocks)
    children={}
    for answer in range(1<<len(query)):
        pp,rest=restrict(p,free,query,answer);qq,_=restrict(q,free,query,answer)
        reduced=qq if s[z]>0 else pp
        require(degree(reduced)<k,'maximum degree failed to decrease')
        require(degree(pp)<=dp and degree(qq)<=dq,'restriction increased degree')
        counts['all_answer_degree_reductions']+=1
        children[answer]=separator(pp,qq,rest,counts)
    def expand(j,answer):
        if j==len(query): return children[answer]
        return (query[j],expand(j+1,answer),expand(j+1,answer|(1<<j)))
    return expand(0,0)

def path(tree,x):
    history=[]
    while isinstance(tree,tuple):
        i,a,b=tree
        require(i not in [j for j,v in history],'repeated separator query')
        history.append((i,(x>>i)&1));tree=b if (x>>i)&1 else a
    return tree,tuple(history)

def covariance_and_laws(tree,p,q,n,counts):
    N=1<<n
    traces=[path(tree,x) for x in range(N)]
    h=[out for out,hist in traces]
    for x in range(N):
        require(not p[x] or h[x]==1,'wrong p support label')
        require(not q[x] or h[x]==0,'wrong q support label')
    T=max(len(hist) for out,hist in traces)
    d=max(degree(p),degree(q),1)
    require(T<=min(n,16*d**4),'separator total depth')
    r=[Q(sum(any(j==i for j,v in hist) for out,hist in traces),N) for i in range(n)]
    mu=Q(sum(h),N); covs=[]
    for a,side in ((p,1),(q,0)):
        norm=sum(v*v for v in a)/N
        require(norm>0,'zero density normalization')
        u=[v*v/norm for v in a]
        A=[sum(abs(u[x]-u[x^(1<<i)]) for x in range(N))/(2*N) for i in range(n)]
        cov=sum(h[x]*u[x] for x in range(N))/N-mu
        require(cov==side-mu,'square density separator covariance')
        require(abs(cov)<=sum(r[i]*A[i] for i in range(n))/2,'adaptive covariance')
        covs.append(cov)
        spectrum=[sum(a[x]*(-1 if (x&m).bit_count()%2 else 1) for x in range(N))/N for m in range(N)]
        require(sum(c*c for c in spectrum)==norm,'Walsh Parseval')
        for i in range(n):
            rho=sum(c*c for m,c in enumerate(spectrum) if m>>i&1)/norm
            require(A[i]**2<=4*rho*(1-rho),'full norm square bound')
            counts['rational_density_coordinate_checks']+=1
    require(abs(covs[0])+abs(covs[1])==1,'common-zero covariance sum')
    prefix=defaultdict(Counter);terminal=defaultdict(Counter);nexti={}
    for x,(out,hist) in enumerate(traces):
        for y in range(N):
            z=x
            for t,(i,v) in enumerate(hist):
                key=hist[:t];nexti[key]=i
                zz=(z&~(1<<i))|(y&(1<<i));prefix[key][(z,zz)]+=1;z=zz
            terminal[hist][z]+=1
    for hist,law in prefix.items():
        i=nexti[hist]
        expected={(z,(z&~(1<<i))|(v<<i)):1<<(n-len(hist)-1) for z in range(N) for v in (0,1)}
        require(dict(law)==expected,'pre-query exact resampling pair law')
        counts['prequery_cylinder_laws']+=1
    for hist,law in terminal.items():
        require(dict(law)=={z:1<<(n-len(hist)) for z in range(N)},'terminal exact independent uniform law')
        counts['terminal_cylinder_laws']+=1
    counts['variable_stopping_trees']+=len({len(hist) for out,hist in traces})>1
    counts['common_zero_trees']+=any(a==b==0 for a,b in zip(p,q))
    counts['constructed_separator_cases']+=1

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--counterfactual',choices=['zero-maximizer','post-query-law','square-density-variance','drop-square-half','demand-cover','covariance-overstrength']);args=ap.parse_args()
    # These are computed explicit counterexamples to six false mathematical
    # statements. They are limited formula/law sanity checks, NOT mutations of
    # the implemented separator or covariance algorithms and not a coverage
    # claim for their error handling.
    if args.counterfactual=='zero-maximizer':
        p,q=(Q(2),Q(0)),(Q(0),Q(-3))
        s=[a*a-b*b for a,b in zip(p,q)]
        require(max(map(abs,s))==0,'global maximizing magnitude cannot be zero')
    if args.counterfactual=='post-query-law':
        def law(condition):
            c=Counter((x,y) for x in (0,1) for y in (0,1) if condition(x))
            return {k:Q(v,sum(c.values())) for k,v in c.items()}
        require(law(lambda x:x==1)==law(lambda x:True),'post-query pair law is not unconditional')
    if args.counterfactual=='square-density-variance':
        a=(Q(2),Q(4));mean=sum(a)/2
        variance=sum((v-mean)**2 for v in a)/2
        wrong_density=[v*v/variance for v in a]
        require(sum(wrong_density)/2==1,'full norm mean-square density must have mean one')
    if args.counterfactual=='drop-square-half':
        a=(Q(0),Q(2));norm=sum(v*v for v in a)/2
        rho=((a[0]-a[1])/2)**2/norm
        wrong_A=sum(abs(a[x]**2-a[x^1]**2) for x in (0,1))/(2*norm)
        require(wrong_A**2<=4*rho*(1-rho),'probability-half resampling sharp square bound')
    if args.counterfactual=='demand-cover':
        p=tuple(Q(x&3==3) for x in range(4));q=tuple(Q(x&3==2) for x in range(4))
        require(all(a or b for a,b in zip(p,q)),'common zeros need not be covered')
    if args.counterfactual=='covariance-overstrength':
        h=(Q(0),Q(1));u=(Q(0),Q(1))
        cov=abs(sum(a*b for a,b in zip(h,u))/2-sum(h)*sum(u)/4)
        A=sum(abs(u[x]-u[y]) for x in (0,1) for y in (0,1))/4
        require(cov<=Q(2,5)*A,'binary covariance cannot use coefficient two-fifths')
    rng=random.Random(20261017114102);counts=Counter()
    for case in range(96):
        n=4;p=[];q=[]
        for x in range(1<<n):
            side=(x+case)%3 if x<3 else rng.randrange(3)
            value=Q(rng.choice([-13,-7,-2,1,5,11]),rng.randrange(1,20))
            p.append(value if side==1 else Q(0));q.append(value if side==2 else Q(0))
        scale=Q(1,10**80) if case%3==0 else Q(-10**80) if case%3==1 else Q(19,23)
        p=tuple(v*scale for v in p);q=tuple(q)
        t=separator(p,q,list(range(n)),counts);covariance_and_laws(t,p,q,n,counts)
    # Degree-four multiplexer pairs force genuine continued degree-reduction
    # stages after the first queried maximum-monomial batch.
    for k in range(24):
        order=list(range(5));rng.shuffle(order);p=[];q=[]
        for x in range(32):
            bit=[(x>>i)&1 for i in order]
            h=bit[1] if bit[0] else bit[2]
            gate=bit[3];sign=1-2*bit[4]
            p.append(Q(k+1,13)*h*gate*(3+2*sign))
            q.append(Q(-19,k+2)*(1-h)*gate*(5-7*sign))
        before=counts['separator_stages']
        t=separator(tuple(p),tuple(q),list(range(5)),counts)
        counts['multistage_separator_cases']+=counts['separator_stages']-before>1
        covariance_and_laws(t,tuple(p),tuple(q),5,counts)
    # Structured degree<=5 pairs with a common-zero half and an independently
    # chosen nontrivial total separator on that half, to stress arbitrary labels.
    for k in range(24):
        n=5
        a=[Q(rng.randrange(-7,8),rng.randrange(1,9)) for j in range(8)]
        b=[Q(rng.randrange(-7,8),rng.randrange(1,9)) for j in range(8)]
        a[0]=Q(1);b[1]=Q(-1)
        p=tuple(a[x>>2] if x&3==3 else Q(0) for x in range(32))
        q=tuple(b[x>>2] if x&3==2 else Q(0) for x in range(32))
        arbitrary=(2,(3,k%2,(4,0,1)),1)
        t=(1,arbitrary,(0,0,1))
        covariance_and_laws(t,p,q,n,counts)
    require(counts['constructed_separator_cases']==144,'complete case plan')
    require(counts['variable_stopping_trees']>0 and counts['common_zero_trees']==144 and counts['multistage_separator_cases']>0,'nonvacuous scope')
    print(json.dumps({'status':'PASS','python':sys.version,'optimized':bool(sys.flags.optimize),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'counts':dict(counts),'scope':'96 actual greedy rational support-separator constructions n=4;24 multiplexer degree<=4 pairs with multiple reduction stages n=5;24 degree<=5 structured pairs n=5 and arbitrary common-zero labels; exact pair/terminal laws at every visited cylinder. Finite consistency controls only.'},indent=2,sort_keys=True))

if __name__=='__main__': main()
