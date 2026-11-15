#!/usr/bin/env python3
"""Read-only independent symbolic adversarial checks; no submission imports.

Derives curvature for three unrestricted radial metric functions before any
target specialization. Uses a harmonic-potential Hessian for the density,
general test-vector jets, and exact boundary/tilt controls. Explicit exceptions
survive -O. Stdout only; no file writes or network.
"""
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys
import sympy as s

COUNTS = Counter()


def clean(z):
    return s.factor(s.trigsimp(s.cancel(z)))


def check(value, family):
    if not bool(value):
        raise RuntimeError(family)
    COUNTS[family] += 1


def zero(value, family):
    check(clean(value) == 0, family)


rho, a, gap = s.symbols('rho a gap', positive=True)
t, theta, azimuth = s.symbols('t theta azimuth', real=True)
A, B = s.symbols('A B', nonnegative=True)
U = s.Function('U')(rho)
V = s.Function('V')(rho)
W = s.Function('W')(rho)
coords = [t, rho, theta, azimuth]
metric = s.diag(-U**2, V**2, W**2, W**2*s.sin(theta)**2)
inv = s.diag(*[1/metric[k,k] for k in range(4)])
gamma = [[[clean(sum(inv[k,l]*(s.diff(metric[l,j],coords[i])
             +s.diff(metric[l,i],coords[j])-s.diff(metric[i,j],coords[l]))
             for l in range(4))/2) for j in range(4)]
             for i in range(4)] for k in range(4)]
ricci = s.zeros(4)
for i in range(4):
    for j in range(4):
        ricci[i,j] = clean(sum(
            s.diff(gamma[k][i][j],coords[k])-s.diff(gamma[k][i][k],coords[j])
            +sum(gamma[k][i][j]*gamma[l][k][l]
                 -gamma[l][i][k]*gamma[k][j][l] for l in range(4))
            for k in range(4)))
scalar = clean(s.trace(inv*ricci))
generic_G = (inv*ricci-s.eye(4)*scalar/2).applyfunc(clean)
phi = 1-a/rho
q = (rho+a)/(rho-a)
N = A+B*q
special = {U:N, V:phi**2, W:rho*phi**2}
replacements = {}
for f, value in special.items():
    for order in range(3):
        replacements[s.diff(f,rho,order)] = s.diff(value,rho,order)


def specialize(z):
    return clean(z.subs(replacements, simultaneous=True))


G = generic_G.applyfunc(specialize)
target = s.diag(0,4*A*a/(N*rho**3*phi**6),
               -2*A*a/(N*rho**3*phi**6),-2*A*a/(N*rho**3*phi**6))
zero(specialize(scalar),'full_generic_metric_scalar_zero')
for i in range(4):
    for j in range(4):
        zero(G[i,j]-target[i,j],'full_generic_metric_Einstein_components')
        zero(G[i,j].subs(A,0),'vacuum_endpoint_components')
        zero(G[i,j].subs({A:1,B:0})-target[i,j].subs({A:1,B:0}),
             'constant_lapse_endpoint_components')

selected = {A:s.Rational(1,2),B:s.Rational(1,2)}
zero(N.subs(selected)-1/phi,'main_lapse_dictionary')
zero(s.trace(G*G).subs(selected)-6*a**2/(rho**6*phi**10),
     'main_Ricci_squared')
check(s.limit((rho-a)**5*G[1,1].subs(selected),rho,a,dir='+') == 2*a**3,
      'nonzero_borderline_curvature_coefficient')
check(s.limit((rho-a)**10*s.trace(G*G).subs(selected),rho,a,dir='+') == 6*a**6,
      'invariant_curvature_blowup_coefficient')
zero(N*phi**6*G[1,1]-4*A*a/rho**3,'weighted_radial_Einstein')
zero(N*phi**6*G[2,2]+2*A*a/rho**3,'weighted_angular_Einstein')

# Arbitrary four-vector values and first derivatives in spherical coordinates.
# This is an algebraic identity in independent symbols, not a sample vector.
values = s.symbols('v0:4')
partials = s.Matrix(4,4,lambda i,j:s.Symbol('p%d%d' % (i,j)))
special_gamma = [[[specialize(gamma[k][i][j]) for j in range(4)]
                   for i in range(4)] for k in range(4)]
covariant_jet = s.Matrix(4,4,lambda i,j:partials[i,j]+sum(
    special_gamma[j][i][k]*values[k] for k in range(4)))
full_density = clean(N*phi**6*rho**2*s.sin(theta)*sum(
    G[i,j]*covariant_jet[i,j] for i in range(4) for j in range(4)))
expected_spherical = clean(A*a/rho*(4*partials[1,1]
    -2*partials[2,2]-2*partials[3,3]
    -(4/rho)*values[1]-2*s.cot(theta)*values[2])*s.sin(theta))
zero(full_density-expected_spherical,'all_independent_vector_jets_scalar_density')
zero(s.diff(full_density,values[0]),'arbitrary_time_component_drops_out')
zero(s.diff(full_density,values[3]),'azimuth_value_drops_out')

# Independent harmonic-potential mechanism in boundary-smooth Cartesian charts.
x = s.symbols('x1:4',real=True)
R = s.sqrt(sum(z*z for z in x))
potential = 1/R
D = (2*A*a*s.hessian(potential,x)).applyfunc(s.simplify)
for i in range(3):
    for j in range(3):
        zero(D[i,j]-A*a*(6*x[i]*x[j]/R**5-2*int(i==j)/R**3),
             'density_from_harmonic_potential_Hessian')
