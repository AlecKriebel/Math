#!/usr/bin/env python3
"""Bounded-memory evaluator for the level-five deepest branch norm.

For a target ``(1,2,s)`` this constructs four successive inverse cubic
quotients and evaluates ``Norm(Delta(X4))``.  The implementation imports the
audited finite-algebra primitives from the level-four package, but builds the
tower in a fresh loop so the depth bookkeeping is explicit.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType


def load_level_four_module() -> ModuleType:
    source = (
        Path(__file__).resolve().parents[1]
        / "w4_search"
        / "finite_field_norm.py"
    )
    specification = importlib.util.spec_from_file_location(
        "audited_w4_finite_field_norm", source
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load the audited level-four evaluator")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


W4 = load_level_four_module()


def tower_profile(
    modulus: int, s_value: int, inverse_depth: int = 4
) -> dict[str, tuple[int, ...] | int]:
    """Return all discriminant, leading, and reconstruction-guard norms."""
    algebra = W4.CubicAlgebra(modulus)
    point = (
        algebra.constant(1),
        algebra.constant(2),
        algebra.constant(s_value),
    )
    discriminant_norms = [W4.discriminant(algebra, point)[0]]
    leading_norms = [2 % modulus]
    guard_norms: list[int] = []

    for _level in range(inverse_depth):
        a, b, c = point
        leading = algebra.scale(a, 2)
        extension = algebra.extend(
            (
                algebra.neg(c),
                algebra.constant(2),
                algebra.neg(b),
                leading,
            )
        )
        embedded_point = tuple(extension.embed(entry) for entry in point)
        root = extension.generator()
        point, guards = W4.reconstruct_with_guards(
            extension, *embedded_point, root
        )
        discriminant_norms.append(
            extension.norm(W4.discriminant(extension, point))
        )
        guard_norms.extend(extension.norm(guard) for guard in guards)
        leading_norms.append(extension.norm(extension.scale(point[0], 2)))
        algebra = extension

    return {
        "dimension": algebra.dimension,
        "discriminant_norms": tuple(discriminant_norms),
        "leading_norms": tuple(leading_norms),
        "reconstruction_guard_norms": tuple(guard_norms),
    }


def deepest_norm(
    modulus: int, s_value: int, inverse_depth: int = 4
) -> int:
    """Evaluate only the deepest norm, omitting all diagnostic guard norms."""
    algebra = W4.CubicAlgebra(modulus)
    point = (
        algebra.constant(1),
        algebra.constant(2),
        algebra.constant(s_value),
    )

    for _level in range(inverse_depth):
        a, b, c = point
        extension = algebra.extend(
            (
                algebra.neg(c),
                algebra.constant(2),
                algebra.neg(b),
                algebra.scale(a, 2),
            )
        )
        embedded_point = tuple(extension.embed(entry) for entry in point)
        point, _guards = W4.reconstruct_with_guards(
            extension, *embedded_point, extension.generator()
        )
        algebra = extension

    return algebra.norm(W4.discriminant(algebra, point))


def deepest_norm_derivative(prime: int, s_value: int) -> int:
    modulus = prime * prime
    at_s = deepest_norm(modulus, s_value)
    at_s_plus_prime = deepest_norm(modulus, s_value + prime)
    difference = (at_s_plus_prime - at_s) % modulus
    if difference % prime:
        raise AssertionError("finite difference is not divisible by p")
    return difference // prime


def hensel_profile(prime: int, s_value: int) -> dict[str, object]:
    """Return three p-adic lifts and their first-order finite differences."""
    modulus = prime * prime
    values = tuple(
        deepest_norm(modulus, s_value + multiple * prime)
        for multiple in range(3)
    )
    differences = tuple((value - values[0]) % modulus for value in values[1:])
    if any(difference % prime for difference in differences):
        raise AssertionError("finite difference is not divisible by p")
    divided = tuple(difference // prime for difference in differences)
    return {
        "modulus": modulus,
        "lifted_parameters": tuple(
            s_value + multiple * prime for multiple in range(3)
        ),
        "lifted_norms": values,
        "divided_differences_mod_p": divided,
        "derivative_mod_p": divided[0],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime", type=int, default=31)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--depth", type=int, default=4)
    diagnostics = parser.add_mutually_exclusive_group()
    diagnostics.add_argument("--profile", action="store_true")
    diagnostics.add_argument("--hensel", action="store_true")
    parser.add_argument("--memory-mib", type=int, default=2048)
    return parser.parse_args()


def main() -> None:
    arguments = parse_args()
    if not W4._is_prime(arguments.prime):
        raise SystemExit("--prime must be prime")
    if arguments.count < 0:
        raise SystemExit("--count must be nonnegative")
    if not 0 <= arguments.depth <= 4:
        raise SystemExit("--depth must lie between 0 and 4")
    W4._set_memory_limit(arguments.memory_mib)
    for offset in range(arguments.count):
        s_value = (arguments.start + offset) % arguments.prime
        record: dict[str, object] = {
            "prime": arguments.prime,
            "s": s_value,
        }
        try:
            if arguments.hensel:
                record.update(hensel_profile(arguments.prime, s_value))
            elif arguments.profile:
                profile = tower_profile(
                    arguments.prime, s_value, inverse_depth=arguments.depth
                )
                record.update(profile)
            else:
                record["norm"] = deepest_norm(
                    arguments.prime,
                    s_value,
                    inverse_depth=arguments.depth,
                )
            record["status"] = "ok"
        except W4.SingularElement as error:
            record["status"] = "exceptional"
            record["reason"] = str(error)
        print(json.dumps(record, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
