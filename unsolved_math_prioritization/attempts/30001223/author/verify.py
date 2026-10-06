#!/usr/bin/env python3
"""Exact coefficient-matrix checks over F_3; no external packages or source files.
These checks support, and do not replace, the all-rank mathematical argument.
"""
import json
from math import comb
from pathlib import Path

P = 3

def require(value, message):
    if not value:
        raise ValueError(message)

def rank(rows):
    a = [[v % P for v in row] for row in rows]
    if not a:
        return 0
    h = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(h, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[h], a[pivot] = a[pivot], a[h]
        u = pow(a[h][j], -1, P)
        a[h] = [u*x % P for x in a[h]]
        for i in range(len(a)):
            if i != h and a[i][j]:
                u = a[i][j]
                a[i] = [(x-u*y) % P for x,y in zip(a[i], a[h])]
        h += 1
        if h == len(a):
            break
    return h

def coefficient_matrices(m, determinant_power):
    """g x=a x+c y, g y=b x+d y, basis x^(m-i)y^i.
    Extract every degree m+2k polynomial coefficient of det(g)^k Sym^m(g).
    The coefficient action, unlike evaluation on GL_2(F_3), captures GL_2(k).
    """
    n = m+1
    out = {}
    for i in range(n):
        for j in range(m-i+1):
            for h in range(i+1):
                row = j+h
                base = (m-i-j, i-h, j, h)  # a,b,c,d
                value = comb(m-i,j)*comb(i,h)
                for t in range(determinant_power+1):
                    term = (determinant_power-t,t,t,determinant_power-t)
                    exponents = tuple(a+b for a,b in zip(base,term))
                    v = value*comb(determinant_power,t)*((-1)**t)
                    mat = out.setdefault(exponents, [[0]*n for _ in range(n)])
                    mat[row][i] = (mat[row][i]+v) % P
    return [out[k] for k in sorted(out)]

def flat(matrix):
    return [v for row in matrix for v in row]

def span_rank(matrices):
    return rank([flat(a) for a in matrices])

def commutant_dimension(matrices):
    n = len(matrices[0])
    rows = []
    for a in matrices:
        for i in range(n):
            for j in range(n):
                row = [0]*(n*n)
                for k in range(n):
                    row[k*n+j] += a[i][k]
                    row[i*n+k] -= a[k][j]
                rows.append(row)
    return n*n-rank(rows)

def splitting_ranks(matrices):
    # Socle coordinates [0,3], quotient coordinates [1,2].
    w, q = [0,3], [1,2]
    equations, augmented = [], []
    for a in matrices:
        for i in range(4):
            for j in range(2):
                row = [0]*4
                for u in range(2):
                    row[u*2+j] += a[i][w[u]]
                if i in w:
                    u = w.index(i)
                    for v in range(2):
                        row[u*2+v] -= a[q[v]][q[j]]
                fixed = a[i][q[j]]-(a[q[q.index(i)]][q[j]] if i in q else 0)
                equations.append(row)
                augmented.append(row+[-fixed])
    return rank(equations), rank(augmented)

def main():
    data = json.loads(Path(__file__).with_name('case.json').read_text())
    require(data == {'characteristic':3,'partition':[4,1],'degree':5,'minimal_rank':2}, 'case metadata changed')
    sym5 = coefficient_matrices(5,0)
    nabla41 = coefficient_matrices(3,1)
    nabla32 = coefficient_matrices(1,2)
    require(span_rank(sym5)==36, 'Sym^5 coefficient span is not full M_6')
    require(span_rank(nabla32)==4, 'det^2 E coefficient span is not full M_2')
    require(all(a[i][j]==0 for a in nabla41 for i in [1,2] for j in [0,3]), 'cube socle is not invariant')
    socle = [[[a[i][j] for j in [0,3]] for i in [0,3]] for a in nabla41]
    quotient = [[[a[i][j] for j in [1,2]] for i in [1,2]] for a in nabla41]
    require(span_rank(socle)==span_rank(quotient)==4, 'socle or quotient not absolutely simple')
    r,ra = splitting_ranks(nabla41)
    require(ra>r, 'extension unexpectedly splits')
    require(commutant_dimension(nabla41)==1, 'endomorphism ring not scalar')
    # Augmentation basis e_i-e_4, i=0..3, for S_5; adjacent transpositions.
    adjacent = []
    for s in range(4):
        perm = list(range(5));perm[s],perm[s+1]=perm[s+1],perm[s]
        a = [[0]*4 for _ in range(4)]
        for j in range(4):
            v=[0]*5;v[perm[j]]+=1;v[perm[4]]-=1
            for i in range(4):a[i][j]=v[i]%P
        adjacent.append(a)
    # Check orbit span from each nonzero F_3 vector as finite supporting test.
    import itertools
    tested=0
    for tup in itertools.product(range(3), repeat=4):
        if not any(tup):continue
        basis=[list(tup)];old=0
        while rank(basis)>old:
            old=rank(basis)
            for a in adjacent:
                images=[[sum(a[i][j]*v[j] for j in range(4))%3 for i in range(4)] for v in basis[:]]
                for v in images:
                    if rank(basis+[v])>rank(basis):basis.append(v)
        require(rank(basis)==4,'augmentation vector generates a proper submodule')
        tested+=1
    result={
      'case':data,
      'status':'PASS',
      'sym5_coefficient_span_rank':span_rank(sym5),
      'nabla41_coefficient_span_rank':span_rank(nabla41),
      'nabla41_endomorphism_dimension':commutant_dimension(nabla41),
      'extension_equation_rank':r,'extension_augmented_rank':ra,
      'augmentation_nonzero_vectors_checked':tested,
      'decomposition_rows':[[1,0,0],[0,1,1],[0,0,1]],
      'labels':[[5],[4,1],[3,2]],
      'injective_and_projective_dimensions':[6,4,6],
      'scope':'Exact finite checks support proof.md; all fields and all n use its mathematical proof.'}
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
