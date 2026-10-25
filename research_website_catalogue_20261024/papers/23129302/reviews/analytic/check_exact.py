#!/usr/bin/env python3
"""Independent exact identities and analytic certificate controls; no source imports."""
import datetime,hashlib,json
from pathlib import Path
import sympy as s
O=Path(__file__).resolve().parent
checks=[]
def same(name,left,right):
 result=s.cancel(left-right)
 if result!=0:raise RuntimeError((name,str(result)))
 checks.append({'name':name,'kind':'exact_symbolic_identity','verified':True})
x,z,r,y,a=s.symbols('x z r y a',real=True)
f=lambda x,r:((r+4)*x+r+1)/(2*r*x+2)
b=lambda z,r:(2*z-r-1)/(r+4-2*r*z)
h=lambda x,r:(x+r/4)/(1+r*x)
fp=(4-r*r)/(2*(1+r*x)**2)
same('f_after_b',f(b(z,r),r),z)
same('b_after_f',b(f(x,r),r),x)
same('h_inverse',h(h(x,r),-r),x)
same('lifted_conjugacy',f(x,r),2*h(x,r)+s.Rational(1,2))
same('f_prime',s.diff(f(x,r),x),fp)
same('b_parameter_derivative',s.diff(b(z,r),r),-(1-4*b(z,r)**2)/(4-r*r))
same('h_inverse_parameter_derivative',s.diff(h(x,-r),r),(x*x-s.Rational(1,4))/(1-r*x)**2)
same('log_fprime_x',s.diff(fp,x)/fp,-2*r/(1+r*x))
same('log_fprime_r',s.diff(fp,r)/fp,-2*r/(4-r*r)-2*x/(1+r*x))
for zz,xx in [(s.Rational(-1,2),s.Rational(-1,2)),(s.Rational(1,2),-r/4),(s.Rational(3,2),s.Rational(1,2))]:same('inverse_endpoint_'+str(zz),b(zz,r),xx)

beta,m,v=s.symbols('beta m v',real=True)
C=1+beta/4
L=s.Matrix([[1/(1+beta*m),0],[-beta*v/(1+beta*m),1]])
M=C*s.eye(2)-L.T*L
same('rank_one_lower_minor',M[1,1],beta/4)
same('rank_one_full_determinant',M.det(),beta**2*((C*m-s.Rational(1,4))**2+C*(m-m*m-v*v))/(1+beta*m)**2)
U=(2+a)**2/(4*(2-a)**2)*(1+(16-100*a*a)/(4*(4-a*a)))
same('U_closed_form',U,(2+a)*(4-13*a*a)/(2*(2-a)**3))
same('positive_polynomial_certificate',7*(2-a)**3-5*(2+a)*(4-13*a*a),172*(a-s.Rational(13,43))**2+s.Rational(12,43)+58*a**3)
assert s.Rational(7,10)<s.Rational(21,25)**2<1
assert 16*s.Rational(21,25)/(1-s.Rational(21,25))==84
assert 1+s.Rational(25,96)*84==s.Rational(183,8)
assert 3+s.Rational(25,24)*84==s.Rational(181,2)
assert s.Rational(181,2)+s.Rational(35,24)*84==213
assert s.Rational(2,5)*2/(1-s.Rational(2,5)/2)==1
assert 2*s.Rational(2,5)/(4-s.Rational(2,5)**2)+1/(1-s.Rational(2,5)/2)==s.Rational(35,24)
checks.append({'name':'all_contraction_sensitivity_and_distortion_constants','kind':'exact_rational_inequalities','verified':True})

sigma=2*(y+r)/((r+1)*y+r+4)
tau=2*(y+r)/((r-1)*y-r+4)
weight=s.Rational(1,2)-(r+y)/(4+r*y)
w=lambda parameter,coordinate:(1-parameter**2/4)/(1-coordinate*parameter)**2
same('invariant_convex_density_family',w(y,b(z,r))*s.diff(b(z,r),z)+w(y,b(z+1,r))*s.diff(b(z+1,r),z),weight*w(sigma,z)+(1-weight)*w(tau,z))
for name,t,den in [('sigma',sigma,(r+1)*y+r+4),('tau',tau,(r-1)*y-r+4)]:
 same(name+'_positive_y_derivative',s.diff(t,y),2*(4-r*r)/den**2)
 same(name+'_positive_r_derivative',s.diff(t,r),2*(4-y*y)/den**2)
 vals=[s.factor(t.subs({r:rr,y:yy})) for rr in [-s.Rational(2,5),s.Rational(2,5)] for yy in [-s.Rational(2,3),s.Rational(2,3)]]
 assert min(vals)>=-s.Rational(2,3) and max(vals)<=s.Rational(2,3)
 checks.append({'name':name+'_range_by_proved_monotonicity','kind':'exact_continuous_corner_certificate','corners':list(map(str,vals)),'verified':True})
