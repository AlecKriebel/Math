#!/usr/bin/env python3
"""Exact algebra controls only. Requires Python 3 and SymPy.

These checks do not construct a shrinking-soliton counterexample and do not
prove the unrestricted gradient estimate. Run from any directory.
"""
import json
from pathlib import Path
import sympy as s

checks = []
def ok(name, predicate):
    assert bool(predicate), name
    checks.append(name)
def zero(name, expr):
    ok(name, s.simplify(expr) == 0)

r, n, alpha, B, delta, A = s.symbols('r n alpha B delta A', real=True)
q, F, R, H2 = s.symbols('q F R H2', real=True)
zero('strict_quadratic_gap_expansion', (r-5*n)**2/4-alpha*r**2-B-((s.Rational(1,4)-alpha)*r**2-5*n*r/2+25*n*n/4-B))
zero('linear_absorption_at_threshold', (delta*r*r/4-5*n*r/2).subs(r,10*n/delta))
zero('constant_absorption_at_threshold', (delta*r*r/4-B).subs(r*r,4*B/delta))
zero('remaining_quadratic_coefficient', delta-delta/4-delta/4-delta/2)
zero('bounded_scalar_formula', (r-5*n)**2/4-A-((r*r-10*n*r+25*n*n)/4-A))
t=s.symbols('t',real=True)
zero('index_endpoint_integral', s.integrate(1-t*t,(t,0,1))-s.Rational(2,3))
zero('index_two_cutoff_energy', 2*s.integrate(1,(t,0,1))-2)
zero('global_Ricci_endpoint_coefficient', 2*s.Rational(2,3)-s.Rational(4,3))
zero('weighted_trace_identity', (n/2-R-q).subs(R,F-q)-(n/2-F))
zero('Bochner_sign_algebra', 2*(H2-q+q/2)-(2*H2-q))
zero('Bochner_trace_substitution', (n/2-R).subs(R,F-q)-(n/2-F+q))
# Explicit Gaussian control in 3D.
x,y,z=s.symbols('x y z',real=True)
coords=[x,y,z]
f=sum(v*v for v in coords)/4
qg=sum(s.diff(f,v)**2 for v in coords)
Dfq=sum(s.diff(qg,v,2)-s.diff(f,v)*s.diff(qg,v) for v in coords)
zero('Gaussian_Hamilton_identity', qg-f)
zero('Gaussian_Bochner_identity', Dfq-(s.Rational(3,2)-qg))
# Product k-dimensional Einstein factor + m-dimensional Gaussian factor.
k,m=s.symbols('k m', positive=True, integer=True)
T=s.symbols('T',nonnegative=True)
fp=k/2+T/4
qp=T/4
zero('product_Hamilton_identity', fp-k/2-qp)
zero('product_weighted_trace', m/2-qp-((k+m)/2-fp))
zero('product_Bochner_identity', m/2-qp-(2*m/4-qp))
# Smooth profile: summable support sizes, exact center bounds.
j=s.symbols('j', integer=True, positive=True)
zero('profile_total_support_bound',2*s.summation(2**(-j-3),(j,2,s.oo))-s.Rational(1,8))
zero('profile_center_derivative_factor', (j/s.sqrt(1+j*j))*j**-3*s.sqrt(1+j*j)/2-1/(2*j*j))
ok('profile_gradient_bound_tends_zero',s.limit(1/(2*j*j),j,s.oo)==0)
ok('profile_Hessian_bound_tends_zero',s.limit((j**-6+1/(j**3*(1+j*j)))/2,j,s.oo)==0)
for v in [2,3,4,8,16,64]:
    upper=s.Rational(1,2)*(s.Rational(1,v**6)+s.Rational(1,v**3*(1+v*v)))
    ok(f'profile_Hessian_defect_center_{v}',0<upper<s.Rational(1,2))
# Cigar: calculate Christoffel, Ricci and Hessian directly.
v=[x,y]
rho=1+x*x+y*y
g=4/rho*s.eye(2)
gi=g.inv()
u=-s.log(rho)
Gamma=[[[s.simplify(sum(gi[a,b]*(s.diff(g[b,c],v[d])+s.diff(g[b,d],v[c])-s.diff(g[c,d],v[b]))/2 for b in range(2))) for d in range(2)] for c in range(2)] for a in range(2)]
Ric=s.zeros(2)
Hess=s.zeros(2)
for a in range(2):
    for b in range(2):
        Ric[a,b]=s.simplify(sum(s.diff(Gamma[c][a][b],v[c])-s.diff(Gamma[c][a][c],v[b])+sum(Gamma[c][c][d]*Gamma[d][a][b]-Gamma[c][b][d]*Gamma[d][a][c] for d in range(2)) for c in range(2)))
        Hess[a,b]=s.simplify(s.diff(u,v[a],v[b])-sum(Gamma[c][a][b]*s.diff(u,v[c]) for c in range(2)))
        zero(f'cigar_steady_equation_{a}_{b}',Ric[a,b]+Hess[a,b])
Sc=s.simplify(s.trace(gi*Ric))
Qc=s.simplify(sum(gi[a,b]*s.diff(u,v[a])*s.diff(u,v[b]) for a in range(2) for b in range(2)))
zero('cigar_scalar',Sc-1/rho)
zero('cigar_gradient_square',Qc-(x*x+y*y)/rho)
zero('cigar_Hamilton_identity',Sc+Qc-1)
zero('cigar_tip_gradient_x',s.diff(u,x).subs({x:0,y:0}))
zero('cigar_tip_gradient_y',s.diff(u,y).subs({x:0,y:0}))
zero('cigar_tip_scalar',Sc.subs({x:0,y:0})-1)
zero('cigar_radial_length_antiderivative',s.diff(2*s.asinh(r),r)-2/s.sqrt(1+r*r))
ok('cigar_complete_radial_length',s.limit(2*s.asinh(r),r,s.oo)==s.oo)
# Metric rescaling: the constant in the soliton equation tends to zero.
a=s.symbols('a',positive=True)
u0=s.symbols('u0',real=True)
zero('rescaled_Hamilton_identity',(F/a).subs(F,u0+a)-(1+u0/a))
ok('rescaled_soliton_constant_tends_zero',s.limit(1/(2*a),a,s.oo)==0)
zero('rescaled_tip_scalar',(F-q).subs(F,a)/a-(1-q/a))

result={
    'all_passed':True,
    'passed':len(checks),
    'checks':checks,
    'method':'Exact symbolic algebra and specified rational controls; no numerical search.',
    'limitations':[
        'No unrestricted gradient bound proved.',
        'The one-dimensional profile is not a shrinking Ricci soliton.',
        'The cigar is steady, not shrinking, and is only a test of the conditional limiting equations.',
        'The infinite smooth profile construction and geometric implications require the proofs in RESULT.md.'
    ]
}
out=Path(__file__).with_name('result.json')
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'all_passed':True,'passed':len(checks),'output':str(out)}))
