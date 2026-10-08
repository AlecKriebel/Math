#!/usr/bin/env python3
"""Independent rational linear-algebra audit; imports no candidate/audit checker.
Uses a full kernel presentation of the Meyer form, including its radical.
Requires SymPy, and writes only JSON to stdout.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as S

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--packet', type=Path, required=True, help='Path to the frozen candidate packet')
PACKET = parser.parse_args().packet.resolve()
I = S.eye(2)
J = S.Matrix([[0, 1], [-1, 0]])
GEN = {1: S.Matrix([[1, 0], [-1, 1]]), 2: S.Matrix([[1, 1], [0, 1]])}
GEN.update({-x: M.inv() for x, M in list(GEN.items())})

def require(condition, message):
    if not condition:
        raise ValueError(message)

def inverse(w):
    return [-x for x in reversed(w)]

def commutator(u, v):
    return u + v + inverse(u) + inverse(v)

def cancel(w):
    answer = []
    for x in w:
        if answer and answer[-1] == -x:
            answer.pop()
        else:
            answer.append(x)
    return answer

def inertia(M):
    require(M == M.T, 'nonsymmetric form')
    coeffs = list(M.charpoly().all_coeffs())
    zero = 0
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()
        zero += 1
    degree = len(coeffs) - 1
    def variations(c):
        signs = [S.sign(x) for x in c if x != 0]
        return sum(x != y for x, y in zip(signs, signs[1:]))
    pos = variations(coeffs)
    neg = variations([x * (-1)**(degree - i) for i, x in enumerate(coeffs)])
    require(pos + neg + zero == M.rows, 'Descartes counts not exhaustive')
    return [pos, neg, zero]

def meyer(A, B):
    # Kernel vectors are pairs (v1,v2) with e=(A^-1-I)v1=(I-B)v2.
    left, right = A.inv() - I, I - B
    basis = (left.row_join(-right)).nullspace()
    if not basis:
        return 0
    K = S.Matrix.hstack(*basis)
    V1, V2 = K[:2, :], K[2:, :]
    E = left * V1
    Q = (V1 + V2).T * J * E
    require(Q == Q.T, 'Meyer pullback is not symmetric')
    # Kernel(E) must be radical; only E's image carries the Meyer form.
    for z in E.nullspace():
        require(Q * z == S.zeros(Q.rows, 1), 'fiber not in Meyer radical')
    p, n, _ = inertia(Q)
    return p - n

def signature(w):
    A = I
    terms = []
    for x in w:
        terms.append(meyer(A, GEN[x]))
        A = A * GEN[x]
    return -sum(terms), terms, A

def goeritz(powers):
    AA, BB = powers[::2], powers[1::2]
    N = sum(abs(x) for x in BB)
    require(N >= 3, 'small cyclic matrix excluded')
    edge_signs = [S.sign(x) for x in BB for _ in range(abs(x))]
    G = S.zeros(N)
    for i, sign in enumerate(edge_signs):
        G[i, i] = -edge_signs[i-1] - sign
        j = (i + 1) % N
        G[i, j] = G[j, i] = sign
    start = 0
    for a, b in zip(AA, BB):
        G[start, start] += a
        start += abs(b)
    p, n, z = inertia(G)
    return p - n - sum(AA), G, [p, n, z]

def expand(powers):
    return [int(S.sign(v))*(1+i%2) for i, v in enumerate(powers) for _ in range(abs(v))]

a, b = [1,1], [2,2]
c = commutator(a,b)
d, e = inverse(a)+c+a, inverse(b)+c+b
word = cancel(commutator(commutator(c,d), commutator(d,e)))
cert = json.loads((PACKET/'certificate.json').read_text())
require(word == cert['word'], 'exact nested expression mismatch')
require(expand(cert['syllables']) == word, 'syllable expansion mismatch')
sig, terms, burau = signature(word)
require(sig == -2 and terms == cert['meyer_terms'], 'Meyer target mismatch')
require(list(burau) == cert['burau_matrix'], 'Burau mismatch')
gsig, G, gi = goeritz(cert['syllables'])
require(gsig == sig and G.tolist() == cert['goeritz'], 'Goeritz target mismatch')
require(gi == [23,25,0] and G.det() == -7154819319988224, 'Goeritz invariants')

controls = []
def control(label, w, expected):
    got, _, _ = signature(w)
    require(got == expected, label)
    controls.append({'name': label, 'signature': got})
control('identity', [], 0)
for k in range(1, 7):
    control('positive_two_strand_torus_' + str(k), [1]*k, 1-k)
    control('negative_two_strand_torus_' + str(k), [-1]*k, k-1)
control('central_delta_fourth', [1,2]*6, -8)
control('target_inverse', inverse(word), 2)
control('target_mirror', [-x for x in word], 2)
control('target_generator_exchange', [int(S.sign(x))*(3-abs(x)) for x in word], -2)
control('target_square', word*2, -4)
control('target_conjugate', [1,2,1]+word+[-1,-2,-1], -2)
control('target_inverse_pair_inserted', word[:19]+[-2,2]+word[19:], -2)
for offset in [1,2,19,51,103]:
    control('target_cyclic_shift_'+str(offset), word[offset:]+word[:offset], -2)
for pre, post in [([],[]), (word[:17],word[17:]), ([-1,2,1],[2,-1]), ([1,1],[-2,-2])]:
    left, right = pre+[1,2,1]+post, pre+[2,1,2]+post
    sl, _, ml = signature(left)
    sr, _, mr = signature(right)
    require(sl == sr and ml == mr, 'Artin relation control')
    controls.append({'name':'Artin_relation_'+str(len(controls)), 'signature':sl})

# Adversarially varied signs, exponents, and singular forms in a separate comparison.
comparisons = 0
singular_comparisons = 0
for powers in itertools.product((-2,-1,1,2), repeat=4):
    if sum(abs(x) for x in powers[1::2]) < 3:
        continue
    sg, gg, ig = goeritz(powers)
    sm, _, _ = signature(expand(powers))
    require(sm == sg, 'Goeritz/Meyer comparison '+str(powers))
    comparisons += 1
    singular_comparisons += bool(ig[2])

# Check the full, not generator-specialized, cocycle on representative products.
mats = [I, GEN[1], GEN[-2], GEN[1]*GEN[2], GEN[1]**2*GEN[2]**-2, burau]
cocycles = 0
for A, B, C in itertools.product(mats, repeat=3):
    require(meyer(A,B)+meyer(A*B,C) == meyer(B,C)+meyer(A,B*C), 'Meyer cocycle identity')
    cocycles += 1
print(json.dumps({
    'status':'PASS_RECOVERED_INDEPENDENT_CONTROLS',
    'method':'Exact kernel-pullback Meyer form with explicit fiber-radical checks; characteristic-polynomial inertia',
    'python_version':__import__('sys').version.split()[0],
    'sympy_version':S.__version__,
    'proof_sha256':hashlib.sha256((PACKET/'PROOF.md').read_bytes()).hexdigest(),
    'manifest_sha256':hashlib.sha256((PACKET/'MANIFEST.json').read_bytes()).hexdigest(),
    'word_length':len(word), 'goeritz_inertia':gi,
    'goeritz_determinant':int(G.det()), 'signature':sig,
    'meyer_term_counts':{str(x):terms.count(x) for x in (-1,0,1)},
    'meyer_terms':terms, 'burau_matrix':list(map(int,burau)),
    'target_and_normalization_controls':controls,
    'independent_goeritz_meyer_comparisons':comparisons,
    'singular_goeritz_comparisons':singular_comparisons,
    'full_meyer_cocycle_controls':cocycles
}, indent=2))
