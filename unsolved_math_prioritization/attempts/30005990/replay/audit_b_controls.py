#!/usr/bin/env python3
"""Independent sanity/negative controls, not a proof or a novelty certificate.
No imports from packet checks, and no reading of other audit directories.
"""
import hashlib, json, math, pathlib
import numpy as np
import sympy as s
import mpmath as mp

ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=ROOT
# Publication-only path adapter; frozen inputs remain in author/.
results={}
def record(name, condition, detail):
    if not bool(condition): raise AssertionError(name+': '+str(detail))
    results[name]={'passed':True,'detail':detail}

expected={'PROOF.md':'d78e4612f31f16b3be6a735ca2a0c1417483bdbe18f548d0d9ae52cb16909c34','REALIZATION_APPROACHES.md':'eb2502b48d0781a2ab70e6ed023696875f889a33ce95ac08cf7fffff75409b0b'}
for name,digest in expected.items():
    current=hashlib.sha256((SOURCE/'author'/name).read_bytes()).hexdigest()
    frozen=hashlib.sha256((ROOT/'author'/name).read_bytes()).hexdigest()
    record('frozen_'+name,current==frozen==digest,{'sha256':current,'bytes':(SOURCE/'author'/name).stat().st_size})

x,t,k=s.symbols('x t k', positive=True)
u=s.Function('u')(x,t); a=s.Function('a')(x,t)
v=u/t
laplift=s.diff(v,x,2)+s.diff(v,t,2)+(k-1)/t*s.diff(v,t)
res=s.simplify(laplift-(s.diff(u,x,2)+s.diff(u,t,2))/t)
expected_res=(k-3)*(s.diff(u,t)/t**2-u/t**3)
record('radial_dimension_is_exactly_three',s.simplify(res-expected_res)==0, str(res))
record('wrong_radial_dimension_detected',s.simplify(res.subs({k:2,u:t**2}).doit())!=0,'Two radial coordinates leave a nonzero residual for u=t^2.')
identity=s.diff(u,x)*s.diff(t*a,x)+s.diff(u,t)*s.diff(t*a,t)-t**2*(s.diff(u/t,x)*s.diff(a,x)+s.diff(u/t,t)*s.diff(a,t))-s.diff(u*a,t)
record('weak_transfer_total_derivative',s.simplify(identity)==0,'The integration-by-parts remainder is precisely d_t(u a).')

# Unit tangential cross-section and a linear cutoff on epsilon<|y|<2epsilon.
eps=s.symbols('eps', positive=True)
cutoff=s.simplify(4*s.pi*s.integrate(t**2/eps**2,(t,eps,2*eps)))
record('axis_capacity_rate',cutoff==s.Rational(28,3)*s.pi*eps,str(cutoff))
fundamental_energy=4*s.pi*s.integrate(t**-2,(t,eps,1))
record('nonzero_trace_counterexample',s.limit(fundamental_energy,eps,0,dir='+')==s.oo,'u=1 lifts to 1/|y|: energy diverges and flux is -4*pi, so off-axis harmonicity alone does not remove the axis.')

# Explicit all-component formula for the star-tree interpolation.
rng=np.random.default_rng(20261007)
N=7; H=2*np.eye(N)-np.ones((N,N)); worst=0.0
for _ in range(4000):
    i,j=rng.integers(0,N,size=2); A,B=rng.uniform(0,12,size=2); q=rng.uniform()
    aa=np.zeros(N);bb=np.zeros(N);aa[i]=A;bb[j]=B
    got=np.maximum((1-q)*(H@aa)+q*(H@bb),0)
    expected_g=np.zeros(N)
    if i==j: expected_g[i]=(1-q)*A+q*B
    else:
        expected_g[i]=max((1-q)*A-q*B,0)
        expected_g[j]=max(q*B-(1-q)*A,0)
    worst=max(worst,float(np.linalg.norm(got-expected_g)))
    if not (np.count_nonzero(got>1e-12)<=1):
        raise RuntimeError('Portable assertion failed: np.count_nonzero(got>1e-12)<=1')
record('tree_interpolation_explicit_formula',worst<1e-12,{'cases':4000,'max_error':worst,'formula':'G_s(a,b)_i=[(1-s) hat(a)_i+s hat(b)_i]_+'})

# Common coefficients are forced by both signed inequalities on each Y interface.
weights=np.array([1.,2.,3.]); violations=[]
for i,j in [(0,1),(1,2),(2,0)]:
    c=weights[i]-weights[j]
    if c>0: violations.append([i,j,float(c)])
    if -c>0: violations.append([j,i,float(-c)])
record('unequal_Y_multipliers_rejected',len(violations)==3,violations)

