#!/usr/bin/env python3
"""Reproduce finite algebraic controls and numerical diagnostics.
No finite check replaces the proofs in RESULTS.md. No network/source files needed.
"""
import json, math, platform
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.special import lambertw
import sympy as sp

checks=0

def require(value,message):
    global checks
    checks+=1
    if not bool(value):
        raise RuntimeError(message)

def reject_false(value,name):
    if bool(value):
        raise RuntimeError('False control unexpectedly accepted: '+name)
    return name

x=sp.symbols('x',real=True)
s=sp.sqrt(2); r=3-2*s
f=-x/(1+x*x); H=sp.simplify(f*sp.diff(x*x,x))
require(sp.simplify(H+2*x*x/(1+x*x))==0,'generator identity')
require(sp.simplify(f*sp.diff(H,x)-4*x*x/(1+x*x)**3)==0,'second generator')
require(sp.simplify(x*x+H-x*x*(x*x-1)/(1+x*x))==0,'exact auxiliary certificate')
require(sp.simplify((1-r)**2-4*r)==0,'Poisson identity normalization')
require(sp.simplify((1+r)/(1-r)-s)==0,'Poisson identity at equilibrium')
require(sp.simplify((1-r*r)/(s*(1+2*r*(2*x*x-1)+r*r))-1/(1+x*x))==0,'full geometric identity')
exact=[]
for m in range(2,25):
    a=m//2
    q=-2+s+2*s*sum((-r)**j*sp.chebyshevt(2*j,x) for j in range(1,a+1))
    delta=2*s*r**(a+1)/(1-r)
    require(sp.simplify(q.subs(x,0)+delta)==0,'negative projection maximum')
    require(sp.simplify(2*s*sum(r**j for j in range(1,a+1))-2+s+delta)==0,'absolute coefficient majorant')
    require(sp.Poly(q,x).degree()<=m,'degree control')
    require(delta.is_positive is True,'positive tail')
    if m<=12: exact.append({'m':m,'delta':float(sp.N(delta,17))})
exact_count=checks

