"""Independent small-graph NP certificate control with explicit tree enumeration."""
from pathlib import Path
from itertools import product
from math import gcd
from functools import reduce
from datetime import datetime, timezone
import json

root=Path(__file__).resolve().parent
def connected(adj):
    for start in range(len(adj)):
        seen={start};todo=[start]
        while todo:
            for v in adj[todo.pop()]:
                if v not in seen:seen.add(v);todo.append(v)
        if len(seen)!=len(adj):return False
    return True
def trees(adj,target):
    others=[v for v in range(len(adj)) if v!=target];count=0
    for heads in product(*(adj[v] for v in others)):
        nxt=dict(zip(others,heads));valid=True
        for start in others:
            seen=set();v=start
            while v!=target and v not in seen:seen.add(v);v=nxt[v]
            if v!=target:valid=False;break
        count+=valid
    return count
def canonical(adj,state):
    x=list(state);f=[0]*len(adj);seen=set()
    while tuple(x) not in seen:
        seen.add(tuple(x));legal=[v for v in range(len(adj)) if x[v]>=len(adj[v])]
        if not legal:return True,f,x
        v=legal[0];x[v]-=len(adj[v]);f[v]+=1
        for w in adj[v]:x[w]+=1
    return False,f,x

graphs=inputs=halting=0;maxfirings=0;slack_failures=0
for n in (2,3):
    arcs=[(u,v) for u in range(n) for v in range(n) if u!=v]
    for mask in range(1<<len(arcs)):
        adj=[[v for i,(u,v) in enumerate(arcs) if u==a and mask>>i&1] for a in range(n)]
        if not connected(adj):continue
        graphs+=1;degree=list(map(len,adj));kappa=[trees(adj,w) for w in range(n)]
        g=reduce(gcd,kappa);pi=[a//g for a in kappa]
        assert min(pi)>0 and max(pi)<=(n-1)**(n-1)
        assert all(degree[v]*pi[v]==sum(pi[u] for u in range(n) if v in adj[u]) for v in range(n))
        cap=sum(degree)-n
        for x in product(range(cap+2),repeat=n):
            if sum(x)>cap+1:continue
            inputs+=1;halt,f,z=canonical(adj,x)
            if not halt:continue
            halting+=1;maxfirings=max(maxfirings,sum(f))
            assert any(f[w]<pi[w] for w in range(n))
            assert all(f[u]+1<=(n-1)**(2*n-2) for u in range(n))
            assert all(0<=z[v]<degree[v] for v in range(n))
            assert all(z[v]==x[v]-degree[v]*f[v]+sum(f[u] for u in range(n) if v in adj[u]) for v in range(n))
            for u in range(n):
                for v in adj[u]:
                    assert f[u]+1<=degree[v]*(f[v]+1)
                    slack_failures+=f[u]>degree[v]*f[v]
assert slack_failures>0
out={'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_FRESH_NP_CONTROLS','strongly_connected_simple_graphs':graphs,'configurations':inputs,'halting_inputs':halting,'largest_terminating_word':maxfirings,'failures_of_unshifted_source_inequality':slack_failures,'scope':'All labelled strongly connected loopless simple graphs on2 or3vertices; configurations through stable capacity plus1. Primitive periods enumerated via actual directed trees. Not a universal proof.'}
(root/'fresh-np-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
