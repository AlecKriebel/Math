#!/usr/bin/env python3
"""Exact verifier for the complete-tripartition-PPT DTH obstruction.

The certificate is a real local-unitary-invariant five-replica moment on

    (Lambda^2 H)_{12} : (Lambda^2 H)_{34} : H_5.

It obeys the complete first-level density-moment Pluecker, support, and
Omega constraints.  This verifier proves, using exact rational arithmetic,
that

* the holomorphic moment is positive definite on its 768-dimensional face;
* its minimal-DTH witness pairing is strictly negative;
* Gamma_{12} is positive definite on the exact 2266-dimensional product
  face; and
* Gamma_5 is positive definite on the exact 751-dimensional final-slot
  face.

Pair exchange identifies Gamma_{12} and Gamma_{34}; complementary partial
transposes differ by full transpose.  The two displayed PPT checks therefore
cover every cut of the grouped moment tripartition.  The result is an exact
pseudomoment obstruction to this strengthened first lift.  It is not a
rank-one Veronese--Segre point and is not a physical DTH counterexample.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATES = HERE / "certificates"

DEFAULT_SOURCE = CERTIFICATES / "dth_complete_ppt_pseudomoment.json.gz"
DEFAULT_GAMMA1_REFERENCE = (
    CERTIFICATES / "dth_complete_ppt_gamma1_pd_reference.json.gz"
)
DEFAULT_GAMMA5_CHARTS = (
    CERTIFICATES / "dth_gamma5_face_integer_charts.json.gz"
)
DEFAULT_GAMMA5_REFERENCE = (
    CERTIFICATES / "dth_complete_ppt_gamma5_pd_reference.json.gz"
)

EXPECTED_SOURCE_SHA256 = (
    "4a42cfc9a3fcafdbf5667f5fb220eb417cea1b2f76398096668e70179e94606a"
)
EXPECTED_GAMMA1_REFERENCE_SHA256 = (
    "d4b10997430cbe1755a07cd5e52867538577604e0a9563c0c714b3e72dacbb1b"
)
EXPECTED_GAMMA5_CHARTS_SHA256 = (
    "6caf453f0043a2e7296b31e2f14bc90b01f38163b1d89ece39276ac625ded9aa"
)
EXPECTED_GAMMA5_REFERENCE_SHA256 = (
    "ebc375184ff929016fda41f344b99cbe8f0d2042e563347a297e0ccd08c6b031"
)

EXPECTED_TRACE_DIGEST = {
    "numerator_digits": 471,
    "denominator_digits": 471,
    "sha256": "368a672912bcffa686528fdb6bb74effcb7e44f89f4bd3127af3a043cd1ed9bd",
}
EXPECTED_OBJECTIVE_DIGEST = {
    "numerator_digits": 470,
    "denominator_digits": 473,
    "sha256": "043d2e3235d928c9aea95e419c3b24f55feaa2906175365f93aea7910b47a15a",
}


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE = import_file(
    "dth_complete_ppt_base", HERE / "verify_dth_constrained_pseudomoment.py"
)
GAMMA1_FACE = import_file(
    "dth_complete_ppt_gamma1_face", HERE / "agent_dth_full_face_crt.py"
)
GAMMA1_PSD = import_file(
    "dth_complete_ppt_gamma1_psd", HERE / "agent_dth_mixed_psd.py"
)
GAMMA5_FACE = import_file(
    "dth_complete_ppt_gamma5_face", HERE / "agent_dth_gamma5_face_crt.py"
)
GAMMA5_PSD = import_file(
    "dth_complete_ppt_gamma5_psd", HERE / "agent_dth_gamma5_psd.py"
)
CENSUS = import_file(
    "dth_complete_ppt_census", HERE / "verify_dth_gamma5_census.py"
)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require_default_hash(path, default, expected):
    digest = sha256(path)
    if Path(path).resolve() == Path(default).resolve() and digest != expected:
        raise AssertionError(f"unexpected artifact hash for {path}: {digest}")
    return digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument(
        "--gamma1-reference", type=Path, default=DEFAULT_GAMMA1_REFERENCE
    )
    parser.add_argument(
        "--gamma5-charts", type=Path, default=DEFAULT_GAMMA5_CHARTS
    )
    parser.add_argument(
        "--gamma5-reference", type=Path, default=DEFAULT_GAMMA5_REFERENCE
    )
    args = parser.parse_args()

    source_hash = require_default_hash(
        args.source, DEFAULT_SOURCE, EXPECTED_SOURCE_SHA256
    )
    gamma1_reference_hash = require_default_hash(
        args.gamma1_reference,
        DEFAULT_GAMMA1_REFERENCE,
        EXPECTED_GAMMA1_REFERENCE_SHA256,
    )
    gamma5_charts_hash = require_default_hash(
        args.gamma5_charts,
        DEFAULT_GAMMA5_CHARTS,
        EXPECTED_GAMMA5_CHARTS_SHA256,
    )
    gamma5_reference_hash = require_default_hash(
        args.gamma5_reference,
        DEFAULT_GAMMA5_REFERENCE,
        EXPECTED_GAMMA5_REFERENCE_SHA256,
    )

    coordinates, metadata = BASE.CODEC.read_certificate(args.source)
    expected_scope = (
        "exact negative pseudomoment for the complete first-level "
        "DTH-constrained five-replica lift"
    )
    if metadata.get("scope") != expected_scope:
        raise AssertionError("unexpected source-certificate scope")

    holomorphic = BASE.audit_holomorphic_blocks(coordinates)
    trace, objective = BASE.audit_functionals(coordinates)
    trace_digest = BASE.rational_digest(trace)
    objective_digest = BASE.rational_digest(objective)
    if Path(args.source).resolve() == DEFAULT_SOURCE.resolve():
        assert trace_digest == EXPECTED_TRACE_DIGEST
        assert objective_digest == EXPECTED_OBJECTIVE_DIGEST

    print("source certificate sha256:", source_hash)
    print("holomorphic exact PD blocks/rank/max:",
          holomorphic["nonzero_blocks"], holomorphic["total_rank"],
          holomorphic["maximum_dimension"])
    print("largest holomorphic final-minor digit count:",
          holomorphic["maximum_last_minor_digits"])
    print("trace digest:", trace_digest)
    print("objective digest:", objective_digest)
    print("trace decimal:", float(trace))
    print("objective decimal:", float(objective))

    gamma1_coordinates = GAMMA1_FACE.verify_coordinates(
        coordinates, verbose=True
    )
    gamma1_result = GAMMA1_PSD.verify_coordinates(
        gamma1_coordinates,
        source_hash,
        certificate=args.gamma1_reference,
        verbose=True,
    )
    assert gamma1_result["certificate_sha256"] == gamma1_reference_hash

    gamma5_coordinates = GAMMA5_FACE.verify_coordinates(
        coordinates,
        verbose=True,
        chart_path=args.gamma5_charts,
    )
    gamma5_result = GAMMA5_PSD.verify_coordinates(
        gamma5_coordinates,
        source_hash,
        args.gamma5_reference,
        verbose=True,
    )
    assert gamma5_result["certificate_sha256"] == gamma5_reference_hash

    CENSUS.audit_ppt_cut_identities()
    print("Gamma5 chart artifact sha256:", gamma5_charts_hash)
    print("tripartition PPT-cut orbit audit passed")
    print("exact complete-tripartition-PPT DTH pseudomoment obstruction passed")
    print("scope: first-lift obstruction, not a physical DTH counterexample")


if __name__ == "__main__":
    main()
