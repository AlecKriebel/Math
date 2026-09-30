#!/usr/bin/env python3
"""Exact finite diagnostics; the statistical theorem is proved in PARTIAL.md."""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import hashlib,json,random
C={}
def ck(b,k):
    assert b,k
    C[k]=C.get(k,0)+1

def dist2(x,y):return sum(((a-b)**2 for a,b in zip(x,y)),F(0))
def directed(P,k):
    return tuple(tuple(sorted(sorted((j for j in range(len(P)) if j!=i),key=lambda j:(dist2(P[i],P[j]),j))[:k])) for i in range(len(P)))
def undirected(B):return tuple(tuple(j for j in range(len(B)) if j!=i and (j in B[i] or i in B[j])) for i in range(len(B)))
def mutual(B):return tuple(tuple(j for j in range(len(B)) if j!=i and j in B[i] and i in B[j]) for i in range(len(B)))
X=[(F(a,10),) for a in (0,10,19,41)]
Y=[(F(a,10),) for a in (0,10,21,38)]
BX,BY=directed(X,2),directed(Y,2)
ck(BX==((1,2),(0,2),(0,1),(1,2)),'explicit_directed_X')
ck(BY==((1,2),(0,2),(1,3),(1,2)),'explicit_directed_Y')
A=undirected(BX)
ck(A==undirected(BY)==((1,2),(0,2,3),(0,1,3),(1,2)),'same_undirected_graph')
for P in (X,Y):
    for i in range(4):ck(len({dist2(P[i],P[j]) for j in range(4) if i!=j})==3,'no_distance_ties')
ck(len(set(A[2])&set(A[0]))==len(set(A[2])&set(A[3]))==1,'common_neighbor_tie')
ck(len(set(A[2])&set(A[1]))==2,'common_neighbor_first_rank')
for scale in (F(-3),F(-1,2),F(2,3),F(7,2)):
    for shift in (F(-2),F(0),F(5,3)):
        for P,B in ((X,BX),(Y,BY)):
            Z=[(scale*x[0]+shift,) for x in P]
            ck(directed(Z,2)==B,'global_similarity_preserves_directed_graph')
# Componentwise transformations on rational point clouds in unit balls.
rng=random.Random(30002105)
clouds=0; graph_pairs=0
for d in (1,2,3):
    for case in range(16):
        s=(F(3,2),F(2),F(5,2),F(3))[case%4];L=10*s
        n0,n1=8+case%5,9+(case*3)%5
        U=[]
        while len(U)<n0+n1:
            u=tuple(F(rng.randrange(-50,51),100*d) for _ in range(d))
            if u not in U:U.append(u)
        labels=[0]*n0+[1]*n1
        P=[];Q=[]
        for z,u in zip(labels,U):
            ck(dist2(u,(F(0),)*d)<1,'latent_points_in_unit_ball')
            P.append(tuple(u[j]+(z*L if j==0 else 0) for j in range(d)))
            Q.append(tuple((s if z else 1)*u[j]+(z*L if j==0 else 0) for j in range(d)))
        for i in range(len(U)):
            for j in range(i+1,len(U)):
                if labels[i]==labels[j]:
                    factor=s*s if labels[i] else F(1)
                    ck(dist2(Q[i],Q[j])==factor*dist2(P[i],P[j]),'within_component_similarity')
                else:
                    ck(dist2(P[i],P[j])>(2*s)**2 and dist2(Q[i],Q[j])>(2*s)**2,'cross_component_separation')
        for k in (1,2,min(n0,n1)-1):
            DP,DQ=directed(P,k),directed(Q,k);graph_pairs+=1
            ck(DP==DQ,'labelled_directed_coupling')
            ck(undirected(DP)==undirected(DQ),'union_graph_coupling')
            ck(mutual(DP)==mutual(DQ),'mutual_graph_coupling')
            ck(all(labels[i]==labels[j] for i in range(len(U)) for j in DP[i]),'no_cross_edges')
        clouds+=1
# Exact finite binomial tail and a rational Chernoff control (n=3m).
for m in range(1,61):
    n=3*m
    fail=F(2*sum(comb(n,j) for j in range(m+1)),2**n)
    # For W~Bin(n,1/2), E[2^{-W}]=(3/4)^n and P(W<=m)<=2^m(3/4)^n.
    ck(sum((F(comb(n,j),2**(n+j)) for j in range(n+1)),F(0))==F(3,4)**n,'binomial_mgf_identity')
    ck(fail<=2*F(27,32)**m,'exact_binomial_failure_bound')
# Scale-free target gaps, independent of the bump normalizer.
for d,s,r in product((1,2,3,5),(F(3,2),F(2),F(5)),(F(1,4),F(1),F(7,3))):
    a,b=F(2,5),F(2,5)/r
    rp=(a/2)/(b/2);rq=(a/2)/(b/(2*s**d))
    ck(rq==s**d*rp and rq-rp==(s**d-1)*r,'relative_density_scale_gap')
    ck(r-r/s==(1-1/s)*r>0,'relative_geometry_scale_gap')
# The positive-probability event gives each unscaled pair a distance in [3/4,5/4].
for u,v in product((F(-5,8),F(-1,2),F(-3,8)),(F(3,8),F(1,2),F(5,8))):
    ck(F(3,4)<=v-u<=F(5,4),'geometric_event_bounds')
base=Path(__file__).resolve().parent
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'categories':C,'rational_clouds':clouds,
 'coupled_graph_pairs':graph_pairs,'artifact_sha256':hashlib.sha256((base/'PARTIAL.md').read_bytes()).hexdigest(),
 'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Exact finite graph, coupling, scaling and binomial controls. No finite diagnostic proves or disproves connected-support asymptotic recovery.'},indent=2,sort_keys=True))
