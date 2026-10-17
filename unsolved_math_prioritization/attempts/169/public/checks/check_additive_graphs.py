#!/usr/bin/env python3
"""Exact finite representation graphs; no asymptotic inference."""
from fractions import Fraction as F
from itertools import combinations,permutations,product
from collections import Counter
from math import prod,factorial
import json

def require(ok,msg):
    if not ok: raise ValueError(msg)


def rat(x):
    x=F(x);return [x.numerator,x.denominator]


def rank_mod(rows,p):
    a=[r[:] for r in rows];rank=0
    for col in range(len(a[0]) if a else 0):
        pivot=next((i for i in range(rank,len(a)) if a[i][col]%p),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank];u=pow(a[rank][col],-1,p)
        a[rank]=[x*u%p for x in a[rank]]
        for i in range(rank+1,len(a)):
            u=a[i][col]
            if u:a[i]=[(x-u*y)%p for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank


def partitions(n):
    def rec(i,blocks):
        if i==n:yield tuple(tuple(x) for x in blocks);return
        for j in range(len(blocks)):
            blocks[j].append(i);yield from rec(i+1,blocks);blocks[j].pop()
        blocks.append([i]);yield from rec(i+1,blocks);blocks.pop()
    yield from rec(0,[])


def kernel_vectors(B,p):
    # RREF of B^T, whose kernel consists of edge-space cycle vectors.
    a=[list(row) for row in zip(*B)];width=len(B);rank=0;pivots=[]
    for col in range(width):
        pivot=next((i for i in range(rank,len(a)) if a[i][col]%p),None)
        if pivot is None:continue
        a[rank],a[pivot]=a[pivot],a[rank];u=pow(a[rank][col],-1,p)
        a[rank]=[x*u%p for x in a[rank]]
        for i in range(len(a)):
            if i==rank:continue
            u=a[i][col];a[i]=[(x-u*y)%p for x,y in zip(a[i],a[rank])]
        pivots.append(col);rank+=1
    free=[j for j in range(width) if j not in pivots]
    for values in product(range(p),repeat=len(free)):
        z=[0]*width
        for col,value in zip(free,values):z[col]=value
        for i,col in enumerate(pivots):z[col]=-sum(a[i][j]*z[j] for j in free)%p
        require(all(sum(row[e]*z[e] for e in range(width))%p==0 for row in zip(*B)),'cycle kernel vector')
        yield z


def cycle_checks():
    results=[];assignments=labelings=partition_terms=0
    for p,k,t in ((5,2,3),(7,2,4),(7,3,3)):
        v=k+t;all_edges=list(product(range(k),range(t)));graphs=list(combinations(range(k*t),p))
        unrestricted=Counter();distinct=Counter();covers=0;representation_sum=0
        for z in product(range(p),repeat=v):
            assignments+=1;groups=[[] for x in range(p)]
            for e,(i,j) in enumerate(all_edges):groups[(z[i]+z[k+j])%p].append(e)
            if any(not a for a in groups):continue
            is_distinct=len(set(z[:k]))==k and len(set(z[k:]))==t
            if is_distinct:covers+=1;representation_sum+=prod(map(len,groups))
            for selection in product(*groups):
                J=tuple(sorted(selection));unrestricted[J]+=1
                if is_distinct:distinct[J]+=1
        require(sum(distinct.values())==representation_sum,'double count representations')
        Ps=list(partitions(p));case=[];perms=list(permutations(range(p)))
        for J in graphs:
            edges=[all_edges[e] for e in J];adj=[[] for i in range(v)];B=[]
            for e,(i,j) in enumerate(edges):
                adj[i].append((k+j,e));adj[k+j].append((i,e))
                b=[0]*v;b[i]=b[k+j]=1;B.append(b)
            # Forest traversal stores parent edge for each nonroot vertex.
            seen=set();roots=[];order=[]
            for root in range(v):
                if root in seen:continue
                roots.append(root);seen.add(root);queue=[root]
                for u in queue:
                    for w,e in adj[u]:
                        if w not in seen:seen.add(w);queue.append(w);order.append((w,u,e))
            h=len(roots);rank=rank_mod(B,p)
            require(rank==v-h,'graph rank including isolated vertices')
            N=0
            for labels in perms:
                labelings+=1;z=[0]*v
                for w,u,e in order:z[w]=(labels[e]-z[u])%p
                N+=all((z[i]+z[k+j])%p==labels[e] for e,(i,j) in enumerate(edges))
            require(unrestricted[J]==p**h*N,'independent vertex/forest cycle count')
            require(N==0 or N>=p*(p-1),'affine label orbit lower bound')
            fourier=None
            if J==graphs[0]:
                freq=Counter()
                vectors=list(kernel_vectors(B,p))
                require(len(vectors)==p**(p-rank),'cycle kernel dimension')
                for xi in vectors:
                    for ell in perms:freq[sum(x*y for x,y in zip(xi,ell))%p]+=1
                require(len({freq[x] for x in range(1,p)})==1,'cyclotomic frequency symmetry')
                exact_character_sum=freq[0]-freq[1]
                require(exact_character_sum==N*p**(p-rank),'exact Fourier cycle identity')
                fourier={'cycle_vectors':len(vectors),'permutations_per_vector':len(perms),
                         'character_residue_frequencies':[freq[x] for x in range(p)],
                         'character_sum':exact_character_sum,'N_J':N,
                         'nonzero_mode_contribution_to_N':rat(N-F(factorial(p),p**(p-rank)))}
            mobius=0
            for P in Ps:
                mu=prod((-1)**(len(block)-1)*factorial(len(block)-1) for block in P)
                D=[]
                for block in P:
                    for e in block[1:]:D.append([(x-y)%p for x,y in zip(B[e],B[block[0]])])
                rr=rank_mod(D,p);mobius+=mu*p**(v-rr);partition_terms+=1
            require(mobius==unrestricted[J],'collision-partition Mobius identity')
            if distinct[J]:require(distinct[J]>=p*p*(p-1),'distinct vertex affine orbit lower bound')
            case.append({'graph_edges':[list(e) for e in edges],'h':h,'rank':rank,'N_J':N,'Q_unrestricted':unrestricted[J],'Q_distinct':distinct[J],
                         'independent_cycle_zero_mode':rat(F(factorial(p),p**(p-rank))),'exact_fourier_check':fourier})
        feasible=sum(bool(distinct[J]) for J in graphs)
        lam=F(k*t,p);orderedA=prod(range(p-k+1,p+1));orderedT=prod(range(p-t+1,p+1))
        bound=F(orderedA*orderedT,p*p*(p-1))*lam**p
        require(feasible<=bound,'feasible graph sparsity bound')
        require(representation_sum<=orderedA*orderedT*lam**p,'AMGM representation upper bound')
        results.append({'p':p,'k':k,'t':t,'graphs':case,'distinct_coordinate_feasible_graphs':feasible,
                        'feasible_graph_bound':rat(bound),'ordered_cover_pairs':covers,'representation_sum':representation_sum})
    return {'cases':results,'vertex_assignments':assignments,'permutation_labelings':labelings,'mobius_partition_terms':partition_terms}


if __name__=='__main__':
    print(json.dumps({'scope':'Exact synthetic graph identities only; no asymptotic probability claim.','cycle_counting':cycle_checks()},sort_keys=True,indent=2))
