"""Fresh exact finite controls for PR239. No imports of historical checkers.
Ballot first-passage/renewal, rational maximal martingales, and formal path
dependency sets complement the prior recurrence/substitution controls.
These finite cases do not prove any infinite or asymptotic assertion.
"""
from fractions import Fraction as Q
from collections import defaultdict, Counter
from itertools import product
from math import comb
import json

counts = Counter()
def check(value, family):
    if not value:
        raise AssertionError(family)
    counts[family] += 1

def first_hit_ballot(t, a):
    # Last step must move, hence holds occupy only the preceding t-1 slots.
    if t == 0:
        return Q(0)
    return sum((Q(comb(t-1, m-1) * (comb(m-1, (m-1)//2)//((m+1)//2))) *
                a**m * (1-2*a)**(t-m)
                for m in range(1, t+1, 2)), Q())

def killed_first_hit(tmax, d, a):
    law = {d: Q(1)}
    hits = [Q(0)]
    for t in range(1, tmax+1):
        nxt = defaultdict(Q)
        hit = Q()
        for x, weight in law.items():
            for y, p in ((x-1, a), (x, 1-2*a), (x+1, a)):
                if y == 0:
                    hit += weight*p
                else:
                    nxt[y] += weight*p
        hits.append(hit)
        law = dict(nxt)
    return hits

parameters = [(Q(1,1000), Q(1,10000)), (Q(1,1000), Q(1)),
              (Q(1,3), Q(1,100)), (Q(1,2), Q(1)),
              (Q(99,100), Q(1,7)), (Q(7,11), Q(3,4))]
for q, ratio in parameters:
    a = q*(1-q)
    delta = ratio*a
    nmax = 20
    hit = killed_first_hit(nmax, 1, a)
    for t in range(nmax+1):
        check(hit[t] == first_hit_ballot(t, a), "ballot_first_hit_coefficients")
    first_return = [Q(), 1-2*delta] + [2*delta*first_hit_ballot(t-1, a)
                                                 for t in range(2, nmax+1)]
    renewal = [Q(1)]
    for t in range(1, nmax+1):
        renewal.append(sum((first_return[j]*renewal[t-j] for j in range(1, t+1)), Q()))
    # Backward profile is computed for every feasible starting gap; forward
    # return is separately computed below. The ballot renewal uses neither.
    u = {0: Q(1)}
    forward = {0: Q(1)}
    for t in range(nmax+1):
        check(forward.get(0, Q()) == renewal[t], "sticky_return_ballot_renewal")
        check(u.get(0, Q()) == renewal[t], "backward_profile_renewal_agreement")
        for d in range(t+2):
            check(u.get(d, Q()) == u.get(-d, Q()), "sticky_profile_symmetry")
            check(u.get(d, Q()) >= u.get(d+1, Q()) >= 0, "sticky_profile_radial_maximum")
        nxt = defaultdict(Q)
        for x, weight in forward.items():
            move = delta if x == 0 else a
            for y,p in ((x-1,move),(x,1-2*move),(x+1,move)):
                nxt[y] += weight*p
        forward = dict(nxt)
        u = {d:(1-2*(delta if d == 0 else a))*u.get(d,Q()) +
                  (delta if d == 0 else a)*(u.get(d-1,Q())+u.get(d+1,Q()))
             for d in range(-t-1,t+2)}
    for d in range(1,5):
        hit = killed_first_hit(12,d,a)
        free = {0: Q(1)}
        survived = Q(1)
        for t in range(13):
            if t:
                survived -= hit[t]
            check(survived == sum((free.get(j,Q()) for j in range(1-d,d+1)),Q()),
                  "ballot_reflection_survival")
            nxt=defaultdict(Q)
            for x,w in free.items():
                nxt[x-1]+=w*a
                nxt[x]+=w*(1-2*a)
                nxt[x+1]+=w*a
            free=dict(nxt)

# Exact finite Doob-maximal check for the biased Bernoulli exponential
# martingale z^B_t/(1-q+qz)^t, with rational z and thresholds.
# Every path is enumerated; this is deliberately a MAXIMUM event.
maximal_strictly_larger_than_endpoint = False
for q in [Q(1,11),Q(1,2),Q(9,10)]:
    for z in [Q(1,3),Q(3,2),Q(7)]:
        normalizer=1-q+q*z
        n=7
        expectations=[Q() for _ in range(n+1)]
        paths=[]
        for bits in product([0,1],repeat=n):
            weight=q**sum(bits)*(1-q)**(n-sum(bits))
            b=0; values=[Q(1)]
            for t,bit in enumerate(bits,1):
                b+=bit
                values.append(z**b/normalizer**t)
            for t,value in enumerate(values):
                expectations[t]+=weight*value
            paths.append((weight,values))
        for expectation in expectations:
            check(expectation==1,"rational_exponential_martingale_means")
        for threshold in [Q(3,2),Q(2),Q(3),Q(5)]:
            maximal=sum((w for w,vals in paths if max(vals)>=threshold),Q())
            endpoint=sum((w for w,vals in paths if vals[-1]>=threshold),Q())
            check(maximal<=1/threshold,"finite_doob_maximal_bound")
            check(endpoint<=maximal,"maximal_contains_endpoint_event")
            maximal_strictly_larger_than_endpoint |= maximal>endpoint
check(maximal_strictly_larger_than_endpoint,"maximal_endpoint_distinction_negative_control")

# Pure path read-variable geometry. No environment values or forward-kernel
# recursion appear in the tube/strip dependency verification.
geometry_cases=0
exit_and_return_witness=False
for drift in [Q(-99,100),Q(-2,7),Q(0),Q(4,9),Q(99,100)]:
    for radius in [1,2,3,5]:
        for steps in range(1,7):
            for start in [-5,-1,3]:
                influence_sets=set()
                for signs in product([-1,1],repeat=steps):
                    x=start;alive=True;all_positions=[start];read_sites=[]
                    for t,dx in enumerate(signs):
                        if alive:
                            read_sites.append((t,x))
                        x+=dx;all_positions.append(x)
                        if alive and abs(x-start-drift*(t+1))>radius:
                            alive=False
                    for t,y in read_sites:
                        k=(Q(y)-drift*t)//radius
                        influence_sets.add(k)
                    check(all(abs(Q(y)-drift*t-start)<=radius for t,y in read_sites),
                          "alive_read_variables_inside_tube_by_path")
                    check(all(((Q(y)-drift*t)//radius)*radius-radius-1<=start<=
                              (((Q(y)-drift*t)//radius)+1)*radius+radius+1
                              for t,y in read_sites),
                          "read_strips_have_start_in_influence_interval_by_path")
                    endpoint_inside=abs(x-start-drift*steps)<=radius
                    exit_and_return_witness |= endpoint_inside and not alive
                # Include EVERY possible strip around the starting site, not
                # only the sampled reachable set, to test worst-case overlap.
                candidates=range(start//radius-5,start//radius+6)
                count=sum(k*radius-radius-1<=start<=(k+1)*radius+radius+1
                          for k in candidates)
                check(count<=6,"deterministic_influence_overlap_bound")
                geometry_cases+=1
check(exit_and_return_witness,"killed_endpoint_only_negative_control")

# The parameter grid includes deterministic elliptic laws delta=a and very
# small positive ratios. It does not claim to include delta=0 arrow laws.
print(json.dumps({"status":"PASS","exact_assertions":sum(counts.values()),
                  "families":dict(sorted(counts.items())),
                  "parameter_laws":len(parameters),
                  "path_geometry_cases":geometry_cases,
                  "scope":"Finite exact independent ballot/renewal, maximal-martingale and symbolic read-variable geometry controls only. No asymptotic, priority, historical reviewer-independence or publication certification."},
                 indent=2,sort_keys=True))

