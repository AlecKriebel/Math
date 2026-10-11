#!/usr/bin/env python3
"""Finite numerical controls for PROOFS.md; not a replacement for its proofs.
Requires Python 3 and mpmath 1.3.0. Default compares with checked-in results.
Use --write only to regenerate CHECK_RESULTS.json intentionally.
"""
import json
import sys
from pathlib import Path
import mpmath as mp

mp.mp.dps = 60
ROOT = Path(__file__).resolve().parent

def check(condition, message):
    if not condition:
        raise RuntimeError(message)

def close(a, b, tol=mp.mpf('1e-45')):
    return abs(a-b) <= tol * max(1, abs(a), abs(b))

def fmt(x):
    return mp.nstr(x, 32)

def d(n):
    return 2*mp.gamma(mp.mpf(n)/2)/(mp.sqrt(mp.pi)*mp.gamma(mp.mpf(n-1)/2))

def C(n):
    return mp.exp((mp.digamma(mp.mpf(n)/2)-mp.digamma(mp.mpf(1)/2))/2)

def entropy_cost(n, t):
    # Substitution z=t*x in the exact small-ball entropy integral.
    return t*d(n)*mp.quad(lambda x: -mp.log(x)*(1+t*t*x*x)**(-mp.mpf(n)/2), [0, 1])

def R(s,t):
    return t**(-s)*mp.atan(t)/mp.atan(1/t)

def bisect(f, lo, hi):
    flo=f(lo); fhi=f(hi)
    check(flo*fhi<=0, 'Bisection interval does not bracket a root')
    for _ in range(220):
        mid=(lo+hi)/2; fm=f(mid)
        if flo*fm<=0:
            hi=mid
        else:
            lo=mid; flo=fm
    return (lo+hi)/2

