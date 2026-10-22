#!/usr/bin/env python3
"""Independent exact checks for the shared handlebody-generator pass.

No author-lane checking module is imported. Integer free words, sparse integer
polynomials, and sparse exterior powers are implemented here. Finite free-group
and exterior-basis tests supplement (and do not replace) the index-general
proofs in AUDIT.md. The p,q polynomial identities are universal algebraic checks.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
N_CHECKS = 0


def need(condition, label):
    global N_CHECKS
    N_CHECKS += 1
    if not condition:
        raise RuntimeError(label)


# Words are tuples of nonzero signed generator indices. Composition is f after g.
def reduce_word(word):
    answer = []
    for letter in word:
        if answer and answer[-1] == -letter:
            answer.pop()
        else:
            answer.append(letter)
    return tuple(answer)


def inv_word(word):
    return tuple(-letter for letter in reversed(word))


def multiply_words(*words):
    return reduce_word(letter for word in words for letter in word)


def word_power(word, n):
    block = word if n >= 0 else inv_word(word)
    return reduce_word(block * abs(n))


def apply_map(mapping, word):
    blocks = (mapping[abs(letter) - 1] if letter > 0
              else inv_word(mapping[abs(letter) - 1]) for letter in word)
    return multiply_words(*blocks)


def compose(f, g):
    return tuple(apply_map(f, word) for word in g)


def partial_conjugation(rank, moving, conjugator):
    mapping = [(i,) for i in range(1, rank + 1)]
    mapping[moving - 1] = (conjugator, moving, -conjugator)
    return tuple(mapping)


def map_power(mapping, inverse, n):
    result = tuple((i,) for i in range(1, len(mapping) + 1))
    block = mapping if n >= 0 else inverse
    for _ in range(abs(n)):
        result = compose(block, result)
    return result


def free_group_checks():
    rows = []
    w = (3, -2, -3, 2)
    need(reduce_word(w) == w and w[0] != -w[-1], 'w cyclically reduced')
    for rank in range(3, 14):
        identity = tuple((i,) for i in range(1, rank + 1))
        A = partial_conjugation(rank, 1, 2)
        Ai = partial_conjugation(rank, 1, -2)
        B = partial_conjugation(rank, 2, 3)
        Bi = partial_conjugation(rank, 2, -3)
        need(compose(A, Ai) == identity == compose(Ai, A), 'A inverse')
        need(compose(B, Bi) == identity == compose(Bi, B), 'B inverse')
        Phi = compose(compose(compose(A, B), Ai), Bi)
        Phii = compose(compose(compose(B, A), Bi), Ai)
        need(compose(Phi, Phii) == identity, 'commutator inverse')
        need(Phi[0] == multiply_words(w, (1,), inv_word(w)), 'commutator x1')
        need(Phi[1:] == identity[1:], 'commutator fixes remaining basis')
        need(apply_map(Phi, w) == w, 'commutator fixes w')
        for n in range(-20, 21):
            actual = map_power(Phi, Phii, n)
            wn = word_power(w, n)
            expected = multiply_words(wn, (1,), inv_word(wn))
            need(actual[0] == expected, 'power image x1')
            need(actual[1:] == identity[1:], 'power fixed generators')
            need(len(actual[0]) == 8 * abs(n) + 1, 'power reduced length')
            if n:
                need(actual != identity, 'nonzero power nonidentity')
        rows.append({'rank': rank, 'powers_checked': [-20, 20]})
    return {'word_w': list(w), 'commutator_order': 'A B A^-1 B^-1; right-to-left',
            'rows': rows, 'scope': 'Finite exact word tests; all-power non-innerness is proved in AUDIT.md.'}


# Sparse polynomials in formal commuting variables p,q, over Z.
ZERO = {}
ONE = {(0, 0): 1}
P = {(1, 0): 1}
Q = {(0, 1): 1}


def padd(*polys):
    out = {}
    for poly in polys:
        for monomial, value in poly.items():
            out[monomial] = out.get(monomial, 0) + value
    return {key: value for key, value in out.items() if value}


def pscale(poly, scalar):
    return {key: scalar * value for key, value in poly.items() if scalar * value}


def pmul(a, b):
    out = {}
    for (i, j), value_a in a.items():
        for (k, l), value_b in b.items():
            key = (i + k, j + l)
            out[key] = out.get(key, 0) + value_a * value_b
    return {key: value for key, value in out.items() if value}


def matrix_product(a, b):
    return [[padd(*(pmul(a[i][k], b[k][j]) for k in range(len(b))))
             for j in range(len(b[0]))] for i in range(len(a))]


def transposed(a):
    return [list(row) for row in zip(*a)]


def genus_two_checks():
    p2, pq, q2 = pmul(P, P), pmul(P, Q), pmul(Q, Q)
    exponents = [padd(pq, pscale(p2, -1)), padd(pq, pscale(q2, -1)), pscale(pq, -1)]
    # Coordinates are upper-left, off-diagonal, lower-right.
    image = [p2, pq, q2]
    basis = [(1, 0, 0), (0, 0, 1), (1, 1, 1)]
    for coordinate in range(3):
        total = padd(image[coordinate], *(pscale(exponents[j], basis[j][coordinate]) for j in range(3)))
        need(total == ZERO, 'universal balanced exponent identity')
    for exponent in exponents:
        orientation_reversal = {key: value * (-1)**sum(key) for key, value in exponent.items()}
        need(exponent == orientation_reversal, 'orientation independence')
    U = [[ONE, ZERO, p2, pq], [ZERO, ONE, pq, q2],
         [ZERO, ZERO, ONE, ZERO], [ZERO, ZERO, ZERO, ONE]]
    J = [[ZERO, ZERO, ONE, ZERO], [ZERO, ZERO, ZERO, ONE],
         [pscale(ONE, -1), ZERO, ZERO, ZERO], [ZERO, pscale(ONE, -1), ZERO, ZERO]]
    need(matrix_product(matrix_product(transposed(U), J), U) == J,
         'universal p,q symplectic transvection')
    # Basis-coordinate inverse is (r,s,t) -> (r-s,t-s,s).
    M = ((1, 0, 1), (0, 0, 1), (0, 1, 1))
    Mi = ((1, -1, 0), (0, -1, 1), (0, 1, 0))
    for i in range(3):
        for j in range(3):
            need(sum(M[i][k] * Mi[k][j] for k in range(3)) == (i == j), 'integral basis inverse')
    determinant = (M[0][0] * (M[1][1]*M[2][2]-M[1][2]*M[2][1])
                   - M[0][1] * (M[1][0]*M[2][2]-M[1][2]*M[2][0])
                   + M[0][2] * (M[1][0]*M[2][1]-M[1][1]*M[2][0]))
    need(determinant == -1, 'theta basis determinant')
    return {'arithmetic': 'universal sparse Z[p,q] identities and integer 3x3 inverse',
            'theta_basis_determinant': determinant,
            'correction_exponents': ['pq-p^2', 'pq-q^2', '-pq'],
            'scope': 'No finite sampling of p,q; topology and group generation proved separately.'}


# Exterior vectors are canonical sorted triples -> integer coefficient.
def eadd(*vectors):
    out = {}
    for vector in vectors:
        for triple, value in vector.items():
            out[triple] = out.get(triple, 0) + value
    return {key: value for key, value in out.items() if value}


def escale(vector, scalar):
    return {key: scalar * value for key, value in vector.items() if scalar * value}


def exterior_monomial(*indices):
    if len(set(indices)) != len(indices):
        return {}
    sign = (-1)**sum(indices[i] > indices[j] for i in range(len(indices)) for j in range(i+1, len(indices)))
    return {tuple(sorted(indices)): sign}


def exterior_action(images, vector):
    result = {}
    for (i, j, k), coefficient in vector.items():
        for ii, ci in images[i].items():
            for jj, cj in images[j].items():
                for kk, ck in images[k].items():
                    result = eadd(result, escale(exterior_monomial(ii, jj, kk), coefficient * ci * cj * ck))
    return result


def identity_images(g):
    return [{i: 1} for i in range(2 * g)]


def slide(g, i, j):
    images = identity_images(g)
    images[j] = {j: 1, i: 1}
    images[g+i] = {g+i: 1, g+j: -1}
    return images


def disk_twist(g, i):
    images = identity_images(g)
    images[g+i] = {g+i: 1, i: 1}
    return images


def difference_action(images, vector):
    return eadd(exterior_action(images, vector), escale(vector, -1))


def lattice_checks():
    rows = []
    for g in range(2, 11):
        D = lambda i, j: exterior_monomial(i, g+i, g+j)
        def B(i, j, k):
            if i == j:
                return D(j, k)
            if i == k:
                return escale(D(k, j), -1)
            return difference_action(slide(g, i, j), D(j, k))
        def A(i, j, k):
            if k != j:
                return difference_action(disk_twist(g, j), B(i, j, k))
            return escale(difference_action(disk_twist(g, i), B(j, i, j)), -1)
        for i in range(g):
            for j in range(g):
                for k in range(g):
                    if j != k:
                        need(B(i, j, k) == exterior_monomial(i, g+j, g+k), 'ABB realization')
        for i, j in combinations(range(g), 2):
            for k in range(g):
                need(A(i, j, k) == exterior_monomial(i, j, g+k), 'AAB realization')
        for i, j, k in combinations(range(g), 3):
            need(difference_action(disk_twist(g, k), A(i, j, k)) == exterior_monomial(i, j, k),
                 'AAA realization')
        W = [triple for triple in combinations(range(2*g), 3) if triple[0] < g]
        relations = [eadd(*(exterior_monomial(x, j, g+j) for j in range(g))) for x in range(2*g)]
        pivots = []
        for x in range(2*g):
            i = x % g
            nxt = (i+1) % g
            pivot = tuple(sorted((x, nxt, g+nxt)))
            need(relations[x].get(pivot) in (-1, 1), 'unit pivot')
            pivots.append(pivot)
        need(len(set(pivots)) == 2*g, 'distinct pivots')
        all_support = set()
        for relation in relations:
            need(len(relation) == g-1, 'relation support length')
            need(not (all_support & set(relation)), 'relation supports disjoint')
            all_support.update(relation)
        nonpivots = set(W) - set(pivots)
        def normal_form(vector):
            out = dict(vector)
            for pivot, relation in zip(pivots, relations):
                coefficient = out.get(pivot, 0) * relation[pivot]
                out = eadd(out, escale(relation, -coefficient))
            return out
        for relation in relations:
            need(normal_form(relation) == {}, 'relations vanish in normal form')
        for triple in W:
            v = {triple: 1}
            nf = normal_form(v)
            need(set(nf) <= nonpivots, 'normal form uses retained basis')
            need(normal_form(nf) == nf, 'normal form idempotent')
            for relation in relations:
                need(normal_form(eadd(v, relation)) == nf, 'integral quotient consistency')
        rows.append({'g': g, 'W_rank': len(W), 'relations': len(relations), 'quotient_rank': len(nonpivots)})
    return {'rows': rows, 'arithmetic': 'exact integers, no floating point, no rational saturation',
            'scope': 'Finite genus checks; uniform realization and primitive quotient proofs are in AUDIT.md.',
            'genus_two_warning': 'g=2 row checks algebra only; Omori normal-generation input is g>=3.'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    result = {'status': 'PASS', 'free_group': free_group_checks(),
              'genus_two': genus_two_checks(), 'johnson_lattice': lattice_checks()}
    result['exact_checks'] = N_CHECKS
    inputs = [ROOT/'pass1_johnson_obstruction'/'PROOF.md',
              ROOT/'pass1_genus_two'/'GENUS_TWO_GENERATORS.md',
              ROOT/'pass1_constructive'/'CONSTRUCTIVE_JOHNSON_GENERATORS.md']
    result['input_sha256'] = {str(path.relative_to(ROOT)): digest(path) for path in inputs}
    result['checker_sha256'] = digest(Path(__file__).resolve())
    result['limitations'] = [
        'Does not prove Luft, Nielsen, Omori, or Johnson theorems.',
        'Does not certify geometric realization of a source figure.',
        'Does not prove the all-genus statements by finite enumeration.',
        'Does not resolve novelty or authorize publication.'
    ]
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
