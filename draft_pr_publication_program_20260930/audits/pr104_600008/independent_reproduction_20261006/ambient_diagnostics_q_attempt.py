#!/usr/bin/env python3
"""Finite diagnostics from the ambient embedding; no global-proof claim.

The ODE uses ordinary longitude phi and normalized ambient latitude q.
It does not use t,v, the proposed conformal metric, or a period-identity
formula to compute trajectories. Those formulas are only comparators.
"""
from pathlib import Path
from fractions import Fraction
from math import sin, cos, sqrt, atan2, pi, floor, gcd, lcm
import json, sys
import sympy as S
import mpmath as mp

ROOT = Path(__file__).resolve().parent
checks = {}
def check(name, value):
    if not bool(value): raise RuntimeError(name)
    checks[name] = checks.get(name, 0) + 1

# Start with direct differentiated ambient coordinates, including all signs.
a,b,c = S.symbols('a b c', positive=True)
phi,lam = S.symbols('phi lam', real=True)
xyz = [S.sqrt(a)*S.cos(lam)*S.cos(phi),
       S.sqrt(b)*S.cos(lam)*S.sin(phi), S.sqrt(c)*S.sin(lam)]
def dot(x,y): return x[0]*y[0]+x[1]*y[1]-x[2]*y[2]
rp = [S.diff(x,phi) for x in xyz]
rl = [S.diff(x,lam) for x in xyz]
f2 = a*S.sin(phi)**2+b*S.cos(phi)**2
h2 = a*S.cos(phi)**2+b*S.sin(phi)**2
E = S.cos(lam)**2*f2
F = (a-b)*S.sin(phi)*S.cos(phi)*S.sin(lam)*S.cos(lam)
G = h2*S.sin(lam)**2-c*S.cos(lam)**2
check('ambient_longitude_metric', S.trigsimp(dot(rp,rp)-E)==0)
check('ambient_cross_metric', S.trigsimp(dot(rp,rl)-F)==0)
check('ambient_latitude_metric', S.trigsimp(dot(rl,rl)-G)==0)
check('ambient_null_discriminant', S.trigsimp(F**2-E*G-S.cos(lam)**2*(c*f2*S.cos(lam)**2-a*b*S.sin(lam)**2))==0)
normal = xyz[0]**2/a**2+xyz[1]**2/b**2-xyz[2]**2/c**2
check('ambient_belt_normal', S.trigsimp(normal-(S.cos(lam)**2*f2/(a*b)-S.sin(lam)**2/c))==0)

# Explicit finite rational state iteration, rather than assuming parity.
for p,den in [(p,q) for p in range(1,13) for q in range(1,13) if gcd(p,q)==1]:
    pos,boundary = Fraction(0),1
    found = None
    for n in range(1,2*den+1):
        pos += Fraction(p,den)
        boundary *= -1
        closed = pos.denominator==1 and boundary==1
        check('explicit_boundary_parity', closed==(n%2==0 and n%den==0))
        if closed and found is None: found=n
    check('minimal_full_arc_period', found==lcm(2,den))

# Dormand-Prince scalar integrator, with explicit error acceptance.
def integrate(rhs, t0, t1, y0, tol):
    direction = 1 if t1>t0 else -1
    t,y,h=t0,y0,direction*0.015
    accepted=rejected=0
    while direction*(t1-t)>1e-14:
        if accepted+rejected>300000: raise RuntimeError('ODE step limit')
        h=direction*min(abs(h),abs(t1-t),0.035)
        k1=rhs(t,y)
        k2=rhs(t+h/5,y+h*k1/5)
        k3=rhs(t+3*h/10,y+h*(3*k1/40+9*k2/40))
        k4=rhs(t+4*h/5,y+h*(44*k1/45-56*k2/15+32*k3/9))
        k5=rhs(t+8*h/9,y+h*(19372*k1/6561-25360*k2/2187+64448*k3/6561-212*k4/729))
        k6=rhs(t+h,y+h*(9017*k1/3168-355*k2/33+46732*k3/5247+49*k4/176-5103*k5/18656))
        y5=y+h*(35*k1/384+500*k3/1113+125*k4/192-2187*k5/6784+11*k6/84)
        k7=rhs(t+h,y5)
        y4=y+h*(5179*k1/57600+7571*k3/16695+393*k4/640-92097*k5/339200+187*k6/2100+k7/40)
        err=abs(y5-y4)
        target=tol*(1+0.01*abs(y))
        if err<=target:
            t,y=t+h,y5; accepted+=1
        else: rejected+=1
        factor=5 if err==0 else min(5,max(.15,.9*(target/err)**.2))
        h*=factor
        if abs(h)<1e-14: raise RuntimeError('ODE step underflow')
    return y,{'accepted':accepted,'rejected':rejected}

