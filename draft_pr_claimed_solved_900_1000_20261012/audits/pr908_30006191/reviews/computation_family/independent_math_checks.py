#!/usr/bin/env python3
"""Independent finite CAR controls. No imports from the frozen candidate.

Exact predicates use integer/rational/symbolic arithmetic. Floating diagnostics
use a stated tolerance and are not rigorous interval enclosures. No assert is
used: checks remain active under Python optimization.
"""
import argparse
import hashlib
import itertools
import json
import math
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import expm
import sympy as sp


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def car_exact(m):
    size = 1 << m
    out = []
    for j in range(m):
        c = sp.zeros(size)
        for occupation in range(size):
            if not (occupation >> j) & 1:
                sign = (-1) ** ((occupation & ((1 << j) - 1)).bit_count())
                c[occupation | (1 << j), occupation] = sign
        out.append(c)
    return out


def dg_exact(h, cs):
    return sum((h[i, j] * cs[i] * cs[j].H
                for i in range(len(cs)) for j in range(len(cs))), sp.zeros(cs[0].rows))


def determinant_slater_exact(gs):
    m, n = gs.shape
    state = sp.zeros(1 << m, 1)
    for occupied in itertools.combinations(range(m), n):
        mask = sum(1 << j for j in occupied)
        state[mask] = gs.extract(occupied, range(n)).det()
    return state


