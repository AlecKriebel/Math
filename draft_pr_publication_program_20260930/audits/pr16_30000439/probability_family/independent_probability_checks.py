#!/usr/bin/env python3
"""Independent exact probes, not a proof of imported geometric theorems.

This file imports no candidate/reviewer code. Outputs are written only beside it.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent
checks = []
mutations = []

def require(name, predicate):
    if not predicate:
        raise AssertionError(name)
    checks.append(name)

def reject(name, predicate, reason):
    require("mutation rejected: " + name, not predicate)
    mutations.append({"mutation": name, "rejected": True, "reason": reason})

# A different parameterization derives each enormous integer from one fourth root.
root = 2**64
n, m = root**4, root**5
p = Q(1, root**6)
M = comb(n, 3)
c = Q(1, 645120)
a = c*c/2
W = Q(comb(n, 7), n-6) - m*M
require("double count identity", Q(comb(n, 7), n-6) == Q(comb(n, 6), 7))
require("coarse six-set bound", comb(n, 6) >= Q((n//2)**6, 720))
require("deletion threshold", n**7 >= 107520**4)
require("uniform surviving witnesses", W >= c*n**6)
require("atomic probability exponent", p*p == Q(1, n**3))
mu_lower = W*p*p
denominator = Q(M*(M-1), 2)*p*p + M*(M-1)*(M-2)*p**3
require("candidate denominator bounds stronger denominator", denominator <= n**4*root**2)
require("rate constant", a > Q(1, 2**41))
require("candidate exponent lower bound", a*root**6 > 2**343)
entropy_upper = m + 256*(20*n + 3*m) # log(m+1)<=m; log(n)<256.
require("candidate entropy bound", entropy_upper < 770*m + 5120*n < 2**331)
net = mu_lower**2/(2*denominator) - entropy_upper
require("exact rate dominates entropy", net > 2**342)
robust_failure = 1/(1+net) # e^(-net) <= 1/(1+net).
require("robust finite failure below eighth", robust_failure < Q(1, 8))
collision_mean = comb(n, 2)*comb(n-2, 2)*p*p
lambda_ = M*p
require("conflict mean upper bound", collision_mean <= Q(n, 4))
require("finite Markov bound", collision_mean/m <= Q(1, 2**66))
require("finite triangle mean", lambda_ > 2**379)
require("finite Chebyshev bound", 4/lambda_ < Q(1, 2**377))
require("nonplanar retained count", lambda_/2-m > n)
combined = robust_failure + collision_mean/m + 4/lambda_
require("joint finite positive probability", combined < 1)
require("displayed three failure bounds below one", Q(1, 8)+Q(1, 2**66)+Q(1, 2**377) < 1)

# Derive the feasible exponent region, rather than merely reusing the numbers.
def exponent_conditions(alpha, beta):
    return {
        "many triangles beyond order-type entropy": 3-alpha > 1,
        "conflict budget with vanishing Markov bound": beta > 4-2*alpha,
        "deletion entropy below Janson rate": beta < 3-alpha,
        "deletion removes negligible potential witnesses": beta < 3,
        "retained triangle mean dominates budget": beta < 3-alpha,
    }

require("candidate exponents satisfy all strict margins",
        all(exponent_conditions(Q(3, 2), Q(5, 4)).values()))
require("deletion entropy need not dominate placement entropy",
        all(exponent_conditions(Q(7, 4), Q(3, 4)).values()))
for alpha, beta, label in [
    (Q(1), Q(5, 4), "p=n^-1"),
    (Q(2), Q(5, 4), "p=n^-2"),
    (Q(5, 4), Q(5, 4), "p=n^-5/4"),
    (Q(3, 2), Q(3, 2), "m=n^3/2"),
]:
    bad = [name for name, ok in exponent_conditions(alpha, beta).items() if not ok]
    reject(label, not bad, "; ".join(bad))
reject("p=n^-7/4 with unchanged budget passes finite retention",
       M*Q(1, root**7)/2-m > n,
       "Expected triangle count has the same exponent as m and smaller coefficient.")

# Exact determinant elimination determines circuits without assuming alternation.
def determinant(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    answer = Q(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            answer = -answer
        value = a[j][j]
        answer *= value
        for i in range(j+1, len(a)):
            multiplier = a[i][j]/value
            for k in range(j+1, len(a)):
                a[i][k] -= multiplier*a[j][k]
            a[i][j] = 0
    return answer

def circuit(points, six):
    columns = [(1,)+tuple(points[v]) for v in six]
    coeffs = []
    for j in range(6):
        matrix = [[columns[k][i] for k in range(6) if k != j] for i in range(5)]
        coeffs.append((-1)**j*determinant(matrix))
    require("circuit all minors nonzero", all(coeffs))
    for i in range(5):
        require("exact affine circuit identity", sum(coeffs[j]*columns[j][i] for j in range(6)) == 0)
    plus = tuple(v for v, coeff in zip(six, coeffs) if coeff > 0)
    minus = tuple(v for v, coeff in zip(six, coeffs) if coeff < 0)
    return frozenset((plus, minus))

points = {v: (v, v*v, v**3, v**4) for v in range(8)}
witnesses = []
for six in combinations(range(8), 6):
    pair = circuit(points, six)
    require("moment curve circuit balanced", all(len(tri) == 3 for tri in pair))
    witnesses.append(pair)
require("moment curve distinct witness count", len(set(witnesses)) == comb(8, 6))
for seven in combinations(range(8), 7):
    require("balanced witness in seven vertices", any(set().union(*map(set, w)) <= set(seven) for w in witnesses))
triangles = list(combinations(range(8), 3))
degrees = {tri: sum(tri in w for w in witnesses) for tri in triangles}
ordered = sum(bool(w & z) for w in witnesses for z in witnesses if w != z)
unordered = sum(bool(w & z) for w, z in combinations(witnesses, 2))
require("ordered dependencies exactly degree double count", ordered == sum(d*(d-1) for d in degrees.values()))
require("ordered dependencies exactly twice unordered", ordered == 2*unordered == 144)
require("ordered dependency upper bound", ordered <= len(triangles)**3)
reject("replace ordered dependence count by unordered without compensation", ordered == unordered,
       "The exact ordered coefficient is 144; unordered is 72.")

# Additional placements use exact integer coordinates, not moment-curve assumptions.
rng = random.Random(16030000439)
random_placements = 0
for trial in range(12):
    while True:
        pts = {v: tuple(rng.randrange(-100, 101) for _ in range(4)) for v in range(7)}
        if all(determinant([[((1,)+pts[v])[i] for v in five] for i in range(5)])
               for five in combinations(range(7), 5)):
            break
    pairs = [circuit(pts, six) for six in combinations(range(7), 6)]
    require("random GP seven-set balanced circuit", any(all(len(s) == 3 for s in pair) for pair in pairs))
    random_placements += 1

# Exact support calculations isolate geometric overlap from Bernoulli overlap.
q = Q(1, 3)
def event_probability(supports):
    return q**len(set().union(*map(set, supports)))
A = ((0, 1, 2), (3, 4, 5))
B = ((0, 1, 3), (2, 4, 5)) # Cross-pair edge overlap, four distinct triangles.
C = ((0, 1, 2), (3, 4, 6)) # One identical atomic triangle.
require("edge overlap does not cause dependence", event_probability([A, B]) == event_probability([A])*event_probability([B]))
require("shared triangle joint expectation", event_probability([A, C]) == q**3)
reject("shared triangle indicators use p^4", event_probability([A, C]) == q**4,
       "The union has three atomic triangles, so the joint expectation is p^3.")
single_witness_failure = 1-q*q
require("single-witness no-hit probability is positive", single_witness_failure > 0)
reject("omit diagonal contribution in a single-witness Janson denominator", single_witness_failure <= 0,
       "A single witness has Delta_distinct=0. A zero-denominator exponent would claim no-hit probability 0, but it equals 8/9.")

# Exhaust all samples for ten triangles on five vertices. Check cleaning and moments.
small_triangles = list(combinations(range(5), 3))
conflicts = [(i, j) for i, j in combinations(range(10), 2)
             if len(set(small_triangles[i]) & set(small_triangles[j])) == 2]
require("edge conflict combinatorial count", len(conflicts) == comb(5, 2)*comb(3, 2))
EB = ET = ET2 = Q(0)
for bits in product((0, 1), repeat=10):
    present = {i for i, b in enumerate(bits) if b}
    offending = [(i, j) for i, j in conflicts if i in present and j in present]
    F = {min(i, j) for i, j in offending}
    require("cleaning deletion count bounded by conflicts", len(F) <= len(offending))
    remaining = present-F
    require("cleaning hits every offending pair", all(not {i, j} <= remaining for i, j in conflicts))
    edges = {edge for i in remaining for edge in combinations(small_triangles[i], 2)}
    require("retained edge count is three times triangle count", len(edges) == 3*len(remaining))
    count = len(present)
    mass = q**count*(1-q)**(10-count)
    EB += len(offending)*mass
    ET += count*mass
    ET2 += count*count*mass
require("exhaustive conflict mean", EB == comb(5, 2)*comb(3, 2)*q*q)
require("exhaustive triangle mean", ET == 10*q)
require("exhaustive binomial variance", ET2-ET*ET == 10*q*(1-q))
require("variance bounded by mean", ET2-ET*ET <= ET)
reject("binomial variance equals mean", ET2-ET*ET == ET,
       "For nonzero p, Var(T)=Mp(1-p), strictly below Mp.")

# An exact small example falsifies treating fixed deletions as adaptive deletions.
matching = [{0, 1}, {2, 3}]
all_deletions = [set()] + [{i} for i in range(4)]
fixed_failure = adaptive_failure = Q(0)
for bits in product((0, 1), repeat=4):
    present = {i for i, b in enumerate(bits) if b}
    mass = Q(1, 16)
    no_witness = lambda F: not any(e <= present-F for e in matching)
    fixed_failure += mass*no_witness({0})
    any_F = any(no_witness(F) for F in all_deletions)
    selected_F = any(no_witness(F) for F in all_deletions if F <= present)
    require("deletions outside sample irrelevant", any_F == selected_F)
    adaptive_failure += mass*any_F
require("fixed-deletion toy failure", fixed_failure == Q(3, 4))
require("adaptive-deletion toy failure", adaptive_failure == Q(15, 16))
reject("drop union over deletion sets", fixed_failure == adaptive_failure,
       "Matching toy model: fixed failure=3/4, adaptive failure=15/16.")

result = {
    "status": "PASS",
    "exact_assertions": len(checks),
    "parameters": {"n": "2^256", "p": "2^-384", "m": "2^320"},
    "finite_combined_failure_below_one": combined < 1,
    "finite_failure_upper_bound_coarse": "1/8 + 2^-66 + 2^-377 < 1",
    "moment_curve": {"vertices": 8, "balanced_witnesses": len(witnesses), "ordered_dependencies": ordered},
    "extra_exact_GP_placements": random_placements,
    "exhaustive_cleaning_samples": 2**10,
    "mutations_rejected": mutations,
    "scope": "Exact finite arithmetic, circuit consistency, exhaustive small support and cleaning checks. These do not prove the imported geometric or probability theorems, enumerate the enormous construction, certify PL inflation, or establish novelty.",
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(HERE/'independent_probability_receipt.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
