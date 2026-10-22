#!/usr/bin/env python3
"""Independent finite-algebra controls; standard-library exact arithmetic only."""
from pathlib import Path
from hashlib import sha256
from itertools import product, permutations
from collections import Counter
import json
C=Counter()
def ck(cat,x):
    assert x,cat
    C[cat]+=1
def mul(a,b,n,p):return tuple(sum(a[n*i+k]*b[n*k+j] for k in range(n))%p for i in range(n) for j in range(n))
def ident(n):return tuple(int(i==j) for i in range(n) for j in range(n))
def power(a,j,n,p):
    b=ident(n)
    for _ in range(j):b=mul(b,a,n,p)
    return b
def commute(a,b,n,p):return mul(a,b,n,p)==mul(b,a,n,p)
def analyze(algebra,gens,n,p):
    fixed=[a for a in algebra if all(commute(a,g,n,p) for g in gens)]
    center=[a for a in fixed if all(commute(a,b,n,p) for b in fixed)]
    ids=[a for a in center if mul(a,a,n,p)==a]
    ambient=[a for a in algebra if all(commute(a,b,n,p) for b in algebra) and mul(a,a,n,p)==a]
    ck('fixed_central_idempotent_equality',set(ids)==set(ambient))
    for a in center:
        ck('fixed_algebra_center_check',all(commute(a,g,n,p) for g in gens))
    return fixed,ids
for p in (2,3,5):
    alg=list(product(range(p),repeat=4));u=(1,1,0,1)
    ck('unipotent_order',power(u,p,2,p)==ident(2) and u!=ident(2))
    fixed,ids=analyze(alg,[u],2,p)
    ck('matrix_centralizer_size',len(fixed)==p*p)
    ck('matrix_block_count',len(ids)==2)

# A nonabelian p-group acting on a nonsemisimple algebra.
alg=[(a,b,c,0,d,e,0,0,f) for a,b,c,d,e,f in product(range(2),repeat=6)]
u=(1,1,0,0,1,0,0,0,1);v=(1,0,0,0,1,1,0,0,1)
gp={ident(3)}
while True:
    new=gp|{mul(g,h,3,2) for g in gp for h in (u,v)}
    if new==gp:break
    gp=new
ck('nonabelian_p_group',len(gp)==8 and not commute(u,v,3,2))
fixed,ids=analyze(alg,[u,v],3,2)
ck('triangular_indecomposability',len(ids)==2)
vectors=list(product(range(2),repeat=3))
act=lambda a,x:tuple(sum(a[3*i+j]*x[j] for j in range(3))%2 for i in range(3))
fv=[x for x in vectors if all(act(g,x)==x for g in (u,v))]
ck('nonabelian_fixed_vector',len(fv)==2 and (1,0,0) in fv)

# Having p-element generators alone is not the p-group hypothesis.
u2=(1,1,0,1);v2=(1,0,1,1)
gp={ident(2)}
while True:
    new=gp|{mul(g,h,2,2) for g in gp for h in (u2,v2)}
    if new==gp:break
    gp=new
act2=lambda a,x:tuple(sum(a[2*i+j]*x[j] for j in range(2))%2 for i in range(2))
ck('generator_order_is_insufficient',len(gp)==6 and power(u2,2,2,2)==ident(2) and power(v2,2,2,2)==ident(2))
ck('generator_order_is_insufficient',all(x==(0,0) for x in product(range(2),repeat=2) if act2(u2,x)==x and act2(v2,x)==x))

# External p-group actions permute blocks. Check the orbit-sum assertion.
for p,perm in ((2,(1,0,3,2,4)),(3,(1,2,0,3))):
    n=len(perm);vals=list(product(range(p),repeat=n))
    fixed=[a for a in vals if tuple(a[perm[i]] for i in range(n))==a]
    ids=[a for a in fixed if all(x*x%p==x for x in a)]
    orbits=[];unseen=set(range(n))
    while unseen:
        start=min(unseen);orbit={start};q=perm[start]
        while q!=start:orbit.add(q);q=perm[q]
        unseen-=orbit;orbits.append(orbit)
    ck('external_orbit_count',len(ids)==2**len(orbits))
    for a in ids:
        ck('external_orbit_sum',all(len({a[i] for i in o})==1 for o in orbits))

# Characteristic-three non-p-group control and its Peirce space.
p=3;alg=list(product(range(p),repeat=4));d=(1,0,0,2)
fixed=[a for a in alg if commute(a,d,2,p)]
ids=[a for a in fixed if mul(a,a,2,p)==a]
ck('sign_control_fixed_algebra',set(fixed)=={(a,0,0,b) for a,b in product(range(3),repeat=2)})
ck('sign_control_idempotents',len(ids)==4)
e=(1,0,0,0);f=(0,0,0,1);x=(0,1,0,0)
ck('Peirce_nonfixed_control',mul(e,x,2,p)==x and mul(x,e,2,p)==(0,0,0,0))
ck('Peirce_nonfixed_control',mul(mul(d,x,2,p),d,2,p)==tuple((-a)%p for a in x))
ck('Peirce_nonfixed_control',e in ids and not all(commute(e,a,2,p) for a in alg))

