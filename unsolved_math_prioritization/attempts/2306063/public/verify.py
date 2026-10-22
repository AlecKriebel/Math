#!/usr/bin/env python3
"""Finite controls only; no numerical certification of infinite end type."""
from fractions import Fraction as F
import cmath
import hashlib
import json
import math
from pathlib import Path

COUNTS={}
MAXERR={}
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    COUNTS[name]=COUNTS.get(name,0)+1

def close(name, lhs, rhs, tol=2e-11):
    err=abs(lhs-rhs)/max(1,abs(lhs),abs(rhs))
    MAXERR[name]=max(MAXERR.get(name,0.0),err)
    check(name,err<tol)

def main():
    # Exact affine complex conjugacy, represented by real/imaginary Fractions.
    for a in map(F,['1/4','1/2','3/4','5/4','2','4']):
        for b in map(F,['0','1/3','2']):
            cr,ci=b/(a-1),1/(a-1)
            for x in map(F,['1/3','1','7','100']):
                check('affine_conjugacy_real', a*x+b+cr==a*(x+cr))
                check('affine_conjugacy_imag', 1+ci==a*ci)
            # The absolute shifted heights give one log-period of radial width.
            lo,hi=sorted([abs(ci),abs(ci+1)])
            check('radial_ratio',hi/lo==max(a,1/a))
            check('signed_angle_log', (a>1)==(ci>0))
            af,bf=float(a),float(b)
            c=complex(float(cr),float(ci))
            for x in [100.,1000.,10000.]:
                q0=cmath.exp(2j*math.pi*cmath.log(x+c)/math.log(af))
                q1=cmath.exp(2j*math.pi*cmath.log(af*x+bf+1j+c)/math.log(af))
                close('affine_seam_periodicity_float',q0,q1)
                theta=cmath.phase(x+c)
                close('affine_radius_float',abs(q0),math.exp(-2*math.pi*theta/math.log(af)))
                check('affine_radius_inside',0<abs(q0)<1)
    for b in [0.,.25,1.,4.]:
        d=b+1j
        for x in [.1,1.,3.]:
            for y in [0.,.25,.75,1.]:
                z=x+1j*y
                q=cmath.exp(2j*math.pi*z/d)
                close('translation_periodicity_float',q,cmath.exp(2j*math.pi*(z+d)/d))
                close('translation_radius_float',math.log(abs(q)),2*math.pi*(x-b*y)/(1+b*b))
    # Exact triangular interpolation controls and an exact PSD norm bound.
    for m,M,B in [(F(1,3),F(3),F(2)),(F(1),F(2),F(1)),(F(1,8),F(5,4),F(1,4))]:
        m0,M0=min(F(1),m),max(F(1),M)
        C=M0*M0+B*B+1
        for hp in [m,(m+M)/2,M]:
            for y in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
                p=1-y+y*hp
                for q in [-B,F(0),B]:
                    # C I-A^T A is positive semidefinite by these minors.
                    u=C-p*p; v=-p*q; w=C-q*q-1
                    check('qc_jacobian_bounds',m0<=p<=M0)
                    check('qc_norm_psd',u>=0 and w>=0 and u*w-v*v>=0)
                    check('qc_bound', (p*p+q*q+1)/p<=C/m0)
    # The first 32 windows of the infinite distortion construction, exact.
    for n in range(1,33):
        t=F(3*n); ell=1/(100*(1+t)**2); s=F(1,2**n)
        hleft=t-ell; hmid=t-ell+s*ell; hright=hmid+(2-s)*ell
        check('pl_endpoint_gluing',hright==t+ell)
        check('pl_positive_slopes',0<s<=1 and 2-s>0)
        check('pl_displacement',abs(hmid-t)==(1-s)*ell<ell)
        check('pl_fine_tolerance_example',ell<4/(t+3)**2)
        check('pl_adjacent_ratio',(hright-hmid)/(hmid-hleft)==(2-s)/s)
        y=1-s/2; p=1-y+y*s
        check('pl_interpolation_lower_bound',p<2*s and 1/p>1/(2*s))
    # Invariant-density normalization and geometric series, exact.
    # Integral_0^1 6v(1-v) dv and its square.
    check('density_integral',6*(F(1,2)-F(1,3))==1)
    check('density_square_integral',36*(F(1,3)-2*F(1,4)+F(1,5))==F(6,5))
    for a in [F(5,4),F(3,2),F(2),F(4)]:
        for b in [F(0),F(1,3)]:
            c=F(2); L=a*c+b-c
            x=c
            for n in range(17):
                expected=a**n*c+b*(a**n-1)/(a-1)
                check('affine_iterates',x==expected)
                check('orbit_escape_formula',x-c==L*(a**n-1)/(a-1))
                total=sum((a**(-j) for j in range(n+1)),F(0))
                tail=a**(-n)/(a-1)
                check('geometric_sum_plus_exact_tail',total+tail==a/(a-1))
                x=a*x+b
            check('density_energy_formula',F(6,5)/L*a/(a-1)==6*a/(5*L*(a-1)))
    for a in [F(5,4),F(2),F(4)]:
        for b in [F(0),F(1,3)]:
            for R in [F(1),F(10),F(100)]:
                cc=(a-1)*R+b
                check('tail_surgery_continuity',a*R+b==R+cc)
                check('tail_surgery_translation_positive',cc>=0)
                for x in [R/4,R/2,R]:
                    beta_R=(a*x+b) if x<=R else (x+cc)
                    alpha=a*x+b
                    check('tail_surgery_compact_agreement',beta_R==alpha)
                for x in [R+1,R+10]:
                    beta_R=(a*x+b) if x<=R else (x+cc)
                    check('tail_surgery_tail_formula',beta_R-x==cc)
                x=R+2/(a-1)
                check('tail_surgery_fails_constant_tube',abs((a*x+b)-(x+cc))==2)
    # Exponential compactification and tolerance ratio: finite float samples.
    for a in [.5,1.,2.,3.]:
        for x in [.1,.5,1.,2.]:
            r=math.exp(-2*math.pi*x)
            tau=math.exp(-2*math.pi*a*x)
            close('compactification_power_float',tau,r**a)
            for e in [.01,.1,.5]:
                beta=a*x+e/2
                ratio=math.exp(-2*math.pi*beta)/tau
                close('compactification_ratio_float',ratio,math.exp(-math.pi*e))
                check('compactification_tube',math.exp(-2*math.pi*e)<ratio<math.exp(2*math.pi*e))
    for x in [.25,1.,2.]:
        r=math.exp(-2*math.pi*x)
        close('midline_fixed_side_float',cmath.exp(-2*math.pi*(x+.5j)),-r)
        check('lower_half_sign',cmath.exp(-2*math.pi*(x+.25j)).imag<0)
        check('upper_half_sign',cmath.exp(-2*math.pi*(x+.75j)).imag>0)
    result={
        'status':'PASS', 'assertions':sum(COUNTS.values()),
        'counts':COUNTS,'maximum_relative_errors':MAXERR,
        'limits':[
            'Finite algebraic and floating-point controls only; infinite end type is proved in PROOF.md, not inferred from samples.',
            'Float tolerance is 2e-11 relative to max(1, magnitudes); floats are diagnostic, not interval-certified.',
            'Only 32 distortion windows and 17 affine iterates are evaluated; arbitrary n claims use the displayed formulas.',
            'No computation constructs a parabolic sewing within every fine tolerance.',
            'No formal proof assistant verification or numerical conformal-welding solver is claimed.'
        ]
    }
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
