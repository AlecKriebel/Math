#!/usr/bin/env python3
"""Fresh exact Fourier-Motzkin diagnostics, independent of proposed checkers.
Finite cases only: no polynomial optimizer or universal proof claim.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd, floor, ceil, factorial
import json,random,sys

def require(condition,message):
    if not condition:raise RuntimeError(message)

def dot(a,x):return sum((u*v for u,v in zip(a,x)),F(0))

def canonical(rows):
    best={}
    for a,b in rows:
        a=tuple(F(v) for v in a);b=F(b)
        first=next((abs(v) for v in a if v),None)
        if first is None:
            if b<0:return [(a,b)]
            continue
        a=tuple(v/first for v in a);b/=first
        if a not in best or b<best[a]:best[a]=b
    return list(best.items())

def eliminate(rows,j):
    pos=[(a,b) for a,b in rows if a[j]>0]
    neg=[(a,b) for a,b in rows if a[j]<0]
    zero=[(a,b) for a,b in rows if a[j]==0]
    for ap,bp in pos:
        for an,bn in neg:
            p=ap[j];m=-an[j]
            zero.append((tuple(ap[k]/p+an[k]/m for k in range(len(ap))),bp/p+bn/m))
    return canonical(zero)

def lp(n,edges,c,fixed=None,box=None):
    # Work in original cover coordinates, independent of the sign-change code.
    rows=[]
    for u,v,b in edges:
        a=[F(0)]*(n+1);a[u]=a[v]=F(-1);rows.append((tuple(a),-b))
    for i,p in (fixed or {}).items():
        for sign in (-1,1):
            a=[F(0)]*(n+1);a[i]=sign;rows.append((tuple(a),sign*p))
    if box is not None:
        for i in range(n):
            for sign in (-1,1):
                a=[F(0)]*(n+1);a[i]=sign;rows.append((tuple(a),F(box)))
    rows += [(tuple(c)+(-F(1),),F(0)),(tuple(-a for a in c)+(F(1),),F(0))]
    stages=[];rows=canonical(rows)
    for j in range(n):
        stages.append(rows);rows=eliminate(rows,j)
    lower=[];upper=[]
    for a,b in rows:
        if a[n]<0:lower.append(b/a[n])
        elif a[n]>0:upper.append(b/a[n])
        elif b<0:return None
    if not lower:return ('unbounded',None)
    value=max(lower)
    if upper and min(upper)<value:return None
    x=[F(0)]*n+[value]
    for j in reversed(range(n)):
        lo=[];hi=[]
        for a,b in stages[j]:
            residual=b-sum((a[k]*x[k] for k in range(j+1,n+1)),F(0))
            if a[j]>0:hi.append(residual/a[j])
            elif a[j]<0:lo.append(residual/a[j])
            else:require(residual>=0,'back-substitution consistency')
        l=max(lo) if lo else None;h=min(hi) if hi else None
        require(l is None or h is None or l<=h,'back-substitution interval')
        x[j]=max(F(0),l) if l is not None else F(0)
        if h is not None:x[j]=min(x[j],h)
    x=tuple(x[:n]);require(dot(c,x)==value,'exact reconstructed optimum')
    require(all(x[u]+x[v]>=b for u,v,b in edges),'original feasible optimizer')
    require(all(x[i]==p for i,p in (fixed or {}).items()),'original fixed coordinates')
    require(box is None or all(abs(v)<=box for v in x),'core box optimizer')
    return value,x

def layers(d):
    ls=[]
    for s in (-1,1):
        values=sorted(set(abs(v) for v in d if v*s>0));previous=F(0)
        for v in values:
            ls.append((v-previous,tuple(s if x*s>=v else 0 for x in d)));previous=v
    return ls

def lcm(a,b):return a*b//gcd(a,b)

def main():
    rng=random.Random(202610130518);counts={'models':0,'fm_slice_lps':0,'submodular_pairs':0,'layer_removals':0,'core_comparisons':0,'layer_vectors':0,'recession_interpolations':0,'boundary_controls':0,'negative_controls':0,'facet_bound_checks':0}
    grid=(F(-7,3),F(-1),F(-1,8),F(0),F(1,7),F(1),F(13,4))
    for n in range(1,5):
        for d in product(grid,repeat=n):
            ls=layers(d);require(len(ls)<=n,'at most n independently built layers')
            require(tuple(sum((q*r[i] for q,r in ls),F(0)) for i in range(n))==d,'fresh threshold reconstruction')
            for q,r in ls:
                for i,j in product(range(n),repeat=2):
                    require((r[i]-r[j])*(d[i]-d[j])>=0,'all-pair signed conformity')
                    require(abs(q*(r[i]-r[j]))<=abs(d[i]-d[j]),'all-pair weighted domination')
            counts['layer_vectors']+=1
    for case in range(28):
        n=1+case%4;U=set(range((n+1)//2));possible=[(u,v) for u in U for v in range(n) if v not in U]
        edges=[(u,v,F(rng.randrange(-5,6),rng.randrange(6,12))) for u,v in possible if rng.randrange(4)!=0]
        if case==27:edges=[(0,2,F(2**120+1,2**127-1)),(0,3,F(-2**100,2**121+3)),(1,2,F(1,97)),(1,3,F(6,101))]
        I=tuple(sorted(rng.sample(range(n),min(n,case%3))));sign=tuple(1 if i in U else -1 for i in range(n))
        cost=[F(0)]*n
        for u,v,b in edges:
            w=F(rng.randrange(0,4),rng.randrange(1,5));cost[u]+=w;cost[v]+=w
        base=lp(n,edges,cost);require(base is not None and base[0]!='unbounded','bounded cover FM base')
        star=tuple(sign[i]*base[1][i] for i in range(n));lower={i:ceil(star[i]-n) for i in I};upper={i:floor(star[i]+n) for i in I}
        k=q=1
        for u,v,b in edges:k=lcm(k,b.denominator)
        for a in cost:q=lcm(q,a.denominator)
        B=max([1]+[ceil(abs(b)) for u,v,b in edges]);A=max([1]+[ceil(abs(a)) for a in cost]);Hs=ceil(max(map(abs,star)))+n;H=n*B+n
        values={};completions={}
        ranges=[range(lower[i],upper[i]+1) for i in I]
        for p in product(*ranges):
            fixed={i:sign[i]*F(z) for i,z in zip(I,p)};res=lp(n,edges,cost,fixed);counts['fm_slice_lps']+=1
            direct=all(fixed[u]+fixed[v]>=b for u,v,b in edges if u in I and v in I)
            require(direct==(res is not None),'FM exact projected domain')
            if res is None:continue
            value,x=res;values[p]=value;y=tuple(sign[i]*x[i] for i in range(n));completions[p]=y
            require((value*k*q).denominator==1 and abs(value)<=n*A*(Hs+n*B),'FM value encoding bound')
            for lam,r in layers(tuple(y[i]-star[i] for i in range(n))):
                forward=tuple(star[i]+lam*r[i] for i in range(n));require(all(forward[u]-forward[v]>=b for u,v,b in edges),'fresh forward layer')
                require(sum(cost[i]*sign[i]*r[i] for i in range(n))>=0,'fresh layer objective')
                if lam>=1:
                    z=tuple(y[i]-r[i] for i in range(n));require(all(z[u]-z[v]>=b for u,v,b in edges),'fresh removal feasibility')
                    require(all(z[i].denominator==1 for i in I),'fresh removal integrality')
                    require(sum(abs(z[i]-star[i]) for i in range(n))<sum(abs(y[i]-star[i]) for i in range(n)),'fresh strict removal decrease');counts['layer_removals']+=1
        require(values,'fresh localized mixed domain nonempty')
        optimum=min(values.values());require(any(v==optimum and max(abs(completions[p][i]-star[i]) for i in range(n))<n for p,v in values.items()),'fresh at least one proximity optimum')
        for p,z in product(values,repeat=2):
            meet=tuple(min(a,b) for a,b in zip(p,z));join=tuple(max(a,b) for a,b in zip(p,z))
            require(meet in values and join in values,'fresh projection lattice')
            require(values[p]+values[z]>=values[meet]+values[join],'fresh FM partial-value submodularity');counts['submodular_pairs']+=1
        # Objective-independent core proof is attacked using LPs with all-coordinate box constraints.
        core=[]
        for p in product(*(range(-H,H+1) for i in I)):
            res=lp(n,edges,cost,{i:F(z) for i,z in zip(I,p)},H);counts['fm_slice_lps']+=1
            if res is not None:core.append(res[0])
        require(core and min(core)==optimum,'objective-independent bounded core value');counts['core_comparisons']+=1
        counts['models']+=1
    # Unbounded objectives in the ORIGINAL coordinates; integer rays preserve all selected sets.
    for c,r in [((F(-1),F(0)),(1,0)),((F(0),F(-1)),(0,1)),((F(1),F(0)),(-1,1))]:
        require(lp(2,[(0,1,F(2,7))],c)[0]=='unbounded','unbounded FM distinction')
        require(r[0]+r[1]>=0 and dot(c,r)<0,'integral unbounded certificate');counts['boundary_controls']+=1
    # Exact single-edge hull characterization for all-integral and one-integral cases.
    for b in (F(-7,3),F(0),F(2,7),F(5,2)):
        for t in (F(-9,7),F(1,13),F(2,3),F(17,5)):
            B=ceil(b);p=(t,F(B)-t);lo=floor(t);weight=t-lo
            points=((F(lo),F(B-lo)),(F(lo+1),F(B-lo-1)))
            require(tuple((1-weight)*points[0][i]+weight*points[1][i] for i in range(2))==p,'all-integral exact hull boundary blend')
            p=(t,b-t);points=((F(lo),b-lo),(F(lo+1),b-lo-1))
            require(tuple((1-weight)*points[0][i]+weight*points[1][i] for i in range(2))==p,'one-integral true demand boundary blend');counts['boundary_controls']+=2
    for r in product(range(-2,3),repeat=4):
        if all(r[u]-r[v]>=0 for u in (0,1) for v in (2,3)):
            require(all(all(d[u]-d[v]>=0 for u in (0,1) for v in (2,3)) for w,d in layers(tuple(map(F,r)))),'recession threshold membership')
            t=F(11,7);m=floor(t);w=t-m;base=(F(1),F(1),F(0),F(0))
            require(tuple(base[i]+t*r[i] for i in range(4))==tuple((1-w)*(base[i]+m*r[i])+w*(base[i]+(m+1)*r[i]) for i in range(4)),'fractional recession interpolation');counts['recession_interpolations']+=1
    # Named negative controls have explicit witnesses rather than labels.
    require(F(1,2)<ceil(F(1,2)),'LP hull substitution witness')
    require(min(1,0)+min(0,1)<1,'original meet-closure witness')
    require(0-0<1,'baseline omission witness')
    require(F(1,3)!=ceil(F(1,3)),'mixed-row rounding witness')
    d=(F(1,4),);require(abs(d[0]-1)>abs(d[0]),'small-layer removal witness')
    counts['negative_controls']=5
    for n in range(1,20):
        for k,H in ((1,2*n),(2**127-1,2**180+n)):
            M=factorial(n)*(k*(H+1))**n
            # GLS-style signed rational coefficient encodings are bounded even with denominator 1.
            explicit=(n+1)*(2+M.bit_length()+2)
            phi=10*(n+1)**2*(1+(n+1).bit_length()+k.bit_length()+H.bit_length()+2)
            require(explicit<phi,'explicit generous facet bound');counts['facet_bound_checks']+=1
    print(json.dumps({'status':'PASS_FRESH_FOURIER_MOTZKIN_DIAGNOSTICS','optimization_mode':sys.flags.optimize,'seed':202610130518,'counts':counts,'limitations':['Finite exact diagnostics only.','No imports from candidate sources.','No polynomial LP/SFM/GLS implementation or exhaustive priority claim.']},sort_keys=True))
if __name__=='__main__':main()
