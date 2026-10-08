#!/usr/bin/env python3
"""Independent finite audit: subset-DP cycles and Tarjan block classification.
No source material or third-party package is required. Finite checks are not a
proof of either asymptotic conjecture or of imported literature theorems.
"""
import itertools
import json
import os
import sys

CHECKS = 0

def require(value, message):
    global CHECKS
    CHECKS += 1
    if not value:
        raise ValueError(message)

def powerset(values):
    values = tuple(values)
    for bits in range(1 << len(values)):
        yield tuple(v for i,v in enumerate(values) if bits & (1 << i))

def distances(values):
    return frozenset(abs(a-b) for a,b in itertools.combinations(values,2))

def graph(n, edges):
    adjacency = [0] * n
    for u,v in edges:
        require(type(u) is int and type(v) is int and 0 <= u < n and 0 <= v < n and u != v, 'simple graph vertices')
        require(not (adjacency[u] >> v) & 1, 'duplicate graph edge')
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return adjacency

def spectrum(adj):
    """Held-Karp reachability on visited subsets, independently of DFS cycles."""
    answer = set()
    n = len(adj)
    for root in range(n):
        adjacency = [a >> root for a in adj[root:]]
        states = [0] * (1 << (n-root))
        states[1] = 1
        for mask in range(1,len(states),2):
            ends = states[mask]
            if not ends:
                continue
            if mask.bit_count() >= 3 and ends & adjacency[0]:
                answer.add(mask.bit_count())
            remaining_ends = ends
            while remaining_ends:
                bit = remaining_ends & -remaining_ends
                remaining_ends -= bit
                choices = adjacency[bit.bit_length()-1] & ~mask
                while choices:
                    nxt = choices & -choices
                    choices -= nxt
                    states[mask | nxt] |= nxt
    return frozenset(answer)

def hub_graph(N,A,B=None):
    edges = [(i,i+1) for i in range(N-1)] + [(N,a) for a in A]
    if B is None:
        return graph(N+1,edges)
    return graph(N+2,edges+[(N+1,b) for b in B])

def interval_formula(N,A,B):
    lengths = {d+2 for d in distances(A)|distances(B)}
    connectors = []
    for a in A:
        for b in B:
            lo,hi = sorted((a,b))
            connectors.append((frozenset(range(lo,hi+1)),hi-lo))
    for (left,d),(right,e) in itertools.combinations(connectors,2):
        if left.isdisjoint(right):
            lengths.add(d+e+4)
    return frozenset(lengths)

def cactus(adj):
    """Tarjan edge blocks; each block must be one edge or a simple cycle."""
    n=len(adj);time=0;disc=[-1]*n;low=[0]*n;stack=[];okay=True
    def visit(u,parent):
        nonlocal time,okay
        disc[u]=low[u]=time;time+=1
        for v in range(n):
            if not adj[u]>>v&1 or v==parent:
                continue
            if disc[v]<0:
                stack.append((u,v));visit(v,u);low[u]=min(low[u],low[v])
                if low[v]>=disc[u]:
                    block=[]
                    while stack:
                        edge=stack.pop();block.append(edge)
                        if edge==(u,v):break
                    if len(block)>1:
                        degrees={}
                        for a,b in block:
                            degrees[a]=degrees.get(a,0)+1;degrees[b]=degrees.get(b,0)+1
                        if len(block)!=len(degrees) or any(d!=2 for d in degrees.values()):okay=False
            elif disc[v]<disc[u]:
                stack.append((u,v));low[u]=min(low[u],disc[v])
    for u in range(n):
        if disc[u]<0:visit(u,-1)
    return okay

def partitions(total,minimum=1):
    if total==0:
        yield ()
    for first in range(minimum,total+1):
        for tail in partitions(total-first,first):yield (first,)+tail

def theta_graph(lengths):
    edges=[];next_vertex=2
    for length in lengths:
        path=[0]+list(range(next_vertex,next_vertex+length-1))+[1]
        next_vertex+=length-1;edges.extend(zip(path,path[1:]))
    return graph(next_vertex,edges)

