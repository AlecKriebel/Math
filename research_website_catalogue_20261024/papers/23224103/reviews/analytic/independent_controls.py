"""Independent analytic controls, written before deposited support inspection.

Standard-library exact rational arithmetic only. Finite checks validate algebra,
geometry, and clock controls; the universal Brownian proof is the accompanying
independent-analysis.md. No discrete approximation is used to prove a limit.
"""
from fractions import Fraction as Q
from math import factorial
from datetime import datetime, timezone
import json

checks=[]
def check(value,name):
    if not value: raise RuntimeError(name)
    checks.append(name)

def poly_eval(p,x):
    return sum(v*x**j for j,v in enumerate(p))

def interval_ode_coefficients(length,degree):
    # v(s,a)=sum_n c_n(a)s^n; v''/2=s v, v(s,0)=1,v(s,l)=0.
    answer=[[Q(1),-1/length]]
    for n in range(1,degree+1):
        prev=answer[-1]
        current=[Q(0),Q(0)]+[2*v/Q((j+1)*(j+2)) for j,v in enumerate(prev)]
        current[1]=-poly_eval(current,length)/length
        answer.append(current)
    return answer

def hyperbolic_ratio_coefficients(alpha,length,degree,clock_factor=Q(2)):
    # sinh((l-a)sqrt(2s))/sinh(l sqrt(2s)), sqrt(s) canceled first.
    a=[(length-alpha)**(2*n+1)*clock_factor**n/Q(factorial(2*n+1)) for n in range(degree+1)]
    b=[length**(2*n+1)*clock_factor**n/Q(factorial(2*n+1)) for n in range(degree+1)]
    quotient=[]
    for n in range(degree+1):
        quotient.append((a[n]-sum(b[j]*quotient[n-j] for j in range(1,n+1)))/b[0])
    return quotient

degree=8
for length in map(Q,[1,2,3]):
    coeff=interval_ode_coefficients(length,degree)
    for n,p in enumerate(coeff):
        check(poly_eval(p,Q(0))==(1 if n==0 else 0),f'ODE left boundary l{length} n{n}')
        check(poly_eval(p,length)==0,f'ODE right boundary l{length} n{n}')
        if n:
            second=[p[j+2]*(j+2)*(j+1)/2 for j in range(len(p)-2)]
            check(second==coeff[n-1],f'ODE recurrence l{length} n{n}')
    for fraction in map(Q,['1/10','1/4','1/2','3/4','9/10']):
        alpha=length*fraction
        series=hyperbolic_ratio_coefficients(alpha,length,degree)
        check(series==[poly_eval(p,alpha) for p in coeff],f'ODE versus hyperbolic ratio l{length} a{alpha}')
        reflected=[poly_eval(p,length-alpha) for p in coeff]
        check(series[0]+reflected[0]==1,f'exit place masses l{length} a{alpha}')
        check(-(series[1]+reflected[1])==alpha*(length-alpha),f'exit mean normalization l{length} a{alpha}')
        wrong=hyperbolic_ratio_coefficients(alpha,length,degree,Q(4))
        check(wrong[1]==2*series[1] and wrong[1]!=series[1],f'wrong diffusivity rejected l{length} a{alpha}')

def component(targets,z):
    targets=sorted(set(targets))
    assert z not in targets and targets
    left=max([a for a in targets if a<z],default=targets[-1]-1)
    right=min([a for a in targets if a>z],default=targets[0]+1)
    return left,right,z-left,right-left,left%1,right%1

left,right,alpha,length,q0,q1=component([Q(3,4)],Q(1,4))
check(length==1 and alpha==Q(1,2) and q0==q1==Q(3,4),'singleton endpoints identified but masses add to one')
left,right,alpha,length,q0,q1=component([Q(1,4),Q(3,4)],Q(0))
check((left,right,alpha,length)==(Q(-1,4),Q(1,4),Q(1,4),Q(1,2)),'wrapped component geometry')
check(q0==Q(3,4) and q1==Q(1,4),'wrapped endpoint identities')
_,_,_,_,q0,q1=component([Q(1,5),Q(2,5),Q(4,5)],Q(0))
check(Q(2,5) not in (q0,q1),'impossible next-target order factor is zero')
_,_,alpha,length,_,_=component([Q(3,4)],Q(1,4))
check(alpha==Q(1,2) and length==1,'previously visited query is removed rather than absorbing')

def physical_times(order,increments):
    running=Q(0); times={}
    for query,u in zip(order,increments):
        running+=u;times[query]=running
    return times

orders=[(1,2),(2,1)]
increments=[(Q(2),Q(100)),(Q(3),Q(1))]
times=[physical_times(o,u) for o,u in zip(orders,increments)]
owners=tuple(min(range(2),key=lambda i:times[i][j])+1 for j in [1,2])
wrong_times=[dict(zip(o,u)) for o,u in zip(orders,increments)]
wrong_owners=tuple(min(range(2),key=lambda i:wrong_times[i][j])+1 for j in [1,2])
check(owners==(1,2),'cumulative physical clock owner event')
check(wrong_owners==(2,2) and owners!=wrong_owners,'increment-only clock counterexample detected')
check(times==[{1:Q(2),2:Q(102)},{2:Q(3),1:Q(4)}],'physical clock values exact')

# Bounded-support coefficient control: a deterministic measurable ownership
# partition with lengths 1/4,3/4. Query expansion is an ordinary product integral.
for theta in [(Q(0),Q(0)),(Q(1),Q(1)),(Q(2),Q(5)),(Q(7,3),Q(0))]:
    lengths=(Q(1,4),Q(3,4)); Z=sum(a*b for a,b in zip(theta,lengths))
    for m in range(9):
        moment=sum(Q(factorial(m),factorial(j)*factorial(m-j))*
                   theta[0]**j*theta[1]**(m-j)*lengths[0]**j*lengths[1]**(m-j)
                   for j in range(m+1))
        check(moment==Z**m and Q(0)<=moment<=max(theta)**m,
              f'query product moment and max bound theta{theta} m{m}')

print(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),
                  'all_passed':True,'exact_check_count':len(checks),
                  'method':'independent exact Fraction ODE/series, circle geometry, cumulative clock and bounded-support algebra',
                  'proof_role':'finite algebra controls only; universal Brownian proof is analytic',
                  'checks':checks},indent=2))