def exact_controls():
    checks = []

    def ck(name, condition, detail=None):
        require(bool(condition), name)
        checks.append({"name": name, "detail": detail})

    for m in range(1, 5):
        cs = car_exact(m)
        identity = sp.eye(1 << m)
        zero = sp.zeros(1 << m)
        number = sum((c * c.H for c in cs), zero.copy())
        ck(f"number_spectrum_m{m}", number == sp.diag(*[s.bit_count() for s in range(1 << m)]))
        for i, j in itertools.product(range(m), repeat=2):
            ck(f"CAR_m{m}_{i}_{j}", cs[i].H * cs[j] + cs[j] * cs[i].H == (identity if i == j else zero))
            ck(f"creation_anticommutator_m{m}_{i}_{j}", cs[i] * cs[j] + cs[j] * cs[i] == zero)
        for sigma in (0, 1):
            density = sum((cs[i] * cs[i].H * cs[j] * cs[j].H
                           for i in range(m) for j in range(m) if sigma == 0 or i != j), zero.copy())
            ck(f"density_self_term_m{m}_sigma{sigma}", density == number * (number - sigma * identity))
        ck(f"wrong_unsigned_creation_detected_m{m}", m == 1 or cs[1][3, 1] == -1)

    m = 4
    cs = car_exact(m)
    # Rational orthonormal frames, with varied occupied and outside projections.
    r = sp.eye(m)
    r[:2, :2] = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                           [sp.Rational(4, 5), sp.Rational(3, 5)]])
    r[2:, 2:] = sp.Matrix([[sp.Rational(5, 13), -sp.Rational(12, 13)],
                           [sp.Rational(12, 13), sp.Rational(5, 13)]])
    s = sp.eye(m)
    s[0, 0] = s[2, 2] = sp.Rational(8, 17)
    s[0, 2] = -sp.Rational(15, 17)
    s[2, 0] = sp.Rational(15, 17)
    for frame_id, frame in enumerate((sp.eye(m), r, s * r)):
        for n in range(0, m + 1):
            gs = frame[:, :n]
            psi = determinant_slater_exact(gs)
            ck(f"Slater_normalized_frame{frame_id}_n{n}", (psi.H * psi)[0] == 1)
            # Independent determinant construction agrees with ordered creators.
            built = sp.zeros(1 << m, 1)
            built[0] = 1
            for j in reversed(range(n)):
                creator = sum((gs[i, j] * cs[i] for i in range(m)), sp.zeros(1 << m))
                built = creator * built
            ck(f"determinant_creator_sign_frame{frame_id}_n{n}", built == psi)
            p = gs * gs.H
            for projection_id, q in enumerate((sp.zeros(m), sp.eye(m),
                                              sp.diag(1, 0, 1, 0),
                                              s * sp.diag(0, 1, 1, 0) * s.H)):
                operator = dg_exact(q, cs)
                mean = (psi.H * operator * psi)[0]
                second = (psi.H * operator * operator * psi)[0]
                lam = sp.trace(p * q)
                variance = sp.trace(p * q) - sp.trace(p * q * p * q)
                tag = f"f{frame_id}_n{n}_q{projection_id}"
                ck("projection_" + tag, q * q == q and q.H == q)
                ck("first_moment_" + tag, mean == lam)
                ck("second_moment_" + tag, sp.simplify(second - lam ** 2 - variance) == 0)
                ck("variance_bound_" + tag, variance >= 0 and variance <= lam)

    # Same-sector correlated state: M is 0 or 3, so Var(M)=9/4>3/2.
    cs6 = car_exact(6)
    q6 = sp.diag(0, 0, 0, 1, 1, 1)
    m6 = dg_exact(q6, cs6)
    correlated = sp.zeros(64, 1)
    correlated[7] = correlated[56] = 1 / sp.sqrt(2)
    mean = (correlated.H * m6 * correlated)[0]
    variance = sp.simplify((correlated.H * m6 * m6 * correlated)[0] - mean ** 2)
    ck("arbitrary_state_Slater_bound_countercontrol", mean == sp.Rational(3, 2) and variance == sp.Rational(9, 4) and variance > mean,
       {"mean": str(mean), "variance": str(variance)})
    # Exact two-mode free cutoff identity detects the sign independently.
    time, integration = sp.symbols('time integration', real=True)
    h2 = sp.Matrix([[0, 1], [1, 0]])
    cutoff = sp.diag(1, 0)
    def u2(value):
        return sp.cos(value) * sp.eye(2) - sp.I * sp.sin(value) * h2
    commutator = h2 * cutoff - cutoff * h2
    lhs = u2(time) * cutoff - cutoff * u2(time)
    integrand = u2(time - integration) * commutator * u2(integration)
    integrated = integrand.applyfunc(lambda expression: sp.integrate(sp.expand_trig(expression), (integration, 0, time)))
    ck('exact_cutoff_Duhamel_sign', (lhs + sp.I * integrated).applyfunc(sp.simplify) == sp.zeros(2))
    ck('wrong_cutoff_Duhamel_sign_detected', (lhs - sp.I * integrated).subs(time, sp.pi / 6).applyfunc(sp.simplify) != sp.zeros(2))
    positive_time, particles = sp.symbols('positive_time particles', positive=True)
    first_integral = sp.integrate(2 * particles * integration * particles ** sp.Rational(5, 6), (integration, 0, positive_time))
    second_integral = sp.integrate(2 * particles * integration ** 2 * particles ** sp.Rational(5, 3), (integration, 0, positive_time))
    ck('exact_comparison_integrals', first_integral == particles ** sp.Rational(11, 6) * positive_time ** 2 and
       second_integral == sp.Rational(2, 3) * particles ** sp.Rational(8, 3) * positive_time ** 3)
    for n in range(0, 13):
        for outside in range(n + 1):
            for sigma in (0, 1):
                actual = (n - outside) * (n - outside - sigma) - n * (n - sigma)
                ck(f"sector_difference_n{n}_M{outside}_s{sigma}", actual == -outside * (2 * n - sigma - outside) and abs(actual) <= 2 * n * outside)
    for n in range(1, 33):
        for sigma in (0, 1):
            delta = (n + 1) * (n + 1 - sigma) - n * (n - sigma)
            t = sp.pi / (2 * n + 1 - sigma)
            ck(f"phase_N{n}_s{sigma}", delta == 2 * n + 1 - sigma and sp.simplify(t * delta - sp.pi) == 0)
            ck(f"uniform_time_sector_ratio_N{n}_s{sigma}", n + 1 <= 2 * n and t <= sp.pi / (2 * n))
    for d in range(1, 9):
        first = -sp.Rational(1, 2) + sp.Rational(1, d)
        second = -1 + sp.Rational(2, d)
        ck(f"dimension_decay_d{d}", (first < 0 and second < 0) == (d > 2),
           {"first": str(first), "second": str(second)})
    ceiling = 1
    for n in range(1, 2001):
        while ceiling ** 3 < n:
            ceiling += 1
        ck(f"packing_ceiling_N{n}", (ceiling - 1) ** 3 < n <= ceiling ** 3 <= 8 * n)
    return {"exact_predicate_count": len(checks), "checks": checks,
            "classification": "finite exact integer/rational/symbolic predicates; not continuum proof"}


def car_numeric(m):
    return [np.array(c.tolist(), dtype=np.complex128) for c in car_exact(m)]


