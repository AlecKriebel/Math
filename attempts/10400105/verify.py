#!/usr/bin/env python3
"""Finite diagnostics for a general proof. No downloaded code or external packages."""
import itertools as it
import json
from collections import Counter
from pathlib import Path

counts=Counter()
def check(ok, family):
    if not ok: raise AssertionError(family)
    counts[family]+=1

def nullspace(rows,p,n):
    a=[list(map(lambda x:x%p,r)) for r in rows]; piv=[]; row=0
    for col in range(n):
        i=next((i for i in range(row,len(a)) if a[i][col]),None)
        if i is None:continue
        a[row],a[i]=a[i],a[row]; q=pow(a[row][col],-1,p)
        a[row]=[(q*x)%p for x in a[row]]
        for i in range(len(a)):
            if i!=row and a[i][col]:
                q=a[i][col];a[i]=[(x-q*y)%p for x,y in zip(a[i],a[row])]
        piv.append(col);row+=1
    out=[]
    for free in (j for j in range(n) if j not in piv):
        v=[0]*n;v[free]=1
        for i,j in enumerate(piv):v[j]=-a[i][free]%p
        out.append(v)
    return out

def scalar_case(p,r):
    X=range(3); star=lambda x,y:(2*y-x)%3
    pairs=list(it.product(X,repeat=2));idx={xy:i for i,xy in enumerate(pairs)}
    ri=pow(r,-1,p)
    rows=[]
    for x in X:
        row=[0]*9;row[idx[x,x]]=1;rows.append(row)
    for x,y,z in it.product(X,repeat=3):
        row=[0]*9
        for xy,c in [((x,y),ri),((star(x,y),z),1),((x,z),-ri),((y,z),-ri*(r-1)),((star(x,z),star(y,z)),-1)]:row[idx[xy]]+=c
        rows.append(row)
    basis=nullspace(rows,p,9)
    cocycles=[]
    for co in it.product(range(p),repeat=len(basis)):
        v=tuple(sum(a*b[j] for a,b in zip(co,basis))%p for j in range(9))
        cocycles.append(v)
    colors=[c for c in it.product(X,repeat=3) if star(c[0],c[1])==c[2] and star(c[1],c[2])==c[0] and star(c[2],c[0])==c[1]]
    hist=Counter(); noncoboundary=0
    cob={tuple((ri*(f[x]+(r-1)*f[y])-f[star(x,y)])%p for x,y in pairs) for f in it.product(range(p),repeat=3)}
    for phi in cocycles:
        noncoboundary+=phi not in cob
        def op(a,b):
            u,x=a;v,y=b
            return ((ri*(u+(r-1)*v)+phi[idx[x,y]])%p,star(x,y))
        E=list(it.product(range(p),X))
        for a in E:check(op(a,a)==a,'scalar_idempotency')
        for b in E:check(len({op(a,b) for a in E})==len(E),'scalar_right_bijections')
        # Full distributivity for every cocycle, rather than selected triples.
        for a,b,c in it.product(E,repeat=3):check(op(op(a,b),c)==op(op(a,c),op(b,c)),'scalar_distributivity')
        for col in colors:
            def L(a):return tuple((a[(i+2)%3]-ri*a[i]-ri*(r-1)*a[(i+1)%3])%p for i in range(3))
            rhs=tuple(phi[idx[col[i],col[(i+1)%3]]] for i in range(3))
            arr=list(it.product(range(p),repeat=3));kernel=[a for a in arr if L(a)==(0,0,0)]
            sol=[a for a in arr if L(a)==rhs]
            direct=[a for a in arr if all(op((a[i],col[i]),(a[(i+1)%3],col[(i+1)%3]))==(a[(i+2)%3],col[(i+2)%3]) for i in range(3))]
            check(sol==direct,'presentation_lifts')
            check(not sol or len(sol)==len(kernel),'torsor_size')
            if sol:
                check({tuple((x+y)%p for x,y in zip(sol[0],k)) for k in kernel}==set(sol),'torsor_action')
            hist[len(sol)]+=1
        # Representative change, all cochains, all pairs of extension points.
        for f in it.product(range(p),repeat=3):
            new=tuple((phi[idx[x,y]]+ri*(f[x]+(r-1)*f[y])-f[star(x,y)])%p for x,y in pairs)
            for a,b in it.product(E,repeat=2):
                u,x=a;v,y=b;w,z=op(a,b)
                rhs=(ri*(u-f[x]+(r-1)*(v-f[y]))+new[idx[x,y]])%p
                check((w-f[z])%p==rhs,'coboundary_extension_isomorphism')
        # All one-crossing gauge identities, source versus CEGS coordinates.
        for a,b in it.product(E,repeat=2):
            u,x=a;v,y=b;w,z=op(a,b)
            check(ri*w%p==(ri*(ri*u)+(1-ri)*(ri*v)+ri*phi[idx[x,y]])%p,'scalar_gauge')
    return {'p':p,'constant_action':r,'cocycle_dimension':len(basis),'cocycles':len(cocycles),'noncoboundary_cocycles':noncoboundary,'trefoil_base_colorings':len(colors),'lift_count_histogram_over_cocycles_and_colorings':dict(sorted(hist.items()))}

