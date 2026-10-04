#!/usr/bin/env python3
"""Exact finite controls for the general closure proof. Standard library only.
Integer scores are logarithms to base 2 of unnormalized positive weights.
None denotes a forbidden local pattern. Tests do not replace all-graph proofs.
"""
from itertools import product, combinations
from collections import Counter, deque
import random, json
rng=random.Random(30005303)
counts=Counter()
def check(condition, key):
    assert condition, key
    counts[key]+=1

def lattice_mtp(scores):
    S=list(scores)
    for x,y in product(S,repeat=2):
        lo=tuple(min(a,b) for a,b in zip(x,y)); hi=tuple(max(a,b) for a,b in zip(x,y))
        if lo not in scores or hi not in scores or scores[lo]+scores[hi]<scores[x]+scores[y]: return False
    return True

def support_control(n,edges,unary,tables):
    X=list(product((0,1),repeat=n));scores={}
    for x in X:
        terms=[unary[i][x[i]] for i in range(n)]+[tables[e][2*x[e[0]]+x[e[1]]] for e in edges]
        if all(t is not None for t in terms): scores[x]=sum(terms)
    if not scores or not lattice_mtp(scores): return False
    counts['accepted_boundary_models']+=1
    S=list(scores);m=tuple(min(x[i] for x in S) for i in range(n));M=tuple(max(x[i] for x in S) for i in range(n))
    active=[i for i in range(n) if m[i]!=M[i]];fixed=[i for i in range(n) if m[i]==M[i]]
    proj={e:{(x[e[0]],x[e[1]]) for x in S} for e in edges}
    arcs=[]
    for i,j in edges:
        if i in active and j in active:
            if (1,0) not in proj[i,j]: arcs.append((i,j))
            if (0,1) not in proj[i,j]: arcs.append((j,i))
    reach={(i,j):i==j or (i,j) in arcs for i in active for j in active}
    for k in active:
        for i in active:
            for j in active: reach[i,j]=reach[i,j] or (reach[i,k] and reach[k,j])
    comps=[];lookup={}
    for i in active:
        if i not in lookup:
            C=[j for j in active if reach[i,j] and reach[j,i]];k=len(comps);comps.append(C)
            for j in C:lookup[j]=k
    rep=[C[0] for C in comps];r=len(rep)
    le={(a,b):reach[rep[a],rep[b]] for a in range(r) for b in range(r)}
    for i,j in product(active,repeat=2):
        check((lookup[i]==lookup[j])==all(x[i]==x[j] for x in S),'SCC_equals_support_equality')
    for x in X:
        allowed=all(x[i]==m[i] for i in fixed) and all((x[i],x[j]) in proj[i,j] for i,j in edges)
        D=sum(x[i]!=m[i] for i in fixed)+sum(x[i]*(1-x[j]) for i,j in arcs)
        check(allowed==(x in scores),'support_projection_identity')
        check((D==0)==(x in scores),'violation_zero_set')
    constant=0;h=[0]*r;K=Counter();edge_choice={}
    for i in range(n):
        if i in fixed:constant+=unary[i][m[i]]
        else:constant+=unary[i][0];h[lookup[i]]+=unary[i][1]-unary[i][0]
    for i,j in edges:
        tab=tables[i,j]
        f=lambda a,b:tab[2*a+b]
        if i in fixed and j in fixed:constant+=f(m[i],m[j]);continue
        if i in fixed:
            constant+=f(m[i],0);h[lookup[j]]+=f(m[i],1)-f(m[i],0);continue
        if j in fixed:
            constant+=f(0,m[j]);h[lookup[i]]+=f(1,m[j])-f(0,m[j]);continue
        a,b=lookup[i],lookup[j]
        constant+=f(0,0)
        if a==b:h[a]+=f(1,1)-f(0,0)
        elif le[a,b]:h[b]+=f(0,1)-f(0,0);h[a]+=f(1,1)-f(0,1)
        elif le[b,a]:h[a]+=f(1,0)-f(0,0);h[b]+=f(1,1)-f(1,0)
        else:
            h[a]+=f(1,0)-f(0,0);h[b]+=f(0,1)-f(0,0)
            pair=tuple(sorted((a,b)));K[pair]+=f(1,1)-f(1,0)-f(0,1)+f(0,0);edge_choice[pair]=(i,j)
    for (a,b),k in K.items():
        U={d for d in range(r) if (d!=a and le[a,d]) or (d!=b and le[b,d])}
        square=[]
        for za,zb in product((0,1),repeat=2):
            T=U|({a} if za else set())|({b} if zb else set())
            x=list(m)
            for d,C in enumerate(comps):
                for i in C:x[i]=int(d in T)
            x=tuple(x);check(x in scores,'incomparable_square_support');square.append(scores[x])
        check(square[0]+square[3]-square[1]-square[2]==k,'incomparable_square_coefficient')
        check(k>=0,'aggregated_nonnegative_couplings')
    H=[0]*n;J=Counter()
    for a in range(r):H[rep[a]]=h[a]
    for pair,k in K.items():J[edge_choice[pair]]+=k
    L=lambda x:sum(H[i]*x[i] for i in range(n))+sum(k*x[i]*x[j] for (i,j),k in J.items())
    for x in S:check(constant+L(x)==scores[x],'log_weight_reconstruction')
    # Verify every smoothed score is an attractive quadratic on exactly G.
    t=7;HH=H[:];JJ=J.copy();offset=0
    for i in fixed:
        if m[i]==0:HH[i]-=t
        else:offset-=t;HH[i]+=t
    for i,j in arcs:HH[i]-=t;JJ[tuple(sorted((i,j)))]+=t
    for edge,k in JJ.items():check(edge in edges and k>=0,'lifted_graph_couplings')
    for x in X:
        D=sum(x[i]!=m[i] for i in fixed)+sum(x[i]*(1-x[j]) for i,j in arcs)
        score=offset+sum(HH[i]*x[i] for i in range(n))+sum(k*x[i]*x[j] for (i,j),k in JJ.items())
        check(score==L(x)-t*D,'smoothed_polynomial_identity')
    counts['active_components_total']+=r
    counts['nontrivial_support_models']+=int(1<len(S)<len(X))
    counts['incomparable_interactions_total']+=len(K)
    return True

