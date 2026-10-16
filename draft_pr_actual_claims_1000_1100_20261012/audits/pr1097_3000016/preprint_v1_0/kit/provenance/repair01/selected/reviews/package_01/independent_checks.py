#!/usr/bin/env python3
"""Independent incidence-matrix/state-space controls; imports no candidate code."""
import sys
sys.dont_write_bytecode = True
import argparse
import itertools as it
import json
from collections import Counter, deque
from fractions import Fraction as F
from functools import reduce
from math import gcd


def must(q, text):
    if not q:
        raise ValueError(text)


def compositions(total, n):
    if n == 1:
        yield (total,)
    else:
        for a in range(total + 1):
            for tail in compositions(total-a, n-1):
                yield (a,) + tail


def incidence(a):
    n = len(a)
    return tuple(tuple(a[v][w] - (sum(a[v]) if w == v else 0)
                       for v in range(n)) for w in range(n))


def endpoint(a, x, count):
    L = incidence(a)
    return tuple(x[w]+sum(L[w][v]*count[v] for v in range(len(a))) for w in range(len(a)))


def active(a, z):
    return tuple(v for v in range(len(a)) if z[v] >= sum(a[v]))


def step(a, z, v):
    must(v in active(a, z), 'illegal word')
    e = tuple(int(w == v) for w in range(len(a)))
    return endpoint(a, z, e)


def strongly_connected(a):
    for s in range(len(a)):
        reached = {s}
        while True:
            enlarged = reached | {w for v in reached for w in range(len(a)) if a[v][w]}
            if enlarged == reached:
                break
            reached = enlarged
        if len(reached) != len(a):
            return False
    return True


def state_graph(a, x):
    edges, todo = {}, [tuple(x)]
    seen = set(todo)
    while todo:
        z = todo.pop()
        edges[z] = tuple(step(a, z, v) for v in active(a, z))
        for y in edges[z]:
            if y not in seen:
                seen.add(y)
                todo.append(y)
                must(len(seen) <= 400000, 'finite state graph exceeded declared cap')
    # DFS finishing colours, rather than a trajectory or greedy dichotomy assumption.
    colour = {}
    has_cycle = False
    for s in edges:
        if colour.get(s):
            continue
        stack = [(s, 0)]
        colour[s] = 1
        while stack:
            u, k = stack[-1]
            if k == len(edges[u]):
                colour[u] = 2
                stack.pop()
                continue
            v = edges[u][k]
            stack[-1] = (u, k+1)
            if colour.get(v) == 1:
                has_cycle = True
            elif not colour.get(v):
                colour[v] = 1
                stack.append((v, 0))
    stable = any(not row for row in edges.values())
    must(stable != has_cycle, 'dichotomy failed in fully explored finite graph')
    return edges, has_cycle


def determinant(m):
    m = [[F(v) for v in row] for row in m]
    d = F(1)
    for j in range(len(m)):
        k = next((k for k in range(j, len(m)) if m[k][j]), None)
        if k is None:
            return 0
        if j != k:
            m[j], m[k] = m[k], m[j]
            d *= -1
        p = m[j][j]
        d *= p
        for k in range(j+1, len(m)):
            q = m[k][j]/p
            for t in range(j+1, len(m)):
                m[k][t] -= q*m[j][t]
    must(d.denominator == 1, 'nonintegral determinant')
    return int(d)


