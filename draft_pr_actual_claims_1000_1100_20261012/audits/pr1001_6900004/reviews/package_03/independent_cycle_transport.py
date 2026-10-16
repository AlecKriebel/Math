#!/usr/bin/env python3
"""Fresh cycle-flow derivation: exact collinear stress transport, no checker imports.
Finite diagnostics do not establish the universal topology statement.
"""
from fractions import Fraction as Q
from itertools import combinations
import json,sys

def demand(ok,msg):
    if not ok:raise RuntimeError(msg)
def signs(v):return tuple((x>0)-(x<0) for x in v)
def cycles(n,edges):
    parent=list(range(n));tree=[[] for _ in range(n)];chords=[]
    def root(u):
        while parent[u]!=u:u=parent[u]
        return u
    for c,(u,v) in enumerate(edges):
        ru,rv=root(u),root(v)
        if ru==rv:chords.append(c)
        else:
            parent[ru]=rv;tree[u].append((v,c));tree[v].append((u,c))
    result=[]
    for c in chords:
        u,v=edges[c];queue=[v];previous={v:None}
        for node in queue:
            if node==u:break
            for nxt,e in tree[node]:
                if nxt not in previous:previous[nxt]=(node,e);queue.append(nxt)
        demand(u in previous,'fundamental path missing');flow=[Q(0)]*len(edges);flow[c]=Q(1);node=u
        while node!=v:
            prev,e=previous[node];flow[e]=Q(1 if edges[e]==(prev,node) else -1);node=prev
        result.append(flow)
    for flow in result:
        balance=[Q(0)]*n
        for val,(u,v) in zip(flow,edges):balance[u]+=val;balance[v]-=val
        demand(not any(balance),'cycle conservation')
    return result,len(set(root(i) for i in range(n)))
def equilibrium(n,edges,points,w):
    force=[[Q(0)]*len(points[0]) for _ in range(n)]
    for (u,v),weight in zip(edges,w):
        for r in range(len(points[0])):
            f=weight*(points[v][r]-points[u][r]);force[u][r]+=f;force[v][r]-=f
    return not any(x for row in force for x in row)
def main():
    cases=0;basis_tests=0;counts={};samples=(Q(-1,2),Q(-1,3),Q(0),Q(1,4),Q(1,2));direction=(Q(0),Q(-2),Q(3))
    for n in range(1,6):
        universe=list(combinations(range(n),2));counts[str(n)]=0
        for mask in range(1<<len(universe)):
            canonical=[e for c,e in enumerate(universe) if mask>>c&1]
            edges=[e if c%2 else e[::-1] for c,e in enumerate(canonical)]
            basis,components=cycles(n,edges)
            demand(len(basis)==len(edges)-n+components,'cycle nullity')
            for i,j in universe:
                if (i,j) in canonical:continue
                counts[str(n)]+=1;x0=[Q(k+2) for k in range(n)];x0[i]=x0[j]=Q(0);delta0=[x0[v]-x0[u] for u,v in edges]
                demand(all(delta0),'initial actual edge collapsed')
                w0s=[[flow[c]/delta0[c] for c in range(len(edges))] for flow in basis]
                for t in samples:
                    xt=x0[:];xt[i]=t;points=[tuple(x*a for a in direction) for x in xt];deltat=[xt[v]-xt[u] for u,v in edges];demand(all(deltat),'moving actual edge collapsed');factors=[a/b for a,b in zip(delta0,deltat)];demand(all(f>0 for f in factors),'positive transport')
                    for flow,w0 in zip(basis,w0s):
                        wt=[factor*weight for factor,weight in zip(factors,w0)];demand(wt==[flow[c]/deltat[c] for c in range(len(edges))],'flow rescaling');demand(signs(wt)==signs(w0),'coordinate signs');demand(equilibrium(n,edges,points,wt),'vector forces');demand([weight/factor for factor,weight in zip(factors,wt)]==w0,'inverse');basis_tests+=1
                    # Reintroduce the missing edge solely for the support detector.
                    unit=[Q(0)]*len(edges)+[Q(1)];demand(equilibrium(n,edges+[(i,j)],points,unit)==(t==0),'singleton collision equivalence');cases+=1
    return {'status':'PASS','mechanism':'spanning-forest fundamental cycle flows scaled by scalar edge differences; no matrix kernel computation or candidate imports','arithmetic':'exact fractions.Fraction','nonedge_witnesses_by_n':counts,'placement_checks':cases,'cycle_basis_transport_checks':basis_tests,'samples':[str(t) for t in samples],'direction':['0','-2','3'],'mixed_edge_orientations':True,'limits':'Finite check only; manuscript and independent symbolic derivation supply all-n,d and connected components.'}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
