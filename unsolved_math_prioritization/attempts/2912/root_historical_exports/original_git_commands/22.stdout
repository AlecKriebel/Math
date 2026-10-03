#!/usr/bin/env python3
"""Finite integral block check for Kirby 4.36 obstruction audit.
Standard library only. This does not test infinite amalgam normal forms,
cohomological theorems, knot realization, or homotopy classification.
"""
import json
from fractions import Fraction

checks = 0
def check(test, label):
    global checks
    assert test, label
    checks += 1

# Affine permutations x -> multiplier*x + shift of F_7.
def mul(g, h):
    u, v = g; w, z = h
    return (u*w % 7, (u*z+v) % 7)
def inv(g):
    u, v = g; w = pow(u, -1, 7)
    return (w, -w*v % 7)
def power(g, n):
    x = (1, 0)
    for _ in range(n): x = mul(x, g)
    return x
A = {(u, v) for u in [1, 2, 4] for v in range(7)}
a, b, one = (2, 0), (1, 1), (1, 0)
check(len(A) == 21, 'order 21')
for g in A:
    check(mul(g, inv(g)) == one == mul(inv(g), g), 'inverse')
    for h in A: check(mul(g,h) in A, 'closure')
check(power(a,3) == power(b,7) == one, 'orders divide 3 and 7')
check(a != one and b != one, 'orders exactly 3 and 7')
check(mul(mul(a,b),inv(a)) == power(b,2), 'semidirect relation')
C = {power(a,i) for i in range(3)}
cosets = [frozenset(mul(power(b,j),c) for c in C) for j in range(7)]
check(len(set(cosets)) == 7 and set.union(*map(set,cosets)) == A, 'seven A/C cosets')
for j, coset in enumerate(cosets):
    check(frozenset(mul(a,x) for x in coset) == cosets[2*j % 7], 'a acts by doubling')
    check(frozenset(mul(b,x) for x in coset) == cosets[(j+1)%7], 'b acts by shift')
# Inversion identifies the right C\\A permutation set with A/C,
# with right multiplication by g corresponding to left multiplication by g^-1.
right = [frozenset(inv(x) for x in coset) for coset in cosets]
for j, coset in enumerate(right):
    for g in [a,b]:
        inverse_images = frozenset(inv(mul(x,g)) for x in coset)
        check(inverse_images == frozenset(mul(inv(g),x) for x in cosets[j]), 'inversion convention')

# Quotient Z^7 / Z*(1,...,1), integral coordinates [v_i-v_6] for i<6.
def reduce(v): return tuple(v[i]-v[6] for i in range(6))
def basis(n,j): return tuple(int(i==j) for i in range(n))
def action_matrix(perm):
    columns = [reduce(basis(7,perm[j])) for j in range(6)]
    return tuple(tuple(columns[j][i] for j in range(6)) for i in range(6))
def matmul(x,y):
    return tuple(tuple(sum(x[i][k]*y[k][j] for k in range(6)) for j in range(6)) for i in range(6))
def matpow(x,n):
    out=I
    for _ in range(n): out=matmul(out,x)
    return out
I=tuple(tuple(int(i==j) for j in range(6)) for i in range(6))
Ma=action_matrix([(2*j)%7 for j in range(7)])
Mb=action_matrix([(j+1)%7 for j in range(7)])
check(reduce((1,)*7)==(0,)*6, 'diagonal killed')
for j in range(6): check(reduce(basis(7,j))==basis(6,j), 'six quotient generators')
check(reduce(basis(7,6))==(-1,)*6, 'last generator relation')
check(matpow(Ma,3)==I and matpow(Mb,7)==I, 'matrix orders')
check(matmul(matmul(Ma,Mb),matpow(Ma,2))==matpow(Mb,2), 'matrix conjugation relation')
# First six standard basis vectors plus the diagonal form a unimodular basis.
U=[[int(i==j) if j<6 else 1 for j in range(7)] for i in range(7)]
def determinant(m):
    m=[list(map(Fraction,row)) for row in m]; det=Fraction(1)
    for j in range(len(m)):
        k=next((k for k in range(j,len(m)) if m[k][j]),None)
        if k is None:return Fraction(0)
        if k!=j:m[k],m[j]=m[j],m[k];det=-det
        pivot=m[j][j];det*=pivot
        for k in range(j+1,len(m)):
            ratio=m[k][j]/pivot
            for l in range(j,len(m)):m[k][l]-=ratio*m[j][l]
    return det
check(determinant(U)==1, 'unimodular diagonal basis')
check(determinant(Ma)==1 and determinant(Mb)==1, 'unimodular actions')
print(json.dumps({'status':'PASS','exact_assertions':checks,'finite_group_order':len(A),
    'coset_count':len(cosets),'quotient_rank':6,'quotient_torsion':[],
    'matrix_a':Ma,'matrix_b':Mb,
    'limits':['Finite block only','No knot realization','No pair of exteriors',
              'No completeness theorem or counterexample']},indent=2))
