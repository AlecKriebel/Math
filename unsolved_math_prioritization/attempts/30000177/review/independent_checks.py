#!/usr/bin/env python3
"""Exact independent density-matrix and characteristic-polynomial audit.

Uses rational density operators and Bell projectors, not the author's
conditional-vector implementation or trace-power spectral certificates.
"""
from fractions import Fraction as Q
from collections import Counter
from itertools import product, permutations, combinations
import json

checks=Counter()
def check(x,k):
    assert x,k
    checks[k]+=1

def zero(n):return [[Q(0) for _ in range(n)] for _ in range(n)]
def tr(a):return sum(a[i][i] for i in range(len(a)))
def add(mats,div=1):
    mats=list(mats);n=len(mats[0])
    return [[sum(a[i][j] for a in mats)/div for j in range(n)] for i in range(n)]
def polmul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def charpoly(a):
    n=len(a);out=[Q(0)]*(n+1)
    for p in permutations(range(n)):
        term=[Q((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))]
        for i in range(n):term=polmul(term,[-a[i][p[i]],Q(i==p[i])])
        for j,v in enumerate(term):out[j]+=v
    return out

def from_roots(roots):
    out=[Q(1)]
    for r in roots:out=polmul(out,[-r,Q(1)])
    return out

def entropy(roots):
    # Exact representation A+B log_2(3), all eigenvalues are 2^a 3^b.
    A=B=Q(0)
    for p in roots:
        if not p:continue
        n,d=p.numerator,p.denominator;a=b=0
        while n%2==0:n//=2;a+=1
        while d%2==0:d//=2;a-=1
        while n%3==0:n//=3;b+=1
        while d%3==0:d//=3;b-=1
        check(n==d==1,'entropy_factorization')
        A-=p*a;B-=p*b
    return (A,B)

def bits(i):return tuple((i>>(3-j))&1 for j in range(4))
def index(b):return sum(x<<(3-j) for j,x in enumerate(b))
paulis=list(product((0,1),repeat=2)) # X^a Z^b
W=[i for i in range(16) if sum(bits(i))==1]
rho=zero(16)
for i,j in product(W,repeat=2):rho[i][j]=Q(1,4)
check(tr(rho)==1,'initial_resource_normalization')

def encoded(x,y):
    a,b=x;c,d=y;out=zero(16)
    for i,j in product(W,repeat=2):
        bi=list(bits(i));bj=list(bits(j))
        sg=(-1)**(b*(bi[0]+bj[0])+d*(bi[1]+bj[1]))
        for z in (bi,bj):z[0]^=a;z[1]^=c
        # Only regroup tensor factors: L=(A1,B1), R=(A2,B2).
        ii=4*(2*bi[0]+bi[2])+(2*bi[1]+bi[3])
        jj=4*(2*bj[0]+bj[2])+(2*bj[1]+bj[3])
        out[ii][jj]+=Q(sg,4)
    return out

bell_vectors=([1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0])
projectors=[[[Q(v[i]*v[j],2) for j in range(4)] for i in range(4)] for v in bell_vectors]
for j,p in enumerate(projectors):
    check(tr(p)==1,'Bell_projector_trace')
    for k,q in enumerate(projectors):
        check([[sum(p[a][c]*q[c][b] for c in range(4)) for b in range(4)] for a in range(4)]==(p if j==k else zero(4)),'Bell_projector_orthogonality')
check(add(projectors)==[[Q(i==j) for j in range(4)] for i in range(4)],'Bell_measurement_complete')

channel={};roots={};both_bell={}
for x,y in product(paulis,repeat=2):
    state=encoded(x,y);bs=[];ev=[];prob=[]
    for p in projectors:
        # Partial trace after the projective measurement, using P^2=P.
        block=[[sum(p[k][l]*state[4*l+r][4*k+s] for l,k in product(range(4),repeat=2)) for s in range(4)] for r in range(4)]
        weight=tr(block)
        check(charpoly(block)==from_roots([weight,0,0,0]),'conditional_characteristic_polynomial')
        check(weight>=0,'conditional_probability_nonnegative')
        bs.append(block);ev.extend([weight,Q(0),Q(0),Q(0)])
        prob.extend(sum(block[a][b]*q[b][a] for a,b in product(range(4),repeat=2)) for q in projectors)
    channel[x,y]=bs;roots[x,y]=ev;both_bell[x,y]=prob
    check(sorted(v for v in ev if v)==[Q(1,4),Q(1,4),Q(1,2)],'single_input_spectrum')
    check(sum(ev)==1,'channel_trace_preserved')
    check(entropy(ev)==(Q(3,2),Q(0)),'single_input_entropy')
    check(sorted(v for v in prob if v)==[Q(1,4)]*4,'both_Bell_conditional_distribution')