def coefficients(u,phi,axes):
    # q=sin(u), tan(lambda)=q sqrt(c f(phi)^2/(ab)).
    aa,bb,cc=axes
    sp,cp=sin(phi),cos(phi)
    ff=aa*sp*sp+bb*cp*cp
    q=sin(u); cu=cos(u); k=sqrt(cc*ff/(aa*bb)); den=1+(q*k)**2
    cl=1/sqrt(den); sl=q*k*cl
    lp=q*k*(aa-bb)*sp*cp/(ff*den)
    lq=k/den
    natural_p=(-sqrt(aa)*cl*sp,sqrt(bb)*cl*cp,0.)
    natural_l=(-sqrt(aa)*sl*cp,-sqrt(bb)*sl*sp,sqrt(cc)*cl)
    pvec=tuple(natural_p[i]+lp*natural_l[i] for i in range(3))
    qvec=tuple(lq*natural_l[i] for i in range(3))
    ee=dot(pvec,pvec); ff_cross=dot(pvec,qvec); gg=dot(qvec,qvec)
    disc=lq*lq*cc*ff*cu*cu/(den*den)
    return ee,ff_cross,gg,disc,cu
def rhs_for(axes,sign):
    def rhs(u,phi):
        ee,ff,gg,disc,cu=coefficients(u,phi,axes)
        if ee<=0 or not disc>=0: raise RuntimeError('invalid ambient ODE signature')
        return cu*(-ff+sign*sqrt(disc))/ee
    return rhs

mp.mp.dps=50
def period_data(axes):
    aa,bb,cc=map(lambda x:mp.mpf(str(x)),axes)
    density=lambda t:mp.sqrt((aa*mp.sin(t)**2+bb*mp.cos(t)**2)/(cc+aa*mp.sin(t)**2+bb*mp.cos(t)**2))
    L=mp.quad(density,[0,mp.pi/2,mp.pi,3*mp.pi/2,2*mp.pi])
    ivfun=lambda t:2*cc*mp.sin(t)**2/mp.sqrt((aa+cc*mp.sin(t)**2)*(bb+cc*mp.sin(t)**2))
    Iv=mp.quad(ivfun,[0,mp.pi/8,mp.pi/4,3*mp.pi/8,mp.pi/2])
    M=L/(2*mp.pi)
    rho=(1-M)/(2*M)
    def spatial(angle):
        angle=mp.mpf(str(angle)); whole=mp.floor(angle/(2*mp.pi)); rest=angle-whole*2*mp.pi
        points=[mp.mpf(0)]+[x for x in [mp.pi/2,mp.pi,3*mp.pi/2] if x<rest]+[rest]
        return whole*L+mp.quad(density,points)
    return L,Iv,M,rho,spatial
def boundary_t(angle,axes):
    aa,bb,cc=axes
    sc=sin(angle); co=cos(angle); ff=aa*sc*sc+bb*co*co
    cl=1/sqrt(1+cc*ff/(aa*bb))
    t0=atan2(sqrt((bb+cc)/bb)*cl*sc,sqrt((aa+cc)/aa)*cl*co)
    return t0+round((angle-t0)/(2*pi))*2*pi

cases=[('rotation_small_c',(1.,1.,.01)),('rotation_rho_half',(1.,1.,3.)),
       ('rotation_rho_one',(1.,1.,8.)),('rotation_rho_third',(1.,1.,16/9)),
       ('rotation_large_c',(1.,1.,10000.)),('anisotropic',(5.,2.,3.)),
       ('swapped',(2.,5.,3.)),('thin_horizontal_axis',(.001,1.,10.)),
       ('wide_horizontal_axis',(1.,1000.,.001)),('strong_anisotropy',(100.,.01,1000.)),
       ('common_small_scale',(5e-8,2e-8,3e-8))]
