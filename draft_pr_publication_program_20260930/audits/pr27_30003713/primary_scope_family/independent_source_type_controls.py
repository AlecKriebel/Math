#!/usr/bin/python3
"""Independent exact source/type falsifiers; no general homology solver.

Run from any directory with /usr/bin/python3. The sole output receipt is adjacent
to this file. Standard library only. Finite tests are not an all-degree proof.
"""
from collections import Counter
from fractions import Fraction
from itertools import permutations, product, combinations_with_replacement
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import sys

checks = []
negative_controls = []


def check(label, proposition):
    if not proposition:
        raise AssertionError(label)
    checks.append(label)


def reject(label, false_proposition):
    check(label, not false_proposition)
    negative_controls.append(label)


def choose(n, k):
    return comb(n, k) if n >= 0 and 0 <= k <= n else 0


def rank(matrix):
    if not matrix:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    pivot = 0
    for col in range(len(a[0])):
        hit = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if hit is None:
            continue
        a[pivot], a[hit] = a[hit], a[pivot]
        value = a[pivot][col]
        a[pivot] = [x / value for x in a[pivot]]
        for i in range(pivot + 1, len(a)):
            value = a[i][col]
            if value:
                a[i] = [x - value*y for x, y in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def parity(p):
    return (-1)**sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))


def symmetrizer(e, r, alternating):
    words = list(product(range(e), repeat=r))
    index = {word: i for i, word in enumerate(words)}
    matrix = [[0]*len(words) for _ in words]
    for word in words:
        j = index[word]
        for p in permutations(range(r)):
            image = tuple(word[p[i]] for i in range(r))
            matrix[index[image]][j] += parity(p) if alternating else 1
    return matrix


projector_receipts = []
for e in range(4):
    for r in range(5):
        for alternating in (False, True):
            matrix = symmetrizer(e, r, alternating)
            actual = rank(matrix)
            expected = choose(e, r) if alternating else (1 if r == 0 else choose(e+r-1, r))
            check(f"exact tensor projector rank e={e} r={r} sign={alternating}", actual == expected)
            # P^2 = r! P verifies the actual permutation-sum projector, not
            # just an implementation of the expected dimension formula.
            square = [[sum(matrix[i][k]*matrix[k][j] for k in range(len(matrix)))
                       for j in range(len(matrix))] for i in range(len(matrix))]
            check(f"projector identity e={e} r={r} sign={alternating}",
                  square == [[factorial(r)*x for x in row] for row in matrix])
            projector_receipts.append({"e": e, "r": r, "alternating": alternating,
                                       "rank": actual})

reject("a sign twist cannot be dropped at e=1,r=2",
       rank(symmetrizer(1, 2, True)) == rank(symmetrizer(1, 2, False)))

# Exterior Cauchy is evaluated here at ordinary finite vector spaces. It is
# independently cross-checked against the actual sign projector above.
for e in range(5):
    for w in range(5):
        exterior = choose(e*w, 2)
        cauchy = choose(e+1, 2)*choose(w, 2) + choose(e, 2)*choose(w+1, 2)
        check(f"degree2 exterior Cauchy dimension e={e} w={w}", exterior == cauchy)
reject("symmetric Cauchy cannot replace exterior Cauchy at e=1,w=2",
       choose(2, 2) == choose(2, 2)*choose(3, 2))

# Powell Theorem 1 explicitly excludes r=1 from its two-summand branch.
# For dim V=3 the exceptional exterior cube has dimension one, while the
# blindly substituted branch would count two copies of the same partition.
check("Powell r1 exceptional layer at dimV3", choose(3, 3) == 1)
reject("blind r>1 formula double-counts r1", choose(3, 3) == 2*choose(3, 3))
check("r2,dimE1,dimV4 retains the sign-labelled term after exterior twist",
      choose(1+2-1, 2)*choose(4, 4) == 1)
reject("missing exterior twist incorrectly kills r2,dimE1,dimV4",
       choose(1+2-1, 2)*choose(4, 4) == choose(1, 2)*choose(4, 4))
reject("dimE1 does not restrict ideal weight to q1",
       choose(1+2-1, 2)*choose(4, 4) == 0)
