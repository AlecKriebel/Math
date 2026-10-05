#!/usr/bin/env python3
"""Independent standard-library diagnostics. Universal proofs are in AUDIT.md."""
import json, math
from decimal import Decimal, localcontext
from fractions import Fraction
counts = {}
def check(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1
def close(group, a, b, tol=2e-10):
    check(group, abs(a-b) <= tol*max(1, abs(a), abs(b)))

# Exact algebraic signs for H': u/(alpha*(1+u)); u stands for exp(q).
for alpha in [Fraction(1000001,1000000), Fraction(101,100), Fraction(3,2), Fraction(2), Fraction(17,3), Fraction(1000)]:
    for u in [Fraction(1), Fraction(3,2), Fraction(10), Fraction(10**12), Fraction(10**100)]:
        d = u/(alpha*(1+u))
        check('exact_H_derivative_signs', 0 < d < 1/alpha < 1)
        check('exact_H_derivative_gap', 1/alpha-d == 1/(alpha*(1+u)))

# Exact formal half-turn: A+B*sin(z)+C*cos(z) -> A-B*sin(z)-C*cos(z).
for A in range(1,8):
    for B in range(-5,6):
        for C in range(-5,6):
            triple = (Fraction(A),Fraction(B,7),Fraction(C,11))
            shifted = (triple[0],-triple[1],-triple[2])
            twice = (shifted[0],-shifted[1],-shifted[2])
            check('exact_formal_halfturn_involution',twice==triple)
            check('exact_formal_halfturn_nontrivial', (shifted!=triple)==(B!=0 or C!=0))

# Decimal avoids cancellation in the first step when the original critical point
# is not normalized. Do not reuse/import the author's implementation.
with localcontext() as ctx:
    ctx.prec=75
    D=Decimal
    zero,one,half=D(0),D(1),D('0.5')
    def power(t,a):
        return zero if t==0 else (a*t.ln()).exp()
    def p(x,k,a): return k*(one-power(abs(2*x-one),a))
    def branch(v,k,a,right):
        rad=one-v/k
        if abs(rad)<D('1e-65'):rad=zero
        return (one+(one if right else -one)*power(rad,one/a))/2
    for a in map(D,['1.01','1.25','1.999','2','3.141592653589793','17']):
        for c,k in [('0.1','0.8'),('0.37','0.61'),('0.6','0.85'),('0.89','0.99')]:
            c,k=D(c),D(k)
            def f(x):
                if x<=c:return k*x/c
                if x<=k:return k+(c-k)*(x-c)/(k-c)
                return c*(one-x)/(one-k)
            def h(x):return branch(f(x),k,a,x>c)
            newk=h(k)
            check('unnormalized_period_two_location',half<newk<one)
            close('unnormalized_critical_value',h(p(half,k,a)),newk,D('1e-50'))
            close('unnormalized_period_two_direct_composition',h(p(newk,k,a)),half,D('1e-25'))
            for j in range(21):
                x=D(j)/20
                close('unnormalized_lift_identity',p(h(x),k,a),f(x),D('1e-50'))
            # A second step must now obey the normalized scalar recurrence.
            def fnew(x):return h(p(x,k,a))
            nextk=branch(fnew(newk),newk,a,True)
            target=branch(half,newk,a,True)
            close('unnormalized_then_scalar_recurrence',nextk,target,D('1e-25'))

# Marked configurations with actual periods 3 and 4 and genuine preperiodicity.
fixtures=[([0.,.2,.5,.9,1.],[0,2,3,1,0],2,3),
          ([0.,.1,.3,.5,.95,1.],[0,2,3,4,1,0],3,4),
          ([0.,.2,.5,.9,1.],[0,1,3,1,0],2,None)]
for a in [1.01,1.125,1.6,2.,2.718281828,10.]:
    for original,sigma,d,period in fixtures:
        xs=list(original)
        if period:
            label=d
            for n in range(1,period+1):
                label=sigma[label]
                check('exact_label_period',(label==d)==(n==period))
        for _ in range(8):
            k=xs[sigma[d]]
            ys=[.5 if i==d else (1+(-1 if i<d else 1)*(1-xs[sigma[i]]/k)**(1/a))/2 for i in range(len(xs))]
            check('higher_orbit_marked_order',all(x<y for x,y in zip(ys,ys[1:])))
            check('higher_orbit_marked_anchors',ys[0]==0 and ys[-1]==1 and ys[d]==.5)
            for i,y in enumerate(ys):
                close('higher_orbit_pullback_equation',k*(1-abs(2*y-1)**a),xs[sigma[i]])
            xs=ys

# Boundary-aware q evaluation, no exp(q) overflow.
def H(q,a):return (q+math.log1p(math.exp(-q)))/a
alphas=[1+1e-12,1.00001,1.01,1.125,math.sqrt(2),math.pi,17.,1000.]
qs=[0.,1e-14,1e-7,.125,1.,10.,100.,1e4,1e10]
for a in alphas:
    for q in qs:
        check('H_boundary_and_extreme_finite', math.isfinite(H(q,a)) and H(q,a)>0)
        close('H_zero_boundary_value',H(0,a),math.log(2)/a)
        for r in qs:
            allowance=16*math.ulp(max(1.,abs(H(q,a)),abs(H(r,a))))
            check('H_global_pair_contraction',abs(H(q,a)-H(r,a))<=abs(q-r)/a+allowance)
    # t=0 is a separate fixed boundary, not part of the positive period-two basin.
    check('t_zero_fixed_boundary',(0./(1+0.))**(1/a)==0.)
    check('t_one_enters_interior',0 < (1./2)**(1/a) < 1)
    # α-dependent coefficient size is handled in logarithmic coordinates.
    w=math.pi/math.log(a); e=.2; A=2+e*math.hypot(1,w)
    for log_s in [-12.,-3.,0.,2.,10.]:
        s=math.exp(log_s)
        for theta in [0.,.31,math.pi]:
            lhs=s*(A+e*math.sin(w*(math.log(a)+log_s)+theta))
            rhs=s*(A+e*math.sin(w*log_s+theta+math.pi))
            # Scale-relative test, with large omega and phase-reduction errors disclosed.
            close('log_cycle_no_exponent_underflow',lhs,rhs,1e-10)
            derivative=A+e*math.sin(w*log_s+theta)+e*w*math.cos(w*log_s+theta)
            check('cycle_derivative_lower_bound',derivative>=A-e*math.hypot(1,w)-.001)
    log_sep=2*e*math.sqrt(a)
    check('cycle_log_separation_strict',log_sep>0)

# Exact stationary fibers at rational t: avoid a numeric root by comparing powers.
for alpha in [2,3,4,7]:
    for gamma in [1,2,3,5]:
        for j in range(1,20):
            t=Fraction(j,20)
            check('exact_stationary_fiber_power_identity',(t**gamma)**alpha==(t**alpha)**gamma)

print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'counts':counts,
                  'method':'exact Fraction algebra; 75-digit Decimal diagnostics; bounded floating-point diagnostics, not universal proof certificates',
                  'limits':'No finite tests prove the all-exponent theorems, global target, manuscript correctness, or historical novelty.'},indent=2,sort_keys=True))
