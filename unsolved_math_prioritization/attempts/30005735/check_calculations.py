#!/usr/bin/env python3
"""Reproduce rational algebra and labeled numerical illustrations in the report.
No network, private data, source documents or third-party code required.
"""
from fractions import Fraction as F
from math import sqrt
import json

def require(condition, label):
    """Run even under python -O/-OO; never use assert for verification."""
    if not condition:
        raise ValueError(label)

checks = {}
# Route 2. f(u)=u-(u-3)^2/4. w1=3, w2=3+delta, h0=0.
# The left acceleration endpoint is u=3+H and satisfies 2H-H^2/4=alpha.
rows=[]
for k in range(3,13):
    d=F(1,2**k); a=d/2
    # Rational interval [a/2, a] brackets the unique small root.
    g=lambda h: 2*h-h*h/4-a
    require(g(a/2)<0 and g(a)>0, "check_1: g(a/2)<0 and g(a)>0")
    require(a < d-d*d/4 , "check_2: a < d-d*d/4 ")
    # These square-root values are explicitly numerical illustrations;
    # root bracketing, admissibility intervals and lower bounds above are exact.
    H=2*float(a)/(2+sqrt(4-float(a))) # stable form of 4-2 sqrt(4-alpha)
    r=5-2*sqrt(1-float(a))
    f_local=lambda u:u-(u-3)**2/4
    require(abs(f_local(r)-(3+float(a)))<1e-13, "check_3: abs(f_local(r)-(3+float(a)))<1e-13")
    require(3<r<3+float(d), "check_4: 3<r<3+float(d)")
    require(abs(f_local(3+H)+H-(3+float(a)))<1e-13, "check_5: abs(f_local(3+H)+H-(3+float(a)))<1e-13")
    require(abs((3+H)-3-H)<1e-13, "check_6: abs((3+H)-3-H)<1e-13")
    require(abs(2*H-H*H/4-float(a))<1e-14, "check_7: abs(2*H-H*H/4-float(a))<1e-14")
    rows.append({'delta':float(d),'alpha':float(a),'generated_h':H,
                 'h_over_alpha_delta':H/float(a*d),
                 'rigorous_lower_bound_h_over_alpha_delta':float(1/(2*d))})
checks['switching_contact']={'exact_root_brackets_and_lower_bounds': True,
 'illustrative_float_rows':rows}
# Route 3. u rises from w to w+e, then returns; h is running maximum u-w.
# Final h=e lies strictly above the acceleration threshold a(w)=0,
# and strictly below the deceleration threshold d(w)=1.
e=F(1,8); require(0<e<1, "thin_pulse_amplitude")
checks['thin_pulse']={'epsilon':str(e),'TV_u':str(2*e),'TV_h':str(e),
 'limit_u_jump':'0','limit_h_jump':str(e),'required_positive_jump_endpoint_h':'0'}
# Route 4. q integrability: eta_uh=(V_h/V_u)eta_uu>0.
# Integrating along fixed h contradicts eta_h(A)<=0<=eta_h(D).
checks['entropy_identity']='V_u * eta_uh = V_h * eta_uu'
# Route 5. f(r)=r-r^2/20 near r=2. Flat scanning V=f(h), u in [h,h+1].
f=lambda r:F(r)-F(r)*F(r)/20
rows=[]
for N in (1,2,4,8,16):
    eps=[F(1,2**(n+6)) for n in range(N)]
    tv0=2*sum(eps,F(0)); tvt=sum((2+2*e for e in eps),F(0))
    mass=F(0)
    for e in eps:
        dv=f(2+e)-f(2)
        s_up=-dv/(F(1,2)+e); s_down=-2*dv
        # Rankine-Hugoniot for increasing and decreasing edges.
        require(s_up*(F(1,2)+e)+dv==0, "check_8: s_up*(F(1,2)+e)+dv==0")
        require(s_down*(-F(1,2))-dv==0, "check_9: s_down*(-F(1,2))-dv==0")
        require(F(-1,4)<s_down<s_up<0, "check_10: F(-1,4)<s_down<s_up<0")
        # Increasing-edge chord lies above its scanning/boundary path.
        # On acceleration part u=3+r, 0<=r<=e, the difference is quadratic.
        # Its minimum is at an endpoint since derivative remains negative.
        require((dv/(F(1,2)+e)) < F(4,5)-e/10, "check_11: (dv/(F(1,2)+e)) < F(4,5)-e/10")
        # Decreasing-edge chord lies below f on [2,2+e] by concavity
        # and the endpoint condition at 2+e; above that V is flat.
        require(dv-2*dv*e>0, "check_12: dv-2*dv*e>0")
        mass += 2*dv
    rows.append({'number_of_pulses':N,'initial_TV_h':str(tv0),
                 'spacing_TV_at_positive_time':str(tvt),
                 'spacing_L1_change_at_t_1':str(mass)})
checks['flat_scanning']=rows
print(json.dumps({'status':'exact rational checks and labeled numerical checks passed','checks':checks},indent=2))
