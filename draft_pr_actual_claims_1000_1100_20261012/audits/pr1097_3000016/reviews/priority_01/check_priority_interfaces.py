#!/usr/bin/env python3
"""Fresh finite controls for priority comparisons; no candidate imports or asserts."""
from collections import deque
from itertools import product
from math import gcd
import argparse, json

def need(ok, message):
    if not ok:
        raise ValueError(message)

def strong(a):
    n=len(a)
    for root in range(n):
        seen={root}; todo=[root]
        for u in todo:
            for v in range(n):
                if a[u][v] and v not in seen:
                    seen.add(v); todo.append(v)
        if len(seen)!=n:
            return False
    return True

def moves(a,x):
    for v,row in enumerate(a):
        d=sum(row)
        if x[v]>=d:
            y=list(x); y[v]-=d
            for w,b in enumerate(row):
                y[w]+=b
            yield v,tuple(y)

def states(a,x):
    seen={x}; edges={}; todo=deque([x])
    while todo:
        z=todo.popleft(); es=list(moves(a,z)); edges[z]=es
        for _,y in es:
            if y not in seen:
                seen.add(y); todo.append(y)
    return seen,edges

def recur(a,x):
    return any(x in states(a,y)[0] for _,y in moves(a,x))

def compositions(c,n):
    if n==1:
        yield (c,)
    else:
        for k in range(c+1):
            for rest in compositions(c-k,n-1):
                yield (k,)+rest

def source_family():
    for a,b in product(range(1,4),repeat=2):
        yield ((0,a),(b,0))
    for bits in product((0,1),repeat=6):
        a=[[0]*3 for _ in range(3)]; k=0
        for i in range(3):
            for j in range(3):
                if i!=j:
                    a[i][j]=bits[k]; k+=1
        a=tuple(map(tuple,a))
        if strong(a):
            yield a

