#!/usr/bin/env python3
"""Exact rational controls. These support, and do not replace, the written proofs."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, gcd, lcm
from pathlib import Path
import json, sys
if not __debug__:
    raise SystemExit('Run without -O; assertions are required.')

COUNT = 0
def check(condition, label):
    global COUNT
    if not condition:
        raise AssertionError(label)
    COUNT += 1

def dot(a,b): return sum((x*y for x,y in zip(a,b)), Q(0))
def add(*vs): return tuple(sum(z,Q(0)) for z in zip(*vs))
def scale(c,v): return tuple(c*x for x in v)
def determinant(a):
    n=len(a)
    if n == 0: return Q(1)
    return sum(((-1)**j*a[0][j]*determinant([row[:j]+row[j+1:] for row in a[1:]]) for j in range(n)),Q(0))
def rank(a):
    a=[list(map(Q,row)) for row in a];r=0
    for j in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][j]),None)
        if k is None: continue
        a[r],a[k]=a[k],a[r];p=a[r][j];a[r]=[v/p for v in a[r]]
        for k in range(len(a)):
            if k!=r:
                p=a[k][j];a[k]=[x-p*y for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a):break
    return r

def inv(a):
    n=len(a);out=[]
    for j in range(n):
        b=[row+[Q(i==j)] for i,row in enumerate(a)];r=0
        for k in range(n):
            p=next((p for p in range(r,n) if b[p][k]),None)
            if p is None:return None
            b[p],b[r]=b[r],b[p];q=b[r][k];b[r]=[v/q for v in b[r]]
            for p in range(n):
                if p!=r:
                    q=b[p][k];b[p]=[x-q*y for x,y in zip(b[p],b[r])]
            r+=1
        out.append([row[-1] for row in b])
    return [list(row) for row in zip(*out)]

# Positive rescalings of Grushevsky--Hulek v2 Proposition 4.1, equation (22).
RAYS=[(1,0,0,72),(0,1,0,-12),(0,1,2,-6),(0,0,1,-3),(0,0,1,1)]
NAMES=['A=1152 S_A','F=96 S_F','D=48 S_D','C=48 sigma_C4','K=4 sigma_K3+1']
FACETS=[(1,0,0,0),(0,1,0,0),(-72,12,3,1),(72,-8,1,-1),(72,-12,3,-1)]
FNAMES=['L^2','LM','F1','F2','G']
def facet_values(v):return tuple(dot(n,v) for n in FACETS)
def decomposition(v):
    x,y,z,w=map(Q,v);_,_,p,q,g=facet_values(v)
    if min(x,y,p,q,g)<0:return None
    d=max(Q(0),y-q/4)
    return (x,y-d,d,d+q/4-y,p/4-3*d)
def reconstruct(co):return add(*(scale(a,r) for a,r in zip(co,RAYS)))

check(rank(RAYS)==4,'primal rank')
check(add(RAYS[1],scale(3,RAYS[4]))==add(RAYS[2],RAYS[3]),'unique circuit')
M2=(0,0,1,0)
check(scale(Q(1,6),add(FACETS[2],FACETS[4]))==M2,'M2 redundant')
P=[[dot(n,r) for n in FACETS] for r in RAYS]
check(P==[[1,0,0,0,0],[0,1,0,4,0],[0,1,12,0,0],[0,0,0,4,6],[0,0,4,0,2]],'incidence')
for n in FACETS:
    check(rank([r for r in RAYS if dot(n,r)==0])==3,'facet rank')

# Independently enumerate every possible supporting facet from rank-three triples.
found=set()
for inds in combinations(range(5),3):
    rows=[list(RAYS[i]) for i in inds]
    if rank(rows)!=3:continue
    n=[(-1)**j*determinant([row[:j]+row[j+1:] for row in rows]) for j in range(4)]
    vals=[dot(n,r) for r in RAYS]
    if max(vals)<=0:n=[-v for v in n];vals=[-v for v in vals]
    if min(vals)<0:continue
    d=lcm(*(v.denominator for v in n));a=[int(v*d) for v in n];g=gcd(*a)
    found.add(tuple(v//g for v in a))
check(found==set(FACETS),'complete independent facet enumeration')

bases=[]
for inds in combinations(range(5),4):
    a=[[Q(RAYS[i][j]) for i in inds] for j in range(4)]
    a_inv=inv(a)
    if a_inv is not None:bases.append((inds,a_inv))
check(len(bases)==4,'number of independent four-ray bases')
def membership_via_bases(v):
    return any(min(dot(row,v) for row in a_inv)>=0 for _,a_inv in bases)
points=0
for x,y,z,u in product(range(3),range(5),range(7),range(-30,31)):
    v=(Q(x),Q(y),Q(z),Q(72*x-12*y+u));co=decomposition(v)
    check((co is not None)==membership_via_bases(v),'independent membership')
    if co is not None:
        check(min(co)>=0 and reconstruct(co)==v,'constructive membership')
    points+=1

# V2's displayed dual cone does not equal the polar of equation (22).
u=(0,1,0,-10)
printed=[FACETS[0],FACETS[1],M2,FACETS[2],FACETS[3]]
check([dot(n,u) for n in printed]==[0,1,0,2,2],'printed tests witness')
check(dot(FACETS[4],u)==-2 and not membership_via_bases(u),'missing facet witness')

# Corrected van der Geer v3 tables 3c--3f, sigma1=D and sigma2=beta2.
Dmix=list(map(Q,['1/181440','0','0','1/720','0','-203/240','-4103/144']))
Bmix=list(map(Q,['0','0','0','-11/48','-445/48']))
t=[sum((Q(comb(j,k))*12**(j-k)*(-1)**k*Dmix[k] for k in range(j+1)),Q(0)) for j in range(7)]
b=[sum((Q(comb(j,k))*12**(j-k)*(-1)**k*Bmix[k] for k in range(j+1)),Q(0)) for j in range(5)]
expected=list(map(Q,['1/181440','1/15120','1/1260','41/5040','1/21','73/336','871/1008']))
check(t==expected,'mixed divisor degrees')
check(b==list(map(Q,['0','0','0','11/48','83/48'])),'beta mixed degrees')
ci=[]
for j in range(5):
    v=(t[j],t[j+1],t[j+2],b[j]);co=decomposition(v)
    check(min(facet_values(v))>0,'complete intersection strict facets')
    check(co is not None and min(co)>=0 and reconstruct(co)==v,'complete intersection decomposition')
    ci.append({'j':j,'coordinates':v,'facets':facet_values(v),'decomposition':co})
# Full universal mixed-divisor argument is expansion with nonnegative coefficients.
ci_trials=0
for coeffs in product([(0,1),(1,0),(1,1),(1,2)],repeat=4):
    poly=[Q(1)]
    for a,c in coeffs:
        nxt=[Q(0)]*(len(poly)+1)
        for k,v in enumerate(poly):nxt[k]+=a*v;nxt[k+1]+=c*v
        poly=nxt
    v=add(*(scale(poly[j],ci[j]['coordinates']) for j in range(5)))
    co=decomposition(v)
    check(co is not None and reconstruct(co)==v,'mixed complete intersection trial')
    ci_trials+=1

# Closed-face cautions, with an explicitly unrealized cone model.
limit=(0,0,1,2)
check(add(scale(Q(4,5),limit),scale(Q(1,5),RAYS[3]))==RAYS[4],'closure loss of extremality')
for n in range(6,70):
    v=(Q(1,n*n),Q(1,n),Q(1),Q(2));x,y,z,w=v
    check(x>0 and y>0 and z>0 and y*y==x*z,'model Hodge equality')
    check(dot(FACETS[3],v)<0,'model outside proposed cone')
    c=(z-w)/4;k=(3*z+w)/4
    check(c<0 and k>0,'limit direction lower face obstruction')

# Theta localization identity; the geometric input is explicitly credited in the proof.
check(add(FACETS[3],(0,-4,2,0))==FACETS[4],'G localization identity')
for y in range(8):
    for z in range(24):
        if 3*z>=8*y:check(2*z-4*y>=0,'localization nonnegative difference')

# Exact numerical candidates; no effectivity is asserted.
candidates=[('fails_F1',(1,3,9,0)),('fails_F2',(1,4,16,57))]
candidate_rows=[]
for label,v in candidates:
    x,y,z,w=v
    tests=[x,y,z,w,12*x-y,12*y-z,y-3*x,z-3*y,3*y-8*x,3*z-8*y,y*y-x*z]
    check(min(tests)>=0,'candidate passes listed necessary tests')
    check(min(facet_values(v))<0 and not membership_via_bases(v),'candidate outside cone')
    for r in RAYS:
        # A is isolated by y=z=0; the remaining original rays have x=0.
        check((r[0]==0 and x>0) or (r[1]==0 and r[2]==0 and y>0),'old-ray extremality cannot use candidate')
    candidate_rows.append({'label':label,'coordinates':v,'facets':facet_values(v),'listed_necessary_tests':tests})

def convert(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {k:convert(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [convert(v) for v in x]
    return x
result={'status':'PASS','assertions':COUNT,'grid_points':points,'mixed_complete_intersection_trials':ci_trials,'normalized_rays':RAYS,'facet_normals':FACETS,'pairing_matrix':P,'printed_dual_witness':{'coordinates':u,'G':-2},'complete_intersections':ci,'unrealized_candidates':candidate_rows,'limits':'Exact finite controls supplement the written proofs. No geometric counterexample or full solution is asserted.'}
print(json.dumps(convert(result),indent=2,sort_keys=True))
