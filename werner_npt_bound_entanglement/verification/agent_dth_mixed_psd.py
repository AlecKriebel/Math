#!/usr/bin/env python3
"""Exact positive-definiteness audit for reconstructed mixed DTH blocks.

The full-face CRT verifier returns 216 exact rational coordinate matrices
``B_mu`` for the partial transpose of the holomorphic certificate.  This
module proves every nonzero ``B_mu`` positive definite.  Its auxiliary
certificate contains, block by block,

* an exact power-of-two rescaling;
* a 100-bit dyadic symmetric reference; and
* an 80-bit dyadic upper-triangular inverse-Cholesky proposal.

All conclusions are then checked over ``QQ``.  The congruent reference must
be strictly diagonally dominant with positive diagonal, and the exact
Frobenius distance from the reconstructed block must be smaller than the
certified spectral gap.  Floating point was used only by the discovery
generator to propose the dyadic transform; it is not used here.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from pathlib import Path
import gzip
import hashlib
import importlib.util
import json


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE / "certificates" / "dth_mixed_pd_reference.json.gz"
)
FORMAT = "dth-mixed-face-pd-reference-v1"
EXPECTED_CERTIFICATE_SHA256 = (
    "648186810cd9e9becc71eb6d319749c2a2c956d3f152f116ff17a1cdd1bcdf33"
)
EXPECTED_SOURCE_SHA256 = (
    "707e183995f1963aebe9eef732530396b2baa53421aaa9fcbf9f5cb31c36e9da"
)
EXPECTED_REFERENCE_BITS = 100
EXPECTED_TRANSFORM_BITS = 80


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MATRIX = import_file("dth_exact_matrix_mixed_psd",
                     HERE / "agent_dth_exact_matrix.py")


def decode_symmetric(values, dimension, denominator):
    expected = dimension * (dimension + 1) // 2
    if len(values) != expected:
        raise ValueError("wrong symmetric dyadic entry count")
    entries = [Fraction(int(value), denominator) for value in values]
    matrix = [[Fraction(0) for _ in range(dimension)]
              for _ in range(dimension)]
    position = 0
    for i in range(dimension):
        matrix[i][i] = entries[position]
        position += 1
    for i in range(dimension):
        for j in range(i + 1, dimension):
            matrix[i][j] = matrix[j][i] = entries[position]
            position += 1
    return matrix


def decode_upper_triangular(values, dimension, denominator):
    expected = dimension * (dimension + 1) // 2
    if len(values) != expected:
        raise ValueError("wrong triangular dyadic entry count")
    matrix = [[Fraction(0) for _ in range(dimension)]
              for _ in range(dimension)]
    position = 0
    for i in range(dimension):
        for j in range(i, dimension):
            matrix[i][j] = Fraction(int(values[position]), denominator)
            position += 1
    return matrix


def rational_digest(value):
    value = Fraction(value)
    text = f"{value.numerator}/{value.denominator}".encode("ascii")
    return {
        "numerator_digits": len(str(abs(value.numerator))),
        "denominator_digits": len(str(value.denominator)),
        "sha256": hashlib.sha256(text).hexdigest(),
    }


def read_reference_certificate(path=DEFAULT_CERTIFICATE):
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if path.resolve() == DEFAULT_CERTIFICATE.resolve():
        assert digest == EXPECTED_CERTIFICATE_SHA256
    with gzip.open(path, "rt", encoding="ascii") as handle:
        payload = json.load(handle)
    if payload.get("format") != FORMAT:
        raise ValueError("unknown mixed-PD reference format")
    reference_bits = int(payload["reference_bits"])
    transform_bits = int(payload["transform_bits"])
    if reference_bits != EXPECTED_REFERENCE_BITS:
        raise ValueError("unexpected reference precision")
    if transform_bits != EXPECTED_TRANSFORM_BITS:
        raise ValueError("unexpected transform precision")
    blocks = {}
    for block in payload["blocks"]:
        tag = block["shape"]
        if len(tag) != 3 or any(letter not in "012345" for letter in tag):
            raise ValueError("invalid mixed shape tag")
        shapes = tuple(map(int, tag))
        if shapes in blocks:
            raise ValueError(f"duplicate mixed shape {tag}")
        dimension = int(block["dimension"])
        reference = decode_symmetric(
            block["reference_upper"], dimension, 1 << reference_bits
        )
        transform = decode_upper_triangular(
            block["transform_upper"], dimension, 1 << transform_bits
        )
        blocks[shapes] = {
            "dimension": dimension,
            "scale_exponent": int(block["scale_exponent"]),
            "reference": reference,
            "transform": transform,
        }
    if set(blocks) != set(product(range(6), repeat=3)):
        raise ValueError("mixed-PD certificate does not contain 216 blocks")
    return blocks, payload["source_certificate_sha256"], digest


def verify_coordinates(mixed_coordinates, source_certificate_sha256,
                       certificate=DEFAULT_CERTIFICATE, verbose=True):
    """Prove all reconstructed exact mixed face coordinates are PD."""
    expected = set(product(range(6), repeat=3))
    if set(mixed_coordinates) != expected:
        raise ValueError("mixed coordinate block set is incomplete")
    blocks, bound_source, certificate_hash = read_reference_certificate(
        certificate
    )
    if bound_source != source_certificate_sha256:
        raise AssertionError("mixed-PD reference is bound to another source")
    if Path(certificate).resolve() == DEFAULT_CERTIFICATE.resolve():
        assert bound_source == EXPECTED_SOURCE_SHA256

    nonzero = 0
    total_rank = 0
    maximum_dimension = 0
    worst_ratio = Fraction(0)
    worst_ratio_shape = None
    minimum_margin = None
    minimum_margin_shape = None
    minimum_lower_bound = None
    minimum_lower_bound_shape = None
    for count, shapes in enumerate(product(range(6), repeat=3), 1):
        exact = mixed_coordinates[shapes]
        dimension = len(exact)
        if any(len(row) != dimension for row in exact):
            raise ValueError(f"nonsquare exact mixed block {shapes}")
        if any(exact[i][j] != exact[j][i]
               for i in range(dimension) for j in range(i)):
            raise ValueError(f"nonsymmetric exact mixed block {shapes}")
        block = blocks[shapes]
        if block["dimension"] != dimension:
            raise AssertionError(f"mixed block dimension mismatch at {shapes}")
        total_rank += dimension
        maximum_dimension = max(maximum_dimension, dimension)
        if not dimension:
            if block["scale_exponent"] != 0:
                raise AssertionError("zero block has a nontrivial scale")
            continue
        nonzero += 1
        exponent = block["scale_exponent"]
        scale = Fraction(2) ** exponent
        scaled = [[Fraction(value) * scale for value in row]
                  for row in exact]
        result = MATRIX.assert_pd_near_reference(
            scaled,
            block["reference"],
            block["transform"],
            triangular=True,
        )
        ratio = (result["difference_frobenius_squared"]
                 / result["matrix_lower_bound"] ** 2)
        if ratio > worst_ratio:
            worst_ratio, worst_ratio_shape = ratio, shapes
        margin = result["minimum_margin"]
        if minimum_margin is None or margin < minimum_margin:
            minimum_margin, minimum_margin_shape = margin, shapes
        lower = result["matrix_lower_bound"]
        if minimum_lower_bound is None or lower < minimum_lower_bound:
            minimum_lower_bound, minimum_lower_bound_shape = lower, shapes
        if verbose and count % 24 == 0:
            print("exact mixed PD blocks", count, "/216", flush=True)

    assert nonzero == 198
    assert total_rank == 2266
    assert maximum_dimension == 53
    assert minimum_margin is not None and minimum_margin > 0
    assert minimum_lower_bound is not None and minimum_lower_bound > 0
    assert worst_ratio < 1
    result = {
        "certificate_sha256": certificate_hash,
        "nonzero_blocks": nonzero,
        "total_rank": total_rank,
        "maximum_dimension": maximum_dimension,
        "minimum_margin": minimum_margin,
        "minimum_margin_shape": minimum_margin_shape,
        "minimum_lower_bound": minimum_lower_bound,
        "minimum_lower_bound_shape": minimum_lower_bound_shape,
        "worst_perturbation_ratio": worst_ratio,
        "worst_perturbation_shape": worst_ratio_shape,
        "minimum_margin_digest": rational_digest(minimum_margin),
        "minimum_lower_bound_digest": rational_digest(minimum_lower_bound),
        "worst_perturbation_ratio_digest": rational_digest(worst_ratio),
    }
    if verbose:
        print("exact mixed-face positive-definiteness certificate passed")
        print("mixed PD reference sha256:", certificate_hash)
        print("nonzero blocks:", nonzero, "total rank:", total_rank)
        print("minimum exact congruent margin:", float(minimum_margin),
              "block", minimum_margin_shape)
        print("minimum certified scaled lower bound:",
              float(minimum_lower_bound), "block", minimum_lower_bound_shape)
        print("worst exact perturbation ratio:", float(worst_ratio),
              "block", worst_ratio_shape)
        print("minimum margin digest:", result["minimum_margin_digest"])
        print("minimum lower-bound digest:",
              result["minimum_lower_bound_digest"])
        print("worst perturbation-ratio digest:",
              result["worst_perturbation_ratio_digest"])
    return result


if __name__ == "__main__":
    raise SystemExit(
        "This module consumes exact mixed coordinates returned by "
        "agent_dth_full_face_crt.py; run "
        "verify_dth_constrained_pseudomoment.py instead."
    )
