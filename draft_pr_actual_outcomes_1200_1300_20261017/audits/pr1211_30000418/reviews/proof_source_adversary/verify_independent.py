"""Independent adversarial checks from the explicit graph and definitions.
No submitted programs or certificate data are imported or executed.
Run from this folder or any cwd; JSON output is beside this script.
"""
from collections import deque
from datetime import datetime, timezone
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent
SUBMITTED = HERE.parent.parent / 'submitted'
V = ('a', 'b', 'c', 'd', 'e', 'a1', 'a2', 'b1', 'd1', 'e1', 'e2')
E = (('a','b'), ('b','c'), ('c','d'), ('d','e'), ('a','a1'), ('a','a2'), ('b','b1'), ('d','d1'), ('e','e1'), ('e','e2'))
A = tuple(range(1,6))
B = (1,3,4,5,6)
BAD = {v: B if v in ('a1','a2','e1','e2') else A for v in V}
WITNESS = dict(zip(V, (1,5,3,1,5,3,4,2,4,2,3)))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def adjacency(vertices, edges):
    adj = {v:set() for v in vertices}
    for u,v in edges:
        require(u != v and v not in adj[u], 'loop or duplicate edge')
        adj[u].add(v); adj[v].add(u)
    return adj

def distances(adj):
    out = {}
    for start in adj:
        d = {start:0}; queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u]+1; queue.append(v)
        out[start] = d
    return out

def valid(adj, lists, labels):
    if set(labels) != set(adj) or any(labels[v] not in lists[v] for v in adj):
        return False
    for v,ns in adj.items():
        if any(abs(labels[v]-labels[w]) < 2 for w in ns):
            return False
        if len({labels[w] for w in ns}) != len(ns):
            return False
    return True

def count_global(adj, lists):
    # Build every constraint from independent shortest-path searches, then use
    # fixed-order global search, without the tree-state recurrence or Hall.
    dist = distances(adj)
    req = {v:{w:2 if d == 1 else 1 for w,d in dist[v].items() if 1 <= d <= 2} for v in adj}
    order = sorted(adj, key=lambda v:(-len(req[v]), str(v)))
    labels = {}; first = None
    def rec(i):
        nonlocal first
        if i == len(order):
            if first is None: first = labels.copy()
            return 1
        v = order[i]; total = 0
        for q in lists[v]:
            if all(abs(q-labels[w]) >= gap for w,gap in req[v].items() if w in labels):
                labels[v] = q; total += rec(i+1); del labels[v]
        return total
    return rec(0),first

def rooted(adj, root):
    par = {root:None}; order = [root]
    for v in order:
        for w in sorted(adj[v],key=str):
            if w not in par: par[w]=v; order.append(w)
    return par,order

def count_dp(adj, lists, root):
    par,order = rooted(adj,root)
    children={v:[w for w in order if par[w] == v] for v in order}
    @lru_cache(None)
    def state(v,p,q):
        # Explicit local domain guards, the suggested textual clarification.
        if q not in lists[v] or p is not None and abs(q-p)<2: return 0
        total=0
        for child_labels in product(*(lists[w] for w in children[v])):
            if len(set(child_labels)) != len(child_labels) or p in child_labels: continue
            ways=1
            for w,r in zip(children[v],child_labels): ways *= state(w,q,r)
            total+=ways
        return total
    answer=sum(state(root,None,q) for q in lists[root])
    compatible=sum(1 for v in order for q in lists[v] for p in ([None] if par[v] is None else lists[par[v]]) if p is None or abs(p-q)>=2)
    return answer, compatible

