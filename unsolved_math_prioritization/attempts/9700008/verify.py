#!/usr/bin/env python3
"""Exact rational controls for the scoped Metropolis conclusions.
No floating-point eigensolver is used. Finite controls supplement the proof.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib,json,random

counts=Counter()
def check(x,name):
    assert x,name
    counts[name]+=1

def solve(A,b):
    n=len(b);M=[[F(x) for x in row]+[F(y)] for row,y in zip(A,b)]
    for j in range(n):
        i=next(i for i in range(j,n) if M[i][j])
        M[i],M[j]=M[j],M[i]
        q=M[j][j];M[j]=[x/q for x in M[j]]
        for i in range(n):
            if i!=j:
                q=M[i][j];M[i]=[x-q*y for x,y in zip(M[i],M[j])]
    return [row[-1] for row in M]

def mv(A,v):return [sum(x*y for x,y in zip(row,v)) for row in A]
def complete(n):return [[j for j in range(n) if i!=j] for i in range(n)]
def cycle(n):return [sorted({(i-1)%n,(i+1)%n}) for i in range(n)]
def cube(k):return [[i^(1<<j) for j in range(k)] for i in range(1<<k)]

def model(neighbors,p,theta=F(1)):
    n=len(neighbors);d=len(neighbors[0]);q=1-p
    P=[[theta/d if j in neighbors[i] else 1-theta if i==j else F(0)
        for j in range(n)] for i in range(n)]
    mu=solve([[F(i==j)-q*P[i][j] for j in range(n)] for i in range(n)],
             [p]+[F(0)]*(n-1))
    check(sum(mu)==1 and min(mu)>0,'resolvent_probability')
    check(mu==[p*F(i==0)+q*x for i,x in enumerate(mv(P,mu))], 'resolvent_equation')
    K=[[P[i][j]*min(F(1),mu[j]/mu[i]) if i!=j else F(0)
        for j in range(n)] for i in range(n)]
    for i in range(n):K[i][i]=1-sum(K[i])
    for i in range(n):
        check(sum(K[i])==1 and min(K[i])>=0,'Metropolis_stochasticity')
        for j in range(n):
            check(mu[i]*K[i][j]==mu[j]*K[j][i],'detailed_balance')
    return mu,K

for n in range(2,15):
    for p in (F(1,5),F(1,2),F(3,4),F(9,10)):
        mu,K=model(complete(n),p)
        a=F(1+(n-2)*p,n-p);b=F(1-p,n-p);r=b/a
        check(mu==[a]+[b]*(n-1),'complete_graph_stationary_formula')
        lam=F(n-2,n-1)-r
        radial=[-(n-1)*b]+[a]*(n-1)
        check(mv(K,radial)==[lam*x for x in radial],'radial_eigenvector')
        check(sum(x*y for x,y in zip(mu,radial))==0,'radial_centered')
        for i in range(2,n):
            v=[F(0)]*n;v[1]=1;v[i]=-1
            check(mv(K,v)==[-F(x,n-1) for x in v],'contrast_eigenspace')
        check(lam>=-F(1,n-1),'second_largest_eigenvalue_order')
        tau=1/(1-lam)
        check(tau==F((n-1)*(1+(n-2)*p),n-p),'relaxation_formula')
        check(tau<=F((n-1)**2,p),'complete_graph_decreasing_bound')
    p0,p1=F(1,2),F(3,4)
    tau=lambda p:F((n-1)*(1+(n-2)*p),n-p)
    check(tau(p1)>tau(p0),'strict_monotonicity_counterexample')
    check(tau(p0)/F(n-1,n)==F(n*n,2*n-1),'endpoint_ratio_formula')
    for theta in (F(1,3),F(1,2)):
        mu,K=model(complete(n),F(1,2),theta)
        r=F(theta, n-1+theta)
        check(mu[1]/mu[0]==r,'lazy_proposal_stationary_ratio')
        lam=1-theta*(r+F(1,n-1))
        radial=[-(n-1)*mu[1]]+[mu[0]]*(n-1)
        check(mv(K,radial)==[lam*x for x in radial],'lazy_proposal_radial_eigenvector')

for p,weights,lam,tau in [(F(1,2),[F(4,7)]+[F(1,7)]*3,F(5,12),F(12,7)),
                          (F(3,4),[F(10,13)]+[F(1,13)]*3,F(17,30),F(30,13))]:
    mu,K=model(complete(4),p)
    check(mu==weights,'K4_exact_weights')
    check(lam>F(1,3),'K4_absolute_gap_agreement')
    check(1/(1-lam)==tau,'K4_exact_times')

rng=random.Random(9700008)
graphs=[('cycle'+str(n),cycle(n)) for n in range(3,13)]
graphs += [('cube'+str(k),cube(k)) for k in range(1,5)]
graphs += [('complete'+str(n),complete(n)) for n in range(2,9)]
path_total=0
for name,neighbors in graphs:
    for p in (F(1,7),F(1,2),F(4,5)):
        n=len(neighbors);d=len(neighbors[0]);mu,K=model(neighbors,p)
        check(mu[0]>max(mu[1:]),'unique_root_maximum')
        flows={}
        for i in range(n):
            for j in neighbors[i]:
                if mu[i]>mu[j]:
                    flows[i,j]=F(1-p,d*p)*(mu[i]-mu[j])
                    check(flows[i,j]<=mu[j]/p,'flow_capacity_bound')
        for i in range(n):
            divergence=sum(w for (x,y),w in flows.items() if x==i)-sum(w for (x,y),w in flows.items() if y==i)
            check(divergence==F(i==0)-mu[i],'flow_divergence')
        residual=dict(flows);demands={i:mu[i] for i in range(1,n)};paths=[]
        while any(demands.values()):
            path=[0]
            while path[-1]==0 or demands[path[-1]]==0:
                x=path[-1]
                y=next(y for (v,y),w in residual.items() if v==x and w>0)
                path.append(y)
            amount=min([demands[path[-1]]]+[residual[x,y] for x,y in zip(path,path[1:])])
            demands[path[-1]]-=amount
            for edge in zip(path,path[1:]):residual[edge]-=amount
            paths.append((tuple(path),amount))
            check(len(path)-1<=n-1 and len(set(path))==len(path),'acyclic_path_length')
        check(not any(residual.values()),'path_flow_decomposition_complete')
        for x in range(1,n):
            check(sum(a for path,a in paths if path[-1]==x)==mu[x],'terminal_masses')
        path_total+=len(paths)
        functions=[[F(i==j) for i in range(n)] for j in range(n)]
        functions += [[F(rng.randrange(-4,5)) for _ in range(n)] for _ in range(3)]
        for f in functions:
            mean=sum(a*b for a,b in zip(mu,f));var=sum(a*(b-mean)**2 for a,b in zip(mu,f))
            anchored=sum(mu[x]*(f[x]-f[0])**2 for x in range(n))
            routed=(n-1)*sum(a*sum((f[x]-f[y])**2 for x,y in zip(path,path[1:])) for path,a in paths)
            energy=sum(mu[i]*K[i][j]*(f[i]-f[j])**2 for i in range(n) for j in range(i+1,n))
            check(var<=anchored<=routed<=F(d*(n-1),p)*energy,'full_variational_chain')

here=Path(__file__).resolve().parent
h=hashlib.sha256((here/'PARTIAL.md').read_bytes()).hexdigest()
check(h=='7e5b4acc667845034b4962bd009cfc1feaa4cb0eabffc90b0632622572364cb4','frozen_partial_hash')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),
 'checks':dict(sorted(counts.items())),'regular_graphs':len(graphs),
 'flow_models':3*len(graphs),'decomposed_paths':path_total,'partial_sha256':h,
 'limitation':'Exact finite controls supplement the all-size spectral formula and all-regular-graph flow proof. The undefined source endpoint remains unresolved.'},indent=2,sort_keys=True))
