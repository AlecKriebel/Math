#!/usr/bin/env python3
"""Independent exact moment-pairing matrices for local apolar quotients."""
from itertools import product
from math import factorial
from pathlib import Path
import random,hashlib,json
from sympy import Matrix
from sympy.polys.matrices import DomainMatrix
C={};records=[]
def ck(b,k):
    assert b,k
    C[k]=C.get(k,0)+1

def mons(r,j):return [a for a in product(range(j+1),repeat=r) if sum(a)<=j]
def addexp(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b,j):
    out={}
    for x,c in a.items():
        for y,d in b.items():
            z=addexp(x,y)
            if sum(z)<=j:out[z]=out.get(z,0)+c*d
    return {m:c for m,c in out.items() if c}
def rank(rows):
    if not rows:return 0
    return DomainMatrix.from_Matrix(Matrix(rows)).to_field().rank()
def ev(F,c):return sum(v*__import__('functools').reduce(lambda a,b:a*b,(t**k for t,k in zip(c,m)),1) for m,v in F.items())
def hessian(F,c,r):
    out=[]
    for i in range(r):
        row=[]
        for h in range(r):
            G={}
            for m,a in F.items():
                v=list(m);coef=a*v[i];v[i]-=1
                if coef and v[h]>0:
                    coef*=v[h];v[h]-=1;G[tuple(v)]=coef
            row.append(ev(G,c))
        out.append(row)
    return out

def test(F,j,c,ell,label):
    r=len(c);M=mons(r,j);zero=(0,)*r
    moments={a:v*__import__('functools').reduce(lambda b,x:b*factorial(x),a,1) for a,v in F.items()}
    def moment(a):return moments.get(a,0)
    H=[[moment(addexp(a,b)) for b in M] for a in M]
    dims=[rank([H[i] for i,a in enumerate(M) if sum(a)>=q]) for q in range(j+2)]
    hilb=[dims[q]-dims[q+1] for q in range(j+1)]
    top={a:v for a,v in F.items() if sum(a)==j}
    ck(ev(top,c)!=0,'nonzero_top_evaluation')
    s=rank([[moment(addexp(a,b)) for b in M if sum(b)==j-1] for a in M if sum(a)==1])
    ck(hilb[-2]==s,'last_Hilbert_entry')
    power={zero:1};ranks=[]
    for q in range(j+2):
        K=[[sum(v*moment(addexp(addexp(a,b),d)) for d,v in power.items()) for b in M] for a in M]
        ranks.append(rank(K));power=mul(power,ell,j)
    hr=rank(hessian(top,c,r))
    ck(ranks[j-2]==2+hr,'nonlinear_operator_Hessian_identity')
    ck(ranks[j:]==[1,0],'top_nilpotent_ranks')
    ck(all(ranks[q]>=ranks[q+1] for q in range(j+1)),'rank_monotonicity')
    if j==3:
        ck(hilb==[1,hilb[1],s,1] and hilb[1]>=s,'cubic_Hilbert_shape')
        ck(ranks[2:]==[2,1,0],'cubic_high_powers')
        P=[sum(h>=t for h in hilb) for t in range(1,max(hilb)+1)]
        required=[sum(max(a-q,0) for a in P) for q in range(j+2)]
        ck((ranks==required)==(hr==s),'cubic_SL_equivalence')
    records.append({'label':label,'socle':j,'Hilbert':hilb,'ranks':ranks,'top_Hessian_rank':hr,'essential_variables':s})

rng=random.Random(30004526)
for j in range(3,8):
    r=3;c=(1,2,3);M=mons(r,j)
    for case in range(2):
        F={a:rng.randrange(-2,3) for a in M if rng.randrange(5)==0}
        F[(j,0,0)]=5;F[(0,j,0)]=3;F[(0,0,j)]=2
        top={a:v for a,v in F.items() if sum(a)==j}
        if ev(top,c)==0:F[(j,0,0)]+=1
        ell={(1,0,0):1,(0,1,0):2,(0,0,1):3,(2,0,0):2,(0,1,1):-1,(1,1,1):2,(0,0,3):1}
        if j>=4:ell[(1,0,3)]=-1
        test(F,j,c,ell,'random_'+str(j)+'_'+str(case))
# Cubic with three essential variables and a genuinely lower-only fourth variable.
for j in (3,4):
    r=4;c=(1,1,2,1)
    F={(j,0,0,0):1,(0,j,0,0):2,(0,0,j,0):1,(1,0,0,1):3,(0,0,0,2):1}
    ell={(1,0,0,0):1,(0,1,0,0):1,(0,0,1,0):2,(0,0,0,1):1,(1,0,0,1):2,(0,0,0,3):1}
    test(F,j,c,ell,'extra_variable_'+str(j))
# A quartic Perazzo top with lower terms in a sixth variable.
r=6;j=4;c=(1,1,1,1,1,1)
G={(1,0,0,3,0,0):1,(0,1,0,2,1,0):1,(0,0,1,0,3,0):1}
F={**G,(2,0,0,0,0,1):2,(0,1,0,0,0,2):1,(0,0,0,0,0,2):3}
ell={tuple(int(i==h) for i in range(r)):1 for h in range(r)}
ell[(0,0,0,1,1,0)]=2;ell[(0,0,0,0,0,3)]=-1
# Avoid an unnecessarily large moment matrix by use of the independent graded Hessian and degree-pairing blocks.
H=hessian(G,c,r)
ck(rank(H)==4,'Perazzo_Hessian_rank_four')
for i in range(3):
    for h in range(3):ck(H[i][h]==0,'Perazzo_zero_block')
for a in range(3):
    ds=[m for m in mons(r,j) if sum(m)==a]
    es=[m for m in mons(r,j) if sum(m)==j-a]
    moments={m:v*__import__('functools').reduce(lambda b,x:b*factorial(x),m,1) for m,v in G.items()}
    rk=rank([[moments.get(addexp(x,y),0) for y in es] for x in ds])
    ck(rk==[1,5,6][a],'Perazzo_catalecticant_dimensions')
# Full combinatorial identity, without pretending all tested sequences are realizable.
for j in range(3,9):
    for a in product(range(1,4),repeat=j-1):
        H=(1,)+a+(1,);P=[sum(x>=t for x in H) for t in range(1,4)]
        ck(sum(max(x-j+2,0) for x in P)==min(a)+2,'partition_rank_identity')
base=Path(__file__).resolve().parent
sha=hashlib.sha256((base/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest()
ck(sha=='1321a6684a831a00c066eee06882dee334400ddf9ed3d350c7e19c4cf0633ac9','frozen_artifact')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'categories':C,'moment_matrix_cases':records,
 'artifact_sha256':sha,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Exact rational moment-pairing and partition controls; all-degree and all-deformation conclusions require the written proof.'},indent=2,sort_keys=True))
