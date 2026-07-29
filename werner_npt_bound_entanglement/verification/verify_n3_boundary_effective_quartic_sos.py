#!/usr/bin/env python3
"""Verify the exact Lyapunov--Schmidt quartic SOS certificate.

Besides checking the positive Gram representation, this verifier rebuilds
the effective quartic from the independently certified raw kernel quartic
and the stored exact mixed-cubic forms:

    q_eff = q_raw - sum_j ell_j^2 / (4 h_j).

It uses only the Python standard library.
"""

from collections import defaultdict
from fractions import Fraction
import importlib.util
import json
from pathlib import Path

from verify_n3_boundary_flat_quartic_sos import verify_certificate


ROOT = Path(__file__).resolve().parent
CERTIFICATE = (
    ROOT
    / "certificates"
    / "n3_boundary_effective_quartic_sos.json"
)
RAW_CERTIFICATE = (
    ROOT
    / "certificates"
    / "n3_boundary_flat_quartic_sos.json"
)
DERIVATION = ROOT / "derive_n3_boundary_effective_quartic.py"


def polynomial(data):
    return {
        tuple(indices): Fraction(*coefficient)
        for indices, coefficient in data
    }


def verify_reduction() -> None:
    certificate = json.loads(CERTIFICATE.read_text())
    raw_certificate = json.loads(RAW_CERTIFICATE.read_text())
    assert raw_certificate["format"] == "n3-flat-kernel-rational-face-v2"

    reconstructed = defaultdict(Fraction)
    reconstructed.update(polynomial(raw_certificate["quartic_terms"]))
    reductions = certificate["lyapunov_schmidt"]
    assert len(reductions) == 149
    for reduction in reductions:
        hessian_diagonal = Fraction(*reduction["hessian_diagonal"])
        assert hessian_diagonal > 0
        form = polynomial(reduction["mixed_quadratic_form"])
        assert all(len(monomial) == 2 for monomial in form)
        for first_monomial, first_coefficient in form.items():
            for second_monomial, second_coefficient in form.items():
                monomial = tuple(sorted(first_monomial + second_monomial))
                reconstructed[monomial] -= (
                    first_coefficient
                    * second_coefficient
                    / (4 * hessian_diagonal)
                )
    reconstructed = {
        monomial: coefficient
        for monomial, coefficient in reconstructed.items()
        if coefficient
    }
    target = polynomial(certificate["quartic_terms"])
    assert reconstructed == target
    print(
        "verified exact Lyapunov--Schmidt reduction:",
        len(reductions),
        "positive Hessian pivots and",
        sum(
            len(reduction["mixed_quadratic_form"])
            for reduction in reductions
        ),
        "mixed-cubic terms",
    )


def verify_chart_derivation() -> None:
    specification = importlib.util.spec_from_file_location(
        "exact_chart_derivation", DERIVATION
    )
    derivation = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(derivation)
    hessian, _, pivots, raw, forms, effective = derivation.derive()

    certificate = json.loads(CERTIFICATE.read_text())
    raw_certificate = json.loads(RAW_CERTIFICATE.read_text())
    assert raw == polynomial(raw_certificate["quartic_terms"])
    assert effective == polynomial(certificate["quartic_terms"])

    reductions = certificate["lyapunov_schmidt"]
    assert len(reductions) == len(pivots) == len(forms) == 149
    for pivot, form, reduction in zip(pivots, forms, reductions):
        assert reduction["pivot_coordinate"] == pivot
        assert (
            Fraction(*reduction["hessian_diagonal"])
            == hessian[pivot][pivot]
        )
        assert (
            polynomial(reduction["mixed_quadratic_form"])
            == form
        )
    print(
        "verified chart-to-Q derivation:",
        len(hessian),
        "Hessian coordinates,",
        len(pivots),
        "positive pivots,",
        len(raw),
        "raw quartic terms, and",
        len(effective),
        "effective quartic terms",
    )


if __name__ == "__main__":
    verify_chart_derivation()
    verify_reduction()
    verify_certificate(
        CERTIFICATE,
        "n3-flat-kernel-effective-rational-face-v1",
    )
