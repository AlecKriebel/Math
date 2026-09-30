#!/usr/bin/env python3
"""Exact finite diagnostics using labeled paintbox mergers and freezing recursion."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, permutations
from math import comb, factorial, prod
from collections import Counter, defaultdict
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
counts=Counter()
def check(kind, statement):
    if not statement: raise AssertionError(kind)
    counts[kind]+=1

@lru_cache(None)
def shapes(n, minimum=1):
    if n==0:return ((),)
    return tuple((i,)+tail for i in range(minimum,n+1) for tail in shapes(n-i,i))

def shape_multiplicity(shape):
    return factorial(sum(shape))//(prod(factorial(x) for x in shape)*prod(factorial(x) for x in Counter(shape).values()))

def canonical(groups):
    return tuple(sorted((tuple(sorted(g)) for g in groups),key=lambda x:x[0]))

class Model:
    def __init__(self, atoms, r, kingman=F(0)):
        self.atoms=tuple((F(rate),tuple(map(F,x))) for rate,x in atoms)
        self.r=F(r);self.kingman=F(kingman)
        assert self.r>0 and self.kingman>=0
        for rate,x in self.atoms:assert rate>=0 and all(y>=0 for y in x) and sum(x)<=1

    @lru_cache(None)
    def merger_rates(self,n):
        out=defaultdict(F)
        for rate,x in self.atoms:
            probs=(1-sum(x),)+x
            for colors in product(range(len(probs)),repeat=n):
                probability=prod(probs[i] for i in colors)
                if not probability:continue
                cohorts=defaultdict(list);groups=[]
                for i,color in enumerate(colors):
                    if color:cohorts[color].append(i)
                    else:groups.append([i])
                groups.extend(cohorts.values())
                if len(groups)<n:out[canonical(groups)]+=rate*probability
        if self.kingman:
            for i in range(n):
                for j in range(i+1,n):
                    groups=[[i,j]]+[[k] for k in range(n) if k not in (i,j)]
                    out[canonical(groups)]+=self.kingman
        return dict(out)

    def g(self,n):return sum(self.merger_rates(n).values(),F(0))

    @lru_cache(None)
    def p(self,shape):
        shape=tuple(shape);n=sum(shape)
        if n<=1:return F(1)
        total=F(0)
        if 1 in shape:
            tail=list(shape);tail.remove(1)
            total+=shape.count(1)*self.r*self.p(tuple(tail))
        labels=tuple(i for i,k in enumerate(shape) for _ in range(k))
        for pi,rate in self.merger_rates(n).items():
            if any(len({labels[j] for j in B})>1 for B in pi):continue
            smaller=[0]*len(shape)
            for B in pi:smaller[labels[B[0]]]+=1
            total+=rate*self.p(tuple(sorted(smaller)))
        return total/(self.g(n)+n*self.r)

    def moments(self):
        a=self.kingman;b=c=d=F(0)
        for rate,x in self.atoms:
            s2=sum(y*y for y in x);s3=sum(y**3 for y in x);s4=sum(y**4 for y in x)
            a+=rate*s2;b+=rate*s3;c+=rate*s4;d+=rate*(s2*s2-s4)
        return a,b,c,d

    def phi(self,N):
        phi=[F(0),F(1)]
        for n in range(2,N+1):phi.append(phi[-1]*(self.g(n)+n*self.r)/(self.g(n)+(n-1)*self.r))
        return phi

    def formal_decrements(self,N):
        phi=self.phi(N)
        return {(n,m):comb(n,m)*sum(((-1)**(j+1))*comb(m,j)*phi[n-m+j] for j in range(m+1))/phi[n]
                for n in range(1,N+1) for m in range(1,n+1)}

    def formal_shape_probability(self,shape,Q):
        out=F(0)
        for order in set(permutations(shape)):
            n=sum(order);term=F(1)
            for m in order:term*=Q[n,m];n-=m
            out+=term
        return out

atom_families=[
 [(1,(F(1,2),))],
 [(1,(F(1,2),F(1,2)))],
 [(1,(F(1,4),F(1,2)))],
 [(2,(F(1,3),)),(F(1,2),(F(1,4),F(1,4),F(1,4)))]
]
models=0
for atoms,r,king in product(atom_families,(F(1,2),F(1),F(3)),(F(0),F(1,3),F(2))):
    M=Model(atoms,r,king);models+=1
    a,b,c,d=M.moments();e=a-2*b+c-d
    check('specified_rates',M.merger_rates(2)[((0,1),)]==a)
    check('specified_rates',M.merger_rates(3).get(((0,1,2),),0)==b)
    check('specified_rates',M.merger_rates(4).get(((0,1,2,3),),0)==c)
    check('specified_rates',M.merger_rates(4).get(((0,1),(2,3)),0)==d)
    check('specified_rates',M.merger_rates(4).get(((0,1),(2,),(3,)),0)==e)
    check('total_rates',M.g(3)==3*a-2*b)
    check('total_rates',M.g(4)==6*a-8*b+3*c-3*d)
    Q=M.formal_decrements(5)
    for n in range(2,6):
        check('singleton_recursion',M.p((1,)*n)/M.p((1,)*(n-1))==n*r/(M.g(n)+n*r))
        check('normalization',sum(shape_multiplicity(s)*M.p(s) for s in shapes(n))==1)
        check('formal_decrement_sum',sum(Q[n,m] for m in range(1,n+1))==1)
    for n in range(1,5):
        for shape in shapes(n):
            rhs=M.p(tuple(sorted(shape+(1,))))
            for i in range(len(shape)):
                bigger=list(shape);bigger[i]+=1;rhs+=M.p(tuple(sorted(bigger)))
            check('sampling_consistency',M.p(shape)==rhs)
    defect=2*r*(3*d*(a+r)-2*b*(a-2*b+c))/((a+2*r)*(3*a-2*b+3*r)*(6*a-8*b+3*c-3*d+4*r))
    check('four_sample_identity',M.p((4,))-Q[4,4]==defect)

# Known positive controls, including zero coalescence.
positive_controls=0
for atoms,king,r in [([],F(1),F(1,2)),([],F(2),F(3)),([(1,(1,))],F(0),F(1)),([(3,(1,))],F(0),F(2)),([],F(0),F(1))]:
    M=Model(atoms,r,king);Q=M.formal_decrements(6);positive_controls+=1
    for n in range(1,7):
        for shape in shapes(n):
            check('known_positive_controls',M.formal_shape_probability(shape,Q)==shape_multiplicity(shape)*M.p(shape))
        check('known_positive_controls',all(Q[n,m]>=0 for m in range(1,n+1)))

# Exact nonexceptional model passing n<=4 and failing n=5.
M=Model([(10,(F(1,2),)),(1,(F(1,2),F(1,2)))],3)
Q=M.formal_decrements(6)
check('five_sample_witness',M.moments()==(F(3),F(3,2),F(3,4),F(1,8)))
for n in range(1,5):
    for shape in shapes(n):
        check('passes_through_four',M.formal_shape_probability(shape,Q)==shape_multiplicity(shape)*M.p(shape))
check('five_sample_witness',M.g(5)==F(73,8))
check('five_sample_witness',M.p((5,))==F(2857,30687))
check('five_sample_witness',Q[5,5]==F(934,10229))
check('five_sample_witness',M.p((5,))-Q[5,5]==F(55,30687))
block_rates=defaultdict(F)
for pi,rate in M.merger_rates(5).items():block_rates[len(pi)]+=rate
check('five_sample_witness',[block_rates[k] for k in (4,3,2,1)]==[F(25,8),F(25,8),F(5,2),F(3,8)])

# Bounded-parent controls: non-singleton allele support at most two.
bounded_controls=0
for x,r in product(((F(1,2),F(1,2)),(F(1,3),F(2,3))),(F(1,2),F(1),F(3))):
    B=Model([(1,x)],r);bounded_controls+=1
    check('bounded_parent_control',B.p((2,2))>0)
    check('bounded_parent_control',B.p((2,2,2))==0)
    Qb=B.formal_decrements(6)
    check('bounded_parent_control',B.p((4,))!=Qb[4,4])
# A three-parent/star mixture shows that the bounded-parent theorem is not
# merely another use of the four-sample identity.
B=Model([(10,(1,)),(1,(F(1,3),F(1,3),F(1,3)))],F(85,27))
Qb=B.formal_decrements(5)
check('bounded_parent_critical_rate',B.p((4,))==Qb[4,4])
check('bounded_parent_critical_rate',B.p((2,2))>0)

print(json.dumps({
 'status':'PASS','assertions':sum(counts.values()),'assertions_by_kind':dict(counts),
 'finite_paintbox_models':models,'positive_controls':positive_controls,'two_parent_controls':bounded_controls,
 'five_sample_true_probability':str(M.p((5,))),
 'five_sample_formal_regenerative_probability':str(Q[5,5]),
 'five_sample_difference':str(M.p((5,))-Q[5,5]),
 'artifact_sha256':sha256((HERE/'PARTIAL_RESULT.md').read_bytes()).hexdigest(),
 'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
 'limitations':'Finite exact diagnostics only; no all-sample regeneration claim follows from matching finite tables.'
},indent=2,sort_keys=True))
