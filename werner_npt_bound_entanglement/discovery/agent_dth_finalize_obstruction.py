#!/usr/bin/env python3
"""Audit and canonically package the exact constrained-DTH obstruction.

The generator emits a convenient per-entry rational JSON file.  This script
rebuilds the exact trace and minimal-DTH witness pairing, requires positive
trace and strictly negative pairing, and writes the deterministic compact-v2
gzip consumed by the independent verifier.

This packaging step proves no mixed-face positivity by itself.  That check is
performed independently by ``agent_dth_full_face_crt.py`` and
``agent_dth_mixed_psd.py``.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VERIFY = ROOT / "verification"


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CODEC = import_file("dth_finalize_codec",
                    VERIFY / "agent_dth_certificate_io.py")
FUNCTIONALS = import_file("dth_finalize_functionals",
                          VERIFY / "agent_dth_exact_functionals.py")


def read_generator_json(path):
    data = json.loads(Path(path).read_text(encoding="ascii"))
    coordinates = {}
    for shapes in product(range(5), repeat=3):
        tag = "".join(map(str, shapes))
        block = data["blocks"][tag]
        dimension = int(block["dimension"])
        values = [Fraction(int(numerator), int(denominator))
                  for numerator, denominator in block["upper"]]
        if len(values) != dimension * (dimension + 1) // 2:
            raise ValueError(f"wrong entry count in block {tag}")
        matrix = [[Fraction(0) for _ in range(dimension)]
                  for _ in range(dimension)]
        position = 0
        for i in range(dimension):
            matrix[i][i] = values[position]
            position += 1
        for i in range(dimension):
            for j in range(i + 1, dimension):
                matrix[i][j] = matrix[j][i] = values[position]
                position += 1
        coordinates[shapes] = matrix
    return coordinates, int(data["rounding_bits"])


def exact_functionals(coordinates):
    exact = {
        shapes: sp.Matrix(coordinates[shapes])
        for shapes in product(range(5), repeat=3)
    }
    trace, objective = FUNCTIONALS.total_functionals(exact)
    if trace <= 0:
        raise AssertionError("candidate trace is not positive")
    if objective >= 0:
        raise AssertionError("candidate witness pairing is not negative")
    return trace, objective


def digest(value):
    value = sp.Rational(value)
    text = f"{int(value.p)}/{int(value.q)}".encode("ascii")
    return hashlib.sha256(text).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/tmp/dth_exact_obstruction.json")
    parser.add_argument(
        "--output",
        default=str(
            VERIFY / "certificates" /
            "dth_constrained_pseudomoment.json.gz"
        ),
    )
    args = parser.parse_args()
    source = Path(args.input)
    coordinates, rounding_bits = read_generator_json(source)
    trace, objective = exact_functionals(coordinates)
    raw_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    metadata = {
        "normalized": False,
        "raw_generator_sha256": raw_hash,
        "rounding_bits": rounding_bits,
        "scope": (
            "exact negative pseudomoment for the complete first-level "
            "DTH-constrained five-replica lift"
        ),
    }
    output = Path(args.output)
    certificate_hash = CODEC.write_compact_certificate(
        output, coordinates, metadata
    )
    decoded, decoded_metadata = CODEC.read_certificate(output)
    assert decoded == coordinates
    assert decoded_metadata == metadata
    print("exact trace sign: positive")
    print("exact objective sign: negative")
    print("trace decimal:", sp.N(trace, 30))
    print("objective decimal:", sp.N(objective, 30))
    print("trace rational sha256:", digest(trace))
    print("objective rational sha256:", digest(objective))
    print("certificate bytes:", output.stat().st_size)
    print("certificate sha256:", certificate_hash)


if __name__ == "__main__":
    main()
