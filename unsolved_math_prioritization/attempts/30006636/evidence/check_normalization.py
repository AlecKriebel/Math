#!/usr/bin/env python3
"""Exact independent finite checks for the trisection normalization audit.

These checks supplement the mathematical arguments in AUDIT.md. They do not
certify topology, categorical coherence, or the cited general MMT theorem.
No floating-point cube roots and no third-party source text are used.
"""

from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path
import argparse
import os
import sys


MUTANT = None

def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def require_readonly():
    require(os.getuid() != 0 and os.geteuid() != 0, "read-only verification requires a real nonroot process")
    source = Path(__file__).resolve()
    require(not os.access(source, os.W_OK), "checker input is writable")
    require(not os.access(source.parent, os.W_OK), "checker input directory is writable")
    probe = source.parent / (".audit-write-probe-" + str(os.getpid()))
    try:
        with probe.open("x"):
            pass
    except PermissionError:
        return
    else:
        probe.unlink()
        raise RuntimeError("actual input-directory write probe unexpectedly succeeded")


def emit_result(result, output):
    payload = json.dumps(result, indent=2) + "\n"
    if output is None:
        sys.stdout.write(payload)
        return
    destination = Path(output)
    require(destination.is_absolute(), "output must be an absolute external destination")
    parent = destination.parent.resolve(strict=True)
    destination = parent / destination.name
    source_directory = Path(__file__).resolve().parent
    require(not destination.is_relative_to(source_directory), "output must be outside the checker input directory")
    require(not destination.exists() and not destination.is_symlink(), "output destination already exists")
    with destination.open("x") as stream:
        stream.write(payload)


MUTATIONS = ['double-raw-product', 'omit-stabilizer-crossing', 'omit-heegaard-constraint', 'wrong-euler-coefficient', 'wrong-stabilization-genus', 'wrong-rescaling-power', 'nonzero-seam']

def monomial(n, coefficient, exponent):
    """Canonical coefficient and a-exponent for a**3=n, allowing Laurent powers."""
    quotient, remainder = divmod(exponent, 3)
    return Fraction(coefficient) * Fraction(n) ** quotient, remainder


def standard_label_count(elements, identity, g, k):
    """Standard genus-g Heegaard pair with g-k identity relators."""
    return sum(
        all(labels[j] == identity for j in range(g - k - (1 if MUTANT == "omit-heegaard-constraint" else 0)))
        for labels in product(elements, repeat=g)
    )


