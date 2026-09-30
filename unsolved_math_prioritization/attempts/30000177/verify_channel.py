#!/usr/bin/env python3
"""Exact rational checks for the specified W-state cq multiple-access channel.

No numerical optimization and no simulation of an asymptotic decoding theorem.
All matrix and entropy identities use exact rational arithmetic. The coding
existence step is Winter's established theorem, applied in CANDIDATE.md.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, math

checks = Counter()
def req(x, label):
    assert x, label
    checks[label] += 1

def zero(n=4): return [[F(0) for _ in range(n)] for _ in range(n)]
def add(ms): return [[sum(m[i][j] for m in ms) for j in range(4)] for i in range(4)]
def scale(m,s): return [[s*x for x in row] for row in m]
def mul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))] for i in range(len(a))]
def tr(a): return sum(a[i][i] for i in range(len(a)))
def spectral(a,ev,label):
    req(len(a)==len(ev),label+'_dimension')
    p=a
    for k in range(1,len(a)+1):
        req(tr(p)==sum(e**k for e in ev),label+'_power_sum')
        p=mul(p,a)
    # A is real symmetric, so equality of all dimension-many power sums fixes
    # its entire real spectrum by Newton's identities.
    req(all(a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a))),label+'_Hermitian')
    req(all(e>=0 for e in ev),label+'_positive_spectrum')

# Qubit order A1 B1 A2 B2. The input W amplitudes are integer/2.
letters=list(product(range(2),repeat=2))  # U_(a,b)=X^a Z^b
bell=((1,0,0,1),(1,0,0,-1),(0,1,1,0),(0,1,-1,0))
for u in bell:
 for v in bell: req(sum(x*y for x,y in zip(u,v))==(2 if u==v else 0),'Bell_orthonormality')
W={1:1,2:1,4:1,8:1}

def encoded(x,y):
    a,b=x;c,d=y;out={}
    for k,v in W.items():
        q=[(k>>j)&1 for j in (3,2,1,0)]
        sign=(-1)**(b*q[0]+d*q[2]);q[0]^=a;q[2]^=c
        j=sum(t<<s for t,s in zip(q,(3,2,1,0)))
        out[j]=sign*v
    req(sum(v*v for v in out.values())==4,'Pauli_normalization')
    return out

blocks={}
for x,y in product(letters,repeat=2):
    v=encoded(x,y); arr=[]
    for z in bell:
        c=[sum(z[l]*v.get(4*l+r,0) for l in range(4)) for r in range(4)]
        m=[[F(c[i]*c[j],8) for j in range(4)] for i in range(4)]
        spectral(m,[tr(m),F(0),F(0),F(0)],'conditional_block_rank_one')
        arr.append(m)
    req(sorted(tr(m) for m in arr)==[0,F(1,4),F(1,4),F(1,2)],'outcome_law')
    req(sum(tr(m) for m in arr)==1,'cq_state_normalization')
    blocks[x,y]=arr

# Average over both independent, uniform Pauli alphabets.
bar=[scale(add([blocks[x,y][z] for x,y in product(letters,repeat=2)]),F(1,16)) for z in range(4)]
for m in bar:
    req(m==[[F(3 if i%2==0 else 1,32) if i==j else F(0) for j in range(4)] for i in range(4)],'fully_averaged_block')
    spectral(m,[F(3,32),F(3,32),F(1,32),F(1,32)],'fully_averaged_spectrum')

for y in letters:
    my=[scale(add([blocks[x,y][z] for x in letters]),F(1,4)) for z in range(4)]
    for m in my: spectral(m,[F(1,8),F(1,8),F(0),F(0)],'X_averaged_spectrum')
for x in letters:
    mx=[scale(add([blocks[x,y][z] for y in letters]),F(1,4)) for z in range(4)]
    counts=Counter()
    for m in mx:
        p=tr(m)
        if p==F(1,2): ev=[F(1,4),F(1,4),0,0];kind='half'
        elif p==F(1,4): ev=[F(1,16)]*4;kind='quarter'
        else: req(p==0,'Y_average_zero_block');ev=[F(0)]*4;kind='zero'
        spectral(m,ev,'Y_averaged_spectrum');counts[kind]+=1
    req(counts=={'half':1,'quarter':2,'zero':1},'Y_averaged_multiplicity')

# Marginals of the original pure state, including the two pair cuts.
def partial(keep):
    n=2**len(keep);m=[[F(0) for _ in range(n)] for _ in range(n)]
    other=[j for j in range(4) if j not in keep]
    for i,j in product(W,repeat=2):
        a=[(i>>(3-t))&1 for t in range(4)];b=[(j>>(3-t))&1 for t in range(4)]
        if any(a[t]!=b[t] for t in other):continue
        ai=sum(a[t]<<(len(keep)-1-s) for s,t in enumerate(keep));bi=sum(b[t]<<(len(keep)-1-s) for s,t in enumerate(keep))
        m[ai][bi]+=F(1,4)
    return m
for t in range(4):spectral(partial([t]),[F(3,4),F(1,4)],'single_qubit_marginal')
for t in ([0,1],[2,3],[1,3]):spectral(partial(t),[F(1,2),F(1,2),0,0],'two_qubit_marginal')

# Entropies as pairs (a,b) meaning a+b log_2(3), certified by factoring
# each rational eigenvalue into 2^u*3^v, including multiplicities.
def power23(q):
    ex=[]
    for p in (2,3):
        e=0
        while q.numerator%p==0:q/=p;e+=1
        while q.denominator%p==0:q*=p;e-=1
        ex.append(e)
    req(q==1,'spectrum_prime_factorization')
    return ex

def entropy(es):
    s=[F(0),F(0)]
    for e in es:
        e=F(e)
        if not e:continue
        u,v=power23(e);s[0]-=e*u;s[1]-=e*v
    return tuple(s)
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
h=entropy([F(3,4),F(1,4)])
Sxy=entropy([F(1,2),F(1,4),F(1,4)])
Sx=entropy([F(1,4)]*2+[F(1,16)]*8)
Sy=entropy([F(1,8)]*8)
Sbar=entropy([F(3,32)]*8+[F(1,32)]*8)
req(h==(F(2),F(-3,4)),'binary_entropy')
req(Sxy==(F(3,2),0),'conditional_entropy')
req(Sx==Sy==(F(3),0),'single_input_averaged_entropy')
req(minus(Sbar,Sxy)==(F(7,2),F(-3,4)),'MAC_sum_information')
req(minus(Sx,Sxy)==minus(Sy,Sxy)==(F(3,2),0),'MAC_individual_information')
req(3**3<2**5,'exact_h_greater_than_three_quarters')
req(F(9,8)<F(3,2),'strict_individual_rate')
req(F(9,4)==F(3,2)+F(3,4),'strict_sum_rate_threshold')
req(F(9,4)>2,'quantum_advantage')

# Negative control: Bell-measuring both sides leaves exactly two bits for the
# uniform product input. This does not bound alternative one-copy strategies.
probs={}
for x,y in product(letters,repeat=2):
    a=[]
    for m in blocks[x,y]:
        for z in bell:a.append(sum(F(z[i]*z[j],2)*m[i][j] for i in range(4) for j in range(4)))
    req(sorted(a)==[F(0)]*12+[F(1,4)]*4,'both_Bell_conditional_distribution')
    probs[x,y]=a
req(all(sum(a[j] for a in probs.values())/16==F(1,16) for j in range(16)),'both_Bell_average_uniform')
req(minus(entropy([F(1,16)]*16),entropy([F(1,4)]*4))==(F(2),0),'both_Bell_information_two')

base=Path(__file__).resolve().parent
out={'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
 'input_pairs':16,'conditional_blocks':64,'cq_MAC_individual_bounds':'3/2 each',
 'cq_MAC_sum_bound':'3/2 + h_2(1/4) = 7/2 - (3/4) log_2(3)',
 'strict_achievable_rate_pair':['9/8','9/8'],
 'approximate_sum_supremum':3.5-.75*math.log2(3),
 'scope':'Exact finite channel and entropy checks. Asymptotic independent-message achievability uses Winter Theorem 9, not a finite simulation.',
 'candidate_sha256':hashlib.sha256((base/'CANDIDATE.md').read_bytes()).hexdigest()}
print(json.dumps(out,indent=2,sort_keys=True))
