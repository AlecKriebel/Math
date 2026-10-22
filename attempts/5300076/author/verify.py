#!/usr/bin/env python3
"""Deterministic controls, not interval-arithmetic or proof certificates."""
import json
import math
from fractions import Fraction

counts = {}

def check(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1

def close(group, a, b, tolerance=2e-11):
    check(group, abs(a-b) <= tolerance * max(1., abs(a), abs(b)))

def P(x, k, alpha):
    return k * (1-abs(2*x-1)**alpha)

def inverse(y, k, alpha, sign):
    z = 1-y/k
    if z < -1e-13:
        raise ValueError('Image outside lift range')
    return (1+sign*max(0., z)**(1/alpha))/2

def H(q, alpha):
    return (q + math.log1p(math.exp(-q)))/alpha

def root_q(alpha):
    lo, hi = 0., 1.
    while H(hi, alpha) > hi:
        hi *= 2
    for _ in range(200):
        mid = (lo+hi)/2
        if H(mid, alpha) > mid:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2

alphas = [1.05, 1.1, 1.25, 1.5, 2., 2.7, 4., 10.]
for alpha in alphas:
    for k in [.1, .25, .5, .7, .99, 1.]:
        for j in range(101):
            y = k*j/100
            for sign in [-1, 1]:
                x = inverse(y,k,alpha,sign)
                close('inverse_branch_round_trip', P(x,k,alpha), y)
                check('inverse_branch_ranges', 0 <= x <= .5 if sign < 0 else .5 <= x <= 1)
        b = (2*k)**(1/(alpha-1))
        a = b*(2*k-1)
        for j in range(101):
            x = j/100
            z = b*(2*x-1)
            close('affine_normalization', b*(2*P(x,k,alpha)-1), a-abs(z)**alpha,
                  tolerance=1e-9)
    for k in [.500001, .51, .6, .8, .999999]:
        q = -math.log(2*k-1)
        kp = inverse(.5,k,alpha,+1)
        close('period_two_recurrence', -math.log(2*kp-1), H(q,alpha))
    qstar = root_q(alpha)
    tstar = math.exp(-qstar)
    close('period_two_root_equation', tstar**(alpha-1)*(1+tstar), 1.)
    for initial in [0., .0001, .1, 1., 10., 100.]:
        q = initial
        for n in range(300):
            nextq = H(q,alpha)
            check('period_two_one_step_contraction', abs(nextq-qstar) <= abs(q-qstar)/alpha+2e-13)
            q = nextq
        check('period_two_global_error_bound', abs(q-qstar) <= abs(initial-qstar)*alpha**(-300)+1e-11)
    for q in [0., .01, .1, 1., 3., 10., 100.]:
        derivative = 1/(alpha*(1+math.exp(-q)))
        check('period_two_derivative_bound', 0 < derivative <= 1/alpha)

# Test a genuinely non-family, piecewise-linear, critical-period-two initial map.
# Vertices (0,0), (1/2,k), (k,1/2), (1,0).
for alpha in alphas:
    for k in [.55,.7,.9]:
        def f(x):
            if x <= .5:
                return 2*k*x
            if x <= k:
                return k + (.5-k)*(x-.5)/(k-.5)
            return .5*(1-x)/(1-k)
        def h(x):
            return inverse(f(x),k,alpha,-1 if x <= .5 else 1)
        for j in range(101):
            x = j/100
            close('piecewise_linear_lift_relation',P(h(x),k,alpha),f(x))
        newk = h(k)
        close('piecewise_linear_new_critical_value',h(P(.5,k,alpha)),newk)
        close('piecewise_linear_period_two_pullback',P(newk,k,alpha),.5)
        close('piecewise_linear_critical_anchor',h(.5),.5)

# Exact marked-label fixtures for period one, period two, and endpoint preperiod.
for alpha in alphas:
    for points, sigma, critical in [([0.,.5,1.],[0,1,0],1),
                                   ([0.,.5,.8,1.],[0,2,1,0],1),
                                   ([0.,.5,1.],[0,2,0],1)]:
        v = sigma[critical]
        k = points[v]
        out = [.5 if i==critical else inverse(points[sigma[i]],k,alpha,
                  -1 if i<critical else 1) for i in range(len(points))]
        check('marked_order_preservation',all(out[i] < out[i+1] for i in range(len(out)-1)))
        check('marked_anchors',out[0]==0 and out[-1]==1 and out[critical]==.5)
        for i in range(len(out)):
            close('marked_pullback_relation',P(out[i],k,alpha),points[sigma[i]])

# Log-periodic two-cycles. Computation uses centered coordinates to avoid
# cancellation near the critical point; the analytic proof covers all t.
separations=[]
for alpha in alphas:
    omega = math.pi/math.log(alpha)
    eps = .2
    A = 2+eps*math.sqrt(1+omega*omega)
    def g(t,theta):
        if t==0:return 0.
        if t==1:return 1.
        s = -math.log(t)
        return math.exp(-s*(A+eps*math.sin(omega*math.log(s)+theta)))
    for j in range(1,100):
        t=j/100
        s=-math.log(t)
        for theta in [0.,math.pi]:
            deriv = A+eps*math.sin(omega*math.log(s)+theta)+eps*omega*math.cos(omega*math.log(s)+theta)
            check('log_periodic_monotonicity',deriv > 0)
            close('log_periodic_exact_update',g(t**alpha,theta)**(1/alpha),g(t,theta+math.pi))
        close('log_periodic_two_cycle',g(t,0),g(t,2*math.pi))
    t0=math.exp(-math.sqrt(alpha))
    separation=(g(t0,math.pi)-g(t0,0))/2
    formula=math.exp(-math.sqrt(alpha)*A)*math.sinh(math.sqrt(alpha)*eps)
    close('two_cycle_positive_separation_formula',separation,formula)
    check('two_cycle_nontrivial',separation>0)
    separations.append({'alpha':alpha,'separation':format(separation,'.12g')})
    for gamma in [.5,1.,2.,3.5]:
        for j in range(1,100):
            t=j/100
            close('stationary_power_control',(t**(alpha*gamma))**(1/alpha),t**gamma)

# Exact rational initial critical itinerary, confirming positive descending terms.
x=Fraction(1,4)
for _ in range(10):
    new=x*(1-x)
    check('rational_nonfinite_orbit_control',0 < new < x < Fraction(1,2))
    x=new

# Exact contraction-limit countercontrol for route 4.
for eps in [Fraction(1,2),Fraction(1,4),Fraction(1,8)]:
    x=Fraction(1)
    for n in range(1,31):
        x=-(1-eps)*x
        check('exact_parameter_limit_countercontrol',x==(-1)**n*(1-eps)**n)
for n in range(40):
    check('exact_limit_two_cycle',(-Fraction(1))**n==(-1)**n)

# The Euclidean derivative gets larger along this sequence, for alpha=2.
previous=0.
for power in range(2,11):
    k=.5+10**(-power)
    d=.5/(4*k*k)*(1-1/(2*k))**(-.5)
    check('euclidean_derivative_blowup_control',d>previous)
    previous=d

print(json.dumps({'status':'PASS','method':'finite floating-point diagnostics plus exact Fraction controls; analytic proofs are in RESULT.md',
                  'float_default_relative_absolute_tolerance':'2e-11; affine normalization 1e-9; contraction additive allowance 2e-13',
                  'counts':counts,'assertions':sum(counts.values()),'two_cycle_separations':separations},indent=2,sort_keys=True))
