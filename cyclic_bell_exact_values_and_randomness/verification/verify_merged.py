#!/usr/bin/env python3
"""Dependency-free hostile regressions for the merged cyclic-Bell manuscript.

The checks here are deliberately redundant with the analytic proofs.  They use
only the Python standard library, avoid numerical eigensolvers, and exercise
both admissible constructions and tempting hypotheses that must fail.
"""

from __future__ import annotations

import cmath
import itertools
import math
import random
import sys
from fractions import Fraction


TOL = 2.0e-9


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_close(actual: complex, expected: complex, message: str, tol: float = TOL) -> None:
    error = abs(actual - expected)
    if error > tol:
        raise AssertionError(
            f"{message}: got {actual!r}, expected {expected!r}, error {error:.3e}"
        )


def roots_and_phases(d: int):
    omega = cmath.exp(2j * math.pi / d)
    eta = cmath.exp(1j * math.pi / d)
    delta = 1 if d % 2 == 0 else 0
    roots = [eta ** (2 * k + delta) for k in range(d)]
    phases = []
    for y in range(d):
        row = []
        for z in roots:
            value = 1 + omega**y * z
            require(abs(value) > 1.0e-12, f"unexpected vanishing scalar factor at d={d}, y={y}")
            row.append(value / abs(value))
        phases.append(row)
    return omega, eta, delta, roots, phases


def scalar_value(d: int, z: complex) -> float:
    omega = cmath.exp(2j * math.pi / d)
    return sum(abs(1 + omega**y * z) for y in range(d))


def scalar_target(d: int) -> float:
    return 2.0 / math.sin(math.pi / (2 * d))


def test_scalar_extremum_and_equality_roots() -> str:
    checked_grid_points = 0
    for d in range(2, 21):
        _, _, _, roots, _ = roots_and_phases(d)
        target = scalar_target(d)
        polynomial_target = (-1) ** (d - 1)

        require(len({round(cmath.phase(z), 12) for z in roots}) == d, f"repeated equality root at d={d}")
        product = 1 + 0j
        for k, z in enumerate(roots):
            require_close(abs(z), 1.0, f"root off unit circle at d={d}, k={k}")
            require_close(z**d, polynomial_target, f"wrong equality polynomial at d={d}, k={k}")
            require_close(scalar_value(d, z), target, f"scalar equality value at d={d}, k={k}")
            product *= z
        require_close(product, 1.0, f"product of equality roots at d={d}", 2.0e-8)

        # Midpoints between consecutive equality phases are strict nonmaximizers.
        equality_offset = (math.pi / d) if d % 2 == 0 else 0.0
        for k in range(d):
            theta = equality_offset + 2 * math.pi * k / d + math.pi / d
            midpoint = cmath.exp(1j * theta)
            require(
                scalar_value(d, midpoint) < target - 1.0e-7,
                f"non-equality midpoint appears maximizing at d={d}, k={k}",
            )

        # A grid checks the global inequality independently of the root list.
        grid_size = 64 * d + 1
        for n in range(grid_size):
            z = cmath.exp(2j * math.pi * (n + 0.317) / grid_size)
            require(
                scalar_value(d, z) <= target + 2.0e-10,
                f"sampled scalar bound violation at d={d}, sample={n}",
            )
        checked_grid_points += grid_size
    return f"scalar extremum/equality roots d=2..20 ({checked_grid_points} hostile grid points)"


# Minimal dense-matrix helpers, used only for the singular polar-factor test.
def eye(n: int):
    return [[1.0 + 0j if i == j else 0j for j in range(n)] for i in range(n)]


def matmul(a, b):
    rows, inner, cols = len(a), len(b), len(b[0])
    require(len(a[0]) == inner, "matrix dimension mismatch")
    return [
        [sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(cols)]
        for i in range(rows)
    ]


def dagger(a):
    return [[a[i][j].conjugate() for i in range(len(a))] for j in range(len(a[0]))]


def matsub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matadd(*matrices):
    return [
        [sum(matrix[i][j] for matrix in matrices) for j in range(len(matrices[0][0]))]
        for i in range(len(matrices[0]))
    ]


def matscale(scalar: complex, a):
    return [[scalar * entry for entry in row] for row in a]


def kron(a, b):
    return [
        [a[i][j] * b[r][s] for j in range(len(a[0])) for s in range(len(b[0]))]
        for i in range(len(a))
        for r in range(len(b))
    ]


