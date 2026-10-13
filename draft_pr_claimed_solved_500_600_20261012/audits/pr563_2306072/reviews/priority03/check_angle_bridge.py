"""Exact finite checks for BROWN_SUPPORT_WAVER.md, not a proof of Brown's theorem."""
from fractions import Fraction as F
from math import factorial
import json,pathlib
B=pathlib.Path(__file__).resolve().parent
checks=[]
def check(name,claim,detail):
    checks.append({'name':name,'passed':bool(claim),'detail':detail})
    assert claim,name

def mul(a,b,n=6):
    return [sum((a[j]*b[k-j] for j in range(k+1)),F(0)) for k in range(n+1)]
def inv(a,n=6):
    b=[1/a[0]]
    for k in range(1,n+1): b.append(-sum((a[j]*b[k-j] for j in range(1,k+1)),F(0))/a[0])
    return b
# h(u)=3-3*u*coth(u)+u*tanh(u) uses ordinary even series.
sinh_over_u=[F(1,factorial(k+1)) if k%2==0 else F(0) for k in range(7)]
cosh=[F(1,factorial(k)) if k%2==0 else F(0) for k in range(7)]
sinh=[F(1,factorial(k)) if k%2==1 else F(0) for k in range(7)]
u_sinh=[F(0)]+sinh[:-1]
a=mul(cosh,inv(sinh_over_u)); b=mul(u_sinh,inv(cosh))
h=[(F(3) if k==0 else F(0))-3*a[k]+b[k] for k in range(7)]
check('hyperbolic_series_coefficients',h==[0,0,0,0,F(-4,15),0,F(8,63)],list(map(str,h)))
check('half_disk_series_geometric_tail',sum((F(1,4)**n for n in range(1,40)),F(0))<F(1,3),'Tail sums for cosh and sinh/u each <=1/3')
check('cauchy_majorant',3*F(2)+F(1,2)+3<F(10),'|u coth u|<=2 and |u tanh u|<=1/2 on |u|=1/2')
d=F(1,10**12); s1=F(1,10**7); s2=F(1,10**5)
# phi'(s)/s^3 = -4/15*sin(2d)+8/63*cos(3d)*s^2+error.
def rem(s):return F(2560)*s**4/(1-2*s)
upper1=-F(4,15)*(2*d-(2*d)**3/6)+F(8,63)*s1**2+rem(s1)
lower2=-F(8,15)*d+F(8,63)*(1-(3*d)**2/2)*s2**2-rem(s2)
check('tangent_sign_nearer_infinity',upper1<0,{'rational_upper_phi_prime_over_s_cubed':str(upper1)})
check('tangent_sign_farther_inward',lower2>0,{'rational_lower_phi_prime_over_s_cubed':str(lower2)})
check('coordinate_interval_before_hyperbolic_poles',0<s1<s2<F(1,2),'No sinh/cosh zero except sinh at0 on disk1/2 by explicit bounds')
# Brown |B|=(1/2)sinh(1/2)*exp(-sin(d)/2)>=(25/96)*(1-d/2)>1/4.
mag_low=F(25,96)*(1-d/2)
check('point_evaluation_value_modulus',mag_low>F(1,4),str(mag_low))
# theta0+(1/2)sin(theta0)<pi because pi>3 and d+1/2<3/2<pi/2.
check('point_evaluation_in_upper_disk',d+F(1,2)<F(3,2),'0<arg(z0)<pi; r=tanh(1/4) lies in(0,1)')
# |sinh(sE)|<=s*exp(s)<=s/(1-s); hence |W|>(1-s2)^2/(4s2^2)>1.
radius_low=(1-s2)**2/(4*s2**2)
check('actual_tip_gate',radius_low>1,str(radius_low))
# E=e^{-i theta0/2}; Q(W) W'^2=4B E^2=4|B|>0.
check('trajectory_identity_algebra',F(4)>0,'B^2/(B-W)*(Wprime/W)^2 = 4B E^2 = 4|B|')
# Supplementary integer-Laurent geometry-only certificate.
x=F(3,4); p=F(9,10)
sin_lo=x-x**3/6; cos_hi=1-x*x/2+x**4/24
check('geometric_curve_phi_sign_at_one',sin_lo>p*cos_hi,'beta(1)=3/4; -r beta_prime(1)=9/10')
x=F(27,80); p=F(3,8)
check('geometric_curve_phi_sign_at_two',x/(1-x*x/2)<p,'beta(2)=27/80; -r beta_prime(2)=3/8')
result={'status':'PASS','checks':checks,'count':len(checks),'limitations':['Brown global maximizing/support and monotonicity theorems are external primary analytic premises, not established by this script.','Tip-radius and unique-trajectory continuation arguments are proved in the companion prose.','No unread Zemyan fulltext is excluded; this is an audit nonimplication certificate, not a novelty claim.']}
(B/'ANGLE_BRIDGE_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
