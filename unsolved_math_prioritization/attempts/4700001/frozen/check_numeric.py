#!/usr/bin/env python3
"""Non-validated exploratory ODE checks. No output is an exclusion proof."""
import json,math,sys
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
T=2*math.pi

def flow(p,r0,tol=2e-11):
    a,b,c,d,e=p
    def f(t,y):
        r=y[0]; co=math.cos(t); si=math.sin(t)
        B=b*co+c*si; C=d*co*co+e*co*si
        return [a*r+B*r*r+C*r**3, a+2*B*r+3*C*r*r]
    def stop(t,y): return 100-abs(y[0])
    stop.terminal=True
    out=solve_ivp(f,(0,T),[r0,0.],method='DOP853',rtol=tol,atol=tol*.02,max_step=.06,events=stop)
    if not out.success or out.t[-1]<T: return None
    return {'delta':float(out.y[0,-1]-r0),'log_multiplier':float(out.y[1,-1])}

def roots_on_grid(p,grid,tol=2e-11):
    vals=[flow(p,float(x),tol) for x in grid]; roots=[]
    for i in range(len(grid)-1):
        l,h=vals[i:i+2]
        if l is None or h is None: continue
        if l['delta']*h['delta']<0:
            rt=brentq(lambda r:flow(p,r,tol)['delta'],grid[i],grid[i+1],xtol=2e-12)
            if not roots or abs(rt-roots[-1]['radius'])>1e-7:
                roots.append({'radius':float(rt),**flow(p,rt,tol)})
    return {'parameters_abcde':list(map(float,p)),'radii':list(map(float,grid)), 'samples':vals,'bracketed_roots':roots,
            'incomplete_flows':sum(x is None for x in vals)}

center=[0,1,1,0,0]
center_samples=[flow(center,x) for x in [.03,.07,.13]]
assert max(abs(x['delta']) for x in center_samples)<1e-10
one=[.1,0,0,-1,.5]
a,b,c,d,e=one
z0=-d/(2*a)+(e-a*d)/(2*(1+a*a)); exact=1/math.sqrt(z0)
v=flow(one,exact)
assert abs(v['delta'])<1e-10 and abs(v['log_multiplier']+4*math.pi*a)<1e-9
# Equality |d|=|a e| is a zero of the reciprocal-square radius, not a finite cycle.
a0,d0,e0=.5,-1,2
A0=-d0/(2*a0); amp=math.sqrt(d0*d0+e0*e0)/(2*math.sqrt(1+a0*a0))
assert abs(A0-amp)<1e-14
family=[]
for eps in [.12,.10,.07]:
    p=[-eps**4/2,1,1,2*eps**2,1]
    grid=np.linspace(.30*eps,2.5*eps,65)
    case=roots_on_grid(p,grid)
    assert len(case['bracketed_roots'])==2
    rr=case['bracketed_roots']; assert rr[0]['log_multiplier']>0>rr[1]['log_multiplier']
    case['epsilon']=eps
    case['refined_roots']=roots_on_grid(p,grid,2e-13)['bracketed_roots']
    assert max(abs(x['radius']-y['radius']) for x,y in zip(rr,case['refined_roots']))<1e-7
    family.append(case)
# Reproducible bounded probe; it cannot find tangencies or rule out distant cycles.
rng=np.random.default_rng(4700001)
scan=[]
for _ in range(24):
    a=rng.uniform(-.4,.4); b,c=rng.uniform(-2,2,2); d=rng.uniform(-1,1); e=rng.choice([-1,1])*rng.uniform(.1,2)
    scan.append(roots_on_grid([a,b,c,d,e],np.geomspace(.005,5,31)))
result={'notice':'Floating-point evidence only; missing/incomplete flows and unbracketed/tangent roots remain unresolved.',
 'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__,
 'controls':{'center':center_samples,'homogeneous_parameters':one,'exact_homogeneous_radius':exact,'homogeneous_flow':v,'boundary_reciprocal_minimum':A0-amp},
 'two_cycle_family':family,'bounded_scan':scan,
 'scan_summary':{'parameter_count':len(scan),'radii_per_parameter':31,'maximum_bracketed_roots':max(len(x['bracketed_roots']) for x in scan),'incomplete_flows':sum(x['incomplete_flows'] for x in scan)}}
print(json.dumps(result,indent=2))