def matrix_error(a, b) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[0])))


def test_nonunitary_partial_isometry_polar_identity() -> str:
    # C=V|C| has rank one.  V is a proper partial isometry, not a unitary
    # masquerading as one on an invertible example.
    c = [[0j, 2.0 + 0j], [0j, 0j]]
    v = [[0j, 1.0 + 0j], [0j, 0j]]
    abs_c = [[0j, 0j], [0j, 2.0 + 0j]]
    abs_c_dagger = [[2.0 + 0j, 0j], [0j, 0j]]
    root_two = math.sqrt(2.0)
    sqrt_abs_c = [[0j, 0j], [0j, root_two + 0j]]
    sqrt_abs_c_dagger = [[root_two + 0j, 0j], [0j, 0j]]
    b = [[1.0 + 0j, 0j], [0j, 1j]]
    identity = eye(2)

    require(matrix_error(matmul(v, abs_c), c) < TOL, "C=V|C| failed")
    initial_projection = matmul(dagger(v), v)
    final_projection = matmul(v, dagger(v))
    require(matrix_error(initial_projection, identity) > 0.5, "V accidentally unitary on its initial side")
    require(matrix_error(final_projection, identity) > 0.5, "V accidentally unitary on its final side")
    require(
        matrix_error(matmul(initial_projection, initial_projection), initial_projection) < TOL,
        "V*V is not a projection",
    )
    require(
        matrix_error(matmul(final_projection, final_projection), final_projection) < TOL,
        "VV* is not a projection",
    )
    require(matrix_error(matmul(matmul(v, dagger(v)), v), v) < TOL, "partial-isometry identity failed")

    p = matsub(
        kron(sqrt_abs_c_dagger, identity),
        kron(matmul(v, sqrt_abs_c), b),
    )
    positive_factor = matscale(0.5, matmul(dagger(p), p))
    expanded = matscale(
        0.5,
        matadd(
            kron(abs_c_dagger, identity),
            kron(abs_c, identity),
            matscale(-1.0, kron(c, b)),
            matscale(-1.0, kron(dagger(c), dagger(b))),
        ),
    )
    require(
        matrix_error(positive_factor, expanded) < 5.0e-12,
        "polar positive-factor identity failed on a singular C",
    )
    return "polar positive-factor identity with a genuinely nonunitary partial isometry"


def product(values) -> complex:
    answer = 1 + 0j
    for value in values:
        answer *= value
    return answer


def check_weighted_cycle_order(weights, label: str) -> None:
    """Apply X diag(weights) d times to every basis vector."""
    d = len(weights)
    require(
        all(abs(abs(weight) - 1.0) < TOL for weight in weights),
        f"weighted cycle is not unitary: {label}",
    )
    for start in range(d):
        position = start
        amplitude = 1 + 0j
        for _ in range(d):
            amplitude *= weights[position]
            position = (position + 1) % d
        require(position == start, f"weighted cycle did not close: {label}, start={start}")
        require_close(amplitude, 1.0, f"weighted cycle is not order d: {label}, start={start}", 2.0e-8)


def permutation_orders(d: int):
    candidates = [tuple(range(d)), tuple(reversed(range(d)))]
    if d >= 4:
        candidates.append(tuple(list(range(d - 2)) + [d - 1, d - 2]))
    for seed in range(4):
        order = list(range(d))
        random.Random(104729 * d + seed).shuffle(order)
        candidates.append(tuple(order))
    seen = set()
    answer = []
    for order in candidates:
        if order not in seen:
            seen.add(order)
            answer.append(order)
    return answer


def first_family_score(d: int, root_order, phase_order=None) -> float:
    omega, _, _, roots, phases = roots_and_phases(d)
    if phase_order is None:
        phase_order = root_order
    bell = 0.0
    for y in range(d):
        correlator = sum(
            (1 + omega**y * roots[root_order[j]])
            * phases[y][phase_order[j]].conjugate()
            for j in range(d)
        ) / d
        bell += correlator.real
    return bell


def first_harmonics(d: int, order):
    _, _, _, roots, phases = roots_and_phases(d)
    a0 = []
    a1 = []
    for y in range(d):
        a0.append(sum(phases[y][order[j]].conjugate() for j in range(d)) / d)
        a1.append(
            sum(
                roots[order[j]] * phases[y][order[j]].conjugate()
                for j in range(d)
            )
            / d
        )
    return a0, a1


