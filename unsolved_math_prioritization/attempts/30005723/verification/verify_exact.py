#!/usr/bin/env python3
"""Check algebra in the partial modular-generator investigation.

Requires SymPy and mpmath. Exact checks are separated from numerical replay.
No output from this script establishes a continuum modular-operator limit.
"""

import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s

OUT = Path(__file__).with_name("results.json")
exact = []
numeric = []
negative = []


def record_exact(name, condition):
    assert condition, name
    exact.append(name)


# The general product rule needs just these coefficient identities. It is not
# restricted to polynomial test functions.
mu = s.symbols("mu", positive=True)
for n in range(1, 6):
    p = s.symbols(f"p0:{n}", real=True)
    r2 = sum(x*x for x in p)
    w = s.sqrt(r2 + mu*mu)
    lap_w = sum(s.diff(w, x, 2) for x in p)
    record_exact(f"omega_laplacian_omega_n{n}",
                 s.simplify(w*lap_w-(n-1)-mu*mu/(r2+mu*mu)) == 0)
    for j, x in enumerate(p):
        record_exact(f"omega_gradient_omega_n{n}_j{j}",
                     s.simplify(w*s.diff(w, x)-x) == 0)
    # Removing the Yukawa term must be detected in every dimension.
    residual = s.simplify(w*lap_w-(n-1))
    assert residual != 0
    negative.append(f"dropped_yukawa_term_rejected_n{n}")

J = s.diag(1, -1)
chi2 = s.diag(1, 0)
blocks = []
for aa, bb in [(1, 2), (3, 4)]:
    a, b = s.Integer(aa), s.Integer(bb)
    T = s.Matrix([[(a+b)/2, (a-b)/2], [(a-b)/2, (a+b)/2]])
    Ti = T.inv()
    A = T**4
    B = T*chi2*Ti + Ti*chi2*T - s.eye(2)
    beta = (a*a+b*b)/(2*a*b)
    record_exact(f"B_rational_block_{aa}_{bb}", B == beta*J)
    record_exact(f"sandwich_J_block_{aa}_{bb}", Ti*J*Ti == J/(a*b))
    record_exact(f"spectral_gap_block_{aa}_{bb}", beta > 1)
    for j in range(2):
        e = s.eye(2)[:, j]
        det = s.Matrix.hstack(T*e, Ti*e).det()
        record_exact(f"standardness_block_{aa}_{bb}_coordinate{j}", det != 0)
    blocks.append((A, T))

# Four-dimensional matrices in the fixed inside/inside/outside/outside order.
A4 = s.zeros(4)
T4 = s.zeros(4)
for j, (Ab, Tb) in enumerate(blocks):
    for r in range(2):
        for c in range(2):
            A4[j+2*r, j+2*c] = Ab[r, c]
            T4[j+2*r, j+2*c] = Tb[r, c]
O = s.eye(4)
O[:2, :2] = s.Matrix([[1, 1], [1, -1]])/s.sqrt(2)
chi4 = s.diag(1, 1, 0, 0)
record_exact("rotation_commutes_with_cut", O*chi4 == chi4*O)
record_exact("rotation_orthogonal", O.T*O == s.eye(4))
record_exact("four_coordinate_fourth_power", T4**4 == A4)
c1, c2 = s.log(3), s.log(7)/6
M4 = O*s.diag(c1, c2, -c1, -c2)*O.T
record_exact("offdiagonal_formula", s.simplify(M4[0, 1]-(c1-c2)/2) == 0)
record_exact("offdiagonal_positive_integer_certificate", 3**6 > 7)

# Scalar endpoint examples and the resolvent integral bound.
eps, a, t = s.symbols("eps a t", positive=True)
endpoint_diff = s.log(2*(2+eps)/(2+2*eps))/2
record_exact("endpoint_instability_limit", s.limit(endpoint_diff, eps, 0) == s.log(2)/2)
record_exact("fixed_gap_integral", s.simplify((1/(a-1)-1/a)-1/(a*(a-1))) == 0)

