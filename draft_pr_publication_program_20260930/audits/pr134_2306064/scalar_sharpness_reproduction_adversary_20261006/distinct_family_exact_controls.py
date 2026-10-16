#!/usr/bin/env python3
"""Additional finite falsification controls, not a proof by sampling."""
from fractions import Fraction as R
from collections import Counter
from pathlib import Path
from hashlib import sha256
import datetime, json, os

counts = Counter()
def check(label, condition):
    if not condition:
        raise RuntimeError(label)
    counts[label] += 1

# Plain pairs, with no imported original checker implementation.
def add(x,y): return x[0]+y[0], x[1]+y[1]
def scale(s,x): return s*x[0], s*x[1]
def mul(x,y): return x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]
def div(x,y):
    d=y[0]*y[0]+y[1]*y[1]
    if not d: raise ZeroDivisionError('Gaussian denominator')
    return (x[0]*y[0]+x[1]*y[1])/d, (x[1]*y[0]-x[0]*y[1])/d
def norm(x): return x[0]*x[0]+x[1]*x[1]
def power(x,n):
    y=(R(1),R(0))
    for _ in range(n): y=mul(y,x)
    return y

directions=[(R(1),R(0)),(R(-1),R(0)),(R(0),R(1)),(R(0),R(-1)),
            (R(5,13),R(12,13)),(R(-20,29),R(21,29))]
for direction in directions: check('phase_unit_norm',norm(direction)==1)

def jet(alpha, coeff, z):
    p=(R(1),R(0)); g=(R(1),R(0)); h=(R(0),R(0))
    for n,c in coeff.items():
        v=mul(c,power(z,n-1)); p=add(p,v); g=add(g,scale(n,v)); h=add(h,scale(n*(n-1),v))
    check('nonzero_sample_denominators',norm(p)>0 and norm(g)>0)
    return add(scale(1-alpha,div(g,p)),scale(alpha,add((R(1),R(0)),div(h,g))))

ks=[R(1,10**6),R(1,1000),R(1,10),R(1,2),R(1),R(2),R(100),R(10**6)]
params=[(R(0),R(0),'zero')]
for k in ks:
    params.append((-2*k*k/(3*k+1),k,'negative'))
    params.append((2*k*k/(1+k) if k<=1 else 2*k*(k+1)/(3*k+1),k,
                   'interior' if k<=1 else 'above_one'))
templates=[{2:1},{17:1},{2:1,4:2,7:3,17:5}]
evaluations=0
for alpha,k,branch in params:
    a,b=abs(1-alpha),abs(alpha)
    check('all_real_parameter_identity',2*k*k-(a+2*b-1)*k-b==0)
    check('branch_domain', branch=='zero' and alpha==0 or branch=='negative' and alpha<0 or
          branch=='interior' and 0<alpha<=1 or branch=='above_one' and alpha>1)
    if k: check('scalar_supremum_one',a/(1+2*k)+b/k==1)
    for template in templates:
        for budget in [R(0),R(1,3),R(1)]:
            total=sum(template.values())
            amps={n:budget*R(raw,total)/(n*(1+k*(n-1))) for n,raw in template.items()}
            check('coefficient_budget',sum(n*(1+k*(n-1))*v for n,v in amps.items())==budget)
            for assignment in range(len(directions)):
                coeff={n:scale(v,directions[(assignment+i)%len(directions)]) for i,(n,v) in enumerate(amps.items())}
                for radius in [R(0),R(1,2),R(9,10),R(999,1000)]:
                    z=scale(radius,directions[(assignment+2)%len(directions)])
                    val=jet(alpha,coeff,z); evaluations+=1
                    check('positive_real_part',val[0]>0)
                    check('unit_centered_disk',norm(add(val,(R(-1),R(0))))<1)
                    A=sum(v*radius**(n-1) for n,v in amps.items())
                    B=sum(n*v*radius**(n-1) for n,v in amps.items())
                    X=B-A;Y=sum(n*(n-1)*v*radius**(n-1) for n,v in amps.items())
                    check('localized_moment_order',A<=B/2 and Y>=2*X)
                    check('localized_strict_budget',B+k*Y<1)
                    majorant=a*X/(1-A)+(b*Y/(1-B) if b else 0)
                    check('localized_scalar_strict',majorant<1)
                    check('complex_majorant',norm(add(val,(R(-1),R(0))))<=majorant*majorant)

witnesses=0
for k in ks:
    if k>1: continue
    alpha=2*k*k/(1+k);star=1/(2*(1+k))
    for factor in [R(0),R(1,2),R(99999999,100000000)]:
        lam=factor*k;upper=min(R(1,2),1/(2*(1+lam)));c=(star+upper)/2
        z=(star/c+1)/2;x=c*z
        check('arbitrarily_close_weaker_weight',0<=lam<k and 2*(1+lam)*c<1)
        check('interior_sharpness_domain',0<star<c<R(1,2) and 0<z<1)
        val=jet(alpha,{2:(-c,R(0))},(z,R(0)))
        quotient=(1-(4+alpha)*x+4*x*x)/((1-x)*(1-2*x))
        check('quadratic_exact_counterexample',val==(quotient,R(0)) and quotient<0)
        witnesses+=1

for N in [2,3,4,7,17,101]:
    m=N-1
    for lam in [R(1,1000),R(1,2),R(1)]:
        alpha=N*lam*lam/(1+m*lam);star=1/(N*(1+lam*m))
        check('degree_N_parameter_domain',0<alpha<=1)
        check('degree_N_boundary_root',1-(2*N+alpha*m*m)*star+N*N*star*star==0)
        for x in [R(0),star/2,star,R(-1,10*N)]:
            direct=1-m*(1-alpha)*x/(1-x)-alpha*N*m*x/(1-N*x)
            formula=(1-(2*N+alpha*m*m)*x+N*N*x*x)/((1-x)*(1-N*x))
            check('degree_N_rational_identity',direct==formula)

# A genuine alpha=0 edge family with finite first and divergent second moment:
# t_n=1/[n^2(n-1)], B_N=1-1/N, Y_N=sum(n=2..N)1/n.
for N in [2,3,10,100,1000]:
    first=sum((R(1,n*(n-1)) for n in range(2,N+1)),R(0))
    second=sum((R(1,n) for n in range(2,N+1)),R(0))
    check('alpha_zero_telescoping_first_moment',first==1-R(1,N))
    check('alpha_zero_second_partial_moment',second>0)

naive=jet(R(1,2),{2:(R(-8,25),R(0))},(R(31,32),R(0)))
check('exact_naive_witness',naive==(R(-53,1311),R(0)))
output={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),
        'pid':os.getpid(),'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'parameter_cases':len(params),'complex_evaluations':evaluations,'quadratic_witnesses':witnesses,
        'exact_controls':sum(counts.values()),'categories':dict(counts),
        'scope':'Finite rational falsification diagnostics; universal deductions and infinite-moment edge reasoning are in INITIAL_MATH_VERDICT.md and AUDIT.md. No priority or additional proof-search claim.'}
print(json.dumps(output,indent=2,sort_keys=True))