def test_first_family_weighted_shifts() -> str:
    tested = 0
    for d in range(2, 21):
        omega, _, _, roots, phases = roots_and_phases(d)
        baseline_a0, baseline_a1 = first_harmonics(d, tuple(range(d)))
        target = scalar_target(d)
        for order in permutation_orders(d):
            require(sorted(order) == list(range(d)), f"nonpermutation entered admissible suite at d={d}")
            ordered_roots = [roots[k] for k in order]
            check_weighted_cycle_order([1.0 + 0j] * d, f"A0,d={d}")
            check_weighted_cycle_order(ordered_roots, f"A1,d={d},order={order}")
            for y in range(d):
                v_weights = [phases[y][k] for k in order]
                b_weights = [value.conjugate() for value in v_weights]
                check_weighted_cycle_order(v_weights, f"V{y},d={d},order={order}")
                check_weighted_cycle_order(b_weights, f"B{y},d={d},order={order}")
                for j in range(d):
                    scalar = 1 + roots[order[j]] * omega**y
                    require_close(
                        scalar * v_weights[j].conjugate(),
                        abs(scalar),
                        f"incorrect equality-phase pairing at d={d}, y={y}, edge={j}",
                    )

            score = first_family_score(d, order)
            require_close(score, target, f"first-family exact score at d={d}, order={order}", 2.0e-8)
            require_close(score + 1.0, target + 1.0, f"first augmented score at d={d}", 2.0e-8)
            a0, a1 = first_harmonics(d, order)
            for y in range(d):
                require_close(a0[y], baseline_a0[y], f"permutation changed <A0 B{y}> at d={d}")
                require_close(a1[y], baseline_a1[y], f"permutation changed <A1 B{y}> at d={d}")
            tested += 1
    return f"weighted-shift order/admissibility and first-family score ({tested} prime/composite strategies)"


def target_fourier_norms(d: int, order):
    omega, _, _, roots, _ = roots_and_phases(d)
    q = [1.0 + 0j]
    for j in range(d - 1):
        q.append(q[-1] * roots[order[j]])
    require_close(q[-1] * roots[order[-1]], 1.0, f"target cycle failed to close at d={d}", 2.0e-8)
    transforms = [sum(q[j] * omega ** (m * j) for j in range(d)) for m in range(d)]
    norms = [abs(value) ** 2 for value in transforms]
    return q, norms


def test_small_dimension_exhaustive_flatness() -> str:
    tested = 0
    for d in (2, 3):
        target = scalar_target(d)
        for order in itertools.permutations(range(d)):
            require_close(first_family_score(d, order), target, f"small-d score at d={d}, order={order}")
            _, norms = target_fourier_norms(d, order)
            for m, norm in enumerate(norms):
                require_close(norm, d, f"nonflat small-d target at d={d}, order={order}, m={m}")
            probabilities = [norm / d**3 for norm in norms]
            require(
                all(abs(p - 1 / d**2) < TOL for p in probabilities),
                f"small-d output law not uniform at d={d}, order={order}",
            )
            tested += 1
    return f"exhaustive d=2,3 permutation flatness ({tested} permutations)"


def test_final_two_bias_and_guessing_bound() -> str:
    for d in range(4, 21):
        _, _, _, roots, _ = roots_and_phases(d)
        order = tuple(list(range(d - 2)) + [d - 1, d - 2])
        q, norms = target_fourier_norms(d, order)
        require_close(sum(norms), d**2, f"Fourier Parseval normalization at d={d}", 3.0e-8)

        # p(a,b)=|qhat_{-(a+b)}|^2/d^3; each norm occurs once in every row.
        probabilities = [norm / d**3 for norm in norms]
        require_close(d * sum(probabilities), 1.0, f"joint-law normalization at d={d}")
        for _a in range(d):
            require_close(sum(probabilities), 1.0 / d, f"Alice marginal at d={d}")
        max_probability = max(probabilities)
        require(max_probability > 1.0 / d**2 + 1.0e-10, f"final-two law unexpectedly flat at d={d}")

        r2 = sum(q[(j + 2) % d] * q[j].conjugate() for j in range(d))
        exact_r2 = (roots[d - 1] - roots[d - 2]) * (roots[d - 3] - roots[0])
        require_close(r2, exact_r2, f"lag-two autocorrelation certificate at d={d}", 3.0e-8)
        require_close(
            abs(r2),
            4 * math.sin(math.pi / d) * math.sin(3 * math.pi / d),
            f"lag-two magnitude at d={d}",
            3.0e-8,
        )
        lower_bound = (
            1.0 / d**2
            + 2 * math.sin(math.pi / d) * math.sin(3 * math.pi / d) / (d**2 * (d - 1))
        )
        require(
            max_probability + 2.0e-12 >= lower_bound,
            f"guessing-probability lower bound failed at d={d}",
        )

        if d == 4:
            for actual, exact in zip(norms, (2.0, 6.0, 2.0, 6.0)):
                require_close(actual, exact, "exact d=4 Fourier certificate", 2.0e-10)
            require_close(max_probability, Fraction(3, 32), "exact d=4 guessing probability")
    return "final-two nonuniformity, d=4 exact certificate, and guessing lower bound d=4..20"


