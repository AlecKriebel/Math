#!/usr/bin/env python3
"""Independent finite diagnostics, not a proof of the universal theorem.

Only the Python standard library is used. Reads optional frozen inputs; writes
only JSON to stdout. All checks survive -O and -OO. Mutations are actual changes
to the tested data or algorithm and are expected to produce exit status 1.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import permutations
import json
from math import factorial, lcm
from pathlib import Path
import random
import sys


class AuditFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise AuditFailure(message)


def clean(chain):
    return {s: Q(a) for s, a in chain.items() if a}


def norm(chain):
    return sum((abs(a) for a in chain.values()), Q(0))


def face(chain, i):
    answer = defaultdict(Q)
    for s, a in chain.items():
        answer[s[:i] + s[i + 1:]] += a
    return clean(answer)


def boundary(chain):
    answer = defaultdict(Q)
    for s, a in chain.items():
        if len(s) <= 1:
            continue
        for i in range(len(s)):
            answer[s[:i] + s[i + 1:]] += (-1) ** i * a
    return clean(answer)


def parity(p):
    # Independent implementation: cycle decomposition, not inversion counting.
    seen = set()
    cycles = 0
    for start in range(len(p)):
        if start not in seen:
            cycles += 1
            cur = start
            while cur not in seen:
                seen.add(cur)
                cur = p[cur]
    return (-1) ** (len(p) - cycles)


def sym(chain, mutation="none"):
    answer = defaultdict(Q)
    for s, a in chain.items():
        for p in permutations(range(len(s))):
            sign = 1 if mutation == "unsigned_symmetrization" else parity(p)
            denominator = 1 if mutation == "omit_denominator" else factorial(len(s))
            answer[tuple(s[j] for j in p)] += a * Q(sign, denominator)
    return clean(answer)


def verify_chain_identities(chain, mutation="none"):
    require(not boundary(boundary(chain)), "boundary squared is nonzero")
    image = sym(chain, mutation)
    require(boundary(image) == sym(boundary(chain), mutation), "symmetrization is not a chain map")
    require(norm(image) <= norm(chain), "symmetrization increased the l1 norm")
    if chain:
        first = face(image, 0)
        for i in range(len(next(iter(chain)))):
            expected = clean({s: (-1) ** i * a for s, a in first.items()})
            require(face(image, i) == expected, "individual face relation failed")
    if not boundary(chain):
        for i in range(len(next(iter(chain), ()))):
            require(not face(image, i), "normalized cycle has nonzero individual face")
    return image


def realization_fixture(chain, mutation="none"):
    normalized = chain if mutation == "skip_symmetrization" else sym(chain)
    require(not boundary(normalized), "input to pairing is not a cycle")
    for i in range(4):
        require(not face(normalized, i), "same-index pairing requires each face operator to vanish")
    m = lcm(*(a.denominator for a in normalized.values()))
    copies = []
    for s, a in sorted(normalized.items()):
        count = m * a
        require(count.denominator == 1, "denominator does not clear coefficient")
        copies.extend([(s, 1 if count > 0 else -1)] * abs(count.numerator))
    require(copies, "empty fixture")
    pairs = []
    for i in range(4):
        buckets = defaultdict(lambda: {1: [], -1: []})
        for index, (s, sign) in enumerate(copies):
            buckets[s[:i] + s[i+1:]][sign].append(index)
        for sides in buckets.values():
            require(len(sides[1]) == len(sides[-1]), "unbalanced same-index face bucket")
            for a, b in zip(sides[1], sides[-1]):
                pairs.append((a, i, b, i, tuple((j, j) for j in range(4) if j != i)))
    if mutation == "drop_face_pair":
        pairs.pop()
    if mutation == "duplicate_face_pair":
        pairs.append(pairs[0])
    a, i, b, j, mapping = pairs[0]
    if mutation == "same_orientation_pair":
        copies[b] = (copies[b][0], copies[a][1])
    if mutation == "wrong_face_index":
        pairs[0] = (a, i, b, (j + 1) % 4, mapping)
    if mutation == "colour_identification":
        targets = [v for _, v in mapping]
        targets[0], targets[1] = targets[1], targets[0]
        pairs[0] = (a, i, b, j, tuple((u, v) for (u, _), v in zip(mapping, targets)))
    parent = list(range(4 * len(copies)))
    dual = [set() for _ in copies]
    used = Counter()

    def root(a):
        while parent[a] != a:
            a = parent[a]
        return a

    for a, i, b, j, mapping in pairs:
        require(i == j, "pairing changed omitted index")
        require(copies[a][1] * (-1)**i == -copies[b][1] * (-1)**j, "paired face orientations agree")
        require(copies[a][0][:i]+copies[a][0][i+1:] == copies[b][0][:j]+copies[b][0][j+1:], "paired singular face maps differ")
        require({u for u, _ in mapping} == set(range(4)) - {i}, "source gluing is not a face bijection")
        require({v for _, v in mapping} == set(range(4)) - {j}, "target gluing is not a face bijection")
        for u, v in mapping:
            require(u == v, "face gluing identifies different colours")
            parent[root(4*a+u)] = root(4*b+v)
        used[a, i] += 1
        used[b, j] += 1
        dual[a].add(b)
        dual[b].add(a)
    require(used == Counter({(a, i): 1 for a in range(len(copies)) for i in range(4)}), "face coverage is not exactly once")
    colours = defaultdict(set)
    for k in range(4 * len(copies)):
        colours[root(k)].add(k % 4)
    require(all(len(v) == 1 for v in colours.values()), "global colour collision")
    for a in range(len(copies)):
        require(len({root(4*a+i) for i in range(4)}) == 4, "vertices of one tetrahedron collapsed")
    unseen = set(range(len(copies)))
    sizes = []
    while unseen:
        stack = [unseen.pop()]
        component = []
        while stack:
            cur = stack.pop()
            component.append(cur)
            for nxt in dual[cur] & unseen:
                unseen.remove(nxt)
                stack.append(nxt)
        require(sum(copies[a][1] for a in component) == 0, "component is not balanced by orientation")
        require(len(component) % 2 == 0, "coloured closed component has odd top count")
        sizes.append(len(component))
    pushed = defaultdict(Q)
    for s, sign in copies:
        pushed[s] += sign
    require(clean(pushed) == clean({s: m*a for s, a in normalized.items()}), "fundamental chain pushforward mismatch")
    claimed_m = m + 1 if mutation == "denominator_mismatch" else m
    require(Q(len(copies), claimed_m) == norm(normalized), "normalized tetrahedron count mismatch")
    require(sum(sizes) == len(copies), "component counts do not add")
    # The following is arithmetic conditional on the cited topological theorem.
    for k, B in [(2, 1), (8, 3), (120, 17)]:
        d = Q(k * B, 2)
        q = (8 if mutation == "wrong_cover_ratio" else 4) * B
        require(q*k == 8*d, "Gaifullin tile identity mismatch")
        require(d/q == Q(k, 8), "cover/map degree ratio mismatch")
    require(Q(24, 8) / Q(1, 8) == 24, "factorial improvement mismatch")
    return {"tetrahedra": len(copies), "face_pairs": len(pairs), "denominator": m,
            "normalized_l1": str(norm(normalized)), "dual_component_sizes": sorted(sizes)}


def algebra_fixtures(mutation):
    # Z direct-sum Z/6: beta=(1,0), gamma=(1,1); their real images agree.
    t = 1 if mutation == "drop_torsion_multiplier" else 6
    require((t * 1) % 6 == 0, "rational equality did not clear integral torsion")
    # An affine rational family r1+2*r2=1 approximates any real solution.
    for denominator in (10, 100, 1000):
        r2 = Q(1414213562 * denominator // 10**9, denominator)
        r1 = 1 - 2*r2
        require(r1 + 2*r2 == 1, "rational affine approximation lost exact class")
        m = lcm(r1.denominator, r2.denominator)
        require((m*r1).denominator == (m*r2).denominator == 1, "affine coefficients did not clear")
    # Multiple components and different q's need separate coefficients, not a
    # tacit common map degree. Cost identity is homogeneous component by component.
    m = 7
    data = [(2, 4), (12, 20)]
    cost = sum(Q(k*q, 8)/(m*q) for k, q in data)
    require(cost == Q(sum(k for k, _ in data), 8*m), "disconnected cover cost mismatch")
    # Same kernel does not imply equality: p=|x|, G=2|x| is a countermodel.
    p, G = Q(1), Q(2)
    require(p < G, "positive comparison alone was treated as equality")
    # Scalar polar radii are 1 and 2; a manifold-bounded functional can have
    # the comparison bound without a unit bound. No actual topology inferred.
    require(G > p, "dual comparison was incorrectly collapsed to unit bound")


def verify_freeze(root):
    document = json.loads((root / "FREEZE.json").read_text())
    checked = []
    for item in document["files"]:
        name = item["name"]
        require(Path(name).name == name, "unsafe frozen filename")
        blob = (root / "authored" / name).read_bytes()
        require(len(blob) == item["bytes"], "frozen size mismatch: " + name)
        require(hashlib.sha256(blob).hexdigest() == item["sha256"], "frozen hash mismatch: " + name)
        checked.append(name)
    require(len(checked) == 7 and len(set(checked)) == 7, "unexpected frozen file set")
    return checked


MUTATIONS = ["unsigned_symmetrization", "omit_denominator", "skip_symmetrization",
             "same_orientation_pair", "wrong_face_index", "colour_identification",
             "drop_face_pair", "duplicate_face_pair", "denominator_mismatch",
             "wrong_cover_ratio", "drop_torsion_multiplier"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutation", choices=["none"] + MUTATIONS, default="none")
    parser.add_argument("--frozen-root", type=Path)
    args = parser.parse_args()
    randomizer = random.Random(30001812)
    checked = 0
    # Arbitrary affine chains include repeated vertices and cancellation.
    for dim in range(1, 6):
        for _ in range(8):
            chain = defaultdict(Q)
            for __ in range(12):
                s = tuple(randomizer.randrange(8) for ___ in range(dim+1))
                chain[s] += Q(randomizer.randint(-5, 5), randomizer.randint(1, 9))
            verify_chain_identities(clean(chain), args.mutation)
            verify_chain_identities(boundary(chain), args.mutation)
            checked += 2
    original = boundary({tuple(range(5)): Q(1)})
    fixture = realization_fixture(original, args.mutation)
    require(fixture["tetrahedra"] == 120 and fixture["face_pairs"] == 240, "boundary-of-4-simplex fixture mismatch")
    # Relabel into disjoint supports to force disconnected pairing components.
    doubled = dict(original)
    doubled.update({tuple(x+10 for x in s): a for s, a in original.items()})
    disconnected = realization_fixture(doubled)
    require(disconnected["tetrahedra"] == 240, "disconnected fixture count mismatch")
    require(len(disconnected["dual_component_sizes"]) >= 2, "disconnected fixture lost a component")
    algebra_fixtures(args.mutation)
    frozen = verify_freeze(args.frozen_root) if args.frozen_root else None
    return {"status": "PASS", "optimization": sys.flags.optimize, "mutation": args.mutation,
            "exact_chain_cases": checked, "primary_pairing": fixture,
            "disconnected_pairing": disconnected, "frozen_files_checked": frozen,
            "scope": "Finite algebra, orientation, colour, pairing, count and integrity checks only; not universal topological certification."}


if __name__ == "__main__":
    try:
        print(json.dumps(main(), indent=2, sort_keys=True))
    except (AuditFailure, OSError, ValueError, KeyError) as error:
        print(json.dumps({"status": "FAIL", "optimization": sys.flags.optimize,
                          "error": str(error)}, sort_keys=True))
        sys.exit(1)
