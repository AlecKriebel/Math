"""Finite exact diagnostics for the accompanying proof, Python >=3.10, stdlib.
MIT licensed. No service calls, external imports, input files or asserts.
Finite tests do not prove the theorem or literature priority.
"""
import itertools
import functools
import json

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def vertices(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length()-1
        mask -= low

def graph(n, edges):
    adj = [0]*n
    for u,v in edges:
        need(0 <= u < n and 0 <= v < n and u != v, "invalid edge")
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return tuple(adj)

def connected(adj, S):
    if not S:
        return False
    seen = todo = S & -S
    while todo:
        bit = todo & -todo
        todo -= bit
        v = bit.bit_length()-1
        fresh = adj[v] & S & ~seen
        todo |= fresh
        seen |= fresh
    return seen == S

def edges_in(adj, S):
    return sum((adj[v] & S).bit_count() for v in vertices(S))//2

def two_connected(adj, S):
    return S.bit_count() >= 3 and all(
        connected(adj,S & ~(1<<v)) for v in vertices(S))

def matcher(adj):
    @functools.lru_cache(None)
    def pm(S):
        if not S:
            return True
        if S.bit_count()%2:
            return False
        v = (S & -S).bit_length()-1
        rest = S & ~(1<<v)
        return any(pm(rest & ~(1<<u)) for u in vertices(adj[v] & rest))
    return pm

def factor_critical_max(adj):
    pm = matcher(adj)
    best = 0
    for S in range(1,1<<len(adj)):
        if two_connected(adj,S) and all(pm(S & ~(1<<v)) for v in vertices(S)):
            best = max(best,edges_in(adj,S)-S.bit_count()+1)
    return best

def base_max(adj, require_connected=True):
    pm = matcher(adj)
    return max((edges_in(adj,S) for S in range(1,1<<len(adj))
                if pm(S) and (not require_connected or connected(adj,S))), default=0)

def cone(adj):
    n = len(adj)
    return tuple(a | (1<<n) for a in adj) + ((1<<n)-1,)

def direct_ear_beta(adj, count_initial=True, count_single=True, stop_at_even=True):
    """Search COMPLETE decompositions using unused-edge masks and open paths.
    It never calls the factor-critical or cone optimizer."""
    n = len(adj)
    edge_list = [(u,v) for u in range(n) for v in vertices(adj[u]) if u < v]
    eid = {frozenset(e):1<<i for i,e in enumerate(edge_list)}
    all_edges = (1<<len(edge_list))-1
    circuits = set()
    def cycles(start, v, seen, em, length):
        for w in vertices(adj[v]):
            if w == start and length >= 2:
                circuits.add(em | eid[frozenset((v,w))])
            elif w > start and not (seen >> w & 1):
                cycles(start,w,seen | (1<<w),em | eid[frozenset((v,w))],length+1)
    for v in range(n):
        cycles(v,v,1<<v,0,0)

    @functools.lru_cache(None)
    def old_vertices(em):
        S = 0
        for i in vertices(em):
            u,v = edge_list[i]
            S |= (1<<u) | (1<<v)
        return S

    @functools.lru_cache(None)
    def new_ears(used):
        old = old_vertices(used)
        result = set()
        def grow(start, v, seen, em):
            for w in vertices(adj[v]):
                e = eid[frozenset((v,w))]
                if used & e:
                    continue
                if old >> w & 1:
                    if w != start:
                        result.add(em | e)
                elif not (seen >> w & 1):
                    grow(start,w,seen | (1<<w),em | e)
        for start in vertices(old):
            grow(start,start,1<<start,0)
        return tuple(sorted(result))

    @functools.lru_cache(None)
    def extend(used, active):
        if used == all_edges:
            return 0
        best = -1000000
        for ear in new_ears(used):
            odd = ear.bit_count()%2 == 1
            onward = active and (odd or not stop_at_even)
            reward = int(active and odd and (count_single or ear.bit_count()>1))
            best = max(best,reward+extend(used | ear,onward))
        return best

    return max((int(count_initial and c.bit_count()%2 == 1) +
                extend(c,c.bit_count()%2 == 1 or not stop_at_even)
                for c in circuits),default=-1000000)

def system(m, sets, k):
    left=[]; right=[]; connectors=[]; es=[]; next_v=0
    for i in range(m+1):
        L=list(range(next_v,next_v+k));next_v+=k
        R=list(range(next_v,next_v+k));next_v+=k
        left.append(L);right.append(R);es.extend(itertools.product(L,R))
    for A in sets:
        c=next_v;next_v+=1;connectors.append(c)
        es.append((c,right[0][0]))
        es.extend((c,right[i+1][0]) for i in vertices(A))
    return graph(next_v,es),left,right,connectors

def minimum_cover(m, sets):
    for r in range(len(sets)+1):
        for J in itertools.combinations(range(len(sets)),r):
            union=0
            for j in J: union |= sets[j]
            if union == (1<<m)-1:
                return list(J)
    return None

def preprocessing(m, sets, s):
    """Return a fixed triangle threshold, or None for the nontrivial branch."""
    if s < 0:
        return 2
    if m == 0:
        return 1
    union = 0
    for A in sets:
        union |= A
    if not sets or union != (1<<m)-1 or s == 0:
        return 2
    if s >= len(sets):
        return 1
    return None

def witness(m, sets, s):
    J=minimum_cover(m,sets)
    if J is None or len(J)>s:
        return None
    # A minimum-cardinality cover is inclusion-minimal.
    private=[]
    for j in J:
        other=0
        for h in J:
            if h!=j: other |= sets[h]
        choices=sets[j] & ~other
        need(choices!=0,"private element missing")
        private.append(next(vertices(choices)))
    need(len(private)==len(set(private)),"private elements collide")
    T=sum(1+A.bit_count() for A in sets)
    k=T+len(sets)+3
    adj,L,R,C=system(m,sets,k)
    S=sum(1<<v for group in L+R for v in group)
    pairs=[]
    assigned={i+1:j for j,i in zip(J,private)}
    for j,i in zip(J,private):
        S |= 1<<C[j]
        S &= ~(1<<L[i+1][0])
        pairs.append((C[j],R[i+1][0]))
    for i in range(m+1):
        if i in assigned:
            pairs.extend(zip(L[i][1:],R[i][1:]))
        else:
            pairs.extend(zip(L[i],R[i]))
    touched=0
    for u,v in pairs:
        need(adj[u]>>v&1,"matching nonedge")
        need(not touched & ((1<<u)|(1<<v)),"matching overlap")
        touched |= (1<<u)|(1<<v)
    need(touched==S,"matching not perfect")
    need(connected(adj,S),"witness not connected")
    M=(m+1)*k*k;F=M-k*s
    exact=M-k*len(J)+sum(1+sets[j].bit_count() for j in J)
    need(edges_in(adj,S)==exact and exact>=F,"forward edge threshold")
    need(k>T and k>s and k*k>k*s+T and F>0,"gap constants")
    return {"m":m,"sets":list(sets),"s":s,"k":k,"cover":J,
            "vertices":len(adj),"selected_edges":exact,"threshold":F}

def main():
    small=[]
    for l,r in [(1,1),(1,2),(2,1),(2,2)]:
        es=list(itertools.product(range(l),range(l,l+r)))
        for mask in range(1<<len(es)):
            B=graph(l+r,[e for i,e in enumerate(es) if mask>>i&1])
            if not connected(B,(1<<len(B))-1):
                continue
            G=cone(B)
            a=direct_ear_beta(G);b=base_max(B);c=factor_critical_max(G)
            need(a==b==c,("three objectives",l,r,mask,a,b,c))
            small.append([l,r,mask,a])
    # Larger sparse examples, still direct complete-ear searches.
    for E in [[(0,3),(0,4),(1,3),(1,5),(2,5)],
              [(0,3),(0,4),(1,4),(1,5),(2,3),(2,5)]]:
        B=graph(6,E);G=cone(B)
        a=direct_ear_beta(G);b=base_max(B);c=factor_critical_max(G)
        need(a==b==c,"larger cone objective")
        small.append([3,3,E,a])
    square=graph(4,[(0,2),(0,3),(1,2),(1,3)]);G=cone(square)
    single=direct_ear_beta(G, count_single=False)
    initial=direct_ear_beta(G,count_initial=False)
    need(direct_ear_beta(G)==4 and single==2 and initial==3,"ear counting controls")
    triangle=graph(3,[(0,1),(1,2),(0,2)])
    need(direct_ear_beta(triangle)==1,"fixed triangle")
    C4=graph(4,[(0,1),(1,2),(2,3),(0,3)])
    need(two_connected(triangle,7) and all(a.bit_count()==2 for a in triangle),
         "triangle cone class")
    need(not any(a.bit_count()==3 for a in C4),"C4 no universal vertex")
    preprocess_checks = []
    for m in (0,1,2):
        for n in (0,1,2):
            for A in itertools.product(range(1<<m), repeat=n):
                minimum = minimum_cover(m,A)
                for s in range(-1,n+2):
                    out = preprocessing(m,A,s)
                    expected = minimum is not None and len(minimum) <= s
                    if out is not None:
                        need((1 >= out) == expected,"fixed preprocessing answer")
                    else:
                        need(m>=1 and n>=1 and 1<=s<=n and minimum is not None,
                             "nontrivial preprocessing branch")
                    preprocess_checks.append([m,list(A),s,out])
    # Balanced does not imply perfectly matchable.
    bad=graph(6,[(0,3),(1,3),(2,3),(2,4),(2,5)])
    need(connected(bad,63) and not matcher(bad)(63),"balance is not matching")
    witnesses=[];systems=0;thresholds=0
    for m in (1,2):
        for n in (1,2,3):
            for A in itertools.product(range(1<<m),repeat=n):
                union=0
                for v in A: union |= v
                if union!=(1<<m)-1:continue
                systems+=1
                for s in range(1,n+1):
                    thresholds+=1
                    w=witness(m,A,s)
                    if w is not None:witnesses.append(w)
    identities=0
    for k in range(1,30):
        for a,b in itertools.product(range(k+1),repeat=2):
            d=k*(a+b)-a*b
            need(d-k*(a-b)==b*(2*k-a) and d>=k*(a-b),"omission identity")
            identities+=1
    # Full induced-subset enumeration on the connectivity-distinction example:
    # 20 vertices would be costly; enumerate all actual subsets of a smaller
    # analogous k=2 construction, independently of any block normal form.
    B,L,R,C=system(2,(1,2),2)
    conn=base_max(B);relaxed=base_max(B,False)
    need(relaxed==12 and conn==12,"k=2 equality boundary")
    # k=3 relaxation gap: all block vertices attain27; matching-loss upper
    # bound for the two connectors is25, constructed witness attains25.
    B,L,R,C=system(2,(1,2),3)
    S=(1<<len(B))-1
    S &= ~(1<<L[1][0]);S &= ~(1<<L[2][0])
    need(connected(B,S) and matcher(B)(S) and edges_in(B,S)==25,"k3 connected witness")
    blocks=sum(1<<v for group in L+R for v in group)
    need(matcher(B)(blocks) and not connected(B,blocks) and edges_in(B,blocks)==27,
         "dropping connectivity changes feasible family")
    # Falsify d >= k(a+b), an invalid stronger inequality.
    k=3;a=b=1;d=k*(a+b)-a*b
    need(d<k*(a+b),"stronger loss mutant")
    # Published boundary H3 of Benchetrit--Sebo, Section3.2:
    # three copies of a chorded C5 sharing the triangle edge (0,1).
    # This tests the first-even cutoff against an actually different optimum.
    es=[(0,1)]
    for i in range(3):
        a,b,c=2+3*i,3+3*i,4+3*i
        es.extend([(1,a),(a,b),(b,c),(c,0),(0,a)])
    H=graph(11,es)
    prefix=direct_ear_beta(H)
    total=direct_ear_beta(H,stop_at_even=False)
    need(prefix==2 and total>=3,"published first-even cutoff boundary")
    cutoff={"edges":es,"prefix":prefix,"total_odd_mutant":total,
            "source":"Benchetrit--Sebo1509.05586v1 Section3.2 H3"}
    return {"status":"PASS","finite_evidence_only":True,
            "complete_ear_cone_factorcritical_comparisons":small,
            "set_systems":systems,"thresholds":thresholds,
            "preprocessing_case_count":len(preprocess_checks),
            "preprocessing_cases":preprocess_checks,
            "full_actual_k_forward_witness_count":len(witnesses),
            "full_actual_k_forward_witnesses":witnesses,
            "exact_omission_identity_count":identities,
            "false_controls":{"omit_one_edge_count":[4,single],
                             "omit_initial_count":[4,initial],
                             "balanced_not_matchable":True,
                             "C4_outside_cone_class":True,
                             "stronger_loss_inequality_false":True,
                             "disconnected_relaxation":[27,25],
                             "first_even_cutoff":cutoff},
            "small_full_induced_subset_boundary":{"k":2,"connected":conn,"relaxed":relaxed}}
if __name__=="__main__":
    print(json.dumps(main(),sort_keys=True,indent=2))