results=[]
max_disc_error=0.
for name,axes in cases:
    norm=max(axes); scaled=tuple(x/norm for x in axes)
    for u in [-pi/2,-1.1,-.3,0.,.3,1.1,pi/2]:
        for ph in [0.,.17,1.3,3.4]:
            ee,ff,gg,disc,cu=coefficients(u,ph,scaled)
            relative=abs((ff*ff-ee*gg)-disc)/max(abs(ff*ff),abs(ee*gg),abs(disc),1e-300)
            max_disc_error=max(max_disc_error,relative)
            # At a tropic both quantities vanish and cancellation is expected;
            # use a nonzero fixed metric scale for that diagnostic.
            check('ambient_metric_discriminant_numeric',abs((ff*ff-ee*gg)-disc)<=2e-10*max(ee*abs(gg),ff*ff,1.))
    L,Iv,M,rho,spatial=period_data(axes)
    identity_error=abs(Iv+L/2-mp.pi)
    check('period_identity_numerical',identity_error<mp.mpf('1e-35'))
    starts=[.123] if name.startswith('rotation') else [-.37,1.234]
    flows=[]
    for phi0 in starts:
        outputs=[]
        for tol in [2e-9,2e-11]:
            north,nstats=integrate(rhs_for(scaled,1),0,pi/2,phi0,tol)
            eq,estats=integrate(rhs_for(scaled,-1),pi/2,0,north,tol)
            south,sstats=integrate(rhs_for(scaled,-1),pi/2,-pi/2,north,tol)
            north2,n2stats=integrate(rhs_for(scaled,1),-pi/2,pi/2,south,tol)
            s0=spatial(phi0); sn=spatial(boundary_t(north,axes)); se=spatial(eq)
            ss=spatial(boundary_t(south,axes)); sn2=spatial(boundary_t(north2,axes))
            errors={'equator_to_north':float(abs((sn-s0)/L-rho/2)),
                    'equator_return':float(abs((se-s0)/L-rho)),
                    'full_north_to_south':float(abs((ss-sn)/L-rho)),
                    'full_south_to_north':float(abs((sn2-ss)/L-rho))}
            outputs.append({'tol':tol,'north_phi':north,'returned_equator_phi':eq,
                            'south_phi':south,'second_north_phi':north2,
                            'rotation_errors':errors,'step_counts':[nstats,estats,sstats,n2stats]})
        tight=outputs[-1]
        error=max(tight['rotation_errors'].values())
        check('direct_null_flow_rotation',error<2e-7)
        difference=max(abs(tight[k]-outputs[0][k]) for k in ['north_phi','returned_equator_phi','south_phi','second_north_phi'])
        check('direct_flow_tolerance_refinement',difference<2e-5)
        flows.append({'initial_phi':phi0,'runs':outputs,'longitude_refinement_difference':difference})
    results.append({'name':name,'axes':axes,'M':str(M),'rho':str(rho),
                    'period_identity_absolute_error':str(identity_error),'flows':flows})

# Real trajectory minimality at two rational rotational test parameters.
rational_orbits=[]
for target,cval in [(Fraction(1,2),3.),(Fraction(1),8.),(Fraction(1,3),16/9)]:
    axes=(1.,1.,cval); norm=max(axes); scaled=tuple(x/norm for x in axes)
    phi0=.123; state=phi0; visits=[]
    for step in range(1,lcm(2,target.denominator)+1):
        increasing=step%2==0
        u0,u1=(-pi/2,pi/2) if increasing else (pi/2,-pi/2)
        state,stats=integrate(rhs_for(scaled,1 if increasing else -1),u0,u1,state,2e-11)
        winding=(state-phi0)/(2*pi)
        residual=abs(winding-round(winding))
        physically_closed=(step%2==0 and residual<2e-7)
        check('numerical_rotational_minimality',physically_closed==(step==lcm(2,target.denominator)))
        visits.append({'step':step,'boundary':'north' if step%2==0 else 'south',
                       'lifted_winding':winding,'integer_winding_residual':residual,
                       'physically_closed':physically_closed})
    rational_orbits.append({'rho':str(target),'visits':visits})

out={'status':'PASS','python':sys.version,'sympy':S.__version__,'mpmath':mp.__version__,
     'exact_and_finite_check_counts':checks,'case_count':len(cases),
     'initial_flow_count':sum(len(x['flows']) for x in results),
     'maximum_rotation_error':max(e for x in results for f in x['flows'] for e in f['runs'][-1]['rotation_errors'].values()),
     'metric_discriminant_relative_error_note':'Relative error is ill conditioned at exact zero; checks use a fixed nonzero metric scale.',
     'cases':results,'rational_boundary_orbits':rational_orbits,
     'scope':'Finite ambient-embedding null ODE and high precision quadrature diagnostics; global validity still requires the written geometric and contour arguments.'}
(ROOT/'DIAGNOSTICS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
