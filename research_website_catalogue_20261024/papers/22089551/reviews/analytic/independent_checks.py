"""Independent finite checks. No imports from manuscript verification code."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from collections import deque, Counter
import json, math, datetime

OUT=Path(__file__).resolve().parent

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def ff(x,y):
    if any(a<b for a,b in zip(x,y)):return 0
    return math.prod(math.prod(range(a-b+1,a+1)) for a,b in zip(x,y))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def polynomial_add(a,b,scale=F(1)):
    z=dict(a)
    for k,v in b.items():z[k]=z.get(k,F(0))+scale*v
    return {k:v for k,v in z.items() if v}
def log_factorial(n):
    c=Counter()
    for j in range(2,n+1):
        v=j;p=2
        while p*p<=v:
            while v%p==0:c[p]+=1;v//=p
            p+=1
        if v>1:c[v]+=1
    return dict(c)
def potential(x,t):
    z={}
    for n in sub(x,t):z=polynomial_add(z,log_factorial(n))
    return z
def log_ratio(a,b):
    z={}
    for v,sgn in [(a,1),(b,-1)]:
        p=2
        while p*p<=v:
            while v%p==0:z[p]=z.get(p,F(0))+sgn;v//=p
            p+=1
        if v>1:z[v]=z.get(v,F(0))+sgn
    return {p:v for p,v in z.items() if v}

# Graph-free falsification of the top-complex claim. Search for a strict-weight
# enabled pair directly; if none exists, independently search a small integer
# nullspace certificate, rather than implement the manuscript's case split.
d=3
all_complexes=[c for c in product(range(3),repeat=d) if sum(c)<=2]
directions=[a for a in product([-1,0,1],repeat=d) if any(a)]
top_counts=Counter();scenarios=0
for mask in range(1,1<<len(all_complexes)):
    C=[c for j,c in enumerate(all_complexes) if (mask>>j)&1]
    if len(C)<2:continue
    for imask in range(1,1<<d):
        I=[i for i in range(d) if (imask>>i)&1]
        B=[i for i in range(d) if i not in I]
        for wI in product(range(3),repeat=len(I)):
            if not any(wI):continue
            w=tuple(wI[I.index(i)] if i in I else 0 for i in range(d))
            h={c:dot(w,c) for c in C}
            for b in product(range(3),repeat=len(B)):
                rho=tuple(4 if i in I else b[B.index(i)] for i in range(d))
                scenarios+=1
                witness=any(h[s]>h[c] and ff(add(rho,c),s)>0 for s in C for c in C)
                if witness:top_counts['higher_weight_enabled_witness']+=1;continue
                cert=next((a for a in directions+[w]
                           if all(a[i]>=0 for i in I) and any(a[i]>0 for i in I)
                           and len({dot(a,c) for c in C})==1),None)
                assert cert is not None,(C,I,w,b)
                top_counts['independently_found_diverging_invariant']+=1

# Exact symbolic logarithms are stored as rational coefficients of log(prime).
# This permits exact equality of endpoint enumeration and episode recursion.
O=(0,0);A=(1,0);B=(0,1);AB=(1,1);AA=(2,0)
channels=[(O,AB,F(2)),(AB,B,F(3)),(B,A,F(5)),(A,AA,F(7)),
          (AA,O,F(11)),(O,AB,F(13)),(O,B,F(17)),(A,AB,F(19))]
C=[O,A,B,AB,AA]
def transitions(x):
    rates=[k*ff(x,s) for s,u,k in channels];total=sum(rates)
    return [(i,r/total,add(sub(x,s),u),u,s) for i,((s,u,k),r) in enumerate(zip(channels,rates)) if r]
def path(t,c):
    q=deque([(t,[]) ]);seen={t}
    while q:
        y,p=q.popleft()
        if y==c:return p
        for j,(s,u,k) in enumerate(channels):
            if s==y and u not in seen:seen.add(u);q.append((u,p+[j]))
def delta(x,t):
    val={}
    for _,p,z,u,s in transitions(x):
        jump=polynomial_add(potential(z,u),potential(x,t),F(-1))
        assert jump==log_ratio(ff(x,t),ff(x,s))
        val=polynomial_add(val,jump,p)
    return val
def recursive(rho,t,P,k=0):
    x=add(rho,t);v=delta(x,t)
    if k==len(P):return v
    channel=P[k]
    p=next(p for j,p,z,u,s in transitions(x) if j==channel)
    u=channels[channel][1]
    return polynomial_add(v,recursive(rho,u,P,k+1),p)
def enumerate_episode(rho,t,P):
    initial=potential(add(rho,t),t);acc={};terminal_mass=F(0)
    def visit(x,t,k,weight):
        nonlocal acc,terminal_mass
        for j,p,z,u,s in transitions(x):
            w=weight*p
            if k<len(P) and j==P[k]:visit(z,u,k+1,w)
            else:
                terminal_mass+=w
                reward=polynomial_add(potential(z,u),initial,F(-1))
                acc=polynomial_add(acc,reward,w)
    visit(add(rho,t),t,0,F(1))
    assert terminal_mass==1
    return acc
episodes=0
for rho in product(range(4),repeat=2):
    for t,c in product(C,repeat=2):
        P=path(t,c)
        assert recursive(rho,t,P)==enumerate_episode(rho,t,P)
        episodes+=1

# Scalar envelope: sampled values lie below the derived optimum, including
# both branches and arbitrarily small continuation probabilities.
envelope_tests=0;C0=3.1
for q in [.01,.2,1.0]:
    for M in [10,0,-.5,-1/q,-2/q,-1e6]:
        bound=C0+q*M if M>=-1/q else C0-1-math.log(-q*M)
        optimum=1 if M>=-1/q else -1/(q*M)
        assert abs(math.log(optimum)+C0+q*optimum*M-bound)<1e-10
        for p in [1, .9,.1,.001,1e-9,optimum]:
            assert math.log(p)+C0+q*p*M<=bound+1e-10
            envelope_tests+=1

# Direct source-probability evaluation of the unit-rate attenuation family.
attenuation=[]
for d in range(2,6):
    N=10**6
    u=N*(N-1);v=(N+2)*(N+1)
    den=1+v+(d-1)*u
    phase_delta=((d-1)*u*math.log(v/u)+math.log(v))/den
    continue_p=v/den
    terminal_delta=-d*u/(1+d*u)*math.log(u)
    J=terminal_delta
    for _ in range(d):J=phase_delta+continue_p*J
    leading=-2/(d**d)
    assert abs(J/math.log(N)-leading)<3e-6
    attenuation.append({'d':d,'D0_over_logN':J/math.log(N),'limit':leading})

out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'passed':True,'top_complex_scenarios':scenarios,'top_complex_outcomes':dict(top_counts),
     'exact_symbolic_episode_cases':episodes,'scalar_envelope_checks':envelope_tests,
     'unit_rate_attenuation':attenuation,
     'scope':'Independent finite falsification controls; no code from paper imported; finite cases do not prove recurrence or enumerate K.'}
(OUT/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
