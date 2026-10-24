#!/usr/bin/env python3
"""Exact finite metabelian quotient covers of the canonical Hydra square complex.
No positive result is inferred from finite testing; a failure is cover-specific.
"""
import argparse, itertools, json, math
from pathlib import Path

class DSU:
    def __init__(self,n): self.p=list(range(n)); self.sz=[1]*n
    def find(self,x):
        while self.p[x]!=x:
            self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self,a,b):
        a,b=self.find(a),self.find(b)
        if a==b:return
        if self.sz[a]<self.sz[b]:a,b=b,a
        self.p[b]=a;self.sz[a]+=self.sz[b]

def binomial(n,k):
    z=1
    for i in range(k): z=z*(n-i)//(i+1)
    return z

def experiment(m,p):
    order=1
    while order<m:order*=p
    vectors=list(itertools.product(range(p),repeat=m)); encode={v:i for i,v in enumerate(vectors)}
    size=len(vectors)*order
    def phi(v,k):
        return tuple(sum(binomial(k,j)*v[i+j] for j in range(m-i))%p for i in range(m))
    def mul(x,y):
        v,k=x;w,l=y;pw=phi(w,-k)
        return tuple((a+b)%p for a,b in zip(v,pw)),(k+l)%order
    def inv(x):
        v,k=x
        return phi(tuple(-a%p for a in v),k),-k%order
    zero=(0,)*m
    s=(zero,-1%order); alpha=[None]*(m+1);alpha[m]=(zero[:-1]+(1,),0)
    for i in range(m-1,0,-1):alpha[i]=mul(mul(inv(alpha[i+1]),s),alpha[i+1])
    generators=[s]+alpha[1:]
    assert mul(mul(inv(alpha[1]),s),alpha[1])==s
    for i in range(2,m+1):assert mul(mul(inv(alpha[i]),s),alpha[i])==alpha[i-1]
    def perm(x):
        ans=[]
        for k in range(order):
            shift=phi(x[0],-k); target=(k+x[1])%order
            for v in vectors: ans.append(target*len(vectors)+encode[tuple((a+b)%p for a,b in zip(v,shift))])
        assert len(set(ans))==size
        return ans
    action=[perm(x) for x in generators]
    d=DSU(size*(m+1))
    def edge(g,i):return g*(m+1)+i
    for g in range(size):
        for i in range(1,m+1):
            d.union(edge(g,i),edge(action[0][g],i))
            d.union(edge(g,0),edge(action[i][g],0 if i==1 else i-1))
    witnesses=[]
    for g in range(size):
        for i in range(1,m+1):
            if d.find(edge(g,0))==d.find(edge(g,i)):
                witnesses.append({'vertex':g,'square':i})
                if len(witnesses)>=12:break
        if len(witnesses)>=12:break
    return {'rank':m,'prime':p,'stable_letter_order':order,'vertices':size,'hyperplanes':len({d.find(i) for i in range(size*(m+1))}),'self_crossing':bool(witnesses),'first_self_crossings':witnesses,'quotient_generators':[{'fiber':v,'height':k} for v,k in generators]}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--max-rank',type=int,default=6);args=parser.parse_args()
    data=[experiment(m,p) for m in range(2,args.max_rank+1) for p in (2,3,5) if p**m * (p**math.ceil(math.log(m,p)))<250000]
    out=Path(__file__).with_name('finite_cover_results.json');out.write_text(json.dumps({'scope':'Canonical square covers from explicitly defined metabelian finite quotients only','results':data},indent=2)+'\n')
    for r in data:print(r['rank'],r['prime'],r['vertices'],r['hyperplanes'],r['self_crossing'])
