"""Independent exact checks for the simple Set Cover reduction; standard library only."""
import itertools, functools, json, pathlib


def cover_number(m, sets):
    for r in range(len(sets)+1):
        for c in itertools.combinations(range(len(sets)), r):
            union = 0
            for j in c: union |= sets[j]
            if union == (1<<m)-1: return r
    return None


def incidence(m, sets):
    return [{0} | {i+1 for i in range(m) if s>>i & 1} for s in sets]


def compressed_opt(m, sets, k):
    """Exact saturation-state optimizer, separately validated on explicit vertex subsets.
    An active block contains a vertex. Saturation fills it to k+k vertices,
    or (k-1)+k when its representative is used to match one connector.
    """
    inc = incidence(m, sets)
    best = k*k
    for cm in range(1, 1<<len(sets)):
        cs = [j for j in range(len(sets)) if cm>>j & 1]
        r = len(cs)
        for bm in range(1, 1<<(m+1)):
            bs = {i for i in range(m+1) if bm>>i & 1}
            if len(bs)<r: continue
            adj = {j: inc[j]&bs for j in cs}
            if any(not adj[j] for j in cs): continue
            # Connectivity of the selected connector/block incidence graph.
            seen_c, seen_b = {cs[0]}, set()
            while True:
                new_b = set().union(*(adj[j] for j in seen_c))
                new_c = {j for j in cs if adj[j]&new_b}
                if new_c == seen_c and new_b == seen_b: break
                seen_c, seen_b = new_c, new_b
            if seen_b != bs or len(seen_c)!=r: continue
            # Hall feasibility tested by direct injection search.
            def inject(t, used):
                return t==r or any(inject(t+1,used|{b}) for b in adj[cs[t]]-used)
            if not inject(0,set()): continue
            val = len(bs)*k*k-k*r+sum(len(adj[j]) for j in cs)
            best=max(best,val)
    return best


def graph(m, sets, k):
    N=2*k*(m+1)+len(sets)
    adj=[0]*N
    def add(u,v):
        adj[u]|=1<<v; adj[v]|=1<<u
    for i in range(m+1):
        for l in range(k):
            for r in range(k): add(2*k*i+l,2*k*i+k+r)
    for j, blocks in enumerate(incidence(m,sets)):
        for i in blocks: add(2*k*(m+1)+j,2*k*i+k)
    return adj


def exact_subset_optimizer(adj, beta=False):
    N=len(adj)
    @functools.lru_cache(None)
    def pm(mask):
        if not mask: return True
        if mask.bit_count()%2: return False
        vb=mask&-mask; v=vb.bit_length()-1; rest=mask^vb
        candidates=adj[v]&rest
        while candidates:
            b=candidates&-candidates; candidates^=b
            if pm(rest^b): return True
        return False
    def connected(mask):
        if not mask: return False
        seen=fringe=mask&-mask
        while fringe:
            v=fringe&-fringe; fringe^=v
            extra=adj[v.bit_length()-1]&mask&~seen
            seen|=extra; fringe|=extra
        return seen==mask
    def vertices(mask):
        while mask:
            b=mask&-mask; mask^=b; yield b
    best=0
    for mask in range(1,1<<N):
        if beta:
            if mask.bit_count()<3 or not mask.bit_count()%2: continue
            if not all(pm(mask^b) and connected(mask^b) for b in vertices(mask)): continue
        elif not pm(mask) or not connected(mask): continue
        e=sum((adj[b.bit_length()-1]&mask).bit_count() for b in vertices(mask))//2
        score=e-mask.bit_count()+1 if beta else e
        best=max(best,score)
    return best


def main():
    explicit=[]
    for m,n in [(1,1),(1,2),(2,1),(2,2),(2,3)]:
        for sets in itertools.product(range(1<<m),repeat=n):
            if cover_number(m,sets) is None: continue
            a=graph(m,sets,2)
            actual=exact_subset_optimizer(a)
            comp=compressed_opt(m,sets,2)
            assert actual==comp,(m,sets,actual,comp)
            explicit.append((m,n))
    cones=[]
    for m,n in [(1,1),(1,2),(2,1),(2,2)]:
        for sets in itertools.product(range(1<<m),repeat=n):
            if cover_number(m,sets) is None: continue
            a=graph(m,sets,2); N=len(a)
            cone=[x|(1<<N) for x in a]+[(1<<N)-1]
            actual=exact_subset_optimizer(cone,beta=True)
            comp=compressed_opt(m,sets,2)
            assert actual==comp,(m,sets,actual,comp)
            cones.append((m,n))
    instances=decisions=0; max_vertices=max_edges=0
    for m in range(1,4):
        for n in range(1,4):
            for sets in itertools.product(range(1<<m),repeat=n):
                tau=cover_number(m,sets)
                if tau is None: continue
                T=sum(1+s.bit_count() for s in sets)
                k=T+n+3
                optimum=compressed_opt(m,sets,k)
                for s in range(n+1):
                    F=(m+1)*k*k-k*s
                    assert (optimum>=F)==(tau<=s),(m,sets,s,k,optimum,F,tau)
                    decisions+=1
                max_vertices=max(max_vertices,2*k*(m+1)+n+1)
                max_edges=max(max_edges,(m+1)*k*k+T+2*k*(m+1)+n)
                instances+=1
    results={"method":"standard-library exact enumeration; no randomized sampling", "explicit_vertex_subset_instances":len(explicit),"explicit_cone_factor_critical_instances":len(cones),"valid_k_compressed_set_systems":instances,"valid_k_threshold_decisions":decisions,"largest_cone_vertices":max_vertices,"largest_cone_edges":max_edges,"failures":0,"limitations":"Finite checks corroborate the proof; compressed larger tests use the saturation invariant proved in AUDIT_HARDNESS.md. They are not a substitute for proof."}
    p=pathlib.Path(__file__).with_name('audit_set_cover_results.json')
    p.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
