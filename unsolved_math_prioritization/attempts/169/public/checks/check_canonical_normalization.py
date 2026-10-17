#!/usr/bin/env python3
"""Independent compact exact exchange, restriction, canonical-count diagnostics."""
from fractions import Fraction as F
from itertools import combinations,permutations,product
from math import comb,factorial,prod
from pathlib import Path
from collections import defaultdict
import json
HERE=Path(__file__).resolve().parent

def require(b,s):
    if not b:raise ValueError(s)
def rat(x):
    x=F(x);return [x.numerator,x.denominator]
def choose(n,k):return comb(n,k) if 0<=k<=n else 0
def conv(A,T,p):
    f=[0]*p
    for a in A:
        for t in T:f[(a+t)%p]+=1
    return f

def exchanges():
    out=[];pairs=0
    for p,A,T in ((5,(0,1),(0,2)),(7,(0,1,3),(0,1,5)),(11,(0,1,2),(0,1,4,8)),(19,(0,1,2,4),(0,1,5,6,11,14))):
        k=len(A);m=len(T);U=set(range(p));Tset=set(T);u=conv(A,T,p).count(0)
        for q in range(1,min(2,m,p-m)+1):
            records=[]
            for D in combinations(T,q):
                for B in combinations(sorted(U-Tset),q):
                    T1=Tset-set(D)|set(B);f=conv(A,T1,p)
                    records.append({i for i,v in enumerate(f) if v==0})
            M=F(sum(map(len,records)),len(records));E2=F(sum(len(H)**2 for H in records),len(records));V=E2-M*M
            pair_sum=F(0)
            for x in range(p):
                Nx={(x-a)%p for a in A};Cx=Nx&Tset;dx=len(Cx)
                for y in range(p):
                    Ny={(y-a)%p for a in A};Cy=Ny&Tset;dy=len(Cy);s=len(Cx&Cy);r=len(Nx&Ny)
                    a=dx+dy-s;b=2*k-dx-dy-r+s
                    formula=F(choose(m-a,q-a),comb(m,q))*F(choose(p-m-b,q),comb(p-m,q))
                    actual=F(sum(x in H and y in H for H in records),len(records))
                    require(formula==actual,'exact pair exchange probability');pairs+=1;pair_sum+=formula
            require(pair_sum==E2,'exchange pair sum second moment')
            Hmax=min(p,u+q*k);h=min(map(len,records));bound=None
            if M<Hmax:
                bound=M-V/(Hmax-M);require(h<=bound,'support variance descent bound')
            else:require(h==M,'constant upper-support endpoint')
            if h>=u:
                delta=M-u;require(0<=delta<=q*k and V<=delta*(q*k-delta),'no-improvement variance condition')
            out.append({'p':p,'A':list(A),'T':list(T),'q':q,'old_holes':u,'exchange_outcomes':len(records),
                        'M':rat(M),'V':rat(V),'minimum_exchange_holes':h,'Hmax':Hmax,'descent_bound':None if bound is None else rat(bound)})
    return {'ordered_pair_probability_checks':pairs,'examples':out}

def restrictions():
    out=[]
    for p,S,T,k in ((7,(0,1,3,4),(0,2,5),2),(11,(0,1,2,3,5),(0,4,7),3),(13,(0,1,2,4,7,8),(0,3,6,9),3)):
        K=len(S);f=conv(S,T,p);samples=list(combinations(S,k))
        actual=F(sum(conv(A,T,p).count(0) for A in samples),len(samples))
        formula=sum((F(choose(K-d,k),comb(K,k)) for d in f),F(0))
        require(actual==formula,'random restriction expectation')
        q=[F(choose(K-d,k),comb(K,k)) for d in range(K+1)]
        for d in range(K-1):require(q[d]-2*q[d+1]+q[d+2]==F(choose(K-d-2,k-2),comb(K,k)),'restriction second difference')
        mean=F(K*len(T),p);lo=mean.numerator//mean.denominator
        interp=q[lo] if lo==K else q[lo]+(mean-lo)*(q[lo+1]-q[lo])
        require(actual>=p*interp,'restriction Jensen direction')
        out.append({'p':p,'S':list(S),'T':list(T),'k':k,'mean_holes':rat(actual),'parent_occupancies':f,'Jensen_lower':rat(p*interp)})
    return out

def canonical_counts():
    cases=[];selected_graphs=0
    for p,k,t in ((5,2,3),(7,3,3),(11,3,4)):
        As=list(combinations(range(p),k));Ts=list(combinations(range(p),t));success=0;all_cover_count=0
        W=defaultdict(F);double_weight=F(0)
        for A in As:
            covers=[T for T in Ts if all(conv(A,T,p))];all_cover_count+=len(covers)
            if not covers:continue
            success+=1;T=covers[0]
            for a in permutations(A):
                for s in permutations(T):
                    choices=[[(i,j) for i in range(k) for j in range(t) if (a[i]+s[j])%p==x] for x in range(p)]
                    R=prod(map(len,choices));count=0
                    for chosen in product(*choices):
                        J=tuple(sorted(chosen));W[J]+=F(1,R);double_weight+=F(1,R*R);count+=1;selected_graphs+=1
                    require(count==R,'representation selections')
        norm=F(factorial(p),factorial(p-k))*factorial(t)
        weighted=sum(W.values(),F(0))/norm;prob=F(success,len(As))
        require(weighted==prob,'cap canonical normalized probability')
        cases.append({'p':p,'k':k,'t':t,'successful_A':success,'total_A':len(As),'success_probability':rat(prob),
                      'canonical_weighted_sum':rat(sum(W.values(),F(0))),'normalization':rat(norm),
                      'graph_weights':[{'edges':[list(e) for e in J],'W':rat(w)} for J,w in sorted(W.items())],
                      'dropping_canonicality_gives_expected_cover_count':rat(F(all_cover_count,len(As))),
                      'dividing_representation_weight_twice_gives':rat(double_weight/norm)})
    require(any(F(*r['dropping_canonicality_gives_expected_cover_count'])>1 for r in cases),'missing canonicality negative guard')
    require(any(r['dividing_representation_weight_twice_gives']!=r['success_probability'] for r in cases),'missing double-division guard')
    return {'selected_labeled_representation_graphs':selected_graphs,'cases':cases}

def run():
    return {'scope':'Compact exact synthetic checks; no asymptotic claim.','resolution_claimed':False,
            'exchange':exchanges(),'restriction':restrictions(),'canonical':canonical_counts()}
if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
