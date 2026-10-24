#!/usr/bin/env python3
"""Exact finite permutation witnesses; bounded absence is not a theorem."""
from itertools import permutations,product
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime,timezone
import json,argparse
PAIRS=[(3,2),(20,14),(119,84)]

def parts(n,lo=1):
    if not n:yield []
    for k in range(lo,n+1):
        for rest in parts(n-k,k):yield [k]+rest

def class_reps(n):
    for par in parts(n):
        p=list(range(n));s=0
        for k in par:
            for j in range(k):p[s+j]=s+(j+1)%k
            s+=k
        yield tuple(p)

def transitive(ps,n):
    seen={0};todo=[0]
    while todo:
        x=todo.pop()
        for p in ps:
            y=p[x]
            if y not in seen:seen.add(y);todo.append(y)
    return len(seen)==n

def matrix(ps,n):
    rows=[]
    for (p,q),sigma in zip(PAIRS,ps):
        for j in range(n):
            row=[0]*(3*n)
            row[sigma[j]]+=p;row[n+j]-=q
            row[2*n+sigma[j]]+=1;row[2*n+j]-=1
            rows.append(row)
    return rows

def rank_mod(m,prime=65521):
    m=[[x%prime for x in r] for r in m];nr=len(m);nc=len(m[0]);k=0
    for c in range(nc):
        r=next((i for i in range(k,nr) if m[i][c]),None)
        if r is None:continue
        m[k],m[r]=m[r],m[k];inv=pow(m[k][c],-1,prime)
        m[k]=[(x*inv)%prime for x in m[k]]
        for i in range(k+1,nr):
            a=m[i][c]
            if a:m[i]=[(x-a*y)%prime for x,y in zip(m[i],m[k])]
        k+=1
        if k==nr:return k
    return k

def rational_kernel(m):
    m=[[F(x) for x in r] for r in m];nr=len(m);nc=len(m[0]);k=0;piv=[]
    for c in range(nc):
        r=next((i for i in range(k,nr) if m[i][c]),None)
        if r is None:continue
        m[k],m[r]=m[r],m[k];v=m[k][c];m[k]=[x/v for x in m[k]]
        for i in range(nr):
            if i!=k and m[i][c]:
                v=m[i][c];m[i]=[x-v*y for x,y in zip(m[i],m[k])]
        piv.append(c);k+=1
    for f in set(range(nc))-set(piv):
        v=[F(0)]*nc;v[f]=F(1)
        for i,c in enumerate(piv):v[c]=-m[i][f]
        yield v

def run(max_degree):
    counts=[]
    for n in range(1,max_degree+1):
        perms=list(permutations(range(n)));tested=0;mod_degenerate=0
        for s1 in class_reps(n):
            for s2,s3 in product(perms,repeat=2):
                ps=(s1,s2,s3)
                if not transitive(ps,n):continue
                tested+=1;m=matrix(ps,n)
                if rank_mod(m)==3*n-1:continue
                mod_degenerate+=1
                for v in rational_kernel(m):
                    if any(v[:n]):
                        assert any(v[n:2*n])
                        assert all(sum(F(x)*y for x,y in zip(r,v))==0 for r in m)
                        return {'result':'POSITIVE_WITNESS','degree':n,'permutations':ps,'vector':[str(x) for x in v],'counts':counts+[{'degree':n,'tested':tested,'mod_degenerate':mod_degenerate}],'scope':'A nonzero horizontal exact finite-permutation representation yields a vertex-injective Euclidean-by-finite map after adjoining the independent height coordinate. This is a positive result for this candidate only.'}
        counts.append({'degree':n,'tested':tested,'mod_degenerate':mod_degenerate})
    return {'result':'NO_WITNESS_IN_BOUND','counts':counts,'scope':'Exhaustive up to simultaneous conjugacy for transitive permutation degree at most the indicated bound. No conclusion for larger finite holonomy groups.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--max-degree',type=int,default=4);args=ap.parse_args()
    result=run(args.max_degree);result['utc']=datetime.now(timezone.utc).isoformat()
    Path(__file__).with_name('finite_holonomy_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
