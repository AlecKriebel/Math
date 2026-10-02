#!/usr/bin/env python3
"""Independent finite controls for the five-turn coagulation audit.

Only exact rational/symbolic algebra is used. This does not prove the analytic
compactness, nonexplosion, comparison, concentration or weak-limit arguments.
"""
from fractions import Fraction as Q
from collections import Counter
from math import gcd, prod
import json
import sympy as S

counts=Counter()
def check(group, condition):
    if not condition: raise AssertionError(group)
    counts[group]+=1

# Rebuild moment derivatives directly from the finite coordinate vector field.
# Test arbitrary positive rates, concentrations, inputs and polynomial weights.
for n in range(2,42):
    for seed in range(1,7):
        a=[Q(1)]+[Q((i+seed)**2, i+2*seed) for i in range(2,n+1)]
        c=[Q((3*i+seed)%17+1, i+seed+1) for i in range(1,n+1)]
        x=c[0];J=Q(seed,7)
        rhs=[J-x*x-x*sum(ai*ci for ai,ci in zip(a,c))]
        rhs += [x*(a[j-2]*c[j-2]-a[j-1]*c[j-1]) for j in range(2,n+1)]
        for power in range(4):
            direct=sum(Q(j**power)*rhs[j-1] for j in range(1,n+1))
            expected=J+(2**power-2)*x*x
            expected+=x*sum(((i+1)**power-i**power-1)*a[i-1]*c[i-1] for i in range(2,n))
            expected-=(n**power+1)*a[-1]*x*c[-1]
            check('direct_finite_moment_polynomial',direct==expected)
        check('first_moment_boundary',sum((j+1)*r for j,r in enumerate(rhs))==J-(n+1)*a[-1]*x*c[-1])
        check('second_moment_boundary',sum((j+1)**2*r for j,r in enumerate(rhs))==J+2*x*sum(i*a[i-1]*c[i-1] for i in range(1,n))-(n*n+1)*a[-1]*x*c[-1])

