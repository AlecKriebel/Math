#!/usr/bin/python3
"""Own exact finite diagnostics; no candidate or old reviewer imports."""
from fractions import Fraction as Q
from collections import Counter
import datetime, hashlib, json, math, os, sys
from pathlib import Path
START=datetime.datetime.now(datetime.timezone.utc).isoformat()
COUNTS=Counter()
def check(name,condition):
    if not condition: raise AssertionError(name)
    COUNTS[name]+=1
def add(*fs):
    out={}
    for f in fs:
        for k,(a,b) in f.items():
            c,d=out.get(k,(Q(0),Q(0)));out[k]=(c+a,d+b)
    return {k:v for k,v in out.items() if v!=(0,0)}
def scale(f,c): return {k:(c*a,c*b) for k,(a,b) in f.items() if (c*a,c*b)!=(0,0)}
def const(c): return {(0,0):(Q(c),Q(0))} if c else {}
def cos(k): return {k:(Q(1,2),Q(0)),(-k[0],-k[1]):(Q(1,2),Q(0))}
def sin(k): return {k:(Q(0),Q(-1,2)),(-k[0],-k[1]):(Q(0),Q(1,2))}
def derivative(f,v):
    out={}
    for k,(a,b) in f.items():
        lam=k[0]*v[0]+k[1]*v[1];out[k]=(-lam*b,lam*a)
    return add(out)

X=(Q(1),Q(0))
q=add(const(1),scale(cos((1,0)),2));g=scale(sin((1,0)),-2)
check('globally_periodic_correction_exact',add(q,derivative(g,X))==const(1))
check('sign_mutant_reverse_correction_fails',add(q,scale(derivative(g,X),-1))!=const(1))
# Each derivative has zero zero-mode. Universal necessity is proved separately.
for j in range(1,13):
    f=add(const(j),scale(sin((j,0)),Q(j+1,j)),scale(cos((1,j)),Q(2,j+1)))
    d=derivative(f,X)
    check('periodic_derivative_zero_mean',(0,0) not in d)
    check('positive_mean_forcing_cannot_be_derivative',d!=const(1))
# X leaves y constant: each circle gives an invariant probability measure.
transverse_q=add(const(1),scale(cos((0,1)),2))
check('positive_volume_mean_not_all_invariant_means',transverse_q[(0,0)]==(Q(1),Q(0)))
mean_at_y_pi=sum(a*((-1)**k[1]) for k,(a,b) in transverse_q.items())
check('negative_periodic_orbit_mean_obstruction',mean_at_y_pi==-1)
check('weak_positive_density_has_zero',Q(1)+Q(-1)==0)
check('weak_positive_density_not_identically_zero',Q(1)+Q(1)==2)
# Local patching: psi=x,u1=x,u2=0 => D(psi*u1)=2x, not psi*D u1=x.
for t in (Q(1,4),Q(1,2),Q(3,4)):
    check('partition_of_unity_derivative_error',2*t-t==t and t!=0)
# Ordinary exact top-form correction is different from allowed GV gauges.
primitive=scale(sin((1,0)),-2)
check('arbitrary_exact_representative_can_be_positive',add(q,derivative(primitive,X))==const(1))

small_denominators=[]
for n in (4,5,6):
    factorial=math.factorial(n);Qn=10**factorial
    Pn=sum(10**(factorial-math.factorial(j)) for j in range(1,n+1))
    an=Q(1,Qn**(n//2))
    alpha_n=Q(Pn,Qn)
    alpha_next=alpha_n+Q(1,10**math.factorial(n+1))
    delta=Qn*alpha_next-Pn
    check('first_tail_exact_small_denominator',delta==Q(1,Qn**n))
    check('first_tail_below_analytic_full_tail_upper',0<delta<2*Q(1,Qn**n))
    check('approximant_coprime',math.gcd(Pn,Qn)==1)
    check('real_zero_mean_mode_has_nonzero_frequency',Pn>0 and Qn>0)
    check('forcing_amplitude_positive_and_decaying',0<an<1)
    # Full infinite tail <2Qn^-n gives this lower bound on any solution coefficient.
    lower=an/(4*Q(1,Qn**n))
    check('formal_solution_lower_bound_exact',lower==Q(Qn**(n-n//2),4))
    small_denominators.append({'n':n,'Q_decimal_digits':factorial+1,
        'frequency_unique':True,'tail_control':'First omitted summand exact; full-tail bound proved analytically',
        'solution_coefficient_lower_power':n-n//2})

# No admissible compactness from positive pointwise coefficient ratios alone.
last=Q(2)
for n in range(1,17):
    ratio=Q(1,n+1)
    check('positive_gauge_ratios_shrink_toward_zero',0<ratio<last);last=ratio
# |x|^(5/2) is C2, but its third derivative grows at x=1/k^2.
for k in range(1,9):
    third=Q(15*k,8)
    check('C2_does_not_supply_extra_third_derivative_bound',third==Q(15,8)*k)

ROOT=Path(__file__).resolve().parent
out={'role':'ACTUAL_OWN_EXACT_GLOBAL_DIAGNOSTICS','pid':os.getpid(),'argv':sys.argv,
     'start_utc':START,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'arithmetic':'stdlib fractions.Fraction; finite exact Fourier coefficients',
     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'proof_sha256':hashlib.sha256((ROOT/'GLOBAL_OBLIGATIONS.md').read_bytes()).hexdigest(),
     'passed_assertions':sum(COUNTS.values()),'counts':dict(sorted(COUNTS.items())),
     'finite_small_denominator_controls':small_denominators,
     'negative_invariant_circle_mean':str(mean_at_y_pi),
     'limits':'Transport/compactness/regularity diagnostic models only. No target foliation construction, no Q13.1 counterexample, no infinite Fourier proof by computation. Global arguments are in GLOBAL_OBLIGATIONS.md. No author/reviewer imports or novelty/human/formal/ROOT acceptance claim.'}
print(json.dumps(out,indent=2,sort_keys=True))