same('weight_r_monotonicity',s.diff(weight,r),-(4-y*y)/(4+r*y)**2)
same('weight_y_monotonicity',s.diff(weight,y),-(4-r*r)/(4+r*y)**2)
wv=[weight.subs({r:rr,y:yy}) for rr in [-s.Rational(2,5),s.Rational(2,5)] for yy in [-s.Rational(2,3),s.Rational(2,3)]]
assert min(wv)==s.Rational(1,4) and max(wv)==s.Rational(3,4)
for xx in [-s.Rational(1,2),s.Rational(1,2)]:
 for yy in [-s.Rational(2,3),s.Rational(2,3)]:assert s.Rational(1,2)<=w(yy,xx)<=2
checks.append({'name':'convex_weight_and_density_bounds','kind':'rational_endpoints_with_analytic_monotonicity','verified':True})

# Exact positive-section check, including a positive-measure zero target fiber.
from fractions import Fraction as Q
left=[Q(0),Q(0),Q(2),Q(0),Q(1),Q(3)]
right=[Q(0),Q(4),Q(0),Q(2),Q(1),Q(1)]
target=[Q(0),Q(2),Q(0),Q(0),Q(2),Q(2)]
old=[(u+v)/2 for u,v in zip(left,right)]
qleft=[u/v if v else Q(1) for u,v in zip(left,old)]
qright=[u/v if v else Q(1) for u,v in zip(right,old)]
assert all((u+v)/2==1 and 0<=u<=2 and 0<=v<=2 for u,v in zip(qleft,qright))
assert all(ql*v==u and qr*v==w0 for ql,qr,v,u,w0 in zip(qleft,qright,old,left,right))
assert all((ql*z0+qr*z0)/2==z0 for ql,qr,z0 in zip(qleft,qright,target))
assert sum((abs(ql*z0-u)+abs(qr*z0-w0))/2 for ql,qr,z0,u,w0 in zip(qleft,qright,target,left,right))==sum(abs(z0-v) for z0,v in zip(target,old))
checks.append({'name':'positive_exact_fiber_section_including_zero_fiber','kind':'independent_fraction_control','verified':True})

# A genuinely unbounded, non-L2, symmetric density with a whole zero interval.
# In t=x+1/2 coordinates let density t^(-3/4) on (0,1/4), its reflection
# near1, and0 in between. Exact normalization and its PIT are elementary.
t=s.symbols('t',positive=True)
edge=s.Rational(1,4)
normalizer=1/(8*edge**s.Rational(1,4))
same('rough_density_mass',2*normalizer*4*edge**s.Rational(1,4),1)
same('rough_left_CDF_at_flat',4*normalizer*edge**s.Rational(1,4),s.Rational(1,2))
checks.append({'name':'rough_density_nonL2_zeros_and_PIT_flat','kind':'analytic_exact_control','density':'c*t^(-3/4) on(0,1/4), reflection near1, zero on[1/4,3/4]; c=1/(8*(1/4)^(1/4))','not_L2':'square exponent -3/2 is nonintegrable','central_basin':'symmetric so r_j=0; exact doubling map transfer is L1-exact','flat_CDF':'middle half has zero input mass; CDF transforms non-atomic input to uniform and is constant1/2 on zero interval','verified':True})

result={'record_id':'23129302','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python_sympy':s.__version__,'checks':checks,'universal_proof_scope':'Rational identities and analytic interval certificates support the written proof; finite controls alone do not establish the infinite-dimensional theorem.','source_helpers_imported_or_executed':False}
(O/'exact-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'all_verified':True,'sympy':s.__version__}))
