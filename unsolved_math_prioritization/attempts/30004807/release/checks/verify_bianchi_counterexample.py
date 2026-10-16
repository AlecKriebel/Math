#!/usr/bin/env python3
"""Exact checks from the coordinate metric, independent of the manuscript formulas."""
import json
from pathlib import Path
import sympy as s

rho, a = s.symbols('rho a', positive=True)
t, theta, azimuth = s.symbols('t theta azimuth', real=True)
coords = [t, rho, theta, azimuth]
phi = 1-a/rho
N = 1/phi
metric = s.diag(-N**2, phi**4, phi**4*rho**2, phi**4*rho**2*s.sin(theta)**2)
inv = s.diag(*[1/metric[i,i] for i in range(4)])
clean = lambda x: s.factor(s.trigsimp(s.cancel(x)))
Gamma = [[[clean(sum(inv[k,l]*(s.diff(metric[l,j],coords[i])+s.diff(metric[l,i],coords[j])-s.diff(metric[i,j],coords[l])) for l in range(4))/2) for j in range(4)] for i in range(4)] for k in range(4)]
Ric = s.zeros(4)
for i in range(4):
    for j in range(4):
        Ric[i,j] = clean(sum(s.diff(Gamma[k][i][j],coords[k])-s.diff(Gamma[k][i][k],coords[j])+sum(Gamma[k][i][j]*Gamma[l][k][l]-Gamma[l][i][k]*Gamma[k][j][l] for l in range(4)) for k in range(4)))
R = clean(s.trace(inv*Ric))
G = s.simplify(inv*Ric - s.eye(4)*R/2)
expected = s.diag(0, 2*a/(rho**3*phi**5), -a/(rho**3*phi**5), -a/(rho**3*phi**5))
checks = {}
checks['direct_4d_Einstein_all_16_components'] = all(clean(G[i,j]-expected[i,j])==0 for i in range(4) for j in range(4))
checks['scalar_curvature_zero'] = R == 0
w = N*phi**6*rho**2
Q = clean(w*G[1,1])
checks['radial_flux_density'] = clean(Q-2*a/rho)==0
checks['radial_flux_boundary_is_two'] = s.limit(Q,rho,a,dir='+')==2
checks['Ricci_squared_curvature_blowup'] = clean(s.trace((inv*Ric)**2)-6*a**2/(rho**6*phi**10))==0
# Check the full covariant contraction for radial psi=chi(rho)*eta(t).
chi = s.Function('chi')(rho)
radial_contraction = clean(w*(G[1,1]*s.diff(chi,rho)+sum(G[i,i]*Gamma[i][i][1] for i in range(4))*chi))
checks['full_radial_contraction_is_flux_derivative'] = clean(radial_contraction-s.diff(Q*chi,rho))==0
# Use a polynomial local germ chi=1 and an exact outer truncation identity;
# smooth bump existence, rather than this polynomial, is used in the proof.
checks['constant_radial_germ_density'] = clean(radial_contraction.subs({s.diff(chi,rho):0,chi:1})+2*a/rho**2)==0
# General lapse flux, from the metric's spherical formula for G^rho_rho.
A, B = s.symbols('A B', nonnegative=True)
Nv = (rho+a)/(rho-a)
Ng = A+B*Nv
Qgeneral = clean(2*(rho*rho-a*a)/rho*s.diff(Ng,rho)+4*a/rho*Ng)
checks['lapse_family_flux_exact'] = clean(Qgeneral-4*a*A/rho)==0
checks['vacuum_lapse_flux_zero'] = clean(Qgeneral.subs(A,0))==0
checks['ultrastatic_flux_nonzero'] = s.limit(Qgeneral.subs({A:1,B:0}),rho,a,dir='+')==4
# Direct conformal Ricci and Hessian identity for the family.
q = s.diff(phi,rho)/phi
Ric_h_cov = s.diag(4*a/(rho**3*phi**2),-2*a/(rho*phi**2),-2*a*s.sin(theta)**2/(rho*phi**2))
HessNv = s.diag(s.diff(Nv,rho,2)-2*q*s.diff(Nv,rho), (rho+2*rho*rho*q)*s.diff(Nv,rho), s.sin(theta)**2*(rho+2*rho*rho*q)*s.diff(Nv,rho))
checks['static_vacuum_hessian_identity'] = all(clean(HessNv[i,j]-Nv*Ric_h_cov[i,j])==0 for i in range(3) for j in range(3))
checks['static_vacuum_harmonic_lapse'] = clean(HessNv[0,0]/phi**4+HessNv[1,1]/(phi**4*rho*rho)+HessNv[2,2]/(phi**4*rho*rho*s.sin(theta)**2))==0
# Independent area-radius metric calculation for the ultrastatic end.
r = rho*phi**2
checks['area_radius_coordinate'] = clean(s.diff(r,rho)**2/(1+4*a/r)-phi**4)==0
checks['ZAS_mass_minus_two_a'] = s.simplify(-(4*a**s.Rational(2,3))**s.Rational(3,2)/4+2*a)==0
# In Cartesian rho-coordinates the density is smooth and divergence-free.
Ar, At = 2*a/rho**3, -a/rho**3
checks['Cartesian_density_divergence_zero'] = clean(s.diff(Ar,rho)+2*(Ar-At)/rho)==0
checks['contracted_connection_trace_zero'] = clean(Ar+2*At)==0
# Negative control: replacing the time lapse by the vacuum one must cancel G.
checks['negative_control_vacuum_parameter_A_zero'] = clean(Qgeneral.subs({A:0,B:1}))==0
result = {
    'sympy_version': s.__version__,
    'metric': '-(1-a/rho)^(-2) dt^2 + (1-a/rho)^4 (d rho^2 + rho^2 d Omega^2)',
    'checks': checks,
    'all_passed': all(checks.values()),
    'exact_values': {'G_mixed_diagonal': [str(clean(G[i,i])) for i in range(4)], 'R': str(R), 'Q': str(Q), 'weak_test_value_eta_integral_one': '-8*pi'},
    'scope': 'Symbolic validation only; the analytic proof supplies geometry, test class, convergence, and theorem scope.'
}
path = Path(__file__).with_name('verification_results.json')
path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert result['all_passed']