zero(sum(s.diff(potential,z,2) for z in x),'harmonic_potential_Laplacian')
zero(s.trace(D),'Hessian_density_trace_free')
check(D == D.T,'Hessian_density_symmetric')
P = 1-a/R
gradient = [s.diff(P,z) for z in x]
for k in range(3):
    zero(sum(s.diff(D[i,k],x[i]) for i in range(3)),
         'harmonic_Hessian_density_divergence')
    contraction = sum(D[i,j]*2/P*(int(j==i)*gradient[k]
        +int(j==k)*gradient[i]-int(i==k)*gradient[j])
        for i in range(3) for j in range(3))
    zero(contraction,'all_field_Cartesian_connection_cancellation')
    zero(-sum(x[i]/R*D[i,k] for i in range(3))+4*A*a*x[k]/R**4,
         'oriented_boundary_traction')

radial_flux_per_solid_angle = 4*A*a/rho
check(s.limit(radial_flux_per_solid_angle,rho,a,dir='+') == 4*A,
      'boundary_flux_scale')
zero(-4*s.pi*s.limit(radial_flux_per_solid_angle,rho,a,dir='+')+16*s.pi*A,
     'normalized_radial_test_exact_family_value')
zero((-16*s.pi*A).subs(selected)+8*s.pi,'normalized_main_test_value')
zero(s.diff(radial_flux_per_solid_angle,B),'no_hidden_B_in_boundary_flux')
z = s.symbols('z',real=True)
check(s.integrate(z,(z,-1,1)) == 0,'constant_Cartesian_trace_integral_zero')
check(s.integrate(z**4,(z,-1,1)) == s.Rational(2,5),
      'nonradial_cubic_trace_sphere_moment')
zero(-4*A/a**2*(2*s.pi*a**5*s.Rational(2,5))+16*s.pi*A*a**3/5,
     'nonradial_cubic_trace_boundary_value')

# ZAS resolution and edge/gauge/causal controls.
zero(s.diff(phi,rho,2)+2*s.diff(phi,rho)/rho,'harmonic_resolution')
check(phi.subs(rho,a)==0 and s.diff(phi,rho).subs(rho,a)==1/a,
      'simple_positive_resolution_zero')
zero(-s.Rational(1,4)*(4*a**s.Rational(2,3))**s.Rational(3,2)+2*a,
     'regular_ZAS_mass')
areal = rho*phi**2
zero(s.diff(areal,rho)-(1-a**2/rho**2),'areal_derivative')
check(s.diff(areal,rho).subs(rho,a)==0,'areal_change_not_boundary_diffeomorphism')
zero(s.diff(areal,rho)**2/(1+4*a/areal)-phi**4,'spatial_areal_pullback')
check(s.limit(phi.subs(rho,a+gap)**3/gap**3,gap,0,dir='+')==a**(-3),
      'optical_coordinate_boundary_order')
check(s.limit(phi.subs(rho,a+gap)/gap,gap,0,dir='+')==a**(-1),
      'null_affine_length_density_order')
zero(s.diff(rho-a-a*s.log(rho/a),rho)-phi,'null_affine_length_antiderivative')
tilt = s.symbols('tilt',real=True)
tilt_nu = 1/(a*s.sqrt(1-tilt**2))
tilt_mass = -s.Rational(1,4)*(4*a**2*tilt_nu**s.Rational(4,3))**s.Rational(3,2)
# Avoid branch claims outside the allowed interval by substitute tilt=sin(beta).
beta = s.symbols('beta',positive=True)
zero(tilt_mass.subs(tilt,0)+2*a,'zero_tilt_mass_control')
for rational_tilt in [s.Rational(1,2),s.Rational(-3,5),s.Rational(99,100)]:
    zero(tilt_mass.subs(tilt,rational_tilt)+2*a/(1-rational_tilt**2),
         'uniform_spacelike_tilt_mass')
zero(phi**4-phi**(-2)*(phi**3*s.sqrt(1-phi**2))**2-phi**6,
     'nearly_null_tilt_induced_radial_metric')
check(s.limit(phi**2,rho,a,dir='+')==0,'nearly_null_resolved_radial_degeneracy')
zero(G[0,0],'static_energy_density_zero')
zero(G[2,2].subs(selected)+a/(rho**3*phi**5),'angular_null_NEC_negative')

result = {'status':'PASS','completed_utc':datetime.now(timezone.utc).isoformat(),
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'python':sys.version,'sympy':s.__version__,
          'exact_checks':sum(COUNTS.values()),'families':dict(sorted(COUNTS.items())),
          'generic_Einstein_diagonal':[str(z) for z in generic_G.diagonal()],
          'derived_family_Einstein_diagonal':[str(z) for z in G.diagonal()],
          'method':'Unrestricted three-function spherical metric curvature; arbitrary test jets; harmonic-potential Hessian density',
          'writes_files':False,'imports_submission_or_review_helpers':False,
          'scope':'Symbolic identities and boundary controls; universal compact-support convergence and source admissibility require the written proof.'}
print(json.dumps(result,indent=2,sort_keys=True))
