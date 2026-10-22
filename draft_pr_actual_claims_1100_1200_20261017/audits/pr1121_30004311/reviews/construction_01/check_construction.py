#!/usr/bin/env python3
"""Independent exact construction audit; stdlib, explicit non-removable guards.

Finite checks supplement the all-input argument in REPORT.md. In particular this
does not enumerate 20000**3 associativity or brace-compatibility triples.
"""
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


ZERO = (0, 0, 0, 0)
R = tuple(product(range(5), repeat=4))
V = tuple(v for v in range(32) if v.bit_count() % 2 == 0)
X = (1, 0, 0, 0)
RB = tuple(tuple(int(i == j) for i in range(4)) for j in range(4))
VB = tuple((1 << j) | 16 for j in range(4))
O = (ZERO, 0, 0)


def ra(a, b):
    return tuple((a[i] + b[i]) % 5 for i in range(4))


def rs(c, a):
    return tuple((c * x) % 5 for x in a)


def rm(a, b):
    # Coefficients of x, x^2, x^3, x^4. No quotient tables imported.
    return (0, a[0] * b[0] % 5,
            (a[0] * b[1] + a[1] * b[0]) % 5,
            (a[0] * b[2] + a[1] * b[1] + a[2] * b[0]) % 5)


def rc(a, b):
    return ra(ra(a, b), rm(a, b))


def polynomial(a, coeffs):
    out, power = ZERO, a
    for c in coeffs:
        out = ra(out, rs(c, power))
        power = rm(power, a)
    return out


def logarithm(a):
    return polynomial(a, (1, 2, 2, 1))


def exponential(a):
    return polynomial(a, (1, 3, 1, 4))


def sigma(a):
    return ((-a[0]) % 5, a[1], (-a[2]) % 5, a[3])


def beta(a, b):
    return (a & b).bit_count() % 2


