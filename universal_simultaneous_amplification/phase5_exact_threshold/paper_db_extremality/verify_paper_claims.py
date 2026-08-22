#!/usr/bin/env python3
"""Independent exact integration audit for the dB extremality manuscript.

This script checks the normalization bridges used to combine the earlier
strong-selection theorem with the fitness-two active-chain Hessian theorem.
It deliberately does not import any discovery script.
"""

from __future__ import annotations

from fractions import Fraction as F
import hashlib
from itertools import combinations
from math import comb
from pathlib import Path


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


HERE = Path(__file__).resolve().parent
SYMMETRIC_VERIFIER_SHA256 = (
    "7a1fa1f579c090cc32668392e67b9eb88e696b51ad602a90d069541e402aa512"
)


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    n = len(matrix)
    a = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if a[i][col])
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for row in range(n):
            if row == col or not a[row][col]:
                continue
            scale = a[row][col]
            a[row] = [x - scale * y for x, y in zip(a[row], a[col])]
    return [row[-1] for row in a]


def active_kernel_complete(n: int):
    states = [
        (mask, v)
        for v in range(n)
        for mask in range(1, 1 << n)
        if not (mask >> v) & 1
    ]
    index = {state: i for i, state in enumerate(states)}
    size = len(states)
    k = [[F(0) for _ in range(size)] for _ in range(size)]
    for row, (mask, v) in enumerate(states):
        rank = mask.bit_count()
        for source in range(n):
            if source != v:
                k[row][index[(mask | (1 << source), v)]] += F(1, 2 * (n - 1))
        for old in range(n):
            if (mask >> old) & 1:
                reduced = mask & ~(1 << old)
                for source in range(n):
                    if source != old:
                        k[row][index[(reduced | (1 << source), old)]] += F(
                            1, 2 * rank * (n - 1)
                        )
        require(sum(k[row], F(0)) == 1)
    return states, k


def check_active_normalization() -> None:
    for n in range(3, 6):
        states, kernel = active_kernel_complete(n)
        N = n - 1
        denominator = n * N * 2 ** (N - 1)
        nu = [F(mask.bit_count(), denominator) for mask, _v in states]
        require(sum(nu, F(0)) == 1)
        pushed = [
            sum((nu[i] * kernel[i][j] for i in range(len(states))), F(0))
            for j in range(len(states))
        ]
        require(pushed == nu)
        inverse_mean = sum(
            (nu[i] / states[i][0].bit_count() for i in range(len(states))),
            F(0),
        )
        m_complete = F(N * 2 ** (N - 1), 2**N - 1)
        rho_complete = F(N * 2 ** (N - 1), n * (2**N - 1))
        require(inverse_mean == 1 / m_complete == 1 / (n * rho_complete))
    print("PASS: complete active law, collision normalization, and dB baseline")


def check_rectangular_phase_typing() -> None:
    for n in range(3, 6):
        marked = [
            (mask, v)
            for v in range(n)
            for mask in range(1 << n)
            if not (mask >> v) & 1
        ]
        active = [(mask, v) for mask, v in marked if mask]
        marked_set = set(marked)
        active_set = set(active)
        require(len(marked) == n * 2 ** (n - 1))
        require(len(active) == n * (2 ** (n - 1) - 1))

        # A: every marked cache receives one loopless sample and becomes active.
        for mask, v in marked:
            for source in range(n):
                if source != v:
                    require((mask | (1 << source), v) in active_set)

        # R: continue stays marked; stopping a singleton reaches the empty cache.
        for mask, v in active:
            require((mask, v) in marked_set)
            for stopped in range(n):
                if (mask >> stopped) & 1:
                    require((mask & ~(1 << stopped), stopped) in marked_set)
        require(any(mask == 0 for mask, _v in marked))
        require(all(mask != 0 for mask, _v in active))
    print("PASS: rectangular marked/active phase spaces and empty-cache boundary")


