#!/usr/bin/env python3
"""Small reproducible checks. Experiments are not a proof of convergence."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
import numpy as np


class Oracle:
    def __init__(self, matrix):
        self.matrix = np.asarray(matrix, dtype=float)
        self.calls = 0

    def __call__(self, x):
        self.calls += 1
        return self.matrix @ x


def tangent(a, rng):
    # Reorthogonalization makes the floating-point test robust near a pole.
    while True:
        z = rng.standard_normal(a.size)
        z -= np.dot(a, z) * a
        z -= np.dot(a, z) * a
        length = np.linalg.norm(z)
        if length > 1e-14:
            return z / length


def estimate(forward, backward, m, d, steps, seed):
    """Oracle-only implementation of PROOF.md Section 2 (no B or adjoints)."""
    rng = np.random.default_rng(seed)
    u = rng.standard_normal(m); u /= np.linalg.norm(u)
    v = rng.standard_normal(d); v /= np.linalg.norm(v)
    av = forward(v); gu = backward(u)
    val = float(np.dot(u, av) - np.dot(gu, v))
    if val < 0:
        u, gu, val = -u, -gu, -val
    history = [val]
    max_identity_error = 0.0
    for _ in range(steps):
        us = [u]; vs = [v]; af = [av]; bg = [gu]
        if m > 1:
            w = tangent(u, rng); us.append(w); bg.append(backward(w))
        if d > 1:
            x = tangent(v, rng); vs.append(x); af.append(forward(x))
        # Each matrix here has at most two columns: constant vector storage.
        U = np.column_stack(us); Q = np.column_stack(vs)
        AQ = np.column_stack(af); GU = np.column_stack(bg)
        C = U.T @ AQ - GU.T @ Q
        p, s, qt = np.linalg.svd(C, full_matrices=False)
        left, right = p[:, 0], qt[0]
        u = U @ left; v = Q @ right
        av = AQ @ right; gu = GU @ left
        # Normalize vectors AND cached images to control accumulated rounding.
        nu, nv = np.linalg.norm(u), np.linalg.norm(v)
        u /= nu; gu /= nu; v /= nv; av /= nv
        value = float(np.dot(u, av) - np.dot(gu, v))
        max_identity_error = max(max_identity_error, abs(value-s[0]))
        history.append(value)
    return np.asarray(history), max_identity_error


def exact_checks():
    rng = np.random.default_rng(562)
    count = 0
    for _ in range(300):
        m, d = 3, 4
        A = [[F(int(z)) for z in row] for row in rng.integers(-7, 8, (m, d))]
        V = [[F(int(z)) for z in row] for row in rng.integers(-7, 8, (m, d))]
        u = [F(int(z), 3) for z in rng.integers(-5, 6, m)]
        v = [F(int(z), 5) for z in rng.integers(-5, 6, d)]
        av = [sum(A[i][j]*v[j] for j in range(d)) for i in range(m)]
        vtu = [sum(V[i][j]*u[i] for i in range(m)) for j in range(d)]
        lhs = sum(u[i]*av[i] for i in range(m))-sum(vtu[j]*v[j] for j in range(d))
        rhs = sum(u[i]*(A[i][j]-V[i][j])*v[j] for i in range(m) for j in range(d))
        assert lhs == rhs
        count += 1
    # The source's projected-determinant nonvanishing assertion fails at rank 1.
    a, b, c, d = F(9, 25), F(-12, 25), F(-12, 25), F(16, 25)
    assert a*d-b*c == 0 and a > 0
    # Generic exact rank-one outer products always have vanishing 2x2 minors.
    for _ in range(300):
        r = [F(int(z), 7) for z in rng.integers(-9, 10, 2)]
        s = [F(int(z), 11) for z in rng.integers(-9, 10, 2)]
        assert (r[0]*s[0])*(r[1]*s[1]) == (r[1]*s[0])*(r[0]*s[1])
        count += 1
    return {"rational_oracle_and_rank_one_checks": count,
            "explicit_rank_one_source_counterexample": "passed"}


def geometry_checks():
    rng = np.random.default_rng(30005215)
    max_err = 0.0
    count = 0
    for n in [2, 3, 5, 8]:
        for _ in range(150):
            a = rng.standard_normal(n); a /= np.linalg.norm(a)
            t = rng.standard_normal(n); t /= np.linalg.norm(t)
            alpha = np.dot(a, t); beta = np.sqrt(max(0, 1-alpha*alpha))
            if beta < 1e-9:
                continue
            z = (t-alpha*a)/beta
            x = tangent(a, rng)
            candidate = alpha*a + beta*x
            err = abs(np.linalg.norm(candidate-t)-beta*np.linalg.norm(x-z))
            max_err = max(max_err, err)
            assert abs(np.linalg.norm(candidate)-1) < 1e-12
            assert err < 1e-12
            count += 1
    return {"random_plane_geometric_identities": count,
            "maximum_rounding_error": float(f"{max_err:.3g}")}


def numerical_checks():
    rng = np.random.default_rng(1947)
    samples = [
        ("zero", np.zeros((4, 3))),
        ("scalar", np.array([[-7.0]])),
        ("row", np.array([[3.0, -4.0, 0.0, 2.0]])),
        ("column", np.array([[3.0], [-4.0], [2.0]])),
        ("rank_one", np.outer([1., 2., -1., 0.], [3., -2., 1.])),
        ("isometry", np.eye(4)),
        ("repeated_top", np.diag([3., 3., 1., 0.])),
        ("two_dimensional", np.array([[0., 4.], [-2., 1.]])),
        ("rectangular_dense", rng.standard_normal((7, 5))),
        ("tall_dense", rng.standard_normal((8, 3))),
        ("wide_dense", rng.standard_normal((3, 8))),
    ]
    results = []
    for i, (label, B) in enumerate(samples):
        m, d = B.shape
        # Dense B is only the independent test fixture; the algorithm sees A,V^T.
        V = rng.standard_normal((m, d)) if label != "zero" else rng.standard_normal((m,d))
        A = V + B
        forward, backward = Oracle(A), Oracle(V.T)
        steps = 600
        h, identity_error = estimate(forward, backward, m, d, steps, 562+i)
        target = np.linalg.norm(B, 2)
        tolerance = 2e-10 * max(1., target)
        assert h.min() >= -tolerance
        assert np.diff(h).min() >= -tolerance
        assert h.max() <= target+tolerance
        assert abs(h[-1]-target) <= 2e-8*max(1., target)
        assert identity_error < tolerance
        assert forward.calls == 1+steps*(d>1)
        assert backward.calls == 1+steps*(m>1)
        results.append({"case": label, "shape": [m,d], "steps": steps,
                        "target_norm": float(f"{target:.12g}"),
                        "final_norm": float(f"{h[-1]:.12g}"),
                        "A_calls": forward.calls, "VT_calls": backward.calls,
                        "monotonicity_and_bound": "passed_with_roundoff_tolerance"})
    return results


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--output")
    args = parser.parse_args()
    result = {"status": "pass", "exact_checks": exact_checks(),
              "geometric_checks": geometry_checks(), "numerical_checks": numerical_checks(),
              "scope": "Exact rational identities and bounded floating-point smoke tests. The almost-sure convergence theorem is proved in PROOF.md, not established by sampling.",
              "dependencies": {"python": ">=3.9", "numpy": np.__version__}}
    data = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        Path(args.output).write_text(data)
    else:
        print(data, end="")


if __name__ == "__main__":
    main()