# A fresh odd-prime, nonnormal subgroup: A4 with P=< (123) > in characteristic 3.
def comp(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inv(a):return tuple(a.index(i) for i in range(len(a)))
def parity(a):return sum(a[i]>a[j] for i in range(len(a)) for j in range(i+1,len(a)))%2
G=[g for g in permutations(range(4)) if parity(g)==0];ix={g:i for i,g in enumerate(G)}
N=len(G);p=3;gen=(1,2,0,3);P={tuple(range(4)),gen,comp(gen,gen)}
table=[[ix[comp(g,h)] for h in G] for g in G]
def gm(a,b):
    out=[0]*N
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:out[table[i][j]]=(out[table[i][j]]+x*y)%p
    return tuple(out)
unseen=set(G);basis=[]
while unseen:
    g=min(unseen);o={comp(comp(h,g),inv(h)) for h in P};unseen-=o
    basis.append(tuple(int(x in o) for x in G))
ck('odd_prime_nonnormal',any(comp(comp(g,h),inv(g)) not in P for g in G for h in P))
def kernel(rows,n):
    a=[list(row) for row in rows if any(row)];piv=[];rr=0
    for col in range(n):
        k=next((k for k in range(rr,len(a)) if a[k][col]%p),None)
        if k is None:continue
        a[rr],a[k]=a[k],a[rr];c=pow(a[rr][col],-1,p);a[rr]=[(c*x)%p for x in a[rr]]
        for k in range(len(a)):
            if k!=rr:
                c=a[k][col];a[k]=[(x-c*y)%p for x,y in zip(a[k],a[rr])]
        piv.append(col);rr+=1
        if rr==len(a):break
    out=[]
    for free in set(range(n))-set(piv):
        v=[0]*n;v[free]=1
        for j,col in enumerate(piv):v[col]=-a[j][free]%p
        ck('odd_prime_kernel_certificate',all(sum(x*y for x,y in zip(row,v))%p==0 for row in rows))
        out.append(tuple(v))
    return out
def combine(coeff,basis):return tuple(sum(c*v[i] for c,v in zip(coeff,basis))%p for i in range(N))
rows=[]
for b in basis:
    cols=[tuple((x-y)%p for x,y in zip(gm(a,b),gm(b,a))) for a in basis]
    rows += [tuple(c[i] for c in cols) for i in range(N)]
zbase=[combine(c,basis) for c in kernel(rows,len(basis))]
zvals=[combine(c,zbase) for c in product(range(p),repeat=len(zbase))]
ids=[a for a in zvals if gm(a,a)==a]
std=[tuple(int(i==j) for i in range(N)) for j in range(N)]
for a in ids:ck('odd_prime_ambient_centrality',all(gm(a,b)==gm(b,a) for b in std))
# Independently form the ambient center from ordinary conjugacy classes.
unseen=set(G);amb=[]
while unseen:
    g=min(unseen);o={comp(comp(h,g),inv(h)) for h in G};unseen-=o
    amb.append(tuple(int(x in o) for x in G))
avals=[combine(c,amb) for c in product(range(p),repeat=len(amb))]
aids=[a for a in avals if gm(a,a)==a]
ck('odd_prime_equal_idempotent_sets',set(ids)==set(aids))
# Class-sum calculation for S3 in characteristic 3, independent direct multiplication.
SG=list(permutations(range(3)));six={g:i for i,g in enumerate(SG)}
st=[[six[comp(g,h)] for h in SG] for g in SG]
def sm(a,b):
    out=[0]*6
    for i in range(6):
        for j in range(6):out[st[i][j]]=(out[st[i][j]]+a[i]*b[j])%3
    return tuple(out)
one=tuple(int(g==tuple(range(3))) for g in SG)
tt=tuple(int(parity(g)==1) for g in SG)
cc=tuple(int(g!=tuple(range(3)) and parity(g)==0) for g in SG)
jj=tuple((a+b)%3 for a,b in zip(one,cc))
ck('S3_center_radical',sm(tt,tt)==(0,)*6)
ck('S3_center_radical',sm(jj,jj)==(0,)*6)
ck('S3_center_radical',sm(tt,jj)==(0,)*6)
for a,b,c in product(range(3),repeat=3):
    v=tuple((a*x+b*y+c*z)%3 for x,y,z in zip(one,tt,jj))
    ck('S3_center_only_trivial_idempotents',(sm(v,v)==v)==(b==0 and c==0 and a in (0,1)))
root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),
     'A4_char3_control':{'group_order':N,'subgroup_order':len(P),'fixed_dimension':len(basis),'center_dimension':len(zbase),'central_idempotents':len(ids),'nonnormal':True},
     'artifact_sha256':sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),
     'scope':'Finite controls for the abstract p-group theorem and its stated limits; no general symmetric-subgroup result.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

