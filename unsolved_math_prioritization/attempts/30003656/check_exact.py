#!/usr/bin/env python3
"""Finite sanity checks, not a replacement for the unbounded proofs in PROOF.md."""
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path

MAX_N = 4  # A_n = {0,...,n}, distinguished point 0


def category(injective):
    result = {}
    for n in range(MAX_N + 1):
        result[n] = []
        for m in range(MAX_N + 1):
            for tail in product(range(m + 1), repeat=n):
                f = (0,) + tail
                if not injective or len(set(f)) == len(f):
                    result[n].append((m, f))
    return result


EQ = ("eq",)
NE = ("not", EQ)
NNE = ("not", NE)
BETA = ("all", NNE)
ALPHA = ("not", BETA)
EXTRA = ("exists", NE)
DEC = ("all", ("or", EQ, NE))


def run_forcing(injective):
    arrows = category(injective)

    @lru_cache(None)
    def forces(formula, n, env=()):
        op = formula[0]
        if op == "eq":
            return env[-1] == 0
        if op == "not":
            return all(not forces(formula[1], m, tuple(f[a] for a in env))
                       for m, f in arrows[n])
        if op == "all":
            return all(forces(formula[1], m, tuple(f[a] for a in env) + (b,))
                       for m, f in arrows[n] for b in range(m + 1))
        if op == "exists":
            return any(forces(formula[1], n, env + (b,)) for b in range(n + 1))
        if op == "or":
            return forces(formula[1], n, env) or forces(formula[2], n, env)
        raise ValueError(op)

    rows = []
    for n in range(MAX_N + 1):
        for a in range(n + 1):
            assert forces(NE, n, (a,)) == (a != 0 if injective else False)
            assert forces(NNE, n, (a,)) == (a == 0 if injective else True)
        row = {"stage_n": n, "beta": forces(BETA, n), "alpha": forces(ALPHA, n),
               "exists_nonbasepoint": forces(EXTRA, n), "decidable_basepoint": forces(DEC, n)}
        assert row["beta"] is (not injective)
        assert row["alpha"] is injective
        assert row["exists_nonbasepoint"] == (injective and n > 0)
        assert row["decidable_basepoint"] is injective
        rows.append(row)
    return {"arrows": sum(map(len, arrows.values())), "objects": MAX_N + 1,
            "rows": rows, "forcing_cache_entries": forces.cache_info().currsize}


def quotient_checks():
    # Terms are c,x1,x2,x3. For each finite equality premise E, verify that
    # equivalence closure exactly matches its consequences in small pointed sets.
    terms = 4
    pairs = list(combinations(range(terms), 2))
    premises = assignments = comparisons = 0
    for bits in product((False, True), repeat=len(pairs)):
        E = [p for p, use in zip(pairs, bits) if use]
        p = list(range(terms))

        def root(a):
            while p[a] != a:
                a = p[a]
            return a

        for a, b in E:
            p[root(a)] = root(b)
        relation = {(a, b): root(a) == root(b) for a in range(terms) for b in range(terms)}
        valid = []
        for size in range(1, terms + 1):
            for tail in product(range(size), repeat=terms - 1):
                v = (0,) + tail
                if all(v[a] == v[b] for a, b in E):
                    valid.append(v)
                    assignments += 1
        for pair, entailed in relation.items():
            a, b = pair
            assert all(v[a] == v[b] for v in valid) == entailed
            comparisons += 1
        # Construct Q explicitly, with the c-class numbered 0.
        reps = [root(0)] + [r for r in sorted({root(a) for a in range(terms)}) if r != root(0)]
        q = tuple(reps.index(root(a)) for a in range(terms))
        assert q[0] == 0
        assert all((q[a] == q[b]) == relation[a, b] for a in range(terms) for b in range(terms))
        premises += 1
    return {"terms": terms, "premise_sets": premises, "satisfying_assignments": assignments,
            "atomic_consequence_comparisons": comparisons}


def main():
    result = {"status": "PASS", "purpose": "finite sanity checks only",
              "max_nonbasepoint_elements": MAX_N,
              "all_pointed_maps": run_forcing(False),
              "pointed_injections": run_forcing(True), "equality_quotients": quotient_checks()}
    target = Path(__file__).with_name("exact_results.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
