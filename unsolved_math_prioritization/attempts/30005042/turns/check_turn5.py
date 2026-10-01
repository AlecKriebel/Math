#!/usr/bin/env python3
"""Exact finite genealogy/jump controls; not a proof of endpoint J1 tightness."""
from fractions import Fraction as F
from itertools import product
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
import hashlib,json
C=Counter()
def ck(p,k):
    assert p,k
    C[k]+=1

# Source-valid single-jump offspring: X(lambda)=1+2*1(U<=lambda),
# U uniform on[1,3]. Finite midpoint quadratures are exact at the grid cuts.
for M in (8,16,32,64):
    times=[1+F(2*j+1,M) for j in range(M)]
    for j in range(M+1):
        lam=1+F(2*j,M)
        ck(sum(F(1+2*int(t<=lam),M) for t in times)==lam,'offspring_mean_at_grid')
        for k in range(j,M+1):
            mu=1+F(2*k,M)
            weighted=sum(F(2,M) for t in times if lam<t<=mu)
            ck(weighted==mu-lam,'expected_marked_jump_measure')

# Actual finite Ulam genealogy, including batch births and inactive parent clocks.
vertices=[()]
for depth in range(1,4):vertices+=list(product((1,2,3),repeat=depth))
times={v:F(3,2)+F((17*i)%101+1,102) for i,v in enumerate(vertices)}
ck(len(set(times.values()))==len(vertices),'intrinsic_times_distinct')
def offspring(v,theta,left=False):
    return 1+2*int(times[v]<theta if left else times[v]<=theta)
def present(v,theta,left=False):
    return all(v[k]<=offspring(v[:k],theta,left) for k in range(len(v)))
def count(v,depth,theta,left=False):
    if depth==0:return 1
    return sum(count(v+(j,),depth-1,theta,left) for j in range(1,offspring(v,theta,left)+1))
inactive=0
for v,theta in times.items():
    k=len(v);active=present(v,theta,True)
    if not active:inactive+=1
    for n in range(5):
        left=count((),n,theta,True);right=count((),n,theta,False)
        if active and n>=k+1:
            added=sum(count(v+(j,),n-k-1,theta,False) for j in (2,3))
            formula=theta**(-k-1)*sum(F(count(v+(j,),n-k-1,theta,False))/theta**(n-k-1) for j in (2,3))
        else:added=0;formula=F(0)
        ck(right-left==added,'exact_batch_population_jump')
        ck(F(right-left)/theta**n==formula,'normalized_descendant_jump_formula')
        ck(right>=left,'all_prelimit_jumps_nonnegative')
    if active:
        ck(F(count((),k+1,theta)-count((),k+1,theta,True))/theta**(k+1)==F(2)/theta**(k+1),'every_active_event_visible')
ck(inactive>0,'inactive_intrinsic_clocks_excluded')

# Geometric all-depth counting bound and an independently summed square bound.
for theta,eta,x in product([F(5,4),F(3,2),F(2),F(7,3),F(3)],[F(1,3),F(1),F(2)],[F(j,3) for j in range(61)]):
    k=0;prefix=F(0)
    while x>eta*theta**(k+1):prefix+=theta**k;k+=1
    ck(prefix<=x/(eta*(theta-1)),'all_depth_macroscopic_count_bound')
    K=0
    while x>theta**(K+1):K+=1
    big=sum((theta**j for j in range(K)),F(0))
    small=x*x*theta**(-K-1)/(theta-1)
    ck(big+small<=2*x/(theta-1),'all_depth_truncated_square_bound')

# Expected generation counts for the real single-jump offspring marginals.
def conv(A,B):
    out=defaultdict(F)
    for x,p in A.items():
        for y,q in B.items():out[x+y]+=p*q
    return out
for theta in [F(5,4),F(3,2),F(2),F(5,2),F(11,4)]:
    p=(theta-1)/2;X={1:1-p,3:p};Z={1:F(1)}
    for k in range(4):
        ck(sum(z*q for z,q in Z.items())==theta**k,'active_parent_intensity')
        ck(sum(Z.values())==1,'generation_probability_mass')
        if k==3:break
        laws=[{0:F(1)}]
        for r in range(max(Z)):laws.append(conv(laws[-1],X))
        out=defaultdict(F)
        for r,pz in Z.items():
            for z,q in laws[r].items():out[z]+=pz*q
        Z=out

# Layer-cake identity integrated exactly for rational envelopes.
for x in [F(j,7) for j in range(40)]:
    endpoint=min(x,F(1))
    ck(endpoint*endpoint==min(x*x,F(1)),'truncated_square_layer_cake')

# Finite dominated l2 jump-vector control; it is not a branching counterexample.
B=[F(1,2**j) for j in range(1,61)]
last=None
for n in range(1,41):
    vector=[v*(1-F(1,2**n)) if j<n else F(0) for j,v in enumerate(B)]
    errors=[abs(x-y) for x,y in zip(vector,B)]
    for e,b in zip(errors,B):ck(e<=b,'jump_envelope_domination')
    square=sum(e*e for e in errors)
    ck(max(errors)**2<=square,'l2_controls_uniform_jump_error')
    if last is not None:ck(square<=last,'finite_jump_vector_convergence_control')
    last=square

out={'problem_id':30005042,'author_turn':5,'exact_assertions':sum(C.values()),'by_kind':dict(sorted(C.items())),
     'scope':'Exact finite actual batch-birth genealogy and jump-intensity controls. Infinite common-envelope and l2 convergence follow from the written proof. Functional X log X tightness remains unresolved.',
     'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(out,indent=2,sort_keys=True))
