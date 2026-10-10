#!/usr/bin/env python3
"""Check finite algebra underlying HU Lemmas 4.4--4.7.

This independently authored check does not compute L-groups, assembly maps,
SK1, GAP SmallGroup identifiers, or a manifold construction. It only checks
the class-two parity identities used in the specified local proof steps.
No third-party documents or extracted prose are required at runtime.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


# Central coordinates are x5, x6, x7, x8, encoded as four bits.
# These square and commutator values specify the elementary finite model.
SQUARES = (0b1011, 0b0011, 0b0001, 0b1000)
COMMUTATORS = {(0, 1): 1, (0, 2): 2, (0, 3): 8,
               (1, 2): 4, (1, 3): 0, (2, 3): 0}
KERNEL_GENERATOR = 0b1100  # x7*x8


def require(condition, message):
    """Keep audit failures active when Python is run with optimization."""
    if not condition:
        raise ValueError(message)


def bits(v):
    return tuple(x & 1 for x in v)


def commutator(a, b):
    """Alternating commutator form in the four central coordinates."""
    a, b = bits(a), bits(b)
    value = 0
    for (i, j), mask in COMMUTATORS.items():
        if (a[i] * b[j] + a[j] * b[i]) & 1:
            value ^= mask
    return value


def square(a):
    """Quadratic square map for an ordered product of the generators."""
    a = bits(a)
    value = 0
    for i, mask in enumerate(SQUARES):
        if a[i]:
            value ^= mask
    for (i, j), mask in COMMUTATORS.items():
        if a[i] * a[j]:
            value ^= mask
    return value


def quotient_central(c):
    """Reduce modulo <x7*x8>, retaining x5, x6, and x7 coordinates."""
    return (c & 3) | ((((c >> 2) ^ (c >> 3)) & 1) << 2)


def run():
    v = list(itertools.product(range(2), repeat=4))
    total = len(v) ** 2
    comm_bad = sum(commutator(a, b) == KERNEL_GENERATOR for a in v for b in v)
    inversion_bad = sum((commutator(a, b) ^ square(b)) == KERNEL_GENERATOR
                        for a in v for b in v)
    quadratic_identity = all(
        square(tuple(x ^ y for x, y in zip(a, b))) ==
        (square(a) ^ square(b) ^ commutator(a, b)) for a in v for b in v)
    # Also enumerate the exponents {0,1,2,3} used in the local source proof.
    w = list(itertools.product(range(4), repeat=4))
    mod4_comm_bad = sum(commutator(a, b) == KERNEL_GENERATOR for a in w for b in w)
    mod4_inversion_bad = sum((commutator(a, b) ^ square(b)) == KERNEL_GENERATOR
                             for a in w for b in w)
    radical = [a for a in v if all(quotient_central(commutator(a, b)) == 0 for b in v)]
    # Each pair records (conjugating element, element to be inverted).
    real_generators = [((0, 1, 1, 1), (1, 0, 0, 0)),
                       ((0, 1, 0, 1), (1, 1, 0, 0)),
                       ((0, 0, 1, 1), (1, 1, 1, 0)),
                       ((1, 0, 0, 0), (0, 0, 0, 1))]
    inversion_checks = [commutator(a, b) == square(b) for a, b in real_generators]
    span = {0}
    for _, b in real_generators:
        mask = sum(bit << i for i, bit in enumerate(b))
        span |= {c ^ mask for c in list(span)}
    # Sanity controls ensure that the predicates do detect nearby targets.
    controls = {
        "nonzero_commutator_detected": commutator((1, 0, 0, 0), (0, 1, 0, 0)) == 1,
        "nonzero_square_detected": square((0, 0, 0, 1)) == 8,
        "zero_square_detected": square((0, 0, 0, 0)) == 0,
    }
    require(quadratic_identity, "Quadratic polarization identity failed")
    require(comm_bad == inversion_bad == mod4_comm_bad == mod4_inversion_bad == 0,
            "A local obstruction equation has a counterexample")
    require(radical == [(0, 0, 0, 0)], "Quotient commutator radical is nontrivial")
    require(all(inversion_checks), "An inversion relation failed")
    require(len(span) == 16, "Inverse-conjugate classes do not span the abelianization")
    require(all(controls.values()), "A sanity control failed")
    return {
        "schema": "hu-local-parity-audit-v1",
        "source": "https://arxiv.org/pdf/2602.05003v1",
        "source_locations": ["Section 4b, pages 14-16", "Lemmas 4.4-4.7"],
        "status": "passed_local_finite_checks_only",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parity_pairs_per_obstruction": total,
        "lemma_4_4_counterexamples": comm_bad,
        "lemma_4_6_counterexamples": inversion_bad,
        "exponent_0_to_3_pairs_per_obstruction": len(w) ** 2,
        "lemma_4_4_exponent_counterexamples": mod4_comm_bad,
        "lemma_4_6_exponent_counterexamples": mod4_inversion_bad,
        "quadratic_identity_checks": total,
        "quadratic_identity_passed": quadratic_identity,
        "quotient_commutator_radical_size": len(radical),
        "central_quotient_elementary_abelian_rank": 4,
        "central_quotient_integral_H2_rank_from_exterior_square": 6,
        "lemma_4_7_inversion_relations_checked": len(inversion_checks),
        "lemma_4_7_inversion_relations_passed": all(inversion_checks),
        "lemma_4_7_abelianization_span_size": len(span),
        "sanity_controls": controls,
        "not_certified": ["SmallGroup identification", "Schur multiplier computation for G",
                          "SK1 computation", "L-theory", "assembly maps",
                          "full HU or KNV theorem", "manifold construction"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write deterministic result JSON")
    parser.add_argument("--check", type=Path, help="Compare against existing result JSON")
    args = parser.parse_args()
    result = run()
    if args.check:
        if json.loads(args.check.read_text()) != result:
            raise SystemExit("Stored parity results do not match the current script")
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
