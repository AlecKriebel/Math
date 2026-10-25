#!/usr/bin/env python3
"""Differential tests for the optimized sparse-kernel routine."""
from __future__ import annotations

if not __debug__:
    raise SystemExit("K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN")

import importlib.util
import itertools
import random
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp


def load_core(path: Path):
    spec = importlib.util.spec_from_file_location("k2p_atlas_core", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["k2p_atlas_core"] = module
    spec.loader.exec_module(module)
    return module


def check(core, columns) -> None:
    fast = core.kernel_sparse_columns_fast(columns)
    exact = core.exact_kernel_sparse_columns(columns)
    if len(fast) != len(exact):
        raise AssertionError(("nullity", columns, fast, exact))
    for vector in fast:
        if core.sparse_lincomb(columns, vector):
            raise AssertionError(("not in kernel", columns, vector))
    if fast and sp.Matrix(fast).rank() != len(fast):
        raise AssertionError(("dependent basis", columns, fast))


def main() -> None:
    core = load_core(Path(__file__).resolve().parent / "atlas" / "k2p_atlas_core.py")
    atoms = ({}, {(0,): Fraction(1)}, {(0,): Fraction(-1)}, {(1,): Fraction(1)})
    for width in range(1, 5):
        for columns in itertools.product(atoms, repeat=width):
            check(core, list(columns))
    randomizer = random.Random(20260820)
    keys = [(0,), (1,), (2,), (0, 1)]
    for _ in range(800):
        columns = []
        for _column in range(randomizer.randint(1, 16)):
            column = {}
            for key in keys:
                numerator = randomizer.randint(-3, 3)
                if numerator:
                    column[key] = Fraction(numerator, randomizer.randint(1, 3))
            columns.append(column)
        check(core, columns)
    # Cubic four-port blocks reach width 40.  Exercise the optimized kernel at
    # its actual production width as well as the exhaustive tiny cases above.
    independent_40 = [{(index,): Fraction(index + 1)} for index in range(40)]
    check(core, independent_40)
    one_relation_40 = independent_40[:-1] + [
        {(0,): Fraction(1), (1,): Fraction(2)}
    ]
    check(core, one_relation_40)
    print("EXACT_SPARSE_KERNEL_DIFFERENTIAL_PASS")


if __name__ == "__main__":
    main()
