"""Exact source-defined controls for k403,b; no numerical identities here."""
from collections import Counter
from fractions import Fraction as F
from math import gcd
from itertools import product
import json
import sympy as z

counts = Counter()


def ck(ok, label):
    assert ok, label
    counts[label] += 1


k, s, S, c, d, C, D, h = z.symbols('k s S c d C D h')
L = 1-k*k*s*s*S*S
H = 1-2*k*k*s*s+k*k*s**4
Rx = -(H*S+k*(c*c-d*d*S*S))/(c*c*L)
Ry = C*(2*h*h-H*(1+k*S))/(h*c*c*L)
a, b = d/c, h/c
relations = [C*C+S*S-1, D*D+k*k*S*S-1, d*d+k*k*s*s-1,
             h*h+k*k-1, c*c+s*s-1]
G = z.groebner(relations, C, D, d, h, c, k, s, S, order='lex')


def reduce_zero(expression):
    numerator = z.fraction(z.together(expression))[0]
    return G.reduce(z.expand(numerator))[1] == 0


ends = []
for sign in [-1, 1]:
    sn = (S*c*d+sign*s*C*D)/L
    cn = (C*c-sign*S*s*D*d)/L
    Px, Py = -a*sn, b*cn
    ends.append((Px, Py))
    ck(reduce_zero((Px-k)*(Rx-Px)+Py*(Ry-Py)), 'symbolic_actual_antipedal_line_incidence')
    ck(reduce_zero(Px*Px/a**2+Py*Py/b**2-1), 'symbolic_endpoint_on_outer_ellipse')
det = (ends[0][0]-k)*ends[1][1]-ends[0][1]*(ends[1][0]-k)
ck(reduce_zero(det-2*h*s*d*D*(1+k*S)/(c*L)), 'symbolic_focal_normal_determinant')
ck(reduce_zero(a*a-b*b-k*k), 'symbolic_confocality')
nx, ny = -S, C/h
norm = nx*nx+ny*ny
qx = k+(1-nx*k)*nx/norm
qy = (1-nx*k)*ny/norm
ck(reduce_zero(qx-(k-S)/(1-k*S)), 'symbolic_actual_pedal_x')
ck(reduce_zero(qy-h*C/(1-k*S)), 'symbolic_actual_pedal_y')
ck(reduce_zero(((k-S)/(1-k*S))**2+(h*C/(1-k*S))**2-1), 'focal_pedal_circle_control')

# The extra apparent focal denominator is absent from the final vertex
# formula; substituting its root is generically regular in the sn variable.
ck(z.cancel(L.subs(S, -1/k)) == 1-s*s, 'extra_focal_denominator_cancelled')
ck(z.cancel(L.subs(S, 1/(k*s))) == 0 and
   z.cancel(L.subs(S, -1/(k*s))) == 0, 'two_actual_antivertex_pole_values')
ck(z.cancel((1-S*S).subs(S, 1/(k*s))) != 0 and
   z.cancel((1-k*k*S*S).subs(S, 1/(k*s))) != 0,
   'actual_pole_derivative_factors_not_identically_zero')

# Exact arithmetic of primitive periods, residues and half-period shifts.
period_cases = 0
for N in range(4, 257, 4):
    m = N//2
    for tau in range(1, m):
        if gcd(N, tau) != 1:
            continue
        period_cases += 1
        ck(tau % 2 == 1 and m % 2 == 0 and gcd(tau, m) == 1,
           'primitive_target_parity')
        ck(F(m+tau, 2) % 1 == F(1, 2), 'pedal_complementary_halfperiod')
        ck(F(m-tau, 2) % 1 == F(1, 2), 'pedal_pole_class_complementary_halfperiod')
        ck(sum(j*tau % m == 0 for j in range(N)) == 2, 'noncancelling_trace_residue_multiplicity')
        ck({j for j in range(N) if j*tau % N == 0} == {0}, 'single_focal_foot_pole_per_real_orbit')
        antipoles = {(N-1) % N, 0, m-1, m}
        ck(len(antipoles) == 4, 'four_antivertex_poles_including_N4')
        double_edges = {(j, (j+1) % N) for j in range(N)
                        if j in antipoles and (j+1) % N in antipoles}
        ck(len(double_edges) == (4 if N == 4 else 2), 'all_N4_cyclic_double_pole_edges_present')


