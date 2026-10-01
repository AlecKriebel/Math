#!/usr/bin/env python3
"""Exact finite controls for the explicit proof. Not a stochastic simulation or an infinite-event proof."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import json

counts=Counter()
def check(x,group):
    assert x, group
    counts[group]+=1

# Every threshold is an exact fourth power, so all inspected tail probabilities
# and deterministic schedule lengths are rational without rounding.
for n in range(256):
    D=16**(n+2)
    Dnext=16**(n+3)
    tail=Q(1,2**(n+3))
    step=Q(1,2**(n+2))
    p=tail*step/2
    check(Dnext==16*D,'threshold_and_tail')
    check(tail**4*Dnext==1,'threshold_and_tail')
    check(p==Q(1,2**(2*n+6)),'threshold_and_tail')
    check(D*p==4**(n+1),'threshold_and_tail')
    check(0<step<=1 and 0<p<1,'threshold_and_tail')
    check(4**(n+1)>=4*(n+1),'failure_bound_exponents')
    check(Q(1,2**(4*(n+1)))==Q(1,16**(n+1)),'failure_bound_exponents')
check(Q(1,4)*(1-Q(1,15))==Q(7,30),'final_probability_constant')
check(Q(1,16)/(1-Q(1,16))==Q(1,15),'final_probability_constant')

# Direct exact binomial controls for the first two actual stages. The infinite
# tail is justified analytically in PROOF.md, not by expanding large degrees.
for n in range(2):
    D=16**(n+2); p=Q(1,2**(2*n+6))
    check((1-p)**D<=Q(1,16**(n+1)),'direct_binomial_failure')

# Finite stage union bound and deterministic geometric tail identities.
for N in range(1,257):
    f=sum((Q(1,16**(n+1)) for n in range(N)),Q(0))
    check(f==Q(1,15)*(1-Q(1,16**N)),'finite_failure_union')
    check(f<Q(1,15),'finite_failure_union')
    check(Q(1,4)*(1-f)>Q(7,30),'finite_failure_union')

for lam in [Q(1,100),Q(1,7),Q(1,2),Q(1),Q(3,2),Q(7),Q(100)]:
    tau=1/(2*lam)
    total=Q(0)
    guards=tau # root
    for n in range(96):
        ell=Q(1,2**(n+2))/lam
        s=(1-Q(1,2**n))/(2*lam)
        end=s+ell
        check(total==s,'schedule')
        check(end==(1-Q(1,2**(n+1)))/(2*lam),'schedule')
        check(lam*ell==Q(1,2**(n+2)),'schedule')
        check(0<=s<end<tau,'schedule')
        # The newly selected child v_(n+1) is guarded starting at s_n.
        guards+=tau-s
        check(guards==3*tau-2*tau*Q(1,2**(n+1)),'recovery_window_sum')
        check(0<guards<3*tau,'recovery_window_sum')
        for fraction in [Q(1,5),Q(1,3),Q(1,2),Q(4,5)]:
            arrow=s+fraction*ell
            check(s<arrow<end,'finite_infection_path')
            check(arrow>=s and arrow<tau,'finite_infection_path')
            if n:
                prev_start=(1-Q(1,2**(n-1)))/(2*lam)
                check(prev_start<=s<arrow,'finite_infection_path')
        total=end
    check(3*tau==Q(3,2)/lam,'recovery_window_sum')
    check(total<tau and tau-total==tau*Q(1,2**96),'schedule')

# Enumerate a finite first-eligible-child exploration with biased selected
# degrees. The outgoing probe is a distinct independent variable. This is a
# finite control of the conditioning used in the proof, not its replacement.
options=list(product((1,2,3),(0,1)))
for D in range(1,7):
    selected=Counter(); success=0
    for states in product(options,repeat=D):
        first=next((i for i,(degree,arrow) in enumerate(states) if degree>=2 and arrow),None)
        if first is None: continue
        success+=1
        selected[(first,states[first][0])]+=1
    check(Q(success,6**D)==1-Q(2,3)**D,'adaptive_selection_enumeration')
    check(sum(selected.values())==success,'adaptive_selection_enumeration')
    # Each selected vertex has an independent six-outcome outgoing probe.
    # Its qualifying probability remains 1/3 even after conditioning on its
    # index and selected degree; the latter is not uniformly distributed on 1,2,3.
    for key,multiplicity in selected.items():
        outcomes=Counter()
        for degree,arrow in options:
            outcomes[degree>=2 and bool(arrow)]+=multiplicity
        check(Q(outcomes[True],sum(outcomes.values()))==Q(1,3),'fresh_probe_conditioning')
        check(key[1]>=2,'fresh_probe_conditioning')
    check(all(k[1]!=1 for k in selected),'selected_degree_bias_negative_control')

# Exact finite controls of the quenched inheritance contradiction.
for denominator in range(2,33):
    for numerator in range(1,denominator):
        x=Q(numerator,denominator)
        # A toy positive-integer law with mass at 2: the general proof uses the
        # same strict pointwise inequality x^xi <= x, strict whenever xi>=2.
        check(x*x<x,'quenched_inheritance_strictness')
        for weight in [Q(1,10),Q(1,3),Q(3,4),Q(1)]:
            check((1-weight)*x+weight*x*x<x,'quenched_inheritance_strictness')

out={
 'status':'PASS',
 'arithmetic':'exact integers and fractions only',
 'assertions':sum(counts.values()),
 'groups':dict(sorted(counts.items())),
 'theorem_constants':{'root_threshold':256,'root_tail':'1/4','failure_sum_upper':'1/15','ray_probability_lower':'7/30','horizon':'1/(2 lambda)','recovery_exponent':'3/(2 lambda)'},
 'scope':'Finite algebra, schedule, first-eligible-child conditioning controls, and probability-bound constants. No numerical simulation, no sampled huge tree, and no computational certification of infinite-event arguments; those are proved in PROOF.md.'
}
print(json.dumps(out,indent=2,sort_keys=True))