def flow_control(n,edges,h,J):
    N=n+2;s=n;t=n+1;c=[[0]*N for _ in range(N)];b=[-a for a in h]
    for i,j in edges:c[i][j]+=J[i,j];b[i]-=J[i,j]
    for i in range(n):
        if b[i]>=0:c[i][t]+=b[i]
        else:c[s][i]+=-b[i]
    residual=[r[:] for r in c];value=0
    while True:
        parent=[None]*N;parent[s]=s;q=deque([s])
        while q and parent[t] is None:
            u=q.popleft()
            for v in range(N):
                if residual[u][v]>0 and parent[v] is None:parent[v]=u;q.append(v)
        if parent[t] is None:break
        path=[];v=t
        while v!=s:u=parent[v];path.append((u,v));v=u
        d=min(residual[u][v] for u,v in path)
        for u,v in path:residual[u][v]-=d;residual[v][u]+=d
        value+=d
    X=list(product((0,1),repeat=n));energy=lambda x:-sum(h[i]*x[i] for i in range(n))-sum(J[i,j]*x[i]*x[j] for i,j in edges)
    minimum=min(map(energy,X));kappa=sum(-z for z in b if z<0)
    check(value==minimum+kappa,'max_flow_min_cut')
    for u,v in product(range(N),repeat=2):
        check(residual[u][v]>=0,'nonnegative_residual_capacity')
        if u<n and v<n and u!=v and tuple(sorted((u,v))) not in edges:check(residual[u][v]==0,'no_new_nonterminal_edge')
    for x in X:
        T={s}|{i for i in range(n) if x[i]};outside=set(range(N))-T
        original=sum(c[u][v] for u in T for v in outside)
        cut=sum(residual[u][v] for u in T for v in outside)
        local=sum(residual[s][i]*(1-x[i])+residual[i][t]*x[i] for i in range(n))+sum(residual[i][j]*x[i]*(1-x[j])+residual[j][i]*x[j]*(1-x[i]) for i,j in edges)
        check(original==energy(x)+kappa,'network_energy_identity')
        check(cut==original-value,'residual_cut_identity')
        check(local==energy(x)-minimum,'bounded_factor_exponent_identity')
        if energy(x)==minimum:check(local==0,'common_unit_configuration')
    counts['flow_models']+=1

# Explicit cancellation case: two equality blocks, multiple connecting edges,
# with one negative original interaction and a positive aggregate interaction.
n=5;edges=[(0,1),(0,2),(1,3),(2,3),(3,4)];tabs={e:[0,0,0,0] for e in edges}
tabs[0,1]=tabs[2,3]=[0,None,None,0];tabs[0,2]=[0,0,0,-3];tabs[1,3]=[0,0,0,5];tabs[3,4]=[0,0,0,2]
assert support_control(n,edges,[[0,0] for _ in range(n)],tabs)
# Exact boundary tables, including fixed vertices, implications and equality.
for _ in range(10000):
    n=rng.randrange(1,7);edges=[e for e in combinations(range(n),2) if rng.random()<.5]
    unary=[[rng.choice([None,-2,-1,0,1,2]) for _ in range(2)] for i in range(n)]
    tables={e:[rng.choice([None,-2,-1,0,1,2]) for _ in range(4)] for e in edges}
    support_control(n,edges,unary,tables)
# Positive attractive examples and their exact max-flow gauges.
for _ in range(2000):
    n=rng.randrange(1,7);edges=[e for e in combinations(range(n),2) if rng.random()<.55]
    h=[rng.randrange(-8,9) for i in range(n)];J={e:rng.randrange(9) for e in edges}
    flow_control(n,edges,h,J)
    if _<300:support_control(n,edges,[[0,z] for z in h],{e:[0,0,0,J[e]] for e in edges})
# Finite multiscale degenerations, checked at the energy level without rounding.
for t in [1,2,5,10,100,10000]:
    edges=[(0,1),(1,2),(2,3),(0,3)]
    flow_control(4,edges,[-t*t,2*t,-t,3],{(0,1):2*t*t,(1,2):t,(2,3):3,(0,3):t+1})
nonassertions={'accepted_boundary_models','active_components_total','nontrivial_support_models','incomparable_interactions_total','flow_models'}
print(json.dumps({'status':'PASS','assertions':sum(v for k,v in counts.items() if k not in nonassertions),'seed':30005303,'counts':dict(sorted(counts.items()))},indent=2,sort_keys=True))