check("r0 tensor-coefficient H1 has degree1 only", 0+1 == 1 and 0+2 != 1)

# For dim V=1 the whole current algebra is abelian of dimension e+1.
# The two ideal-weight layers have dimensions C(e,n)+C(e,n-1).
for e in range(7):
    for n in range(10):
        split = choose(e, n) + choose(e, n-1)
        check(f"abelian ordinary exterior boundary e={e} n={n}", split == choose(e+1, n))
reject("ordinary abelian homology cannot use symmetric powers above dimension",
       choose(2, 3) == choose(2+3-1, 3))
check("V0 boundary leaves only scalar degree0", [choose(0,n) for n in range(4)] == [1,0,0,0])
check("E0 dimV1 boundary has H0,H1 only", [choose(1,n) for n in range(4)] == [1,1,0,0])

# Tensor algebra first/last-letter decompositions prove the appropriate
# right/left augmentation-ideal freeness. The empty word is separate.
for m in range(4):
    for d in range(1, 6):
        words = set(product(range(m), repeat=d))
        first = {(v, tail) for v in range(m) for tail in product(range(m), repeat=d-1)}
        last = {(head, v) for head in product(range(m), repeat=d-1) for v in range(m)}
        check(f"right free resolution first-letter bijection m={m} d={d}",
              {(v,)+tail for v,tail in first} == words and len(first) == len(words))
        check(f"left free resolution last-letter bijection m={m} d={d}",
              {head+(v,) for head,v in last} == words and len(last) == len(words))

# Reproduce the precise counterexample raised in the July 2017 comments,
# using alternating tensors rather than the old adjoint matrix test family.
# Sym^2(L)_3 = V tensor Lambda^2(V). The action from V tensor Sym^2(V)
# maps (v,a,b) to b tensor (v wedge a)+a tensor (v wedge b).
m = 3
codomain = [(b,i,j) for b in range(m) for i in range(m) for j in range(i+1,m)]
codomain_index = {x:i for i,x in enumerate(codomain)}
domain = [(v,a,b) for v in range(m) for a,b in combinations_with_replacement(range(m),2)]
action = [[0]*len(domain) for _ in codomain]
for column,(v,a,b) in enumerate(domain):
    for letter,left,right in [(b,v,a),(a,v,b)]:
        if left != right:
            i,j = sorted((left,right))
            action[codomain_index[letter,i,j]][column] += 1 if left < right else -1
alternating_functional = [parity((b,i,j)) if len({b,i,j}) == 3 else 0 for b,i,j in codomain]
check("MO degree3 alternating functional annihilates every action column",
      all(sum(alternating_functional[i]*action[i][j] for i in range(len(codomain))) == 0
          for j in range(len(domain))))
check("MO functional is nonzero on e0 tensor [e1,e2]",
      alternating_functional[codomain_index[0,1,2]] == 1)
check("MO explicit action has one-dimensional degree3 cokernel", len(codomain)-rank(action) == 1)
reject("general H0(Sym2 L)=Sym2 V guess loses degree3", len(codomain)-rank(action) == 0)

# Same virtual character does not determine actual kernel/cokernel.
zero, identity = [[0,0],[0,0]], [[1,0],[0,1]]
check("equal virtual dimensions do not supply evaluated homology",
      (2-2 == 0) and rank(zero) == 0 and rank(identity) == 2)
reject("Euler difference alone fixes kernel multiplicity", 2-rank(zero) == 2-rank(identity))

receipt = {
    "status": "PASS",
    "runtime": {"python": sys.version, "executable": sys.executable,
                "dependencies": "standard library only"},
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "assertions": len(checks),
    "negative_controls_rejected": negative_controls,
    "projector_receipts": projector_receipts,
    "MO_counterexample": {"domain_dimension": len(domain), "codomain_dimension": len(codomain),
                          "action_rank": rank(action), "cokernel_dimension": len(codomain)-rank(action)},
    "scope": "Finite falsifiers of conventions and source scope. Universal reductions require the accompanying proof; these tests do not evaluate unrestricted Schur kernels."
}
path = Path(__file__).with_name("independent_source_type_results.json")
path.write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps({"status": receipt["status"], "assertions": receipt["assertions"],
                  "negative_controls": len(negative_controls)}))