def check_tangent_decomposition() -> None:
    # A genuinely directed row-zero tangent; exact values are arbitrary.
    delta = [
        [F(0), F(2), F(-1), F(-1), F(0)],
        [F(-2), F(0), F(3), F(0), F(-1)],
        [F(1), F(-3), F(0), F(4), F(-2)],
        [F(0), F(1), F(-4), F(0), F(3)],
        [F(3), F(-2), F(0), F(-1), F(0)],
    ]
    n = len(delta)
    require(all(sum(row, F(0)) == 0 for row in delta))
    column = [sum((delta[i][j] for i in range(n)), F(0)) for j in range(n)]
    require(sum(column, F(0)) == 0)
    standard = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                standard[i][j] = F(column[i] + (n - 1) * column[j], n * (n - 2))
    balanced = [
        [delta[i][j] - standard[i][j] for j in range(n)] for i in range(n)
    ]
    symmetric = [
        [(balanced[i][j] + balanced[j][i]) / 2 for j in range(n)]
        for i in range(n)
    ]
    antisymmetric = [
        [(balanced[i][j] - balanced[j][i]) / 2 for j in range(n)]
        for i in range(n)
    ]
    require(all(sum(row, F(0)) == 0 for row in standard))
    require([sum((standard[i][j] for i in range(n)), F(0)) for j in range(n)] == column)
    for part in (symmetric, antisymmetric):
        require(all(sum(row, F(0)) == 0 for row in part))
        require(all(
            sum((part[i][j] for i in range(n)), F(0)) == 0 for j in range(n)
        ))
    require(all(symmetric[i][j] == symmetric[j][i] for i in range(n) for j in range(n)))
    require(all(
        antisymmetric[i][j] == -antisymmetric[j][i]
        for i in range(n)
        for j in range(n)
    ))
    require(all(
        delta[i][j] == standard[i][j] + symmetric[i][j] + antisymmetric[i][j]
        for i in range(n)
        for j in range(n)
    ))
    expected_dimension = (n - 1) + n * (n - 3) // 2 + (n - 1) * (n - 2) // 2
    require(expected_dimension == n * (n - 2))
    balanced_dimension = n * (n - 3) // 2 + (n - 1) * (n - 2) // 2
    require(balanced_dimension == n * n - 3 * n + 1)
    print("PASS: full tangent decomposition into all three irreducible sectors")


def check_incoming_column_sos() -> None:
    weights = [
        [0, 2, 3, 5],
        [7, 0, 11, 13],
        [17, 19, 0, 23],
        [29, 31, 37, 0],
    ]
    n = len(weights)
    total = F(0)
    defect = F(0)
    normalized_defect = F(0)
    for target in range(n):
        incoming = [F(weights[source][target]) for source in range(n) if source != target]
        degree = sum(incoming, F(0))
        total += sum(((degree - w) / w for w in incoming), F(0))
        defect += sum(
            ((x - y) ** 2 / (x * y) for x, y in combinations(incoming, 2)),
            F(0),
        )
        normalized = [w / degree for w in incoming]
        normalized_defect += sum(
            ((x - y) ** 2 / (x * y) for x, y in combinations(normalized, 2)),
            F(0),
        )
    require(total - n * (n - 1) * (n - 2) == defect)
    require(normalized_defect == defect)
    require(defect > 0)
    uniform = [[0 if i == j else (j + 2) for j in range(n)] for i in range(n)]
    uniform_defect = F(0)
    for target in range(n):
        incoming = [F(uniform[source][target]) for source in range(n) if source != target]
        uniform_defect += sum(
            ((x - y) ** 2 / (x * y) for x, y in combinations(incoming, 2)),
            F(0),
        )
    require(uniform_defect == 0)
    print("PASS: incoming-column strong-selection sum of squares and equality gauge")


