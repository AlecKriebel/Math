#!/usr/bin/env python3
"""Cross-check distinct direct and trace reductions against trial division.

The complete enumeration is finite TEST CODE ONLY. It supplies no asymptotic
prime-field factorization theorem. Uses independent reduction and arithmetic
modules, and a third algorithm that enumerates all monic possible divisors.
"""
import argparse
import hashlib
import itertools
import json
import platform
import time
from pathlib import Path

import extension_direct_verify as direct
import finite_fields as trace


def elements(F):
    return list(itertools.product(range(F.p), repeat=F.m))


def exhaustive_trial_division(F, f):
    """Small-instance independent comparator, no Frobenius linear algebra."""
    n = len(f) - 1
    remainder = list(f)
    found = []
    alphabet = elements(F)
    for degree in range(1, n // 2 + 1):
        for coefficients in itertools.product(alphabet, repeat=degree):
            g = list(coefficients) + [F.one]
            exponent = 0
            while len(remainder) >= len(g):
                q, r = direct.divmod_poly(F, remainder, g)
                if r:
                    break
                exponent += 1
                remainder = q
            if exponent:
                found.append((g, exponent))
    if len(remainder) > 1:
        found.append((remainder, 1))
    return sorted((tuple(g), exponent) for g, exponent in found)


def run():
    started = time.perf_counter()
    parameter_sets = [(2, [0, 1], 4), (3, [0, 1], 3), (5, [0, 1], 2),
                      (2, [1, 1, 1], 3), (2, [1, 1, 0, 1], 2),
                      (3, [1, 0, 1], 2)]
    rows, total = [], 0
    for p, h, maxdegree in parameter_sets:
        F = direct.Field(p, h)
        K = trace.FiniteField(p, h)
        alphabet = elements(F)
        count = 0
        for degree in range(1, maxdegree + 1):
            for coefficients in itertools.product(alphabet, repeat=degree):
                f = list(coefficients) + [F.one]
                expected = exhaustive_trial_division(F, f)
                answer = direct.factor(F, f, direct.small_prime_oracle)
                actual = sorted((tuple(g), exponent) for g, exponent in answer["factors"])
                trace_answer = trace.factor(K, tuple(f), trace.exhaustive_prime_split_oracle)
                if actual != expected or list(trace_answer.factors) != expected:
                    raise AssertionError({"p": p, "h": h, "f": f,
                                          "direct": actual, "trace": trace_answer.factors,
                                          "trial_division": expected})
                if answer["scalar"] != F.one or trace_answer.unit != K.one:
                    raise AssertionError("Scalar mismatch")
                count += 1
        rows.append({"p": p, "h": h, "extension_degree": F.m,
                     "all_monic_degrees": [1, maxdegree], "cases": count})
        total += count
    # All field values in F_8 give eight simultaneous linear factors and an
    # eight-dimensional p-fixed algebra, exercising many same-coordinate values.
    F = direct.Field(2, [1, 1, 0, 1])
    K = trace.FiniteField(2, [1, 1, 0, 1])
    expected = sorted(((F.neg(a), F.one), 1) for a in elements(F))
    f = direct.product_poly(F, [list(g) for g, _ in expected])
    actual = direct.factor(F, f, direct.small_prime_oracle)
    trace_answer = trace.factor(K, tuple(f), trace.exhaustive_prime_split_oracle)
    if sorted((tuple(g), e) for g, e in actual["factors"]) != expected:
        raise AssertionError("F_8 all-values direct case")
    if list(trace_answer.factors) != expected:
        raise AssertionError("F_8 all-values trace case")
    total += 1
    hashes = {}
    for name in ["extension_crosscheck.py", "extension_direct_verify.py", "finite_fields.py"]:
        hashes[name] = hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
    return {"status": "pass", "total_cases": total,
            "comparison": "direct p-fixed reduction = trace reduction = exhaustive trial division",
            "exhaustive_family_results": rows,
            "additional_case": "F_8 polynomial with all eight distinct field roots",
            "additional_case_diagnostics": actual["trace"],
            "python": platform.python_version(), "source_sha256": hashes,
            "elapsed_seconds": round(time.perf_counter() - started, 6),
            "scope": "Small-field mechanics only; prime oracles enumerate p and remain test fixtures"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    data = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(data)
    print(data, end="")