def greedy(adj, lists, root):
    par,order=rooted(adj,root); labels={}
    delta=max(map(len,adj.values()),default=0); max_forbidden=0
    for v in order:
        forbidden=set()
        for w in adj[v]:
            if w in labels: forbidden.update((labels[w]-1,labels[w],labels[w]+1))
            for z in adj[w]:
                if z != v and z in labels: forbidden.add(labels[z])
        max_forbidden=max(max_forbidden,len(forbidden))
        require(not labels or len(forbidden) <= delta+2,'greedy forbidden bound failed')
        choices=set(lists[v])-forbidden
        require(bool(choices),'greedy list exhausted')
        labels[v]=min(choices)
    require(valid(adj,lists,labels),'greedy witness invalid')
    return max_forbidden

def prufer_tree(n, code):
    if n == 1: return {0:set()}
    deg=[1]*n
    for v in code: deg[v]+=1
    edges=[]
    for v in code:
        leaf=next(u for u in range(n) if deg[u] == 1)
        edges.append((leaf,v));deg[leaf]-=1;deg[v]-=1
    rem=[u for u in range(n) if deg[u] == 1]
    edges.append(tuple(rem))
    return adjacency(range(n),edges)

def extensions(lengths):
    adj=adjacency(V,E);labels=WITNESS.copy()
    for leaf,length in zip(('a1','a2','b1','d1','e1','e2'),lengths):
        old=leaf
        for i in range(length):
            v=f'{leaf}x{i}'
            adj[v]={old};adj[old].add(v)
            forbidden={labels[old]-1,labels[old],labels[old]+1}
            for z in adj[old]-{v}: forbidden.add(labels[z])
            choices=set(A)-forbidden
            require(bool(choices),'pendant extension failed')
            labels[v]=min(choices);old=v
    require(max(map(len,adj.values())) == 3,'extension changed max degree')
    require(valid(adj,{v:A for v in adj},labels),'invalid extended ordinary labeling')
    return len(adj)

adj=adjacency(V,E);dist=distances(adj)
require(len(E)==len(V)-1 and all(len(d)==len(V) for d in dist.values()),'not tree')
require(valid(adj,{v:A for v in V},WITNESS),'ordinary witness invalid')
D2=[(u,v) for u,v in combinations(V,2) if dist[u][v] == 2]
result={'started_or_rerun_utc':datetime.now(timezone.utc).isoformat(),
        'proof_sha256':hashlib.sha256((SUBMITTED/'PROOF.md').read_bytes()).hexdigest(),
        'audit_sha256':hashlib.sha256((SUBMITTED/'AUDIT.md').read_bytes()).hexdigest(),
        'graph':{'vertices':len(V),'edges':len(E),'degree':{v:len(adj[v]) for v in V},'distance_two_pairs':D2,'diameter':max(max(d.values()) for d in dist.values()),'radius':min(max(d.values()) for d in dist.values())}}
counts={};dp={}
for name,lists in [('bad',BAD)]+[(f'common{k}',{v:tuple(range(1,k+1)) for v in V}) for k in (4,5,6)]:
    count,_=count_global(adj,lists);counts[name]=count
    per_root={r:count_dp(adj,lists,r) for r in V}
    require(all(t[0] == count for t in per_root.values()),'DP/global count mismatch')
    dp[name]={'all_11_root_counts_equal_global':True,'root_a_edge_compatible_states':per_root['a'][1]}
