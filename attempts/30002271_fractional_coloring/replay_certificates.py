#!/usr/bin/env python3
"""Independent exact certificate reconstruction; no network or third-party packages."""
import json, itertools
from fractions import Fraction as F
import check_exact as original

def require(value, message):
    if not value: raise ValueError(message)

def replay():
    rows=[]
    for k in range(1,13):
        n=k*(k+1)
        edges={(i,j) for i in range(k) for j in range(i+1,k)} | {(i,k+i*k+j) for i in range(k) for j in range(k)}
        adj={v:{w for a,b in edges for w in ([b] if a==v else [a] if b==v else [])} for v in range(n)}
        # Enumerate maximal independent sets directly from the core/pedant structure.
        independent=[set(range(k,n))]+[{i}|{v for v in range(k,n) if (v-k)//k!=i} for i in range(k)]
        colors={v:(v if v<k else ((v-k)//k+1)%k) for v in range(n)} if k>=2 else {0:0,1:1}
        primal=[{'vertices':[v for v in range(n) if colors[v]==c], 'weight':'1'} for c in sorted(set(colors.values()))]
        dual=[int(v<k) for v in range(n)] if k>=2 else [1,1]
        require(all(not(set(p['vertices']) & adj[v]) for p in primal for v in p['vertices']),'primal independence')
        require(all(sum(F(p['weight']) for p in primal if v in p['vertices'])>=1 for v in range(n)), 'primal coverage')
        require(all(x>=0 for x in dual),'dual nonnegative')
        require(all(sum(dual[v] for v in s)<=1 for s in independent),'dual feasible')
        require(sum(F(p['weight']) for p in primal)==sum(dual)==max(k,2),'primal dual equality')
        gamma={v:F(len(adj[v])+1+(max(k,2) if v<k else 2),2) for v in range(n)}
        averages=[sum((gamma[w] for w in adj[v]|{v}),F())/(len(adj[v])+1) for v in range(n)]
        require(set(averages)=={F(3*k,4)+1 if k>=2 else F(2)},'all averages')
        # Exact finite-palette demand certificate, also include exceptional K2.
        slots=6*k if k>=2 else 2
        palette={v:set(range(4*v,4*v+4)) for v in range(k)} if k>=2 else {0:{0}}
        for v in range(k,n):
            parent=(v-k)//k
            palette[v]=set(x for x in range(slots) if x not in palette[parent])
            palette[v]=set(sorted(palette[v])[:3*k if k>=2 else 1])
        require(all(not(palette[a]&palette[b]) for a,b in edges),'demand adjacency')
        require(all(F(len(palette[v]),slots)>=1/gamma[v] for v in range(n)),'demand coverage')
        rows.append({'k':k,'edges':[list(e) for e in sorted(edges)],'primal':primal,'dual':dual,'maximal_independent_sets':[sorted(s) for s in independent],'gamma':[str(gamma[v]) for v in range(n)],'averages':list(map(str,averages)),'demand_slots':slots,'demand_palette':[sorted(palette[v]) for v in range(n)]})
    graphs=0
    for n in range(1,6):
        pairs=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            adj={v:set() for v in range(n)}
            for i,(a,b) in enumerate(pairs):
                if mask>>i&1: adj[a].add(b);adj[b].add(a)
            brute=[]
            for subset in range(1,1<<n):
                s={v for v in range(n) if subset>>v&1}
                if all(b in adj[a] for a,b in itertools.combinations(s,2)) and not any(all(v in adj[w] for w in s) for v in set(adj)-s): brute.append(frozenset(s))
            got=list(map(frozenset,original.maximal_cliques(adj)))
            require(len(got)==len(set(got)) and set(got)==set(brute),'exhaustive clique comparison')
            graphs+=1
    require(graphs==1099,'graph total')
    return {'problem_id':30002271,'cases':rows,'certificate_cases':12,'demand_cases':12,'exhaustive_graphs':graphs,'passed':True}
if __name__=='__main__': print(json.dumps(replay(),indent=2))
