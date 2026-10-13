#!/usr/bin/env python3
"""Independent tensor/potential/boundary derivations; Python 3 + SymPy.

No network or writes. Finite symbolic identities supplement the analytical
compactness/positivity argument; they do not prove universal nonexistence alone.
"""
import json
import sympy as s

passed = []


def require(name, residual):
    terms = list(residual) if isinstance(residual, s.MatrixBase) else [residual]
    if not all(s.simplify(term) == 0 for term in terms):
        raise ValueError(name)
    passed.append(name)


x, y, t, u, v, z, a, b = s.symbols("x y t u v z a b", real=True)
m, n, p, q = s.symbols("m n p q", integer=True)
coordinate = (x, y)
developed = s.Matrix([x, y + t*x**2/2])
jacobian = developed.jacobian(coordinate)

# Different route: the global affine coframe theta = (dx, dy + t*x*dx)
# is exact on the cover. d(theta)=0; its Jacobian recovers the connection.
connection = [jacobian.inv()*jacobian.diff(k) for k in coordinate]
require("cover_affine_coframe_closed_first", s.diff(jacobian[0, 1], x)-s.diff(jacobian[0, 0], y))
require("cover_affine_coframe_closed_second", s.diff(jacobian[1, 1], x)-s.diff(jacobian[1, 0], y))
require("coframe_connection_first", connection[0]-s.Matrix([[0, 0], [t, 0]]))
require("coframe_connection_second", connection[1])
require("parallel_volume", sum(s.trace(k) for k in connection))
for i in range(2):
    for j in range(2):
        require(f"flatness_from_coframe_{i}{j}", connection[j].diff(coordinate[i])-connection[i].diff(coordinate[j])+connection[i]*connection[j]-connection[j]*connection[i])
        require(f"torsion_from_coframe_{i}{j}", connection[i][:, j]-connection[j][:, i])

# Arbitrary smooth tensor, evaluated via the moving coframe rather than
# special metric coefficients. Transforming Dg to that coframe reproduces
# the same exterior-derivative obstruction in the original quotient frame.
A, B, C = [s.Function(name)(x, y) for name in ("A", "B", "C")]
metric = s.Matrix([[A, B], [B, C]])
covariant = [metric.diff(k)-connection[i].T*metric-metric*connection[i]
             for i, k in enumerate(coordinate)]
curl_alpha = B.diff(x)-A.diff(y)
require("arbitrary_metric_Stokes_density", covariant[0][1, 0]-covariant[1][0, 0]-(curl_alpha-t*C))
require("arbitrary_metric_second_component", covariant[0][1, 1]-covariant[1][0, 1]-(C.diff(x)-B.diff(y)))

# Compute covariant Hessians of arbitrary potentials on the cover. This
# separately checks necessity of Codazzi and the positive local boundary case.
Phi = s.Function("Phi")(u, v)
pulled = Phi.subs({u: developed[0], v: developed[1]}, simultaneous=True)
cov_hessian = s.hessian(pulled, coordinate)-s.Matrix([[t*s.diff(pulled, y), 0], [0, 0]])
developed_hessian = jacobian.T*s.hessian(Phi, (u, v)).subs({u: developed[0], v: developed[1]}, simultaneous=True)*jacobian
require("arbitrary_local_potential_covariant_hessian", cov_hessian-developed_hessian)
potential_derivative = [cov_hessian.diff(k)-connection[i].T*cov_hessian-cov_hessian*connection[i]
                       for i, k in enumerate(coordinate)]
for k in range(2):
    require(f"arbitrary_local_potential_Codazzi_{k}", potential_derivative[0][1, k]-potential_derivative[1][0, k])
local_positive = jacobian.T*jacobian
require("local_positive_determinant", local_positive.det()-1)
require("local_positive_A", local_positive[0, 0]-(1+t**2*x**2))
require("local_positive_C", local_positive[1, 1]-1)
require("local_positive_nonperiodic_B", local_positive[0, 1].subs(x, x+1)-local_positive[0, 1]-t)
require("local_positive_Stokes_boundary_matches", s.integrate(s.diff(local_positive[0, 1], x), (x, 0, 1), (y, 0, 1))-t)

