"""Floating diagnostics only. No validated quadrature or rigorous ODE integration."""
import json
import mpmath as mp
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.special import logsumexp
from itertools import combinations
mp.mp.dps=60
checks=0

def check(p):
    global checks
    assert p
    checks += 1

def radial_mean(e):
    e=mp.mpf(str(e))
    f=lambda d:mp.exp(-d*d/8)*mp.acosh(d/(2*e))*mp.acos(2*e/d)/(2*mp.pi)
    return mp.quad(f,[2*e,2*e+1,max(2*e+2,mp.mpf(8)),mp.inf])

def original_gaussian_mean(e):
    # Independent input-coordinate integral: u~N(0,1), v~abs(N(0,1)).
    # Odd asinh(u/v) term cancels only after using the original Gaussian symmetry.
    def outer(v):
        def inner(u):
            r=np.hypot(u,v)
            return np.exp(-u*u/2)*np.arccosh(r/e)/r
        return np.exp(-v*v/2)*quad(inner,0,np.inf,epsabs=2e-11,epsrel=2e-11)[0]/np.pi
    value,error=quad(outer,e,np.inf,epsabs=2e-10,epsrel=2e-10)
    return value,error

quadrature=[]
for e in [.1,1,3]:
    a=radial_mean(e); b,err=original_gaussian_mean(e)
    check(abs(float(a)-b)<2e-8)
    quadrature.append({'epsilon':e,'radial_60_digit':mp.nstr(a,45),'input_coordinate_scipy':b,'scipy_outer_error_estimate':err,'absolute_difference':abs(float(a)-b)})
C=mp.sqrt(mp.pi/8);B=C*(mp.log(2)-mp.euler)/2
asymptotic=[]
for e in [mp.mpf('0.001'),mp.mpf('0.00001'),mp.mpf('0.0000001')]:
    value=radial_mean(e)
    err=value-C*mp.log(1/e)-B
    asymptotic.append({'epsilon':str(e),'residual':mp.nstr(err,35)})
check(abs(mp.mpf(asymptotic[-1]['residual']))<abs(mp.mpf(asymptotic[0]['residual'])))
# Endpoint integrand vanishes linearly; its product/h limit is 1/epsilon.
for e in [mp.mpf('.01'),mp.mpf(1),mp.mpf(8)]:
    h=e*mp.mpf('1e-25');d=2*e+h
    ratio=mp.acosh(d/(2*e))*mp.acos(2*e/d)/h
    check(abs(ratio*e-1)<mp.mpf('1e-20'))
# Initial-below and exactly-on-rising-boundary adversarial cases.
d=mp.mpf(4);e=mp.mpf('0.5');A=mp.acosh(d/(2*e));s=-3
check(d/(2*mp.cosh(s))<e)
check((A-s)/d>0) # outgoing-root substitution would be wrong.
s=-A
check(d/(2*mp.cosh(s+mp.mpf('1e-20')))>e)
check(abs(d/(2*mp.cosh(s+2*A))-e)<mp.mpf('1e-58'))

# Independent integration of the entrywise Toda ODE against tau sums.
# Nonmonotone example additionally separates simultaneous and individual first crossings.
a0=np.array([-2.,0.,2.]);b0=np.array([.1,1.]);n=3;e=.5
J=np.diag(a0)+np.diag(b0,1)+np.diag(b0,-1)
lam,Q=np.linalg.eigh(J);w=Q[0]**2

def rhs(t,y):
    a=y[:n];b=y[n:];bb=np.r_[0.,b*b,0.]
    return np.r_[2*np.diff(bb),b*np.diff(a)]

def b_spectral(t):
    logs=[0.]
    for k in range(1,n+1):
        terms=[]
        for I in combinations(range(n),k):
            val=sum(np.log(w[i])+2*t*lam[i] for i in I)
            val+=2*sum(np.log(lam[j]-lam[i]) for i,j in combinations(I,2))
            terms.append(val)
        logs.append(logsumexp(terms))
    return np.array([np.exp((logs[k-1]+logs[k+1]-2*logs[k])/2) for k in range(1,n)])

def all_event(t,y):return max(y[n:])-e
all_event.direction=-1
all_event.terminal=True

def second_event(t,y):return y[n+1]-e
second_event.direction=-1
second_event.terminal=False
sol=solve_ivp(rhs,[0,10],np.r_[a0,b0],rtol=2e-12,atol=2e-13,max_step=.01,dense_output=True,events=[all_event,second_event])
T=float(sol.t_events[0][0]);Tsecond=float(sol.t_events[1][0])
errors=[]
for t in np.linspace(0,T,31):
    err=np.max(np.abs(sol.sol(t)[n:]-b_spectral(t)))
    errors.append(float(err));check(err<1e-9)
check(b0[0]<e<b0[1])
check(Tsecond<T-.5)
check(sol.sol(Tsecond)[n]>.9)
# Complete Lyapunov budget, plus original lower bound, checked numerically.
Finf=sum((i+1)*lam[n-1-i] for i in range(n))
F0=sum((i+1)*a0[i] for i in range(n))
budget=(F0-Finf)/(2*e*e)
check(0<T<=budget)
check(T>=np.log(max(b0)/e)/(lam[-1]-lam[0]))
print(json.dumps({'status':'PASS','floating_predicates':checks,'scope':'Non-rigorous independent numerical diagnostics only.','quadrature_comparisons':quadrature,'small_tolerance_residuals':asymptotic,'nonmonotone_three_by_three':{'a0':a0.tolist(),'b0':b0.tolist(),'epsilon':e,'max_individual_first_times':Tsecond,'first_simultaneous_time':T,'b1_at_b2_first_crossing':float(sol.sol(Tsecond)[n]),'max_ode_tau_discrepancy':max(errors),'lyapunov_budget':budget}},indent=2))