# This is a supplementary high-precision replay of the finite formula.
mp.mp.dps = 90


def as_mp(X):
    return mp.matrix([[mp.mpf(str(s.N(X[i, j], 95))) for j in range(X.cols)]
                      for i in range(X.rows)])


def opnorm_entry(X):
    """Maximum entry magnitude, used only as a finite replay error statistic."""
    return max(abs(X[i, j]) for i in range(X.rows) for j in range(X.cols))


def spectral(X, fun):
    eig, V = mp.eigsy(X)
    return V*mp.diag([fun(v) for v in eig])*V.T


def arcoth(x):
    assert abs(x) > 1
    return mp.log((x+1)/(x-1))/2


A0 = as_mp(O*A4*O.T)
Ch = as_mp(chi4)
Om = as_mp(O)


def matrices(lam):
    A = A0 + lam*mp.eye(4)
    T = spectral(A, lambda x: x**mp.mpf("0.25"))
    E = T**-1
    C = T*Ch*E
    B = C+C.T-mp.eye(4)
    F = spectral(B, arcoth)
    M = 2*E*F*E
    return A, T, E, C, B, F, M


def coeff(aa, bb, lam):
    alpha = (mp.mpf(aa)**4+lam)**mp.mpf("0.25")
    beta = (mp.mpf(bb)**4+lam)**mp.mpf("0.25")
    return 2*mp.log((beta+alpha)/(beta-alpha))/(alpha*beta)


def closed_matrix(lam):
    c = coeff(1, 2, lam)
    d = coeff(3, 4, lam)
    return Om*mp.diag([c, d, -c, -d])*Om.T


for lam in map(mp.mpf, [0, 1, 10, 100]):
    vals = matrices(lam)
    err = opnorm_entry(vals[-1]-closed_matrix(lam))
    assert err < mp.mpf("1e-65")
    numeric.append({"check": "closed_finite_formula", "lambda": str(lam),
                    "max_entry_error": mp.nstr(err, 12),
                    "M01": mp.nstr(vals[-1][0, 1], 30)})

lam = mp.mpf(1)
A, T, E, C, B, F, M = matrices(lam)
Ai = A**-1
Bp = (Ai*(C-C.T)-(C-C.T)*Ai)/4
ev, V = mp.eigsy(B)
Xp = V.T*Bp*V
DFb = mp.matrix(4)
for i in range(4):
    for j in range(4):
        if abs(ev[i]-ev[j]) < mp.mpf("1e-60"):
            divided = -1/(ev[i]**2-1)
        else:
            divided = (arcoth(ev[i])-arcoth(ev[j]))/(ev[i]-ev[j])
        DFb[i, j] = divided*Xp[i, j]
DF = V*DFb*V.T
derivative = -(Ai*M+M*Ai)/4 + 2*E*DF*E
h = mp.mpf("1e-20")
finite_diff = (matrices(lam+h)[-1]-matrices(lam-h)[-1])/(2*h)
err = opnorm_entry(derivative-finite_diff)
assert err < mp.mpf("1e-35")
numeric.append({"check": "mass_derivative_formula", "max_entry_error": mp.nstr(err, 12),
                "derivative_max_entry": mp.nstr(opnorm_entry(derivative), 30)})

omitted_factor_term = 2*E*DF*E
wrong_err = opnorm_entry(omitted_factor_term-finite_diff)
assert wrong_err > mp.mpf("1e-4")
negative.append("omitted_exterior_factor_derivative_rejected")

results = {
    "verdict": "PASS",
    "scope": "Exact finite algebra and supplementary finite numerical replay only; no continuum-limit claim.",
    "exact_checks": exact,
    "exact_check_count": len(exact),
    "numerical_replays": numeric,
    "negative_controls": negative,
    "versions": {"sympy": s.__version__, "mpmath": mp.__version__, "mpmath_digits": mp.mp.dps},
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
OUT.write_text(json.dumps(results, indent=2)+"\n")
print(json.dumps(results, indent=2))


if __name__ == "__main__":
    pass
