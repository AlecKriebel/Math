#!/usr/bin/env python3
"""Independent Schur S(2,5) orbit algebra on tensor space, exact arithmetic mod 3."""
import itertools,json,sys,hashlib,math
from pathlib import Path
import numpy as np
P=3
def need(condition,message):
    if not condition: raise RuntimeError(message)
def rank(vectors):
    pivots={}
    for vector in vectors:
        v=np.array(vector,dtype=np.int64).reshape(-1)%P
        for i,b in sorted(pivots.items()):
            if v[i]:v=(v-v[i]*b)%P
        nz=np.flatnonzero(v)
        if len(nz):
            i=int(nz[0]);v=v*pow(int(v[i]),-1,P)%P;pivots[i]=v
    return len(pivots)
def nullity(matrix,nvars):
    return nvars-rank(matrix)
def homdim(source,target):
    n=source[0].shape[0];d=target[0].shape[0];eq=[]
    for s,t in zip(source,target):
        for a in range(d):
            for b in range(n):
                row=np.zeros(d*n,dtype=np.int64)
                for j in range(n):row[a*n+j]+=s[j,b]
                for j in range(d):row[j*n+b]-=t[a,j]
                eq.append(row%P)
    return nullity(eq,d*n)
words=list(itertools.product((0,1),repeat=5));index={w:i for i,w in enumerate(words)}
keys=sorted({tuple(sum(1 for a,b in zip(u,v) if (a,b)==pair) for pair in ((0,0),(0,1),(1,0),(1,1))) for u in words for v in words})
basis=[];representatives=[]
for key in keys:
    a=np.zeros((32,32),dtype=np.int64);reps=[]
    for i,u in enumerate(words):
        for j,v in enumerate(words):
            k=tuple(sum(1 for x,y in zip(u,v) if (x,y)==pair) for pair in ((0,0),(0,1),(1,0),(1,1)))
            if k==key:a[i,j]=1;reps.append((i,j))
    basis.append(a);representatives.append(reps[0])
need(len(basis)==56 and rank(basis)==56,'Schur orbit basis dimension')
I=np.eye(32,dtype=np.int64);E=np.zeros_like(I);F=np.zeros_like(I)
for j,w in enumerate(words):
    for k,t in enumerate(w):
        v=list(w);v[k]=1-t
        if t:E[index[tuple(v)],j]+=1
        else:F[index[tuple(v)],j]+=1
H=np.diag([5-2*sum(w) for w in words])%P
C=(E@F+F@E+2*H@H)%P
need(all(np.array_equal((C@a)%P,(a@C)%P) for a in basis),'Casimir central in full Schur algebra')
z=np.linalg.matrix_power(C,3)%P
need(np.array_equal(z@z%P,z),'Casimir block idempotent')
other=(I-z)%P
weights={}
for a in range(6):
    e=np.diag([int(5-sum(w)==a) for w in words])
    d0=rank([b@e%P for b in basis]);d1=rank([b@e@z%P for b in basis]);d2=rank([b@e@other%P for b in basis])
    need(d0==(a+1)*(6-a) and d0==d1+d2,'weight projective dimensions')
    weights[str((a,5-a))]={'full_ideal_dimension':d0,'semisimple_L5_ideal_dimension':d1,'other_block_ideal_dimension':d2}
e32=np.diag([int(5-sum(w)==3) for w in words])@other%P
e41=np.diag([int(5-sum(w)==4) for w in words])@other%P
N=e32@C@e32%P
need(rank([e32@b@e32%P for b in basis])==2,'P32 corner dimension two')
need(rank([e32,N])==2 and not np.any(N@N%P),'P32 corner dual numbers and primitive idempotent')
need(rank([e41@b@e41%P for b in basis])==1,'P41 corner scalar and primitive idempotent')
# The quotient wedge^2(E) tensor Sym^3(E) of the appropriate tensor subspace.
module=[]
for b in basis:
    a=np.zeros((4,4),dtype=np.int64)
    for j in range(4):
        rest=(0,)*(3-j)+(1,)*j
        v=(b[:,index[(0,1)+rest]]-b[:,index[(1,0)+rest]])%P
        for k,w in enumerate(words):
            if w[:2]==(0,1):a[sum(w[2:]),j]+=v[k]
    module.append(a%P)