def test_expected_hypothesis_failures() -> str:
    # Correct root multiset but the Bob phases are paired to the wrong cycle
    # edges: all observables remain order d, yet exact saturation is lost.
    d = 4
    final_two = (0, 1, 3, 2)
    canonical = tuple(range(d))
    target = scalar_target(d)
    mismatched = first_family_score(d, final_two, canonical)
    require(target - mismatched > 0.5, "mismatched root/phase pairing did not lose the Bell maximum")

    # Repeating a maximizing scalar label can formally keep every summand at
    # its scalar maximum, but it destroys the order-d measurement relation.
    _, _, _, roots, _ = roots_and_phases(d)
    repeated = (0, 1, 3, 3)
    require_close(first_family_score(d, repeated), target, "repeated-label formal scalar score")
    require(abs(product(roots[k] for k in repeated) - 1.0) > 0.5, "repeated labels accidentally admissible")

    # Product preservation alone is not equality: move two roots in opposite
    # directions so A1^d=I survives, then pair each moved root optimally.
    d = 5
    omega, _, _, roots, _ = roots_and_phases(d)
    moved = roots[:]
    epsilon = 0.08
    moved[0] *= cmath.exp(1j * epsilon)
    moved[1] *= cmath.exp(-1j * epsilon)
    require_close(product(moved), 1.0, "off-equality product-preserving perturbation")
    moved_score = sum(
        sum(abs(1 + omega**y * z) for y in range(d)) / d
        for z in moved
    )
    require(scalar_target(d) - moved_score > 1.0e-3, "off-equality roots retained the scalar maximum")
    return "expected failures: mismatched pairing, repeated labels, and off-equality phases"


def second_family_parameters(d: int, ell: int):
    _, eta, delta, _, _ = roots_and_phases(d)
    sign = -1 if (ell - 1) % 2 else 1
    lam = sign * eta ** (ell * (ell - 1)) / (
        d * math.sin(math.pi * (ell - 0.5) / d)
    )
    chi = eta ** (-ell * (ell - 1 + delta))
    return lam, chi


def test_second_family_fourier_sos() -> str:
    tested = 0
    for d in range(2, 21):
        omega, _, _, _, phases = roots_and_phases(d)
        for order in permutation_orders(d):
            b_rows = [[phases[y][order[j]].conjugate() for j in range(d)] for y in range(d)]
            fourier_norm_diagonal = [0.0] * d
            lambda_norm = 0.0
            second_score = 0.0
            total_sos_residual = 0.0
            for ell in range(d):
                lam, chi = second_family_parameters(d, ell)
                lambda_norm += abs(lam) ** 2
                d_weights = [chi * omega ** (-ell * order[j]) for j in range(d)]
                check_weighted_cycle_order(d_weights, f"D{ell},d={d},order={order}")
                check_weighted_cycle_order(
                    [value.conjugate() for value in d_weights],
                    f"A{ell},d={d},order={order}",
                )
                require(
                    all(abs(abs(value) - 1.0) < TOL for value in d_weights),
                    f"D{ell} has a nonunit-modulus edge at d={d}",
                )
                c_weights = [
                    sum(omega ** (ell * y) * b_rows[y][j] for y in range(d))
                    for j in range(d)
                ]
                residuals = [
                    c_weights[j] - d * lam * d_weights[j]
                    for j in range(d)
                ]
                total_sos_residual += sum(abs(value) ** 2 for value in residuals) / d
                require(
                    max(abs(value) for value in residuals) < 3.0e-8,
                    f"second-family Fourier compression failed at d={d}, ell={ell}, order={order}",
                )

                # On |Phi_d>, A_ell=conj(D_ell) gives
                # <A_ell C_ell>=d lambda_ell and P_ell|Phi_d>=0.
                expectation = sum(
                    d_weights[j].conjugate() * c_weights[j] for j in range(d)
                ) / d
                require_close(expectation, d * lam, f"second-family correlator at d={d}, ell={ell}", 4.0e-8)
                second_score += (lam.conjugate() * expectation).real
                for j in range(d):
                    fourier_norm_diagonal[j] += abs(c_weights[j]) ** 2

            require_close(lambda_norm, 1.0, f"second-family lambda normalization at d={d}", 3.0e-8)
            for j, diagonal in enumerate(fourier_norm_diagonal):
                require_close(diagonal, d**2, f"sum C_l^*C_l at d={d}, edge={j}", 8.0e-8)
            require(total_sos_residual < 2.0e-13, f"nonzero SOS residual at d={d}, order={order}")
            require_close(second_score, d, f"second-family exact score at d={d}, order={order}", 7.0e-8)
            require_close(second_score + 1.0, d + 1.0, f"second augmented score at d={d}", 7.0e-8)
            tested += 1
    return f"second-family Fourier compression, order, and SOS saturation d=2..20 ({tested} strategies)"


