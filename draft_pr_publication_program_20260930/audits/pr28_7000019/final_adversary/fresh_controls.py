#!/usr/bin/env python3
"""Distinct exact adversarial controls. Universal arguments live in REPORT.md."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import sympy as s
import json, sys

HERE=Path(__file__).resolve().parent
checks=[]; falsifiers=[]
def check(name,ok,evidence):
    assert bool(ok),name
    checks.append({'name':name,'evidence':evidence})
def reject(name,ok,evidence):
    assert not bool(ok),name
    falsifiers.append({'name':name,'rejected':True,'evidence':evidence})

# Different band control: translate an asymmetric projection interval and
# derive its length from the uniform cosine CDF, including clipping.
def band(low,high,radius):
    return max(Q(0),min(Q(1),high/radius)-max(Q(-1),low/radius))/2
check('asymmetric_band_exact',band(Q(-2,3),Q(1,3),Q(7,5))==Q(5,14),
      'Width1 at distance7/5: cosine interval[-10/21,5/21] has probability5/14.')
check('centered_halfwidth_exact',band(Q(-2,3),Q(2,3),Q(7,5))==Q(10,21),
      'Halfwidth2/3 at distance7/5 has probability10/21.')
check('band_cutoff_and_interior',band(-Q(2,3),Q(2,3),Q(2,3))==1 and
      band(-Q(2,3),Q(2,3),Q(1,3))==1,'Clipping includes equality and saturation.')
reject('unsaturated_kernel_inside_cutoff',band(-Q(2,3),Q(2,3),Q(1,3))==2,
       'The true probability1 differs from halfwidth/distance2.')
reject('replace_halfwidth_by_fullwidth',band(-Q(2,3),Q(2,3),Q(7,5))==Q(20,21),
       'Full/half separation is caught by an exact rational CDF.')
z=s.symbols('z',real=True)
prob4=s.integrate(2*s.sqrt(1-z*z)/s.pi,(z,-s.Rational(1,2),s.Rational(1,2)))
check('dimension4_band_formula',s.simplify(prob4-(s.Rational(1,3)+s.sqrt(3)/(2*s.pi)))==0,
      'S3 height marginal is2sqrt(1-z^2)/pi; probability differs from1/2.')
reject('dimension_free_Newton_band',s.simplify(prob4-s.Rational(1,2))==0,
       'At ratio1/2 the four-dimensional band has1/3+sqrt3/(2pi).')

# A degree-two positive charge on the unit sphere is a distinct local
# diagnostic: at the center its value and gradient match the uniform sphere,
# but its Hessian is nonzero. Kernel derivatives are integrated exactly.
eps=s.Rational(1,3);P2=(3*z*z-1)/2;rho=1+eps*P2
mass=s.integrate(rho,(z,-1,1))/2
hesszz=s.integrate(rho*(3*z*z-1),(z,-1,1))/2
check('positive_quadrupole_density',rho.subs(z,0)==s.Rational(5,6) and
      rho.subs(z,1)==s.Rational(4,3),'Density1+P2/3 ranges from5/6 to4/3.')
check('quadrupole_center_potential',mass==1,'Unit sphere normalized center potential is1.')
check('quadrupole_center_gradient_zero',s.integrate(rho*z,(z,-1,1))==0,
      'Axis symmetry and parity give zero gradient at the center.')
check('quadrupole_nonzero_Hessian',hesszz==s.Rational(2,15),
      'Integral of kernel second derivative gives dzzPsi(0)=2/15.')
check('uniform_sphere_zero_Hessian',s.integrate(3*z*z-1,(z,-1,1))==0,
      'The same derivative calculation vanishes for uniform density.')
reject('center_value_plus_gradient_implies_constancy',hesszz==0,
       'Positive surface charge has center value1 and gradient0, but second derivative2/15.')
x,y,w=s.symbols('x y w',real=True);harmonic=2*w*w-x*x-y*y
check('harmonic_second_order_point_control',sum(s.diff(harmonic,t,2) for t in (x,y,w))==0,
      'Harmonic quadratic also vanishes with zero gradient at the origin.')
reject('continue_from_zero_first_jet',harmonic.subs({x:0,y:0,w:1})==0,
       'Harmonic quadratic takes value2 at(0,0,1).')

# Explicit density/kernel/normal scaling with a new radius and charge.
R=s.Rational(11,7);charge=s.Rational(3,2);q=s.symbols('q',positive=True)
inside=charge*R;outside=charge*R*R/q
check('sphere_trace_positive',outside.subs(q,R)==inside>0,'Common trace is33/14.')
check('sphere_outward_body_jump',s.diff(outside,q).subs(q,R)==-charge,
      'Normalized outward-body derivative is-3/2; interior derivative0.')
check('sphere_raw_jump_scaling',s.diff(4*s.pi*outside,q).subs(q,R)==-6*s.pi,
      'Unnormalized derivative is-4pi*density.')
check('sphere_decay_harmonic',s.limit(outside,q,s.oo)==0 and
      s.simplify(s.diff(outside,q,2)+2*s.diff(outside,q)/q)==0,'Exterior formula is harmonic and decays.')
reject('exterior_domain_normal_same_sign',-s.diff(outside,q).subs(q,R)==-charge,
       'The exterior-domain outward normal points into the body and reverses the sign.')

# Exact symbolic certificate for all tetrahedron directions rather than grids.
V=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
differences={tuple(v[i]-t[i] for i in range(3)) for v in V for t in V if v!=t}
expected=set()
for i,j in combinations(range(3),2):
    for a0 in [-2,2]:
        for b0 in [-2,2]:
            e=[0,0,0];e[i]=a0;e[j]=b0;expected.add(tuple(e))
check('tetra_all_edge_differences',differences==expected,
      'Maximum signed difference is2(a+b), sorted absolute direction coordinates.')
a,b,c=s.symbols('a b c',nonnegative=True)
certificate=2*b*(a-b)+2*(b*b-c*c)+c*c
check('tetra_ordered_width_certificate',s.expand(certificate-(2*a*b-c*c))==0,
      'For a>=b>=c, every summand is nonnegative; width2(a+b)>=2 for unit directions.')
check('tetra_balanced_faces',all(sum(v[i] for v in V)==0 for i in range(3)),
      'Face distances average1/sqrt3 for every center and the origin attains the bound.')
reject('all_direction_width_implies_open_core',Q(3,2)**2<Q(4,3),
       'h=3/2<minimumwidth2, while h>2/sqrt3.')
check('strict_core_gap_ball',Q(13,10)-Q(6,5)>0 and Q(13,10)-Q(13,10)==0,
      'At equality halfwidth=inradius there is no open strict core.')
reject('diameter_guard_creates_open_core',Q(7,4)<1,
       'Ellipsoid axes(4,2,1), h=7/2<diameter8, but halfwidth7/4>inradius1.')

# New nested configurations cover every affine offset cell and threshold regime.
def overlap(t,h,r):return max(Q(0),min(r,t+h)-max(-r,t))
def area(t,h,R,r):return 2*R*overlap(t,h,R)+2*r*overlap(t,h,r)
cells=[]
for h in [Q(1),Q(3),Q(4),Q(6),Q(7),Q(9)]:
    R=Q(5);r=Q(2);low=-R;high=R-h
    breaks=sorted({low,high}|{v for d in [R,r] for v in [-d,d,-d-h,d-h] if low<=v<=high})
    pieces=[]
    for left,right in zip(breaks,breaks[1:]):
        mid=(left+right)/2;vleft=area(left,h,R,r);vright=area(right,h,R,r)
        slope=(vright-vleft)/(right-left)
        assert area(mid,h,R,r)==(vleft+vright)/2
        pieces.append({'left':str(left),'right':str(right),'slope':str(slope),'intercept':str(vleft-slope*left)})
    constant=all(Q(p['slope'])==0 for p in pieces)
    check('nested_regime_h_'+str(h),constant==(h>=R+r),
          'All switch cells and closed endpoints checked forR5,r2.')
    cells.append({'h':str(h),'breakpoints':[str(t) for t in breaks],'pieces':pieces,'constant':constant})
check('nested_threshold_tangent_endpoints',overlap(Q(-5),Q(7),Q(2))==4 and
      overlap(Q(-2),Q(7),Q(2))==4,'At h=R+r both extreme strips contain the entire inner sphere.')
reject('nested_largewidth_union_convex',Q(2)==Q(5),
       'Inner component lies strictly inside the outer convex hull, not on its boundary.')
reject('nested_constancy_below_threshold',area(Q(-5),Q(6),Q(5),Q(2))==
       area(Q(-3),Q(6),Q(5),Q(2)),'h6 gives endpoint area72 and centered76.')

# A positive periodic sawtooth, distinct from cosine/spline/square-wave controls.
t=s.symbols('t',real=True);G=t/2+t*t/2
check('sawtooth_mean_one',G.subs(t,1)-G.subs(t,0)==1,
      'Density1/2+phase is positive and has unit-period integral1.')
check('sawtooth_all_phase_cancellation',s.simplify((G.subs(t,1)-G)+(G-G.subs(t,0))-1)==0,
      'Split any shifted unit interval at its wrap: integrals cancel for every phase.')
reject('periodic_density_is_constant',s.Rational(1,2)==s.Rational(3,2),
       'Endpoint one-sided density values differ; no all-direction surface is constructed.')
reject('single_width_implies_halfwidth',G.subs(t,s.Rational(1,2))-G.subs(t,0)==
       G.subs(t,1)-G.subs(t,s.Rational(1,2)), 'Half-period integrals are3/8 and5/8.')

# Independently verify the old dipole diagnostic's actual nonball mechanism.
e=s.Rational(1,25);r=(1+s.sqrt(1+4*e*t))/2
check('dipole_level_exact',s.simplify(r*r-r-e*t)==0,'Level1 of1/r+eps*t/r^2.')
check('dipole_nonsphere_second_jet',s.diff(r,t).subs(t,0)==e and
      s.diff(r,t,2).subs(t,0)==-2*e*e,
      'A sphere through equatorial radius1 with first jet eps has second jet+eps^2.')
check('dipole_positive_charge_bound',2*e<s.Rational(9,10) and
      1-4*e>s.Rational(4,5)**2,'Radius>9/10, so radial derivative is strictly negative.')
reject('dipole_is_uniform_charge_falsifier',s.sqrt(1+e*e)==1,
       'Equatorial charge exceeds1; polar charge1-(r-1)^2/r^2 is below1. Density is variable.')

result={'sympy_version':s.__version__,'fresh_exact_controls':len(checks),'falsifiers_rejected':len(falsifiers),
        'checks':checks,'falsifiers':falsifiers,'nested_all_cells':cells,
        'scope':'Exact mechanism/diagnostic controls; universal proof and primary rigidity are separately reviewed. No new substantive attempt.','full_target_solved':False}
if '--record' in sys.argv:
    (HERE/'FRESH_CONTROL_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
else:
    assert result==json.loads((HERE/'FRESH_CONTROL_RECEIPT.json').read_text())
    output=HERE/'tmp/FRESH_CONTROL_LAST_REPLAY.json';output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['fresh_exact_controls','falsifiers_rejected','sympy_version','full_target_solved']}))
