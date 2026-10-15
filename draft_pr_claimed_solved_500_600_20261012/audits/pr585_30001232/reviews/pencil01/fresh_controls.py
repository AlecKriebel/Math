#!/usr/bin/env python3
"""Independent exact controls. These are not geometric-existence certificates.

Requires SymPy 1.14.0 for byte-exact replay of the saved JSON. No network,
mutation, private inputs, clocks, or assertions disabled by Python -O.
"""
import json
from collections import Counter
from fractions import Fraction
import sympy as sp

counts = Counter()


def check(name, condition):
    if not bool(condition):
        raise RuntimeError(name)
    counts[name] += 1


def primitive_linear_certificate(poly, variable):
    p = sp.Poly(poly, variable)
    if p.degree() != 1:
        return False
    a, b = p.all_coeffs()
    return a != 0 and sp.gcd(a, b) == 1


def main():
    x, y, z, s, t, u, v = sp.symbols('x y z s t u v')
    local_rows = []
    for degree in range(3, 24):
        a = x**(degree-1)-y**(degree-1)
        f = z*a+x**degree
        check('primitive_linear_integrality', primitive_linear_certificate(f, z))
        tangent = t**(degree-1)-1
        check('squarefree_tangent_cone', sp.gcd(tangent, sp.diff(tangent, t)) == 1)
        affine = f.subs(z, 1)
        terms = sp.Poly(affine, x, y).terms()
        order = min(sum(exp) for exp, _ in terms)
        check('affine_multiplicity', order == degree-1)
        gradients = [sp.diff(f, q) for q in (x, y, z)]
        origin = sp.groebner([q.subs(z, 1) for q in gradients], x, y)
        expected = [x**(degree-2), y**(degree-2)]
        check('affine_singular_ideal', [q.as_expr() for q in origin.polys] == expected)
        # Any point with Y != 0 is in this chart. With Y=0, f_Z forces X=0.
        other = sp.groebner([q.subs(y, 1) for q in gradients], x, z)
        check('complementary_projective_singular_chart', [q.as_expr() for q in other.polys] == [1])
        check('singular_line_Y_zero', gradients[2].subs(y, 0) == x**(degree-1))
        # A homogeneous parametrization, basepoint-free because gcd(A,s^d)=1.
        at = s**(degree-1)-t**(degree-1)
        coords = {x:s*at, y:t*at, z:-s**degree}
        check('normalization_substitution', sp.expand(f.subs(coords, simultaneous=True)) == 0)
        check('normalization_no_common_zero', sp.gcd(at, s**degree) == 1)
        check('normalization_generic_inverse', sp.expand(coords[x]*t-coords[y]*s) == 0)
        local_rows.append({'d':degree, 'multiplicity':order,
                           'jacobian_ideal_generators':[str(q) for q in expected],
                           'all_other_projective_points_excluded':True})

    # Dimension identities independently expressed in terms of monomial counts.
    dimension_rows = []
    for degree in range(2, 202):
        monomials = (degree+1)*(degree+2)//2
        space_dimension = monomials-1
        product_dims = []
        for left_degree in range(1, degree):
            right_degree = degree-left_degree
            left_count = (left_degree+1)*(left_degree+2)//2
            right_count = (right_degree+1)*(right_degree+2)//2
            image_bound = left_count+right_count-2
            deficit = space_dimension-image_bound
            check('factor_dimension_identity', deficit == left_degree*right_degree)
            product_dims.append(image_bound)
        check('reducible_max_dimension', space_dimension-max(product_dims) == degree-1)
        join_bound = max(product_dims)+1
        check('join_is_proper_exact_threshold', (join_bound < space_dimension) == (degree >= 3))
        if degree in (2,3,6,7,201):
            dimension_rows.append({'d':degree, 'ambient_dimension':space_dimension,
                                   'reducible_dimension_bound':max(product_dims),
                                   'join_dimension_bound':join_bound})

    # Restriction of O(d) separates values and every tangent direction: the
    # monomials 1,x,y in an affine chart already give all length-two jets.
    for qx in range(-2, 3):
        for qy in range(-2, 3):
            full_jets = sp.Matrix([[1, qx, qy], [0,1,0], [0,0,1]])
            check('full_jet_surjectivity', full_jets.det() == 1)
            for tx, ty in [(1,0),(0,1),(1,1),(1,-1),(2,3)]:
                curve_jets = sp.Matrix([[1, qx, qy],[0,tx,ty]])
                check('curve_jet_surjectivity', curve_jets.rank() == 2)
    # Local blowup uv-graph: u*beta-v*alpha=0. In alpha=1, v=u*beta.
    alpha, beta = sp.symbols('alpha beta')
    graph = u*beta-v*alpha
    check('blowup_graph_chart', sp.expand(graph.subs({alpha:1,v:u*beta})) == 0)
    for aa in range(-4,5):
        for bb in range(-4,5):
            if aa or bb:
                check('member_simple_at_transverse_basepoint', (sp.diff(aa*u+bb*v,u),sp.diff(aa*u+bb*v,v)) != (0,0))

    degree = sp.symbols('d', integer=True)
    # Use the restricted Gram matrix for H,F,E1, not the old full diagonal
    # blowup-vector computation or its incidence-hypersurface computation.
    gram = sp.Matrix([[1,degree,0],[degree,0,1],[0,1,-1]])
    H = sp.Matrix([1,0,0])
    F = sp.Matrix([0,1,0])
    E = sp.Matrix([0,0,1])
    A = 2*F+E
    K = (degree-3)*H-F
    N = K+2*F

    def pair(a,b):
        return sp.factor((a.T*gram*b)[0])

    identities = {'A_squared':pair(A,A), 'A_dot_F':pair(A,F),
                  'A_dot_E':pair(A,E), 'N_squared':pair(N,N),
                  'N_dot_E':pair(N,E), 'K_dot_F':pair(K,F),
                  'cover_K_squared':2*pair(N,N),
                  'cover_L_squared':2*pair(A,A)}
    expected = {'A_squared':3,'A_dot_F':1,'A_dot_E':1,
                'N_squared':3*(degree-1)*(degree-3),'N_dot_E':1,
                'K_dot_F':degree*(degree-3),
                'cover_K_squared':6*(degree-1)*(degree-3),
                'cover_L_squared':6}
    for name,value in identities.items():
        check('symbolic_restricted_lattice', sp.expand(value-expected[name]) == 0)
    e, excess = sp.symbols('e excess', nonnegative=True, integer=True)
    r = degree*e-excess
    check('universal_Bezout_positivity_identity',
          sp.expand((2*degree-3)*e-r-((degree-3)*e+excess)) == 0)

    # Local base change is regular at each smooth branch fibre. Branching
    # through the marked singular point would instead give a singular source.
    smooth_relation = t-v**2
    check('smooth_branch_local_Jacobian', sp.diff(smooth_relation,t) == 1)
    bad_relation = v**2-(x**6-y**6+x**7)
    bad_gradient = [sp.diff(bad_relation,q).subs({x:0,y:0,v:0}) for q in (x,y,v)]
    check('negative_branch_through_singular_fibre_detected', bad_gradient == [0,0,0])
    branch_rows = []
    for branch_count in (0,2,4,6,8):
        D = sp.Rational(branch_count,2)*F
        section_K_intersection = sp.simplify(2*pair(K+D,E))
        genus = Fraction(branch_count-2,2)
        check('branch_Hurwitz_section_consistency', section_K_intersection == 2*genus)
        check('branch_section_positivity_threshold', (section_K_intersection > 0) == (branch_count >= 4))
        branch_rows.append({'branch_points':branch_count,
                            'section_K_intersection':int(section_K_intersection),
                            'formal_Hurwitz_genus_connected_cover_exists_only_if_nonnegative':str(genus)})
    # n=0 is the formal unramified comparison; no connected genus -1 curve exists.
    Q, T = sp.symbols('Q T')
    cover_gram = sp.Matrix([[0,1],[1,-2]])
    ell = sp.Matrix([4,1])
    fibre = sp.Matrix([1,0])
    check('individual_cover_fibre_degree', (ell.T*cover_gram*fibre)[0] == 1)
    check('total_cover_fibre_degree', (ell.T*cover_gram*(2*fibre))[0] == 2)
    check('cover_polarization_square', (ell.T*cover_gram*ell)[0] == 6)

    threshold_rows = []
    for dd in range(4, 2002):
        k2 = 6*(dd-1)*(dd-3)
        margin = (dd-3)**4-k2
        cubic = (dd-3)**3-6*(dd-1)
        check('strict_inequality_primary_denominator', (margin > 0) == (dd >= 7))
        check('fourth_power_reduction', margin == (dd-3)*cubic)
        delta = (dd-2)**3-6*dd-cubic
        check('successive_difference', delta == 3*(dd-3)**2+3*(dd-3)-5)
        if dd >= 7:
            check('positive_successive_difference', delta > 0)
        if dd <= 9 or dd == 2001:
            threshold_rows.append({'d':dd,'K2':k2,'L2':6,'epsilon_upper_bound':str(Fraction(1,dd-1)),
                                   'strict_margin':margin,
                                   'specified_witness_strictly_violates_primary_bound':margin>0})

    negative = []

    def reject(name, false_claim):
        check('negative_formula_rejections', not false_claim)
        negative.append({'mutation':name,'rejected':True})

    reject('nonprimitive_linear_Z_integrality', primitive_linear_certificate(z*x**6+x**7,z))
    reject('repeated_tangent_root_called_ordinary', sp.gcd((t-1)**6,sp.diff((t-1)**6,t)) == 1)
    reject('degree_two_join_claimed_proper', 4+1 < 5)
    reject('degree_six_primary_violation', (6-3)**4 > 6*(6-1)*(6-3))
    reject('branch_correction_F_instead_of_2F', pair(K+F,E) > 0)
    reject('lifted_E_called_rational_minus_one', (-2,1) == (-1,0))
    reject('one_lifted_fibre_degree_doubled', (ell.T*cover_gram*fibre)[0] == 2)
    reject('pullback_F_mistaken_single_fibre', (ell.T*cover_gram*(2*fibre))[0] == 1)
    reject('forgot_cover_degree_on_K2', 3*(7-1)*(7-3) == 144)
    reject('wrong_primary_root_formula_at_K2_zero', Fraction(1,2)**4 == Fraction(1,2))
    check('degree_seven_exact_strict_target', 144 < (6-2)**4)
    check('degree_seven_stronger_catalogue_target', 144+2 < 6**4)
    result = {'status':'PASS','geometric_existence_not_certified_by_finite_controls':True,
              'sympy_version':sp.__version__, 'counts':dict(sorted(counts.items())),
              'total_checks':sum(counts.values()), 'local_polynomial_rows':local_rows,
              'dimension_selected_rows':dimension_rows,
              'symbolic_lattice':{k:str(v) for k,v in identities.items()},
              'branch_comparisons':branch_rows, 'threshold_selected_rows':threshold_rows,
              'negative_controls':negative}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
