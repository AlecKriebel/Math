"""Exact rational check of mixed.tex 648-665, not of algebraicity of P.
No external packages. Rows/columns use ordinary ordered matrix units.
"""
from fractions import Fraction
import json
from pathlib import Path

J = [[0, 1], [-1, 0]]
labels = [(i, j) for i in range(2) for j in range(2)]
q = [[J[i][k] * J[j][l] for k,l in labels] for i,j in labels]
# (J tensor J)^2 = I, hence q inverse equals q.
assert [[sum(q[i][k]*q[k][j] for k in range(4)) for j in range(4)] for i in range(4)] == [[int(i==j) for j in range(4)] for i in range(4)]
A = []
B = []
for i,j in labels:
    A.append([int(r == j)*J[i][c] for r in range(2) for c in range(2)])
    B.append([int(r == i)*J[j][c] for r in range(2) for c in range(2)])
P = [[sum(q[a][b]*A[a][r]*B[b][s] for a in range(4) for b in range(4)) for s in range(4)] for r in range(4)]

def rank(mat):
    mat = [[Fraction(x) for x in row] for row in mat]
    p = 0
    for c in range(len(mat[0])):
        pivot = next((r for r in range(p,len(mat)) if mat[r][c]),None)
        if pivot is None: continue
        mat[p], mat[pivot] = mat[pivot], mat[p]
        value = mat[p][c]
        mat[p] = [x/value for x in mat[p]]
        for r in range(len(mat)):
            if r != p:
                value = mat[r][c]
                mat[r] = [x-value*y for x,y in zip(mat[r],mat[p])]
        p += 1
        if p == len(mat): break
    return p

# Hom(X,Y) output Y_0 has row-major positions 0,1.
# Hom(Y,X) input Y_0 has row-major positions 0,2.
P_line = [[P[r][s] for s in [0,2]] for r in [0,1]]
assert rank(P) == 4
assert rank(P_line) == 2
out = {'field':'Q', 'quadratic_metric':q, 'full_Hom_pairing_matrix':P,
       'full_Hom_pairing_rank':rank(P), 'torus_line_pairing_matrix':P_line,
       'torus_line_pairing_rank':rank(P_line),
       'verified_scope':'mixed.tex local perfect-pairing linear algebra only; no geometric algebraicity assertion'}
print(json.dumps(out, indent=2))
Path(__file__).with_name('local_spin_pairing_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
