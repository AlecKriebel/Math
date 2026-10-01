#!/usr/bin/env python3
"""Independent exact controls for the scoped branching audit; no J1 certificate."""
from fractions import Fraction as F
from itertools import product,permutations
from collections import Counter
import json
C=Counter()
def ck(x,label):
    assert x,label
    C[label]+=1
# Reconstruct conditional law under an ancestry-measurable ordering of active labels.
types=[(2,2,2),(1,2,2),(1,1,2),(1,1,1)]
for m,sizes in [(3,(1,2,3)),(4,(2,3,4))]:
    baseline=Counter()
    for marks in product(types,repeat=m):
        baseline[tuple(sum(marks[i][j] for i in range(sizes[j])) for j in range(3))]+=1
    for perm in permutations(range(m)):
        law=Counter()
        for marks in product(types,repeat=m):
            law[tuple(sum(marks[i][j] for i in perm[:sizes[j]]) for j in range(3))]+=1
        ck(law==baseline,'nested_noninitial_labels_have_exact_source_transition_law')
# Threshold symmetrization reduction for deterministic monotone curves.
curves=[(0,1,1),(0,1,2),(1,1,3),(0,0,2),(1,2,4)]
for fs in product(curves,repeat=3):
    weights=[f[-1] for f in fs]
    probs=[(F(f[0],f[-1]),F(f[1]-f[0],f[-1]),F(f[2]-f[1],f[-1])) for f in fs]
    rademacher=F(0)
    for eps in product((-1,1),repeat=3):
        direct=max(sum(eps[i]*fs[i][j] for i in range(3))**2 for j in range(3))
        threshold=F(0)
        for js in product(range(3),repeat=3):
            mass=probs[0][js[0]]*probs[1][js[1]]*probs[2][js[2]]
            threshold+=mass*max(sum(eps[i]*weights[i]*int(js[i]<=j) for i in range(3))**2 for j in range(3))
        ck(direct<=threshold,'conditional_threshold_Jensen')
        rademacher+=F(direct,8)
    ck(rademacher<=4*sum(w*w for w in weights),'deterministic_monotone_Doob_square_bound')
# Infinite scalar geometric tail computed exactly, with threshold ties included.
a=F(5,4)
for lam,n,y in product([a,F(3,2),F(2),F(7,3)],range(1,8),[F(i,3) for i in range(91)]):
    k=n
    while lam**k<y:k+=1
    exact=y*y*lam**(-k)/(1-1/lam)
    bound=a/(a-1)*min(y*y/a**n,y)
    ck(exact<=bound,'uniform_scalar_variance_tail_bound')
# Finite first-moment truncation constants and monotone tail-bias summation.
for vals in [(8,4,2,1),(3,3,2,2),(1,1,1,1),(5,1,0,0)]:
    b=list(map(F,vals));ck(all(b[i]>=b[i+1] for i in range(3)),'bias_sequence_monotone')
    ck(sum((i+1)*x*x for i,x in enumerate(b))<=sum(b)**2,'weighted_square_bias_bound')
# Exact finite tree with inactive intrinsic clocks and genuine batches.
vertices=[()]
for k in range(1,4):vertices.extend(product((1,2,3),repeat=k))
events=[];profiles={};raw=[]
for i,v in enumerate(vertices):
    base=i%2
    marks=[2] if base else [1,2]
    for j,J in enumerate(marks):raw.append((v,J))
N=len(raw)
for index,(v,J) in enumerate(raw):events.append((F(6,5)+F((index*17)%N+1,N+1),v,J))
ck(len(set(t for t,v,J in events))==N,'fixture_intrinsic_event_times_distinct')
for i,v in enumerate(vertices):profiles[v]=(i%2,[(t,J) for t,u,J in events if u==v])
def off(v,t,left=False):
    base,jumps=profiles[v]
    return base+sum(J for s,J in jumps if s<t or not left and s==t)
def pop(v,n,t,left=False):
    if not n:return 1
    return sum(pop(v+(i,),n-1,t,left) for i in range(1,off(v,t,left)+1))
