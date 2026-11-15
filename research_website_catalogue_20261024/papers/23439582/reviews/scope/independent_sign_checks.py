"""Own exact mixed even/odd Hopf convention checks, before supplied code reading.

H=F_p[y]/(y^p) tensor exterior(x1,x2), |y|=2, |x_i|=1.
These finite identities corroborate formulas, not the infinite theorem.
"""
from itertools import product
from math import comb
from datetime import datetime, timezone
import json


def require(test, message):
    if not test:
        raise ValueError(message)


def run_model(p, bosonize):
    basis = list(product(range(p), range(4), range(2 if bosonize else 1)))
    unit = (0, 0, 0)
    checks = 0

    def parity(mask):
        return mask.bit_count() % 2

    def clean(items):
        return {x: c % p for x, c in items.items() if c % p}

    def add(out, x, c):
        out[x] = (out.get(x, 0) + c) % p

    def mult(a, b):
        n, m, i = a
        r, s, j = b
        if n + r >= p or m & s:
            return None, 0
        inversions = int(bool(m & 2) and bool(s & 1))
        sign = (-1) ** (inversions + i * parity(s))
        return (n + r, m | s, i ^ j), sign % p

    def delta(a, omit_parity=False):
        n, mask, i = a
        out = {}
        for r in range(n + 1):
            for left in range(4):
                if left & ~mask:
                    continue
                right = mask ^ left
                crossings = int(bool(right & 1) and bool(left & 2))
                coefficient = comb(n, r) * (-1) ** crossings
                gleft = i ^ (parity(right) if bosonize and not omit_parity else 0)
                add(out, ((r, left, gleft), (n-r, right, i)), coefficient)
        return clean(out)

    def antipode(a, omit_parity=False):
        n, mask, i = a
        q = parity(mask)
        g = i ^ (q if bosonize and not omit_parity else 0)
        # First SH, then left multiplication by the parity-group element.
        coefficient = (-1) ** (n + mask.bit_count() + g * q)
        return (n, mask, g), coefficient % p

    def eps(a):
        return int(a[0] == 0 and a[1] == 0)

    def tensor_mult(x, y):
        out = {}
        for (a, b), c in x.items():
            for (u, v), d in y.items():
                av, ca = mult(a, u)
                bv, cb = mult(b, v)
                if ca and cb:
                    add(out, (av, bv), c*d*ca*cb)
        return clean(out)

    ds = {a: delta(a) for a in basis}
    for a in basis:
        lhs, rhs = {}, {}
        leftc, rightc = {}, {}
        antileft, antiright = {}, {}
        for (b, c), coefficient in ds[a].items():
            for (u, v), k in ds[b].items():
                add(lhs, (u, v, c), coefficient*k)
            for (u, v), k in ds[c].items():
                add(rhs, (b, u, v), coefficient*k)
            add(leftc, c, coefficient*eps(b))
            add(rightc, b, coefficient*eps(c))
            sb, kb = antipode(b)
            sc, kc = antipode(c)
            u, ku = mult(sb, c)
            v, kv = mult(b, sc)
            if ku:
                add(antileft, u, coefficient*kb*ku)
            if kv:
                add(antiright, v, coefficient*kc*kv)
        require(clean(lhs) == clean(rhs), 'coassociativity')
        require(clean(leftc) == clean(rightc) == {a: 1}, 'counit')
        expected = {unit: 1} if eps(a) else {}
        require(clean(antileft) == clean(antiright) == expected, 'both antipodes')
        checks += 4
    for a, b in product(basis, repeat=2):
        c, coefficient = mult(a, b)
        expected = clean({x: v*coefficient for x, v in ds[c].items()}) if coefficient else {}
        require(tensor_mult(ds[a], ds[b]) == expected, 'Delta multiplicativity')
        require(eps(c)*coefficient % p == eps(a)*eps(b) % p if coefficient else eps(a)*eps(b) == 0, 'epsilon multiplicativity')
        checks += 2
    for a, b, c in product(basis, repeat=3):
        ab, k = mult(a, b)
        bc, l = mult(b, c)
        left, lk = mult(ab, c) if k else (None, 0)
        right, rk = mult(a, bc) if l else (None, 0)
        left, right = ({left: k*lk % p} if k*lk % p else {}), ({right: l*rk % p} if l*rk % p else {})
        require(left == right, 'associativity')
        checks += 1
    controls = {}
    if bosonize and p != 2:
        x = (0, 1, 0)
        bad_delta = delta(x, omit_parity=True)
        residue = tensor_mult(bad_delta, bad_delta)
        require(bool(residue), 'odd parity omission must fail Delta(x*x)=0')
        controls['omit_coproduct_parity_detected'] = True
        anti_residue = {}
        for (a, b), coefficient in ds[x].items():
            sa, k = antipode(a, omit_parity=True)
            v, l = mult(sa, b)
            if l:
                add(anti_residue, v, coefficient*k*l)
        require(bool(clean(anti_residue)), 'odd antipode parity omission must fail')
        controls['omit_antipode_parity_detected'] = True
    return {'characteristic': p, 'model': 'parity bosonization' if bosonize else 'char2 grading forgotten',
            'H_basis_dimension': 4*p, 'tested_ordinary_Hopf_dimension': len(basis),
            'identity_checks': checks, 'all_basis_triples_associativity': len(basis)**3,
            'all_basis_pairs_Delta_multiplicativity': len(basis)**2,
            'negative_controls': controls}


if __name__ == '__main__':
    models = [run_model(2, False), run_model(3, True), run_model(5, True)]
    print(json.dumps({'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
                      'construction': 'Mixed primitive even truncated polynomial and two odd exterior generators; no supplied imports.',
                      'models': models, 'identity_checks_total': sum(x['identity_checks'] for x in models),
                      'limits': 'Finite exact convention checks; no topological or universal infinite-Hopf conclusion inferred.'}, indent=2))