def q(a):
    return (a.bit_count() // 2) % 2


def rotate(a, s=1):
    s %= 5
    return ((a << s) | (a >> (5 - s))) & 31


LOG = {a: logarithm(a) for a in R}
EXP = {a: exponential(a) for a in R}


def eta(a):
    return LOG[a][3]


def add(a, b):
    return (ra(a[0], b[0]), a[1] ^ b[1], a[2] ^ b[2])


def scale(n, a):
    return (rs(n, a[0]), a[1] if n % 2 else 0, a[2] if n % 2 else 0)


def sub(a, b):
    return add(a, scale(-1, b))


def circle(a, b, raw_eta=False, omit_q=False, omit_sigma=False, omit_m=False):
    r, v, z = a
    u, w, zz = b
    s = r[3] if raw_eta else eta(r)
    e = z if omit_q else z ^ q(v)
    transformed_u = sigma(u) if e and not omit_sigma else u
    transformed_w = w if omit_m else rotate(w, s)
    return (rc(r, transformed_u), v ^ transformed_w,
            z ^ zz ^ beta(v, transformed_w))


def lam(a, b):
    return sub(circle(a, b), a)


def star(a, b):
    return sub(lam(a, b), b)


def psi(a):
    r, v, z = a
    l = LOG[r]
    return (l[:3], z ^ q(v), v, l[3])


def unpsi(c):
    k, e, v, s = c
    return (EXP[k + (s,)], v, e ^ q(v))


def gp(a, b):
    k, e, v, s = a
    h, f, w, t = b
    signed = ((-h[0]) % 5, h[1], (-h[2]) % 5) if e else h
    return (tuple((k[i] + signed[i]) % 5 for i in range(3)), e ^ f,
            v ^ rotate(w, s), (s + t) % 5)


def rank(columns, p):
    matrix = [list(row) for row in zip(*columns)]
    row = 0
    for col in range(len(columns)):
        pivot = next((j for j in range(row, len(matrix))
                      if matrix[j][col] % p), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inv = pow(matrix[row][col], -1, p)
        matrix[row] = [(x * inv) % p for x in matrix[row]]
        for j in range(len(matrix)):
            if j != row:
                c = matrix[j][col]
                matrix[j] = [(x - c * y) % p
                             for x, y in zip(matrix[j], matrix[row])]
        row += 1
        if row == len(matrix):
            break
    return row


def vcoords(v):
    return tuple((v >> i) & 1 for i in range(4))


def main():
    base = Path(__file__).resolve().parents[2]
    pin = '68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75'
    proof_hash = sha256((base / 'inputs/PROOF.md').read_bytes()).hexdigest()
    require(proof_hash == pin, 'Frozen proof hash mismatch')
    require(len(R) == 625 and len(V) == 16, 'Wrong finite sets')
    counts = {}
    for a in R:
        require(LOG[EXP[a]] == a and EXP[LOG[a]] == a, 'Log/exp inverse')
        require(LOG[sigma(a)] == sigma(LOG[a]), 'Log sigma equivariance')
        a1, a2, a3, a4 = a
        closed_eta = (a4 - a1*a3 - 3*a2*a2 + a1*a1*a2 - 4*a1**4) % 5
        require(eta(a) == closed_eta, 'Displayed eta formula')
        for b in R:
            require(LOG[rc(a, b)] == ra(LOG[a], LOG[b]), 'Log circle homomorphism')
            for e in range(2):
                sb = sigma(b) if e else b
                require(LOG[rc(a, sb)] == ra(LOG[a], sigma(LOG[b]) if e else LOG[b]),
                        'Twisted ring coordinate formula')
    counts['log_inverse_and_equivariance_inputs'] = len(R)
    counts['log_homomorphism_pairs'] = len(R)**2
    counts['twisted_ring_coordinate_cases'] = 2 * len(R)**2

    for v in V:
        require(beta(v, v) == 0, 'Alternation')
        require(rotate(v, 5) == v, 'Order divides five')
        if v:
            require(any(beta(v, w) for w in V), 'Nondegeneracy')
            require(rotate(v) != v, 'Fixed vector')
        for w in V:
            require(q(v ^ w) == q(v) ^ q(w) ^ beta(v, w), 'Quadratic identity')
            require(beta(rotate(v), rotate(w)) == beta(v, w), 'Orthogonality')
            for u in V:
                require(beta(v, w ^ u) == beta(v, w) ^ beta(v, u), 'Bilinearity')
            for z, zz, s in product(range(2), range(2), range(5)):
                mw = rotate(w, s)
                out_v = v ^ mw
                out_z = z ^ zz ^ beta(v, mw)
                require(out_z ^ q(out_v) == z ^ q(v) ^ zz ^ q(w),
                        'Binary group-coordinate formula')
    counts['binary_bilinearity_triples'] = len(V)**3
    counts['binary_group_coordinate_cases'] = len(V)**2 * 4 * 5

    basis = tuple((r, 0, 0) for r in RB) + tuple((ZERO, v, 0) for v in VB) + ((ZERO, 0, 1),)
    B = tuple(product(R, V, range(2)))
    coords = set()
    for a in B:
        c = psi(a)
        require(unpsi(c) == a, 'Psi inverse')
        coords.add(c)
        for b in basis:
            require(psi(circle(a, b)) == gp(c, psi(b)), 'Right generator isomorphism')
            require(psi(circle(b, a)) == gp(psi(b), c), 'Left generator isomorphism')
    require(len(coords) == len(B) == 20000, 'Psi not bijective')
    counts['psi_bijection_inputs'] = len(B)
    counts['supplementary_both_direction_basis_pairs'] = 2 * len(B) * len(basis)

    # Independently recover every possible ring lambda block as a matrix, and
    # check all binary lambda block inputs/pairs rather than sampling B triples.
    for r, e in product(R, range(2)):
        a = (r, 0, e)
        columns = tuple(lam(a, (u, 0, 0))[0] for u in RB)
        require(rank(columns, 5) == 4, 'Singular ring lambda block')
        for u in R:
            predicted = ZERO
            for c, col in zip(u, columns):
                predicted = ra(predicted, rs(c, col))
            require(lam(a, (u, 0, 0))[0] == predicted, 'Nonlinear ring lambda block')
    binary = tuple((ZERO, v, z) for v, z in product(V, range(2)))
    for v, s in product(V, range(5)):
        a = ((0, 0, 0, s), v, 0)
        images = {lam(a, b) for b in binary}
        require(len(images) == 32, 'Singular binary lambda block')
        for b in binary:
            for c in binary:
                require(lam(a, add(b, c)) == add(lam(a, b), lam(a, c)),
                        'Nonadditive binary lambda block')
    counts['ring_lambda_matrices'] = 1250
    counts['ring_lambda_matrix_inputs'] = 1250 * 625
    counts['binary_lambda_permutation_inputs'] = 80 * 32
    counts['binary_lambda_additivity_pairs'] = 80 * 32 * 32

    # Semidirect-product derived images: tau-1 has rank 2 and M-1 rank 4.
    tau_image = tuple(tuple(((-k[i] if i in (0, 2) else k[i]) - k[i]) % 5
                            for i in range(3))
                      for k in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    require(rank(tau_image, 5) == 2, 'Wrong tau commutator image')
    m_image = tuple(vcoords(rotate(v) ^ v) for v in VB)
    require(rank(m_image, 2) == 4, 'Wrong M commutator image')
    for a in binary:
        for b in binary:
            require(circle(a, b) == circle(b, a), 'Nonabelian Sylow 2 subgroup')
            require(circle(a, b)[0] == ZERO, 'Sylow 2 closure')
    # The entire P5 law was exhausted above via the circle-log homomorphism.
    counts['derived_order'] = 5**2 * 2**4
    counts['actual_Sylow_2_commutativity_pairs'] = 32**2
    counts['actual_Sylow_5_log_group_pairs'] = 625**2

    # A proof-producing membership engine. Each rule validates its already-known
    # premise, evaluates the literal operation, and appends a reproducible record.
    stream = sha256()
    steps = 0
    preimage = {rotate(w) ^ w: w for w in V}
    require(len(preimage) == 16, 'M-1 not bijective')
    for seed in B:
        if seed == O:
            continue
        known = {seed}
        stream.update((json.dumps(['seed', seed], separators=(',', ':')) + '\n').encode())

        def infer(rule, source, actor=None, scalar=None):
            nonlocal steps
            require(source in known, 'Membership proof used unknown source')
            if rule == 'scale':
                result = scale(scalar, source)
            elif rule == 'lambda_difference':
                result = sub(lam(actor, source), source)
            elif rule == 'star':
                result = star(source, actor)
            else:
                raise RuntimeError('Unknown membership inference')
            known.add(result)
            record = [rule, source, actor, scalar, result]
            stream.update((json.dumps(record, separators=(',', ':')) + '\n').encode())
            steps += 1
            return result

        if seed[0] != ZERO:
            primary = infer('scale', seed, scalar=2)
            require(primary[0] != ZERO and primary[1:] == (0, 0), 'Primary projection')
            j = next(i for i, c in enumerate(primary[0]) if c)
            top = primary if j == 3 else infer('lambda_difference', primary,
                                               actor=(RB[2-j], 0, 0))
            require(top[0][:3] == (0, 0, 0) and top[0][3], 'Lowest-term extraction')
            a4 = infer('scale', top, scalar=pow(top[0][3], -1, 5))
        else:
            if seed[1]:
                w = next(w for w in V if beta(w, seed[1]))
                bbit = infer('lambda_difference', seed, actor=(ZERO, w, 0))
            else:
                bbit = seed
            require(bbit == (ZERO, 0, 1), 'Binary shear failed')
            x = infer('scale', infer('star', bbit, actor=(X, 0, 0)), scalar=2)
            require(x == (X, 0, 0), 'Binary reflection did not yield x')
            a4 = infer('lambda_difference', x, actor=(RB[2], 0, 0))
        require(a4 == (RB[3], 0, 0), 'No normalized x^4')
        for v in VB:
            p = infer('star', a4, actor=(ZERO, preimage[v], 0))
            require(p == (ZERO, v, 0), 'x^4 did not propagate to V')
        p = (ZERO, VB[0], 0)
        w = next(w for w in V if beta(w, p[1]))
        bbit = infer('lambda_difference', p, actor=(ZERO, w, 0))
        require(bbit == (ZERO, 0, 1), 'No binary central basis vector')
        x = infer('scale', infer('star', bbit, actor=(X, 0, 0)), scalar=2)
        p = x
        for j in range(3):
            p = infer('lambda_difference', p, actor=(X, 0, 0))
            require(p == (RB[j+1], 0, 0), 'Monomial propagation failed')
        require(all(b in known for b in basis), 'Missing additive basis element')
    counts['nonzero_ideal_seed_derivations'] = len(B) - 1
    counts['validated_ideal_membership_steps'] = steps
    counts['ideal_derivation_stream_sha256'] = stream.hexdigest()

    require(star((X, 0, 0), (X, 0, 0)) == (RB[1], 0, 0), 'Nontriviality witness')
    require(star(star((X, 0, 0), (X, 0, 0)), (X, 0, 0)) == (RB[2], 0, 0),
            'Triple-star witness')
    controls = {}
    for name, witness, option in (
        ('raw_x4_eta', ((X, 0, 0), (RB[2], 0, 0), (ZERO, 3, 0)), {'raw_eta': True}),
        ('omit_quadratic_correction', ((ZERO, 3, 0), (ZERO, 5, 0), (X, 0, 0)), {'omit_q': True}),
    ):
        a, b, c = witness
        left = circle(circle(a, b, **option), c, **option)
        right = circle(a, circle(b, c, **option), **option)
        require(left != right, 'Broken associativity control did not fail: ' + name)
        controls[name] = {'witness': witness, 'left': left, 'right': right}
    # Algebraic kernel arguments in REPORT.md prove the proper ideals universally.
    # Here test their necessary generator invariance/star closures exactly.
    for name, primary, option in (
        ('omit_sigma', binary, {'omit_sigma': True}),
        ('omit_M', tuple((r, 0, 0) for r in R), {'omit_m': True}),
    ):
        primary_set = set(primary)
        require(1 < len(primary_set) < len(B), 'Broken simplicity control size')
        for i in primary:
            for g in basis:
                require(sub(circle(g, i, **option), g) in primary_set,
                        'Kernel lambda generator invariance')
                require(sub(sub(circle(i, g, **option), i), g) in primary_set,
                        'Kernel star generator closure')
        controls[name] = {'proper_ideal_order': len(primary_set),
                          'generator_cases': len(primary_set) * len(basis)}
    out = {'status': 'PASS', 'target_pr_head': 'f86b108ac1bc024302648eee9f47f74e26c810ec',
           'proof_sha256': proof_hash, 'checks': counts, 'negative_controls': controls,
           'scope_limit': 'Factored exhaustive identities, basis cross-checks, and all-seed '
                          'ideal derivations; no 20000^3 triple enumeration and no literature claim.'}
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