def main():
    # All two red/green labels for the parallel genus-one C2 diagram.
    genus_one = [(2 if MUTANT == "double-raw-product" else 1) for r, c in product(range(2), repeat=2)]
    require(sum(genus_one) == 4, 'invariant failed: sum(genus_one) == 4')

    # All 2**6 terms of the genus-three stabilizer, with two transverse pairs.
    stabilizer = [
        (-1) ** (r1 * c1 + (0 if MUTANT == "omit-stabilizer-crossing" else r3 * c3))
        for r1, r2, r3, c1, c2, c3 in product(range(2), repeat=6)
    ]
    require(len(stabilizer) == 64, 'invariant failed: len(stabilizer) == 64')
    require(sum(stabilizer) == 16, 'invariant failed: sum(stabilizer) == 16')
    require(Fraction(sum(genus_one) ** 3, sum(stabilizer)) == 4, 'invariant failed: Fraction(sum(genus_one) ** 3, sum(stabilizer)) == 4')
    require(1**3 < 4 < 2**3, 'invariant failed: 1**3 < 4 < 2**3')

    # Checks including a genuinely nonabelian group; only equality with its
    # identity is needed in this standard Heegaard presentation.
    group_inputs = [("C" + str(n), list(range(n)), 0) for n in range(1, 8)]
    s3 = list(permutations(range(3)))
    group_inputs.append(("S3", s3, (0, 1, 2)))
    label_cases = 0
    for name, elements, identity in group_inputs:
        n = len(elements)
        for g in range(1, 5):
            for k in range(g + 1):
                count = standard_label_count(elements, identity, g, k)
                require(count == n**k, ('invariant failed: count == n**k', (name, g, k, count)))
                require(count * n**g == n ** (g + k), 'invariant failed: count * n**g == n ** (g + k)')
                label_cases += 1

    # Symbolic Laurent identities hold for every complex root a**3=n.
    # xi=n*a, hence xi**(-g)*n**(g+k)=n**k*a**(-g).
    parameter_cases = 0
    for n in range(1, 21):
        require(n**4 == n**3 * n, 'invariant failed: n**4 == n**3 * n')
        for g in range(1, 31):
            for k in range(g + 1):
                chi = 2 + g - (2 if MUTANT == "wrong-euler-coefficient" else 3) * k
                raw_normalized = monomial(n, n**k, -g)
                family = monomial(n, 1, 2 - chi)
                require(raw_normalized == family, 'invariant failed: raw_normalized == family')
                stabilized = monomial(n, n ** (k + 1), -(g + (2 if MUTANT == "wrong-stabilization-genus" else 3)))
                require(stabilized == family, 'invariant failed: stabilized == family')
                require(monomial(n, n**k, -g - (1 if MUTANT == "wrong-rescaling-power" else 2)) == monomial(n, 1, -chi), 'invariant failed: monomial(n, n**k, -g - 2) == monomial(n, 1, -chi)')
                parameter_cases += 1

    # Exact Euler gluing exponents for chi(Y)=0; integer cases are a finite
    # stress test of the universally proved additive identity.
    euler_cases = 0
    for x, y in product(range(-20, 21), repeat=2):
        require(-(x + y - (1 if MUTANT == "nonzero-seam" else 0)) == -x - y, 'invariant failed: -(x + y - 0) == -x - y')
        euler_cases += 1
    require(-0 == 0, 'invariant failed: -0 == 0')                 # Every closed three-manifold cylinder.
    require(-(1 + 1 - 0) == -2, 'invariant failed: -(1 + 1 - 0) == -2')     # Two four-balls glued along S3.
    require(monomial(2, 1, -2 + 2) == (Fraction(1), 0), 'invariant failed: monomial(2, 1, -2 + 2) == (Fraction(1), 0)')

    result = {
        "status": "PASS",
        "method": "Exact integer and rational arithmetic; no numerical roots",
        "c2_parallel_diagram": {
            "raw_terms": len(genus_one), "averaged_evaluation": sum(genus_one)
        },
        "c2_stabilizer": {
            "raw_terms": len(stabilizer),
            "positive_terms": stabilizer.count(1),
            "negative_terms": stabilizer.count(-1),
            "averaged_evaluation": sum(stabilizer),
            "stabilization_constant": 16,
        },
        "closed_S1_times_S3_value_cubed": 4,
        "standard_heegaard_label_cases": label_cases,
        "formal_parameter_identity_cases": parameter_cases,
        "euler_exponent_cases": euler_cases,
        "limitations": [
            "Parameter checks do not assert every tested pair is a realized trisection.",
            "Finite checks supplement the general mathematical proofs.",
            "The general MMT evaluation theorem is an external dependency.",
        ],
    }
    return result

def cli():
    global MUTANT
    parser = argparse.ArgumentParser(description="Exact source-free audit checks; stdout by default")
    parser.add_argument("--output", help="Optional absolute new file outside the input directory")
    parser.add_argument("--require-readonly", action="store_true", help="Require nonroot execution and actual nonwritable input")
    parser.add_argument("--mutant", choices=MUTATIONS, help="Deliberate semantic corruption; every choice must fail a guard")
    args = parser.parse_args()
    MUTANT = args.mutant
    if args.require_readonly:
        require_readonly()
    emit_result(main(), args.output)


if __name__ == "__main__":
    cli()
