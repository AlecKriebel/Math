#!/usr/bin/env python3
"""Independent algebra/ODE controls for the frozen MTW audit.
Not a cut-locus computation or a global A3w certificate.
"""
import json, pathlib, platform, sympy as s
from scipy.integrate import solve_ivp
import numpy as np
checks={}; details={}
x,a,z,r,t=s.symbols('x a z r t', real=True)
k0,k1,k2=s.symbols('k0 k1 k2')
# Solve polynomial ODE residuals for unknown coefficients, rather than replaying
# the author's forward recurrence.
q=s.symbols('q0:7');c=sum(q[j]*t**j for j in range(7));pot=k0+k1*t+k2*t*t/2
ceqs=[q[0]-1,q[1]]+[s.expand(s.diff(c,t,2)+pot*c).coeff(t,j) for j in range(5)]
jeqs=[q[0],q[1]-1]+[s.expand(s.diff(c,t,2)+pot*c).coeff(t,j) for j in range(5)]
C=c.subs(s.solve(ceqs,q));J=c.subs(s.solve(jeqs,q));H=s.series(t*C/J,t,0,5).removeO().expand()
checks['independent_jacobi_series']=s.expand(H-(1-k0*t**2/3-k1*t**3/12-(k2/60+k0**2/45)*t**4))==0
# A source/target orientation trap: endpoint Hessian r J'/J has K1/4,
# not K1/12. These differ when curvature varies along the segment.
endpoint=s.series(t*s.diff(J,t)/J,t,0,4).removeO().expand()
checks['source_target_distinction']=s.expand(endpoint).coeff(t,3)==-k1/4 and H.coeff(t,3)==-k1/12
f=s.cos(x)+a*s.cos(x)**3*s.sin(x)**4
N=1+a*(-49*z**3+55*z**2-12*z);D=1+a*(z**2-z**3)
checks['warped_curvature_identity']=s.trigsimp(-s.diff(f,x,2)*D.subs(z,s.sin(x)**2)-f*N.subs(z,s.sin(x)**2))==0
checks['positive_curvature_decomposition']=s.expand(N-(1-6*a+a*(1-z)*(49*z*z-6*z+6)))==0
checks['positive_quadratic_discriminant']=(-6)**2-4*49*6<0
checks['pole_oddness_and_unit_slope']=s.trigsimp(f.subs(x,s.pi/2-r)+f.subs(x,s.pi/2+r))==0 and s.diff(f.subs(x,s.pi/2-r),r).subs(r,0)==1
checks['equatorial_metric_jet']=s.diff(f,x).subs(x,0)==0 and s.diff(f,x,2).subs(x,0)==-1 and s.diff(f,x,4).subs(x,0)==1+24*a
# Latitude Jacobi variation from the linearized geodesic equation.
X=s.sin(r*t)/r
checks['latitude_variation_ode']=s.simplify(s.diff(X,t,2)+r*r*X)==0 and X.subs(t,0)==0 and s.diff(X,t).subs(t,0)==1
# Independently evaluate the two boundary variation integrals in arclength u.
u=s.symbols('u',real=True)
I0=(r-s.sin(r)*s.cos(r))/(2*r*s.sin(r)**2)
I1=(r*(1+2*s.cos(r)**2)-3*s.sin(r)*s.cos(r))/(8*r*s.sin(r)**2)
# Exact trig primitive identities verify the integral endpoints.
# The expressions are obtained by product-to-sum before integration.
integrand0=(1-s.cos(2*(r-u)))/2
integrand1=(1-s.cos(2*(r-u))-s.cos(2*u)+(s.cos(2*r-4*u)+s.cos(2*r))/2)/4
checks['I0_closed_form']=s.trigsimp(s.integrate(integrand0,(u,0,r))/(r*s.sin(r)**2)-I0)==0
checks['I1_closed_form']=s.trigsimp(s.integrate(integrand1,(u,0,r))/(r*s.sin(r)**2)-I1)==0
h=r*s.cot(r);k=1-h
checks['I0_radial_identity']=s.trigsimp(I0+s.diff(h,r)/(2*r))==0
kap=s.symbols('kappa');F=2*I0+kap*I1-2*k/r**2
checks['small_distance_full_coefficient']=s.simplify(s.limit(F/r**2,r,0)-(s.Rational(2,45)+kap/30))==0
checks['pi2_boundary_second_variation']=s.simplify((-2*I0-kap*I1).subs({r:s.pi/2,kap:-s.Rational(12,5)}))==-s.Rational(7,10)
checks['pi2_negative_full_value']=s.simplify(F.subs({r:s.pi/2,kap:-s.Rational(12,5)})-(s.Rational(7,10)-8/s.pi**2))==0
# Independent arbitrary-direction full tensor extraction from a line z+lambda w.
l,b0,b1,ub,us,wb,ws=s.symbols('lambda b0 b1 ub us wb ws',real=True)
H0,Hb,Hs,Hbb,Hbs,Hss=s.symbols('H Hb Hs Hbb Hbs Hss',real=True)
b=l*wb;v=r+l*ws
jH=H0+l*(Hb*wb+Hs*ws)+l*l*(Hbb*wb**2+2*Hbs*wb*ws+Hss*ws**2)/2
val=ub**2+us**2+(jH-1)*(ub*v-us*b)**2/(b*b+v*v)
full=s.factor(-s.diff(val,l,2).subs(l,0))
# Parametrize ALL null pairs projectively, u=(1,t), w=(-t,1).
null=s.expand(full.subs({ub:1,us:t,wb:-t,ws:1}))
expected=-Hss+2*Hbs*t+(-Hbb-4*Hs/r+6*(H0-1)/r**2)*t*t+4*Hb/r*t**3+2*(1-H0)/r**2*t**4
checks['general_quartic_independent_line_method']=s.simplify(null-expected)==0
P=-s.diff(h,r,2);Q=2*k/r**2;T=-8*I0+4*k/r**2
geq=s.trigsimp(full.subs({H0:h,Hb:0,Hs:s.diff(h,r),Hbb:-2*I0-kap*I1,Hbs:0,Hss:s.diff(h,r,2)})-(F*ub**2*wb**2+P*ub**2*ws**2+Q*us**2*wb**2+T*ub*us*wb*ws))
checks['equatorial_full_tensor_all_directions']=geq==0
checks['null_mixed_coefficient']=s.trigsimp(F-T-(10*I0+kap*I1-6*k/r**2))==0
checks['endpoint_jacobi_normalization']=s.simplify(X.subs({t:1,r:s.pi/2}))==2/s.pi
checks['strict_null_margin_pi2']=s.Rational(47,10)-24/s.Integer(9)>s.Rational(8,10) and 8/(s.Rational(22,7)**2)>s.Rational(8,10)
# Bounded numerical control independently integrates the full latitude and
# Jacobi IVP at the one analytically certified off-cut witness. No global scan.
a_num=.1;rv=np.pi/2

