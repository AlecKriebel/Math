#!/usr/bin/env python3
"""Independent exact support checks, not a proof of the analytic PDE claims.
Optional fixture values alter mathematical data; invalid certificates must fail.
Only the standard library is used. No writes, network, assert, or source bodies.
"""
import argparse
from fractions import Fraction as F
import json
import sys


def require(value, label):
    if not value:
        raise ValueError(label)


def tv(xs):
    return sum((abs(xs[(j+1) % len(xs)]-x) for j,x in enumerate(xs)), F(0))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--fixture')
    args=ap.parse_args()
    cfg={'scheme_sign':'1','H_linear_coefficient':'2','alpha_delta_ratio':'1/2',
         'pulse_final_ratio':'1','entropy_cross_sign':'1','up_speed_sign':'-1',
         'down_speed_factor':'-2','contact_velocity_sign':'-1'}
    if args.fixture:
        with open(args.fixture,encoding='utf8') as f:
            supplied=json.load(f)
        require(isinstance(supplied,dict),'fixture must be an object')
        require(set(supplied)<=set(cfg),'unknown fixture field')
        cfg.update(supplied)
    p={k:F(v) for k,v in cfg.items()}
    results={}

    # (12)-(16): heterogeneous frozen parameter and genuinely concave velocity.
    f=lambda u:F(u)-F(u)**2/20
    ks=[F(2),F(9,4),F(5,2),F(11,4),F(3)]
    zs=[2-f(k) for k in ks]
    perturb=[F(1,16),F(-1,16),F(1,32),F(-1,32),F(0)]
    us=[k+d for k,d in zip(ks,perturb)]
    vs=[f(u)+z for u,z in zip(us,zs)]
    lam=F(1,2)
    new=[u+p['scheme_sign']*lam*(vs[(j+1)%len(vs)]-vs[j]) for j,u in enumerate(us)]
    vnew=[f(u)+z for u,z in zip(new,zs)]
    require(all(min(vs)<=v<=max(vs) for v in vnew),'route1 velocity maximum principle')
    require(tv(vnew)<=tv(vs),'route1 velocity TVD')
    require(sum(map(abs,(a-b for a,b in zip(new,us))))<=lam*tv(vs),
            'route1 exact L1 time estimate')
    for j in range(len(us)):
        rhs=abs(us[j]-ks[j])+lam*(abs(vs[(j+1)%len(vs)]-2)-abs(vs[j]-2))
        require(abs(new[j]-ks[j])<=rhs,'route1 adapted entropy inequality')
    # Mean-value coefficients and difference recurrence, including zero jumps.
    aa=[]
    for j,u in enumerate(us):
        dv=vs[(j+1)%len(vs)]-vs[j]
        aa.append((vnew[j]-vs[j])/dv if dv else lam*(1-u/10))
    require(all(0<=a<=1 for a in aa),'route1 CFL coefficient interval')
    for j in range(len(us)):
        j1=(j+1)%len(us); j2=(j+2)%len(us)
        require(vnew[j1]-vnew[j]==(1-aa[j])*(vs[j1]-vs[j])+aa[j1]*(vs[j2]-vs[j1]),
                'route1 velocity-difference recurrence')
    results['route1']={'initial_velocity_TV':str(tv(vs)),
                       'updated_velocity_TV':str(tv(vnew)),'cells':len(us)}

    # (21)-(23): exact root certificates and feasibility, never square-root floats.
    rows=[]
    for k in range(4,20):
        delta=F(1,2**k); alpha=p['alpha_delta_ratio']*delta
        require(0<alpha<delta-delta*delta/4,'route2 right scanning feasibility')
        g=lambda h:p['H_linear_coefficient']*h-h*h/4-alpha
        require(g(alpha/2)<0<g(alpha),'route2 transmitted root bracket')
        # If D^2=4-alpha and H=4-2D, polynomial g(H) must be identically zero.
        # After reducing D^2, coefficients in basis (1,D) are these rationals.
        constant=4*p['H_linear_coefficient']-8
        coeff_D=4-2*p['H_linear_coefficient']
        require(constant==0 and coeff_D==0,'route2 closed-form polynomial identity')
        # On (alpha/2, alpha) g'=2-H/2>0, giving unique small root H.
        require(2-alpha/2>0,'route2 unique small root derivative')
        rshift=lambda y:y-y*y/4-alpha
        require(rshift(0)<0<rshift(delta),'route2 incoming root interval')
        # Exact expansion residual for H_2=alpha/2+alpha^2/32.
        h2=alpha/2+alpha*alpha/32
        require(g(h2)==-alpha**3/128-alpha**4/4096,'route2 quadratic expansion')
        lo=alpha/2; hi=alpha
        for _ in range(60):
            mid=(lo+hi)/2
            if g(mid)<0: lo=mid
            else: hi=mid
        require(g(lo)<=0<=g(hi),'route2 exact bisection certificate')
        require(lo/(alpha*delta)>1/(2*delta),'route2 first-order amplification')
        rows.append({'delta':str(delta),'alpha':str(alpha),
                     'H_lower':str(lo),'H_upper':str(hi),
                     'ratio_lower_bound':str(1/(2*delta))})
    results['route2']={'exact_rational_root_brackets':rows}

    # (25)-(26): path projection and retained memory, not a PDE solution check.
    e=F(1,8); ulevels=[F(0),e,F(0)]; memory=F(0); hs=[]
    for u in ulevels:
        memory=max(u,min(memory,u+1)); hs.append(memory)
    reported_final=e*p['pulse_final_ratio']
    require(reported_final==hs[-1],'route3 retained memory at pulse return')
    require(hs==[0,e,e],'route3 projection path')
    require(hs[-1]!=ulevels[-1],'route3 limiting positive-jump endpoint fails')
    require(sum(abs(a-b) for a,b in zip(ulevels,ulevels[1:]))==2*e,'route3 input TV')
    require(sum(abs(a-b) for a,b in zip(hs,hs[1:]))==e,'route3 memory TV')
    results['route3']={'input_levels':list(map(str,ulevels)),
                       'memory_levels':list(map(str,hs)),
                       'PDE_solution_claim':False}

    # (27)-(31): exact algebra in V=u+h, eta_uu=1 chart, plus general sign logic.
    V_u=F(1); V_h=F(1); eta_uu=F(1); eta_uh=p['entropy_cross_sign']
    require(V_u*eta_uh==V_h*eta_uu,'route4 mixed-derivative identity')
    width=F(1); boundary_eta_h_difference=eta_uh*width
    require(boundary_eta_h_difference>0,'route4 strict positive entropy boundary difference')
    # Required boundary signs would force the same difference <=0.
    results['route4']={'forced_positive_difference':str(boundary_eta_h_difference),
                       'required_nonpositive_difference_incompatible':True,
                       'general_proof_location':'AUDIT_REPORT.md'}

    # (32)-(36): exact model, Rankine-Hugoniot, chord signs, and sums.
    rows=[]
    for N in (1,2,4,8,16,32):
        es=[F(1,2**(n+6)) for n in range(N)]
        mass=F(0)
        for e in es:
            dv=f(2+e)-f(2)
            require(isinstance(dv,F),'route5 rational arithmetic type')
            require(dv==F(4,5)*e-e*e/20,'route5 velocity increment polynomial')
            sup=p['up_speed_sign']*dv/(F(1,2)+e)
            sdown=p['down_speed_factor']*dv
            require(sup*(F(1,2)+e)+dv==0,'route5 increasing-edge Rankine-Hugoniot')
            require(sdown*(-F(1,2))-dv==0,'route5 decreasing-edge Rankine-Hugoniot')
            require(F(-1,4)<sdown<sup<0,'route5 front speed order and separation')
            chord_slope=dv/(F(1,2)+e)
            require(chord_slope<F(4,5)-e/10,'route5 increasing chord derivative certificate')
            require(dv*(1-2*e)>0,'route5 decreasing chord endpoint certificate')
            # On deceleration segment u=2+r, gap f(2+r)-[f(2)+2dv*r]
            # is r*(4/5-r/20-2dv), positive throughout 0<r<=e.
            require(F(4,5)-e/20-2*dv>0,'route5 decreasing chord coefficient certificate')
            mass+=2*dv
        rows.append({'N':N,'initial_TV':str(2*sum(es,F(0))),
                     'spacing_TV':str(2*N+2*sum(es,F(0))),
                     'spacing_L1_at_t1':str(mass)})
    esum=F(1,64)/(1-F(1,2)); e2sum=F(1,64)**2/(1-F(1,4))
    total_mass=2*(F(4,5)*esum-e2sum/20)
    require(2*esum==F(1,16),'route5 countable initial TV')
    require(total_mass==F(307,6144),'route5 countable L1 total')
    results['route5']={'finite_pulses':rows,'countable_initial_TV':str(2*esum),
                       'countable_spacing_L1_at_t1':str(total_mass),
                       'time_interval':'0<t<=1','full_source_counterexample':False}

    # Stationary B=1 profile equation u'=v0-f(h), at exact interior test states.
    profile_rows=[]
    for kind,u,h0,h in [('high',F(11,4)+F(1,128),2+F(1,64),2+F(1,64)+F(1,256)),
                        ('low',F(9,4),F(2),F(2)-F(1,256))]:
        v0=f(h0)
        slope=(f(h)-v0)/p['contact_velocity_sign']
        residual=slope+f(h)-v0
        require(residual==0,'stationary contact viscosity equation')
        require(u-1<h<u,'stationary contact physical strip')
        require((slope<0 and h>h0) if kind=='high' else (slope>0 and h<h0),
                'stationary contact excursion direction')
        profile_rows.append({'contact':kind,'u':str(u),'h':str(h),'u_prime':str(slope)})
    results['stationary_contact']={'exact_interior_equation_checks':profile_rows,
                                   'full_profile_proof':'AUDIT_REPORT.md'}
    print(json.dumps({'status':'all independent exact support checks passed','checks':results},indent=2))
    return 0


if __name__=='__main__':
    try:
        sys.exit(main())
    except (ValueError,TypeError,KeyError) as e:
        print('verification failed: '+str(e),file=sys.stderr)
        sys.exit(1)