def run():
    check(close(C(2),2), 'C_2 normalization failed')
    check(close(C(3),mp.e), 'C_3 normalization failed')
    check(close(C(4),2*mp.sqrt(mp.e)), 'C_4 normalization failed')
    for n,want in [(2,2/mp.pi),(3,mp.mpf(1)),(4,4/mp.pi),(5,mp.mpf('1.5'))]:
        check(close(d(n),want), 'd_n normalization failed')
    rows=[]
    for n in range(2,11):
        t=mp.mpf('1e-6')
        actual=entropy_cost(n,t)/t
        check(abs(actual/d(n)-1)<mp.mpf('1e-11'), 'Entropy first-order control failed')
        rows.append({'n':n,'old_p_minus_one_bound':fmt(1/C(n)),
                     'line_mass_sufficient_bound':fmt(1/(1+d(n))),
                     'entropy_derivative':fmt(d(n))})
    samples=0
    for j in range(-120,121):
        t=mp.exp(mp.mpf(j)/10)
        r=R(mp.mpf(1),t)
        check(2/mp.pi < r < mp.pi/2, 'Strict four-atom interval failed')
        check(close(r*R(1,1/t),1), 'Reciprocity failed')
        # Direct exterior-angle total curvature.
        check(close(4*mp.atan(t)+4*mp.atan(1/t),2*mp.pi), 'Total J mass failed')
        samples += 1
    roots=[]
    for s in [mp.mpf('1.1'),mp.mpf('1.2'),mp.mpf(2),mp.mpf(3)]:
        for ratio in [mp.mpf('0.01'),mp.mpf('0.5'),mp.mpf(1),mp.mpf(2),mp.mpf(100)]:
            z=bisect(lambda x: R(s,mp.exp(x))-ratio,mp.mpf(-1000),mp.mpf(1000))
            check(abs(R(s,mp.exp(z))/ratio-1)<mp.mpf('1e-40'),'Ratio root residual')
            roots.append({'s':fmt(s),'pair_mass_ratio':fmt(ratio),'log_aspect_ratio':fmt(z)})
    s=mp.mpf('1.1')
    zlo=bisect(lambda x:R(s,mp.exp(x))-1,mp.mpf(-20),mp.mpf('-0.01'))
    zhi=bisect(lambda x:R(s,mp.exp(x))-1,mp.mpf('0.01'),mp.mpf(20))
    check(close(zlo,-zhi),'Multiple-solution reciprocity failed')
    check(zlo<0<zhi, 'Three distinct aspect ratios missing')
    # Independent derivative route for the equal-mass family.
    def first(x,s):
        return mp.exp(s*x)/(1+mp.exp(s*x))-(2/mp.pi)*mp.atan(mp.exp(x))
    second=mp.diff(lambda x:first(x,mp.mpf(2)),0)
    check(close(second,mp.mpf(1)/2-1/mp.pi), 'Stationary Hessian failed')
    check(second>0,'Nonmaximizer control failed')
    t=mp.mpf('1e-6'); m=mp.mpf('0.5')
    delta=mp.log(1+((1-m)/m)*t*t)/2-entropy_cost(2,t)
    check(delta<0,'s>1 perturbation barrier failed')
    # Correct radial formula for an ellipse whose minor semiaxis is eps^2.
    eps=mp.mpf('1e-6')
    rho=1/mp.sqrt(mp.cos(eps)**2+mp.sin(eps)**2/eps**4)
    check(abs(rho/eps-1)<mp.mpf('1e-10'),'Radial semicontinuity counterexample failed')
    # General join entropy O(t^k): evaluate its spherical beta integral after scaling.
    join=[]
    for n,k in [(3,2),(4,2),(4,3),(6,2),(6,4)]:
        t=mp.mpf('1e-5'); lim=t/mp.sqrt(1+t*t)
        coef=2/mp.beta(mp.mpf(k)/2,mp.mpf(n-k)/2)
        # R=lim*x; support comparison is t*sqrt(1-R^2)/R.
        val=coef*lim**k*mp.quad(lambda x: x**(k-1)*(1-(lim*x)**2)**(mp.mpf(n-k)/2-1)*mp.log(t*mp.sqrt(1-(lim*x)**2)/(lim*x)),[0,1])
        leading=coef/(k*k)
        check(abs(val/t**k/leading-1)<mp.mpf('1e-8'),'Join entropy rank control failed')
        join.append({'n':n,'k':k,'limiting_entropy_coefficient':fmt(leading)})
    # Nonorthogonal-pair beta formula, limiting ratios, and positivity.
    oblique=0
    for alpha in [mp.pi/12,mp.pi/6,mp.pi/3,mp.pi/2]:
        for t in [mp.mpf('0.01'),mp.mpf('0.5'),mp.mpf(1),mp.mpf(2),mp.mpf(100)]:
            beta=mp.atan2(2*t*mp.sin(alpha),1-t*t)
            check(0<beta<mp.pi,'Oblique exterior angle out of range')
            reverse=mp.atan2(2/t*mp.sin(alpha),1-1/(t*t))
            check(close(beta+reverse,mp.pi),'Oblique opposite pair angle sum')
            if alpha==mp.pi/2:
                check(close(beta,2*mp.atan(t)),'Orthogonal specialization failed')
            oblique += 1
    return {'schema':'negative-p-aleksandrov-controls-v1','status':'PASS',
            'kind':'finite high-precision controls, not proof or interval certificates',
            'precision_decimal_digits':60,'line_thresholds':rows,
            'strict_planar_boundary':fmt(mp.pi/(mp.pi+2)),
            'planar_interval_samples':samples,'root_controls':roots,
            'three_equal_mass_solution_log_aspects_s_1_1':[fmt(zlo),'0.0',fmt(zhi)],
            'aspect_hessian_s_2':fmt(second),
            'join_entropy_rank_controls':join,
            'oblique_geometry_samples':oblique,
            'radial_collapse_control':'ellipse radial value tends to 0 while limit segment radial value is 1',
            'full_problem_solved':False,'independent_audit':'pending'}

if __name__=='__main__':
    result=run()
    output=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if sys.argv[1:]==['--write']:
        (ROOT/'CHECK_RESULTS.json').write_text(output)
    elif sys.argv[1:]:
        raise SystemExit('Usage: verify_math.py [--write]')
    else:
        check((ROOT/'CHECK_RESULTS.json').read_text()==output,'Saved controls differ from replay')
    print('PASS: finite controls reproduced; deductive claims require review of PROOFS.md')