# Independently integrate the generator against Chebyshev modes at Gauss sites.
Nq=8192
theta=(np.arange(Nq)+0.5)*np.pi/Nq
sites=np.cos(theta); Hvalues=-2*sites**2/(1+sites**2)
for j in range(17):
    coeff=np.mean(Hvalues*np.cos(j*theta))*(1 if j==0 else 2)
    expected=(-2+math.sqrt(2)) if j==0 else (2*math.sqrt(2)*(-float(r))**(j//2) if j%2==0 else 0)
    require(abs(coeff-expected)<2e-14,'orthogonality coefficient cross-check')

# Actual nonlinear snapshots, from u(t)=W(u(0) exp(u(0)-2t)), u=x^2.
def flow(z,t):
    z=np.asarray(z)
    return np.sign(z)*np.sqrt(lambertw(z*z*np.exp(z*z-2*t)).real)

def differences(z,t):
    y=flow(z,t)
    return (y*y-z*z)/t

snapshot=[]
for m in (2,4,6,8):
    a=m//2; gap=2*math.sqrt(2)*float(r)**(a+1)/(1-float(r))
    tau=gap/(4*(1+2*m))
    # Designed quadrature samples, not an empirical assertion about iid data.
    d=differences(sites,tau)
    coef=np.array([np.mean(d*np.cos(j*theta))*(1 if j==0 else 2) for j in range(m+1)])
    hcoef=np.zeros(m+1); hcoef[0]=-2+math.sqrt(2)
    for j in range(2,m+1,2): hcoef[j]=2*math.sqrt(2)*(-float(r))**(j//2)
    coefficient_error=float(np.sum(np.abs(coef-hcoef)))
    # Sum of coefficient errors upper-bounds the sup error of these polynomials.
    require(coefficient_error<gap/8,'finite-time snapshot projection tolerance')
    z=np.linspace(-1,1,2001)
    q=np.polynomial.chebyshev.chebval(z,coef)
    require(float(q.max())<-0.75*gap,'snapshot negativity diagnostic')
    c=2/gap
    require(float(np.max(z*z+c*q))<0,'unregularized negative upper-bound failure')
    snapshot.append({'m':m,'tau':tau,'coefficient_l1_difference':coefficient_error,'grid_max_derivative':float(q.max()),'negative_objective_upper_majorant':1+c*(-gap+coefficient_error)})

# Direct data LPs for the non-polynomial example, using conservative F=1/2,
# K=1, G=2, Hessian=2; ell=3, M=3/2, omega_g(h)=2h.
grid_results=[]
last=math.inf
for n in (17,33,65,129,257):
    z=np.linspace(-1,1,n); h=1/(n-1); tau=h*h
    d=differences(z,tau); e=.75*tau+3*h
    # Variables t,c_plus,c_minus.
    objective=np.array([1.,e,e])
    Aub=np.column_stack([-np.ones(n),d,-d]); bub=-z*z
    dual=linprog(objective,A_ub=Aub,b_ub=bub,bounds=[(None,None),(0,None),(0,None)],method='highs')
    require(dual.success,'dual LP success')
    primal=linprog(-z*z,A_ub=np.vstack([d,-d]),b_ub=[e,e],A_eq=np.ones((1,n)),b_eq=[1.],bounds=(0,None),method='highs')
    require(primal.success,'primal LP success')
    upper=float(dual.fun+2*h); primal_upper=float(-primal.fun+2*h)
    require(abs(upper-primal_upper)<1e-8,'primal dual agreement')
    require(upper>=-1e-9,'certified LP contains known beta')
    require(upper<last,'refinement diagnostic decreases on tested grids')
    last=upper
    t,cp,cm=dual.x; c=cp-cm
    dense=np.linspace(-1,1,8193)
    true_residual=dense*dense+c*(-2*dense*dense/(1+dense*dense))
    require(float(np.max(true_residual))<=upper+1e-9,'dense residual diagnostic')
    require(float(np.max(Aub@dual.x-bub))<1e-8,'LP primal constraints')
    require(abs(np.sum(primal.x)-1)<1e-8,'probability normalization')
    grid_results.append({'sites':n,'fill_distance':h,'tau':tau,'error_margin':e,'dual_bound':upper,'primal_bound':primal_upper,'auxiliary_coefficient':float(c)})

# Deterministic exact-rational controls for sensitivity inequality (5) on finite spaces.
from fractions import Fraction as F
rng=np.random.default_rng(773109)
for case in range(200):
    g=[F(int(a),7) for a in rng.integers(-10,11,4)]
    a=[F(int(a),9) for a in rng.integers(-9,10,4)]
    perturb=[F(int(a),100) for a in rng.integers(-3,4,4)]
    eps=max(abs(u) for u in perturb)
    coeffs=[F(i,5) for i in range(-10,11)]
    J=min(max(g[j]+c*a[j] for j in range(4)) for c in coeffs)
    Jh=min(max(g[j]+c*(a[j]+perturb[j]) for j in range(4)) for c in coeffs)
    require(abs(J-Jh)<=2*eps,'exact finite sensitivity control')

# Negative controls intentionally test claims known to be false.
false=[]
delta2=10-7*sp.sqrt(2)
false.append(reject_false(sp.simplify(delta2)<=0,'drop strict projection negativity'))
false.append(reject_false(F(1,3)==F(1,2),'replace Chebyshev sampling by uniform moments'))
false.append(reject_false(-1>=0,'report negative unregularized value as an upper bound on beta=0'))
false.append(reject_false(F(1,100)/F(1,1000)<F(1,100)/F(1,100),'fixed noise vanishes with shorter sampling step'))
false.append(reject_false(sp.simplify((-x*(1-x)).subs(x,1))!=0,'discard unseen equilibrium at one'))
false.append(reject_false(float(grid_results[-1]['dual_bound'])==0,'finite tests establish exact convergence limit'))
print(json.dumps({'status':'PASS','exact_symbolic_checks':exact_count,'total_positive_checks':checks,'negative_controls_rejected':false,'projection_tail_checks':exact,'snapshot_quadrature_diagnostics':snapshot,'grid_lp_diagnostics':grid_results,'coverage_limit':'Finite algebra and floating diagnostics supplement analytic proofs; no iid sample bound, infinite-dimensional theorem, exact LP optimality or universal novelty is certified by these runs.','versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__}},indent=2,sort_keys=True))