def dg_numeric(h, cs):
    out = np.zeros_like(cs[0])
    for i in range(len(cs)):
        for j in range(len(cs)):
            out += h[i, j] * cs[i] @ cs[j].conj().T
    return out


def determinant_slater_numeric(gs):
    m, n = gs.shape
    out = np.zeros(1 << m, dtype=np.complex128)
    for occupied in itertools.combinations(range(m), n):
        out[sum(1 << j for j in occupied)] = np.linalg.det(gs[list(occupied), :])
    return out


def numeric_controls():
    tolerance = 2e-11
    rows = []
    counter = {"wrong_phase": 0, "wrong_bra": 0, "late_orthogonality": 0,
               "first_moment_as_second_moment": 0, "first_moment_as_M_norm": 0}
    maximum = 0.0

    def close(tag, actual, expected):
        nonlocal maximum
        error = float(np.linalg.norm(np.asarray(actual) - np.asarray(expected)))
        maximum = max(maximum, error)
        require(error <= tolerance, f"{tag}: error={error}")
        rows.append({"name": tag, "absolute_residual": error})

    for m in (4, 5, 6):
        cs = car_numeric(m)
        size = 1 << m
        number = np.diag([s.bit_count() for s in range(size)])
        for seed in (142, 908, 6191):
            rng = np.random.default_rng(seed + 100 * m)
            z = rng.normal(size=(m, m)) + 1j * rng.normal(size=(m, m))
            frame = np.linalg.qr(z)[0]
            h = z + z.conj().T
            f = frame[:, 0]
            a = sum((f[j] * cs[j] for j in range(m)), np.zeros((size, size), dtype=complex))
            kinetic = dg_numeric(h, cs)
            qframe = np.linalg.qr(rng.normal(size=(m, m)) + 1j * rng.normal(size=(m, m)))[0]
            for n in (1, m - 1):
                gs = frame[:, 1:n + 1]
                psi = determinant_slater_numeric(gs)
                xi = a @ psi
                close(f"norms_m{m}_seed{seed}_n{n}", [np.linalg.norm(psi), np.linalg.norm(xi)], [1, 1])
                for rank in (0, 1, m // 2, m):
                    q = qframe[:, :rank] @ qframe[:, :rank].conj().T
                    for time in (0.0, 0.17, 0.83):
                        ugs = expm(-1j * time * h) @ gs
                        state = determinant_slater_numeric(ugs)
                        p = ugs @ ugs.conj().T
                        mop = dg_numeric(q, cs)
                        mean = np.vdot(state, mop @ state).real
                        second = np.vdot(state, mop @ mop @ state).real
                        lam = np.trace(p @ q).real
                        var = np.trace(p @ q).real - np.trace(p @ q @ p @ q).real
                        close(f"moments_m{m}_seed{seed}_n{n}_rank{rank}_t{time}", [mean, second], [lam, lam ** 2 + var])
                        require(var >= -tolerance and var <= lam + tolerance, "numerical Slater variance")
                        if second - mean > 1e-4:
                            counter["first_moment_as_second_moment"] += 1
                        if math.sqrt(max(second, 0)) - mean > 1e-4:
                            counter["first_moment_as_M_norm"] += 1
                for sigma in (0, 1):
                    k = kinetic + number @ (number - sigma * np.eye(size))
                    for time in (0.0, 0.17, 0.83, math.pi / (2 * n + 1 - sigma)):
                        minus = expm(-1j * time * k)
                        actual = np.vdot(xi, minus.conj().T @ a @ minus @ psi)
                        overlap = np.vdot(f, expm(1j * time * h) @ f)
                        expected = np.exp(1j * time * (2 * n + 1 - sigma)) * overlap
                        close(f"creation_matrix_element_m{m}_seed{seed}_n{n}_s{sigma}_t{time}", actual, expected)
                        # These are deliberately wrong formulas; require observed rejection.
                        wrong_phase = np.exp(-1j * time * (2 * n + 1 - sigma)) * overlap
                        wrong_bra = np.vdot(xi, a @ minus @ psi)
                        late_overlap = np.linalg.norm(gs.conj().T @ expm(1j * time * h) @ f)
                        if abs(actual - wrong_phase) > 1e-4:
                            counter["wrong_phase"] += 1
                        if abs(actual - wrong_bra) > 1e-4:
                            counter["wrong_bra"] += 1
                        if late_overlap > 1e-4:
                            counter["late_orthogonality"] += 1
                        annihilator = a.conj().T
                        d = minus.conj().T @ annihilator @ minus - annihilator
                        close(f"creation_annihilation_adjoint_m{m}_seed{seed}_n{n}_s{sigma}_t{time}",
                              np.vdot(psi, d @ xi), np.conj(actual - 1))
                        require(np.linalg.norm(d @ xi) <= 2 + tolerance, "annihilation vector upper bound")
                    if m == 4 and seed == 142:
                        # Independent bounded local-number reference comparison.
                        inside = dg_numeric(np.diag([1, 1, 1, 0]), cs)
                        outside = number - inside
                        local_h = kinetic + inside @ (inside - sigma * np.eye(size))
                        difference = local_h - k
                        nodes, weights = np.polynomial.legendre.leggauss(48)
                        for comparison_time in (0.13, 0.41):
                            uh = expm(-1j * comparison_time * local_h)
                            uk = expm(-1j * comparison_time * k)
                            fh = np.vdot(uh @ xi, a @ uh @ psi)
                            fk = np.vdot(uk @ xi, a @ uk @ psi)
                            epsi = np.linalg.norm((uh - uk) @ psi)
                            exi = np.linalg.norm((uh - uk) @ xi)
                            require(abs(fh - fk) <= epsi + exi + tolerance, 'two-evolved-vector comparison')
                            rows.append({'name': f'two_vector_n{n}_s{sigma}_t{comparison_time}',
                                         'matrix_element_error': float(abs(fh - fk)), 'upper': float(epsi + exi)})
                            for state, count in ((psi, n), (xi, n + 1)):
                                integral = np.zeros(size, dtype=complex)
                                integral_bound = 0.0
                                for node, weight in zip(nodes, weights):
                                    s = comparison_time * (node + 1) / 2
                                    reference = expm(-1j * s * k) @ state
                                    integrand = expm(-1j * (comparison_time - s) * local_h) @ difference @ reference
                                    integral += comparison_time * weight / 2 * integrand
                                    integral_bound += comparison_time * weight / 2 * 2 * count * np.linalg.norm(outside @ reference)
                                close(f'bounded_Duhamel_identity_n{count}_s{sigma}_t{comparison_time}', (uh - uk) @ state, -1j * integral)
                                require(np.linalg.norm((uh - uk) @ state) <= integral_bound + tolerance, 'bounded Duhamel comparison upper bound')
    for name, count in counter.items():
        require(count > 0, "planted wrong formula not detected: " + name)
    # Finite bounded commutator model with initial support and q chi=0.
    h = np.array([[0, 1, 0, 0, 0], [1, 2, 1, 0, 0], [0, 1, 3, 1, 0],
                  [0, 0, 1, 4, 1], [0, 0, 0, 1, 5]], dtype=complex)
    chi = np.diag([1, 1, 1, 0.5, 0])
    q = np.diag([0, 0, 0, 0, 1])
    comm = h @ chi - chi @ h
    for j in range(3):
        g = np.eye(5)[:, j]
        for time in (-0.2, 0.0, 0.01, 0.4):
            leakage = np.linalg.norm(q @ expm(-1j * time * h) @ g)
            upper = abs(time) * np.linalg.norm(comm, 2)
            require(leakage <= upper + tolerance, "finite commutator leakage bound")
            rows.append({"name": f"finite_commutator_j{j}_t{time}", "leakage": float(leakage), "upper": float(upper)})
    return {"floating_diagnostic_count": len(rows), "absolute_tolerance": tolerance,
            "maximum_equality_residual": maximum, "wrong_formula_detection_counts": counter,
            "rows": rows, "classification": "floating diagnostics, not rigorous enclosures or continuum approximations"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {"status": "PASS", "exact": exact_controls(), "numeric": numeric_controls(),
              "environment": {"python": platform.python_version(), "numpy": np.__version__,
                              "scipy": scipy.__version__, "sympy": sp.__version__},
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "remaining_gap": "Finite controls cannot establish continuum domains, uniform Sobolev/Duhamel bounds, compact-support geometry, or the N-to-infinity conclusion; those need written proof review."}
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "exact_predicates": result["exact"]["exact_predicate_count"],
                      "floating_diagnostics": result["numeric"]["floating_diagnostic_count"],
                      "maximum_residual": result["numeric"]["maximum_equality_residual"]}))


if __name__ == "__main__":
    main()
