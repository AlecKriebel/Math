"""Independent exact finite controls for the PR239 martingale/coarse-scale audit.
Uses only authored formulas and stdlib; does not import any submission code.
Finite controls supplement, and do not replace, the analytic derivation.
"""
from fractions import Fraction as F
from collections import defaultdict, Counter
from itertools import product
from math import comb, factorial, ceil
import json

C=Counter()
def check(v,label):
    if not v:
        raise AssertionError(label)
    C[label]+=1

LAWS=[
    ((F(1,7),F(5,7)),(F(2,5),F(3,5))),
    ((F(1,101),F(100,101)),(F(3,7),F(4,7))),
    ((F(1,6),F(1,2),F(5,6)),(F(1,3),F(1,3),F(1,3))),
    ((F(2,7),),(F(1),)),
]
def constants(law):
    ps,ws=law
    q=sum(p*w for p,w in zip(ps,ws))
    a=q*(1-q)
    d=sum(w*p*(1-p) for p,w in zip(ps,ws))
    sig=sum(w*(p-q)**2 for p,w in zip(ps,ws))
    check(0<d<=a<=F(1,4),'elliptic_fixed_law_parameters')
    check(sig==a-d,'exact_parameter_decomposition')
    return q,a,d,sig

KERNELS=[]
for law in LAWS:
    q,a,d,sig=constants(law)
    u={0:F(1)}
    us=[u]
    for n in range(70):
        v={j:u.get(j,F(0))-u.get(j+1,F(0)) for j in range(n+2)}
        nxt={}
        for j in range(-n-1,n+2):
            h=d if j==0 else a
            nxt[j]=(1-2*h)*u.get(j,F(0))+h*(u.get(j-1,F(0))+u.get(j+1,F(0)))
        check(nxt[0]-nxt.get(1,F(0))==(1-2*d-a)*v[0]+a*v[1],
              'boundary_backward_difference_identity')
        for j in range(1,n+2):
            lhs=nxt.get(j,F(0))-nxt.get(j+1,F(0))
            rhs=a*v.get(j-1,F(0))+(1-2*a)*v.get(j,F(0))+a*v.get(j+1,F(0))
            check(lhs==rhs,'interior_backward_difference_identity')
        for j in range(n+2):
            check(nxt.get(j,F(0))==nxt.get(-j,F(0)),'backward_kernel_symmetry')
            check(nxt.get(j,F(0))>=nxt.get(j+1,F(0)),'backward_kernel_radial_monotonicity')
            check(nxt.get(j,F(0))<=nxt[0],'backward_kernel_origin_maximum')
        check(nxt[0]<=u[0],'lazy_reversible_return_monotonicity')
        u=nxt
        us.append(u)
    KERNELS.append(us)

def children(mu,law):
    ps,ws=law
    sites=tuple(sorted(mu))
    for labels in product(range(len(ps)),repeat=len(sites)):
        prob=F(1)
        new=defaultdict(F)
        env={}
        for x,j in zip(sites,labels):
            p=ps[j]
            prob*=ws[j]
            env[x]=p
            new[x+1]+=mu[x]*p
            new[x-1]+=mu[x]*(1-p)
        yield prob,dict(new),env

