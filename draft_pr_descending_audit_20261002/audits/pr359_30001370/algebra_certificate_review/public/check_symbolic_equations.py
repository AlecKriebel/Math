#!/usr/bin/env python3
"""Independently derive rational identities. SymPy1.14; read-only."""
import json
import sympy as s

a,r,x,z,y = s.symbols('a r x z y')
f = ((r+4)*x+r+1)/(2*r*x+2)
b = (2*z-r-1)/(r+4-2*r*z)
h = (x+r/4)/(1+r*x)
fp = s.diff(f,x)
checks = {}

def zero(name, expr):
    value=s.factor(expr)
    assert value==0,(name,value)
    checks[name]='exact_zero'

zero('inverse_composition', f.subs(x,b)-z)
zero('forward_composition', b.subs(z,f)-x)
zero('doubling_transport_factorization',f-(2*h+s.Rational(1,2)))
zero('inverse_sensitivity', s.diff(b,r)+(1-4*b*b)/(4-r*r))
zero('inverse_jacobian',s.diff(b,z)-2*(4-r*r)/(r+4-2*r*z)**2)
zero('forward_jacobian',fp-(4-r*r)/(2*(1+r*x)**2))
zero('spatial_log_sensitivity',s.diff(fp,x)/fp+2*r/(1+r*x))
zero('parameter_log_sensitivity',s.diff(fp,r)/fp+2*r/(4-r*r)+2*x/(1+r*x))
zero('new_cut_matching',b.subs(z,s.Rational(1,2))+r/4)
zero('lower_endpoint',b.subs(z,-s.Rational(1,2))+s.Rational(1,2))
zero('upper_endpoint',b.subs(z,s.Rational(3,2))-s.Rational(1,2))
beta=(16-100*a*a)/(4-a*a)
factor=(2+a)**2/(4*(2-a)**2)
C=s.Rational(91,100)/factor-1-beta/4
R=559*a**3+1846*a*a-1292*a+328
P=2749829*a**6+18324452*a**5+17679340*a**4-38590240*a**3+26922160*a*a-7787968*a+808256
zero('C_cubic_numerator',C-R/(25*(2-a)*(2+a)**2))
zero('square_test_sextic_numerator',9*C*C-beta-P/(625*(2-a)**2*(2+a)**4))
zero('beta_monotone_derivative',s.diff(beta,a)+768*a/(4-a*a)**2)
zero('expansion_factor_derivative',s.diff(factor,a)-2*(a+2)/(2-a)**3)
zero('source_assumption_I_margin',(25-50*a)-(16-100*a*a)-100*(a-s.Rational(1,4))**2-s.Rational(11,4))
wy=(1-y*y/4)/(1-x*y)**2
sigma=2*(y+r)/((r+1)*y+r+4)
tau=2*(y+r)/((r-1)*y-r+4)
p=s.Rational(1,2)-(r+y)/(4+r*y)
for label,branch,target,weight in [('lower',0,sigma,p),('upper',1,tau,1-p)]:
    inv=b.subs(z,x+branch)
    zero(label+'_normalized_transport',wy.subs(x,inv)*s.diff(inv,x)-weight*wy.subs(y,target))
    denominator=s.denom(target)
    zero(label+'_y_monotonicity',s.diff(target,y)-2*(4-r*r)/denominator**2)
    zero(label+'_r_monotonicity',s.diff(target,r)-2*(4-y*y)/denominator**2)
# Independent exact source-kernel counterexample and resolvent coefficients.
P0=lambda q:s.expand((q.subs(x,x/2-s.Rational(1,4))+q.subs(x,x/2+s.Rational(1,4)))/2)
phi=lambda q:s.integrate(x*q,(x,-s.Rational(1,2),s.Rational(1,2)))
q=x**3-s.Rational(3,20)*x
zero('source_kernel_phi',phi(q))
zero('source_kernel_noninvariance',phi(P0(q))-s.Rational(1,320))
B,lam=s.symbols('B lam')
zero('linear_unstable_eigenvalue',P0(x)+B*x*phi(x)-(s.Rational(1,2)+B/12)*x)
zero('BV_tail_constant',(1+B/(2*(s.Rational(1,2)+B/12)-1))-7)
print(json.dumps(dict(status='PASS',sympy=s.__version__,identities=checks,
                      limitation='Exact rational identities only; functional analysis is in the accompanying audit.'),indent=2,sort_keys=True))
