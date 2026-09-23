#!/usr/bin/env python3
"""Exact, independent coordinate checks for the radial statistical example.

Run: python verify_symbolic.py
Requires only SymPy (see requirements.txt); no floating-point arithmetic or
assert statements are used. Coordinates cover 0 < theta < pi. The proof, not
this calculation, supplies the all-centres radial-integrability theorem and
the coordinate-independent conclusion at the polar coordinate singularities.

Index convention:
  Gamma[k][i][j] = coefficient of partial_k in nabla_{partial_i} partial_j
  R[k][i][j][l] = coefficient of partial_k in R(partial_i,partial_j) partial_l
  R(X,Y)Z = nabla_X nabla_Y Z - nabla_Y nabla_X Z - nabla_[X,Y] Z.
"""

from itertools import product
import platform

import sympy as s


N = 3
I = range(N)
theta, chi, t = s.symbols("theta chi t", real=True)
coords = (theta, chi, t)
checks = 0


def reduced(expression):
    return s.trigsimp(s.simplify(expression), method="fu")


def check_zero(expression, label):
    """Raise an exception on failure even when Python runs with -O."""
    global checks
    result = reduced(expression)
    if result != 0:
        raise RuntimeError(f"FAIL {label}: residual = {result}")
    checks += 1


def require(condition, label):
    global checks
    if not condition:
        raise RuntimeError(f"FAIL {label}")
    checks += 1


def connection_from_metric(metric):
    inverse = metric.inv()
    return [[[reduced(sum(inverse[k, m] * (
        s.diff(metric[m, j], coords[i])
        + s.diff(metric[m, i], coords[j])
        - s.diff(metric[i, j], coords[m])
    ) / 2 for m in I)) for j in I] for i in I] for k in I]


def curvature(gamma):
    # This definition is used for every connection, including nonmetric ones.
    return [[[[reduced(
        s.diff(gamma[k][j][l], coords[i])
        - s.diff(gamma[k][i][l], coords[j])
        + sum(gamma[k][i][m] * gamma[m][j][l]
              - gamma[k][j][m] * gamma[m][i][l] for m in I)
    ) for l in I] for j in I] for i in I] for k in I]


def covariant_metric_derivative(gamma, metric):
    return [[[reduced(s.diff(metric[j, l], coords[i]) - sum(
        gamma[m][i][j] * metric[m, l]
        + gamma[m][i][l] * metric[j, m] for m in I
    )) for l in I] for j in I] for i in I]


def flatness_obstruction_system(tensor, metric):
    """Test all components of R^k_ijl = h_jl A^k_i - h_il A^k_j.

    A is completely unrestricted. An inconsistent system therefore excludes
    any A constructed from a conformal factor and its derivatives.
    """
    unknowns = s.symbols("a0:9")
    A = s.Matrix(N, N, unknowns)
    equations = [tensor[k][i][j][l] - metric[j, l] * A[k, i]
                 + metric[i, l] * A[k, j]
                 for k, i, j, l in product(I, repeat=4)]
    matrix, rhs = s.linear_eq_to_matrix(equations, unknowns)
    return matrix.rank(), matrix.row_join(rhs).rank(), s.linsolve(
        (matrix, rhs), unknowns)