# Noncommuting action: X is the transpositions in S3 acting on A=F2^3.
perms=list(it.permutations(range(3)))
def compose(s,t):return tuple(s[t[i]] for i in range(3))
def inverse(s):return tuple(s.index(i) for i in range(3))
X=[s for s in perms if sum(s[i]!=i for i in range(3))==2]
def star(x,y):return compose(inverse(y),compose(x,y))
V=list(it.product(range(2),repeat=3));zero=(0,0,0)
def add(*vv):return tuple(sum(v[i] for v in vv)%2 for i in range(3))
def act(s,v):return tuple(v[inverse(s)[i]] for i in range(3))
def eta(x,y,a):return act(inverse(y),a)
def tau(x,y,a):return act(inverse(y),add(act(x,a),a))
for x,y in it.product(X,repeat=2):
    check(star(x,y) in X,'noncommuting_action_closure')
    for a in V:check(act(star(x,y),a)==act(inverse(y),act(x,act(y,a))),'noncommuting_action_law')
# A fixed nonconstant cochain yields a genuine gauge test with mixed coordinates.
f={x:V[i+1] for i,x in enumerate(X)}
def phi(x,y):return add(eta(x,y,f[x]),tau(x,y,f[y]),f[star(x,y)])
def op(a,b):
    u,x=a;v,y=b
    return add(eta(x,y,u),tau(x,y,v),phi(x,y)),star(x,y)
E=list(it.product(V,X))
for a in E:check(op(a,a)==a,'vector_idempotency')
for b in E:check(len({op(a,b) for a in E})==len(E),'vector_right_bijections')
for a,b,c in it.product(E,repeat=3):check(op(op(a,b),c)==op(op(a,c),op(b,c)),'vector_distributivity')
for a,b in it.product(E,repeat=2):
    u,x=a;v,y=b;w,z=op(a,b)
    left=act(inverse(z),w)
    U=act(inverse(x),u);W=act(inverse(y),v)
    right=add(act(inverse(y),U),W,act(inverse(z),W),act(inverse(z),phi(x,y)))
    check(left==right,'noncommuting_gauge')
# Reidemeister II and III as actual switches on the finite extension.
def switch(a,b):return b,op(a,b)
for a,b in it.product(E,repeat=2):
    out=switch(a,b)
    recovered=next(q for q in E if op(q,out[0])==out[1])
    check((recovered,out[0])==(a,b),'switch_inverse')
for a,b,c in it.product(E,repeat=3):
    v=[a,b,c]
    for j in (0,1,0):v[j:j+2]=switch(*v[j:j+2])
    w=[a,b,c]
    for j in (1,0,1):w[j:j+2]=switch(*w[j:j+2])
    check(v==w,'switch_braid_relation')

out={'status':'PASS','scope':'Exact finite algebra, affine lifting, gauge and local-move diagnostics; the proof and published input audit establish the general claims. No numerical approximations.','scalar_cases':[scalar_case(3,1),scalar_case(3,2)],'assertions_by_family':dict(sorted(counts.items())),'total_assertions':sum(counts.values())}
path=Path(__file__).with_name('verification.json');path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
