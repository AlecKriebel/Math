#!/usr/bin/env python3
"""Independent exact finite-moment and staged synthetic-port checks.

No manuscript verifier or generated certificate is imported.  Rational linear
algebra and explicit independent routing implement the checks.  The finite
fixtures are regression evidence, not a proof of the universal graph theorem.
"""

import itertools
import json
from fractions import Fraction as F


COUNTS = {"moment_fixtures": 0, "boundary_fixtures": 0, "predicates": 0}


def require(condition, message):
    COUNTS["predicates"] += 1
    if not condition:
        raise RuntimeError(message)


def determinant(matrix):
    a = [list(row) for row in matrix]
    result = F(1)
    for c in range(len(a)):
        pivot = next((r for r in range(c, len(a)) if a[r][c]), None)
        if pivot is None:
            return F(0)
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]
            result = -result
        p = a[c][c]
        result *= p
        for r in range(c + 1, len(a)):
            factor = a[r][c] / p
            for j in range(c + 1, len(a)):
                a[r][j] -= factor * a[c][j]
    return result


def solve(matrix, vector):
    a = [list(row) + [b] for row, b in zip(matrix, vector)]
    for c in range(len(a)):
        pivot = next(r for r in range(c, len(a)) if a[r][c])
        a[c], a[pivot] = a[pivot], a[c]
        p = a[c][c]
        a[c] = [x / p for x in a[c]]
        for r in range(len(a)):
            if r != c:
                factor = a[r][c]
                a[r] = [x - factor * y for x, y in zip(a[r], a[c])]
    return [row[-1] for row in a]


def decode(atoms):
    combined = {}
    for weight, rate in atoms:
        if weight and rate:
            combined[rate] = combined.get(rate, F(0)) + weight
    r = len(combined)
    m = {k: sum((w * rate**k for rate, w in combined.items()), F(0))
         for k in range(1, 2 * r + 3)}
    if r == 0:
        require(m[1] == 0, "zero-atom moment")
        return F(0)
    h = lambda size: [[m[i + j + 2] for j in range(size)]
                      for i in range(size)]
    for size in range(1, r + 1):
        require(determinant(h(size)) > 0, "positive shifted-Hankel minor")
    require(determinant(h(r + 1)) == 0, "exact count singularity")
    v = [m[i + 1] for i in range(r)]
    value = sum((x * y for x, y in zip(v, solve(h(r), v))), F(0))
    require(value == sum(combined.values(), F(0)), "decoded positive mass")
    return value


def moment_checks():
    for r in range(7):
        for repeated in (False, True):
            atoms = [(F(j + 1, 200), F(j + 1, j + 2)) for j in range(r)]
            if repeated and r:
                atoms += [(F(1, 300), atoms[0][1])]
            atoms += [(F(1, 9), F(0))]
            value = decode(atoms)
            require(value == sum((w for w, rate in atoms if rate), F(0)),
                    "constant separated mass must be excluded")
            COUNTS["moment_fixtures"] += 1


def pair_mass(states, i, j):
    return sum((weight for weight, population in states
                if population[i] == population[j]), F(0))


def moment_mass(states, i, j, rates):
    return decode([(weight, rates[population[i]])
                   for weight, population in states
                   if population[i] == population[j]])


def port_checks():
    # Child labels denote arriving blocks, including a nonsingleton block.
    # u,v have independent side ports; z arrives at a later parental port.
    for n in range(2, 6):
        for gamma in (F(1, 2), F(1, 3), F(2, 5)):
            for equal_rates in (False, True):
                child = ["{a1,a2}"] + ["{b%d}" % i for i in range(1, n)]
                labels = child + ["u", "v", "z"]
                before_map = {x: "C" for x in child}
                before_map.update({"u": "U", "v": "V", "z": "Z_wait"})
                before = [(F(1), before_map)]
                after = []
                for choices in itertools.product(("P", "Q"), repeat=n):
                    weight = F(1)
                    population = dict(before_map)
                    for label, target in zip(child, choices):
                        weight *= gamma if target == "P" else 1 - gamma
                        population[label] = target
                    # An unrelated ordinary event at exactly the routing age.
                    population["u"] = population["v"] = "D"
                    after.append((weight, population))
                require(sum(w for w, _ in after) == 1, "routing total")
                rates = {p: F(1) for p in ("C", "U", "V", "Z_wait", "P", "Q", "D")}
                if not equal_rates:
                    rates["P"], rates["Q"], rates["D"] = F(2), F(3), F(5)
                negative = set()
                for i, j in itertools.combinations(labels, 2):
                    q0 = moment_mass(before, i, j, rates)
                    q1 = moment_mass(after, i, j, rates)
                    require(q0 == pair_mass(before, i, j), "raw left occupancy")
                    require(q1 == pair_mass(after, i, j), "raw right occupancy")
                    if q1 < q0:
                        negative.add((i, j))
                    if i in child and j in child:
                        require(q1 - q0 == -2 * gamma * (1 - gamma), "child split mass")
                require(negative == set(itertools.combinations(child, 2)),
                        "negative clique includes block labels, not side ports")
                require(pair_mass(after, "u", "v") == 1, "simultaneous positive jump")
                # A later synthetic-port injection cannot invent a negative jump.
                injected = [(w, dict(pop, z="P")) for w, pop in after]
                for i, j in itertools.combinations(labels, 2):
                    require(pair_mass(injected, i, j) >= pair_mass(after, i, j),
                            "isolated placeholder injection is nonnegative")
                require(pair_mass(injected, child[0], "z") == gamma,
                        "private parent entry recovers oriented route weight")
                COUNTS["boundary_fixtures"] += 1
    # The pair's own finite-survival mass scales both one-sided atom measures.
    for gamma in (F(1, 2), F(1, 3), F(2, 5)):
        survival = F(1, 8)
        left = decode([(survival, F(1))])
        right = decode([(survival * gamma**2, F(2)),
                        (survival * (1 - gamma)**2, F(3))])
        require(right - left == -2 * gamma * (1 - gamma) * survival,
                "unnormalized pair survival scaling")


if __name__ == "__main__":
    moment_checks()
    port_checks()
    print(json.dumps({"status": "PASS", "claim_nodes": ["NMSA-011"],
                      "checks": COUNTS,
                      "limits": "Finite exact regression evidence; universal conclusions use the independent proof review."},
                     indent=2, sort_keys=True))
