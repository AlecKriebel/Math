"""Independent symbolic/exact checks for the outer-pedal k304 theorem.
No author code is imported. The written complex analysis remains necessary.
"""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from math import gcd
import json
import sympy as s

C = Counter()


def ck(x, label):
    assert x, label
    C[label] += 1


nx, ny, X, Y = s.symbols('nx ny X Y')
Nplus, Nminus = nx+s.I*ny, nx-s.I*ny
Z, W = X+s.I*Y, X-s.I*Y
qx = X+(1-nx*X-ny*Y)*nx/(nx*nx+ny*ny)
qy = Y+(1-nx*X-ny*Y)*ny/(nx*nx+ny*ny)
ck(s.cancel(qx+s.I*qy-(Z/2+(1-Nplus*W/2)/Nminus)) == 0,
   'isotropic_foot_plus_coordinate_identity')
ck(s.cancel(qx-s.I*qy-(W/2+(1-Nminus*Z/2)/Nplus)) == 0,
   'isotropic_foot_minus_coordinate_identity')

# At a zero of Nplus only the minus foot coordinate can be singular.
alpha, k, kp, sv, cv, dv = s.symbols('alpha k kp sv cv dv', nonzero=True)
a, b = alpha*dv/cv, alpha*kp/cv
n = s.Matrix([-dv/(k*cv*a), -s.I*kp/(k*cv*b)])
ck(s.cancel(n[0]+s.I*n[1]) == 0, 'common_row_plus_normal_vanishes')
ck(s.cancel(n[0]-s.I*n[1]+2/(alpha*k)) == 0, 'common_row_minus_normal_nonzero')
derivative = -2*k*k*cv*cv*(dv/(k*cv))*(kp*kp*sv/(k*cv*cv))
ck(s.cancel(derivative+2*kp*kp*sv*dv/cv) == 0, 'simple_outer_normal_zero_derivative')
ck(s.cancel(dv*dv-k*k*cv*cv*(dv/(k*cv))**2) == 0, 'outer_normal_zero_location')

# Generic common Jacobi poles: multiplying normal coordinates by t makes
# removability explicit whenever the leading bilinear norm is nonzero.
A, B, D, E, t = s.symbols('A B D E t')
vx, vy = A+t*B, D+t*E
u, v = vx/t, vy/t
old = X+(1-u*X-v*Y)*u/(u*u+v*v)
new = X+t*vx/(vx*vx+vy*vy)-vx*(vx*X+vy*Y)/(vx*vx+vy*vy)
ck(s.cancel(old-new) == 0, 'common_jacobi_pole_clearing_identity')
ck(s.cancel(new.subs(t, 0)-(X-A*(A*X+D*Y)/(A*A+D*D))) == 0,
   'common_jacobi_pole_finite_limit')

# Universal quadratic-area telescope in complex coordinates. U,V denote
# squared unit tangent phases, so the reciprocal phases are U^-1,V^-1.
U, V, z, w = s.symbols('U V z w', nonzero=True)
zi, wi = (z+U*w)/2, (w+z/U)/2
zj, wj = (z+V*w)/2, (w+z/V)/2
determinant = s.expand((wi*zj-zi*wj)/(2*s.I))
formula = ((V-U)*w*w+(1/U-1/V)*z*z+(V/U-U/V)*z*w)/(8*s.I)
ck(s.cancel(determinant-formula) == 0, 'universal_complex_quadratic_telescope')

def det(p, q):
    return p[0]*q[1]-p[1]*q[0]


def dot(p, q):
    return p[0]*q[0]+p[1]*q[1]


def pedal(normal, height, point):
    # Intersection of the line normal.X=height with the perpendicular
    # through point, solved as a two-line determinant problem.
    tangent = -normal[1], normal[0]
    rhs = dot(tangent, point)
    den = det(normal, tangent)
    return ((height*tangent[1]-normal[1]*rhs)/den,
            (normal[0]*rhs-height*tangent[0])/den)


def area(points):
    return sum(det(points[j], points[(j+1) % len(points)]) for j in range(len(points)))/2


for m in range(2, 17):
    # Vary cyclic order, allowing nonsimple/star-like line lists.
    for step in range(1, m):
        if gcd(step, m) != 1:
            continue
        first = [(F(1-j*j), F(2*j)) for j in [(i*step) % m+1 for i in range(m)]]
        normals = first+[(-x, -y) for x, y in first]
        heights = [F(i+2, i+1) for i in range(m)]*2
        f = lambda point: area([pedal(n, h, point) for n, h in zip(normals, heights)])
        b0 = f((F(0), F(0)))
        coeff = f((F(1), F(0)))-b0
        for point in [(F(x, 3), F(y, 5)) for x, y in product(range(-2, 3), repeat=2)]:
            ck(f(point) == b0+coeff*dot(point, point), 'exact_noncircular_line_radial_identity')

# Complete finite indexing controls on the reduced real period lattice.
period_cases = 0
for N in range(4, 257, 4):
    m = N//2
    for tau in range(1, m):
        if gcd(N, tau) != 1:
            continue
        period_cases += 1
        ck(gcd(m, tau) == 1 and m % 2 == 0, 'reduced_lattice_and_K_alignment')
        # Work modulo 2K=1; the two base poles differ by tau/m.
        poles = {j for j in range(N) if F(j*tau, m) % 1 in {F(0), F(tau, m) % 1}}
        ck(poles == {0, 1, m, m+1}, 'complete_simultaneous_pole_index_set')
        coincident_edges = {(j, (j+1) % N) for j in poles if (j+1) % N in poles}
        ck(coincident_edges == ({(j, (j+1) % 4) for j in range(4)} if N == 4 else
                                {(0, 1), (m, m+1)}), 'all_N4_cyclic_edges_included')
        ck(all(sum((j*tau) % m == a for j in range(N)) == 2 for a in range(m)),
           'trace_poles_nonzero_double_multiplicity')

for a, b in product([F(1, 3), F(1), F(7, 3)], repeat=2):
    normal = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    heights = [a, b, a, b]
    for x, y in product(range(-5, 6), repeat=2):
        ck(area([pedal(n, h, (F(x), F(y))) for n, h in zip(normal, heights)]) == 2*a*b,
           'rectangle_four_period_half_area_for_arbitrary_point')
ck(F(3, 4)*F(15, 16) == F(45, 64), 'star_exact_lower_angle_bound')
ck(F(3, 4)/F(15, 16) == F(4, 5), 'star_exact_upper_angle_bound')
ck(F(1, 2) < F(45, 64) < F(4, 5) < 1, 'star_strict_negative_double_sine_interval')

print(json.dumps({'status': 'PASS', 'exact_assertions': sum(C.values()),
                  'families': dict(sorted(C.items())), 'primitive_period_cases': period_cases,
                  'scope': 'Independent exact isotropic-coordinate, common-pole, radial-area, finite lattice and star-bound checks. Universal meromorphic and source-domain conclusions are established by the written review, not finite enumeration.'},
                 indent=2, sort_keys=True))