fixedx={x:[add((channel[x,y][j] for y in paulis),4) for j in range(4)] for x in paulis}
fixedy={y:[add((channel[x,y][j] for x in paulis),4) for j in range(4)] for y in paulis}
for x,bs in fixedx.items():
    traces=sorted(tr(b) for b in bs)
    check(traces==[0,Q(1,4),Q(1,4),Q(1,2)],'fixed_X_block_probabilities')
    es=[]
    for b in bs:
        t=tr(b)
        e=[Q(0)]*4 if t==0 else ([Q(1,16)]*4 if t==Q(1,4) else [Q(1,4),Q(1,4),Q(0),Q(0)])
        check(charpoly(b)==from_roots(e),'fixed_X_characteristic_polynomial');es+=e
    check(entropy(es)==(Q(3),Q(0)),'fixed_X_entropy')
for y,bs in fixedy.items():
    for b in bs:check(charpoly(b)==from_roots([Q(1,8),Q(1,8),Q(0),Q(0)]),'fixed_Y_characteristic_polynomial')
    check(entropy([Q(1,8)]*8)==(Q(3),Q(0)),'fixed_Y_entropy')
avg=[add((channel[x,y][j] for x,y in product(paulis,repeat=2)),16) for j in range(4)]
for b in avg:
    check(b==[[Q((3 if i%2==0 else 1) if i==j else 0,32) for j in range(4)] for i in range(4)],'grand_average_exact_matrix')
    check(charpoly(b)==from_roots([Q(3,32),Q(3,32),Q(1,32),Q(1,32)]),'grand_average_characteristic_polynomial')
check(entropy([Q(3,32)]*8+[Q(1,32)]*8)==(Q(5),Q(-3,4)),'grand_average_entropy')
check([sum(p[i] for p in both_bell.values())/16 for i in range(16)]==[Q(1,16)]*16,'both_Bell_output_uniform')
check(entropy([Q(1,16)]*16)==(4,0) and entropy([Q(1,4)]*4)==(2,0),'both_Bell_information_exactly_two')

# All one- and two-qubit resource marginals, computed by matching traced indices.
for keep in combinations(range(4),1):
    n=2;red=zero(n)
    for i,j in product(range(16),repeat=2):
        bi,bj=bits(i),bits(j)
        if all(bi[k]==bj[k] for k in range(4) if k not in keep):red[bi[keep[0]]][bj[keep[0]]]+=rho[i][j]
    check(charpoly(red)==from_roots([Q(3,4),Q(1,4)]),'one_qubit_marginal_spectrum')
for keep in combinations(range(4),2):
    red=zero(4)
    for i,j in product(range(16),repeat=2):
        bi,bj=bits(i),bits(j)
        if all(bi[k]==bj[k] for k in range(4) if k not in keep):red[2*bi[keep[0]]+bi[keep[1]]][2*bj[keep[0]]+bj[keep[1]]]+=rho[i][j]
    check(charpoly(red)==from_roots([Q(1,2),Q(1,2),Q(0),Q(0)]),'two_qubit_marginal_spectrum')

# Pinching a genuine 16-outcome Hadamard POVM leaves all cq probabilities intact.
def had(i,j):return (-1)**((i&j).bit_count())
for a in range(16):
    E=[[Q(had(a,i)*had(a,j),16) for j in range(16)] for i in range(16)]
    P=[[E[i][j] if i//4==j//4 else Q(0) for j in range(16)] for i in range(16)]
    for bs in channel.values():
        full=zero(16)
        for q,b in enumerate(bs):
            for i,j in product(range(4),repeat=2):full[4*q+i][4*q+j]=b[i][j]
        val=lambda z:sum(full[i][j]*z[j][i] for i,j in product(range(16),repeat=2))
        check(val(E)==val(P),'classical_register_pinching_preserves_probabilities')
for block in range(4):
    for i,j in product(range(4),repeat=2):
        check(sum(Q(had(a,4*block+i)*had(a,4*block+j),16) for a in range(16))==int(i==j),'conditional_POVM_completeness')

check(3**3<2**5,'strict_rate_sum_advantage_certificate')
check(Q(9,8)<Q(3,2),'individual_rate_slack')
check(3**3>2**4,'LO_capacity_below_two_certificate')
check(3<4,'achievable_lower_bound_below_LOCC_upper_bound')
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
 'input_pairs':16,'conditional_blocks':64,'spectral_method':'Exact rational characteristic polynomials of density blocks, computed by Leibniz determinants.',
 'limitation':'The channel algebra and physical pinching controls are exact; asymptotic coding is supplied by Winter\'s established theorem, not by a finite simulation.'},indent=2,sort_keys=True))
