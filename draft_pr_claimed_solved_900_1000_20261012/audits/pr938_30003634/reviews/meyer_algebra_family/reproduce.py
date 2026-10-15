#!/usr/bin/env python3
"""Independent exact braid/Burau/Meyer reconstruction, Python standard library only.
No original candidate code or data is imported. Matrices act on column vectors.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import Counter
import json, datetime, argparse, sys
HERE = Path(__file__).resolve().parent

class VerificationError(RuntimeError):
    """A failed mathematical or provenance check, active in every Python mode."""

def require(condition, message):
    if not condition:
        raise VerificationError(str(message))

def frac(M):
    return [[F(x) for x in row] for row in M]

def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def transpose(M):
    return list(map(list, zip(*M))) if M else []

def multiply(A, B):
    if not A or not B:
        return []
    return [[sum((a * b for a, b in zip(row, col)), F(0)) for col in zip(*B)] for row in A]

def subtract(A, B):
    return [[a - b for a, b in zip(x, y)] for x, y in zip(A, B)]

def mv(A, x):
    return [sum((a * b for a, b in zip(row, x)), F(0)) for row in A]

def det2(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]

def inv2(A):
    d = det2(A)
    require(d, 'Verification failed: d')
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]

def rref(M, ncols=None):
    R = frac(M)
    cols = ncols if ncols is not None else len(R[0])
    piv = []
    row = 0
    for j in range(cols):
        k = next((i for i in range(row, len(R)) if R[i][j]), None)
        if k is None:
            continue
        R[row], R[k] = (R[k], R[row])
        a = R[row][j]
        R[row] = [x / a for x in R[row]]
        for i in range(len(R)):
            if i != row:
                a = R[i][j]
                R[i] = [x - a * y for x, y in zip(R[i], R[row])]
        piv.append(j)
        row += 1
        if row == len(R):
            break
    return (R, piv)

def nullspace(M, n):
    R, piv = rref(M, n)
    out = []
    for j in range(n):
        if j not in piv:
            v = [F(0)] * n
            v[j] = F(1)
            for i, k in enumerate(piv):
                v[k] = -R[i][j]
            out.append(v)
    return out

def rank_columns(columns, n):
    if not columns:
        return 0
    return len(rref(transpose(columns), len(columns))[1])

def inertia(M):
    """Exact rational congruences. Off-diagonal-only pivot gives one of each sign."""
    R = frac(M)
    p = m = z = 0
    pivots = []
    require(R == transpose(R), 'Verification failed: R == transpose(R)')
    while R:
        n = len(R)
        i = next((i for i in range(n) if R[i][i]), None)
        if i is not None:
            order = [i] + [j for j in range(n) if j != i]
            R = [[R[j][k] for k in order] for j in order]
            a = R[0][0]
            p += a > 0
            m += a < 0
            pivots.append({'size': 1, 'value': str(a)})
            R = [[R[j][k] - R[j][0] * R[0][k] / a for k in range(1, n)] for j in range(1, n)]
        else:
            edge = next(((i, j) for i in range(n) for j in range(i + 1, n) if R[i][j]), None)
            if edge is None:
                z += n
                break
            i, j = edge
            order = [i, j] + [k for k in range(n) if k not in (i, j)]
            R = [[R[j][k] for k in order] for j in order]
            a = R[0][1]
            p += 1
            m += 1
            pivots.append({'size': 2, 'off_diagonal': str(a)})
            R = [[R[j][k] - (R[j][0] * R[1][k] + R[j][1] * R[0][k]) / a for k in range(2, n)] for j in range(2, n)]
    return dict(positive=p, negative=m, zero=z, signature=p - m, pivots=pivots)
I = ident(2)
J = frac([[0, 1], [-1, 0]])
T = {1: frac([[1, 0], [-1, 1]]), 2: frac([[1, 1], [0, 1]])}
T.update({-i: inv2(T[i]) for i in [1, 2]})

def omega(x, y):
    return x[0] * y[1] - x[1] * y[0]

def meyer(A, B, full=False):
    """GG p544 form on E=im(A^-1-I) intersect im(I-B).
    Compute both E with chosen lifts and its pullback to ker[D1,-D2].
    Kernel ambiguity belongs to the radical; no nonsingularity is assumed.
    """
    D1 = subtract(inv2(A), I)
    D2 = subtract(I, B)
    K = nullspace([D1[i] + [-x for x in D2[i]] for i in range(2)], 4)
    E = []
    lifts = []
    for z in K:
        e = mv(D1, z[:2])
        old = rank_columns(E, 2)
        if rank_columns(E + [e], 2) > old:
            E.append(e)
            lifts.append(z)

    def form(L):
        Q = []
        for z in L:
            xy = [z[i] + z[i + 2] for i in range(2)]
            Q.append([omega(xy, mv(D1, w[:2])) for w in L])
        require(Q == transpose(Q), 'Verification failed: Q == transpose(Q)')
        return Q
    Q = form(lifts)
    QK = form(K)
    ie = inertia(Q)
    ik = inertia(QK)
    require(ie['signature'] == ik['signature'], "Verification failed: ie['signature'] == ik['signature']")
    require(ie['positive'] == ik['positive'] and ie['negative'] == ik['negative'], "Verification failed: ie['positive'] == ik['positive'] and ie['negative'] == ik['negative']")
    require(ik['zero'] == ie['zero'] + len(K) - len(E), "Verification failed: ik['zero'] == ie['zero'] + len(K) - len(E)")
    if full:
        return dict(signature=ie['signature'], D1=D1, D2=D2, kernel_basis=K, kernel_dimension=len(K), intersection_basis=E, intersection_dimension=len(E), chosen_lifts=lifts, intersection_form=Q, pullback_form=QK, intersection_inertia=ie, pullback_inertia=ik)
    return ie['signature']

def inverse_word(w):
    return [-x for x in reversed(w)]

def reduce_word(w):
    out = []
    for x in w:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return out

def comm(x, y):
    return x + y + inverse_word(x) + inverse_word(y)

def power_pairs(w):
    runs = []
    for x in w:
        if runs and runs[-1][0] == abs(x):
            runs[-1][1] += 1 if x > 0 else -1
        else:
            runs.append([abs(x), 1 if x > 0 else -1])
    require(len(runs) % 2 == 0 and all((g == 1 + i % 2 for i, (g, _) in enumerate(runs))), 'Verification failed: len(runs) % 2 == 0 and all((g == 1 + i % 2 for i, (g, _) in enumerate(runs)))')
    return ([v for _, v in runs[::2]], [v for _, v in runs[1::2]])

def matrix_word(w):
    A = I
    for x in w:
        A = multiply(A, T[x])
    return A

def signature(w, full=False):
    A = I
    total = 0
    terms = []
    for j, x in enumerate(w, 1):
        data = meyer(A, T[x], full)
        val = data['signature'] if full else data
        total -= val
        if full:
            terms.append(dict(step=j, letter=x, prefix_matrix=A, generator_matrix=T[x], meyer=val, closure_signature_after=total, **{k: v for k, v in data.items() if k != 'signature'}))
        A = multiply(A, T[x])
    return (total, A, terms) if full else total

def strand_data(w, n=3):
    labels = list(range(1, n + 1))
    crossings = Counter()
    self_crossings = Counter()
    trace = []
    for j, x in enumerate(w, 1):
        i = abs(x) - 1
        a, b = labels[i:i + 2]
        sgn = 1 if x > 0 else -1
        if a == b:
            self_crossings[a] += 1
        else:
            crossings[tuple(sorted((a, b)))] += sgn
        trace.append(dict(step=j, positions_before=list(labels), letter=x, strand_pair=[a, b], sign=sgn))
        labels[i], labels[i + 1] = (labels[i + 1], labels[i])
    return dict(permutation=labels, pure=labels == list(range(1, n + 1)), pairwise_signed_crossing_sums={f'{a},{b}': crossings[a, b] for a in range(1, n + 1) for b in range(a + 1, n + 1)}, linking_numbers={f'{a},{b}': F(crossings[a, b], 2) for a in range(1, n + 1) for b in range(a + 1, n + 1)}, self_crossing_counts=dict(self_crossings), trace=trace)

def substitute(w, images):
    out = []
    for x in w:
        out = reduce_word(out + (images[abs(x) - 1] if x > 0 else inverse_word(images[abs(x) - 1])))
    return out

def free_artin(w):
    imgs = [[1], [2], [3]]
    for g in w:
        i = abs(g)
        gen = [[1], [2], [3]]
        if g > 0:
            gen[i - 1] = [i, i + 1, -i]
            gen[i] = [i]
        else:
            gen[i - 1] = [i + 1]
            gen[i] = [-(i + 1), i, i + 1]
        imgs = [substitute(x, gen) for x in imgs]
    return imgs

def encode(obj):
    if isinstance(obj, F):
        return int(obj) if obj.denominator == 1 else str(obj)
    raise TypeError(type(obj).__name__)

def calculate(expected_signature=-2):
    a = [1, 1]
    b = [2, 2]
    c = comm(a, b)
    d = inverse_word(a) + c + a
    e = inverse_word(b) + c + b
    u = comm(c, d)
    v = comm(d, e)
    raw = comm(u, v)
    beta = reduce_word(raw)
    A, B = power_pairs(beta)
    sig, mat, terms = signature(beta, True)
    strands = strand_data(beta)
    require(len(beta) == 104 and len(A) == 23 and (sum(A) == sum(B) == 0), 'Verification failed: len(beta) == 104 and len(A) == 23 and (sum(A) == sum(B) == 0)')
    require(all((x % 2 == 0 for x in A + B)), 'Verification failed: all((x % 2 == 0 for x in A + B))')
    require(reduce_word([y for aa, bb in zip(A, B) for z, p in [(1, aa), (2, bb)] for y in [z if p > 0 else -z] * abs(p)]) == beta, 'Verification failed: reduce_word([y for aa, bb in zip(A, B) for z, p in [(1, aa), (2, bb)] for y in [z if p > 0 else -z] * abs(p)]) == beta')
    require(strands['pure'] and all((x == 0 for x in strands['linking_numbers'].values())), "Verification failed: strands['pure'] and all((x == 0 for x in strands['linking_numbers'].values()))")
    require(det2(mat) == 1 and sig == expected_signature, 'Verification failed: det2(mat) == 1 and sig == expected_signature')
    require(mat == frac([[-1401703009468415, 3686720931790848], [2187353096552448, -5753116310519807]]), 'Verification failed: mat == frac([[-1401703009468415, 3686720931790848], [2187353096552448, -5753116310519807]])')
    require(multiply(transpose(mat), multiply(J, mat)) == J, 'Verification failed: multiply(transpose(mat), multiply(J, mat)) == J')
    controls = []

    def ck(name, w, expected):
        value = signature(w)
        require(value == expected, (name, value, expected))
        controls.append(dict(name=name, word=w, signature=value, expected=expected))
    ck('identity', [], 0)
    for g in [1, 2, -1, -2]:
        ck(f'generator_{g}', [g], 0)
        ck(f'inverse_pair_{g}', [g, -g], 0)
        for k in range(1, 9):
            ck(f'2braid_power_{g}_{k}', [g] * k, (1 - k) * (1 if g > 0 else -1))
    for name, w, expected in [('positive_stabilized_unknot', [1, 2], 0), ('negative_stabilized_unknot', [-1, -2], 0), ('positive_stabilized_trefoil', [1, 1, 1, 2], -2), ('negative_stabilized_trefoil', [-1, -1, -1, -2], 2), ('figure_eight', [1, -2, 1, -2], 0), ('positive_T33', [1, 2] * 3, -4), ('positive_T34', [1, 2] * 4, -6)]:
        ck(name, w, expected)
    require(free_artin([1, 2, 1]) == free_artin([2, 1, 2]), 'Verification failed: free_artin([1, 2, 1]) == free_artin([2, 1, 2])')
    require(free_artin([1, -1]) == [[1], [2], [3]], 'Verification failed: free_artin([1, -1]) == [[1], [2], [3]]')
    require(matrix_word([1, 2, 1]) == matrix_word([2, 1, 2]), 'Verification failed: matrix_word([1, 2, 1]) == matrix_word([2, 1, 2])')
    require(inertia([[0, 1], [1, 0]])['signature'] == 0, "Verification failed: inertia([[0, 1], [1, 0]])['signature'] == 0")
    require(inertia([[0, 0], [0, 0]])['zero'] == 2, "Verification failed: inertia([[0, 0], [0, 0]])['zero'] == 2")
    reduced = [[]]
    for length in range(1, 5):
        reduced.extend([list(w) for w in product([1, -1, 2, -2], repeat=length) if all((w[i] != -w[i + 1] for i in range(length - 1)))])
    exhaustive = {'words': len(reduced), 'inverse_and_mirror': 0, 'braid_relation_contexts': 0, 'free_cancellation_contexts': 0, 'cocycle_triples': 0, 'meyer_symmetries': 0}
    for w in reduced:
        s = signature(w)
        require(signature(inverse_word(w)) == -s and signature([-x for x in w]) == -s, 'Verification failed: signature(inverse_word(w)) == -s and signature([-x for x in w]) == -s')
        exhaustive['inverse_and_mirror'] += 1
        require(signature(w + [1, 2, 1]) == signature(w + [2, 1, 2]), 'Verification failed: signature(w + [1, 2, 1]) == signature(w + [2, 1, 2])')
        exhaustive['braid_relation_contexts'] += 1
        require(signature(w + [1, -1, 2, -2]) == s, 'Verification failed: signature(w + [1, -1, 2, -2]) == s')
        exhaustive['free_cancellation_contexts'] += 1
    matrices = []
    for w in reduced:
        matw = matrix_word(w)
        if matw not in matrices:
            matrices.append(matw)
    for X in matrices:
        for Y in [I, T[1], T[-1], T[2], T[-2], matrix_word([1, 2, 1]), matrix_word([1, -2])]:
            q = meyer(X, Y)
            require(q == meyer(Y, X) == -meyer(inv2(X), inv2(Y)) == -meyer(transpose(X), transpose(Y)), 'Verification failed: q == meyer(Y, X) == -meyer(inv2(X), inv2(Y)) == -meyer(transpose(X), transpose(Y))')
            exhaustive['meyer_symmetries'] += 1
            for Z in [T[1], T[-2]]:
                require(meyer(X, Y) + meyer(multiply(X, Y), Z) == meyer(X, multiply(Y, Z)) + meyer(Y, Z), 'Verification failed: meyer(X, Y) + meyer(multiply(X, Y), Z) == meyer(X, multiply(Y, Z)) + meyer(Y, Z)')
                exhaustive['cocycle_triples'] += 1
    cases = []
    for name, X, Y in [('identity_identity', I, I), ('identity_transvection', I, T[1]), ('transvection_identity', T[1], I), ('equal_transvections', T[1], T[1]), ('inverse_transvections', T[1], T[-1]), ('distinct_lines', T[1], T[2]), ('minus_identity_pair', frac([[-1, 0], [0, -1]]), frac([[-1, 0], [0, -1]]))]:
        cases.append(dict(name=name, A=X, B=Y, **meyer(X, Y, True)))
    rank_cases = Counter()
    for X in matrices:
        for Y in matrices[:24]:
            data = meyer(X, Y, True)
            ii = data['intersection_inertia']
            rank_cases[data['intersection_dimension'], ii['positive'], ii['negative'], ii['zero']] += 1
    result = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), scope='Independent existing Burau/Meyer route, not a new discovery mechanism; author 1/5, audit adds 0 positive proof-search turns', raw_word_length=len(raw), free_reduced_word=beta, free_reduced_length=len(beta), power_pairs=dict(A=A, B=B, count=len(A), absolute_Artin_length=sum(map(abs, A + B))), component_deduction='Pure braid: each strand closes separately; deleting other strands is the trivial one-strand braid, hence each component is an unknot.', strand_tracking=strands, final_Burau_matrix=mat, final_Burau_determinant=det2(mat), signature=sig, meyer_sum=sum((t['meyer'] for t in terms)), term_count=len(terms), meyer_terms=terms, controls=controls, exhaustive_controls=exhaustive, distinct_short_matrices=len(matrices), degenerate_cases=cases, inertia_case_counts=[dict(intersection_dimension=k[0], positive=k[1], negative=k[2], zero=k[3], count=v) for k, v in sorted(rank_cases.items())])
    return result

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Explicit result destination; omitted means stdout only.')
    parser.add_argument('--expected-signature', type=int, default=-2, help='Expected witness signature, checked explicitly; default -2.')
    args = parser.parse_args(argv)
    payload = json.dumps(calculate(args.expected_signature), indent=2, default=encode) + '\n'
    if args.output is not None:
        args.output.write_text(payload)
    sys.stdout.write(payload)
if __name__ == '__main__':
    try:
        main()
    except VerificationError as exc:
        print('Verification failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)
