#!/usr/bin/env python3
"""Independent exact controls and nonmutating replay for the scoped audit.

Run from any directory. Only audit/audit_verification.json is written here;
the author's verifier is run on a temporary copy. No finite control below
purports to prove an unrestricted mathematical assertion.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent / 'packet'
EXPECTED = {
    'ATTEMPTS.md': 'ce64163ad1dd5d72dfc53ac53d27181202c4ac9c03cb40948f25bcf5e8d16a65',
    'PROOF.md': '12bae950ee014a78e2b374c741abcd3355cb9c6894e9e277908bd44fa6fd4430',
    'README.md': '1076869e7d8a6ed0fad1bc7a2632bc8e834f62dfc50244fe981099e5ec96edab',
    'SOURCES.md': 'e423f6cf1e8a8fbfd6dc840bb35f2bc4b34ee67bfc2f90b3282120b06491d57c',
    'verification.json': '08c3b370edf2f36975996015e15d818669322286deb9a462fb17a7f041af8915',
    'verify.py': '0f08290a42336313d93b2839c79ac6f30c9cb4eb44ae31671179cb7024e60006',
}
counts = Counter()

def check(label, proposition):
    counts[label] += 1
    if not proposition:
        raise AssertionError(f'{label}: control {counts[label]} failed')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for name, expected in EXPECTED.items():
    check('frozen_hashes_before', digest(PACKET / name) == expected)

# Run exactly the frozen verifier without allowing its output to overwrite
# the frozen record. The subprocess is ordinary local, standard-library code.
with tempfile.TemporaryDirectory(prefix='polynomial-audit-') as temporary:
    target = Path(temporary) / 'verify.py'
    target.write_bytes((PACKET / 'verify.py').read_bytes())
    replay = subprocess.run([sys.executable, str(target)], capture_output=True,
                            text=True, check=True)
    replay_bytes = target.with_name('verification.json').read_bytes()
    replay_result = json.loads(replay_bytes)
    check('author_replay', replay_result['status'] == 'PASS')
    check('author_replay', replay_result['exact_assertions'] == 8850)
    check('author_replay', replay_bytes == (PACKET / 'verification.json').read_bytes())
    check('author_replay', json.loads(replay.stdout) == replay_result)

# Recompute each Fourier quotient from a closed finite product, rather than
# importing the author's recurrence or functions.
def fourier(a, k):
    out = Q((-1) ** k)
    for j in range(k):
        out *= (a - j) / (a + j + 1)
    return out

def kernel(a, degree):
    return [fourier(a, k) for k in range(degree + 1)]

def energy(p, r):
    return sum(Q(p[i] * p[j]) * r[abs(i-j)]
               for i in range(len(p)) for j in range(len(p)))

def difference(p):
    return [p[0]] + [p[j]-p[j-1] for j in range(1, len(p))] + [-p[-1]]

def step_norm(p, k):
    return sum((
        (p[j+k] if 0 <= j+k < len(p) else 0) -
        (p[j] if 0 <= j < len(p) else 0)
    ) ** 2 for j in range(-k, len(p)))

def interval_energy(n, a):
    return n + 2*sum((n-k)*fourier(a, k) for k in range(1, n))

def half_integer_fourier(m, k):
    # Independent rational closed form for a=m+1/2.
    numerator = (-1)**(m+1) * math.prod(range(1, 2*m+2, 2))**2
    denominator = math.prod(4*k*k - j*j for j in range(1, 2*m+2, 2))
    return Q(numerator, denominator)

for m in range(7):
    for k in range(45):
        check('half_integer_closed_forms',
              fourier(Q(2*m+1, 2), k) == half_integer_fourier(m, k))

alphas = (Q(1, 10), Q(1, 3), Q(1, 2), Q(9, 10))
for a in alphas:
    r = kernel(a, 65)
    for n in range(65):
        check('exact_tail_identity',
              1 + 2*sum(r[1:n+1]) == -(n+a+1)*r[n+1]/a)
    for p in product(range(-3, 4), repeat=4):
        if not any(p):
            continue
        e = energy(p, r)
        norm = sum(x*x for x in p)
        # Tail is handled exactly, rather than cutting off an infinite sum.
        tail = -(3+a+1)*r[4] / (2*a)
        discrete = sum(-r[k]*step_norm(p, k) for k in range(1, 4)) + 2*norm*tail
        check('signed_energy_and_equality', e == discrete)
        check('signed_energy_and_equality', e >= 1)
        check('signed_energy_and_equality', (e == 1) == (norm == 1))
        for k in range(1, 6):
            check('integer_chain_norms', step_norm(p, k) >= 2)
        q = difference(p)
        eq = energy(q, r)
        A, B = [max(x, 0) for x in q], [max(-x, 0) for x in q]
        check('zero_sum_strict_separation', eq > energy(A, r) + energy(B, r))
        check('zero_sum_strict_separation', eq > 2)
        check('fractional_factorization',
              eq == Q(2*(2*a+1), a+1)*energy(p, kernel(a+1, len(p)-1)))
    for p in product(range(5), repeat=4):
        if not any(p):
            continue
        check('nonnegative_mass_rearrangement',
              energy(p, r) >= interval_energy(sum(p), a))
    for n in range(1, 33):
        check('interval_increments',
              interval_energy(n+1, a)-interval_energy(n, a) ==
              -(n+a+1)*r[n+1]/a)
        check('interval_increments', interval_energy(n+1, a) > interval_energy(n, a))
        check('geometric_sum_formula',
              Q(2*(2*a+1), a+1)*energy([1]*n, kernel(a+1, n-1)) == 2*(1-r[n]))
    for n in range(2, 25):
        q = [0]*(2*n+2)
        q[0], q[n], q[n+1], q[2*n+1] = 1, -1, -1, 1
        check('cluster_formula', energy(q, r) == 4-4*r[n]-4*r[n+1]+2*r[2*n+1]+2*r[1])
        check('cluster_formula', energy(q, r) > Q(2*(a+2), a+1))

# Integer Parseval and mass constraints over a wider coefficient alphabet.
for m in range(1, 9):
    for p in product(range(-2, 3), repeat=3):
        if not any(p):
            continue
        q = list(p)
        for _ in range(m):
            q = difference(q)
        norm = sum(x*x for x in q)
        mass = sum(x for x in q if x > 0)
        check('integer_mass_and_parseval', sum(q) == 0)
        check('integer_mass_and_parseval', mass >= m)
        check('integer_mass_and_parseval', norm >= 2*m and norm % 2 == 0)
        check('integer_mass_and_parseval',
              norm == math.comb(2*m, m)*energy(p, kernel(Q(m), len(p)-1)))
        for t in range(m):
            check('integer_moment_constraints', sum(v*j**t for j, v in enumerate(q)) == 0)

# Check witnesses via subset enumeration instead of polynomial convolution.
# Recover the quotient by exact successive synthetic divisions at z=1.
factors = ((1,), (1,2), (1,2,3), (1,2,3,5), (1,2,3,5,7), (1,2,3,4,5,7))
witnesses = []
for m, ds in enumerate(factors, 1):
    terms = Counter()
    for number in range(m+1):
        for subset in combinations(range(m), number):
            terms[sum(ds[j] for j in subset)] += (-1)**number
    terms = {k:v for k,v in terms.items() if v}
    positive = sorted(k for k,v in terms.items() if v > 0)
    negative = sorted(k for k,v in terms.items() if v < 0)
    check('subset_witnesses', set(terms.values()) <= {-1, 1})
    check('subset_witnesses', len(positive) == len(negative) == m)
    for t in range(m):
        check('subset_witnesses', sum(x**t for x in positive) == sum(x**t for x in negative))
    check('subset_witnesses', sum(x**m for x in positive) != sum(x**m for x in negative))
    q = [(-1)**m*terms.get(j, 0) for j in range(max(terms)+1)]
    for _ in range(m):
        out = [0]*(len(q)-1)
        out[-1] = q[-1]
        for j in range(len(out)-1, 0, -1):
            out[j-1] = q[j] + out[j]
        check('synthetic_division', q[0] == -out[0])
        q = out
    check('synthetic_division', q[-1] == 1)
    check('synthetic_division', q == replay_result['integer_witnesses'][m-1]['P_coefficients'])
    check('synthetic_division', math.comb(2*m, m)*energy(q, kernel(Q(m), len(q)-1)) == 2*m)
    witnesses.append({'m':m, 'positive_exponents':positive, 'negative_exponents':negative,
                      'energy':2*m, 'quotient_coefficients':q})

# A repeated-term ideal PTE solution is insufficient for squared-norm equality.
X, Y = (0, 3, 3), (1, 1, 4)
for t in range(3):
    check('repeated_term_negative_control', sum(x**t for x in X) == sum(y**t for y in Y))
q = [Counter(X)[j]-Counter(Y)[j] for j in range(5)]
check('repeated_term_negative_control', sum(x*x for x in q) == 10 > 6)

for name, expected in EXPECTED.items():
    check('frozen_hashes_after', digest(PACKET / name) == expected)
result = {
    'status':'PASS',
    'author_replay':{'exact_assertions':8850, 'byte_identical_output':True,
                     'frozen_inputs_unchanged':True},
    'independent_exact_assertions':sum(counts.values())-counts['author_replay'],
    'control_counts':dict(sorted(counts.items())),
    'integer_witnesses':witnesses,
    'limitations':'Finite controls only. Universal inequalities, convergence, infimum limits, nonattainment, and the integer existence equivalence are assessed analytically in AUDIT.md.',
}
text = json.dumps(result, indent=2, sort_keys=True)+'\n'
(HERE / 'audit_verification.json').write_text(text)
print(text)