def determinant(p, q):
    return p[0]*q[1]-p[1]*q[0]


def dot(p, q):
    return p[0]*q[0]+p[1]*q[1]


def area(points):
    return sum(determinant(points[i], points[(i+1) % len(points)])
               for i in range(len(points)))/2


def derived(points, focus):
    feet, anti = [], []
    for i, p in enumerate(points):
        q = points[(i+1) % len(points)]
        edge = q[0]-p[0], q[1]-p[1]
        t = dot((focus[0]-p[0], focus[1]-p[1]), edge)/dot(edge, edge)
        feet.append((p[0]+t*edge[0], p[1]+t*edge[1]))
        n, v = (p[0]-focus[0], p[1]-focus[1]), (q[0]-focus[0], q[1]-focus[1])
        hh, gg = dot(n, p), dot(v, q)
        denominator = determinant(n, v)
        if denominator == 0:
            return None
        anti.append(((hh*v[1]-gg*n[1])/denominator,
                     (n[0]*gg-v[0]*hh)/denominator))
    return feet, anti


# Central pairing makes the two focal areas equal without any area division.
for m in range(2, 15):
    for step in range(1, m):
        if gcd(step, m) != 1:
            continue
        first = []
        for i in range(m):
            t = F((i*step) % m+1, m+1)
            first.append((5*(1-t*t)/(1+t*t), 6*t/(1+t*t)))
        points = first+[(-x, -y) for x, y in first]
        plus, minus = derived(points, (F(4), F(0))), derived(points, (F(-4), F(0)))
        if plus is None or minus is None:
            continue
        ck(area(plus[0]) == area(minus[0]), 'exact_central_focal_pedal_equality')
        ck(area(plus[1]) == area(minus[1]), 'exact_central_focal_antipedal_equality')

# Two actual primitive four-period billiards with the same confocal caustic.
root5 = z.sqrt(5)
focus = (z.sqrt(3), z.Integer(0))
orbits = [([(2, 0), (0, 1), (-2, 0), (0, -1)], (z.Rational(32, 25), z.Integer(8))),
          ([(4/root5, 1/root5), (-4/root5, 1/root5),
            (-4/root5, -1/root5), (4/root5, -1/root5)],
           (z.Rational(8, 5), z.Rational(32, 5)))]
for points, expected in orbits:
    points = [tuple(z.sympify(t) for t in p) for p in points]
    ck(len(set(points)) == 4, 'low_period_primitive_distinct_vertices')
    for i, p in enumerate(points):
        q, prev = points[(i+1) % 4], points[i-1]
        ck(z.simplify(p[0]**2/4+p[1]**2-1) == 0, 'low_period_outer_incidence')
        chord_normal = p[1]-q[1], q[0]-p[0]
        hh = dot(chord_normal, p)
        ck(z.simplify(z.Rational(16, 5)*chord_normal[0]**2+
                      z.Rational(1, 5)*chord_normal[1]**2-hh**2) == 0,
           'low_period_same_confocal_caustic_tangency')
        vin = z.Matrix([p[0]-prev[0], p[1]-prev[1]])
        vout = z.Matrix([q[0]-p[0], q[1]-p[1]])
        vin /= z.sqrt(vin.dot(vin)); vout /= z.sqrt(vout.dot(vout))
        n = z.Matrix([p[0]/4, p[1]])
        reflected = vin-2*vin.dot(n)/n.dot(n)*n
        ck(all(z.simplify(t) == 0 for t in reflected-vout), 'low_period_actual_specular_reflection')
    feet, anti = derived(points, focus)
    ck(z.simplify(area(feet)-expected[0]) == 0, 'low_period_exact_pedal_area')
    ck(z.simplify(area(anti)-expected[1]) == 0, 'low_period_exact_antipedal_area')
    ck(z.simplify(area(feet)*area(anti)-z.Rational(256, 25)) == 0,
       'low_period_exact_common_product')

print(json.dumps({'status': 'PASS', 'exact_assertions': sum(counts.values()),
                  'families': dict(sorted(counts.items())),
                  'primitive_period_controls': period_cases,
                  'scope': 'Exact symbolic line geometry, arithmetic and finite controls. Pole completeness, symmetry cancellation and compact-torus constancy are proved analytically in PROOF.md; finite controls do not replace them.'},
                 indent=2, sort_keys=True))