def test_canonical_fourier_flatness() -> str:
    for d in range(2, 21):
        _, norms = target_fourier_norms(d, tuple(range(d)))
        for m, norm in enumerate(norms):
            require_close(norm, d, f"canonical chirp is not Fourier-flat at d={d}, m={m}", 4.0e-8)
            require_close(norm / d**3, 1.0 / d**2, f"canonical target probability at d={d}, m={m}")
    return "canonical Fourier-flat target distribution d=2..20"


def test_one_input_local_reconstruction() -> str:
    cases = 0
    for d in range(2, 7):
        for settings in range(1, 4):
            raw_alice = [0] + [a + 1 for a in range(1, d)]
            alice_total = sum(raw_alice)
            p_alice = [Fraction(value, alice_total) for value in raw_alice]
            conditional = {}
            for y in range(settings):
                for a in range(d):
                    raw = [1 + ((a + 2 * b + 3 * y) % 7) for b in range(d)]
                    total = sum(raw)
                    conditional[y, a] = [Fraction(value, total) for value in raw]

            behavior = {
                (a, b, y): p_alice[a] * conditional[y, a][b]
                for a in range(d)
                for b in range(d)
                for y in range(settings)
            }
            hidden = {}
            for a in range(d):
                for outputs in itertools.product(range(d), repeat=settings):
                    weight = p_alice[a]
                    for y, b in enumerate(outputs):
                        weight *= conditional[y, a][b]
                    hidden[(a,) + outputs] = weight
            require(sum(hidden.values(), Fraction(0, 1)) == 1, f"local weights not normalized at d={d}")

            for a in range(d):
                for b in range(d):
                    for y in range(settings):
                        reconstructed = sum(
                            weight
                            for label, weight in hidden.items()
                            if label[0] == a and label[1 + y] == b
                        )
                        require(
                            reconstructed == behavior[a, b, y],
                            f"one-input reconstruction failed at d={d}, settings={settings}, a={a}, b={b}, y={y}",
                        )

            # A purifying flag carrying the hidden label predicts both target
            # outputs exactly, so its average guessing probability is one.
            guessing_probability = sum(hidden.values(), Fraction(0, 1))
            require(guessing_probability == 1, f"flagged-Eve guessing probability at d={d}")
            cases += 1
    return f"one-input exact local reconstruction with flagged Eve ({cases} rational behaviors)"


def main() -> int:
    tests = [
        test_scalar_extremum_and_equality_roots,
        test_nonunitary_partial_isometry_polar_identity,
        test_first_family_weighted_shifts,
        test_small_dimension_exhaustive_flatness,
        test_final_two_bias_and_guessing_bound,
        test_expected_hypothesis_failures,
        test_second_family_fourier_sos,
        test_canonical_fourier_flatness,
        test_one_input_local_reconstruction,
    ]
    reports = []
    try:
        for test in tests:
            reports.append(test())
    except Exception as exc:
        print(f"FAIL: merged cyclic-Bell verification: {exc}", file=sys.stderr)
        raise

    print("PASS: merged cyclic-Bell hostile verification")
    for report in reports:
        print(f"  [PASS] {report}")
    print(f"PASS: {len(reports)} independent regression groups; no external dependencies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
