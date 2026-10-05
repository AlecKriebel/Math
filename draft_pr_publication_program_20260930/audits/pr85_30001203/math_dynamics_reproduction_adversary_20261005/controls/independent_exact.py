#!/usr/bin/env python3
"""Independent exact controls authored before inspection of submitted verify.py.

This audits identities of stationary dynamics and induced geometry. It does not
construct a Nash embedding or prove covering existence. All asserted identities
are symbolic; no finite disk grid is used for the continuum chart bounds.
"""
import collections
import datetime
import hashlib
import json
import pathlib
import platform
import sympy as s

COUNTS = collections.Counter()


def exact_zero(expr, family):
    reduced = s.factor(s.cancel(s.together(expr)))
    if reduced != 0:
        raise AssertionError((family, reduced))
    COUNTS[family] += 1


def exact_matrix(A, B, family):
    assert A.shape == B.shape
    for x in A - B:
        exact_zero(x, family)


def check(condition, family):
    if not condition:
        raise AssertionError(family)
    COUNTS[family] += 1


def geometry(g, q):
    """Christoffel/Riemann/Ricci from the defining coordinate formulas."""
    n = len(q)
    gi = g.inv().applyfunc(s.factor)
    Gamma = [[[s.factor(sum(gi[k, ell] * (
        s.diff(g[ell, j], q[i]) + s.diff(g[ell, i], q[j])
        - s.diff(g[i, j], q[ell])) for ell in range(n))/2)
        for j in range(n)] for i in range(n)] for k in range(n)]
    # R^ell_(k i j) is the coefficient of R(partial_i,partial_j)partial_k.
    R = [[[[s.factor(s.diff(Gamma[ell][j][k], q[i])
        - s.diff(Gamma[ell][i][k], q[j])
        + sum(Gamma[ell][i][m]*Gamma[m][j][k]
              - Gamma[ell][j][m]*Gamma[m][i][k] for m in range(n)))
        for j in range(n)] for i in range(n)] for k in range(n)]
        for ell in range(n)]
    Ric = s.Matrix(n, n, lambda k, j: s.factor(sum(R[i][k][i][j]
                                                    for i in range(n))))
    scalar = s.factor(sum(gi[k, j]*Ric[k, j] for k in range(n)
                         for j in range(n)))
    return Gamma, R, Ric, scalar


T, t = s.symbols('T t', positive=True)
u, v, X, Y = s.symbols('u v X Y', real=True)
disk = 4/(1-u*u-v*v)**2 * s.eye(2)
upper = s.eye(2)/Y**2
geometries = []
for label, base, q in [('disk', disk, (u, v)),
                       ('upper_half_plane', upper, (X, Y))]:
    G, R, Ric, scalar = geometry(T*base, q)
    G0, R0, Ric0, scalar0 = geometry(base, q)
    exact_zero(scalar/2 + 1/T, label+'_curvature_from_full_riemann')
    exact_matrix(Ric, -base, label+'_ricci')
    exact_zero(scalar0/2 + 1, label+'_unit_curvature')
    # Constant scaling has the same connection and same (1,3) curvature.
    for k in range(2):
        for i in range(2):
            for j in range(2):
                exact_zero(G[k][i][j]-G0[k][i][j], label+'_connection_scale')
                exact_zero(G[k][i][j]-G[k][j][i], label+'_torsion')
                covder = s.diff((T*base)[i,j], q[k]) - sum(
                    G[m][k][i]*(T*base)[m,j]
                    + G[m][k][j]*(T*base)[i,m] for m in range(2))
                exact_zero(covder, label+'_metric_compatibility')
                for ell in range(2):
                    exact_zero(R[ell][k][i][j]-R0[ell][k][i][j],
                               label+'_mixed_curvature_scale')
    geometries.append({'chart': label, 'curvature': str(scalar/2),
                       'ricci': str(Ric)})

# A nonorthogonal change of state coordinates must change matrix eigenvalues,
# while preserving intrinsic curvature and the Gramian pullback law.
xi, eta = s.symbols('xi eta', real=True)
J = s.Matrix([[2, 1], [1, 1]])
qchange = {u:2*xi+eta, v:xi+eta}
gnew = (J.T * (T*disk).subs(qchange) * J).applyfunc(s.factor)
Gn, Rn, Ricn, scalarn = geometry(gnew, (xi, eta))
exact_zero(scalarn/2 + 1/T, 'nonorthogonal_chart_curvature')
exact_matrix(Ricn, -gnew/T, 'nonorthogonal_chart_ricci')
check(J.det() != 0, 'nonorthogonal_chart_invertible')
check((4*J.T*J)[0,0] != 4, 'matrix_bound_not_arbitrary_chart_invariant')
check(max((4*J.T*J).eigenvals()) > s.Rational(64,9),
      'matrix_bound_not_arbitrary_chart_invariant')