# Establish the complete algebra action, rather than finite GL_2(F_3) sampling.
stack=np.stack(basis);Mstack=np.stack(module);product_checks=0
for a,ma in zip(basis,module):
    for b,mb in zip(basis,module):
        product=a@b%P
        coeff=np.array([product[i,j] for i,j in representatives])
        need(np.array_equal(np.tensordot(coeff,stack,axes=1)%P,product),'orbit multiplication closure')
        need(np.array_equal(np.tensordot(coeff,Mstack,axes=1)%P,ma@mb%P),'wedge symmetric quotient action multiplicative')
        product_checks+=1
W=[a[np.ix_([0,3],[0,3])] for a in module];Q=[a[np.ix_([1,2],[1,2])] for a in module]
need(all(not np.any(a[np.ix_([1,2],[0,3])]) for a in module),'cube submodule invariant')
need(rank(W)==rank(Q)==4,'two absolutely simple two-dimensional factors')
need(homdim(module,W)==0 and homdim(module,Q)==1,'head exactly quotient simple L32')
need(homdim(module,module)==1,'module endomorphism ring scalar')
# Compute dimensions independently of reciprocity from actual left ideals.
p32=rank([b@e32%P for b in basis]);p41=rank([b@e41%P for b in basis])
need(p32==6 and p41==4,'actual primitive projective ideal dimensions')
# Weight-directed divided-power graph checks for the full odd-prime family.
families=[]
for p in (3,5,7,11,13,17,19,23,29,31):
    r=2*p-1;m=2*p-3;J=set(range(p-2))|set(range(p,m+1))
    support={j for j in range(m+1) if math.comb(m,j)%p}
    need(support==J,'Lucas support in family')
    need(all(math.comb(r,j)%p for j in range(r+1)),'simple upper costandard support')
    # Divide-power arrows v_i -> v_j under both root subgroups.
    edges={i:{j for j in range(m+1) if ((j<=i and math.comb(i,j)%p) or (j>=i and math.comb(m-i,j-i)%p))} for i in range(m+1)}
    def closure(start,allowed):
        reached={start};todo=[start]
        while todo:
            i=todo.pop()
            for j in edges[i]&allowed:
                if j not in reached:reached.add(j);todo.append(j)
        return reached
    need(all(edges[i]<=J for i in J),'W closed under every formal root coefficient')
    missing=set(range(m+1))-J
    need(all(closure(i,J)==J for i in J),'W cyclic from every weight')
    need(all(closure(i,missing)==missing for i in missing),'quotient cyclic from every weight')
    need(0 in edges[p-2] and 0 in J,'canonical weight complement fails')
    families.append({'p':p,'r':r,'lambda':[r-1,1],'I2_dimension':m+1,'socle_dimension':len(J),'head_dimension':len(missing),'all_weight_checks':True})
result={'result':'PASS','field':'F_3 exact tensor orbit computations; ranks valid after algebraic closure','Schur_algebra':'S(2,5)','tensor_dimension':32,'orbit_basis_dimension':56,'full_multiplication_and_module_action_checks':product_checks,'Casimir_idempotent_power':3,'weights':weights,'projective_P32_dimension':p32,'projective_P41_dimension':p41,'primitive_P32_corner':'k[epsilon]/epsilon^2; nonzero N=eCe, N^2=0','primitive_P41_corner':'k','detSym3_dimension':4,'detSym3_composition_factor_dimensions':[2,2],'detSym3_Hom_to_socle_dimension':homdim(module,W),'detSym3_Hom_to_head_dimension':homdim(module,Q),'detSym3_End_dimension':homdim(module,module),'conclusion':'The four-dimensional I_2(4,1) has head L_2(3,2), whose primitive projective cover has dimension six, so I_2(4,1) is not projective.','odd_prime_divided_power_family_checks':families,'limitations':['Finite tensor calculation validates only p=3 rank2; universal odd-p and all-rank statements require INDEPENDENT_DERIVATION.md','Identification of detSym3 with polynomial injective uses highest-weight reciprocity; arbitrary projectivity does not follow from finite GL_2(F_3) matrices'],'optimization_safe':True}
print(json.dumps(result,indent=2))
