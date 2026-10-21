#!/usr/bin/env python3
"""Fresh finite proof controls, written for this edition; stdout only.

No candidate/sibling checker is imported. No historical omitted program is replayed.
All requirements use unconditional exceptions and remain active with Python -O.
"""
import sys
sys.dont_write_bytecode = True
import argparse
from collections import deque
from itertools import product
from math import gcd
import json

def need(q, message):
    if not q:
        raise ValueError(message)

def degrees(a):
    return tuple(sum(row) for row in a)

def moves(a, x):
    return tuple(v for v, d in enumerate(degrees(a)) if x[v] >= d)

def fire(a, x, v):
    need(v in moves(a, x), "illegal requested firing")
    y = list(x)
    y[v] -= sum(a[v])
    for w, count in enumerate(a[v]):
        y[w] += count
    need(sum(y) == sum(x), "conservation failed")
    return tuple(y)

def strong(a):
    for start in range(len(a)):
        seen = {start}
        todo = [start]
        while todo:
            v = todo.pop()
            for w, count in enumerate(a[v]):
                if count and w not in seen:
                    seen.add(w)
                    todo.append(w)
        if len(seen) != len(a):
            return False
    return True

def space(a, initial, limit=100000):
    pred = {tuple(initial): None}
    queue = deque(pred)
    edges = {}
    stable = False
    while queue:
        x = queue.popleft()
        edges[x] = []
        legal = moves(a, x)
        stable |= not legal
        for v in legal:
            y = fire(a, x, v)
            edges[x].append((y, v))
            if y not in pred:
                pred[y] = (x, v)
                queue.append(y)
                need(len(pred) <= limit, "state-space cap; no completed check")
    incoming = {x: 0 for x in edges}
    for row in edges.values():
        for y, _ in row:
            incoming[y] += 1
    queue = deque(x for x, d in incoming.items() if d == 0)
    removed = 0
    while queue:
        x = queue.popleft()
        removed += 1
        for y, _ in edges[x]:
            incoming[y] -= 1
            if incoming[y] == 0:
                queue.append(y)
    cycle = removed < len(edges)
    need(stable != cycle, "halting dichotomy failed in complete finite graph")
    return edges, pred, cycle

def construct(a, x, scale=None, early=0):
    n = len(a)
    cutoff = (sum(x) + 1) ** n
    scale = cutoff + 1 if scale is None else scale
    budget = cutoff * (scale * max(degrees(a)) + 1)
    h = [[0] * (n + 2) for _ in range(n + 2)]
    for v in range(n):
        for w in range(n):
            h[v][w] = scale * a[v][w]
        h[v][n] = 1
        h[n][v] = budget
    h[n][n+1] = h[n+1][n] = 1
    initial = tuple(scale * t + cutoff for t in x) + (n * budget + 1 - cutoff + early, 0)
    count = (cutoff,) * n + (1, 0)
    target = list(initial)
    for v, t in enumerate(count):
        target[v] -= sum(h[v]) * t
        for w, mult in enumerate(h[v]):
            target[w] += mult * t
    return tuple(map(tuple, h)), initial, tuple(target), cutoff, scale, budget

def prefix_and_cleanup(a, x):
    h, initial, target, cutoff, scale, budget = construct(a, x)
    n = len(a)
    need(strong(h) and all(h[v][v] == 0 for v in range(n+2)), "output graph class")
    need(min(initial + target) >= 0 and sum(initial) == sum(target), "output validity")
    need(target[-1] == 1 and initial[-1] == 0, "marker endpoint")
    layers = {(0,) * n: (tuple(x), initial)}
    states = transitions = cleanup = 0
    has_cutoff = False
    for total in range(cutoff + 1):
        following = {}
        for counts, (z, w) in layers.items():
            states += 1
            need(all(w[v] == scale*z[v] + cutoff-counts[v] for v in range(n)), "old invariant")
            need(w[-2] == sum(h[-2])-cutoff+total and w[-1] == 0, "gate/marker invariant")
            need((n in moves(h, w)) == (total == cutoff), "gate timing")
            need(n+1 not in moves(h, w), "early marker")
            if total < cutoff:
                need(tuple(v for v in moves(h, w) if v < n) == moves(a, z), "prefix legality")
                for v in moves(a, z):
                    count = list(counts)
                    count[v] += 1
                    count = tuple(count)
                    next_pair = (fire(a, z, v), fire(h, w, v))
                    if count in following:
                        need(following[count] == next_pair, "count-state identity")
                    following[count] = next_pair
                    transitions += 1
            else:
                has_cutoff = True
                start = fire(h, w, n)
                need(min(start[:n]) >= budget, "cleanup initial budget")
                # Every remaining-count ordering, not just a chosen block schedule.
                pending = deque([(counts, start)])
                seen = {counts}
                while pending:
                    count, state = pending.popleft()
                    if count == (cutoff,) * n:
                        need(state == target, "cleanup endpoint")
                    for v in range(n):
                        if count[v] < cutoff:
                            need(v in moves(h, state), "cleanup order illegally funded")
                            nxt = list(count)
                            nxt[v] += 1
                            nxt = tuple(nxt)
                            end = fire(h, state, v)
                            cleanup += 1
                            if nxt not in seen:
                                seen.add(nxt)
                                pending.append((nxt, end))
        layers = following
        if not layers and total < cutoff:
            break
    _, _, nonhalting = space(a, x)
    need(has_cutoff == nonhalting, "cutoff classification")
    return states, transitions, cleanup, nonhalting

