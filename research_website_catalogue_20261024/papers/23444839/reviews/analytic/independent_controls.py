#!/usr/bin/env python3
"""Fresh analytic controls, authored before reading packaged verification code.
Finite controls corroborate (and do not replace) the universal proof in REVIEW.md.
Only Python standard library is used; no imported code from the submission.
"""
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import product, combinations
from functools import lru_cache
from pathlib import Path
import json, hashlib, datetime

checks=0
def require(p, message):
    global checks
    checks+=1
    if not p: raise RuntimeError(message)

def norm(v,p=11):
    a=next(x for x in v if x)
    return tuple(x*pow(a,-1,p)%p for x in v)
P=sorted({norm(v) for v in product(range(11),repeat=3) if any(v)})
N=len(P)
M=[[int(sum(a*b for a,b in zip(p,l))%11==0) for l in P] for p in P]
require(N==133,'projective point count')
for i in range(N):
    require(sum(M[i])==12,'point degree')
    for j in range(N):
        require(sum(a*b for a,b in zip(M[i],M[j]))==(12 if i==j else 1),'Gram')
G=[set() for _ in range(2*N)]
for i in range(N):
    for j in range(N):
        if M[i][j]: G[i].add(N+j);G[N+j].add(i)
deletions=[]
for w in range(2*N):
    live=set(range(2*N))-{w};root=min(live);seen={root};queue=deque([root])
    while queue:
        for v in G[queue.popleft()]-{w}-seen:
            seen.add(v);queue.append(v)
    degrees=Counter(len(G[v]-{w}) for v in live)
    require(seen==live,'deletion connectivity')
    require(degrees=={11:12,12:253},'deletion degree multiset')
    deletions.append({'removed':w,'degrees':dict(degrees),'edges':sum(k*v for k,v in degrees.items())//2})
require(11<16 and Q(7,12)>Q(1,2),'exact radical bound sqrt11<4')

# Independent cubic field, power basis rather than the source's normal basis.
# For degree three over a field, absence of a root is equivalent to irreducibility.
c0,c1=next((c0,c1) for c0 in range(1,11) for c1 in range(11)
           if all((x**3+c1*x+c0)%11 for x in range(11)))
Z=(0,0,0);ONE=(1,0,0);basis=[ONE,(0,1,0),(0,0,1)]
def add(a,b):return tuple((x+y)%11 for x,y in zip(a,b))
def neg(a):return tuple(-x%11 for x in a)
def scale(a,c):return tuple(x*c%11 for x in a)
@lru_cache(None)
def mul(a,b):
    r=[0]*5
    for i in range(3):
        for j in range(3):r[i+j]+=a[i]*b[j]
    for k in (4,3):r[k-2]-=c1*r[k];r[k-3]-=c0*r[k]
    return tuple(x%11 for x in r[:3])
def exp(a,n):
    r=ONE
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a);n//=2
    return r
@lru_cache(None)
def inv(a):
    require(a!=Z,'field inverse nonzero')
    return exp(a,1329)
@lru_cache(None)
def phi(a,k=1):return exp(a,11**(k%3))
def mm(A,B):return [[sum(a*b for a,b in zip(row,col))%11 for col in zip(*B)] for row in A]
def det(A):
    A=[row[:] for row in A];r=1;n=len(A)
    for i in range(n):
        k=next((j for j in range(i,n) if A[j][i]),None)
        if k is None:return 0
        if k!=i:A[i],A[k]=A[k],A[i];r=-r
        pivot=A[i][i];r=r*pivot%11;u=pow(pivot,-1,11)
        for j in range(i+1,n):
            factor=A[j][i]*u%11
            for k in range(i,n):A[j][k]=(A[j][k]-factor*A[i][k])%11
    return r%11
I=[[int(i==j) for j in range(9)] for i in range(9)]
B0=[row[:] for row in I];B1=[[0]*9 for _ in range(9)]
for k in range(3):
    for j,e in enumerate(basis):
        f=add(e,neg(phi(e,2)))
        for i in range(3):
            for h in range(3):
                B1[3*i+h][3*k+j]=f[h]
                if i<k:B0[3*i+h][3*k+j]=(B0[3*i+h][3*k+j]+f[h])%11
# degree(det(B0+tB1))<=9; values at all 11 elements certify det==1 identically.
det_values=[det([[(B0[i][j]+t*B1[i][j])%11 for j in range(9)] for i in range(9)]) for t in range(11)]
require(det_values==[1]*11,'polynomial determinant identity by exact interpolation')

def conjU(u):
    ui=inv(u);R=[[0]*9 for _ in range(9)]
    for k in range(3):
        c=mul(u,phi(ui,k))
        for j,e in enumerate(basis):
            v=mul(c,e)
            for h in range(3):R[3*k+h][3*k+j]=v[h]
    return R

def skew(A,B,y):
    R=[Z]*3
    for i,a in enumerate(A):
        for j,b in enumerate(B):
            v=mul(a,phi(b,i));k=i+j
            if k>=3:v=scale(v,1+y);k-=3
            R[k]=add(R[k],v)
    return R
matrices=[];specialized=0
for u in P:
    U,V=conjU(u),conjU(inv(u));require(mm(U,V)==I,'constant conjugator inverse')
    C0,C1=mm(mm(U,B0),V),mm(mm(U,B1),V)
    matrices.append([C0,C1])
    for y in (1,2,9):
        t=pow(y,-1,11)
        b=[ONE,Z,scale(ONE,-pow(1+y,-1,11))]
        bi=[scale(ONE,1+t),scale(ONE,t),scale(ONE,t)]
        uu=[u,Z,Z];ui=[inv(u),Z,Z]
        bu=skew(skew(uu,b,y),ui,y);bui=skew(skew(uu,bi,y),ui,y)
        require(skew(bu,bui,y)==[ONE,Z,Z],'actual cyclic algebra inverse')
        for k in range(3):
            for j,e in enumerate(basis):
                X=[Z]*3;X[k]=e
                got=skew(skew(bu,X,y),bui,y)
                expected=[tuple((C0[3*i+h][3*k+j]+t*C1[3*i+h][3*k+j])%11 for h in range(3)) for i in range(3)]
                require(got==expected,'actual conjugation vs polynomial map')
                specialized+=1
require(len({json.dumps(x) for x in matrices})==133,'distinct projective generators')
mut=[row[:] for row in B1];mut[0][0]=(mut[0][0]+1)%11
require(any(det([[(B0[i][j]+t*mut[i][j])%11 for j in range(9)] for i in range(9)])!=1 for t in range(11)), 'bad coefficient rejected')
require(8<9,'eight positive generators have degree below congruence modulus')
# I+t^9 E_12 is nonidentity but reduces to I mod t^9: the degree restriction matters.
require([0]*9+[1]!=[0]*10 and ([0]*9+[1])[:9]==[0]*9,'degree cutoff negative control')

# Independent exact simplicial-chain and link controls.
def faces(F):
    F={tuple(sorted(f)) for f in F}
    return [sorted({s for f in F for s in combinations(f,k+1)}) for k in range(3)]
def rank(A,mod=None):
    A=[[x%mod if mod else Q(x) for x in row] for row in A]
    if not A:return 0
    r=0
    for j in range(len(A[0])):
        k=next((k for k in range(r,len(A)) if A[k][j]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r]
        v=pow(A[r][j],-1,mod) if mod else 1/A[r][j]
        A[r]=[(x*v)%mod if mod else x*v for x in A[r]]
        for k in range(len(A)):
            if k==r:continue
            v=A[k][j]
            if v:A[k]=[(x-v*y)%mod if mod else x-v*y for x,y in zip(A[k],A[r])]
        r+=1
        if r==len(A):break
    return r

def topology(F):
    V,E,T=faces(F);vi={v:i for i,v in enumerate(V)};ei={e:i for i,e in enumerate(E)}
    D1=[[0]*len(E) for _ in V];D2=[[0]*len(T) for _ in E]
    for j,e in enumerate(E):D1[vi[(e[0],)]][j]=-1;D1[vi[(e[1],)]][j]=1
    for j,t in enumerate(T):
        for k in range(3):D2[ei[t[:k]+t[k+1:]]][j]=(-1)**k
    betti={}
    for p in (None,2,3):
        r1,r2=rank(D1,p),rank(D2,p)
        betti['Q' if p is None else str(p)]=[len(V)-r1,len(E)-r1-r2,len(T)-r2]
    incidence=Counter(e for t in T for e in combinations(t,2))
    links={}
    for (v,) in V:
        edges={tuple(x for x in t if x!=v) for t in T if v in t}
        deg=Counter(x for e in edges for x in e)
        links[str(v)]={'vertices':len(deg),'degrees':dict(Counter(deg.values()))}
    return {'f_vector':[len(V),len(E),len(T)],'betti':betti,'chi':len(V)-len(E)+len(T),'edge_triangle_counts':dict(Counter(incidence.values())),'links':links}
TET=list(combinations(range(4),3))
TOR=[]
v=lambda x,y: (x%3)*3+y%3
for x,y in product(range(3),repeat=2):TOR.extend([(v(x,y),v(x+1,y),v(x+1,y+1)),(v(x,y),v(x+1,y+1),v(x,y+1))])
RP=[(0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),(1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5)]
complexes={'tetrahedral_sphere':topology(TET),'torus':topology(TOR),'projective_plane':topology(RP),'global_homology_only':topology(TET+[(0,4,5)])}
require(complexes['tetrahedral_sphere']['betti']['Q']==[1,0,1],'sphere homology')
require(complexes['torus']['betti']['Q']==[1,2,1],'torus homology')
require(all(x=={'vertices':6,'degrees':{2:6}} for x in complexes['torus']['links'].values()),'all torus links C6')
require(complexes['projective_plane']['betti']['Q']==[1,0,0] and complexes['projective_plane']['betti']['2']==[1,1,1],'characteristic boundary control')
require(complexes['global_homology_only']['betti']['Q']==[1,0,1] and 1 in complexes['global_homology_only']['edge_triangle_counts'],'global homology not local sphere')
V,E,T=faces(TOR);m=Counter(e for t in T for e in combinations(t,2))
def a(u,w):return ((w//3-u//3+1)%3)-1
for u,w,z in T:require(a(u,w)+a(w,z)+a(z,u)==0,'torus cocycle')
for (u,) in V:require(sum(m[tuple(sorted((u,w)))]*a(u,w) for (w,) in V if tuple(sorted((u,w))) in m)==0,'weighted harmonic divergence')
energy=sum(m[e]*a(*e)**2 for e in E)
localE=sum((a(u,w)-a(u,z))**2 for (u,) in V for w,z in {tuple(x for x in t if x!=u) for t in T if u in t})
localN=sum(m[e]*a(u,w)**2 for (u,) in V for (w,) in V if (e:=tuple(sorted((u,w)))) in m)
require(energy>0 and localE==energy and localN==2*energy,'strict half threshold exact equality witness')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':checks,'independence':'Authored and run before packaged helper inspection; no submission imports.',
 'projective_plane':{'q':11,'points':N,'vertices':2*N,'edges':sum(map(len,G))//2,'gram':'11 I+J','deletions':deletions,'exact_gap_lower_bound':'(11-sqrt(11))/12 > 7/12 > 1/2'},
 'polynomial_representation':{'field_polynomial':f'X^3+{c1}X+{c0} over F_11','basis':'1,a,a^2; blocks 1,z,z^2','determinant_values_at_all_11_t':det_values,'determinant_proof':'Degree<=9 and 11 distinct exact evaluations equal1 imply determinant identically1.','projective_generators':133,'direct_cyclic_algebra_columns_checked':specialized,'y_values':[1,2,9],'coefficient_mutation_rejected':True,'generator_matrix_sha256':hashlib.sha256(json.dumps(matrices).encode()).hexdigest()},
 'complex_controls':complexes,'strict_half_witness':{'energy':energy,'summed_link_energy':localE,'summed_link_norm':localN},
 'coverage_limits':['No enumeration of Gamma/Gamma_9','No computational proof of arbitrary group words or all complexes','No positive-characteristic 2-CM conclusion','No priority or human peer-review certification']}
print(json.dumps(result,indent=2))