# Independently solve finite pure-birth Laplace recurrences, including absorbing
# stopping at n. This checks both starting-size shifts and the dimer indexing.
for n in range(3,24):
    for style in range(3):
        rates={k:(Q(1) if style==0 else Q(k*k+style,2*k+1)) for k in range(2,n+1)}
        for z in [Q(1,5),Q(7,3),Q(13)]:
            for start in [2,n//2+1]:
                F={start:1/(z+rates[start])}
                for j in range(start+1,n):F[j]=rates[j-1]*F[j-1]/(z+rates[j])
                F[n]=rates[n-1]*F[n-1]/z
                check('stopped_birth_total_probability',sum(F.values())==1/z)
                for j in range(start,n):
                    hitting=prod(rates[k]/(z+rates[k]) for k in range(start,j))
                    check('shifted_occupancy_transform',F[j]==hitting/(z+rates[j]))
            g=Q(1)
            c=1/(z+rates[2])
            for j in range(2,n+1):
                if j>2:c=rates[j-1]*c/(z+rates[j])
                g*=rates[j]/(z+rates[j])
                check('weighted_forcing_transfer',rates[j]*c==g)

# Check the exact finite Chernoff optimization and a polynomial remainder bound.
for den in range(2,16):
    for num in range(1,den//2+1):
        z=Q(num,den)
        for terms in [2,3,8,20]:
            remainder=sum(z**k/k for k in range(2,terms+1))
            check('log_series_positive_remainder',remainder<=z*z/(2*(1-z))<=z*z)
for x in [Q(i,3) for i in range(1,35)]:
    for variance in [Q(1,8),Q(2,3),Q(13)]:
        for maxmean in [Q(1,5),Q(2),Q(19)]:
            lam=min(x/(2*variance),1/(2*maxmean))
            check('chernoff_parameter',lam*maxmean<=Q(1,2))
            check('chernoff_two_branch_bound',lam*x-lam*lam*variance>=min(x*x/(4*variance),x/(4*maxmean)))

# Independent strict-regime parameter scan checks the closed form of the
# bootstrap, crossing-curve error, profile constants in logarithmic coordinates,
# and deliberate zero-exponent cases (not only generic inequalities).
max_steps=0;zero_cases=[];parameters=0
for den in range(3,20):
    for num in range(1,den):
        if gcd(num,den)!=1:continue
        p=Q(num,den);nu=p/(1-p)
        for bn in range(8,81):
            beta=Q(bn,15);w=beta-1;d=beta*(1-p)
            if d>=Q(1,2):continue
            parameters+=1
            a0=max(w/2,Q(0));b0=a0+d;b=b0;fixed=(2*d-1)/(1-p);steps=0
            check('strict_fixed_point_negative',fixed<0)
            while b>0:
                steps+=1;b=p*b+2*d-1
                check('bootstrap_closed_form',b==p**steps*(b0-fixed)+fixed)
                if steps>1000:raise AssertionError('bootstrap budget')
            if b==0:
                zero_cases.append([str(p),str(beta),steps])
                eps=(1-2*d)/(3*p)
                check('zero_exponent_escape',2*d-1+p*eps<0)
            max_steps=max(max_steps,steps)
            check('physical_input_barrier_error',d-2-w==-p*beta-1<0)
            if w>0:
                k=(beta-w/2)/(nu+2)
                check('preliminary_clock_lower',k==(1+w/2)/(nu+2))
                check('moving_clock_curve_error',w-k*(2*nu+1)<0)
            r=1/d-1;q=p+(1-p)*r
            check('strict_profile_exponent',q==2*p-1+1/beta)
            check('bulk_mass_scale_gap',beta*(2-q)-beta==2*d-1)
            # B has alpha,beta,N exponents (1-p,p,p-1); multiplying by
            # (kappa/N)^(-(d-1)/beta) gives C*(1-p)^r.
            ratio=(d-1)/beta
            exp_alpha=1-p-ratio;exp_beta=p+ratio;exp_N=p-1+ratio
            check('profile_normalization_alpha',exp_alpha==1/beta)
            check('profile_normalization_beta',exp_beta==w/beta)
            check('profile_normalization_number',exp_N==-1/beta)

# Deliberately hit the a+d=0 branch, which a generic rational grid may miss.
p=Q(1,2);beta=Q(4,5);d=beta*(1-p);b=d
b=p*b+2*d-1
check('deliberate_zero_exponent',b==0)
zero_cases.append([str(p),str(beta),1])
eps=(1-2*d)/(3*p)
check('zero_exponent_escape',2*d-1+p*eps<0)
for p in [Q(1,4),Q(1,2),Q(3,4),Q(99,100)]:
    b=Q(1,3)
    for step in range(1,15):
        b=p*b
        check('critical_bootstrap_does_not_close',b>0)
    b=Q(1,3)
    for step in range(1,15):
        b=p*b+Q(1,10)
        check('supercritical_bootstrap_does_not_close',b>0)

# Exact independent Jensen controls for p=m/q on support consisting of qth powers.
for den in range(2,15):
    for num in range(1,den):
        for w1 in range(1,6):
            weights=[Q(w1,w1+5),Q(2,w1+5),Q(3,w1+5)]
            mean=sum(w*k**den for w,k in zip(weights,[2,3,5]))
            pmean=sum(w*k**num for w,k in zip(weights,[2,3,5]))
            check('stopped_process_Jensen',pmean**den<=mean**num)

# Symbolic derivative of actual-N comparison curves; no derivative of an
# asymptotic equivalence is substituted. The power/log constants are computed
# from the exact inversion relation and profile multiplier.
t,N,alpha,f,eps=S.symbols('t N alpha f eps',positive=True)
u=2*alpha*(1+eps)/(t*N)
du=S.diff(u,t)+S.diff(u,N)*f
check('critical_actual_curve_derivative',S.simplify(du+u*(1/t+f/N))==0)
for e in [Q(i,23) for i in range(1,23)]:
    delta=e/(2*(1+e))
    check('critical_upper_signed_field',1/(1+e)-(1-delta)<0)
    check('critical_lower_signed_field',1/(1-e)-(1+delta)>0)
for aval in [S.Rational(1,7),S.Rational(2,5),S.Integer(1),S.Integer(19)]:
    tc=2**S.Rational(3,4)*aval**S.Rational(1,4)
    xc=aval**S.Rational(1,4)/2**S.Rational(1,4)
    nc=S.sqrt(2*aval);sc=S.sqrt(aval/2)
    check('critical_inversion_constant',S.simplify(tc**2/(2*S.sqrt(2*aval)))==1)
    check('critical_rate_constant',S.simplify(S.sqrt(2*aval)/tc-xc)==0)
    check('critical_mass_product',S.simplify(nc*sc-aval)==0)
    check('critical_size_coefficient',S.simplify(tc**2/4-sc)==0)
    check('critical_profile_cancellation',S.simplify((2*S.sqrt(aval)*t)*(S.sqrt(aval)/t)/(2*aval))==1)

# Time-integrated mass obstruction, plus equality controls that do not imply
# convergence. Check the sharp algebraic implication, not a Riemann-sum ansatz.
for sn in range(1,31):
    ss=Q(sn,13)
    for rn in range(-11,23):
        rr=Q(rn,9);beta=Q(8,7)
        difference=2-rr+1/ss-(beta+1)/ss
        check('fixed_ray_mass_condition',(difference>0)==(ss*(2-rr)>beta))
check('literal_counterexample_exponent',Q(4,5)*(2-Q(2,3))==Q(16,15))
check('literal_corrected_amplitude_boundary',Q(4,5)*(2-Q(3,4))==1)

print(json.dumps(dict(status='PASS',exact_assertions=sum(counts.values()),
    counts=dict(sorted(counts.items())),strict_parameter_pairs=parameters,
    maximum_bootstrap_steps=max_steps,zero_exponent_cases=zero_cases,
    floating_point_used=False,
    scope='Finite operator, kernel, rational-parameter, comparison and normalization controls. Analytic conclusions are separately reviewed in REVIEW.md.'),indent=2,sort_keys=True))
