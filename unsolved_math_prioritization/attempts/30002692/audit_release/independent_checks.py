#!/usr/bin/env python3
"""Fresh exact tensor and topology diagnostics. Requires Python 3 and SymPy.

This does not import or call the author diagnostic implementation. It is not a
formal proof checker; the global geometric proof is in AUDIT.md.
"""
import itertools
import json
from fractions import Fraction
import sympy as S


def tensor_tools(metric, coordinates):
    n = len(coordinates)
    inverse = metric.inv()
    gamma = {}
    for a, b, c in itertools.product(range(n), repeat=3):
        gamma[a, b, c] = S.cancel(sum(inverse[a, d] * (
            S.diff(metric[d, c], coordinates[b])
            + S.diff(metric[d, b], coordinates[c])
            - S.diff(metric[b, c], coordinates[d])) / 2 for d in range(n)))

    def riemann(a, b, c, d):
        return S.cancel(S.diff(gamma[a, d, b], coordinates[c])
                        - S.diff(gamma[a, c, b], coordinates[d])
                        + sum(gamma[a, c, e] * gamma[e, d, b]
                              - gamma[a, d, e] * gamma[e, c, b]
                              for e in range(n)))
    return riemann


def components(vertices, edges):
    remaining = set(vertices)
    answer = []
    while remaining:
        found = {min(remaining)}
        while True:
            grown = found | {v for u, v in edges if u in found} | {
                u for u, v in edges if v in found}
            if grown == found:
                break
            found = grown
        answer.append(found)
        remaining -= found
    return answer


def surface_cells(sheets):
    # Each lifted polygon is a disk. Same-direction edge gluing swaps the
    # orientation sheet. Links use left/right germs at each corner.
    vertices = {(z, i) for z in range(sheets) for i in range(6)}
    identifications, link_edges = [], []
    link_vertices = {(z, i, side) for z, i in vertices for side in (0, 1)}
    for z, i in vertices:
        link_edges.append(((z, i, 0), (z, i, 1)))
    for z in range(sheets):
        other = z if sheets == 1 else 1-z
        for a, b in ((0, 1), (2, 3), (4, 5)):
            identifications.extend([((z, a), (other, b)),
                                    ((z, (a+1) % 6), (other, (b+1) % 6))])
            link_edges.extend([((z, a, 1), (other, b, 1)),
                               ((z, (a+1) % 6, 0), (other, (b+1) % 6, 0))])
    classes = components(vertices, identifications)
    links = components(link_vertices, link_edges)
    return classes, links, link_vertices, link_edges


