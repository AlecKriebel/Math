#!/usr/bin/env python3
"""Independent exact checks; no mapping-class or geometric proof oracle."""
from itertools import product
from collections import Counter
import json
import sys

def check(x, label):
    if not x:
        raise ValueError(label)

def mm(a,b,mod=None):
    n=len(a)
    v=tuple(tuple(sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)) for i in range(n))
    return v if mod is None else tuple(tuple(t%mod for t in row) for row in v)

def ident(n): return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def multiply_word(w, n, mod=None):
    r=ident(n)
    for a in w:r=mm(r,a,mod)
    return r

def inv2(a): return ((a[1][1],-a[0][1]),(-a[1][0],a[0][0]))
def cg(h,x):return mm(mm(h,x),inv2(h))

def integer_and_hurwitz():
    a=((1,1),(0,1));b=((1,0),(-1,1)); w=[a,b]*3
    z=multiply_word(w,2)
    check(z==((-1,0),(0,-1)),'negative identity')
    check(mm(mm(a,b),a)==mm(mm(b,a),b),'braid')
    check(multiply_word(w+w,2)==ident(2),'boundary homology')
    check(mm(z,a)==mm(a,z),'centralizer witness')
    # Five inverse moves move a to the end, conjugating the others by a.
    t=list(w);states=[t.copy()]
    for i in range(5):
        x,y=t[i:i+2]; t[i:i+2]=[cg(x,y),x];states.append(t.copy())
    # Five inverse moves move that last factor to the front. Since total z is
    # central, the resulting first factor is a, and the other factors stay put.
    for i in range(4,-1,-1):
        x,y=t[i:i+2];t[i:i+2]=[cg(x,y),x];states.append(t.copy())
    check(t==[cg(a,x) for x in w],'ten-move conjugation identity')
    check(all(multiply_word(s,2)==z for s in states),'all intermediate products')
    count=0
    for p,q,r,s in product(range(-8,9),repeat=4):
        if p*s-q*r !=1:continue
        m=((p,q),(r,s));count+=1
        check((mm(m,a)==mm(a,m))==(r==0 and s==p and p in (-1,1)),'centralizer identity')
    return {'integer_matrices':count,'hurwitz_steps':10,'block_image':z,'scope':'integer images plus algebraic Hurwitz identity; boundary equality uses two-chain relation'}

def doubling():
    count=0
    for m in range(1,71):
        for j in range(m+1):
            ks=[m-j,m+3*j,m-2*j]
            if min(ks)<1 or ks[0]>m or ks[1]>4*ks[0] or ks[2]>4*ks[1]:continue
            data={0:m}; genus=2*m+1; g0=genus; blowups=0
            for k in ks:
                blowups+=data[0]-k
                new={0:4*k,1:0,2:data[0]+data.get(1,0)-k}
                for degree,value in data.items():
                    if degree>=2:new[degree+1]=value
                data=new;genus=2*genus+k-1
            want=[4*m-8*j,0,3*m+14*j,3*m-7*j,j]
            check(all(data.get(i,0)==v for i,v in enumerate(want)),'exceptional data')
            check(blowups+data[0]==10*m,'total blowups')
            check(genus==8*g0+7*m-7,'genus')
            count+=1
    return {'admissible_sequences':count,'m_range':[1,70],'scope':'arithmetic only; no existence inferred'}

def pairing(x,y,n):
    return sum(((x>>(2*i))&1)*((y>>(2*i+1))&1)+((x>>(2*i+1))&1)*((y>>(2*i))&1) for i in range(n))%2

def mv(a,x):
    return sum((sum(a[i][j]*((x>>j)&1) for j in range(len(a)))%2)<<i for i in range(len(a)))

def trans(a,n):
    cols=[(1<<i) ^ (a if pairing(a,1<<i,n) else 0) for i in range(2*n)]
    return tuple(tuple((cols[j]>>i)&1 for j in range(2*n)) for i in range(2*n))

def q(x,l):return (sum(((x>>(2*i))&1)*((x>>(2*i+1))&1) for i in range(2))+(x&l).bit_count())%2

def quadratic():
    count=0
    for a,l,x in product(range(16),repeat=3):
        tx=mv(trans(a,2),x)
        check(q(tx,l)==(q(x,l)+pairing(x,a,2)*(q(a,l)+1))%2,'quadratic formula')
        count+=1
    a=5; basis=[1,2,4,8]; before=[2,2]+sum(([v,v] for v in basis),[])
    after=[mv(trans(a,2),v) for v in before[:2]]+before[2:]
    f=lambda vectors:[l for l in range(16) if all(q(v,l)==1 for v in vectors)]
    check(f(before)==[15] and f(after)==[],'common refinement failure')
    check(multiply_word([trans(v,2) for v in before],4,2)==ident(4),'before identity product')
    check(multiply_word([trans(v,2) for v in after],4,2)==ident(4),'after identity product')
    check(multiply_word([trans(v,2) for v in before[:2]],4,2)==ident(4),'block identity')
    return {'formula_cases':count,'before_vectors':before,'after_vectors':after,'before_refinements':[15],'after_refinements':[],'scope':'Sp(4,F2) only'}

def finite_orbits():
    ts=[trans(a,1) for a in [1,2,3]]; e=ident(2)
    words=[w for w in product(range(3),repeat=6) if multiply_word([ts[a] for a in w],2,2)==e]
    idx={w:i for i,w in enumerate(words)}
    check(len(words)==243,'identity word count')
    def conjugate(t,s):return ts.index(mm(mm(ts[t],ts[s],2),ts[t],2))
    parents=[list(range(len(words))),list(range(len(words)))]
    def find(p,i):
        while p[i]!=i:p[i]=p[p[i]];i=p[i]
        return i
    def union(p,i,j):p[find(p,j)]=find(p,i)
    h_edges=0;p_edges=0
    for w in words:
        for i in range(5):
            v=w[:i]+(w[i+1],conjugate(w[i+1],w[i]))+w[i+2:]
            check(v in idx,'Hurwitz product')
            for p in parents:union(p,idx[w],idx[v])
            h_edges+=1
        for start in range(6):
            for end in range(start+1,7):
                block=multiply_word([ts[t] for t in w[start:end]],2,2)
                for t in range(3):
                    if mm(ts[t],block,2)!=mm(block,ts[t],2):continue
                    v=w[:start]+tuple(conjugate(t,s) for s in w[start:end])+w[end:]
                    check(v in idx,'partial product')
                    union(parents[1],idx[w],idx[v]);p_edges+=1
    sizes=[sorted(Counter(find(p,i) for i in range(len(words))).values()) for p in parents]
    check(sizes==[[1,1,1,240],[243]],'components')
    return {'identity_words':len(words),'hurwitz_edges':h_edges,'partial_edges':p_edges,'components':sizes,'scope':'independent 2x2 F2 implementation, undirected union-find'}

def main():
    return {'schema':'boundary-twist-independent-checks-v1','integer_hurwitz':integer_and_hurwitz(),'doubling':doubling(),'quadratic':quadratic(),'finite_orbits':finite_orbits(),'optimize':sys.flags.optimize,'main_problem_resolved':False,'formal_certification':False}

if __name__=='__main__':print(json.dumps(main(),sort_keys=True))
