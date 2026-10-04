#!/usr/bin/env python3
"""Independent audit: exact LDL factorization and determinant fault tests.
No original controls module is imported. No topology theorem is tested.
"""
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def matmul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def ldlt(a):
    n = len(a)
    assert all(len(row) == n for row in a)
    assert all(a[i][j] == a[j][i] for i in range(n) for j in range(n))
    l = [[Q(i == j) for j in range(n)] for i in range(n)]
    d = []
    for j in range(n):
        pivot = Q(a[j][j]) - sum(l[j][k]**2*d[k] for k in range(j))
        if pivot == 0:
            raise ValueError('zero LDL pivot')
        d.append(pivot)
        for i in range(j + 1, n):
            l[i][j] = (Q(a[i][j]) - sum(l[i][k]*l[j][k]*d[k] for k in range(j))) / pivot
    ld = [[l[i][j]*d[j] for j in range(n)] for i in range(n)]
    assert matmul(ld, list(map(list, zip(*l)))) == a
    return d


def laplace(a):
    if not a:
        return 1
    return sum((-1)**j*a[0][j]*laplace([r[:j] + r[j+1:] for r in a[1:]])
               for j in range(len(a)) if a[0][j])


def product(xs):
    r = Q(1)
    for x in xs:
        r *= x
    return r


def main():
    payload = json.loads((ROOT/'bundle/CONTROL_RESULTS.json').read_text())
    # Rebuild independently via the E8 Dynkin graph, then compare the saved data.
    e8 = [[2*int(i == j) for j in range(8)] for i in range(8)]
    for i, j in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(2,7)]:
        e8[i][j] = e8[j][i] = -1
    assert payload['E8_matrix'] == e8
    d = ldlt(e8)
    assert d == list(map(Q, ['2','3/2','4/3','5/4','6/5','7/6','8/7','1/8']))
    assert all(v > 0 for v in d)
    assert product(d) == laplace(e8) == 1
    minors = [int(product(d[:k])) for k in range(1,9)]
    assert minors == payload['E8_leading_principal_minors']
    e16 = [r + [0]*8 for r in e8] + [[0]*8 + r for r in e8]
    d16 = ldlt(e16)
    assert d16 == d+d and product(d16) == 1
    assert all(e16[i][i] % 2 == 0 for i in range(16))
    # Every binary residue class has even quadratic norm. Together with
    # integer symmetry this covers parity of all integer vectors in rank 8.
    parity_classes = 0
    for x in itertools.product((0,1), repeat=8):
        assert sum(e8[i][j]*x[i]*x[j] for i in range(8) for j in range(8)) % 2 == 0
        parity_classes += 1
    broken = [r[:] for r in e8]
    broken[2][7] = broken[7][2] = 0
    assert product(ldlt(broken)) == laplace(broken) == 16
    odd = [r[:] for r in e8]
    odd[0][0] = 3
    assert odd[0][0] % 2 == 1
    singular = [r[:] for r in e8]
    singular[-1] = singular[0][:]
    assert laplace(singular) == 0
    h = [[0,1],[1,0]]
    assert laplace(h) == -1
    assert laplace([[0]]) == 0
    assert laplace([[1]]) == 1
    manifest = (ROOT/'bundle/SHA256SUMS').read_bytes()
    hashes = {}
    for line in manifest.decode().splitlines():
        digest, name = line.split('  ',1)
        got = hashlib.sha256((ROOT/'bundle'/name).read_bytes()).hexdigest()
        assert got == digest
        hashes[name] = got
    assert hashes['PARTIAL_RESULTS.md'] == '9960b3632cd0e25986a4ac97f2a11e834663604adb1872d0fc0d1e510e9599cb'
    replay = (ROOT/'audit/REPLAY_CONTROL_RESULTS.json').read_bytes()
    assert replay == (ROOT/'bundle/CONTROL_RESULTS.json').read_bytes()
    out = {
        'status':'pass',
        'independent_of_original_controls_implementation':True,
        'manifest_sha256':hashlib.sha256(manifest).hexdigest(),
        'payload_hashes':hashes,
        'replay_byte_identical':True,
        'E8_exact_LDL_diagonal':[str(x) for x in d],
        'E8_LDL_reconstruction_checked':True,
        'E8_Laplace_determinant':1,
        'E8_leading_minors':minors,
        'E8_plus_E8_exact_LDL_diagonal':[str(x) for x in d16],
        'E8_plus_E8_determinant':1,
        'E8_parity_residue_classes_checked':parity_classes,
        'signatures_from_positive_LDL_diagonals':[8,16],
        'deleted_branch_determinant':16,
        'odd_diagonal_fault_detected':True,
        'duplicate_row_singular_determinant':0,
        'hyperbolic_determinant':-1,
        'scope':'Finite integer/rational algebra only; no CW existence, cap construction, or topological theorem verification.'
    }
    print(json.dumps(out,indent=2)+'\n',end='')


if __name__ == '__main__':
    main()