# Conditional-future integration begins from arbitrary old laws, including
# profiles that are not obtained by the submitted walk. This directly checks
# the claimed uniform dependence on an exposed past.
INITIALS=[
    ({0:F(1)},3),
    ({-2:F(1,2),0:F(1,3),2:F(1,6)},2),
    ({-1:F(3,7),3:F(4,7)},2),
]
for law,us in zip(LAWS,KERNELS):
    for initial,depth in INITIALS:
        I0=sum(v*v for v in initial.values())
        states=[(F(1),initial,I0)]
        for t in range(depth+1):
            total=sum(w for w,mu,V in states)
            check(total==1,'future_environment_total_probability')
            overlap=sum(w*sum(v*v for v in mu.values()) for w,mu,V in states)
            predicted=sum(px*py*us[t].get((x-y)//2,F(0))
                          for x,px in initial.items() for y,py in initial.items())
            check(overlap==predicted,'arbitrary_past_conditional_replica_identity')
            check(overlap<=us[t][0],'arbitrary_past_conditional_overlap_bound')
            A=sum(us[j][0] for j in range(t+1))
            for k in range(1,9):
                moment=sum(w*V**k for w,mu,V in states)
                check(moment<=factorial(k)*A**k,'arbitrary_past_occupation_moment_bound')
            if t<depth:
                new=[]
                for w,mu,V in states:
                    for p,nxt,env in children(mu,law):
                        new.append((w*p,nxt,V+sum(v*v for v in nxt.values())))
                states=new

def average_test(mu,t,q,f):
    val=F(0)
    for x,w in mu.items():
        for j in range(t+1):
            val+=w*F(comb(t,j))*q**j*(1-q)**(t-j)*f(x+2*j-t)
    return val

# Full layer-exposure increment and conditional variance, with biased,
# symmetric, near-arrow and deterministic strictly elliptic laws.
N=3
tests=[
    lambda x:F(1) if x>=0 else F(-1),
    lambda x:F(1) if x%3==0 else F(-1),
    lambda x:max(F(0),min(F(1),F(1)-abs(F(x)-F(1,3))/F(7,3))),
    lambda x:F((x*x+3*x+1)%5,2)-1,
]
for law in LAWS:
    q,a,d,sig=constants(law)
    level=[{0:F(1)}]
    for s in range(N):
        following=[]
        for mu in level:
            for f in tests:
                old=average_test(mu,N-s,q,f)
                gradients={x:average_test({x+1:F(1)},N-s-1,q,f)
                             -average_test({x-1:F(1)},N-s-1,q,f) for x in mu}
                mean=F(0)
                variance=F(0)
                for p,nxt,env in children(mu,law):
                    inc=average_test(nxt,N-s-1,q,f)-old
                    formula=sum(mu[x]*(env[x]-q)*gradients[x] for x in mu)
                    check(inc==formula,'exact_layer_martingale_increment')
                    check(abs(inc)<=max(abs(v) for v in gradients.values()),
                          'layer_increment_oscillation_bound')
                    mean+=p*inc
                    variance+=p*inc**2
                check(mean==0,'conditional_layer_increment_centering')
                predicted=sig*sum(mu[x]**2*gradients[x]**2 for x in mu)
                check(variance==predicted,'conditional_layer_quadratic_variance')
            for p,nxt,env in children(mu,law):
                following.append(nxt)
        level=following

# A parity-sensitive residue control, checked as an inequality on the actual
# physical lattice, not by treating that lattice as aperiodic.
for n in range(1,26):
    for q in (F(2,9),F(1,2),F(19,23)):
        p={2*j-n:F(comb(n,j))*q**j*(1-q)**(n-j) for j in range(n+1)}
        peak=max(p.values())
        tv=sum(abs(p.get(x,F(0))-p.get(x-2,F(0))) for x in range(-n,n+3,2))
        check(tv==2*peak,'parity_binomial_shift_total_variation')
        for M in range(1,18):
            for residue in range(M):
                mass=sum(w for x,w in p.items() if x%M==residue)
                check(mass<=F(2,M)+2*peak,'uniform_physical_residue_bound')

def distance_to_grid(z,M):
    rem=z%M
    return min(rem,M-rem)
def cell(z,align,M):
    return (z-align)//M

# Exact rational alignments and biased nonintegral translations.
for M in range(5,23):
    r=F(M,10)
    for align in (F(0),F(1,7),F(-11,6)):
        for q in (F(2,9),F(1,2),F(19,23)):
            for ell in (1,3,6):
                shift=(2*q-1)*ell
                fb={}
                for x in range(M):
                    z=distance_to_grid(F(x)+shift-align,M)
                    fb[x]=max(F(0),min(F(1),2-z/r))
                check(sum(v>0 for v in fb.values())<=ceil(4*r)+2,
                      'alignment_uniform_boundary_residue_count')
                for x in range(-30,31):
                    z=F(x)+shift
                    dist=distance_to_grid(z-align,M)
                    fx=fb[x%M]
                    check(dist>r or fx==1,'boundary_majorant')
                    fy=fb[(x+1)%M]
                    check(abs(fx-fy)<=1/r,'periodic_boundary_lipschitz')
                    for y in range(x-ell,x+ell+1):
                        if dist>r and abs(F(y)-z)<=r:
                            check(cell(F(y),align,M)==cell(z,align,M),
                                  'translated_endpoint_same_cell_off_boundary')
                n=12
                p={2*j-n:F(comb(n,j))*q**j*(1-q)**(n-j) for j in range(n+1)}
                peak=max(p.values())
                expectation=sum(w*fb[x%M] for x,w in p.items())
                count=sum(v>0 for v in fb.values())
                check(expectation<=count*(F(2,M)+2*peak),
                      'boundary_majorant_expectation_from_residues')

for N in range(2,81):
    for ell in range(1,N//2+1):
        blocks=defaultdict(list)
        for s in range(N-ell):
            t=N-s-1
            j=(t//ell).bit_length()-1
            blocks[j].append(s)
        check(sorted(x for B in blocks.values() for x in B)==list(range(N-ell)),
              'dyadic_exact_time_cover')
        for j,B in blocks.items():
            h=2**j*ell
            check(B==list(range(min(B),max(B)+1)),'dyadic_contiguous_deterministic_block')
            check(len(B)<=h,'dyadic_block_length_bound')
            check(all(N-s>=h for s in B),'dyadic_variance_denominator_bound')

for d in [F(1,10**6),F(1,20000),F(1,100)]+[F(k,200) for k in range(1,50)]:
    gamma=F(1,4)+d
    beta=(gamma+F(1,4))/2
    eta=(gamma-F(1,4))/4
    check(F(1,4)<beta<gamma<F(1,2),'fixed_gamma_parameter_order')
    check(beta-eta-(F(1,2)-gamma)==5*d/4>0,'sign_entropy_power_margin')
    check(2*beta-F(1,2)-eta==3*d/4>0,'boundary_concentration_power_margin')
    check(gamma-beta==d/2,'uniform_scale_ratio_power_margin')
for u,w,b in product((F(1,1000),F(1,7),F(1),F(30)),repeat=3):
    lam=u/(2*(w+b*u))
    check(0<lam*b<=F(1,2),'scalar_exponential_domain')
    check(lam*u-lam*lam*w>=u*u/(4*(w+b*u)),
          'scalar_joint_event_exponential_constant')

# Controls intentionally falsifying omitted hypotheses; these are not models
# being used to prove the theorem.
a=F(1,4)
invalid_delta=F(1,2)
check(1-2*invalid_delta<a,'origin_maximum_can_fail_when_delta_exceeds_a')
arrow_mass={0:F(1)}
for n in range(1,36):
    new=defaultdict(F)
    for x,wgt in arrow_mass.items():
        step=F(0) if x==0 else a
        new[x]+=wgt*(1-2*step)
        new[x-1]+=wgt*step
        new[x+1]+=wgt*step
    arrow_mass={x:wgt for x,wgt in new.items() if wgt}
    check(arrow_mass=={0:F(1)},'zero_delta_arrow_overlap_does_not_decay')
signs=[(F(x),F(y)) for x,y in product((-1,1),repeat=2)]
good=[(x,y) for x,y in signs if x+y>0]
check(sum(x for x,y in good)/len(good)>0,'future_conditioning_does_not_preserve_martingale_centering')

print(json.dumps({
    "schema":"independent-pr239-martingale-exact-finite-controls-v1",
    "status":"PASS",
    "exact_assertions":sum(C.values()),
    "families":dict(sorted(C.items())),
    "submission_code_imported":False,
    "random_simulations":False,
    "finite_controls_replace_analytic_proof":False,
},indent=2,sort_keys=True))

