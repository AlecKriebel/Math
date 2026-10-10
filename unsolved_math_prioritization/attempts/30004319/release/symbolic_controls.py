#!/usr/bin/env python3
"""Exact free nonassociative polynomial controls over Z[n], standard library only."""
import itertools
import json

# A polynomial maps (power of central scalar n, binary multiplication tree) to Z.
# The symbol '1' is the multiplicative unit. No associativity is imposed.
def atom(s): return {(0,s):1}
def plus(*ps):
    out={}
    for p in ps:
        for k,v in p.items(): out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}
def neg(p): return {k:-v for k,v in p.items()}
def times(p,q):
    out={}
    for (i,a),u in p.items():
        for (j,b),v in q.items():
            t=b if a=='1' else a if b=='1' else (a,b)
            key=(i+j,t);out[key]=out.get(key,0)+u*v
    return {k:v for k,v in out.items() if v}
def assoc(a,b,c): return plus(times(times(a,b),c),neg(times(a,times(b,c))))
def matrix_mul(A,B):
    out={}
    for (i,j),a in A.items():
        for (k,l),b in B.items():
            if j==k: out[i,l]=plus(out.get((i,l),{}),times(a,b))
    return {k:v for k,v in out.items() if v}
def matrix_add(A,B,sign=1):
    out=dict(A)
    for k,v in B.items():out[k]=plus(out.get(k,{}),v if sign==1 else neg(v))
    return {k:v for k,v in out.items() if v}
def bracket(A,B):return matrix_add(matrix_mul(A,B),matrix_mul(B,A),-1)
def roots(n):return [tuple(int(i==a)-int(i==b) for i in range(n+1))
                    for a in range(n+1) for b in range(a+1,n+1)]
def vadd(a,b):return tuple(x+y for x,y in zip(a,b))
def chains(n):
    positive=roots(n);S=set(positive)
    return [(a,b,c) for a,b,c in itertools.product(positive,repeat=3)
            if vadd(a,b) in S and vadd(b,c) in S and vadd(vadd(a,b),c) in S]
def main():
    a,b,c,y=map(atom,('a','b','c','y'))
    shifted=plus(a,{(1,'1'):1})
    assert assoc(shifted,shifted,y)==assoc(a,a,y)
    assert assoc(y,shifted,shifted)==assoc(y,a,a)
    A={(0,1):a};B={(1,2):b};C={(2,0):c}
    J=matrix_add(matrix_add(bracket(bracket(A,B),C),bracket(bracket(B,C),A)),
                 bracket(bracket(C,A),B))
    assert J=={(0,0):assoc(a,b,c),(1,1):assoc(b,c,a),(2,2):assoc(c,a,b)}
    assert not chains(2)
    assert chains(3)
    print(json.dumps({'scalar_shift_left_defect_invariant':True,
                      'scalar_shift_right_defect_invariant':True,
                      'matrix_jacobi_equals_cyclic_associator_diagonal':True,
                      'A2_positive_nested_chain_count':len(chains(2)),
                      'A3_positive_nested_chain_count':len(chains(3)),
                      'limits':['free unital nonassociative polynomial identities only',
                                'no algebra-to-group existence conclusion']},
                     indent=2,sort_keys=True))
if __name__=='__main__':main()