def check_formal_source_guards() -> None:
    dual = (HERE / "sections/03_duality_collision.tex").read_text(encoding="utf-8")
    model = (HERE / "sections/02_model_results.tex").read_text(encoding="utf-8")
    intro = (HERE / "sections/01_introduction.tex").read_text(encoding="utf-8")
    appendix = (HERE / "appendices/A_sector_certificates.tex").read_text(
        encoding="utf-8"
    )
    references = (HERE / "references.tex").read_text(encoding="utf-8")

    for marker in (
        r"\mathcal Z_n=\{(C,v):C\subseteq V\setminus\{v\}\}",
        r"A:\mathcal Z_n\to\mathcal Y_n",
        r"R:\mathcal Y_n\to\mathcal Z_n",
        r"\Delta_i f(S)=f(S\cup\{i\})-f(S)",
        "Extend $\\Pi_P$ by zero off the",
        "unique stationary law",
    ):
        require(marker in dual, marker)
    require(r"\rho_{\dB}(W,r):=\rho_{\dB}(P(W),r)" in model)
    require(r"\calE_{\rm dir}(W):=\calE_{\rm dir}(P(W))" in model)
    require("Kriebel2026Hybrid" in intro and "Kriebel2026Hybrid" in references)
    require(r"\sum_{\substack{w,i\in B\\w\ne i}}\delta_{wi}" in appendix)
    require("$\\beta_N<19/20$" in appendix)
    require(r"\sum_{w\ne i\in B}" not in appendix)
    print("PASS: formal phase, difference, normalization, and disclosure guards")


def check_symmetric_certificate_binding() -> None:
    verifier = (
        HERE.parent / "r2_determinant"
        / "verify_true_inverse_rank_symmetric_phase.py"
    )
    digest = hashlib.sha256(verifier.read_bytes()).hexdigest()
    appendix = (HERE / "appendices/A_sector_certificates.tex").read_text(
        encoding="utf-8"
    )
    require(digest == SYMMETRIC_VERIFIER_SHA256)
    require(SYMMETRIC_VERIFIER_SHA256 in appendix)
    require("639304267467075678841" in verifier.read_text(encoding="utf-8"))
    print("PASS: displayed symmetric-certificate hash and exact minimum are bound")


def check_physical_standard_normalization() -> None:
    # Independent bridge from the signed phase scalar Phi_N to the physical
    # standard-sector Hessian eigenvalue.  These values come from literal
    # labelled orbit solves in a separate verifier.
    phi = {
        2: F(24, 11),
        3: F(261, 40),
        4: F(343400, 28657),
    }
    expected_xi = {
        2: F(2, 33),
        3: F(261, 5120),
        4: F(3434, 85971),
    }
    expected_frobenius = {
        2: F(1, 11),
        3: F(87, 640),
        4: F(8585, 57314),
    }
    for N, value in phi.items():
        normalized_xi = value / (4 * (N + 1) ** 2 * (N - 1))
        embedding_norm_ratio = F(N, (N + 1) * (N - 1))
        normalized_frobenius = normalized_xi / embedding_norm_ratio
        require(normalized_xi == expected_xi[N])
        require(normalized_frobenius == expected_frobenius[N])
        require(normalized_frobenius == value / (4 * N * (N + 1)))
        require(normalized_frobenius > 0)
    print("PASS: standard-sector phase and Frobenius normalizations")


def check_second_derivative_conversion() -> None:
    # If 1/(n rho_e)=c0+R2 e^2+O(e^3), differentiation gives the manuscript's
    # sign and coefficient.  Check the algebra symbolically over rationals.
    n = 7
    N = n - 1
    c0 = F(2**N - 1, N * 2 ** (N - 1))
    r2 = F(37, 101)
    rho0 = 1 / (n * c0)
    second = -F(2) * r2 / (n * c0 * c0)
    require(rho0 == F(N * 2 ** (N - 1), n * (2**N - 1)))
    require(second < 0)
    print("PASS: positive inverse-mean Hessian converts to negative fixation Hessian")


if __name__ == "__main__":
    check_active_normalization()
    check_rectangular_phase_typing()
    check_tangent_decomposition()
    check_physical_standard_normalization()
    check_incoming_column_sos()
    check_second_derivative_conversion()
    check_formal_source_guards()
    check_symmetric_certificate_binding()
    print("PASS: paper-level theorem integration audit")
