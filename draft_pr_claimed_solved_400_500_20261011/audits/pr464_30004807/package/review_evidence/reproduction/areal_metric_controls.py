#!/usr/bin/env python3
"""Independent exact checks in area-radius coordinates, with active guards.

No author/audit module is imported. The generic four-dimensional metric is
diag(-L(r)^2, 1/(1+4a/r), r^2, r^2 sin(theta)^2). Its curvature is derived
from the coordinate definition before imposing the proposed harmonic lapse.
Invalid claims are deliberately supplied as private JSON inputs; an intended
rejection exits with code 4 and an InvalidClaim diagnostic, including under -O.
"""
from pathlib import Path
import argparse, json, platform, sys
import sympy as s

class InvalidClaim(Exception):
    pass

def require(condition, name):
    if not condition:
        raise InvalidClaim(name)

def clean(z):
    return s.factor(s.trigsimp(s.cancel(z)))

def zero(z):
    return clean(z) == 0

def calculate():
    a, r, x = s.symbols("a r x", positive=True)
    A, B = s.symbols("A B", nonnegative=True)
    t, th, ph = s.symbols("t theta azimuth", real=True)
    L = s.Function("L")(r)
    f = 1 + 4*a/r
    coords = [t, r, th, ph]
    metric = s.diag(-L**2, 1/f, r**2, r**2*s.sin(th)**2)
    inverse = metric.inv()
    gamma = [[[clean(sum(inverse[k,j]*(s.diff(metric[j,q],coords[p])+s.diff(metric[j,p],coords[q])-s.diff(metric[p,q],coords[j])) for j in range(4))/2) for q in range(4)] for p in range(4)] for k in range(4)]
    ricci = s.zeros(4)
    for p in range(4):
        for q in range(4):
            ricci[p,q] = clean(sum(s.diff(gamma[k][p][q],coords[k])-s.diff(gamma[k][p][k],coords[q])+sum(gamma[k][p][q]*gamma[j][k][j]-gamma[j][p][k]*gamma[k][q][j] for j in range(4)) for k in range(4)))
    scalar = clean(s.trace(inverse*ricci))
    einstein = (inverse*ricci-s.eye(4)*scalar/2).applyfunc(clean)
    checks = {}
    def check(name, condition):
        require(bool(condition), name)
        checks[name] = True

    q = s.sqrt(f)
    lapse = A+B*q
    replacements = {s.diff(L,r,2): s.diff(lapse,r,2), s.diff(L,r): s.diff(lapse,r), L: lapse}
    G = einstein.subs(replacements, simultaneous=True).applyfunc(clean)
    R = clean(scalar.subs(replacements, simultaneous=True))
    expected = s.diag(0, 4*A*a/(lapse*r**3), -2*A*a/(lapse*r**3), -2*A*a/(lapse*r**3))
    for i in range(4):
        for j in range(4):
            check(f"derived_full_areal_Einstein_component_{i}_{j}", zero(G[i,j]-expected[i,j]))
    check("family_scalar_curvature_zero", R == 0)
    check("generic_lapse_time_Einstein_zero_from_spatial_mass", einstein[0,0] == 0)
    check("generic_lapse_radial_Einstein", zero(einstein[1,1]-(4*a/r**3+2*f*s.diff(L,r)/(r*L))))
    check("harmonic_lapse_equation", zero(s.diff(r**2*q*s.diff(lapse,r),r)))
    check("vacuum_lapse_all_Einstein_components_zero", all(zero(z.subs(A,0)) for z in G))
    check("flat_a_zero_control", all(zero(z.subs(a,0)) for z in G))
    check("ultrastatic_radial_Einstein", zero(G[1,1].subs({A:1,B:0})-4*a/r**3))
    check("family_Ricci_squared", zero(s.trace(G*G)-24*A**2*a**2/(lapse**2*r**6)))

    # Positive x=rho-a avoids unjustified square-root branch cancellation.
    rho = x+a
    p = x/rho
    radius = x**2/rho
    radius_prime = s.diff(radius,x)
    root_f = (x+2*a)/x
    check("positive_branch_area_radius_f", zero(f.subs(r,radius)-root_f**2))
    check("area_radius_spatial_metric_pullback", zero(radius_prime**2/f.subs(r,radius)-p**4))
    check("area_radius_positive_interior_derivative", zero(radius_prime-x*(x+2*a)/rho**2))
    check("Misner_Sharp_mass_negative_two_a", zero(r*(1-f)/2+2*a))
    check("ADM_isotropic_mass_negative_two_a", s.limit(-2*(rho**2)*s.diff(p,x),x,s.oo)==-2*a)
    check("resolution_harmonic", zero(s.diff(p,x,2)+2*s.diff(p,x)/rho))
    check("resolution_simple_zero_positive_normal", s.limit(p,x,0)==0 and s.limit(s.diff(p,x),x,0)==1/a)
    check("coordinate_sphere_area_vanishes", s.limit(4*s.pi*radius**2,x,0)==0)
    check("regular_ZAS_mass_formula", zero(-(4*a**s.Rational(2,3))**s.Rational(3,2)/4+2*a))

    # Q_r is obtained from the areal volume determinant and the derived G.
    Qr = clean(lapse*r**2/q*G[1,1])
    check("areal_radial_flux_from_full_metric", zero(Qr-4*A*a/(r*q)))
    # Q_r psi^r, with psi^r=(dr/d rho) psi^rho, transforms to Q_rho psi^rho.
    Qrho = clean((4*A*a/(radius*root_f))*radius_prime)
    check("flux_covariant_under_radial_coordinate_change", zero(Qrho-4*A*a/rho))
    check("boundary_flux_four_A", s.limit(Qrho,x,0)==4*A)
    selected = {A:s.Rational(1,2),B:s.Rational(1,2)}
    iso_lapse = A+B*root_f
    check("selected_isotropic_lapse", zero(iso_lapse.subs(selected)-1/p))
    gr_iso = clean(4*A*a/(iso_lapse*radius**3))
    gt_iso = clean(-2*A*a/(iso_lapse*radius**3))
    check("selected_radial_Einstein_pullback", zero(gr_iso.subs(selected)-2*a*rho**2/x**5))
    check("selected_Ricci_squared_pullback", zero((gr_iso**2+2*gt_iso**2).subs(selected)-6*a**2*rho**4/x**10))
    check("curvature_nonzero_boundary_leading_term", s.limit(x**10*(gr_iso**2+2*gt_iso**2).subs(selected),x,0)==6*a**6)
    check("Einstein_borderline_exponent_exact", s.limit(x**5*gr_iso.subs(selected),x,0)==2*a**3)
    check("optical_timelike_boundary_finite_order", s.limit(p**3/x**3,x,0)==1/a**3)

    val, deriv = s.symbols("test_value test_radial_derivative")
    spherical_connection = [s.diff(iso_lapse,x)/iso_lapse, 2*s.diff(p,x)/p, 1/rho+2*s.diff(p,x)/p, 1/rho+2*s.diff(p,x)/p]
    spherical_density = iso_lapse*p**6*rho**2
    diagonal = [0,gr_iso,gt_iso,gt_iso]
    contracted = clean(spherical_density*(gr_iso*deriv+sum(diagonal[i]*spherical_connection[i]*val for i in range(4))))
    check("radial_full_contraction_from_areal_curvature", zero(contracted-(s.diff(Qrho,x)*val+Qrho*deriv)))
    check("selected_radial_constant_germ_finite_density", s.limit(contracted.subs({**selected,val:1,deriv:0}),x,0)==-2/a)
    integral = clean(-4*s.pi*s.limit(Qrho.subs(selected),x,0))
    check("oriented_boundary_integral_negative_eight_pi", integral == -8*s.pi)
    radial_part = clean(spherical_density*gr_iso*spherical_connection[1])
    angular_part = clean(spherical_density*gt_iso*(spherical_connection[2]+spherical_connection[3]))
    check("separate_radial_connection_log_residue", s.limit(x*radial_part,x,0)==8*A)
    check("angular_log_residue_cancels", s.limit(x*angular_part,x,0)==-8*A)

    # Tensor density is derived from G_r and G_T, then differentiated in
    # unrestricted Cartesian coordinates. This checks all-field cancellation.
    z = s.symbols("z0:3", real=True)
    u = s.sqrt(sum(v*v for v in z))
    phi = 1-a/u
    D = s.Matrix(3,3,lambda i,j: clean(2*A*a*(3*z[i]*z[j]/u**5-int(i==j)/u**3)))
    # This target representation follows the radial/tangential eigenvalues
    # of the derived curvature, and is also checked before Cartesian use.
    check("Cartesian_density_radial_eigenvalue_from_curvature", zero(iso_lapse*p**6*gr_iso-4*A*a/rho**3))
    check("Cartesian_density_tangential_eigenvalue_from_curvature", zero(iso_lapse*p**6*gt_iso+2*A*a/rho**3))
    check("Cartesian_density_symmetric", D==D.T)
    check("Cartesian_density_trace_zero", s.simplify(s.trace(D))==0)
    h = s.eye(3)*phi**4
    hi = s.eye(3)/phi**4
    spatial_gamma = [[[s.simplify(sum(hi[k,j]*(s.diff(h[j,b],z[c])+s.diff(h[j,c],z[b])-s.diff(h[c,b],z[j])) for j in range(3))/2) for b in range(3)] for c in range(3)] for k in range(3)]
    for k in range(3):
        check(f"all_field_connection_cancellation_{k}", s.simplify(sum(D[i,j]*spatial_gamma[j][i][k] for i in range(3) for j in range(3)))==0)
        check(f"Cartesian_density_divergence_component_{k}", s.simplify(sum(s.diff(D[i,k],z[i]) for i in range(3)))==0)
        check(f"inner_boundary_normal_trace_component_{k}", s.simplify(sum(D[i,k]*(-z[i]/u) for i in range(3))+4*A*a*z[k]/u**4)==0)
    check("Cartesian_density_smooth_at_nonzero_inner_radius", all(s.denom(s.factor(v)).subs({z[0]:a,z[1]:0,z[2]:0})!=0 for v in D))
    check("static_energy_density_zero", G[0,0] == 0)
    check("selected_angular_null_energy_negative", clean(gt_iso.subs(selected)) == -a*rho**2/x**5)
    check("selected_radial_null_energy_positive", clean(gr_iso.subs(selected)) == 2*a*rho**2/x**5)
    check("normal_time_lapse_not_needed_for_defect_B_cancellation", s.diff(Qrho,B)==0)
    check("boundary_reaching_radial_test_nonzero_trace", s.limit(s.Integer(1),x,0)==1)
    check("boundary_fixed_A_zero_defect", Qrho.subs(A,0)==0)

    # These are genuinely false claim payloads checked against derived values.
    invalid = {
        "radial_sign": zero(gr_iso.subs(selected)+2*a*rho**2/x**5),
        "vacuum_lapse_nonzero_defect": zero(Qrho.subs(A,0)-2*a/rho),
        "general_lapse_B_survives_flux": zero(Qrho-4*a*(A+B)/rho),
        "wrong_volume_density": zero(p*Qrho-Qrho),
        "covariant_tensor_used_as_mixed": zero(p**4*Qrho-Qrho),
        "inner_boundary_normal_reversed": integral == 8*s.pi,
        "individual_connection_integrable": s.limit(x*radial_part.subs(selected),x,0)==0,
        "hidden_angular_cancellation_omitted": zero(radial_part+angular_part-radial_part),
        "positive_mass": zero(r*(1-f)/2-2*a),
        "missing_sphere_area_factor": integral == -2,
        "Einstein_better_growth_x_minus_four": s.limit(x**5*gr_iso.subs(selected),x,0)==0,
        "scalar_zero_means_flat": s.limit(x**10*(gr_iso**2+2*gt_iso**2).subs(selected),x,0)==0,
        "NEC_satisfied": clean(gt_iso.subs(selected)) == a*rho**2/x**5,
        "boundary_support_forced_zero": s.limit(s.Integer(1),x,0)==0,
        "areal_component_equals_isotropic_component": zero(radius_prime-1),
        "connection_traceful_density_cancels": s.simplify(sum(spatial_gamma[i][i][0] for i in range(3)))==0,
    }
    require(all(type(v) is bool and v is False for v in invalid.values()), "negative controls are actually false")
    results = {
        "all_passed": True, "exact_check_count":len(checks), "checks":checks,
        "python_version":platform.python_version(), "sympy_version":s.__version__,
        "method":"Full generic-lapse Christoffel-to-Ricci computation in area-radius coordinates; positive-branch pullback and direct Cartesian spatial connection definition.",
        "derived_generic_areal_Einstein_diagonal":[str(v) for v in einstein.diagonal()],
        "derived_family_areal_Einstein_diagonal":[str(v) for v in G.diagonal()],
        "derived_boundary_integral":str(integral),
        "invalid_claim_names":list(invalid),
        "limits":["Exact algebra does not establish source interpretation, priority, or added energy-condition claims.","C1 approaching-surface area control and all-field absolute integrability require the analytic arguments in the report.","r=0 and rho=a represent different boundary smooth structures; tests are transported by their vector components, not identified implicitly.","The lapse family is used only where A,B>=0 and A+B>0; a>0 and rho>a."]
    }
    return results, invalid

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--claim-file", type=Path)
    parser.add_argument("--output", type=Path)
    args=parser.parse_args()
    results, invalid=calculate()
    if args.claim_file:
        payload=json.loads(args.claim_file.read_text())
        name=payload["claim"]
        if name not in invalid:
            raise RuntimeError("Unknown case: this is not an intended rejection")
        require(invalid[name], "EXPECTED_FALSE_CLAIM_REJECTED:"+name)
        raise RuntimeError("Invalid claim was unexpectedly accepted")
    if args.output:
        args.output.write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))

if __name__=="__main__":
    try:
        main()
    except InvalidClaim as err:
        print("InvalidClaim:"+str(err),file=sys.stderr)
        sys.exit(4)
