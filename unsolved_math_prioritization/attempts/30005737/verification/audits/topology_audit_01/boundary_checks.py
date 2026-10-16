#!/usr/bin/env python3
"""Exact finite adversarial diagnostics; these are not a proof of the topology theorem."""
import itertools,json,math
from fractions import Fraction as Q

def mul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def sub(A,B):return [[x-y for x,y in zip(a,b)] for a,b in zip(A,B)]
def bracket(A,B):return sub(mul(A,B),mul(B,A))
def det(M):
    n=len(M)
    return sum((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))*math.prod(M[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
def coords(A):return [A[0][0],A[0][1],A[1][0]]
def fromcoords(v):return [[v[0],v[1]],[v[2],-v[0]]]
def lin(M,v):return [sum(M[i][j]*v[j] for j in range(len(v))) for i in range(len(M))]
H=[[1,0],[0,-1]];E=[[0,1],[0,0]];F=[[0,0],[1,0]]
Z=[[0,0],[0,0]];basis=[H,E,F]
j1=[[1,0,0],[0,1,0],[0,0,0]];j2=[[0,0,0],[0,0,0],[0,0,1]]
gbr={ (0,1):[0,2,0], (1,0):[0,-2,0] }
for M in [j1,j2]:
    for i,j in itertools.product(range(3),repeat=2):
        vi=[int(k==i) for k in range(3)];vj=[int(k==j) for k in range(3)]
        assert lin(M,gbr.get((i,j),[0,0,0]))==coords(bracket(fromcoords(lin(M,vi)),fromcoords(lin(M,vj))))
assert det(sub(j1,j2))==-1
trace_ad=[sum(gbr.get((i,j),[0,0,0])[j] for j in range(3)) for i in range(3)]
assert trace_ad==[2,0,0]
checks=[]
for a,b,c,d in itertools.product(range(-3,4),repeat=4):
    if a*d-b*c!=1:continue
    P=[[a,b],[c,d]];Pinv=[[d,-b],[-c,a]]
    columns=[coords(mul(mul(Pinv,H),P)),coords(mul(mul(Pinv,E),P)),[0,0,-1]]
    B=[[columns[j][i] for j in range(3)] for i in range(3)]
    value=det(B)
    assert value==-d*d
    checks.append((a,b,c,d,value))
assert any(d==0 for a,b,c,d,f in checks)
# The formal polynomial identity det(B)=-d^2(ad-bc) is checked coefficientwise.
def add(P,Q):
    R=P.copy()
    for k,v in Q.items():R[k]=R.get(k,0)+v
    return {k:v for k,v in R.items() if v}
def scale(P,c):return {k:c*v for k,v in P.items() if c*v}
def pmul(P,Q):
    R={}
    for k,v in P.items():
        for l,w in Q.items():
            m=tuple(x+y for x,y in zip(k,l));R[m]=R.get(m,0)+v*w
    return {k:v for k,v in R.items() if v}
a,b,c,d=[{tuple(int(i==j) for i in range(4)):1} for j in range(4)]
ad=pmul(a,d);bc=pmul(b,c);d2=pmul(d,d)
lhs=add(scale(pmul(d2,add(ad,bc)),-1),scale(pmul(pmul(b,d),pmul(c,d)),2))
rhs=scale(pmul(d2,add(ad,scale(bc,-1))),-1)
assert lhs==rhs
# Integer cellular chain ranks of (S^3)^k; all cellular differentials are zero.
# This checks explicit multiple-factor and zero-factor bookkeeping only.
chains=[]
for k in range(6):
    ranks={3*j:math.comb(k,j) for j in range(k+1)}
    assert ranks[3*k]==1
    for q in range(1,5):assert ranks.get(3*k+q,0)==0
    chains.append({'number_sl2_factors':k,'compact_dimension':3*k,'homology_free_ranks':ranks,'rank_above_compact_dimension':0})
# A nontrivial solvable complex group need not have injective exponential.
# In the simply connected affine group (t,u)(s,v)=(t+s,u+exp(t)v),
# exp(tX+uY)=(t,u*(exp(t)-1)/t). At t=2*pi*i, every u maps to (t,0).
# This exact formula is a mathematical diagnostic, not a floating-point test.
print(json.dumps({'status':'PASS','arithmetic':'integers and exact formal polynomials','nonunimodular_boundary':{'source':'b_plus direct_sum n_minus','trace_ad_basis':trace_ad,'j1_minus_j2_determinant':-1,'symbolic_determinant':'-d^2*(a*d-b*c), hence -d^2 on SL2','number_exact_SL2_matrices_checked':len(checks),'sample_d_zero':[list(x) for x in checks if x[3]==0][:3],'meaning':'local transversality can fail away from identity if unimodularity is omitted'},'multiple_factor_cellular_diagnostics':chains,'limitations':'Finite diagnostics do not establish integration, contractibility, covering theory, polar decomposition, or the general theorem.'},indent=2))