def xgcd(a, b):
    if b == 0:
        return a, 1, 0
    g, u, v = xgcd(b, a % b)
    return g, v, u - (a // b) * v

def reduced_two(a, b, x, y):
    d = y[0] - x[0]
    g, u, v = xgcd(a, b)
    if sum(x) != sum(y) or d % g:
        return None
    h = (-u * (d // g), v * (d // g))
    period = (b // g, a // g)
    shift = min(h[i] // period[i] for i in range(2))
    count = tuple(h[i] - shift*period[i] for i in range(2))
    need(min(count) >= 0 and any(count[i] < period[i] for i in range(2)), "reduced count")
    need(-a*count[0] + b*count[1] == d, "integer image equation")
    return count

def certificate(a, b, x, g, u, proper=True, strict=True):
    if min(u) < 0 or any(u[i] > g[i] for i in range(2)) or (proper and u == g):
        return False
    state = (x[0]-a*u[0]+b*u[1], x[1]+a*u[0]-b*u[1])
    return all((state[i] < (a,b)[i] if strict else state[i] <= (a,b)[i])
               for i in range(2) if u[i] < g[i])

def signed_normalize(a, x):
    b = [list(row) for row in a]
    y = list(x)
    for v in range(len(a)):
        offset = max(0, -x[v])
        b[v][v] += offset
        y[v] += offset
    return tuple(map(tuple, b)), tuple(y)

def relay(a, x):
    n = len(a)
    owners = [v for v in range(n) if a[v][v]]
    b = [[0]*(n+len(owners)) for _ in range(n+len(owners))]
    for v in range(n):
        for w in range(n):
            if v != w:
                b[v][w] = a[v][w]
    for k, v in enumerate(owners):
        b[v][n+k] = b[n+k][v] = a[v][v]
    return tuple(map(tuple, b)), tuple(x)+(0,)*len(owners), owners

def run():
    coverage = {"source_instances": 0, "prefix_states": 0, "prefix_transitions": 0,
                "cleanup_order_transitions": 0, "source_nonhalting": 0}
    for a, b in product(range(1,4), repeat=2):
        matrix = ((0,a),(b,0))
        for x in product(range(3), repeat=2):
            s, t, c, nh = prefix_and_cleanup(matrix, x)
            coverage["source_instances"] += 1
            coverage["prefix_states"] += s
            coverage["prefix_transitions"] += t
            coverage["cleanup_order_transitions"] += c
            coverage["source_nonhalting"] += nh
    # A three-vertex cycle and an imbalanced strongly connected source add dimension controls.
    for matrix in (((0,1,0),(0,0,1),(1,0,0)), ((0,2,0),(0,0,1),(1,0,0))):
        for x in ((0,0,0),(1,0,0),(0,1,0)):
            s,t,c,nh = prefix_and_cleanup(matrix,x)
            coverage["source_instances"] += 1
            coverage["prefix_states"] += s
            coverage["prefix_transitions"] += t
            coverage["cleanup_order_transitions"] += c
            coverage["source_nonhalting"] += nh
    unrestricted = []
    for a,b in product(range(1,3),repeat=2):
        matrix=((0,a),(b,0))
        for x in ((0,0),(1,0),(0,1)):
            h,X,Y,N,M,B=construct(matrix,x)
            edges,_,cycle=space(h,X)
            _,_,nh=space(matrix,x)
            need((Y in edges)==nh, "unrestricted arbitrary-odometer equivalence")
            unrestricted.append({"a":a,"b":b,"x":x,"states":len(edges),"reachable":Y in edges,"source_nonhalting":nh})
    # Explicit two target-reaching words with different gate/marker counts.
    a=((0,1),(1,0));h,X,Y,N,M,B=construct(a,(1,0))
    z=X; word=[]; counts=[0]*4
    for _ in range(N):
        v=next(v for v in moves(h,z) if v<2)
        z=fire(h,z,v);word.append(v);counts[v]+=1
    z=fire(h,z,2);word.append(2);counts[2]+=1
    for v in range(2):
        while counts[v]<N:
            z=fire(h,z,v);word.append(v);counts[v]+=1
    need(z==Y,"designated word")
    period=(B,B,1,1); left=list(period); extra=[]
    while any(left):
        available=[v for v in moves(h,z) if left[v]>0]
        need(available,"complete period blocked")
        v=available[0];left[v]-=1;extra.append(v);z=fire(h,z,v)
    need(z==Y,"period endpoint")
    alternative={"first_counts":counts,"additional_period":period,
                 "second_counts":[counts[v]+period[v] for v in range(4)],
                 "first_word":word,"extra_word":extra}
    pairs=partial=found=nonimage=0
    for a,b in product(range(1,4),repeat=2):
        matrix=((0,a),(b,0))
        for total in range(5):
            for k in range(total+1):
                x=(k,total-k);states,_,_=space(matrix,x)
                for j in range(total+1):
                    y=(j,total-j);pairs+=1;g=reduced_two(a,b,x,y)
                    if g is None:
                        need(y not in states,"nonimage reachable");nonimage+=1;continue
                    witness=False
                    for u in product(range(g[0]+1),range(g[1]+1)):
                        partial+=1
                        if certificate(a,b,x,g,u):
                            need(y not in states,"false nonreachability certificate")
                            witness=True
                    need(witness==(y not in states),"certificate completeness")
                    found+=witness
    signed_cases=signed_edges=relay_states=0
    for loops in product(range(2),repeat=2):
        a=((loops[0],1),(1,loops[1]))
        for x in product(range(-1,3),repeat=2):
            b,y=signed_normalize(a,x)
            # Finite signed state orbit is bounded below by its initial minima.
            edges,_,nh=space(a,x)
            offsets=tuple(y[v]-x[v] for v in range(2))
            for z,row in edges.items():
                zz=tuple(z[v]+offsets[v] for v in range(2))
                need(moves(a,z)==moves(b,zz),"signed threshold conjugacy")
                for end,v in row:
                    need(fire(b,zz,v)==tuple(end[w]+offsets[w] for w in range(2)),"signed update conjugacy")
                    signed_edges+=1
            expanded,initial,owners=relay(b,y)
            expanded_edges,_,expanded_nh=space(expanded,initial)
            need(expanded_nh==nh,"relay nonhalting")
            for z,row in expanded_edges.items():
                projected=list(z[:2])
                for idx,owner in enumerate(owners):
                    projected[owner]+=z[2+idx]
                for _,v in row:
                    if v<2:need(v in moves(b,projected),"arbitrary relay projection")
            signed_cases+=1;relay_states+=len(expanded_edges)
    singleton=[]
    for ell in range(4):
        for chips in range(5):
            _,_,nh=space(((ell,),),(chips,))
            need(nh==(chips>=ell),"singleton including degree zero")
            singleton.append([ell,chips,nh])
    faults=[]
    need(certificate(1,1,(0,0),(0,0),(0,0),proper=False),"properness fault absent")
    faults.append("omitting certificate properness accepts a reachable identical pair")
    need(certificate(1,1,(0,0),(1,1),(0,0)),"reducedness fault absent")
    faults.append("using an unreduced full count falsely rejects the empty word")
    g=reduced_two(1,1,(1,0),(0,1))
    need(certificate(1,1,(1,0),g,(0,0),strict=False),"strictness fault absent")
    faults.append("replacing strict obstruction by <= rejects a legal firing")
    # Search an explicitly bounded small grid for scaling and gate false positives.
    for label,params in (("scale=1",{"scale":1}),("gate one chip early",{"early":1})):
        example=None
        for a,b in product(range(1,3),repeat=2):
            for x in product(range(3),repeat=2):
                matrix=((0,a),(b,0));_,_,nh=space(matrix,x)
                if nh:continue
                h,X,Y,_,_,_=construct(matrix,x,**params)
                states,_,_=space(h,X)
                if Y in states:
                    example={"fault":label,"a":a,"b":b,"x":x,"states":len(states)};break
            if example:break
        need(example is not None,"invalid reduction escaped falsification")
        faults.append(example)
    _,_,old=space(((1,1),(1,0)),(1,0))
    _,_,new=space(((0,1),(1,0)),(1,0))
    need(not old and new,"naive loop deletion control")
    faults.append("deleting loops changes a halting source into a nonhalting one")
    binary=[]
    for bits in (1,16,128,1024):
        matrix=((0,2**bits+1),(2**(bits+1)+1,0));x=(2**bits+3,0)
        h,X,Y,N,M,B=construct(matrix,x)
        need(min(X+Y)>=0 and sum(X)==sum(Y) and strong(h),"binary output")
        bound=20*(bits+2)
        maximum=max(v.bit_length() for row in h for v in row)
        maximum=max(maximum,*(v.bit_length() for v in X+Y))
        need(maximum<=bound,"binary linear bit bound in test family")
        binary.append({"input_bits_parameter":bits,"maximum_output_bits":maximum,"bound":bound})
    return {"status":"PASS","coverage":coverage,"unrestricted_target_cases":unrestricted,
            "alternative_target_words":alternative,"certificate_pairs":pairs,"partial_certificate_vectors":partial,
            "nonimage_pairs":nonimage,"negative_certificates":found,"signed_cases":signed_cases,
            "signed_transition_checks":signed_edges,"relay_states":relay_states,"singletons":singleton,
            "faults_detected":faults,"large_binary_controls":binary,
            "finite_controls_only":True,"historical_omitted_code_replayed":False}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inject-failure", action="store_true")
    args=parser.parse_args()
    need(not args.inject_failure,"deliberate unconditional failure control")
    print(json.dumps(run(),sort_keys=True,indent=2))

if __name__=="__main__":
    main()