def primitive(a):
    L = incidence(a)
    cof = [abs(determinant([[L[i][j] for j in range(len(a)) if j != w]
                            for i in range(len(a)) if i != w])) for w in range(len(a))]
    q = reduce(gcd, cof)
    p = tuple(v//q for v in cof)
    must(min(p) > 0 and endpoint(a, (0,)*len(a), p) == (0,)*len(a), 'period cofactors')
    return p


def solve(m, b):
    m = [[F(v) for v in row]+[F(y)] for row, y in zip(m, b)]
    for j in range(len(m)):
        k = next(k for k in range(j, len(m)) if m[k][j])
        m[j], m[k] = m[k], m[j]
        p = m[j][j]
        m[j] = [v/p for v in m[j]]
        for k in range(len(m)):
            if k != j:
                q = m[k][j]
                m[k] = [v-q*w for v,w in zip(m[k], m[j])]
    return tuple(row[-1] for row in m)


def reduced(a, x, y, p):
    if sum(x) != sum(y):
        return None
    L = incidence(a)
    # This small control enumerates p_0 residues; it is not the polynomial algorithm.
    for h0 in range(p[0]):
        rest = solve([list(row[1:]) for row in L[1:]],
                     [y[w]-x[w]-L[w][0]*h0 for w in range(1, len(a))])
        if any(v.denominator != 1 for v in rest):
            continue
        h = (h0,) + tuple(int(v) for v in rest)
        if endpoint(a, x, h) != y:
            continue
        q = min(h[v]//p[v] for v in range(len(a)))
        g = tuple(h[v]-q*p[v] for v in range(len(a)))
        must(min(g) >= 0 and any(g[v] < p[v] for v in range(len(a))), 'normalization')
        return g
    return None


def stuck(a, x, g, u, proper=True, strict=True):
    if any(q < 0 or q > r for q,r in zip(u,g)) or (proper and u == g):
        return False
    z = endpoint(a, x, u)
    return all(z[v] < sum(a[v]) if strict else z[v] <= sum(a[v])
               for v in range(len(a)) if u[v] < g[v])


def make(a, x, scale_fault=False, gate_early=False, marker_fault=False):
    n = len(a)
    N = (sum(x)+1)**n
    M = 1 if scale_fault else N+1
    B = N*(M*max(map(sum, a))+1)
    h = [[0]*(n+2) for _ in range(n+2)]
    for v in range(n):
        for w in range(n):
            h[v][w] = M*a[v][w]
        h[v][n] = 1
        h[n][v] = B
    h[n][n+1] = h[n+1][n] = 1
    h = tuple(map(tuple, h))
    X = tuple(M*v+N for v in x)+(n*B+1-N+int(gate_early), 0)
    f = (N,)*n+(1,0)
    Y = endpoint(h, X, f)
    if marker_fault:
        Y = X
    return h, X, Y, N, M, B


def all_prefixes(a, x, coverage):
    h, X, Y, N, M, B = make(a, x)
    n = len(a)
    must(strongly_connected(h) and all(h[v][v] == 0 for v in range(n+2)), 'graph validity')
    must(min(X+Y) >= 0 and sum(X) == sum(Y), 'configuration validity')
    incoming = [sum(row[v] for row in a) for v in range(n)]
    must(Y == tuple(M*x[v]+M*N*(incoming[v]-sum(a[v]))+B for v in range(n))+((n-1)*N,1), 'Y coordinates')
    counts = {(0,)*n}
    at_cutoff = []
    for t in range(N+1):
        nxt = set()
        for u in counts:
            z = endpoint(a, x, u)
            w = endpoint(h, X, u+(0,0))
            coverage['prefix_count_states'] += 1
            must(min(z) >= 0, 'source nonnegative prefix')
            must(w[:n] == tuple(M*z[v]+N-u[v] for v in range(n)), 'offset identity')
            must(w[n:] == (n*B+1-N+t,0), 'first-gate/marker identity')
            must((n in active(h,w)) == (t >= N), 'first gate timing')
            if t == N:
                at_cutoff.append(u)
                continue
            must(active(a,z) == tuple(v for v in active(h,w) if v < n), 'exact prefix equivalence')
            for v in active(a,z):
                q = list(u); q[v] += 1
                nxt.add(tuple(q)); coverage['prefix_edges'] += 1
        counts = nxt
    _, nh = state_graph(a,x)
    must(bool(at_cutoff) == nh, 'cutoff versus full state graph')
    # Enumerate the entire remaining-count box once per instance; all suffix orders are edges.
    if at_cutoff:
        available = set(at_cutoff)
        pending = list(available)
        while pending:
            u = pending.pop()
            w = endpoint(h, X, u+(1,0))
            for v in range(n):
                if u[v] == N:
                    continue
                must(v in active(h,w), 'arbitrary cleanup order')
                q = list(u); q[v] += 1; q = tuple(q)
                coverage['cleanup_edges'] += 1
                if q not in available:
                    available.add(q); pending.append(q)
        must(endpoint(h,X,(N,)*n+(1,0)) == Y, 'cleanup target')
    coverage['constructions'] += 1
    coverage['nonhalting_sources'] += nh


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inject-failure', action='store_true')
    args = parser.parse_args()
    must(not args.inject_failure, 'deliberate failure is unconditional')
    cov = Counter()
    graphs = [((0,a),(b,0)) for a,b in it.product((1,2,4),repeat=2)]
    for bits in it.product((0,1), repeat=6):
        a = [[0]*3 for _ in range(3)]
        for (v,w), bit in zip(((i,j) for i in range(3) for j in range(3) if i != j),bits):
            a[v][w] = bit
        a = tuple(map(tuple,a))
        if strongly_connected(a):
            graphs.append(a)
    examples = []
    for a in graphs:
        n = len(a); p = primitive(a)
        for total in range(3):
            configs = list(compositions(total,n))
            for x in configs:
                edges, nh = state_graph(a,x)
                all_prefixes(a,x,cov)
                cov['full_state_graphs'] += 1
                cov['full_states'] += len(edges)
                for y in configs:
                    cov['reachability_pairs'] += 1
                    g = reduced(a,x,y,p)
                    if g is None:
                        cov['nonimage_pairs'] += 1
                        must(y not in edges, 'nonimage reachable')
                        continue
                    witnesses = []
                    for u in it.product(*(range(v+1) for v in g)):
                        cov['partial_vectors'] += 1
                        if stuck(a,x,g,u):
                            witnesses.append(u)
                    must(bool(witnesses) == (y not in edges), 'coNP certificate soundness/completeness')
                    cov['certificate_negative_pairs'] += bool(witnesses)
                    for u in witnesses:
                        if endpoint(a,x,u) not in edges:
                            cov['nonrealizable_certificate_vectors'] += 1
                            if len(examples) < 3:
                                examples.append({'a':a,'x':x,'y':y,'p':p,'g':g,'u':u,'state':endpoint(a,x,u)})
                # A bounded tree of real words directly checks period deletion, including retained suffixes.
                words = [(x,())]
                for length in range(7):
                    nxt = []
                    for z, word in words:
                        count = tuple(word.count(v) for v in range(n))
                        if all(count[v] >= p[v] for v in range(n)):
                            removed = [0]*n; kept=[]
                            for v in word:
                                if removed[v] < p[v]: removed[v] += 1
                                else: kept.append(v)
                            state=x
                            for v in kept: state=step(a,state,v)
                            must(state == z, 'period-deleted legal word endpoint')
                            cov['period_deletions'] += 1
                        for v in active(a,z): nxt.append((step(a,z,v),word+(v,)))
                    words=nxt
    # Signed loops and delayed relay projection, full-state rather than a selected schedule.
    for l0,l1,a,b in it.product(range(3),range(3),(1,2),(1,2)):
        old=((l0,a),(b,l1))
        for x in it.product(range(-1,2),repeat=2):
            k=tuple(max(0,-v) for v in x)
            norm=((l0+k[0],a),(b,l1+k[1])); init=tuple(x[v]+k[v] for v in range(2))
            edges,nh=state_graph(old,x)
            for z,row in edges.items():
                zz=tuple(z[v]+k[v] for v in range(2))
                must(active(old,z) == active(norm,zz), 'signed threshold conjugacy')
                for v in active(old,z):
                    must(step(norm,zz,v) == tuple(step(old,z,v)[w]+k[w] for w in range(2)), 'signed word conjugacy')
                    cov['signed_moves'] += 1
            owners=[v for v in range(2) if norm[v][v]]
            rel=[[0]*(2+len(owners)) for _ in range(2+len(owners))]
            rel[0][1]=a; rel[1][0]=b
            for j,v in enumerate(owners): rel[v][2+j]=rel[2+j][v]=norm[v][v]
            rel=tuple(map(tuple,rel)); re,rnh=state_graph(rel,init+(0,)*len(owners))
            must(nh == rnh, 'relay nonhalting equivalence')
            for z in re:
                proj=list(z[:2])
                for j,v in enumerate(owners): proj[v] += z[2+j]
                for v in active(rel,z):
                    if v < 2:
                        must(v in active(norm,proj), 'arbitrary delayed relay projection')
                        cov['delayed_old_moves'] += 1
            cov['signed_relay_instances'] += 1
    for ell,chips in it.product(range(5),range(6)):
        _,nh=state_graph(((ell,),),(chips,))
        must(nh == (chips >= ell), 'singleton zero-degree case')
        cov['singleton_cases'] += 1
    # Faults are independent failed inferences, not injected discrepancies to expected output.
    faults=[]
    a=((0,1),(1,0)); x=(0,0)
    must(stuck(a,x,(0,0),(0,0),proper=False), 'omitted properness fault')
    faults.append('certificate properness omitted: identical reachable pair is falsely rejected')
    must(stuck(a,x,(1,1),(0,0)), 'unreduced vector fault')
    faults.append('unreduced full period: identical reachable pair is falsely rejected')
    must(stuck(a,(1,0),(1,0),(0,0),strict=False), 'nonstrict fault')
    faults.append('weak threshold obstruction: legal one-move target falsely rejected')
    for fault in ('scale_fault','gate_early','marker_fault'):
        found=None
        for aa,bb in it.product((1,2),repeat=2):
            for x in it.product(range(2),repeat=2):
                a=((0,aa),(bb,0)); _,nh=state_graph(a,x)
                if nh: continue
                h,X,Y,*_=make(a,x,**{fault:True}); states,_=state_graph(h,X)
                if Y in states:
                    found={'fault':fault,'a':a,'x':x,'target':Y,'reachable_states':len(states)};break
            if found: break
        must(found is not None, 'broken reduction escaped controls')
        faults.append(found)
    _,before=state_graph(((2,1),(1,0)),(2,0))
    _,after=state_graph(((0,1),(1,0)),(2,0))
    must(not before and after, 'naive loop deletion fault')
    faults.append('deleting loops without a relay changes HALTING to NONHALTING')
    large=[]
    for bits,n in ((37,2),(131,3),(509,4)):
        a=[[0]*n for _ in range(n)]
        for v in range(n): a[v][(v+1)%n]=2**bits+v+1
        a=tuple(map(tuple,a));x=(2**(bits+1)+1,)+(0,)*(n-1)
        h,X,Y,N,M,B=make(a,x)
        must(strongly_connected(h) and min(X+Y)>=0 and sum(X)==sum(Y), 'large binary validity')
        maximum=max(v.bit_length() for row in h for v in row)
        maximum=max(maximum,*(v.bit_length() for v in X+Y))
        bound=10*(n+1)*(bits+2)
        must(maximum <= bound, 'large bit-size family bound')
        large.append({'n':n,'bits':bits,'maximum_output_bits':maximum,'conservative_bound':bound})
    print(json.dumps({'status':'PASS','coverage':dict(sorted(cov.items())),
                      'nonrealizable_certificate_examples':examples,'faults_detected':faults,
                      'large_binary_cases':large,'finite_controls_only':True,
                      'imports_candidate_or_prior_checker':False},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
