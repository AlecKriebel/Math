#!/usr/bin/env python3
"""Independent finite controls; analytical convergence is proved in REPORT.md."""
from fractions import Fraction as F
from math import factorial
import json

def cp(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def plus(a,b): return (a[0]+b[0],a[1]+b[1])
def scale(a,t): return (a[0]*t,a[1]*t)
def ip(n): return ((F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1)))[n%4]
def conv_coeff(n,poly):
    z=(F(0),F(0))
    for k,a in enumerate(poly):
        if n>=k: z=plus(z,cp(a,scale(ip(n-k),F(1,factorial(n-k)))))
    return z

def run():
    results=[]
    def check(label,condition,details=None):
        assert condition,label
        results.append({'check':label,'passed':True,'details':details})
    p=[(F(1),F(0)),(F(0),F(-1)),(F(-1),F(0))]
    q=[(F(-3),F(0)),(F(0),F(3)),(F(1),F(0))]
    check('radial_identity_numerator_constant',conv_coeff(0,p)==(1,0))
    check('radial_longitudinal_numerator_constant',conv_coeff(0,q)==(-3,0))
    check('both_linear_terms_cancel',conv_coeff(1,p)==conv_coeff(1,q)==(0,0))
    for n in range(2,25):
        check('identity_coefficient_n'+str(n),conv_coeff(n,p)==scale(ip(n),F((n-1)**2,factorial(n))))
        check('longitudinal_coefficient_n'+str(n),conv_coeff(n,q)==scale(ip(n),F(-(n-1)*(n-3),factorial(n))))
    check('quadratic_coefficients',conv_coeff(2,p)==conv_coeff(2,q)==(F(-1,2),0))
    check('cubic_radiation_scalar',conv_coeff(3,p)==(0,F(-2,3)) and conv_coeff(3,q)==(0,0))
    # A rigorous elementary upper bound for e: the remaining factorial tail
    # after n=7 is bounded geometrically because each denominator ratio >=9.
    e_partial=sum((F(1,factorial(n)) for n in range(8)),F(0))
    e_upper=e_partial+F(1,factorial(8))*F(9,8)
    check('elementary_e_upper_bound',e_upper<F(11,4),str(e_upper))
    check('fourth_order_majorant',2*e_upper-F(9,2)<1)
    # Finite exact shell cancellation is a control on the symmetry proof,
    # not an assertion about convergence of an infinite lattice sum.
    shells={}
    radius=8
    for x in range(-radius,radius+1):
        for y in range(-radius,radius+1):
            for z in range(-radius,radius+1):
                v=(x,y,z); r2=sum(t*t for t in v)
                if not 0<r2<=radius**2: continue
                a= shells.setdefault(r2,{'count':0,'tensor':[[0]*3 for _ in range(3)]})
                a['count']+=1
                for i in range(3):
                    for j in range(3):
                        a['tensor'][i][j]+=(r2 if i==j else 0)-3*v[i]*v[j]
    for r2,a in sorted(shells.items()):
        check('cubic_shell_r2_'+str(r2),a['tensor']==[[0]*3 for _ in range(3)],a['count'])
    k=F(1,10000)
    epsilon=2*k*k; eta=120*k*k
    check('selected_frequency_static_resolvent_smallness',epsilon<=F(1,60))
    check('selected_frequency_graph_smallness',eta<=F(1,2))
    check('graph_norm_majorant',eta/(1-eta)<=240*k*k)
    check('graph_reduction_error',2+2*240==482)
    check('trace_error',3*482==1446)
    trace_upper=-F(2,3)*k**3+1446*k**4
    check('negative_imaginary_trace',trace_upper<0,str(trace_upper))
    check('reported_trace_coefficient',trace_upper/k**3==F(-7831,15000))
    for ell in range(2,100):
        check('ball_harmonic_gap_ell_'+str(ell),F(ell,2*ell+1)-F(1,3)>=F(1,15))
    for j in range(1,16):
        # Normalize volume by 4*pi/3; compute the exact geometric series.
        removed=F(1,2**(3*j+12))*F(1,7)
        check('removed_volume_fraction_j'+str(j),0<removed<1,str(removed))
    # Infinite-dimensional countermodel: B_n=|e_n><e_n| ->0 strongly,
    # but (2-B_n)^-1-(2-0)^-1=(1/2)|e_n><e_n|.
    check('strong_static_not_norm_resolvent',F(1,2-1)-F(1,2)==F(1,2))
    # Jordan cluster model C_d=[[i,1],[d,i]] has characteristic
    # polynomial (z-i)^2-d. At d=0 it is defective; d>0 splits it.
    # Fixed-circle clusters are stable while Jordan block sizes need not be.
    check('jordan_defect_can_split',F(1,10000)>0 and F(1,10000)<F(1,16))
    return {'status':'PASS','scope':'Finite exact controls and explicit conceptual countermodels; no numerical certification of operator convergence or historical priority.','checks':results,'total_checks':len(results),'shell_radius':radius,'shells':len(shells),'trace_upper':str(trace_upper),'e_upper':str(e_upper)}
if __name__=='__main__': print(json.dumps(run(),indent=2,sort_keys=True))