# Positivity is essential: a nonsingular indefinite Hessian metric descends.
indefinite_potential = u*v-t*u**3/3
indefinite = jacobian.T*s.hessian(indefinite_potential, (u, v)).subs({u: developed[0], v: developed[1]}, simultaneous=True)*jacobian
require("indefinite_descending_metric", indefinite-s.Matrix([[0, 1], [1, 0]]))
require("indefinite_determinant", indefinite.det()+1)
require("indefinite_C_zero", indefinite[1, 1])

# A general affine straight line in developing coordinates pulls back to a
# globally defined polynomial geodesic for arbitrary real initial data.
x0, y0, velx, vely = s.symbols("x0 y0 velx vely", real=True)
geodesic = s.Matrix([x0+velx*z, y0+vely*z-t*velx**2*z**2/2])
velocity = geodesic.diff(z)
require("global_geodesic_x", geodesic.diff(z, 2)[0])
require("global_geodesic_y", geodesic.diff(z, 2)[1]+t*velocity[0]**2)
require("arbitrary_initial_position", geodesic.subs(z, 0)-s.Matrix([x0, y0]))
require("arbitrary_initial_velocity", velocity.subs(z, 0)-s.Matrix([velx, vely]))
require("developed_geodesic_affine_line", developed.subs({x: geodesic[0], y: geodesic[1]}, simultaneous=True).diff(z, 2))

# Parallel transport supplies an independent linear-holonomy check. Along a
# lifted loop x(s)=m*s, a parallel vector has v_y(s)=v_y(0)-t*m*s*v_x(0).
transport = s.Matrix([[1, 0], [-t*m, 1]])
deck_linear = s.Matrix([[1, 0], [t*m, 1]])
require("parallel_transport_inverse_deck_linear", transport*deck_linear-s.eye(2))
transport_along_loop = s.Matrix([[1, 0], [-t*m*z, 1]])
require("parallel_transport_ODE", transport_along_loop.diff(z)+m*connection[0]*transport_along_loop)
require("nonzero_parameter_changes_linear_holonomy", deck_linear[1, 0]-t*m)
def holonomy(mm, nn):
    return s.Matrix([[1, 0, mm], [t*mm, 1, nn+t*mm**2/2], [0, 0, 1]])
require("integer_deck_composition_all_parameters", holonomy(m, n)*holonomy(p, q)-holonomy(m+p, n+q))
require("integer_deck_equivariance", (holonomy(m, n)*s.Matrix([developed[0], developed[1], 1]))[:2, 0]-developed.subs({x: x+m, y: y+n}, simultaneous=True))

# Signed parameters and optional cubic reparameterization preserve the exact
# necessary equation. No positive-parameter or differentiable-period assumption.
for value in (s.Rational(-7, 3), s.Rational(-1, 11), s.Rational(1, 17), s.Rational(5, 2)):
    require(f"signed_parameter_obstruction_{str(value).replace('/', '_')}", (covariant[0][1, 0]-covariant[1][0, 0]).subs(t, value)-(curl_alpha-value*C))
require("cubic_parameter_obstruction", (covariant[0][1, 0]-covariant[1][0, 0]).subs(t, a**3)-(curl_alpha-a**3*C))
require("central_global_metric", (s.eye(2).diff(x)-connection[0].T-connection[0]).subs(t, 0))

# Periodic derivative cancellation on an arbitrary finite Fourier family is
# a reproducible illustration only. The report proves all smooth coefficients.
fourier_A = a + b*s.sin(2*s.pi*x)*s.cos(4*s.pi*y)
fourier_B = a*s.cos(6*s.pi*x)*s.sin(2*s.pi*y)+b*s.cos(2*s.pi*x)
require("Fourier_periodic_derivative_integral", s.integrate(s.diff(fourier_B, x)-s.diff(fourier_A, y), (x, 0, 1), (y, 0, 1)))
print(json.dumps({"status": "PASS", "independent_identity_count": len(passed),
                  "checks": passed,
                  "analytical_claim": "For arbitrary smooth periodic A,B,C with C>0, Codazzi implies 0=t*integral(C); hence t=0.",
                  "limitations": "Symbolic identities do not certify strict positivity, Stokes' theorem, source interpretation, or historical novelty."}, indent=2, sort_keys=True))