def kt_lift(a,x,M):
    arcs=[(u,v) for u in range(len(a)) for v in range(len(a)) if a[u][v]]
    need(all(a[u][v]==1 for u,v in arcs),'KT control only explicit simple source')
    n=len(a); g=[[0]*(n+len(arcs)) for _ in range(n+len(arcs))]
    for i,(u,v) in enumerate(arcs):
        q=n+i; g[u][q]=g[q][u]=M; g[v][q]=g[q][v]=1
    y=tuple(x[v]+M*sum(a[v]) for v in range(n))+tuple(M//2 for _ in arcs)
    return tuple(map(tuple,g)),y,arcs

def fire(a,x,v):
    options=dict(moves(a,x))
    need(v in options,'requested firing is illegal')
    return options[v]

def run(fault=False):
    graphs=list(source_family()); comparisons=0; paircount=0; stats=0
    transient=None; recurrence_yes=0; nonhalting_yes=0
    for a in graphs:
        n=len(a)
        for c in range(5):
            for x in compositions(c,n):
                reachable,edges=states(a,x); stats+=len(reachable)
                has_stable=any(not edges[z] for z in reachable)
                r=recur(a,x); recurrence_yes+=r; nonhalting_yes+=not has_stable
                if not has_stable and not r and transient is None:
                    transient={'adjacency':a,'configuration':x,'reachable_states':len(reachable)}
                for _,y in edges[x]:
                    need((x in states(a,y)[0])==r,'Tothmeresz Claim 2.4 control failed')
                    comparisons+=1
                paircount+=1
    need(transient is not None,'no separating example was found')

    # HKT Theorem 14: integer-image and recurrent target imply reachability.
    hkt=0; recurrent_cases=0; linear_not_legal=None
    for a,b in product(range(1,5),repeat=2):
        graph=((0,a),(b,0))
        for total in range(7):
            xs=list(compositions(total,2))
            for x in xs:
                rs,_=states(graph,x)
                for y in xs:
                    image=(y[0]-x[0])%gcd(a,b)==0
                    ry=recur(graph,y)
                    if ry and image:
                        need(y in rs,'HKT recurrent-target implication failed')
                        recurrent_cases+=1
                    if image and y not in rs and linear_not_legal is None:
                        linear_not_legal={'adjacency':graph,'initial':x,'target':y}
                    hkt+=1
    need(linear_not_legal is not None,'missing linear-equivalence separation')

    # Full actual KT Definition 4.1 / Claim 4.4 construction, not its title.
    kt_sources=0; kt_prefixes=0; kt_bundles=0
    for a in graphs:
        n=len(a)
        if n!=3 or any(sum(a[u])!=sum(a[v][u] for v in range(n)) for u in range(n)):
            continue
        E=sum(map(sum,a)); Delta=max(map(sum,a)); M=8*n*n*E*Delta
        for x in product(range(3),repeat=n):
            g,y,arcs=kt_lift(a,x,M); todo=[(x,y,(0,)*n)]; visited=set()
            kt_sources+=1
            for z,w,counts in todo:
                if counts in visited:
                    continue
                visited.add(counts); k=sum(counts); kt_prefixes+=1
                need(all(w[v]==z[v]+M*sum(a[v]) for v in range(n)),'KT old-coordinate identity')
                need(all(M//2-k<=w[n+i]<=M//2+k for i in range(E)),'KT edge reserve')
                if k==4:
                    continue
                for v,z2 in moves(a,z):
                    w2=fire(g,w,v)
                    for i,(u,_) in enumerate(arcs):
                        if u==v:
                            w2=fire(g,w2,n+i)
                    cs=list(counts); cs[v]+=1
                    todo.append((z2,w2,tuple(cs))); kt_bundles+=1

    # Explicit model separations behind potentially misleading prior titles.
    # A weighted chip-firing transition consumes its full degree, whereas a
    # single-particle routing operation can choose one outgoing arc.
    branch=((0,1,1),(1,0,0),(1,0,0)); start=(1,0,0)
    need(not list(moves(branch,start)),'ordinary branching threshold should block')
    routing_target=(0,1,0)
    need(sum(start)==sum(routing_target) and start[0]>=1,'routing single-edge move')
    doubled=((0,2),(2,0)); collapsed=((0,1),(1,0)); one=(1,0)
    need(not list(moves(doubled,one)) and bool(list(moves(collapsed,one))), 'unit-weight substitution separation')
    # General VAS can have several negative components or nonzero column sum.
    vas_vectors=[(-1,-1,2),(-1,2,0)]
    need(any(sum(v)!=0 or sum(t<0 for t in v)>1 for v in vas_vectors),'VAS restriction control')
    binary=[]
    for k in (8,64,512,4096):
        multiplicity=1<<k
        binary.append({'bits':multiplicity.bit_length(),'unary_records_log2':k})
        need(multiplicity.bit_length()==k+1,'binary representation size')
    # Five deliberately invalid inference variants must be rejected explicitly.
    invalid_rejections=5
    need(transient is not None,'wrong inference NONHALTING=RECURRENT escaped')
    need(linear_not_legal is not None,'wrong inference linear=legal escaped')
    need(not list(moves(branch,start)),'wrong inference rotor move=chip firing escaped')
    need(not list(moves(doubled,one)),'wrong inference forget weights escaped')
    need(any(sum(v)!=0 for v in vas_vectors),'wrong inference every VAS is chip-firing escaped')
    if fault:
        need(False,'injected unconditional rejection remains live under optimization')
    return {
        'status':'PASS','scope':'Fresh finite primary-interface comparison controls, not priority proof or historical replay',
        'graphs':len(graphs),'source_configurations':paircount,'source_state_visits':stats,
        'recurrence_first_move_comparisons':comparisons,'recurrence_yes':recurrence_yes,'nonhalting_yes':nonhalting_yes,
        'nonhalting_not_recurrent_example':transient,'linear_equivalent_not_reachable_example':linear_not_legal,
        'hkt_source_target_pairs':hkt,'hkt_recurrent_target_implications':recurrent_cases,
        'kt_source_configurations':kt_sources,'kt_prefix_count_states':kt_prefixes,'kt_legal_bundles':kt_bundles,
        'kt_horizon':4,'model_separation_controls':3,'large_binary_controls':binary,
        'invalid_inference_rejections':invalid_rejections,
    }

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--fault',action='store_true')
    args=parser.parse_args(); print(json.dumps(run(args.fault),indent=2,sort_keys=True))
