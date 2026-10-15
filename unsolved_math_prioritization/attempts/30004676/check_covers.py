#!/usr/bin/env python3
"""Finite semantic diagnostics for PARTIAL.md, using only the standard library.

These toy domains are NOT KPU models. Covers are external finite subsets here.
The tests exercise the cover equalities and bounded-quantifier translation;
they do not prove internal cover existence, Sigma definability or the conjecture.
"""

from itertools import product
import hashlib
import json
from pathlib import Path


COUNTS = {}


def require(category, condition):
    if not condition:
        raise AssertionError(category)
    COUNTS[category] = COUNTS.get(category, 0) + 1


def subsets(n):
    return [tuple(i for i in range(n) if mask & (1 << i))
            for mask in range(1 << n)]


def images(cover):
    # Each target b has two distinct representatives 2*b and 2*b+1.
    return {x // 2 for x in cover}


def main():
    for n in range(1, 5):
        target_subsets = subsets(n)
        covers = subsets(2 * n)
        for target in target_subsets:
            good = [c for c in covers if images(c) == set(target)]
            require("nonempty_cover_family", bool(good))
            # There are three nonempty choices of representatives per member.
            require("cover_family_cardinality", len(good) == 3 ** len(target))
            for c in good:
                require("exact_image", images(c) == set(target))
                for truth_set in target_subsets:
                    truth = set(truth_set)
                    require("bounded_exists",
                            any(b in truth for b in target)
                            == any(x // 2 in truth for x in c))
                    require("bounded_forall",
                            all(b in truth for b in target)
                            == all(x // 2 in truth for x in c))
                    require("negated_atom_forall",
                            all(b not in truth for b in target)
                            == all(x // 2 not in truth for x in c))
            for x, z in product(range(2 * n), repeat=2):
                require("quotient_equality", (x // 2 == z // 2)
                        == any(x in (2*b, 2*b+1) and z in (2*b, 2*b+1)
                               for b in range(n)))

    # Every acyclic membership relation on three ordered points; all binary
    # predicate tables. This tests nested bounds with a fresh cover each time.
    n = 3
    possible_edges = [(x, y) for y in range(n) for x in range(y)]
    covers = subsets(2 * n)
    for edge_mask in range(1 << len(possible_edges)):
        members = {y: {x for i, (x, y0) in enumerate(possible_edges)
                       if y0 == y and edge_mask & (1 << i)}
                   for y in range(n)}
        family = {y: [c for c in covers if images(c) == members[y]]
                  for y in range(n)}
        for pred_mask in range(1 << (n * n)):
            pred = lambda x, p: bool(pred_mask & (1 << (x*n+p)))
            for y, p in product(range(n), repeat=2):
                # forall x in y exists z in x R(z,p)
                b_value = all(any(pred(z, p) for z in members[x])
                              for x in members[y])
                a_value = any(all(any(any(pred(z // 2, p) for z in inner)
                                     for inner in family[x // 2])
                                  for x in outer)
                              for outer in family[y])
                require("nested_forall_exists", a_value == b_value)
                # exists x in y forall z in x not R(z,p)
                b_value = any(all(not pred(z, p) for z in members[x])
                              for x in members[y])
                a_value = any(any(any(all(not pred(z // 2, p) for z in inner)
                                     for inner in family[x // 2])
                                  for x in outer)
                              for outer in family[y])
                require("nested_exists_forall_negated", a_value == b_value)

    # Explicit negative controls: incomplete coverage, excess elements,
    # absent totality, and confusing representative identity with equality.
    require("reject_missing_member",
            all(x // 2 != 1 for x in (0,)) != all(b != 1 for b in (0, 1)))
    require("reject_extra_member",
            all(x // 2 == 0 for x in (0, 2)) != all(b == 0 for b in (0,)))
    require("reject_empty_cover_family",
            any(all(True for _ in c) for c in []) != all([]))
    require("reject_literal_equality", (0 == 1) != (0 // 2 == 1 // 2))

    root = Path(__file__).resolve().parent
    digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    proof_digest = hashlib.sha256((root / "PARTIAL.md").read_bytes()).hexdigest()
    out = {
        "status": "PASS",
        "diagnostic_assertions": sum(COUNTS.values()),
        "categories": COUNTS,
        "script_sha256": digest,
        "proof_sha256": proof_digest,
        "meaning": "Finite cover-translation and rejection controls only",
        "not_verified": ["KPU models", "Sigma definability of covers",
                         "internal set existence", "original conjecture"],
        "external_packages": [],
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