require(counts == {'bad':0,'common4':0,'common5':8,'common6':6336},'unexpected exact counts')
result['counts']=counts;result['dp']=dp
result['dp_missing_guard_example']={'tree':'single vertex with external parent','p':1,'q':1,'child_sets':[], 'SDR_exists':True,'valid_state':False,'required_guard':'q in L(v) and (p is None or abs(p-q)>=2)'}
# Local obstruction equations, independent of whole-graph enumeration.
near={x:[y for y in A if abs(x-y)>=2] for x in A}
end={x:[r for r in B if abs(x-r)>=2 and r != 1] for x in (4,5)}
require(near == {1:[3,4,5],2:[4,5],3:[1,5],4:[1,2],5:[1,2,3]},'A neighborhood mismatch')
require(end == {4:[6],5:[3]},'endpoint contradiction mismatch')
result['local_obstruction']={'A_compatible_neighbors':near,'B_leaf_after_b1':end}
# Every labeled tree through six vertices, every root, arbitrary non-interval
# list patterns: dense translated, sparse, and pseudorandom positive lists.
rng=random.Random(121130000418);trees=roots=runs=0;largest_forbidden=0
for n in range(1,7):
    for code in product(range(n),repeat=max(0,n-2)):
        t=prufer_tree(n,code);delta=max(map(len,t.values()));k=delta+3;trees+=1
        patterns=[{v:tuple(range(1,k+1)) for v in t},
                  {v:tuple(1+3*j+2*v for j in range(k)) for v in t},
                  {v:tuple(sorted(rng.sample(range(1,5*k+1),k))) for v in t}]
        for root in t:
            roots+=1
            for lists in patterns:
                largest_forbidden=max(largest_forbidden,greedy(t,lists,root));runs+=1
result['greedy']={'labeled_trees_orders1to6':trees,'rooted_trees':roots,'list_patterns_per_root':3,'runs':runs,'max_observed_forbidden':largest_forbidden}
# All 4^6 small extension vectors plus long and uneven independent extensions.
length_vectors=list(product(range(4),repeat=6))+[(100,0,0,0,0,0),(100,100,100,100,100,100),(0,1,20,0,50,2)]
max_n=max(extensions(x) for x in length_vectors)
result['extensions']={'vectors_tested':len(length_vectors),'max_order':max_n,'all_ordinary_witnesses_valid':True}
# Rank-compression direction over all labeled graphs on 3 vertices and all
# 2-list assignments with values in [1,5], including disconnected graphs.
smallV=(0,1,2);edge_choices=list(combinations(smallV,2));small_lists=list(combinations(range(1,6),2));cases=badcases=good_lift=0
for bits in product((0,1),repeat=3):
    g=adjacency(smallV,[e for e,b in zip(edge_choices,bits) if b])
    for lists_tuple in product(small_lists,repeat=3):
        lists=dict(zip(smallV,lists_tuple));union=sorted(set().union(*map(set,lists_tuple)))
        ranks={q:i+1 for i,q in enumerate(union)}
        comp={v:tuple(ranks[q] for q in lists[v]) for v in g}
        co,wo=count_global(g,lists);cc,wc=count_global(g,comp);cases+=1
        if co == 0:
            badcases+=1;require(cc==0,'bad original compressed feasible')
        if cc:
            good_lift+=1;lift={v:union[q-1] for v,q in wc.items()}
            require(valid(g,lists,lift),'compressed witness lift invalid')
edge=adjacency((0,1),((0,1),))
orig,_=count_global(edge,{0:(1,3),1:(1,3)});comp,_=count_global(edge,{0:(1,2),1:(1,2)})
require(orig==2 and comp==0,'reverse-direction witness failed')
result['rank_compression']={'cases':cases,'original_bad_cases':badcases,'compressed_feasible_witnesses_lifted':good_lift,'all_claimed_directions_hold':True,'reverse_failure':{'graph':'K2','original_lists':[[1,3],[1,3]],'original_solutions':orig,'compressed_solutions':comp}}
edge_boundary_cases=0
for left in combinations(range(1,7),3):
    for right in combinations(range(1,7),3):
        require(count_global(edge,{0:left,1:right})[0]>0,'edge three-list boundary failed')
        edge_boundary_cases+=1
result['boundaries']={'single_edge_three_lists_on_universe1to6':edge_boundary_cases,
                      'all_feasible':True,
                      'common_two_list_edge_solution_count':count_global(edge,{0:(1,2),1:(1,2)})[0],
                      'empty_graph_solution_count':count_global({}, {})[0],
                      'isolated_vertex_single_list_solution_count':count_global({0:set()},{0:(999,)})[0]}
result['completed_utc']=datetime.now(timezone.utc).isoformat()
result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(HERE/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
