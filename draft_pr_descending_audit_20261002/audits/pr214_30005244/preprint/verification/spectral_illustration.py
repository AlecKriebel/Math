"""Independent adversarial finite-block check of the abstract spectral claim.

This is a reproducible illustration, not the proof. The proof and exact infinite
operator counterexamples are in INDEPENDENT_RECONSTRUCTION.md. The moving third
coordinate represents e_n in l2, not a fixed coordinate in the limiting space.
"""

from fractions import Fraction
import json
import numpy as np


def opnorm(a):
    return float(np.linalg.norm(a, 2))


def projection(a, center=2j, radius=0.5, points=2048):
    eye = np.eye(len(a), dtype=complex)
    result = np.zeros_like(a, dtype=complex)
    for k in range(points):
        phase = np.exp(2j * np.pi * k / points)
        z = center + radius * phase
        result += radius * phase * np.linalg.inv(z * eye - a)
    return result / points


def main():
    # Exact resolvent calculation for B_n=|e_n><e_n|, B=0 at z=2.
    exact_static_resolvent_gap = Fraction(1, 2 - 1) - Fraction(1, 2)
    assert exact_static_resolvent_gap == Fraction(1, 2)

    # K X_n=X_n for X_n=|e_1><e_n|, K=|e_1><e_1|.
    x = np.array([[0., 1.], [0., 0.]])
    k = np.diag([1., 0.])
    assert np.array_equal(k @ x, x)
    assert opnorm(k @ x) == 1
    assert np.array_equal(x @ k, np.zeros((2, 2)))

    # Fixed rank-two compact limit with a defective eigenvalue 2i.
    limit = np.array([[2j, 1, 0], [0, 2j, 0], [0, 0, 0]], dtype=complex)
    p = np.diag([1., 1., 0.])
    static_moving = np.diag([0., 0., 1.])
    rows = []
    for denom in (16, 64, 256, 1024, 4096):
        epsilon = 1 / denom
        compact_error = epsilon * np.array(
            [[0., 0., 1.], [1., 0., 0.], [0., 1., 0.]])
        a = limit + static_moving + compact_error
        eigenvalues = np.linalg.eigvals(a)
        count = int(sum(abs(z - 2j) < .5 for z in eigenvalues))
        pn = projection(a)
        pn2 = projection(a, points=4096)
        gap = opnorm(pn - p)
        full_gap = opnorm(np.linalg.inv(3j*np.eye(3)-a)
                          - np.linalg.inv(3j*np.eye(3)-limit))
        assert count == 2
        assert opnorm(pn @ pn - pn) < 1e-11
        assert abs(np.trace(pn).real - 2) < 1e-11
        assert abs(np.trace(pn).imag) < 1e-11
        assert opnorm(pn - pn2) < 1e-11
        assert gap < 2 * epsilon
        assert full_gap > .1
        rows.append({
            "epsilon": epsilon,
            "compact_error_norm": opnorm(compact_error),
            "cluster_eigenvalues": [[float(z.real), float(z.imag)]
                                    for z in eigenvalues if abs(z-2j)<.5],
            "cluster_algebraic_multiplicity": count,
            "riesz_projection_norm_gap": gap,
            "full_resolvent_norm_gap_at_3i": full_gap,
            "contour_double_resolution_gap": opnorm(pn-pn2),
        })

    return {
        "purpose": "Adversarial finite-block illustration; not a proof certificate",
        "exact_static_resolvent_norm_gap": str(exact_static_resolvent_gap),
        "right_compact_product_counterexample_norm": 1,
        "defective_cluster_rows": rows,
        "all_assertions_passed": True,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
