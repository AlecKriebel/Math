"""Exact symbolic controls for the smooth degenerate-conductivity example.

No finite check replaces the distributional test/density proof in PROOF.md.
Only locally installed SymPy and the standard library are used.
"""
import sympy as s
import json
from collections import Counter
from fractions import Fraction
counts=Counter()
def ck(t,name):
    assert t,name
    counts[name]+=1
x,y,z=s.symbols('x y z',real=True);q=x*x+y*y;r=s.sqrt(q)
chi=s.Function('chi')(q,z);eta=s.Function('eta')(q,z)
A0=s.Matrix([-y/q,x/q,0]);A=chi*A0;B=eta*A0
coords=(x,y,z)
def div(V):return s.simplify(sum(s.diff(V[j],coords[j]) for j in range(3)))
def curl(V):return s.Matrix([s.diff(V[2],y)-s.diff(V[1],z),s.diff(V[0],z)-s.diff(V[2],x),s.diff(V[1],x)-s.diff(V[0],y)]).applyfunc(s.simplify)
ck(div(A0)==0,'circulation_divergence')
ck(curl(A0)==s.zeros(3,1),'circulation_locally_curl_free')
ck(div(A)==0,'smooth_cutoff_preserves_solenoidal_input')
ck(div(B)==0,'dual_test_solenoidal')
ck(s.simplify(A0.dot(s.Matrix([s.diff(q,c) for c in coords])))==0,'radial_gradient_orthogonality')
ck(s.simplify(A0.dot(A0)-1/q)==0,'circulation_squared_norm')
sigma=eta*(r-x)
ck(s.simplify(div(sigma*A0)-eta*y/q)==0,'smooth_weighted_rhs_identity_off_axis')
ck(s.simplify(A0.dot(B)-eta/q)==0,'strict_dual_pairing_integrand')

eps=s.symbols('eps',positive=True);theta=s.symbols('theta',real=True)
hminus=-theta-s.pi;hmiddle=(s.pi/eps-1)*theta;hplus=-theta+s.pi
ck(s.simplify(hminus.subs(theta,-eps)-hmiddle.subs(theta,-eps))==0,'potential_left_join')
ck(s.simplify(hplus.subs(theta,eps)-hmiddle.subs(theta,eps))==0,'potential_right_join')
ck(hminus.subs(theta,-s.pi)==hplus.subs(theta,s.pi)==0,'potential_periodic_endpoint_values')
ck(s.diff(hminus,theta)==s.diff(hplus,theta)==-1,'potential_periodic_endpoint_derivatives')
wout=s.diff(hplus,theta);win=s.diff(hmiddle,theta)
ck(s.simplify((2*s.pi-2*eps)*wout+2*eps*win)==0,'single_valued_zero_mean_derivative')
ck(s.simplify(win+1-s.pi/eps)==0 and wout+1==0,'weighted_residual_pulse')
ck(s.simplify((2*s.pi-2*eps)*wout*wout+2*eps*win*win-(2*s.pi**2/eps-2*s.pi))==0,'unweighted_angular_energy')
angular=s.integrate(1-s.cos(theta),(theta,-eps,eps))
ck(s.simplify(angular-2*(eps-s.sin(eps)))==0,'weighted_angular_energy_exact')
ck(s.simplify(s.integrate(theta**2/2,(theta,-eps,eps))-eps**3/3)==0,'quadratic_angular_upper_integral')
f=eps-s.sin(eps)
ck([s.diff(f,eps,j).subs(eps,0) for j in range(3)]==[0,0,0],'cubic_error_zero_initial_derivatives')
# f'''=cos, hence 0<=f<=eps^3/6 on 0<eps<1 by integral remainder;
# alternatively integrate 0<=1-cos(theta)<=theta^2/2.
ck(s.diff(f,eps,3)==s.cos(eps),'cubic_error_third_derivative')
ck(s.limit((eps-s.sin(eps))/eps**3,eps,0)==s.Rational(1,6),'weighted_energy_asymptotic_coefficient')
R=s.symbols('R',positive=True)
ck(s.simplify(s.integrate(1/R,(R,1,2))*2-2*s.log(2))==0,'unweighted_radial_factor')
# Cylindrical Jacobian cancels the metric and radial conductivity factors.
E=s.symbols('E',positive=True)
ck(s.simplify((E*R*(1-s.cos(theta)))*(1/R**2)*R-E*(1-s.cos(theta)))==0,'cylindrical_weight_metric_Jacobian')
for k in range(1,101):
    e=Fraction(1,2**k)
    ck(0<e<1,'admissible_approximation_scales')
    ck(e**3/(e*e)==e,'linear_weighted_error_scale')
    ck(1/e==2**k,'unweighted_growth_scale')
# Translation by -(3/2,0,0): the inner-ball radius1/4 stays within the annular cylinder.
ck(Fraction(3,2)-Fraction(1,4)>1 and Fraction(3,2)+Fraction(1,4)<2 and Fraction(1,4)<1,'optional_origin_ball_translation')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'categories':dict(sorted(counts.items())),'scope':'Algebraic, single-valuedness, cylindrical integration and scale controls. The complete H1-local nonexistence proof, density and source interpretation are in PROOF.md and require independent review.','numerical_solver_used':False,'substantive_author_turns':1},indent=2,sort_keys=True))
