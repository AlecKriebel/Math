#!/usr/bin/env python3
"""Exact rational controls for KOU-21.42's credited positive-grading route.
These controls are not a finite verification of the universal grading theorem.
No network, file changes, external group packages, or private inputs required.
"""
from fractions import Fraction as F
from itertools import product
import json

N=10
NAMES=['x','y','z','u','v','A','B','C','D','E']
WEIGHTS=[1,2,1,2,3,3,4,5,3,4]
# Unlisted brackets vanish; reverse brackets are their negatives.
PAIRS={(0,1):8,(0,2):3,(1,2):4,(0,3):5,(1,3):6,
       (0,4):6,(1,4):7,(2,3):8,(2,4):9}
COUNTS={}
def check(b,kind):
    COUNTS[kind]=COUNTS.get(kind,0)+1
    if not b: raise AssertionError(kind)
def vec(i=None,scale=1):
    return tuple(F(scale if j==i else 0) for j in range(N))
ZERO=vec()
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,q):return tuple(q*x for x in a)
def bracket(a,b,pairs=PAIRS):
    out=[F(0)]*N
    for (i,j),k in pairs.items():out[k]+=a[i]*b[j]-a[j]*b[i]
    return tuple(out)
def bch(a,b):
    c=bracket(a,b)
    return add(add(add(a,b),scale(c,F(1,2))),
               scale(add(bracket(a,c),bracket(b,bracket(b,a))),F(1,12)))
def delta(a,m):return tuple(x*F(m)**w for x,w in zip(a,WEIGHTS))
def comm(a,b):return bch(bch(bch(scale(a,-1),scale(b,-1)),a),b)
def rank(rows):
    rows=[list(r) for r in rows if any(r)]
    r=0
    for c in range(N):
        i=next((i for i in range(r,len(rows)) if rows[i][c]),None)
        if i is None:continue
        rows[r],rows[i]=rows[i],rows[r]
        rows[r]=[v/rows[r][c] for v in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][c]:
                t=rows[i][c]; rows[i]=[a-t*b for a,b in zip(rows[i],rows[r])]
        r+=1
        if r==len(rows):break
    return r
B=[vec(i) for i in range(N)]
for a,b,c in product(B,repeat=3):
    check(add(add(bracket(a,bracket(b,c)),bracket(b,bracket(c,a))),bracket(c,bracket(a,b)))==ZERO,'jacobi_basis')
for a,b in product(B,repeat=2):
    check(bracket(a,b)==scale(bracket(b,a),-1),'antisymmetry_basis')
    for m in [2,3,F(1,2)]:
        check(delta(bracket(a,b),m)==bracket(delta(a,m),delta(b,m)),'grading_automorphism_basis')
L2=[bracket(a,b) for a,b in product(B,repeat=2)]
L3=[bracket(a,b) for a,b in product(B,L2)]
L4=[bracket(a,b) for a,b in product(B,L3)]
check(rank(L2)==7,'lower_central_dimensions')
check(rank(L3)==5,'lower_central_dimensions')
check(rank(L4)==0,'lower_central_dimensions')
Gens=B[:3]
Gen2=[bracket(a,b) for a,b in product(Gens,repeat=2)]
Gen3=[bracket(a,b) for a,b in product(Gens,Gen2)]
check(rank(Gens+Gen2+Gen3)==10,'three_lie_generators')
# BCH controls on integral lattice 12 Z^10. General closure follows from divisibility.
M=[scale(b,12) for b in B]
for a,b in product(M,repeat=2):
    p=bch(a,b)
    check(all(v.denominator==1 and v.numerator%12==0 for v in p),'lattice_closure_basis')
    check(bch(a,scale(a,-1))==ZERO,'inverse_basis')
    check(delta(p,2)==bch(delta(a,2),delta(b,2)),'bch_dilation_basis')
for a,b,c in product(M,repeat=3):
    check(bch(bch(a,b),c)==bch(a,bch(b,c)),'bch_associativity_basis')
# A three-generated lattice: <exp(12x), exp(12y), exp(12z)>.
# Its triple commutators supply all five central Lie directions.
x,y,z=M[:3]
u=comm(x,z);v=comm(y,z)
triples=[comm(x,u),comm(y,u),comm(y,v),comm(z,u),comm(z,v)]
check(rank(triples)==5,'group_central_certificate')
check(rank([x,y,z,u,v]+triples)==10,'group_full_lattice_certificate')
check(all(t[i]==0 for t in triples for i in range(5)),'group_central_certificate')
check(sum(WEIGHTS)==28,'dilation_index_exponent')
for a,w in zip([x,y,z],WEIGHTS[:3]):
    check(delta(a,2)==scale(a,2**w),'generator_power_endomorphism')
# Direct contraction certificate on arbitrary lattice vectors: a coordinate
# surviving n inverse dilations must be divisible by 2^(n*w).
for i,w in enumerate(WEIGHTS):
    for k in [-17,-4,-1,1,4,17]:
        n=abs(k).bit_length()+1
        q=delta(scale(B[i],12*k),F(1,2)**n)[i]/12
        check(q.denominator>1,'eventual_exit_from_lattice')
# Negative controls for common invalid implications. They do NOT refute KOU-21.42.
naive=[1,1,1,2,2,3,3,3,3,3]
check(any(naive[k]!=naive[i]+naive[j] for (i,j),k in PAIRS.items()),'reject_naive_lower_central_grading')
mutated=WEIGHTS.copy();mutated[8]+=1
check(any(mutated[k]!=mutated[i]+mutated[j] for (i,j),k in PAIRS.items()),'reject_wrong_degree')
# On Z^2, f(2a,b)=(a,b) preserves the nonzero subgroup 0 x Z.
check((0,F(1))==(F(0,2),F(1)),'zero_weight_core_negative_control')
# A contracting irrational map of R need not define a finite-index datum on Z.
# If nonzero k and l integers obey k/sqrt(2)=l then k^2=2*l^2,
# contradicting the parity of the 2-adic valuation; tested values supplement this proof.
for k,l in product(range(-20,21),repeat=2):
    if k or l:check(k*k!=2*l*l,'irrational_domain_negative_control')
# Contracting individual generators is not a homomorphism unless degrees add.
a,b=x,y
wrong=lambda t:scale(t,F(1,2))
check(wrong(bch(a,b))!=bch(wrong(a),wrong(b)),'reject_uniform_linear_scaling')
print(json.dumps({'status':'PASS','checks':COUNTS,'total_checks':sum(COUNTS.values()),
 'lie_basis':NAMES,'positive_weights':WEIGHTS,'lower_central_dimensions':[10,7,5,0],
 'rational_three_generator_lattice':'generated by exp(12*x), exp(12*y), exp(12*z)',
 'self_embedding_index_at_m_2':2**28,
 'scope':'Exact controls for the authored example and proof pitfalls; the universal grading theorem is an explicitly credited external dependency.'},indent=2,sort_keys=True))
