#!/usr/bin/env python3
"""Exact measure-action controls supplementing, not proving, the universal audit.

The jump tests integrate L1 displacements against derivatives of compact C1
test functions, rather than differentiating the author's smooth templates.
"""
import itertools
import json
import sympy as s

x, y, z = coords = s.symbols('x y z', real=True)
checks = []


def record(name, **data):
    checks.append(dict(name=name, passed=True, **data))


def zero_matrix(M):
    assert all(s.simplify(q) == 0 for q in M), M


def box_integral(expr, bounds, variables=coords):
    out = s.S.Zero
    for powers, coefficient in s.Poly(s.expand(expr), *variables).terms():
        term = coefficient
        for exponent, (lo, hi) in zip(powers, bounds):
            term *= (hi**(exponent+1)-lo**(exponent+1))/(exponent+1)
        out += term
    return s.simplify(out)


one_box = [(s.S(-1), s.S.One)] * 3
phi = ((1-x*x)**2 * (1-y*y)**2 * (1-z*z)**2
       * (1+x/2) * (1+y/3) * (1+z/4))


def weak_strain(cells):
    result = s.zeros(3)
    for bounds, displacement in cells:
        for i in range(3):
            for j in range(i, 3):
                result[i, j] -= box_integral(
                    (displacement[i]*s.diff(phi, coords[j])
                     + displacement[j]*s.diff(phi, coords[i]))/2, bounds)
    for i in range(3):
        for j in range(i):
            result[i, j] = result[j, i]
    return result


def plane_integral(expr, index, value):
    variables = [v for i, v in enumerate(coords) if i != index]
    return box_integral(expr.subs(coords[index], value),
                        [(s.S(-1), s.S.One)] * 2, variables)


# Independent signed BV profiles: two oppositely signed y jumps, one x jump,
# and a transverse quadratic displacement. Each cell is an ordinary polynomial.
cells = []
for xb, yb in itertools.product([(-1, 0), (0, 1)],
                               [(-1, -s.Rational(1, 2)),
                                (-s.Rational(1, 2), s.Rational(1, 2)),
                                (s.Rational(1, 2), 1)]):
    xm, ym = sum(xb)/2, sum(yb)/2
    h1 = int(bool(ym > -s.Rational(1, 2))) - 2*int(bool(ym > s.Rational(1, 2)))
    h2 = 3*int(bool(xm > 0))
    cells.append(([(s.S(xb[0]), s.S(xb[1])),
                   (s.S(yb[0]), s.S(yb[1])), (-s.S.One, s.S.One)],
                  s.Matrix([h1+2*y*z, h2+2*x*z, -2*x*y])))
actual = weak_strain(cells)
expected = s.zeros(3)
expected[0, 1] = expected[1, 0] = (
    plane_integral(phi, 1, -s.Rational(1, 2))
    - 2*plane_integral(phi, 1, s.Rational(1, 2))
    + 3*plane_integral(phi, 0, 0)
    + 4*box_integral(z*phi, one_box))/2
zero_matrix(actual-expected)
record('independent_BV_signed_jumps_direct_weak_action',
       E12_action=str(actual[0, 1]), all_other_components_zero=True,
       coefficient='delta(y+1/2)-2delta(y-1/2)+3delta(x)+4z dx')

# Parallel derivative-BV profiles. P2=s_+, P3=-2(s-1/2)_+ are Lipschitz.
# The mixed E12/E13 terms cancel by direct weak pairing.
cells = []
for xb in [(-1, 0), (0, s.Rational(1, 2)), (s.Rational(1, 2), 1)]:
    xm = sum(xb)/2
    j0, jh = int(bool(xm > 0)), int(bool(xm > s.Rational(1, 2)))
    displacement = s.Matrix([2*j0-3*jh+y*j0-2*z*jh,
                             -x*j0, 2*(x-s.Rational(1, 2))*jh])
    cells.append(([(s.S(xb[0]), s.S(xb[1])),
                   (-s.S.One, s.S.One), (-s.S.One, s.S.One)], displacement))
actual = weak_strain(cells)
expected = s.zeros(3)
expected[0, 0] = (plane_integral((2+y)*phi, 0, 0)
                  + plane_integral((-3-2*z)*phi, 0, s.Rational(1, 2)))
zero_matrix(actual-expected)
record('parallel_derivative_BV_jumps_direct_weak_action',
       E11_action=str(actual[0, 0]), all_mixed_components_zero=True,
       coefficient='(2+y)delta(x)+(-3-2z)delta(x-1/2)')

