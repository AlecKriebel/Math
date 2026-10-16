#!/usr/bin/env python3
"""Independent, portable exact controls for the regular-ZAS counterexample.

Uses proper-distance warped-product curvature, rather than the author's
coordinate Christoffel-to-Ricci implementation. Python 3 and SymPy required.
Writes audit_controls.json next to this file; no sources or network needed.
"""
import json
from pathlib import Path
import sympy as s

x, a = s.symbols('x a', positive=True)
A, B = s.symbols('A B', nonnegative=True)
rho = x+a
p = x/rho
r = x*x/rho
N = A+B*(x+2*a)/x
clean = lambda z: s.factor(s.cancel(z))
checks = {}

def verify(name, condition):
    checks[name] = bool(condition)
    if not checks[name]:
        raise AssertionError(name)

# dl = p^2 dx. For -N(l)^2 dt^2 + dl^2 + r(l)^2 dOmega^2,
# independent sectional curvature components are R0101,R0202,R1212,R2323.
ddl = lambda z: clean(s.diff(z,x)/p**2)
k01 = clean(ddl(ddl(N))/N)
k02 = clean(ddl(N)*ddl(r)/(N*r))
k12 = clean(-ddl(ddl(r))/r)
k23 = clean((1-ddl(r)**2)/r**2)
Ric = s.diag(-k01-2*k02,-k01+2*k12,-k02+k12+k23,-k02+k12+k23)
R = clean(s.trace(Ric))
G = (Ric-s.eye(4)*R/2).applyfunc(clean)
expected = s.diag(0,4*A*a/(N*rho**3*p**6),-2*A*a/(N*rho**3*p**6),-2*A*a/(N*rho**3*p**6))
verify('proper_distance_curvature_reproduces_family_Einstein_tensor',
       all(clean(G[i,j]-expected[i,j])==0 for i in range(4) for j in range(4)))
verify('family_scalar_curvature_zero',R==0)
selected={A:s.Rational(1,2),B:s.Rational(1,2)}
Gs=G.subs(selected).applyfunc(clean)
verify('selected_lapse',clean(N.subs(selected)-1/p)==0)
verify('selected_G_diagonal',list(Gs.diagonal())==[0,2*a*rho**2/x**5,-a*rho**2/x**5,-a*rho**2/x**5])
verify('selected_Ricci_squared',clean(s.trace(Gs**2)-6*a*a*rho**4/x**10)==0)
K=clean(4*(k01**2+2*k02**2+2*k12**2+k23**2))
Ks=clean(K.subs(selected))
verify('selected_Kretschmann',clean(Ks-24*a*a*rho**4*(8*a*a+12*a*x+5*x*x)/x**12)==0)
verify('invariant_curvature_blowup',s.limit(x**12*Ks,x,0,dir='+')==192*a**8)
verify('vacuum_control_all_Einstein_components_zero',all(clean(z.subs(A,0))==0 for z in G))
verify('vacuum_control_Kretschmann',clean(K.subs({A:0,B:1})-192*a*a/r**6)==0)
verify('flat_control_all_Einstein_components_zero',all(clean(z.subs(a,0))==0 for z in G))

# Geometry and causal checks.
verify('area_radius_spatial_coefficient',clean(s.diff(r,x)**2/(1+4*a/r)-p**4)==0)
verify('spatial_harmonic_resolution',clean(s.diff(p,x,2)+2*s.diff(p,x)/rho)==0)
verify('resolution_simple_positive_zero',s.limit(p,x,0)==0 and s.limit(s.diff(p,x),x,0)==1/a)
verify('regular_ZAS_mass',s.simplify(-(4*a**s.Rational(2,3))**s.Rational(3,2)/4)==-2*a)
verify('Misner_Sharp_mass_constant',clean(r*(1-ddl(r)**2)/2)==-2*a)
verify('optical_coordinate_boundary_order',s.limit(p**3/x**3,x,0)==1/a**3)
verify('null_affine_parameter_boundary_order',s.limit(p/x,x,0)==1/a)
verify('lapse_blowup_order',s.limit(x/p,x,0)==a)
verify('Einstein_borderline_nonzero_leading_coefficient',s.limit(x**5*Gs[1,1],x,0)==2*a**3)
verify('theorem_ii_prime_constant_mismatch',s.limit(s.diff(s.log(1/p),x)+1/x,x,0)==1/a)
verify('NEC_angular_null_violation',clean(Gs[2,2]+a*rho**2/x**5)==0)

