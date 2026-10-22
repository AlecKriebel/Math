#!/usr/bin/env python3
"""Independent finite controls, not an infinite convergence or theorem verifier.

The exact series algorithms use finite powers rather than the author's derivative
recurrences. Numerical differentiation uses mpmath at 80 decimal digits and
closed chain-rule products, not the author's floating-point recurrence.
"""
from fractions import Fraction
from math import factorial
import json
import random
import sys
import mpmath as mp

if sys.flags.optimize:
    raise SystemExit('Optimized Python is not supported.')

def require(ok, description):
    if not ok:
        raise RuntimeError(description)

Q=Fraction

def multiply(a,b):
    n=len(a)
    result=[Q(0)]*n
    for i,x in enumerate(a):
        for j,y in enumerate(b[:n-i]):
            result[i+j]+=x*y
    return result

def power_series(a,kind):
    n=len(a)
    constant=Q(1) if kind in ('exp','inverse') else Q(0)
    result=[constant]+[Q(0)]*(n-1)
    power=[Q(1)]+[Q(0)]*(n-1)
    for j in range(1,n):
        power=multiply(power,a)
        coefficient={'exp':Q(1,factorial(j)),
                     'log':Q((-1)**(j+1),j),
                     'inverse':Q((-1)**j)}[kind]
        result=[x+coefficient*y for x,y in zip(result,power)]
    return result

