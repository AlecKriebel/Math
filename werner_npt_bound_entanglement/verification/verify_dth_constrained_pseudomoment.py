#!/usr/bin/env python3
"""Independent exact verifier for the constrained first DTH lift.

The certificate is a local-unitary invariant density moment in the corrected
five-replica cone.  It is represented by 125 rational matrices in the exact
holomorphic support charts.  This verifier reconstructs every chart from
the defining permutation actions and checks

* positive semidefiniteness and the Pluecker/Omega range constraints;
* positive trace and a strictly negative minimal-DTH witness pairing;
* exact partial-transpose membership in the 2266-dimensional physical
  product-DTH face; and
* positive semidefiniteness on that mixed face.

The last two checks are delegated to small exact-arithmetic companion
modules.  The only inputs are the two committed rational certificate
artifacts; no floating-point sign, rank tolerance, or discovery checkpoint
is used.  A successful replay is a proof-complexity obstruction at the
first corrected Veronese--Segre level.  It is not a physical DTH vector and
does not settle the Werner problem.
"""

from __future__ import annotations

from itertools import product
from pathlib import Path
import argparse
import hashlib
import importlib.util

import sympy as sp


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = (
    HERE / "certificates" / "dth_constrained_pseudomoment.json.gz"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "707e183995f1963aebe9eef732530396b2baa53421aaa9fcbf9f5cb31c36e9da"
)
EXPECTED_TRACE_DIGEST = {
    "numerator_digits": 472,
    "denominator_digits": 472,
    "sha256": "e0223ca2026953a6aa032df45c5926fca31a917f4e2f434296a7a9e01a19f72c",
}
EXPECTED_OBJECTIVE_DIGEST = {
    "numerator_digits": 471,
    "denominator_digits": 474,
    "sha256": "7e1c917ebb25eca853454516571dc86a6c3c7f1f26cbbd785fdaac551fea5446",
}


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


CODEC = import_file("dth_certificate_codec",
                    HERE / "agent_dth_certificate_io.py")
MATRIX = import_file("dth_exact_matrix_final",
                     HERE / "agent_dth_exact_matrix.py")
FUNCTIONALS = import_file("dth_exact_functionals_final",
                          HERE / "agent_dth_exact_functionals.py")
EXACT_K = FUNCTIONALS.EXACT_K


def audit_holomorphic_blocks(coordinates):
    """Prove exact support and strict positivity of every nonzero block."""
    nonzero = 0
    total_rank = 0
    maximum_dimension = 0
    maximum_last_minor_digits = 0
    for shapes in product(range(5), repeat=3):
        coordinate = coordinates[shapes]
        physical, gram, restriction = EXACT_K.hol_k_coordinates(shapes)
        dimension = physical.cols
        if len(coordinate) != dimension or any(
                len(row) != dimension for row in coordinate):
            raise AssertionError(f"wrong coordinate dimension in {shapes}")
        assert restriction == gram * physical
        assert dimension == EXACT_K.expected_k_dimension(shapes)
        total_rank += dimension
        maximum_dimension = max(maximum_dimension, dimension)
        if not dimension:
            continue
        metadata = MATRIX.assert_positive_definite(coordinate)
        nonzero += 1
        maximum_last_minor_digits = max(
            maximum_last_minor_digits,
            len(str(abs(metadata["last_minor"]))),
        )
    assert nonzero == 118
    assert total_rank == 768
    assert maximum_dimension == 16
    return {
        "nonzero_blocks": nonzero,
        "total_rank": total_rank,
        "maximum_dimension": maximum_dimension,
        "maximum_last_minor_digits": maximum_last_minor_digits,
    }


def rational_digest(value):
    value = sp.Rational(value)
    text = f"{int(value.p)}/{int(value.q)}".encode("ascii")
    return {
        "numerator_digits": len(str(abs(int(value.p)))),
        "denominator_digits": len(str(int(value.q))),
        "sha256": hashlib.sha256(text).hexdigest(),
    }


def audit_functionals(coordinates):
    exact = {
        shapes: sp.Matrix(coordinates[shapes])
        for shapes in product(range(5), repeat=3)
    }
    trace, objective = FUNCTIONALS.total_functionals(exact)
    if trace <= 0:
        raise AssertionError("certificate trace is not positive")
    if objective >= 0:
        raise AssertionError("certificate witness pairing is not negative")
    return trace, objective


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path,
                        default=DEFAULT_CERTIFICATE)
    parser.add_argument(
        "--skip-mixed",
        action="store_true",
        help="run only the holomorphic and functional subcertificate",
    )
    args = parser.parse_args()

    coordinates, metadata = CODEC.read_certificate(args.certificate)
    certificate_hash = hashlib.sha256(
        args.certificate.read_bytes()
    ).hexdigest()
    if args.certificate.resolve() == DEFAULT_CERTIFICATE.resolve():
        assert certificate_hash == EXPECTED_CERTIFICATE_SHA256
    hol = audit_holomorphic_blocks(coordinates)
    trace, objective = audit_functionals(coordinates)
    trace_digest = rational_digest(trace)
    objective_digest = rational_digest(objective)
    if args.certificate.resolve() == DEFAULT_CERTIFICATE.resolve():
        assert trace_digest == EXPECTED_TRACE_DIGEST
        assert objective_digest == EXPECTED_OBJECTIVE_DIGEST

    print("certificate sha256:", certificate_hash)
    print("holomorphic exact PD blocks:", hol["nonzero_blocks"])
    print("holomorphic total supported rank:", hol["total_rank"])
    print("largest exact PD block:", hol["maximum_dimension"])
    print("largest final-minor digit count:",
          hol["maximum_last_minor_digits"])
    print("trace digest:", trace_digest)
    print("objective digest:", objective_digest)
    print("trace decimal:", float(trace))
    print("objective decimal:", float(objective))

    if args.skip_mixed:
        print("mixed checks explicitly skipped")
        return

    FACE = import_file("dth_full_face_final",
                       HERE / "agent_dth_full_face_crt.py")
    MIXED = import_file("dth_mixed_psd_final",
                        HERE / "agent_dth_mixed_psd.py")
    mixed_coordinates = FACE.verify_coordinates(coordinates)
    MIXED.verify_coordinates(mixed_coordinates, certificate_hash)
    print("exact corrected first-level DTH pseudomoment obstruction passed")


if __name__ == "__main__":
    main()