def main():
    require(sys.flags.isolated==1, 'isolated mode required')
    require(os.geteuid()!=0, 'nonroot audit required')
    all_graph_counts=[];cactus_counts=[];graph_cases=0
    for n in range(7):
        edges=tuple(itertools.combinations(range(n),2));images=set();cactus_images=set()
        for chosen in powerset(edges):
            adj=graph(n,chosen);C=spectrum(adj);images.add(C);graph_cases+=1
            if cactus(adj):cactus_images.add(C)
        target={frozenset(S) for S in powerset(range(3,n+1)) if sum(x-1 for x in S)<=n-1} if n else {frozenset()}
        require(cactus_images==target, 'exhaustive cactus vertex budget')
        all_graph_counts.append(len(images));cactus_counts.append(len(cactus_images))
    require(all_graph_counts==[1,1,1,2,4,6,11], 'f(n) through six')
    fan_cases=0
    for N in range(11):
        for A in powerset(range(N)):
            require(spectrum(hub_graph(N,A))=={d+2 for d in distances(A)}, 'one-hub identity')
            fan_cases+=1
    baseline_cases=0
    for m in range(2,9):
        images=set()
        for B in powerset(range(m+1,2*m+1)):
            adj=graph(2*m,[(v,v+1) for v in range(2*m-1)]+[(0,b-1) for b in B])
            C=spectrum(adj);images.add(C)
            require({ell for ell in C if ell>m}==set(B), 'Faudree high-band decoder')
            baseline_cases+=1
        require(len(images)==2**m, 'Faudree cardinality')
    require(spectrum(graph(2,[(0,1)]))==frozenset() and all_graph_counts[2]==1,'m=1 control')
    require(distances((0,1,4,6))==distances((0,1,2,3,6))==frozenset(range(1,7)),'one-hub collision')
    distance_counts=[];missing_cases=0;fib=[0,1]
    for i in range(25):fib.append(sum(fib[-2:]))
    for N in range(1,17):
        images=set();missing=[0]*N
        for A in powerset(range(N)):
            D=distances(A);images.add(D)
            if N<=14:
                for d in range(1,N):missing[d]+=d not in D
        distance_counts.append(len(images))
        if N<=14:
            for d in range(1,N):
                q,r=divmod(N,d)
                require(missing[d]==fib[q+2]**(d-r)*fib[q+3]**r,'exact missing-distance recurrence')
                matching=sum(len(range(a,N,d))//2 for a in range(d))
                require(2*matching>=N-d, 'matching-size lower bound')
                require(missing[d]*4**matching<=2**N*3**matching,'exact probability comparison')
                missing_cases+=1
    theta_cases=0
    for weight in range(13):
        for partition in partitions(weight):
            for edge in [(),(1,)]:
                lengths=tuple(w+1 for w in partition)+edge
                require(spectrum(theta_graph(lengths))=={a+b for a,b in itertools.combinations(lengths,2)},'theta formula')
                theta_cases+=1
    twohub_cases=0
    for N in range(7):
        for A in powerset(range(N)):
            for B in powerset(range(N)):
                require(spectrum(hub_graph(N,A,B))==interval_formula(N,A,B),'two-hub interval formula')
                twohub_cases+=1
    specialized_cases=0
    for m in range(2,7):
        for t in range(1,m):
            for B in powerset(range(m,2*m)):
                predicted={b+2 for b in B}|{d+2 for d in distances(B)}|{t+2}|{b-t+4 for b in B}
                require(spectrum(hub_graph(2*m,(0,t),(0,)+B))==predicted,'specialized two-hub formula')
                specialized_cases+=1
    collision=[]
    for B in [(6,7,9,11),(6,7,8,9,11)]:
        collision.append(sorted(spectrum(hub_graph(12,(0,5),(0,)+B))))
    require(collision[0]==collision[1]==[3,4,5,6,7,8,9,10,11,13],'fourteen-vertex collision')
    symmetric_counts=[]
    for m in range(1,8):
        choices=[(0,)+B for B in powerset(range(m,2*m))]
        images={interval_formula(2*m,A,B) for A in choices for B in choices}
        symmetric_counts.append(len(images))
        if m<=4:
            direct={spectrum(hub_graph(2*m,A,B)) for A in choices for B in choices}
            require(images==direct,'symmetric two-hub images from DP')
    require(symmetric_counts==[3,6,19,46,127,310,721], 'symmetric family counts')
    return {'schema':'erdos-cycle-sets-independent-checks-v1','checks':CHECKS,'uid':os.geteuid(),'optimize':sys.flags.optimize,'isolated':sys.flags.isolated,'all_graph_cases':graph_cases,'exact_f_n0_to_n6':all_graph_counts,'exact_cactus_counts_n0_to_n6':cactus_counts,'one_hub_cases':fan_cases,'faudree_cases':baseline_cases,'distance_counts_n1_to_n16':distance_counts,'missing_distance_cases':missing_cases,'theta_cases':theta_cases,'two_hub_cases':twohub_cases,'specialized_two_hub_cases':specialized_cases,'symmetric_two_hub_counts':symmetric_counts,'fourteen_vertex_collision_spectrum':collision[0],'formal_certification':False,'main_problem_resolved':False}

if __name__=='__main__':
    try:
        print(json.dumps(main(),sort_keys=True))
    except (ValueError,TypeError,OverflowError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);sys.exit(1)