# Continuum bounds: slack factorizations for a symbolic squared radius rho.
# Their factors have known signs on 0 <= rho <= 1/4, not just at a grid.
rho = s.symbols('rho', nonnegative=True)
lam = 4*T/(1-rho)**2
exact_zero(lam-4*T - 4*T*rho*(2-rho)/(1-rho)**2,
           'all_radius_lower_slack_factorization')
exact_zero(s.Rational(64,9)*T-lam
           - 4*T*(1-4*rho)*(7-4*rho)/(9*(1-rho)**2),
           'all_radius_upper_slack_factorization')
exact_zero(lam.subs(rho,0)-4*T, 'sharp_center_lower_bound')
exact_zero(lam.subs(rho,s.Rational(1,4))-s.Rational(64,9)*T,
           'sharp_boundary_upper_bound')
# Divide by positive T before asking the rational inequality solver.
check(s.solve_univariate_inequality(s.diff(lam, rho)/T>0, rho)
      == (rho<1), 'radial_monotonicity_domain')

# Stationary flow/variational equation, without finite time quadrature.
Phi = s.eye(2)
F = s.zeros(2)
exact_matrix(Phi.diff(t), F*Phi, 'zero_flow_variational_equation')
exact_matrix(Phi.subs(t, 0), s.eye(2), 'zero_flow_initial_condition')
# Completely symbolic rectangular observation differential and nonlinear chart
# covariance: this is universal local algebra and does not instantiate Nash e.
E = s.Matrix(3,2, s.symbols('e0:6'))
r, q = s.symbols('r q', real=True)
pi_local = s.Matrix([r+q*q, 2*q])
B = pi_local.jacobian([r,q])
check(B.det() != 0, 'nonlinear_projection_local_invertibility')
H = E*B
integrated = (Phi.T*H.T*H*Phi).applyfunc(lambda a:s.integrate(a,(t,0,T)))
exact_matrix(integrated, T*B.T*(E.T*E)*B,
             'symbolic_stationary_gramian_chart_covariance')

# Chain rule for a concrete nonlinear local observation, including derivatives
# of the projection chart. Not a compact hyperbolic/Nash construction.
e_local = s.Matrix([u, v, u*u+u*v])
h_local = e_local.subs({u:pi_local[0],v:pi_local[1]}, simultaneous=True)
exact_matrix(h_local.jacobian([r,q]),
             e_local.jacobian([u,v]).subs({u:pi_local[0],v:pi_local[1]},
                                         simultaneous=True)*B,
             'nonlinear_chain_rule')

# History norms: all time samples are equal when f=0. The exact L2 distance
# shows that equality of histories is precisely equality of output values.
d0,d1,d2 = s.symbols('d0 d1 d2', real=True)
d = s.Matrix([d0,d1,d2])
exact_zero(s.integrate((d.T*d)[0],(t,0,T))-T*sum(a*a for a in d),
           'exact_history_distance')
for length in [s.Rational(1,7), s.Integer(1), s.Rational(23,4)]:
    check(length>0, 'fixed_positive_interval')
    exact_zero((length*d.T*d)[0]-length*sum(a*a for a in d),
               'exact_history_distance_at_fixed_interval')
exact_matrix((T*disk).subs(T,0), s.zeros(2), 'zero_interval_loses_pd')
exact_zero(s.limit(T*4,T,0), 'no_common_lower_bound_as_T_to_zero')
check(s.limit(4*T,T,s.oo) == s.oo, 'no_common_upper_bound_as_T_to_infinity')
exact_zero(s.limit(-1/T,T,s.oo), 'no_common_negative_curvature_margin_all_T')

receipt = {
    'status':'PASS',
    'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'checker_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    'python_version':platform.python_version(),
    'sympy_version':s.__version__,
    'exact_assertions':sum(COUNTS.values()),
    'checks':dict(sorted(COUNTS.items())),
    'geometries':geometries,
    'chart_bound_proof':'Analytic factorizations for every 0<=rho<=1/4; no finite grid.',
    'limits':'Does not construct or computationally certify Nash embedding, compact quotient, covering, global fiber count, or completeness. Those are deductive theorem inputs and arguments in INDEPENDENT_DERIVATION.md.',
    'independence':'Authored before reading submitted verify.py or any submitted review files.'
}
print(json.dumps(receipt,indent=2))