def run():
    print(f"Python {platform.python_version()}; SymPy {s.__version__}")
    print("Exact symbolic arithmetic; coordinates (theta, chi, t).")
    print("Curvature convention: R(X,Y)Z = [nabla_X,nabla_Y]Z - nabla_[X,Y]Z.")

    h = s.diag(1, s.sin(theta) ** 2, 1)
    gamma = connection_from_metric(h)
    cubic0 = covariant_metric_derivative(gamma, h)
    for k, i, j in product(I, repeat=3):
        check_zero(gamma[k][i][j] - gamma[k][j][i], "Levi-Civita torsion")
        check_zero(cubic0[k][i][j], "Levi-Civita metric compatibility")
    R = curvature(gamma)
    for k, i, j, l in product(I, repeat=4):
        expected = (h[j, l] * s.KroneckerDelta(k, i)
                    - h[i, l] * s.KroneckerDelta(k, j)) if (
                        k < 2 and i < 2 and j < 2 and l < 2) else 0
        check_zero(R[k][i][j][l] - expected, "product curvature component")
    ricci = s.Matrix(N, N, lambda j, l: sum(R[k][k][j][l] for k in I))
    for j, l in product(I, repeat=2):
        check_zero(ricci[j, l] - s.diag(1, s.sin(theta)**2, 0)[j, l],
                   "Ricci component")
    print("PASS: all Christoffel torsion, metric-compatibility, curvature and Ricci components.")
    print(f"Ricci in coordinate basis: {ricci}")
    print(f"R(partial_theta,partial_chi)partial_chi: ({R[0][0][1][1]}, 0, 0)")
    print(f"R(partial_theta,partial_t)partial_t: ({R[0][0][2][2]}, 0, 0)")

    # Directly calculate the curvature of the full changed connection for an
    # arbitrary smooth function, then compare all 81 components to the formula.
    phi = s.Function("phi")(*coords)
    V = h.inv() * s.Matrix([s.diff(phi, x) for x in coords])
    gamma_hat = [[[gamma[k][i][j] - h[i, j] * V[k] for j in I]
                  for i in I] for k in I]
    R_hat = curvature(gamma_hat)
    A = s.Matrix(N, N, lambda k, i: s.diff(V[k], coords[i])
                 + sum(gamma[k][i][m] * V[m] for m in I)
                 - s.diff(phi, coords[i]) * V[k])
    for k, i, j, l in product(I, repeat=4):
        check_zero(R_hat[k][i][j][l] - R[k][i][j][l]
                   + h[j, l] * A[k, i] - h[i, l] * A[k, j],
                   "arbitrary-phi curvature transformation")
    print("PASS: arbitrary-phi conformal curvature formula, all 81 components.")

    # Two equations contradict each other throughout the coordinate chart,
    # where sin(theta) != 0: both determine the same entry A^theta_theta.
    check_zero(R[0][0][1][1] / h[1, 1] - 1, "generic sphere equation forces A^0_0=1")
    check_zero(R[0][0][2][2] / h[2, 2], "generic mixed equation forces A^0_0=0")

    # At theta=pi/2 the coordinate basis is orthonormal. The proof uses these
    # same two incompatible components at any point in an orthonormal frame.
    Rp = [[[[entry.subs(theta, s.pi / 2) for entry in row]
             for row in plane] for plane in block] for block in R]
    rank, augmented_rank, solutions = flatness_obstruction_system(Rp, s.eye(N))
    require((rank, augmented_rank) == (9, 10), "product obstruction ranks")
    require(solutions == s.EmptySet, "product obstruction is inconsistent")
    check_zero(Rp[0][0][1][1] - 1, "sphere equation forces A^0_0=1")
    check_zero(Rp[0][0][2][2], "mixed equation forces A^0_0=0")
    print(f"PASS: arbitrary-A flatness equations inconsistent; ranks {rank} and {augmented_rank}.")
    # Independent projective Weyl component, with the symmetric Ricci formula.
    W_component = R[2][2][0][0] - ricci[0, 0] / (N - 1)
    check_zero(W_component + s.Rational(1, 2), "projective Weyl obstruction")
    print(f"Projective Weyl: W^t_(t theta theta) = {W_component} (nonzero).")

    # The non-self-dual construction is calculated from the new metric and
    # connection, without assuming the paper's cubic or duality formulas.
    eta = (0, 0, 1)
    h1 = s.exp(t) * h
    gamma1 = [[[gamma[k][i][j] + eta[i] * s.KroneckerDelta(k, j)
                + eta[j] * s.KroneckerDelta(k, i) for j in I]
               for i in I] for k in I]
    cubic1 = covariant_metric_derivative(gamma1, h1)
    for i, j, l in product(I, repeat=3):
        expected = -eta[i] * h1[j, l] - eta[j] * h1[i, l] - eta[l] * h1[i, j]
        check_zero(cubic1[i][j][l] - expected, "nonmetric cubic formula")
        check_zero(cubic1[i][j][l] - cubic1[j][i][l], "cubic symmetry i,j")
        check_zero(cubic1[i][j][l] - cubic1[i][l][j], "cubic symmetry j,l")
        check_zero(gamma1[i][j][l] - gamma1[i][l][j], "new connection torsion")
    check_zero(cubic1[2][2][2] + 3 * s.exp(t), "nowhere-zero cubic component")
    inverse1 = h1.inv()
    dual1 = [[[reduced(sum(inverse1[k, j] * (
        s.diff(h1[j, l], coords[i])
        - sum(gamma1[m][i][j] * h1[m, l] for m in I)
    ) for j in I)) for l in I] for i in I] for k in I]
    for k, i, l in product(I, repeat=3):
        check_zero(dual1[k][i][l] - gamma[k][i][l] + h[i, l] * eta[k],
                   "dual connection from defining identity")
    velocity = s.symbols("v0:3")
    for k in I:
        check_zero(sum((gamma1[k][i][j] - gamma[k][i][j])
                       * velocity[i] * velocity[j] for i, j in product(I, repeat=2))
                   - 2 * velocity[2] * velocity[k], "geodesic acceleration difference")
    psi = s.Function("psi")(*coords)
    grad1 = inverse1 * s.Matrix([s.diff(psi, x) for x in coords])
    grad_total = h.inv() * s.Matrix([s.diff(t + psi, x) for x in coords])
    for k, i, j in product(I, repeat=3):
        check_zero(dual1[k][i][j] - h1[i, j] * grad1[k]
                   - gamma[k][i][j] + h[i, j] * grad_total[k],
                   "dual conformal change equals base change with t+psi")
    print("PASS: non-self-dual torsion, cubic symmetry, duality, geodesic acceleration and composition.")
    print(f"Nonzero cubic component: C_ttt = {cubic1[2][2][2]}")

    # Controls: the obstruction solver must accept compatible tensors. The
    # Euclidean control is computed from its metric; the unit-sphere tensor
    # is the algebraic constant-curvature model, with A=identity.
    R_flat = curvature(connection_from_metric(s.eye(N)))
    rank0, augmented0, solution0 = flatness_obstruction_system(R_flat, s.eye(N))
    require((rank0, augmented0) == (9, 9), "flat control ranks")
    require(solution0 == s.FiniteSet((0,) * 9), "flat control A=0")
    R_space_form = [[[[s.KroneckerDelta(j, l) * s.KroneckerDelta(k, i)
                      - s.KroneckerDelta(i, l) * s.KroneckerDelta(k, j)
                      for l in I] for j in I] for i in I] for k in I]
    rank1, augmented1, solution1 = flatness_obstruction_system(R_space_form, s.eye(N))
    require((rank1, augmented1) == (9, 9), "constant-curvature control ranks")
    require(solution1 == s.FiniteSet(tuple(s.eye(N))), "constant-curvature control A=I")

    # Negative control: omit the required metric rescaling. The projectively
    # changed connection paired with h does NOT define a statistical structure.
    wrong_cubic = covariant_metric_derivative(gamma1, h)
    residual = reduced(wrong_cubic[2][0][0] - wrong_cubic[0][2][0])
    require(residual != 0, "control must detect asymmetric unscaled cubic")
    print("PASS: compatible Euclidean and constant-curvature controls accepted.")
    print(f"PASS: omitted-rescaling negative control rejected; cubic symmetry residual = {residual}.")
    print(f"SUCCESS: {checks} explicit exact checks; no Python assert statements.")
    print("Scope: tensor identities only; radial integrability and original-source interpretation require the proof/audit.")


if __name__ == "__main__":
    run()