# Evaluate covariant radial contraction using diagonal spherical metric
# connections, with independent symbols for a test's value and derivative.
f, fp=s.symbols('f fp')
conn=[s.diff(N,x)/N,2*s.diff(p,x)/p,1/rho+2*s.diff(p,x)/p,1/rho+2*s.diff(p,x)/p]
weight=N*p**6*rho**2
contract=clean(weight*(G[1,1]*fp+sum(G[i,i]*conn[i]*f for i in range(4))))
verify('family_radial_full_contraction',clean(contract-4*A*a*(fp/rho-f/rho**2))==0)
flux=clean(weight*G[1,1])
verify('family_boundary_flux',flux==4*A*a/rho and s.limit(flux,x,0)==4*A)
verify('selected_integral_minus_8pi',clean(-4*s.pi*s.limit(flux.subs(selected),x,0))==-8*s.pi)
verify('constant_germ_density_absolutely_integrable',s.limit(contract.subs({f:1,fp:0}),x,0)==-4*A/a)
# This confirms that convergence is for the contracted scalar, not every
# uncontracted coordinate summand separately.
parts=[clean(weight*G[i,i]*conn[i]) for i in range(4)]
verify('radial_connection_summand_has_logarithmic_divergence',s.limit(x*parts[1],x,0)==8*A)
verify('angular_connection_summands_cancel_log_divergence',s.limit(x*(parts[2]+parts[3]),x,0)==-8*A)

# Independent Cartesian tensor-density derivatives, off-axis and all indices.
z=s.symbols('z0:3',real=True)
q=sum(v*v for v in z)
u=s.sqrt(q)
D=s.Matrix(3,3,lambda i,j:2*A*a*(3*z[i]*z[j]/u**5-(1 if i==j else 0)/u**3))
verify('Cartesian_density_trace_zero',s.simplify(s.trace(D))==0)
verify('Cartesian_density_symmetric',D==D.T)
verify('Cartesian_density_divergence_all_components',
       all(s.simplify(sum(s.diff(D[i,j],z[i]) for i in range(3)))==0 for j in range(3)))
# Gamma^j_ik=2(phi_i delta^j_k+phi_k delta^j_i-phi_j delta_ik)/phi.
P=1-a/u
dP=[s.diff(P,v) for v in z]
C=[]
for k in range(3):
    C.append(s.simplify(sum(D[i,j]*2*(int(j==k)*dP[i]+int(j==i)*dP[k]-int(i==k)*dP[j])/P for i in range(3) for j in range(3))))
verify('Cartesian_full_connection_cancellation_all_components',C==[0,0,0])
normal_flux=[s.simplify(sum(D[i,j]*z[i]/u for i in range(3))-4*A*a*z[j]/u**4) for j in range(3)]
verify('Cartesian_normal_trace_all_components',normal_flux==[0,0,0])

# Negative controls must reject two tempting false claims.
verify('negative_control_wrong_radial_sign_rejected',clean(contract.subs({A:s.Rational(1,2),f:1,fp:0})-2*a/rho**2)!=0)
verify('negative_control_nonzero_defect_for_vacuum_rejected',clean(flux.subs(A,0)-2*a/rho)!=0)
verify('negative_control_traceful_connection_does_not_cancel',clean(6*s.diff(p,x)/p)!=0)

result={
    'all_passed':all(checks.values()),
    'assertions_passed':len(checks),
    'sympy_version':s.__version__,
    'checks':checks,
    'exact_results':{
        'selected_G_mixed_diagonal':[str(v) for v in Gs.diagonal()],
        'selected_Kretschmann':str(Ks),
        'family_radial_contracted_density_without_eta_dOmega':str(contract),
        'selected_test_integral':'-8*pi',
        'family_boundary_functional':'-(4*A/a^2) integral_{R x S_a} (psi dot n) dt dA_delta',
        'selected_null_affine_parameter':'lambda-lambda_0=(rho-a-a*log(rho/a))/E',
        'negative_controls_rejected':3,
    },
    'limits':'Exact algebra supports but does not replace source and geometric admissibility review.'
}
Path(__file__).with_name('audit_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
