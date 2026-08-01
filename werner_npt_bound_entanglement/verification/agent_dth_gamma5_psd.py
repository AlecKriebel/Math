#!/usr/bin/env python3
"""Independent exact PSD audit for the recovered Gamma5 face blocks."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json


HERE = Path(__file__).resolve().parent
FORMAT = "dth-gamma5-face-pd-reference-v1"
EXPECTED_ACTIVE = 188
EXPECTED_REDUCED_RANK = 751
EXPECTED_MAXIMUM_DIMENSION = 40


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MATRIX = import_file("dth_gamma5_psd_matrix", HERE / "agent_dth_exact_matrix.py")


def decode_symmetric(values, dimension, denominator):
    expected = dimension * (dimension + 1) // 2
    if len(values) != expected:
        raise ValueError("wrong Gamma5 symmetric reference entry count")
    entries = [Fraction(int(value), denominator) for value in values]
    matrix = [[Fraction(0) for _ in range(dimension)]
              for _ in range(dimension)]
    position = 0
    for row in range(dimension):
        matrix[row][row] = entries[position]
        position += 1
    for row in range(dimension):
        for column in range(row + 1, dimension):
            matrix[row][column] = matrix[column][row] = entries[position]
            position += 1
    return matrix


def decode_upper(values, dimension, denominator):
    expected = dimension * (dimension + 1) // 2
    if len(values) != expected:
        raise ValueError("wrong Gamma5 triangular transform entry count")
    matrix = [[Fraction(0) for _ in range(dimension)]
              for _ in range(dimension)]
    position = 0
    for row in range(dimension):
        for column in range(row, dimension):
            matrix[row][column] = Fraction(int(values[position]), denominator)
            position += 1
    return matrix


def read_reference(path):
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with gzip.open(path, "rt", encoding="ascii") as handle:
        payload = json.load(handle)
    if payload.get("format") != FORMAT:
        raise ValueError("unknown Gamma5 PD reference format")
    reference_bits = int(payload["reference_bits"])
    transform_bits = int(payload["transform_bits"])
    blocks = {}
    for block in payload["blocks"]:
        tag = block["shape"]
        if len(tag) != 3 or any(letter not in "012345" for letter in tag):
            raise ValueError("invalid Gamma5 block tag")
        shapes = tuple(map(int, tag))
        dimension = int(block["dimension"])
        blocks[shapes] = {
            "dimension": dimension,
            "scale_exponent": int(block["scale_exponent"]),
            "reference": decode_symmetric(
                block["reference_upper"], dimension, 1 << reference_bits
            ),
            "transform": decode_upper(
                block["transform_upper"], dimension, 1 << transform_bits
            ),
        }
    if set(blocks) != set(product(range(6), repeat=3)):
        raise ValueError("Gamma5 reference does not contain 216 blocks")
    return blocks, payload["source_certificate_sha256"], digest


def rational_digest(value):
    value = Fraction(value)
    text = f"{value.numerator}/{value.denominator}".encode("ascii")
    return {
        "numerator_digits": len(str(abs(value.numerator))),
        "denominator_digits": len(str(value.denominator)),
        "sha256": hashlib.sha256(text).hexdigest(),
    }


def verify_coordinates(exact_blocks, source_hash, certificate, verbose=True):
    if set(exact_blocks) != set(product(range(6), repeat=3)):
        raise ValueError("Gamma5 exact coordinate block set is incomplete")
    references, bound_source, reference_hash = read_reference(certificate)
    if bound_source != source_hash:
        raise AssertionError("Gamma5 PD reference is bound to another source")
    active = total_rank = maximum_dimension = 0
    worst_ratio = Fraction(0)
    worst_shape = None
    minimum_margin = None
    minimum_margin_shape = None
    minimum_lower_bound = None
    minimum_lower_bound_shape = None
    for count, shapes in enumerate(product(range(6), repeat=3), 1):
        exact = exact_blocks[shapes]
        dimension = len(exact)
        if any(len(row) != dimension for row in exact):
            raise ValueError(f"nonsquare Gamma5 block {shapes}")
        if any(exact[row][column] != exact[column][row]
               for row in range(dimension) for column in range(row)):
            raise ValueError(f"nonsymmetric Gamma5 block {shapes}")
        reference = references[shapes]
        if reference["dimension"] != dimension:
            raise AssertionError(f"Gamma5 dimension mismatch at {shapes}")
        total_rank += dimension
        maximum_dimension = max(maximum_dimension, dimension)
        if not dimension:
            if reference["scale_exponent"] != 0:
                raise AssertionError("zero Gamma5 block has nonzero scale")
            continue
        active += 1
        scaled = [[Fraction(value) * Fraction(2) **
                   reference["scale_exponent"] for value in row]
                  for row in exact]
        result = MATRIX.assert_pd_near_reference(
            scaled, reference["reference"], reference["transform"],
            triangular=True,
        )
        ratio = (result["difference_frobenius_squared"]
                 / result["matrix_lower_bound"] ** 2)
        if ratio > worst_ratio:
            worst_ratio, worst_shape = ratio, shapes
        margin = result["minimum_margin"]
        if minimum_margin is None or margin < minimum_margin:
            minimum_margin, minimum_margin_shape = margin, shapes
        lower = result["matrix_lower_bound"]
        if minimum_lower_bound is None or lower < minimum_lower_bound:
            minimum_lower_bound, minimum_lower_bound_shape = lower, shapes
        if verbose and count % 24 == 0:
            print("exact Gamma5 PD blocks", count, "/216", flush=True)

    assert active == EXPECTED_ACTIVE
    assert total_rank == EXPECTED_REDUCED_RANK
    assert maximum_dimension == EXPECTED_MAXIMUM_DIMENSION
    assert minimum_margin is not None and minimum_margin > 0
    assert minimum_lower_bound is not None and minimum_lower_bound > 0
    assert worst_ratio < 1
    result = {
        "certificate_sha256": reference_hash,
        "active_blocks": active,
        "total_rank": total_rank,
        "maximum_dimension": maximum_dimension,
        "minimum_margin": minimum_margin,
        "minimum_margin_shape": minimum_margin_shape,
        "minimum_lower_bound": minimum_lower_bound,
        "minimum_lower_bound_shape": minimum_lower_bound_shape,
        "worst_perturbation_ratio": worst_ratio,
        "worst_perturbation_shape": worst_shape,
        "minimum_margin_digest": rational_digest(minimum_margin),
        "minimum_lower_bound_digest": rational_digest(minimum_lower_bound),
        "worst_perturbation_ratio_digest": rational_digest(worst_ratio),
    }
    if verbose:
        print("exact Gamma5 positive-definiteness certificate passed")
        print("Gamma5 PD reference sha256:", reference_hash)
        print("active/rank/max:", active, total_rank, maximum_dimension)
        print("minimum congruent margin:", float(minimum_margin),
              "block", minimum_margin_shape)
        print("minimum scaled lower bound:", float(minimum_lower_bound),
              "block", minimum_lower_bound_shape)
        print("worst perturbation ratio:", float(worst_ratio),
              "block", worst_shape)
        print("minimum margin digest:", result["minimum_margin_digest"])
        print("minimum lower-bound digest:",
              result["minimum_lower_bound_digest"])
        print("worst perturbation-ratio digest:",
              result["worst_perturbation_ratio_digest"])
    return result
