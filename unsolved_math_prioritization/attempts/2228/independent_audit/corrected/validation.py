"""Finite sanity checks for the authored lemmas; standard library only.
These checks do not decide the infinite extremal problem.
"""
import itertools, json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def cycles(adj):
    # Unique minimum vertex is first; orientation selected by second < last.
    for start in range(len(adj)):
        def dfs(path, used):
            last = path[-1]
            if len(path) >= 3 and start in adj[last] and path[1] < path[-1]:
                yield tuple(path)
            for nxt in sorted(adj[last]):
                if nxt > start and nxt not in used:
                    yield from dfs(path + [nxt], used | {nxt})
        yield from dfs([start], {start})


def graph(n, edges):
    a = [set() for _ in range(n)]
    for u,v in edges:
        require(0 <= u < n and 0 <= v < n and u != v, "invalid simple-graph edge")
        a[u].add(v); a[v].add(u)
    return a


def components(a):
    unseen = set(range(len(a)))
    while unseen:
        todo = [unseen.pop()]; s = set(todo)
        while todo:
            for v in a[todo.pop()]:
                if v in unseen:
                    unseen.remove(v); s.add(v); todo.append(v)
        yield s


def check(a):
    cs = list(cycles(a)); witnesses = []; margins=[]
    for c in cs:
        s = set(c); induced = sum(len(a[v]&s) for v in s)//2
        q = induced-len(c); boundary=sum(len(a[v]-s) for v in s)
        require(2*(q-len(c)) == sum(len(a[v])-4 for v in s)-boundary, "boundary identity mismatch")
        margins.append(q-len(c))
        if q >= len(c): witnesses.append(c)
    if max(map(len,a),default=0) <= 4:
        classified = any(all(len(a[v])==4 for v in s) and any(set(c)==s for c in cs) for s in components(a))
        require(bool(witnesses)==classified, "maximum-degree-four classification mismatch")
    return {'vertices':len(a),'edges':sum(map(len,a))//2,'cycles':len(cs),'max_cycle_length':max(map(len,cs),default=0),'max_chords_minus_length':max(margins,default=None),'violating_cycles':len(witnesses)}


def main():
    tested=0
    for n in range(6):
        es=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(es)):
            a=graph(n,[e for k,e in enumerate(es) if mask>>k&1])
            check(a);tested+=1
    es=[]
    for off in [0,5]:
        es += [(off+i,off+j) for i,j in itertools.combinations(range(5),2) if (i,j)!=(0,1)]
        es += [(10,off),(10,off+1)]
    a=graph(11,es)
    require(all(len(x)==4 for x in a), "example is not four-regular")
    explicit=check(a);require(explicit['violating_cycles']==0 and explicit['max_cycle_length']<11, "example classification mismatch")
    fam=[]
    for n in range(6,12):
        z=check(graph(n,[(i,j) for i in range(3) for j in range(3,n)]))
        require(z['violating_cycles']==0 and z['edges']==3*n-9, "bipartite family mismatch")
        fam.append(z)
    out={'passed':True,'all_labeled_graphs_orders_0_through_5':tested,'eleven_vertex_example':explicit,'complete_bipartite_family':fam,'scope':'Finite consistency checks only; the proofs establish the general statements. No global extremal claim is inferred.'}
    p=Path(__file__).with_name('validation_results.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