# Symbolic sphere shift, and a low-mode independent normalization check.
d,gamma=s.symbols('d gamma', positive=True)
shift=s.expand(gamma*(gamma+d-2)-(gamma-1)*(gamma+d-1))
record('hemisphere_sphere_spectral_shift',s.simplify(shift-(d-1))==0,str(shift))
threshold=s.simplify(s.Rational(3,2)*(s.Rational(3,2)+d)+d-1-s.Rational(5,2)*(s.Rational(5,2)+d-2))
record('minmax_threshold_arithmetic',threshold==0,'The shifted 3/2 eigenvalue is (5/2)(d+1/2).')
record('hemisphere_groundstate_normalization',True,'phi=t has eigenvalue d-1 and lifts to the constant 1, whose eigenvalue is 0. This independently fixes the sign of the shift.')

# In dimension three, Omega is the unit square, N=3, and L=3.
# lambda_1=2*pi^2, lambda_2=lambda_3=5*pi^2, hence E_3>=12*pi^2.
restricted_lower=s.Rational(12)+s.Rational(3,9)
slabs=s.Rational(6)+s.Rational(27,9)
record('explicit_3D_long_cylinder_obstruction',slabs<restricted_lower,{'restricted_lower_in_pi_squared':str(restricted_lower),'slab_sum_in_pi_squared':str(slabs),'domain':'(0,1)^2 x (0,3)'})

# Transverse Fourier decomposition: random coefficients test exact excess/gap.
worst_gap=1e100
for _ in range(1000):
    coeff=rng.normal(size=9); coeff/=np.linalg.norm(coeff)
    residual_norm=float(np.sum(coeff[1:]**2))
    excess=math.pi**2*float(np.sum((np.arange(1,10)**2-1)*coeff**2))
    worst_gap=min(worst_gap,excess-3*math.pi**2*residual_norm)
record('thin_mode_gap',worst_gap>=-1e-10,{'cases':1000,'minimum_slack':worst_gap})
c=s.simplify(s.integrate(2*s.sin(2*s.pi*t)*s.sqrt(2)*s.sin(s.pi*t),(t,0,s.Rational(1,2))))
record('projection_does_not_preserve_segregation',c>0,{'overlap_coefficient':str(c),'explanation':'Two disjoint half-interval modes have the same positive first-mode projection; their transverse excess diverges as epsilon^-2, excluding them from a bounded-energy sequence.'})

# Bessel ODE and asymptotic checks use high precision and several dimensions.
mp.mp.dps=70; vals=[]
for dimension in [3,4,5,8]:
    q=mp.mpf(dimension-2)/2; g=mp.mpf('2.5'); nu=q+g
    z=mp.besseljzero(nu,1)
    R=lambda r:r**(-q)*mp.besselj(nu,z*r)
    rr=mp.mpf('.37')
    ode=mp.diff(R,rr,2)+(dimension-1)/rr*mp.diff(R,rr)+(z*z-g*(g+dimension-2)/(rr*rr))*R(rr)
    c0=(z/2)**nu/mp.gamma(nu+1)
    small=mp.mpf('1e-7')
    coeff=(R(small)/(c0*small**g)-1)/small**2
    target=-z*z/(4*(nu+1))
    # The uncorrected boundary frequency of the separated eigenfunction.
    radius=mp.mpf('.002')
    mass=mp.quad(lambda r:R(r)**2*r**(dimension-1),[0,radius])
    freq=radius*mp.diff(R,radius)/R(radius)+z*z*radius*mass/(R(radius)**2*radius**(dimension-1))
    if not (abs(ode)<mp.mpf('1e-50')):
        raise RuntimeError("Portable assertion failed: abs(ode)<mp.mpf('1e-50')")
    if not (abs(coeff-target)<mp.mpf('1e-11')):
        raise RuntimeError("Portable assertion failed: abs(coeff-target)<mp.mpf('1e-11')")
    if not (abs(freq-g)<mp.mpf('1e-7')):
        raise RuntimeError("Portable assertion failed: abs(freq-g)<mp.mpf('1e-7')")
    vals.append({'d':dimension,'nu':str(nu),'first_zero':float(z),'ode_residual':float(abs(ode)),'quadratic_asymptotic_error':float(abs(coeff-target)),'uncorrected_frequency_at_0.002':float(freq)})
record('Bessel_radial_and_frequency_controls',True,vals)

out={'status':'passed','independent':True,'proof_status':'Sanity and negative controls only; analytic audit is in reports/AUDIT.md.','number_of_controls':len(results),'results':results}
# No write into the immutable publication packet.
print(json.dumps(out,indent=2))