def run():
    rng=random.Random(5300062)
    exact=0
    for degree in range(1,9):
        for _ in range(20):
            h=[Q(0)]+[Q(rng.randint(-5,5),rng.randint(1,7)) for k in range(degree)]
            e=power_series(h,'exp');e[0]-=1
            require(power_series(e,'log')==h,'formal log(exp(h))')
            exact+=1
            l=power_series(h,'log')
            require(power_series(l,'exp')==[Q(1)]+h[1:],'formal exp(log(1+h))')
            exact+=1
            require(multiply([Q(1)]+h[1:],power_series(h,'inverse'))==[Q(1)]+[Q(0)]*degree,'geometric-series reciprocal')
            exact+=1
    mp.mp.dps=80
    F=mp.expm1
    def orbit(t,n):
        values=[mp.mpc(t)]
        for _ in range(n):values.append(F(values[-1]))
        return values
    def preimages(k,t,s):
        f=orbit(t,len(s))
        x=[mp.mpc(0)]*len(f);x[-1]=f[-1]
        for j in range(len(s)-1,-1,-1):x[j]=mp.log(x[j+1])-k+2j*mp.pi*s[j]
        return f,x
    def value(k,t,s):return preimages(k,t,s)[1][0]
    counts=dict(conjugacy=0,derivative=0,branch=0,growth=0,tail_buffer=0,simple_root=0,flat_positive=0)
    tolerance=mp.mpf('1e-65')
    max_residual=mp.mpf(0)
    def near(x,y,label):
        nonlocal max_residual
        residual=abs(x-y)/(1+abs(y));max_residual=max(max_residual,residual)
        require(residual<tolerance,label)
    for j in range(30):
        k=mp.mpc(-mp.mpf(15)/100+mp.mpf(j)/120,-mp.mpf(2)/10+mp.mpf(j)/100)
        z=mp.mpc(-mp.mpf(7)/10+mp.mpf(j)/80,mp.mpf(2)/10-mp.mpf(j)/170)
        E=lambda phase:mp.exp(phase+k)
        T=lambda phase:phase+k
        T_inverse=lambda phase:phase-k
        near(T(E(T_inverse(z))),mp.exp(z)+k,'translation conjugacy');counts['conjugacy']+=1
        near(mp.exp(k)*mp.exp(z),mp.exp(z+k),'lambda normalization');counts['conjugacy']+=1
        t=mp.mpf(6)/10+mp.mpf(j)/150;s=[0,1,-1];f,x=preimages(k,t,s)
        # Sum of the effects of inserting -k at each level, and full product.
        dk=-sum(mp.fprod(1/x[l] for l in range(1,jj+1)) for jj in range(len(s)))
        dt=mp.exp(sum(f[:-1]))/mp.fprod(x[1:])
        near(dk,mp.diff(lambda kk:value(kk,t,s),k),'closed parameter derivative');counts['derivative']+=1
        near(dt,mp.diff(lambda tt:value(k,tt,s),t),'closed potential derivative');counts['derivative']+=1
        v=mp.mpc(6+mp.mpf(j)/100,mp.mpf(3)/100);U=F(v);d=mp.mpc(-mp.mpf(1)/10,mp.mpf(2)/10)
        near(v+mp.log1p(-mp.exp(-v))+mp.log1p(d/U),mp.log(U+d),'continued two-log identity');counts['branch']+=1
        tt=mp.mpf(j)/11
        gp=mp.diff(lambda y:y+1j*y*y,tt)
        phi_t=mp.diff(lambda y:k-y-1j*y*y,tt)
        near(gp,-phi_t,'implicit derivative');counts['simple_root']+=1
    for u in [mp.mpf(2),mp.mpf('2.1'),mp.mpf('2.2')]:
        for delta in map(mp.mpf,['.01','.02','.04','.1']):
            for n in [1,2]:
                um=orbit(u,n)[-1].real;vm=orbit(u+delta,n)[-1].real
                require(vm-um>=2**n*delta,'iterate separation');counts['growth']+=1
                require(um/vm<=2*mp.exp(-2**(n-1)*delta),'iterate ratio');counts['growth']+=1
    for K in [1,2,5,10,20]:
        for extra in map(mp.mpf,['.1','.5','1','2']):
            a=K+6+extra
            require((K+2)*mp.exp(-a)<1-mp.exp(-1),'baseline safety');counts['tail_buffer']+=1
            require(mp.log(F(a)-K-1)-K>=a-K-1,'baseline pullback');counts['tail_buffer']+=1
            require(abs(1/(1-mp.exp(-mp.mpc(a,'.03'))))<2,'q derivative');counts['tail_buffer']+=1
    for j in range(1,10):
        t=mp.mpf(1)/(j+1)
        require(mp.exp(-1/t**2)>0,'flat function positive side');counts['flat_positive']+=1
    require(exact==480,'exact count')
    require(sum(counts.values())==297,'numerical count')
    # Deliberately make Im U exceed pi: principal log(F(U)) then differs from
    # its holomorphic continuation q(U). This is the branch trap §3.2 avoids.
    branch_traps=0
    for real in [7,8,9]:
        for imag in [mp.mpf('.01'),mp.mpf('.02'),mp.mpf('.04'),mp.mpf('.06')]:
            v=mp.mpc(real,imag);U=F(v)
            continued=U+mp.log1p(-mp.exp(-U))
            naive=mp.log(F(U))
            require(abs(continued-naive)>2*mp.pi-mp.mpf('1e-60'),'naive branch countercontrol')
            d=mp.mpc('.3','.4')
            near(v+mp.log1p(-mp.exp(-v))+mp.log1p(d/U),mp.log(U+d),'valid two-log continuation beyond naive branch')
            branch_traps+=1
    # The original threshold need not meet the cited sufficient threshold.
    K=mp.mpf(1);x0=mp.mpf(100);a=mp.mpf('100.01')
    require(a>max(x0,K+6) and a<x0+2*mp.log(K+3),'tail threshold repair witness')
    return {'problem_id':5300062,'result':'PASS_FINITE_CONTROLS_ONLY',
            'exact_rational_jet_controls':exact,'numerical_controls':sum(counts.values()),
            'numerical_breakdown':counts,'additional_principal_branch_trap_controls':branch_traps,
            'original_tail_citation_threshold_countercontrol':True,
            'maximum_normalized_residual_below_1e_minus_65':bool(max_residual<tolerance),
            'precision_decimal_digits':80,'mpmath_version':mp.__version__,
            'independence':'No author code imported. Formal finite power sums; arbitrary-precision differentiation and closed products.',
            'limits':['Finite numerical checks are not interval-certified.','No infinite convergence, transversality, all-address construction, geometric analyticity or endpoint theorem is proved by this program.']}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
