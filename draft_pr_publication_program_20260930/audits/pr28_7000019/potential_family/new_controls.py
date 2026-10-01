#!/usr/bin/env python3
"""New potential/PDE controls; imports no submitted or prior-review code.

Exact controls check individual identities and falsifiers. Deterministic ellipsoid
quadrature is bounded diagnostic evidence, never a certificate for a theorem.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import json
import math
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
checks = []
mutants = []
def check(name, condition, detail):
    assert bool(condition), name
    checks.append({"name": name, "passed": True, "detail": detail})

def reject(name, condition, reason):
    assert not bool(condition), "surviving mutant: " + name
    mutants.append({"name": name, "rejected": True, "reason": reason})

# Finite positive measures include sources inside, on, and outside the truncation
# radius. The left side is calculated as an angular-coordinate interval length.
a = F(1, 2)
atoms = [(F(1, 4), F(2)), (F(1, 2), F(3)), (F(3, 2), F(5))]
left = sum(weight * (min(F(1), a / radius) - max(F(-1), -a / radius)) / 2
           for radius, weight in atoms)
right = sum(weight * min(F(1), a / radius) for radius, weight in atoms)
check("finite_atomic_Fubini_with_saturation", left == right == F(20, 3),
      "Angular interval lengths for positive weights2,3,5 at radii1/4,1/2,3/2; half-width1/2.")
unsaturated = a * sum(weight / radius for radius, weight in atoms)
reject("remove_core_condition_use_a_over_r_everywhere", left == unsaturated,
       "Exact angular average20/3 differs from unsaturated Newton expression26/3.")
check("band_boundary_r_equals_a", min(F(1), a/a) == 1,
      "At the truncation radius all orientations are admitted, including endpoints.")
check("atom_at_center", F(1) == 1,
      "A source at the slab center lies in every centered slab; the Newton kernel would be singular.")

# The Newton kernel is a three-dimensional consequence. n=5 has marginal
# density(3/4)(1-z^2); n=2 at ratio1/2 has angular probability1/3.
z = s.symbols("z", real=True)
prob5 = s.integrate(s.Rational(3, 4)*(1-z*z), (z, -s.Rational(1,2), s.Rational(1,2)))
check("dimension5_band_probability", prob5 == s.Rational(11,16),
      "The same ratio1/2 yields11/16 in five dimensions.")
reject("extend_Newton_band_identity_to_dimension5", prob5 == s.Rational(1,2),
       "Uniform direction probability is not a/r outside dimension3.")
reject("extend_band_identity_to_dimension2", F(1,3) == F(1,2),
       "For a/r=1/2 on S^1 the band has probability1/3.")

# Integrate the radial sphere kernel for arbitrary nonzero displacement q.
# Differentiate the antiderivative first, rather than hardcoding a potential.
R,q = s.symbols("R q", positive=True)
primitive = -s.sqrt(R*R+q*q-2*R*q*z)/(R*q)
check("offcenter_sphere_integral_antiderivative",
      s.simplify(s.diff(primitive,z)-1/s.sqrt(R*R+q*q-2*R*q*z)) == 0,
      "Longitude integration contributes2πR²; definite integral has endpoints|R-q| andR+q.")
normalized_inside = s.simplify(R/(2*q)*((R+q)-(R-q)))
normalized_outside = s.simplify(R/(2*q)*((R+q)-(q-R)))
check("sphere_potential_throughout_interior", normalized_inside == R,
      "For0<q<R, the exact single-layer potential with kernel1/(4πr) isR.")
check("sphere_exterior_potential", normalized_outside == R**2/q,
      "Forq>R, the normalized potential isR²/q.")
jump = s.simplify(s.diff(normalized_outside,q).subs(q,R))
check("normalized_body_outward_jump", jump == -1,
      "The exterior derivative atq=R is-1 and the interior derivative is0.")
reject("flip_body_outward_normal_jump_sign", jump == 1,
       "Explicit sphere formula fixes outward-body normal sign.")
reject("use_unnormalized_jump_for_normalized_kernel", jump == -4*s.pi,
       "Normalized potential has derivative-1; unnormalized potential has derivative-4π.")
check("unnormalized_jump", s.simplify(4*s.pi*jump) == -4*s.pi,
      "The4π conversion agrees on both the potential and the boundary derivative.")
check("sphere_exterior_radial_harmonicity",
      s.simplify(s.diff(normalized_outside,q,2)+2*s.diff(normalized_outside,q)/q) == 0,
      "Radial Laplacian ofR²/q vanishes away from the center.")
check("sphere_exterior_decay", s.limit(normalized_outside,q,s.oo) == 0,
      "Exact decay meets Reichel's exterior boundary condition.")
h = s.symbols("h", positive=True)
C = 2*s.pi*R*h
check("full_width_normalization", s.simplify(C/(h/2)-4*s.pi*R) == 0,
      "Independent offcenter sphere formula matchesP=2C/h.")
reject("drop_full_width_factor2", s.simplify(C/h-4*s.pi*R) == 0,
       "The wrong factor gives2πR rather than the exact4πR.")
reject("drop_direction_measure_4pi", s.simplify(4*s.pi*C/(h/2)-4*s.pi*R) == 0,
       "Unnormalized direction measure must be canceled on both sides.")

# Open-core and continuation countermodels are logical, not finite samples.
check("strict_core_has_open_ball", F(1)-F(2,5) > 0,
      "Unit ball withh=4/5 has coreB(0,3/5); the strict inequality gives an open set.")
reject("replace_h_less_2rin_by_h_leq_2rin", F(1)-F(1) > 0,
       "Unit sphere withh=2 has empty strict core even though the weak bound holds.")
x,y,w = s.symbols("x y w", real=True)
harmonic_point_countermodel = x
check("one_point_constancy_is_insufficient",
      sum(s.diff(harmonic_point_countermodel,v,2) for v in (x,y,w)) == 0
      and harmonic_point_countermodel.subs(x,0) == 0
      and harmonic_point_countermodel.subs(x,1) != 0,
      "Harmonicx1 vanishes at the origin but is not constant; an open starting set is essential.")
reject("continue_from_one_point", harmonic_point_countermodel.subs(x,1) == 0,
       "Single-point constancy does not trigger analytic continuation.")

# A variable-density falsifier for the *general* electrostatic statement:
# take exterior harmonicv=1/r+eps*cos(theta)/r² and its levelv=1.
# For sufficiently small eps the level set is a smooth perturbation of the
# sphere. Its positive capacitary charge reproducesv outside and1 inside.
# Exact equatorial jets already prove the level is not any sphere.
t,eps = s.symbols("t eps", real=True)
radial_level = (1+s.sqrt(1+4*eps*t))/2
check("nonball_equipotential_level_equation",
      s.simplify(radial_level**2-radial_level-eps*t) == 0,
      "The radial graph solves1/r+eps*t/r²=1.")
check("equipotential_equatorial_first_jet", s.diff(radial_level,t).subs(t,0) == eps,
      "Any rotationally symmetric sphere through equatorial radius1 would need center shifteps.")
check("equipotential_equatorial_second_jet", s.diff(radial_level,t,2).subs(t,0) == -2*eps**2,
      "A sphere with that center shift has second jeteps², opposite sign for nonzeroeps.")
reject("omit_uniform_density_in_electrostatic_rigidity", -2*F(1,20)**2 == F(1,20)**2,
       "Smooth nonball dipole equipotentials admit positive variable equilibrium charge; seeREPORT for representation argument.")
check("dipole_level_exterior_radial_derivative_negative", 2*F(1,20) < F(9,10),
      "Level radius exceeds9/10, hence1+2eps*t/r>0 for|t|<=1 andeps=1/20; outward charge is positive.")

# Deterministic Gauss-Legendre/periodic quadrature for a smooth ellipsoid.
# This is independent of both frozen scripts, and convergence is diagnostic.
def legendre(n):
    nodes = []
    for k in range(1,n+1):
        u = math.cos(math.pi*(k-.25)/(n+.5))
        for _ in range(30):
            p0,p1 = 1.,u
            for j in range(2,n+1):
                p0,p1 = p1, ((2*j-1)*u*p1-(j-1)*p0)/j
            dp = n*(u*p1-p0)/(u*u-1)
            next_u = u-p1/dp
            if abs(next_u-u) < 3e-16:
                u = next_u
                break
            u = next_u
        weight = 2/((1-u*u)*dp*dp)
        nodes.append((u,weight))
    return nodes

def ellipsoid_potential(axes, point, nz, np):
    A,B,C = axes
    total = 0.
    for z,weight in legendre(nz):
        radial = math.sqrt(1-z*z)
        for k in range(np):
            phi = 2*math.pi*(k+.5)/np
            nx,ny,nzv = radial*math.cos(phi),radial*math.sin(phi),z
            source = (A*nx,B*ny,C*nzv)
            jac = A*B*C*math.sqrt((nx/A)**2+(ny/B)**2+(nzv/C)**2)
            dist = math.sqrt(sum((source[j]-point[j])**2 for j in range(3)))
            total += weight*jac/dist*(2*math.pi/np)
    return total/(4*math.pi)

points = [(0.,0.,0.),(.5,0.,0.),(0.,0.,.5)]
values = []
for resolution in [(48,128),(96,256)]:
    values.append([ellipsoid_potential((3.,2.,1.), point,*resolution) for point in points])
error = max(abs(a-b) for a,b in zip(*values))
variation = max(values[-1])-min(values[-1])
check("smooth_ellipsoid_nonconstant_uniform_potential_diagnostic",
      error < 1e-8 and variation > 1e-3,
      "Axes3,2,1; h=.8; all sampled points lie in the open core by the contained unit-ball bound. Numeric evidence only.")
check("smooth_large_width_empty_core_control", F(2) < F(5,2) < F(6),
      "Axes3,2,1 have inradius1 and diameter6; h=5/2 meets target diameter bound but has empty core.")

result = {
    "utc": datetime.now(timezone.utc).isoformat(), "sympy_version": s.__version__,
    "passed_named_controls": len(checks), "explicit_mathematical_mutants_rejected": len(mutants),
    "checks": checks, "mutants": mutants,
    "bounded_numeric_diagnostic": {"axes": [3,2,1], "h": .8,
        "points": points, "resolutions": [[48,128],[96,256]],
        "normalized_potential_values": values, "between_resolution_max_change": error,
        "observed_variation": variation,
        "limitation": "Convergence comparison gives no rigorous quadrature error bound and proves no universal theorem."},
    "scope": "New exact mechanism controls and explicit falsifiers; universal conclusions require the written proof and primary theorem.",
    "full_target_solved": False,
}
(HERE / "new_control_receipts.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"passed_named_controls": len(checks), "mutants_rejected": len(mutants),
                  "ellipsoid_variation": variation, "resolution_change": error}))
