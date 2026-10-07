"""Checkable reference examples for established finite-field construction reductions.

This implements the degree-m*d lift (Shoup's construction consequence; the exact
lift is explicit in Rai2024 Algorithm2), and the odd-characteristic 2-power branch
of Shoup's prime-field construction.  It does NOT implement or certify a uniform
unconditional prime-field factorization algorithm.  Both reductions accept an
external prime-field split-root oracle through finite_fields.factor.  The main
examples use the toy exhaustive O(p) oracle, restricted to p=2,3,5.

For characteristic-two degrees 3 and 4, the example constructor is a fixed table
of independently Frobenius-checked polynomials.  It is a test fixture, not a
universal prescribed-degree construction algorithm.  The complete construction
proof and cost ledger are in agent_notes/construction_reduction.md.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Sequence
import argparse
import json

from finite_fields import (
    FiniteField, Polynomial, PrimeOracle, Statistics,
    exhaustive_prime_split_oracle, factor, irreducible,
    prime_polynomial_irreducible,
)


PrimeConstructor = Callable[[int, int], Sequence[int]]


def _valuation(n: int, r: int) -> int:
    if n < 1 or r < 2:
        raise ValueError("positive valuation input and r>=2 required")
    k = 0
    while n % r == 0:
        n //= r
        k += 1
    return k


def _substitute_power(f: Sequence[int], power: int) -> tuple[int, ...]:
    if power < 1:
        raise ValueError("positive substitution power required")
    result = [0] * ((len(f) - 1) * power + 1)
    for i, coefficient in enumerate(f):
        result[i * power] = coefficient
    return tuple(result)


def construct_odd_two_power(
    p: int, e: int, prime_oracle: PrimeOracle,
) -> tuple[int, ...]:
    """Conditional Shoup variant; promised odd prime p, numeric degree 2**e.

    Only valuation at the known prime 2 is used; p-1 and p*p-1 are not factored.
    A polynomial factorization is supplied by the independently implemented
    extension/fixed-algebra reduction and the caller's prime split-root oracle.
    The binomial 4|D exception is handled by the p mod4 branches.
    """
    if p < 3 or p % 2 == 0 or not isinstance(e, int) or e < 1:
        raise ValueError("promised odd prime and e>=1 required")
    K = FiniteField(p, (0, 1))
    if p % 4 == 1:
        current = (1, 1)  # Phi_2; root -1 has order2.
        k = _valuation(p - 1, 2)
        for _ in range(2, k + 1):
            factored = factor(K, K.poly(_substitute_power(current, 2)), prime_oracle)
            if any(len(g) != 2 or multiplicity != 1 for g, multiplicity in factored.factors):
                raise ArithmeticError("cyclotomic order did not give linear factors")
            first = min(g for g, _ in factored.factors)
            current = tuple(coefficient[0] for coefficient in first)
        result = _substitute_power(current, 2 ** e)
    else:
        current = (1, 0, 1)  # roots have order4 in F_(p^2).
        if e == 1:
            return current
        k = _valuation(p * p - 1, 2)
        for _ in range(3, k + 1):
            factored = factor(K, K.poly(_substitute_power(current, 2)), prime_oracle)
            if any(len(g) != 3 or multiplicity != 1 for g, multiplicity in factored.factors):
                raise ArithmeticError("cyclotomic order did not give quadratic factors")
            first = min(g for g, _ in factored.factors)
            current = tuple(coefficient[0] for coefficient in first)
        result = _substitute_power(current, 2 ** (e - 1))
    if len(result) - 1 != 2 ** e or not prime_polynomial_irreducible(p, result):
        raise ArithmeticError("constructed polynomial failed independent Frobenius check")
    return result


def lift_irreducible(
    K: FiniteField, degree: int, prime_constructor: PrimeConstructor,
    prime_oracle: PrimeOracle,
) -> Polynomial:
    """Conditional degree-product lift with explicit verification and tie breaking.

    The constructor callback must return a monic irreducible prime-field
    polynomial of numeric degree m*degree.  No complexity promise about an
    arbitrary callback is inferred.  Irreducibility is independently checked.
    """
    if not isinstance(degree, int) or isinstance(degree, bool) or degree < 1:
        raise ValueError("positive numeric output degree required")
    if degree == 1:
        return K.poly((0, 1))
    N = K.m * degree
    H = tuple(prime_constructor(K.p, N))
    if len(H) != N + 1 or H[-1] != 1:
        raise ArithmeticError("constructor returned incorrect degree or leading coefficient")
    if any(not isinstance(a, int) or not 0 <= a < K.p for a in H):
        raise ArithmeticError("constructor returned noncanonical coefficients")
    if not prime_polynomial_irreducible(K.p, H):
        raise ArithmeticError("constructor polynomial is reducible")
    lifted = K.poly(H)
    result = factor(K, lifted, prime_oracle)
    if (len(result.factors) != K.m
            or any(len(g) - 1 != degree or multiplicity != 1
                   for g, multiplicity in result.factors)):
        raise ArithmeticError("Frobenius-orbit degree-product assertion failed")
    if not result.verify(K, lifted):
        raise ArithmeticError("lifted factorization did not reconstruct")
    answer = min(g for g, _ in result.factors)
    if not irreducible(K, answer):
        raise ArithmeticError("selected output failed independent Frobenius check")
    return answer


def example_prime_constructor(p: int, degree: int) -> tuple[int, ...]:
    """Restricted test fixture; not a universal construction algorithm."""
    fixtures = {
        (2, 3): (1, 1, 0, 1),
        (2, 4): (1, 1, 0, 0, 1),
    }
    if (p, degree) in fixtures:
        return fixtures[p, degree]
    if p in (3, 5) and degree >= 2 and degree & (degree - 1) == 0:
        return construct_odd_two_power(
            p, degree.bit_length() - 1, exhaustive_prime_split_oracle,
        )
    raise ValueError("test constructor only supports the documented small examples")


def run_examples() -> dict:
    records = []
    cases = (
        ("characteristic two, nonprime base", 2, (1, 1, 1), 2),
        ("extension degree one", 2, (0, 1), 3),
        ("degree-one requested extension", 2, (1, 1, 1), 1),
        ("odd characteristic, p=3 mod4", 3, (1, 0, 1), 2),
        ("odd characteristic, p=1 mod4", 5, (2, 0, 1), 2),
        ("higher two-power output", 3, (1, 0, 1), 4),
    )
    for name, p, h, degree in cases:
        stats = Statistics()
        K = FiniteField(p, h, stats)
        output = lift_irreducible(K, degree, example_prime_constructor,
                                 exhaustive_prime_split_oracle)
        H = None if degree == 1 else example_prime_constructor(p, K.m * degree)
        records.append({
            "case": name, "p": p, "base_modulus": list(h), "m": K.m,
            "requested_degree": degree, "prime_polynomial": H,
            "output_coefficients": [list(a) for a in output],
            "independent_irreducibility_check": irreducible(K, output),
            "statistics": stats.as_dict(),
        })

    negative_checks = []
    K = FiniteField(2, (1, 1, 1))
    for name, callback in (
        ("wrong constructor degree", lambda p, n: (1, 1, 1)),
        ("reducible constructor output", lambda p, n: (1, 0, 0, 0, 1)),
    ):
        try:
            lift_irreducible(K, 2, callback, exhaustive_prime_split_oracle)
        except ArithmeticError as ex:
            negative_checks.append({"case": name, "rejected": True, "reason": str(ex)})
        else:
            raise AssertionError("bad constructor was not rejected")

    # An actual counterexample to the wrong blanket nonsquare/binomial rule.
    P = FiniteField(3, (0, 1))
    counterexample = P.poly((1, 0, 0, 0, 1))
    cfac = factor(P, counterexample, exhaustive_prime_split_oracle)
    if irreducible(P, counterexample) or not cfac.verify(P, counterexample):
        raise AssertionError("F3 binomial counterexample not reproduced")
    return {
        "scope": "conditional reductions with p=2,3,5 toy exhaustive oracle",
        "uniform_unconditional_prime_algorithm_implemented": False,
        "example_count": len(records), "examples": records,
        "negative_checks": negative_checks,
        "binomial_exception_counterexample": {
            "p": 3, "polynomial": [1, 0, 0, 0, 1],
            "factors": [[a[0] for a in g] for g, _ in cfac.factors],
            "verified": cfac.verify(P, counterexample),
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_examples()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "example_count": result["example_count"],
        "all_irreducibility_checks_passed": all(
            x["independent_irreducibility_check"] for x in result["examples"]),
        "negative_checks": result["negative_checks"],
        "binomial_exception_counterexample": result["binomial_exception_counterexample"],
        "output": str(args.output) if args.output else None,
    }, indent=2))
