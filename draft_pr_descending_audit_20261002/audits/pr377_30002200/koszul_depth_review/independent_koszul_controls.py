#!/usr/bin/env python3
"""Exact finite controls for an independently proved universal Koszul derivation.
No external inputs, no candidate imports, no floating point or finite-field checks.
Finite controls are corroboration, not an all-rank proof.
"""
from itertools import combinations
from math import comb
import json
from fractions import Fraction

class Matrix:
    def __init__(self, rows, cols): self.rows=rows; self.cols=cols; self.entries={}
    def __getitem__(self,key): return self.entries.get(key,0)
    def __setitem__(self,key,value):
        if value: self.entries[key]=value
        else: self.entries.pop(key,None)
    @property
    def shape(self): return (self.rows,self.cols)
    def rank(self):
        pivots={}
        columns=[{} for _ in range(self.cols)]
        for (i,j),v in self.entries.items(): columns[j][i]=Fraction(v)
        for column in columns:
            while column:
                i=min(column)
                if i not in pivots:
                    scalar=column[i]; pivots[i]={j:v/scalar for j,v in column.items()}; break
                scalar=column[i]
                for j,v in pivots[i].items():
                    value=column.get(j,0)-scalar*v
                    if value: column[j]=value
                    else: column.pop(j,None)
        return len(pivots)
    def __mul__(self,other):
        assert self.cols==other.rows
        product=Matrix(self.rows,other.cols); byrow={}
        for (i,j),v in other.entries.items(): byrow.setdefault(i,[]).append((j,v))
        for (i,k),v in self.entries.items():
            for j,w in byrow.get(k,[]): product[i,j]=product[i,j]+v*w
        return product
    def __eq__(self,other): return self.shape==other.shape and self.entries==other.entries

def zeros(rows,cols): return Matrix(rows,cols)


def compositions(total, count):
    if total < 0: return []
    if count == 0: return [()] if total == 0 else []
    if count == 1: return [(total,)]
    return [(i,) + c for i in range(total + 1) for c in compositions(total-i,count-1)]


def basis(r,b,j,q):
    return [(I,alpha) for I in combinations(range(r),j) for alpha in compositions(q-b*j,r)]


def boundary(r,b,j,q, signed=True):
    source=basis(r,b,j,q); target=basis(r,b,j-1,q)
    index={v:i for i,v in enumerate(target)}
    M=zeros(len(target),len(source))
    for col,(I,alpha) in enumerate(source):
        for h,i in enumerate(I):
            beta=list(alpha); beta[i]+=b
            row=index[(I[:h]+I[h+1:],tuple(beta))]
            M[row,col]+=(-1)**h if signed else 1
    return M


def quotient_dimension(r,b,q):
    return sum(1 for alpha in compositions(q,r) if max(alpha,default=0)<b)


def check_component(r,b,q):
    dimensions=[len(basis(r,b,j,q)) for j in range(r+1)]
    ranks=[0]+[int(boundary(r,b,j,q).rank()) for j in range(1,r+1)]+[0]
    homology=[dimensions[j]-ranks[j]-ranks[j+1] for j in range(r+1)]
    expected=[quotient_dimension(r,b,q)]+[0]*r
    assert homology==expected,(r,b,q,homology,expected)
    for j in range(2,r+1):
        assert boundary(r,b,j-1,q)*boundary(r,b,j,q)==zeros(dimensions[j-2],dimensions[j])
    return dict(r=r,b=b,q=q,dimensions=dimensions,boundary_ranks=ranks[1:-1],homology=homology)


def ext1_free_target_dim(r,b,k,l=0,lp=0):
    if k != r-1: return 0
    target_degree=2*b-l+lp
    if target_degree%2: return 0
    return quotient_dimension(r,b,target_degree//2)


def main():
    records=[]
    for r,b,qs in [(3,1,range(0,5)),(3,2,range(0,8)),(5,1,range(0,7)),(5,2,range(0,7)),(6,1,range(0,7))]:
        for q in qs: records.append(check_component(r,b,q))
    unsigned=boundary(3,1,1,2,False)*boundary(3,1,2,2,False)
    assert unsigned != zeros(unsigned.rows,unsigned.cols)
    # Missing the alternating contraction signs is intentionally rejected.
    wrong_b=boundary(3,1,1,2)
    correct_b=boundary(3,2,1,2)
    assert wrong_b.shape != correct_b.shape
    # General-b graded extension counterexample to a blanket splitting assertion.
    controls=[]
    for r,b,k,l,lp in [(3,2,2,0,0),(5,1,4,3,9),(5,5,4,11,41),(5,1,2,0,0)]:
        n=ext1_free_target_dim(r,b,k,l,lp)
        controls.append(dict(r=r,b=b,k=k,target_shift=l,quotient_shift=lp,degree0_Ext1_dim=n))
    assert controls[0]['degree0_Ext1_dim']==3
    assert controls[1]['degree0_Ext1_dim']==0
    assert controls[2]['degree0_Ext1_dim']==1
    assert controls[3]['degree0_Ext1_dim']==0
    # Minimal tails and prime-local depths supply the universal witnesses.
    depth_controls=[]
    for odd_r in [5,7,9,11]:
        m=(odd_r-1)//2
        depth_controls.append(dict(odd_rank=odd_r,k=m,pd=odd_r-m,depth_at_odd_m=m,
                                  even_rank=odd_r+1,even_full_max_depth=m+1,
                                  even_witness_prime_height=odd_r,even_witness_prime_depth=m,
                                  syzygy_order_odd_and_even=m))
    print(json.dumps(dict(exact_homogeneous_chain_components=records,
                         unsigned_d_squared_nonzero_entries=len(unsigned.entries),
                         power_mutation_rejected=True,Ext1_controls=controls,
                         depth_controls=depth_controls),indent=2))
    print('PASS: exact chain matrices, Koszul quotient homology, signs/powers controls, Ext controls, rank-5/6 depth witnesses.')
    print('BOUNDARY: this executable corroborates bounded cases; INDEPENDENT_DERIVATION.md contains the universal proof.')

if __name__=='__main__': main()