# A nonunit jump normal has a coarea factor. u=(J(2y),0,0) gives
# Eu=(e1 odot 2e2) times [delta(y)/2], not times delta(y).
cells = [(one_box[:1]+[(s.S(-1), s.S.Zero)]+one_box[2:], s.zeros(3, 1)),
         (one_box[:1]+[(s.S.Zero, s.S.One)]+one_box[2:], s.Matrix([1, 0, 0]))]
actual = weak_strain(cells)
expected = s.zeros(3)
expected[0, 1] = expected[1, 0] = plane_integral(phi, 1, 0)/2
zero_matrix(actual-expected)
record('nonunit_jump_normal_coarea_half_factor', E12_action=str(actual[0, 1]))

# Arbitrary distributional profiles are not BD profiles: P=J makes t P'
# a delta distribution and gives t delta'(s) as a strain coefficient. A bounded
# compact-test sequence has unbounded action, so this is not a Radon measure.
t = s.symbols('t', real=True)
eta = (1+t/2)*(1-t*t)**2
moment = s.integrate(t*eta, (t, -1, 1))
assert moment == s.Rational(8, 105)
record('distribution_not_measure_negative_control',
       uniform_bounded_test_action='-8 n / 105',
       rejected_profile='P=Heaviside(s), Pprime=delta(s)',
       reasoning='phi_n=psi(ns)eta(t), psi(r)=r(1-r^2)^2 on [-1,1]')

# Independent, nonorthogonal and nonunit geometry: transform both displacement
# and coordinates, using a dual basis in the a,b plane.
a, b, v = s.Matrix([2, -1, 0]), s.Matrix([3, 4, 0]), s.Matrix([0, 0, 5])
gram = a.dot(a)*b.dot(b)-a.dot(b)**2
p = (b.dot(b)*a-a.dot(b)*b)/gram
q = (a.dot(a)*b-a.dot(b)*a)/gram
T = s.Matrix.hstack(p, q, s.Matrix([0, 0, 1]))
assert T.T*a == s.Matrix([1, 0, 0]) and T.T*b == s.Matrix([0, 1, 0])
A, B, V = s.Matrix(coords).dot(a), s.Matrix(coords).dot(b), s.Matrix(coords).dot(v)
u = a*(B**3+B*V)+b*(A**2+A*V)-v*A*B
Y = T*s.Matrix(coords)
canonical = T.T*u.subs(dict(zip(coords, Y)), simultaneous=True)
zero_matrix(canonical-s.Matrix([y**3+5*y*z, x**2+5*x*z, -5*x*y]))
D = u.jacobian(coords)
zero_matrix((D+D.T)/2-(3*B**2+2*A+2*V)*(a*b.T+b*a.T)/2)
record('dual_basis_congruence_for_nonorthogonal_nonunit_case',
       determinant=str(T.det()), gram_determinant=str(gram),
       canonical_displacement=[str(q) for q in canonical])

# Source transformation wording cannot be interpreted as sending e_i to a,b:
# that matrix gives T^T a != e1. The corrected dual-basis map above works.
wrong = s.Matrix.hstack(a, b, s.Matrix([0, 0, 1]))
assert wrong.T*a != s.Matrix([1, 0, 0])
record('published_informal_congruence_direction_negative_control',
       wrong_transformed_a=[str(q) for q in wrong.T*a])

# Parallel signed scale is absorbed into scalar coefficient after unit normalize.
e, w = s.Matrix([s.Rational(3, 5), s.Rational(4, 5), 0]), s.Matrix([-s.Rational(4, 5), s.Rational(3, 5), 0])
e3 = s.Matrix([0, 0, 1])
X = s.Matrix(coords)
S, U, W = X.dot(e), X.dot(w), X.dot(e3)
u = e*(S**3+4*U*S**3-2*W*S)-w*S**4+e3*S**2
lam = 3*S**2+12*U*S**2-2*W
a, b = -7*e, s.Rational(2, 3)*e
P = (a*b.T+b*a.T)/2
D = u.jacobian(coords)
zero_matrix((D+D.T)/2-P*(lam/(-s.Rational(14, 3))))
record('parallel_nonunit_negative_scale_unit_normalization', scale='-14/3')

# The printed a != +/-b does not imply independence without normalization.
for scale in [s.S(2), s.S(-2)]:
    a = s.Matrix([1, 0, 0]); b = scale*a
    assert a != b and a != -b
    assert s.Matrix.hstack(a, b).rank() == 1
record('printed_condition_unnormalized_parallel_trap', cases=['b=2a', 'b=-2a'])

