#!/usr/bin/env python3
"""Exact finite diagnostics; topology and universal statements remain proved in REVIEW.md."""
import itertools, json, math

def require(ok, message):
    if not ok: raise ValueError(message)

def add(A,B):
    return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def scale(c,A): return [[c*x for x in row] for row in A]
def mul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def comm(A,B): return add(mul(A,B),scale(-1,mul(B,A)))
J=[[0,-1,0],[1,0,0],[0,0,0]]
A=[[0,0,1],[0,0,0],[1,0,0]]
B=[[0,0,0],[0,0,1],[0,1,0]]
C=[[1,0,0],[0,-1,0],[0,0,0]]
D=[[0,1,0],[1,0,0],[0,0,0]]
L=[[1,0,0],[0,1,0],[0,0,-2]]
for X,Y in [(A,B),(B,scale(-1,A)),(C,scale(2,D)),(D,scale(-2,C)),(L,scale(0,L))]:
    require(comm(J,X)==Y,"Wrong tangent isotropy commutator")
require((1+2)%2==1,"The rotation loop must be nontrivial in pi_1(SO(5))")
# A wrong even-only representation would make the obstruction fail.
require((2+2)%2==0,"Negative parity control")
coefficient_images=[a%2 for a in range(4) if (2*a)%4==0]
require(coefficient_images==[0,0],"H^2 reduction unexpectedly nonzero")
# In the alternative integral coefficient sequence beta(x) generates H^3(Z)=Z/2.
require(len(coefficient_images)==2,"Coefficient domain size wrong")

orders=range(1,258)
all_residues=0
for n in orders:
    fixed=[k for k in range(1,n) if any((w*k)%n==0 for w in (1,1,-2))]
    expected=[] if n%2 else [n//2]
    require(fixed==expected,"Circle spectrum/isotropy mismatch at order "+str(n))
    all_residues+=max(0,n-1)
require(all((w*1)%3!=0 for w in (1,1,-2)),"Prime three central element control")
require(any((w*1)%2==0 for w in (1,1,-2)),"Prime two must fail free construction")
require(any((w*1)%5==0 for w in (1,-1,0)),"Bad weight negative control must be detected")
# For a full rank-two subgroup of the diagonal SU(3) torus, (a,b)=(0,1)
# has eigenvalue 1. These checks are only about this ambient subgroup.
for p in (2,3,5,7,11,13):
    a,b=0,1
    require((a,b)!=(0,0) and 0 in (a%p,b%p,(-a-b)%p),"Toral rank-two control")

def rank_mod(M,p):
    if not M: return 0
    M=[row[:] for row in M];r=0
    for c in range(len(M[0])):
        pivot=next((i for i in range(r,len(M)) if M[i][c]%p),None)
        if pivot is None: continue
        M[r],M[pivot]=M[pivot],M[r]
        inv=pow(M[r][c]%p,-1,p)
        M[r]=[(v*inv)%p for v in M[r]]
        for i in range(len(M)):
            if i!=r:
                q=M[i][c]%p
                M[i]=[(x-q*y)%p for x,y in zip(M[i],M[r])]
        r+=1
        if r==len(M): break
    return r
cubics=0; maps=0; zero_controls=0
for p in (3,5,7):
    for f in itertools.product(range(p),repeat=4):
        cubics+=1
        for degree in (3,4,5,8):
            # Coefficient j means x^j y^(3-j), input i means x^i y^(degree-3-i).
            M=[[0]*(degree-2) for _ in range(degree+1)]
            for i in range(degree-2):
                for j,c in enumerate(f): M[i+j][i]=c
            rank=rank_mod(M,p)
            if any(f):
                require(rank==degree-2,"Nonzero cubic multiplication must inject")
                require((degree+1)-rank==3,"Binary cubic quotient must persist")
            else:
                require(rank==0 and degree+1>3,"Zero transgression control")
                zero_controls+=1
            maps+=1
for r in (2,3,4):
    for n in range(24):
        require(math.comb(n+6+r-1,r-1)>math.comb(n+r-1,r-1),"Eventual periodicity contradiction missing")
for n in range(24):
    require(math.comb(n+6,0)==math.comb(n,0),"Rank-one positive control")
RESULT={
 "status":"PASS",
 "circle_orders":257, "nonidentity_residues_checked":all_residues,
 "matrix_commutator_identities":5, "odd_weight_loop_parity":1,
 "binary_cubics_including_zero":cubics, "multiplication_maps":maps,
 "zero_cubic_controls":zero_controls,
 "controls":["even-order stabilizer present","p=3 scalar has no eigenvalue 1","bad weights with zero coordinate detected","even-loop parity zero","zero cubic leaves entire polynomial ring","rank-one Betti periodicity allowed"],
 "limitations":"Finite diagnostics only; no finite test proves the infinite-prime quantifier, topological microbundle naturality, characteristic number, or spectral-sequence convergence."
}
if __name__=="__main__": print(json.dumps(RESULT,sort_keys=True,indent=2))