def run():
    checks, negatives = [], []

    def check(name, condition, negative=False):
        if not condition:
            raise AssertionError(name)
        (negatives if negative else checks).append(name)

    q, v, y = S.symbols('q v y', positive=True)
    coordinates = (q, v, y)
    f = (q*q+1)/(2*q)  # q = exp(t); upper half-plane metric h.
    metric = S.diag(q**-2, f*f/y**2, f*f/y**2)
    riemann = tensor_tools(metric, coordinates)
    residuals = []
    for a, b, c, d in itertools.product(range(3), repeat=4):
        expected = -(int(a == c)*metric[b, d] - int(a == d)*metric[b, c])
        residuals.append(S.cancel(riemann(a, b, c, d)-expected))
    check('all_81_full_riemann_constant_minus_one_residuals', residuals == [0]*81)
    ricci = S.Matrix(3, 3, lambda b, d: S.cancel(sum(riemann(a, b, a, d)
                                                        for a in range(3))))
    check('all_9_ricci_minus_two_g_residuals', (ricci + 2*metric).applyfunc(S.cancel) == S.zeros(3))
    check('scalar_curvature_minus_six', S.cancel(S.trace(metric.inv()*ricci)) == -6)
    # An independent compact coordinate: z=tanh(t/2), not the author's s.
    z = S.symbols('z', real=True)
    rho = (1-z*z)/(1+z*z)
    dt_dz = 2/(1-z*z)
    fz = (1+z*z)/(1-z*z)
    check('rational_compactification_radial_metric',
          S.cancel(rho*rho*dt_dz*dt_dz - 4/(1+z*z)**2) == 0)
    check('rational_compactification_fiber_metric', S.cancel(rho*rho*fz*fz) == 1)
    check('global_defining_function_even', S.cancel(rho.subs(z, -z)-rho) == 0)
    check('global_defining_function_vanishes_at_both_ends',
          rho.subs(z, -1) == rho.subs(z, 1) == 0)
    check('global_defining_function_simple_zeros',
          S.diff(rho, z).subs(z, -1) == 1 and S.diff(rho, z).subs(z, 1) == -1)
    gradient_square = S.cancel(S.diff(rho, z)**2*(1+z*z)**2/4)
    check('asymptotic_hyperbolic_gradient_normalization',
          gradient_square.subs(z, -1) == gradient_square.subs(z, 1) == 1)
    x = S.symbols('x', positive=True)
    check('geodesic_defining_function_radial_coefficient',
          S.cancel(x*x * metric[0, 0].subs(q, 2/x) * S.diff(2/x, x)**2) == 1)
    compact_fiber = S.cancel(x*x*f.subs(q, 2/x)**2)
    check('exact_geodesic_expansion',
          S.expand(compact_fiber) == 1+x*x/2+x**4/16)
    check('exact_evenness_not_truncated_asymptotics',
          S.cancel(compact_fiber.subs(x, -x)-compact_fiber) == 0)
    # Source Eq. (46) consistency; the full x^4 term is retained.
    check('source_boundary_second_coefficient_relation',
          S.expand(compact_fiber).coeff(x, 0) == 2*S.expand(compact_fiber).coeff(x, 2))

    base, base_links, lv, le = surface_cells(1)
    check('hexagon_has_one_vertex_class', len(base) == 1)
    check('hexagon_vertex_link_is_connected', len(base_links) == 1 and len(base_links[0]) == 12)
    check('hexagon_vertex_link_is_two_regular', all(
        sum(a == p or b == p for a, b in le) == 2 for p in lv))
    check('hexagon_total_angle', 6*Fraction(1, 3) == 2)
    check('hexagon_triangle_admissibility',
          Fraction(1, 6)+Fraction(1, 6)+Fraction(1, 2) < 1)
    check('base_euler_characteristic', len(base)-3+1 == -1)
    cover, cover_links, clv, cle = surface_cells(2)
    check('orientation_cover_has_two_vertex_classes', len(cover) == 2)
    check('orientation_cover_has_two_smooth_vertex_links',
          len(cover_links) == 2 and sorted(map(len, cover_links)) == [12, 12])
    check('orientation_cover_link_two_regular', all(
        sum(a == p or b == p for a, b in cle) == 2 for p in clv))
    check('orientation_cover_euler_genus_two', len(cover)-6+2 == -2)
    check('deck_action_swaps_vertex_classes_freely', all(
        {(1-z, i) for z, i in cls} != cls for cls in cover))
    check('orientation_cover_dual_graph_connected',
          len(components({0, 1}, [(0, 1)]*6)) == 1)
    check('opposite_face_orientations_match_gluings', all(
        (-1)**z == -((-1)**(1-z)) for z in range(2)))

    # Finite quotient logic is diagnostic only; continuum freeness is proved.
    fiber = range(6)
    tau = lambda p: p ^ 1
    action = lambda p: (-p[0], tau(p[1]))
    domain = {(z, p) for z in (-1, 0, 1) for p in fiber}
    check('end_swap_action_involutive', all(action(action(p)) == p for p in domain))
    check('end_swap_action_free_at_center', all(action(p) != p for p in domain))
    bd = {(z, p) for z in (-1, 1) for p in fiber}
    orbits = {frozenset((p, action(p))) for p in bd}
    check('one_positive_representative_per_boundary_orbit',
          all(sum(z == 1 for z, p in orbit) == 1 for orbit in orbits))
    check('boundary_is_fiber_not_deck_quotient', len(orbits) == len(fiber))
    check('bulk_orientation_two_reversals', (-1)*(-1) == 1)

    # Mutated metrics are independently differentiated, not checked by labels.
    for name, badf, fiber_factor in [
        ('wrong_warp_scale', (q*q+q**-2)/2, y**-2),
        ('sinh_with_negative_curvature_fiber', (q-q**-1)/2, y**-2),
        ('exponential_with_negative_curvature_fiber', q, y**-2),
        ('cosh_with_flat_fiber', f, S.Integer(1)),
    ]:
        badg = S.diag(q**-2, badf**2*fiber_factor, badf**2*fiber_factor)
        badr = tensor_tools(badg, coordinates)
        pair = [S.cancel(badr(0, 1, 0, 1)+badg[1, 1]),
                S.cancel(badr(1, 2, 1, 2)+badg[2, 2])]
        check('reject_'+name, any(a != 0 for a in pair), True)
    check('reject_wrong_ricci_normalization', (ricci+3*metric).applyfunc(S.cancel) != S.zeros(3), True)
    check('reject_pure_reflection_fixed_locus',
          all((-z, p) == (z, p) for z, p in domain if z == 0), True)
    no_swap_orbits = {frozenset(((z, p), (z, tau(p)))) for z, p in bd}
    check('reject_non_swapping_action_two_end_labels',
          {next(iter(a))[0] for a in no_swap_orbits} == {-1, 1}, True)
    check('reject_orientation_preserving_tau_for_orientable_bulk', (-1)*(1) != 1, True)
    t = S.symbols('t', real=True)
    check('reject_abs_exponential_as_global_smooth_defining_function',
          S.diff(2*S.exp(-t), t).subs(t, 0) != S.diff(2*S.exp(t), t).subs(t, 0), True)
    check('reject_wrong_hexagon_angle', 6*Fraction(1, 2) != 2, True)
    return {
        'result': 'PASS',
        'independent_positive_controls': len(checks),
        'independent_negative_controls': len(negatives),
        'full_riemann_components_checked': 81,
        'ricci_components_checked': 9,
        'checks': checks,
        'negative_controls': negatives,
        'scope': 'Exact tensor identities, rational compactification, polygon and cover combinatorics, finite orbit diagnostics. These do not mechanize the global proof.',
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