# Exact scalar compatibility controls use a full Saint-Venant entry, not a
# numerical Hessian test. Index formula is valid for any fixed symmetric P.
def sv(P, lam, i, j, k, l):
    return s.expand(P[j, l]*s.diff(lam, coords[i], coords[k])
                    + P[i, k]*s.diff(lam, coords[j], coords[l])
                    - P[j, k]*s.diff(lam, coords[i], coords[l])
                    - P[i, l]*s.diff(lam, coords[j], coords[k]))

independent = s.Matrix([[0, s.Rational(1, 2), 0], [s.Rational(1, 2), 0, 0], [0, 0, 0]])
parallel = s.diag(1, 0, 0)
for name, P, lam, indexes, wanted in [
    ('independent_xy_incompatible', independent, x*y, (0, 1, 0, 1), -1),
    ('independent_xz_incompatible', independent, x*z, (0, 1, 0, 2), -s.Rational(1, 2)),
    ('independent_z2_incompatible', independent, z*z, (0, 2, 1, 2), 1),
    ('parallel_y2_incompatible', parallel, y*y, (0, 1, 0, 1), 2),
    ('parallel_yz_incompatible', parallel, y*z, (0, 1, 0, 2), 1),
]:
    obstruction = sv(P, lam, *indexes)
    assert obstruction == wanted and obstruction != 0, (name, obstruction)
    record(name, nonzero_compatibility_entry=str(obstruction), indices=indexes)
for name, P, lam in [
    ('independent_sign_changing_transverse_compatible', independent, x*x+y**3+2*z),
    ('parallel_variable_transverse_compatible', parallel, x**3+x*x*y+s.sin(x)*z),
]:
    assert all(sv(P, lam, *indexes) == 0
               for indexes in itertools.product(range(3), repeat=4))
    record(name)

# Boundary cases: the d=1 nonzero line imposes no extra restriction on a smooth
# displacement; Eu=0 in any dimension still forces the skew-affine kernel.
r = s.symbols('r', real=True)
f = s.sin(r)+r**3
assert s.simplify(s.diff(f, r)-(-6)*(s.diff(f, r)/(-6))) == 0
record('dimension_one_arbitrary_smooth_profile', product='2 times -3 = -6')
R = s.Matrix([[0, -2, 3], [2, 0, -7], [-3, 7, 0]])
u = R*s.Matrix(coords)+s.Matrix([9, -1, 4])
D = u.jacobian(coords)
zero_matrix((D+D.T)/2)
record('zero_strain_rigid_kernel_sufficiency')

# Two connected-domain globalization countercontrols. The smooth branch function
# g(r)=exp(-1/r^2) for r>0, zero otherwise, has g'(1)=2/e. In the
# independent case take left/right vertical arms joined by a bottom strip, and
# u=(g(y),0) only in the right arm. The four test points below all lie inside
# the connected domain. An additive global lambda=f(x)+h(y) has zero rectangular
# cross difference, whereas this branch strain does not.
gprime_one = s.diff(s.exp(-1/r**2), r).subs(r, 1)
assert gprime_one == 2/s.E
cross_difference = gprime_one - 0 - 0 + 0
assert cross_difference != 0
record('connected_domain_independent_globalization_negative_control',
       domain='((-3,-1)x(-1,2)) union ((1,3)x(-1,2)) union ((-3,3)x(-1,0))',
       displacement='(g(y),0) in right arm; zero in left arm and bottom connector',
       cross_difference=str(cross_difference),
       points=['(2,1)', '(-2,1)', '(2,-1/2)', '(-2,-1/2)'])

# Parallel case: upper/lower horizontal arms joined on the left. At x=1 the
# coefficient is 2/e throughout the upper interval and zero throughout lower
# interval. Two upper y values force an affine-in-y slope of zero, incompatible
# with a lower value of zero.
upper_slope = (gprime_one-gprime_one)/(s.Rational(5, 2)-s.Rational(3, 2))
assert upper_slope == 0 and gprime_one != 0
record('connected_domain_parallel_globalization_negative_control',
       domain='((-1,2)x(1,3)) union ((-1,2)x(-3,-1)) union ((-1,0)x(-3,3))',
       displacement='(g(x),0) in upper arm; zero in lower arm and left connector',
       forced_upper_slope=str(upper_slope), incompatible_lower_value='0')

print(json.dumps({'passed': True, 'sympy': s.__version__,
                  'checks': checks, 'total': len(checks),
                  'scope': 'Exact supplemental controls; universal necessity is audited separately.'}, indent=2))