def active(v,t):return all(v[j]<=off(v[:j],t,True) for j in range(len(v)))
inactive=0;batch=0
for t,v,J in events:
    k=len(v);on=active(v,t);inactive+=not on;batch+=on and J>1
    for n in range(5):
        jump=pop((),n,t)-pop((),n,t,True)
        rhs=F(0)
        if on and n>=k+1:
            first=off(v,t,True)+1
            rhs=t**(-k-1)*sum(F(pop(v+(i,),n-k-1,t))/t**(n-k-1) for i in range(first,first+J))
        ck(F(jump)/t**n==rhs,'reconstructed_active_batch_jump_identity')
        ck(jump>=0,'no_negative_prelimit_jump')
        if on and n==k+1:ck(jump==J,'own_depth_event_visible')
ck(inactive>0 and batch>0,'fixture_tests_inactive_clocks_and_batches')
# All-depth geometric intensity sum and exact capped-square sum.
for theta,x in product([F(6,5),F(3,2),F(2),F(7,3)],[F(i,3) for i in range(70)]):
    for eta in [F(1,5),F(1),F(3)]:
        k=0;s=F(0)
        while x>eta*theta**(k+1):s+=theta**k;k+=1
        ck(s<=x/(eta*(theta-1)),'all_depth_marked_count_bound')
    K=0
    while x>theta**(K+1):K+=1
    prefix=sum(theta**k for k in range(K))
    tail=x*x*theta**(-K-2)/(1-1/theta)
    ck(prefix+tail<=2*x/(theta-1),'exact_infinite_capped_square_envelope_bound')
# Independently reconstruct geometric joint moments from the factorial expansion.
for lam,delta in product([F(5,4),F(3,2),F(2),F(3)], [F(1,5),F(1,2),F(1),F(2)]):
    mu=lam+delta;m20=2*lam/(lam-1);m02=2*mu/(mu-1)
    m11=(2*lam*lam+lam*delta)/(lam*mu-lam)
    m21=(2*lam*lam*(m20+2*m11)+6*lam**3+delta*(lam*m20+2*lam*lam))/(lam*lam*mu-lam)
    closed=2*lam*(2*lam*lam*mu+lam*mu*mu-lam-2*mu)/((lam-1)*(mu-1)*(lam*mu-1))
    fake=2*lam*(2*lam+mu)/((lam-1)*(mu-1))
    ck(m21==closed,'independent_factorial_third_moment')
    ck(m21-fake==2*lam*(lam-mu)/((lam-1)*(mu-1)*(lam*mu-1))<0,'independent_increment_candidate_discrepancy')
    ck((lam-1)*(mu-1)*(m11-1)==lam*lam-1,'same_covariance_does_not_force_same_law')
    phi=lambda r,t:(r-1+t)/(r-1+r*t)
    for t in [F(0),F(1,2),F(3)]:
        B=phi(mu,t/mu);c=(1+lam*(1-B))/(1+mu*(1-B))
        ck(c==phi(mu,t)*(1+lam*(1-B)) and 0<c<=1,'Laplace_recurrence_factor')
        for z in [F(0),F(1,2),F(1)]:
            ck(0<=c/(1+lam-lam*z)<=1,'Laplace_map_preserves_unit_interval')
            ck(c*lam/(1+lam-lam*z)**2<=lam,'Laplace_error_amplification_bound')
# Rebuild the rational n=8 separation without using the author's evaluator.
lam=F(2);mu=F(3);s=t=F(1);n=8
z=1-s/lam**n-t/mu**n
for j in reversed(range(n)):
    tj=t/mu**j;B=(mu-1+tj/mu)/(mu-1+mu*tj/mu)
    c=(1+lam*(1-B))/(1+mu*(1-B));z=c/(1+lam-lam*z)
err=lam**n/F(2)*(s*s/lam**(2*n)*4+2*s*t/(lam*mu)**n*F(5,2)+t*t/mu**(2*n)*3)
ck(z>F(1,2),'true_bivariate_transform_separated_from_subordinator')
ck(err>0,'rational_enclosure_width_positive')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'bivariate_certificate':{'lower':str(z),'upper':str(z+err),'excluded_value':'1/2'},'scope':'Independent exact finite controls and explicit infinite geometric-series arithmetic. The separate report audits the analytic proofs; no endpoint J1 theorem or novelty is certified.'},indent=2,sort_keys=True))
