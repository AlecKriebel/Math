#!/usr/bin/env python3
"""Exact diagnostic controls, not a formal checker of the geometric proof."""
from fractions import Fraction as Q
import json

def poly(d):
    return {k: Q(v) for k, v in d.items() if v}
def add(a, b):
    return poly({k: a.get(k, 0) + b.get(k, 0) for k in a.keys() | b.keys()})
def neg(a):
    return {k: -v for k, v in a.items()}
def sub(a, b):
    return add(a, neg(b))
def mul(a, b):
    out = {}
    for k, v in a.items():
        for l, w in b.items():
            out[k+l] = out.get(k+l, 0) + v*w
    return poly(out)
def Dt(a):
    # u = exp(t), so d/dt(u^k) = k u^k.
    return poly({k: k*v for k, v in a.items()})

def run():
    passed = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        passed.append(name)
    one = {0: Q(1)}
    f = {1: Q(1, 2), -1: Q(1, 2)}
    fp = {1: Q(1, 2), -1: Q(-1, 2)}
    check('warp_first_derivative', Dt(f) == fp)
    check('warp_second_derivative', Dt(fp) == f)
    check('hyperbolic_identity', sub(mul(f, f), mul(fp, fp)) == one)
    check('radial_curvature_residual', sub(Dt(Dt(f)), f) == {})
    check('tangential_curvature_residual', sub(sub(mul(f, f), mul(fp, fp)), one) == {})
    # The coefficient of m and the constant coefficient of the Ricci residual
    # vanish independently; this is an identity in every dimension m.
    check('ricci_parameter_coefficient', sub(sub(mul(f, f), mul(fp, fp)), one) == {})
    check('ricci_constant_coefficient', add(sub(one, mul(f, Dt(Dt(f)))), mul(fp, fp)) == {})
    # A = x cosh(t) after u=2/x, hence A=1+x^2/4.
    A = {0: Q(1), 2: Q(1, 4)}
    x_f_substituted = poly({1-k: v*Q(2)**k for k, v in f.items()})
    check('geodesic_warp_substitution', A == x_f_substituted)
    A2 = mul(A, A)
    check('geodesic_even_expansion', A2 == {0: Q(1), 2: Q(1, 2), 4: Q(1, 16)})
    check('boundary_metric_coefficient', A2[0] == 1)
    check('all_warp_powers_even', all(k % 2 == 0 for k in A2))
    # cos(s)=2u/(u^2+1), sin(s)=(u^2-1)/(u^2+1).
    C, S, B = {1: Q(2)}, {2: Q(1), 0: Q(-1)}, {2: Q(1), 0: Q(1)}
    check('compactification_trig_identity', add(mul(C, C), mul(S, S)) == mul(B, B))
    check('compactification_warp_inverse', mul(C, f) == B)
    dC_B_minus_C_dB = sub(mul(Dt(C), B), mul(C, Dt(B)))
    check('defining_function_s_derivative', dC_B_minus_C_dB == neg(mul(S, C)))
    check('defining_function_boundary_gradient_square',
          (S[0]/B[0])**2 == 1 and (S[2]/B[2])**2 == 1)
    # Explicit quotient of a hexagon by side pairs (0,1),(2,3),(4,5).
    parent = list(range(6))
    def root(a):
        while parent[a] != a:
            a = parent[a]
        return a
    def union(a, b):
        parent[root(a)] = root(b)
    graph = {('l', i): set() for i in range(6)}
    graph.update({('r', i): set() for i in range(6)})
    def edge(a, b):
        graph[a].add(b)
        graph[b].add(a)
    for i in range(6):
        edge(('l', i), ('r', i))
    for i, j in [(0, 1), (2, 3), (4, 5)]:
        union(i, j)
        union((i+1) % 6, (j+1) % 6)
        edge(('r', i), ('r', j))
        edge(('l', (i+1) % 6), ('l', (j+1) % 6))
    check('hexagon_single_vertex_class', len({root(i) for i in range(6)}) == 1)
    seen, stack = set(), [('l', 0)]
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            stack.extend(graph[node] - seen)
    check('hexagon_vertex_link_is_one_cycle', len(seen) == 12 and all(len(v) == 2 for v in graph.values()))
    check('hexagon_total_vertex_angle_in_pi_units', 6*Q(1, 3) == 2)
    check('hyperbolic_triangle_angle_sum_less_than_pi', Q(1, 6)+Q(1, 6)+Q(1, 2) < 1)
    chi_N = 1-3+1
    check('base_euler_characteristic', chi_N == -1)
    check('orientation_cover_genus_two', 2*chi_N == 2-2*2)
    # A finite model checks the orbit-identification logic, not the existence
    # of a hyperbolic surface or the topology of the full quotient.
    tau = {0: 1, 1: 0, 2: 3, 3: 2}
    J = lambda z: (-z[0], tau[z[1]])
    points = {(s, p) for s in [-1, 0, 1] for p in tau}
    check('model_involution', all(J(J(z)) == z for z in points))
    check('model_free_action_including_center', all(J(z) != z for z in points))
    boundary = {(s, p) for s in [-1, 1] for p in tau}
    orbits = {frozenset([z, J(z)]) for z in boundary}
    check('model_boundary_one_positive_representative', all(sum(s == 1 for s, p in o) == 1 for o in orbits))
    check('model_boundary_not_fiber_quotient', len(orbits) == len(tau) and len(orbits) != len(tau)//2)
    check('orientation_sign_product', (-1)*(-1) == 1)
    # Exact falsification controls for nearby incorrect constructions.
    badf = {2: Q(1, 2), -2: Q(1, 2)}
    check('negative_control_wrong_warp_scale', sub(Dt(Dt(badf)), badf) != {})
    check('negative_control_sinh_hyperbolic_fiber', sub(sub(mul(fp, fp), mul(f, f)), one) != {})
    check('negative_control_flat_fiber', sub(mul(f, f), mul(fp, fp)) != {})
    reflection = lambda z: (-z[0], z[1])
    check('negative_control_reflection_has_fixed_points', all(reflection((0, p)) == (0, p) for p in tau))
    preserve_ends = lambda z: (z[0], tau[z[1]])
    unchanged_end_orbits = {frozenset([z[0], preserve_ends(z)[0]]) for z in boundary}
    check('negative_control_no_end_swap', unchanged_end_orbits == {frozenset([-1]), frozenset([1])})
    check('negative_control_orientation_preserving_tau', (-1)*(+1) == -1)
    return {'result': 'PASS', 'assertion_count': len(passed), 'checks': passed,
            'scope': 'Exact algebra, finite polygon gluing, orbit-model diagnostics and negative controls. The written geometric proof remains necessary.'}

if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
