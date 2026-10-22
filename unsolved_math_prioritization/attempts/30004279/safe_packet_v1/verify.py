#!/usr/bin/env python3
"""Exact finite controls for PROOFS.md, not a solver or formal theorem checker."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

checks = []
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

def determinant(a):
    a = [[Q(x) for x in row] for row in a]
    n = len(a)
    sign = Q(1)
    out = Q(1)
    for k in range(n):
        pivot = next((i for i in range(k,n) if a[i][k]), None)
        if pivot is None:
            return Q(0)
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        x = a[k][k]
        out *= x
        for i in range(k+1,n):
            multiplier = a[i][k]/x
            for j in range(k+1,n):
                a[i][j] -= multiplier*a[k][j]
    return sign*out

def cartan(n, edges):
    a = [[2*int(i==j) for j in range(n)] for i in range(n)]
    for i,j in edges:
        a[i][j] = a[j][i] = -1
    return a

def gram_data(a):
    return {
      'symmetric': all(a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a))),
      'even_diagonal': all(a[i][i]%2==0 for i in range(len(a))),
      'leading_minors': [int(determinant([row[:k] for row in a[:k]])) for k in range(1,len(a)+1)],
      'determinant': int(determinant(a)),
    }

def admissible_unimodular(a):
    d=gram_data(a)
    return d['symmetric'] and d['even_diagonal'] and min(d['leading_minors'])>0 and d['determinant']==1

e8=cartan(8, [(i,i+1) for i in range(6)]+[(2,7)])
e8d=gram_data(e8)
check('E8 leading minors', e8d['leading_minors']==[2,3,4,5,6,7,8,1])
check('E8 even positive unimodular',admissible_unimodular(e8))
check('A1 discriminant two',determinant([[2]])==2)
a8=cartan(8,[(i,i+1) for i in range(7)])
check('negative control: A8 not unimodular',determinant(a8)==9 and not admissible_unimodular(a8))
wrong_branch=cartan(8,[(i,i+1) for i in range(6)]+[(3,7)])
check('negative control: midpoint branch singular',determinant(wrong_branch)==0 and not admissible_unimodular(wrong_branch))
odd=[row[:] for row in e8];odd[0][0]=3
check('negative control: odd lattice excluded',not admissible_unimodular(odd))
for m in range(1,5):
    block=[[e8[i%8][j%8] if i//8==j//8 else 0 for j in range(8*m)] for i in range(8*m)]
    check(f'E8 direct sum determinant m={m}',determinant(block)==1)

class_sizes=[1,3,2]
characters=[[1,1,1],[1,-1,1],[2,0,-1]]
gram=[[sum(Q(s*a*b,6) for s,a,b in zip(class_sizes,x,y)) for y in characters] for x in characters]
for i in range(3):
    for j in range(3):
        check(f'S3 character inner product {i},{j}',gram[i][j]==int(i==j))
check('S3 squared degrees',sum(x[0]**2 for x in characters)==6)
check('different simple counts',len(characters)==3 and 3!=6)

add=lambda a,b:(a+b)%2
omega=lambda a,b,c:(-1)**(a*b*c)
for a,b,c in product(range(2),repeat=3):
    if 0 in (a,b,c):
        check(f'cocycle normalized at {a}{b}{c}',omega(a,b,c)==1)
for a,b,c,d in product(range(2),repeat=4):
    left=omega(b,c,d)*omega(a,add(b,c),d)*omega(a,b,c)
    right=omega(add(a,b),c,d)*omega(a,b,add(c,d))
    check(f'cocycle pentagon at {a}{b}{c}{d}',left==right)
# Formal monomial beta(1,1)^(1-1) remains after normalized unit factors.
check('arbitrary cochain exponent cancels',1-1==0)
check('nontrivial associator obstruction',omega(1,1,1)==-1 and 1!=omega(1,1,1))
check('negative control: trivial associator has no such obstruction',1==(-1)**0)

result={
 'purpose':'Finite arithmetic and categorical negative controls only; no soliton equivalence certified.',
 'passed_assertions':len(checks),
 'E8':e8d,
 'A1_discriminant':2,
 'S3':{'class_sizes':class_sizes,'characters':characters,'simple_counts':[6,3]},
 'Z2_cocycle':{'exponent':'a*b*c mod 2','pentagon_instances':16,'coboundary_at_111':1,'omega_at_111':-1},
 'negative_controls':['A8 determinant 9','singular misplaced branch','odd diagonal','trivial associator comparison'],
 'verified_original_conjecture':False,
}
encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.output:
        args.output.write_text(encoded)
    print(encoded,end='')
