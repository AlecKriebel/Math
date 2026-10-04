#!/usr/bin/env python3
"""Small exact controls only; these do not prove the entire-function target."""
from fractions import Fraction
import json


def compositions(n):
    if n == 0:
        yield ()
    else:
        for first in range(1, n + 1):
            for rest in compositions(n - first):
                yield (first,) + rest


def orbits(n, permutations):
    unseen = set(range(n))
    answer = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        todo = [seed]
        while todo:
            x = todo.pop()
            for p in permutations:
                y = p[x]
                if y not in orbit:
                    orbit.add(y)
                    todo.append(y)
        unseen -= orbit
        answer.append(sorted(orbit))
    return answer


def main():
    checks = 0
    budget_cases = 0
    for n in range(1, 13):
        for degrees in compositions(n):
            ramification = sum(d - 1 for d in degrees)
            assert ramification == n - len(degrees)
            assert (ramification == n - 1) == (len(degrees) == 1)
            budget_cases += 1
            checks += 2
    # These permutations encode the standard cyclic cover z -> z^n.
    cyclic = []
    for n in range(2, 17):
        cycle = tuple((i + 1) % n for i in range(n))
        with_branch_loop = orbits(n, [cycle])
        without_branch_loop = orbits(n, [])
        assert len(with_branch_loop) == 1
        assert len(without_branch_loop) == n
        checks += 2
        cyclic.append({"degree": n, "with_loop_orbits": len(with_branch_loop),
                       "without_loop_orbits": len(without_branch_loop)})
    # A three-sheet tree model: dropping one required edge leaves two orbits.
    p = (1, 0, 2)
    q = (0, 2, 1)
    assert len(orbits(3, [p, q])) == 1
    assert len(orbits(3, [p])) == len(orbits(3, [q])) == 2
    checks += 2
    # All points 1/j belong to 0<|z|<1; their omitted limit is 0.
    # Finite tests are controls, not a proof that any f realises this singular set.
    closure_control = []
    for n in (2, 3, 10, 100, 1000):
        values = [Fraction(1, j) for j in range(2, n + 1)]
        assert all(0 < x < 1 for x in values)
        assert min(values) == Fraction(1, n)
        checks += 2
        closure_control.append({"last_index": n, "minimum": str(min(values))})
    # Compactness does not imply one Jordan subdomain can contain a set:
    # the unit circle lies in 1/2<|z|<2 while its winding around 0 is one.
    annulus_inner, circle_radius, annulus_outer = Fraction(1, 2), 1, 2
    assert annulus_inner < circle_radius < annulus_outer
    checks += 1
    return {
        "status": "passed",
        "checks": checks,
        "degree_compositions": budget_cases,
        "cyclic_cover_controls": cyclic,
        "closure_controls": closure_control,
        "claims_certified": "finite arithmetic and permutation-orbit controls only",
        "target_resolution": False,
        "analytic_proof_location": "RESULT.md"
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