def curvature(xx):
 zz=np.sin(xx)**2;return (1+a_num*(-49*zz**3+55*zz**2-12*zz))/(1+a_num*(zz**2-zz**3))
def warp(xx):return np.cos(xx)+a_num*np.cos(xx)**3*np.sin(xx)**4
def warp_prime(xx):return -np.sin(xx)+a_num*(-3*np.cos(xx)**2*np.sin(xx)**5+4*np.cos(xx)**4*np.sin(xx)**3)
def transverse(bb):
 speed2=rv*rv+bb*bb
 def ode(tt,y):
  xx,xd,C,Cd,J,Jd=y
  return [xd,rv*rv*warp_prime(xx)/warp(xx)**3,Cd,-speed2*curvature(xx)*C,Jd,-speed2*curvature(xx)*J]
 sol=solve_ivp(ode,[0,1],[0,bb,1,0,0,1],method='DOP853',rtol=3e-13,atol=1e-14)
 assert sol.success
 return sol.y[2,-1]/sol.y[4,-1]
fd=[];base=transverse(0)
for eps in [2e-3,1e-3,5e-4]:
 hbb=(transverse(eps)+transverse(-eps)-2*base)/eps**2
 fd.append({'step':eps,'H_bb':hbb,'absolute_error_from_minus_0_7':abs(hbb+.7)})
checks['numerical_local_Hbb_control']=fd[-1]['absolute_error_from_minus_0_7']<1e-6
checks={key:bool(value) for key,value in checks.items()}
assert all(checks.values()),checks
out={'status':'PASS','python':platform.python_version(),'sympy':s.__version__,'count':len(checks),'checks':checks,'numerical_local_diagnostic':fd,'scope':'Independent finite algebra and local ODE controls only. Geometry is audited in INDEPENDENT_REVIEW.md; no global A3w or cut-domain numerical certification.'}
pathlib.Path(__file__).with_name('INDEPENDENT_CONTROL_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
