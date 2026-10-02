#!/usr/bin/env python3
"""Finite exact controls; no claim about direct finiteness of infinite rings."""
import itertools,json
counts={}
def ck(name,x):
    assert x,name
    counts[name]=counts.get(name,0)+1
S=list(itertools.permutations(range(3))); ident=S.index((0,1,2))
def compose(a,b):return tuple(a[b[i]] for i in range(3))
table=[[S.index(compose(a,b)) for b in S] for a in S]
def conv(a,b):
    z=0
    for i in range(6):
        if a>>i&1:
            for j in range(6):
                if b>>j&1:z^=1<<table[i][j]
    return z
one=1<<ident
for a in range(64):
    for b in range(64):
        ab=conv(a,b)
        if ab==one:ck('scalar_direct_finite',conv(b,a)==one)
        for g in range(6):ck('left_action',conv(1<<g,ab)==conv(conv(1<<g,a),b))
def mul(a,b):return ((a&1)*(b&1)^((a>>1)*(b>>1))) | (((a&1)*(b>>1)^((a>>1)*(b&1)))<<1)
# C2 ring: 1=1, g=2, 1+g=3; XOR is addition.
ms=list(itertools.product(range(4),repeat=4)); I=(1,0,0,1)
def mm(A,B):return tuple(mul(A[2*i],B[j])^mul(A[2*i+1],B[2+j]) for i in range(2) for j in range(2))
def row(v,A):return tuple(mul(v[0],A[j])^mul(v[1],A[2+j]) for j in range(2))
units=0
for X in ms:
    for Y in ms:
        if mm(X,Y)!=I:continue
        units+=1;ck('matrix_direct_finite',mm(Y,X)==I)
        defect=tuple(a^b for a,b in zip(I,mm(Y,X)))
        ck('kernel_orientation',mm(defect,Y)==(0,0,0,0))
        for v in itertools.product(range(4),repeat=2):ck('right_inverse_orientation',row(row(v,X),Y)==v)
T=(1,2,0,1)
ck('triangular_inverse',mm(T,T)==I)
for v in itertools.product(range(4),repeat=2):
    ck('matrix_equivariance',row(tuple(mul(2,a) for a in v),T)==tuple(mul(2,a) for a in row(v,T)))
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'categories':counts,'scalar_ring_size':64,'matrix_ring_size':256,'matrix_pairs_examined':65536,'right_inverse_pairs':units,'scope':'Finite rings only; conditional infinite-ring obstruction remains hypothetical.'},indent=2,sort_keys=True))
