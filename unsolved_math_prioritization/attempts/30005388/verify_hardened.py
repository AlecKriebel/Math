#!/usr/bin/env python3
"""Exact algebra checks for the accompanying partial research report.

No network, source corpus, symbolic package, filesystem output or knot-realizability
oracle is used. The models are formal complexes, not asserted knot complexes.
All guards survive python -O and -OO.
"""
import argparse
import json
from itertools import product

ZERO = frozenset()
ONE = frozenset({(0, 0)})
NAMES = ('a', 'b', 'c', 'd', 'x')


def need(condition, message):
    if not condition:
        raise ValueError(message)


def mon(u=0, v=0):
    return frozenset({(u, v)})


def padd(a, b):
    return a ^ b


def pmul(a, b):
    out = ZERO
    for u, v in a:
        for s, t in b:
            out ^= mon(u + s, v + t)
    return out


def sigma(a):
    return frozenset((v, u) for u, v in a)


def zero(n):
    return [[ZERO for _ in range(n)] for _ in range(n)]


def ident(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = ONE
    return a


def add(a, b):
    return [[x ^ y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def mul(a, b):
    n = len(a)
    c = zero(n)
    for i, j, k in product(range(n), repeat=3):
        c[i][j] ^= pmul(a[i][k], b[k][j])
    return c


def trans_coeff(a):
    return [[sigma(p) for p in row] for row in a]


def deriv(a, var):
    def dp(p):
        out = ZERO
        for uv in p:
            if uv[var] % 2:
                t = list(uv)
                t[var] -= 1
                out ^= frozenset({tuple(t)})
        return out
    return [[dp(p) for p in row] for row in a]


def hat(a):
    return [[ONE if (0, 0) in p else ZERO for p in row] for row in a]


def horiz(a):
    return [[frozenset((u, v) for u, v in p if v == 0) for p in row] for row in a]


def tensor(a, b):
    n, m = len(a), len(b)
    return [[pmul(a[i // m][j // m], b[i % m][j % m])
             for j in range(n * m)] for i in range(n * m)]


def model(n, lam, mu):
    need(n >= 1 and lam in (0, 1) and mu in (0, 1), 'bad model parameters')
    d = zero(5)
    d[1][0], d[2][0] = mon(n), mon(0, n)
    d[3][1], d[3][2] = mon(0, n), mon(n)
    j = ident(5)
    j[1][1] = j[2][2] = ZERO
    j[2][1] = j[1][2] = ONE
    j[4][0] = ONE if lam else ZERO
    j[3][4] = mon(n-1, n-1) if mu else ZERO
    grades = [(0, 0), (2*n-1, -1), (-1, 2*n-1), (2*n-2, 2*n-2), (0, 0)]
    return d, j, grades


def check_grades(a, grades, differential=False, skew=False):
    for i, j in product(range(len(a)), repeat=2):
        gu, gv = grades[j]
        target = (gu-1, gv-1) if differential else ((gv, gu) if skew else (gu, gv))
        for u, v in a[i][j]:
            need((grades[i][0]-2*u, grades[i][1]-2*v) == target, 'grading mismatch')


def bits(a):
    return [sum((int(bool(p)) << j) for j, p in enumerate(row)) for row in a]


def solve(rows, values, n):
    rows = [r | (v << n) for r, v in zip(rows, values)]
    pivots = []
    k = 0
    for c in range(n):
        hit = next((i for i in range(k, len(rows)) if (rows[i] >> c) & 1), None)
        if hit is None:
            continue
        rows[k], rows[hit] = rows[hit], rows[k]
        for i in range(len(rows)):
            if i != k and (rows[i] >> c) & 1:
                rows[i] ^= rows[k]
        pivots.append(c)
        k += 1
    mask = (1 << n)-1
    if any((r & mask) == 0 and (r >> n) for r in rows):
        return None
    return sum(((rows[i] >> n) & 1) << c for i, c in enumerate(pivots))


def local_constant_maps(d, j, grades, tower):
    # For the tested models, every degree-zero polynomial map to/from O is
    # constant: no basis grade (2k,0) or (-2k,0) with k>0 occurs.
    allowed = [i for i, g in enumerate(grades) if g == (0, 0)]
    need(tower in allowed, 'tower not degree zero')
    for g in grades:
        need(not (g[1] == 0 and g[0] != 0), 'nonconstant maps not covered')
    n = len(d)
    # All nonzero horizontal differential entries have one common U-power.
    nonzero = {p for row in d for p in row if p}
    need(len(nonzero) <= 1, 'differential has multiple powers')
    db = [[ONE if p else ZERO for p in row] for row in d]
    w = add(j, ident(n))
    def restrict(row):
        return sum((bool(row[i]) << k) for k, i in enumerate(allowed))
    eq_g = [restrict(row) for a in (db, w) for row in a]
    eq_f = [restrict([a[i][col] for i in range(n)])
            for a in (db, w) for col in range(n)]
    anchor = 1 << allowed.index(tower)
    result = []
    for eq in (eq_g, eq_f):
        v = solve(eq + [anchor], [0]*len(eq) + [1], len(allowed))
        result.append(None if v is None else [allowed[k] for k in range(len(allowed)) if (v >> k) & 1])
    return result


def trefoil_tensor_v0(power):
    # The usual right-trefoil staircase: p,q are cycles, dr=p+q.
    # Filtrations are (0,1),(1,0),(1,1), Maslov degrees 0,0,1.
    base = list(product(range(3), repeat=power))
    index = {t: i for i, t in enumerate(base)}
    filt = [(sum(x != 0 for x in t), sum(x != 1 for x in t)) for t in base]
    maslov = [t.count(2) for t in base]
    for k in range(4):
        allowed = []
        for i, ((a, b), m) in enumerate(zip(filt, maslov)):
            if m % 2 == 0:
                u = (m + 2*k)//2
                if a <= u and b <= u:
                    allowed.append(i)
        columns = []
        for i in allowed:
            mask = 0
            t = base[i]
            for pos, x in enumerate(t):
                if x == 2:
                    for y in (0, 1):
                        s = list(t)
                        s[pos] = y
                        mask ^= 1 << index[tuple(s)]
            columns.append(mask)
        rows = [sum(((col >> i) & 1) << j for j, col in enumerate(columns))
                for i in range(len(base))]
        augment = sum((int(2 not in base[i]) << j) for j, i in enumerate(allowed))
        answer = solve(rows + [augment], [0]*len(rows) + [1], len(allowed))
        if answer is not None:
            return k
    raise ValueError('staircase bound exceeded')


def verify(corrupt=None):
    out = {'scope': 'formal-complex and elementary character checks only', 'cases': []}
    # A hypothetical homomorphism identity is tested directly, not asserted.
    for u, v in product(range(2), repeat=2):
        need(((u ^ (u ^ v)) == v), 'difference character')
    need((0 ^ 1) == 1, 'nonzero residual witness')
    need(all((z*z) % 8 == 1 for z in range(1, 32, 2)), 'odd squares mod 8')
    out['trefoil_V0'] = [trefoil_tensor_v0(n) for n in (1, 2)]
    need(out['trefoil_V0'] == [1, 1], 'surgery nonadditivity calculation')
    out['HKL_Arf_residue_checks'] = 64
    for n in range(1, 65):
        residue = (4*n*n+1) % 8
        need(residue == (5 if n % 2 else 1), 'HKL determinant parity')
    for n in range(1, 12):
        for lam, mu in product(range(2), repeat=2):
            d, j, grades = model(n, lam, mu)
            check_grades(d, grades, differential=True)
            check_grades(j, grades, skew=True)
            need(mul(d, d) == zero(5), 'd squared')
            need(mul(d, j) == mul(j, trans_coeff(d)), 'skew chain map')
            phi, psi = deriv(d, 0), deriv(d, 1)
            square_defect = add(add(mul(j, trans_coeff(j)), ident(5)), mul(phi, psi))
            actual = (square_defect == zero(5))
            expected = (lam*mu == n % 2)
            if corrupt == 'full_lift' and n == 3 and lam == mu == 0:
                expected = True
            need(actual == expected, 'full lift identity guard')
            if actual:
                need(mul(j, trans_coeff(phi)) == mul(psi, j), 'derivative conjugation')
            hd, hj = horiz(d), hat(j)
            hphi = hat(deriv(hd, 0))
            hpsi = mul(mul(hj, hphi), hj)
            hsquare = add(add(mul(hj, hj), ident(5)), mul(hphi, hpsi))
            horizontal_valid = (hsquare == zero(5))
            need(horizontal_valid == (n > 1 or expected), 'horizontal axiom')
            if horizontal_valid:
                need(mul(hphi, hpsi) == mul(hpsi, hphi), 'horizontal commutation')
                # For n>1 both maps vanish; for n=1 use the V derivative lift.
                lift = zero(5) if n > 1 else horiz(psi)
                need(hat(lift) == hpsi, 'Psi lift hat')
                need(mul(hd, lift) == mul(lift, hd), 'Psi lift chain map')
                maps = local_constant_maps(hd, hj, grades, 4)
                if n > 1:
                    need(maps[0] is not None, 'tower inclusion')
                    need((maps[1] is not None) == (lam == 0), 'projection obstruction')
                elif lam == mu == 1:
                    need(maps == [None, None], 'figure-eight incomparability')
            # Euler characteristic is 3-t^n-t^-n, using parity of gr_U.
            delta = {}
            for gu, gv in grades:
                a = (gu-gv)//2
                delta[a] = delta.get(a, 0) + (-1 if gu % 2 else 1)
            need(delta == {-n: -1, 0: 3, n: -1}, 'Euler polynomial')
            det = sum(c*((-1)**a) for a, c in delta.items())
            need(det == (5 if n % 2 else 1), 'Euler value at minus one')
            out['cases'].append({'n': n, 'lambda': lam, 'mu': mu,
                                 'full_square_identity': actual, 'horizontal_valid': horizontal_valid})
    # Explicit local maps for the actual figure-eight horizontal model squared.
    d, j, grades = model(1, 1, 1)
    d, j = horiz(d), hat(j)
    phi = hat(deriv(d, 0))
    dt = add(tensor(d, ident(5)), tensor(ident(5), d))
    jt = add(tensor(j, j), tensor(mul(phi, j), mul(j, phi)))
    gt = [(a+c, b+e) for a, b in grades for c, e in grades]
    check_grades(dt, gt, differential=True)
    check_grades(jt, gt, skew=True)
    # A tensor involution must satisfy the horizontal square axiom itself.
    # Merely finding maps for an arbitrary matrix does not establish this.
    tensor_phi = hat(deriv(dt, 0))
    tensor_psi = mul(mul(jt, tensor_phi), jt)
    need(mul(jt, jt) == add(ident(25), mul(tensor_phi, tensor_psi)),
         'tensor horizontal square axiom')
    need(mul(tensor_phi, tensor_psi) == mul(tensor_psi, tensor_phi),
         'tensor horizontal derivative commutation')
    maps = local_constant_maps(dt, jt, gt, 24)
    need(all(m is not None for m in maps), 'tensor-square local maps missing')
    # Verify the report's literal certificates, not whichever supports a
    # solver finds. The indices are ad, bc, cb, da, xx in the stated basis.
    g = [3, 7, 11, 15, 24]
    f = [3, 7, 11, 15, 24]
    if corrupt == 'tensor_map':
        g = [24]
    # Check these fixed displayed lists against polynomial matrices.
    gv = [ONE if i in g else ZERO for i in range(25)]
    fv = [ONE if i in f else ZERO for i in range(25)]
    for i in range(25):
        v = ZERO
        w = ZERO
        for k in range(25):
            v ^= pmul(dt[i][k], gv[k])
            w ^= pmul(add(jt, ident(25))[i][k], gv[k])
        need(not v and not w, 'tensor inclusion guard')
    for k in range(25):
        v = ZERO
        w = ZERO
        for i in range(25):
            v ^= pmul(fv[i], dt[i][k])
            w ^= pmul(fv[i], add(jt, ident(25))[i][k])
        need(not v and not w, 'tensor projection guard')
    need(24 in f and 24 in g, 'localized tower check')
    out['tensor_square_maps'] = {
        'inclusion_image': [NAMES[i//5]+NAMES[i%5] for i in g],
        'projection_support': [NAMES[i//5]+NAMES[i%5] for i in f]}
    out['result'] = 'PASS'
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corrupt', choices=('full_lift', 'tensor_map'))
    args = parser.parse_args()
    print(json.dumps(verify(args.corrupt), sort_keys=True, indent=2))
