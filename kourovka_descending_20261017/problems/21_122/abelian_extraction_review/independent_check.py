"""Independent finite tests of delta1; stdlib only, no full 21.122 claim.

Use explicit group multiplication and repeated powers, quotient cocycle
enumeration, all central-coordinate lifts in a small stage, and the p=2
boundary. The infinite statement is proved in REVIEW.md, not certified by
these finite tests.
"""

from datetime import datetime, timezone
from itertools import product
from math import comb
import json


class Stage:
    def __init__(self, p, n):
        self.p, self.n = p, n
        self.pairs = tuple((i, j) for i in range(n) for j in range(i + 1, n))
        self.zero = ((0,) * n, (0,) * len(self.pairs))

    def beta(self, a, b):
        p = self.p
        return tuple(((a[i] % p) * (b[j] % p)) % p for i, j in self.pairs)

    def mul(self, x, y):
        p = self.p
        a, c = x
        b, d = y
        return (
            tuple((a[i] + b[i]) % (p * p) for i in range(self.n)),
            tuple((c[k] + d[k] + q) % p for k, q in enumerate(self.beta(a, b))),
        )

    def inverse(self, x):
        a, c = x
        return (
            tuple(-u % (self.p * self.p) for u in a),
            tuple((-c[k] + q) % self.p for k, q in enumerate(self.beta(a, a))),
        )

    def power(self, x, m):
        answer = self.zero
        for _ in range(m):
            answer = self.mul(answer, x)
        return answer

    def formula(self, x, m):
        a, c = x
        return (
            tuple(m * u % (self.p * self.p) for u in a),
            tuple((m * c[k] + comb(m, 2) * q) % self.p
                  for k, q in enumerate(self.beta(a, a))),
        )

    def elements(self):
        for a in product(range(self.p * self.p), repeat=self.n):
            for c in product(range(self.p), repeat=len(self.pairs)):
                yield (a, c)


def quotient_tests(p, n):
    group = Stage(p, n)
    vectors = tuple(product(range(p), repeat=n))
    pairs_checked = triples_checked = 0
    for a in vectors:
        for b in vectors:
            ba, ab = group.beta(b, a), group.beta(a, b)
            minors_vanish = all(x == y for x, y in zip(ab, ba))
            dependent = not any(a) or any(
                all(b[i] == t * a[i] % p for i in range(n)) for t in range(p)
            )
            assert minors_vanish == dependent
            pairs_checked += 1
            for c in vectors:
                apb = tuple((a[i] + b[i]) % p for i in range(n))
                bpc = tuple((b[i] + c[i]) % p for i in range(n))
                left = tuple((u + v) % p for u, v in zip(ab, group.beta(apb, c)))
                right = tuple((u + v) % p for u, v in zip(group.beta(b, c), group.beta(a, bpc)))
                assert left == right
                triples_checked += 1
    return {"p": p, "n": n, "commuting_quotient_pairs": pairs_checked,
            "cocycle_triples": triples_checked}


def power_image_tests(p, n):
    group = Stage(p, n)
    outputs = set()
    checked = 0
    for a in product(range(p * p), repeat=n):
        x = (a, (0,) * len(group.pairs))
        actual = group.power(x, p)
        expected = (tuple(p * (u % p) for u in a), (0,) * len(group.pairs))
        assert actual == expected
        outputs.add(actual)
        checked += 1
    assert len(outputs) == p ** n
    return {"p": p, "n": n, "central_zero_representatives_checked": checked,
            "power_image_size": len(outputs)}


def all_lifts_small_stage():
    group = Stage(3, 2)
    elements = tuple(group.elements())
    all_powers = {x: group.power(x, 3) for x in elements}
    for x in elements:
        assert group.mul(group.inverse(x), x) == group.zero
        assert group.mul(x, group.inverse(x)) == group.zero
        for m in range(10):
            assert group.power(x, m) == group.formula(x, m)
        assert group.power(x, 9) == group.zero
    commuting_pair_count = 0
    homomorphism_pair_count = 0
    for x in elements:
        for y in elements:
            xy = group.mul(x, y)
            yx = group.mul(y, x)
            assert all_powers[xy] == group.mul(all_powers[x], all_powers[y])
            homomorphism_pair_count += 1
            a, _ = x
            b, _ = y
            expected_commutator = (
                (0, 0),
                tuple((u - v) % 3 for u, v in zip(group.beta(a, b), group.beta(b, a))),
            )
            actual_commutator = group.mul(
                group.mul(group.mul(group.inverse(x), group.inverse(y)), x), y
            )
            assert actual_commutator == expected_commutator
            if xy == yx:
                commuting_pair_count += 1
    # Every subgroup with one-dimensional mod-p image is contained in
    # one of these complete line preimages. Check them without subgroup
    # enumeration; each complete preimage is itself abelian.
    line_vectors = ((1, 0), (1, 1), (1, 2), (0, 1))
    line_results = []
    for v in line_vectors:
        reductions = {tuple(t * u % 3 for u in v) for t in range(3)}
        preimage = tuple(x for x in elements if tuple(u % 3 for u in x[0]) in reductions)
        for x in preimage:
            for y in preimage:
                assert group.mul(x, y) == group.mul(y, x)
        images = {all_powers[x] for x in preimage}
        assert len(images) == 3
        line_results.append({"line_generator": v, "preimage_order": len(preimage),
                             "power_image_size": len(images)})
    central = tuple(x for x in elements if all(group.mul(x, y) == group.mul(y, x) for y in elements))
    assert len(central) == 27
    assert all(not any(u % 3 for u in x[0]) for x in central)
    e1, e2 = ((1, 0), (0,)), ((0, 1), (0,))
    assert group.mul(e1, e2) != group.mul(e2, e1)
    return {"p": 3, "n": 2, "group_order": len(elements),
            "center_order": len(central), "power_image_size": len(set(all_powers.values())),
            "commuting_pairs": commuting_pair_count,
            "power_homomorphism_pairs": homomorphism_pair_count,
            "exact_nilpotency_class": 2, "line_preimages": line_results}


def even_prime_boundary():
    group = Stage(2, 2)
    x = ((1, 1), (0,))
    square = group.power(x, 2)
    assert square == ((2, 2), (1,))
    assert square != ((2, 2), (0,))
    e1, e2 = ((1, 0), (0,)), ((0, 1), (0,))
    assert group.power(group.mul(e1, e2), 2) != group.mul(group.power(e1, 2), group.power(e2, 2))
    return {"p": 2, "n": 2, "test_element": x, "actual_square": square,
            "claimed_odd_prime_simplification_fails": True,
            "square_map_is_not_a_homomorphism": True}


def main():
    quotient = [quotient_tests(p, n) for p, n in ((3, 2), (3, 3), (5, 2), (7, 2))]
    images = [power_image_tests(p, n)
              for p, max_n in ((3, 5), (5, 3), (7, 2))
              for n in range(1, max_n + 1)]
    return {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "status": "passed", "full_21_122_resolution_estimate_percent": 0,
            "solves_21_122": False, "quotient_checks": quotient,
            "power_image_checks": images, "all_lifts_small_stage": all_lifts_small_stage(),
            "even_prime_boundary": even_prime_boundary(),
            "limits": "Finite checks support the explicit algebra only; infinite continuity, cardinality, and the abstract abelian-subgroup bound require the proof in REVIEW.md."}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
