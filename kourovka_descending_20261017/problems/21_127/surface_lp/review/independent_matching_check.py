#!/usr/bin/env python3
"""Independent finite audit of the fixed-P4-graph relative matching formula."""
from collections import deque
from itertools import combinations
from pathlib import Path
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
LABELS = {'L':'ab','M':'bc','R':'cd'}


def partition(vertices, edges):
    p = {v:v for v in vertices}
    def root(v):
        while p[v] != v:
            p[v] = p[p[v]]
            v = p[v]
        return v
    for u,v in edges:
        p[root(u)] = root(v)
    groups = {}
    for v in vertices:
        groups.setdefault(root(v),set()).add(v)
    return [(c, sum(u in c for u,v in edges)) for c in groups.values()]


def components_by_coordinate(types, edges, q):
    out = {}
    for x in 'abcd':
        vs = [i for i,t in enumerate(types) if x in LABELS[t]]
        es = [(u,v) for u,v,y in edges if y == x]
        out[x] = [(c, count, sum(q[v].get(x,0) for v in c)) for c,count in partition(vs,es)]
    return out


def minimum_hit(constraints, D):
    masks = [sum(1<<v for v in c) for c in constraints]
    for k in range(len(D)+1):
        for choice in combinations(sorted(D),k):
            mask = sum(1<<v for v in choice)
            if all(mask & constraint for constraint in masks):
                return k
    raise AssertionError('taking all target vertices must hit all constraints')


def maximum_matching(U, V, links):
    # Independent unit-capacity max-flow, rather than the author's Kuhn recursion.
    source, sink = 0, 1+len(U)+len(V)
    cap = [[0]*(sink+1) for _ in range(sink+1)]
    for i in range(len(U)):
        cap[source][1+i] = 1
    for j in range(len(V)):
        cap[1+len(U)+j][sink] = 1
    for i,j in links:
        cap[1+i][1+len(U)+j] = 1
    value = 0
    while True:
        parents = {source:None}
        todo = deque([source])
        while todo and sink not in parents:
            v = todo.popleft()
            for w,c in enumerate(cap[v]):
                if c and w not in parents:
                    parents[w] = v
                    todo.append(w)
        if sink not in parents:
            return value
        w = sink
        while parents[w] is not None:
            v = parents[w]
            cap[v][w] -= 1
            cap[w][v] += 1
            w = v
        value += 1


def stable_formula(types, edges, q, D):
    forced = {v for v in D if (types[v]=='L' and q[v].get('a',0)!=0)
              or (types[v]=='R' and q[v].get('d',0)!=0)}
    parts = components_by_coordinate(types,edges,q)
    def bad(x):
        return [c for c,e,total in parts[x] if e==len(c)-1 and total!=0 and c <= D-forced]
    U,V = bad('b'),bad('c')
    links = [(i,j) for i,u in enumerate(U) for j,v in enumerate(V) if u&v]
    nu = maximum_matching(U,V,links)
    return len(forced)+len(U)+len(V)-nu


def literal_loss(types,edges,q,D,trees_only):
    # Directly minimize exceptions against all original coordinate constraints,
    # including a/d singleton constraints. This does not first remove forced nodes.
    constraints = [c for parts in components_by_coordinate(types,edges,q).values()
                   for c,e,total in parts
                   if c <= D and total!=0 and (not trees_only or e==len(c)-1)]
    return minimum_hit(constraints,D)


def main():
    snapshot = HERE/'matching_reproduction'
    snapshot.mkdir(exist_ok=True)
    for name in ('check_p4_optimization.py','check_flow.py'):
        shutil.copyfile(BASE/name,snapshot/name)
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run([sys.executable,str(snapshot/'check_p4_optimization.py')],
                            env=env,check=True,capture_output=True,text=True)
    original = json.loads((BASE/'P4_OPTIMIZATION_CHECKS.json').read_text())
    repeated = json.loads((snapshot/'P4_OPTIMIZATION_CHECKS.json').read_text())
    assert original == repeated

    rng = random.Random(8121127)
    counts = {'forest_exact_minima':0,'general_tree_hitting_minima':0,'cover_scaling':0}
    for case in range(2000):
        n = rng.randrange(1,9)
        types = [rng.choice('LMR') for _ in range(n)]
        allowed = [(u,v,'b' if 'L' in (types[u],types[v]) else 'c')
                   for u in range(n) for v in range(u+1,n)
                   if {types[u],types[v]} in ({'L','M'},{'M','R'})]
        edges = []
        for edge in rng.sample(allowed,len(allowed)):
            u,v,x = edge
            if case < 1000:
                # Keep the entire graph a forest, so finite and stable losses agree.
                parts = partition(range(n),[(a,b) for a,b,y in edges])
                if any(u in c and v in c for c,e in parts):
                    continue
            if rng.randrange(2):
                edges.append(edge)
                if case >= 1000 and rng.randrange(3)==0:
                    edges.append(edge)  # explicit parallel edges
        q = [{x:rng.randrange(-2,3) for x in LABELS[t]} for t in types]
        D = {v for v in range(n) if rng.randrange(4)}
        alpha = stable_formula(types,edges,q,D)
        assert alpha == literal_loss(types,edges,q,D,True)
        counts['general_tree_hitting_minima'] += 1
        if case < 1000:
            assert alpha == literal_loss(types,edges,q,D,False)
            counts['forest_exact_minima'] += 1
        if case % 5 == 0:
            m = rng.randrange(1,6)
            ee = []
            for u,v,x in edges:
                perm = rng.sample(range(m),m)
                ee.extend((m*u+s,m*v+perm[s],x) for s in range(m))
            tt = [t for t in types for _ in range(m)]
            qq = [dict(a) for a in q for _ in range(m)]
            DD = {m*v+s for v in D for s in range(m)}
            assert stable_formula(tt,ee,qq,DD) == m*alpha
            counts['cover_scaling'] += 1

    # A single isolated middle vertex has no genuinely private singleton choices.
    # One physical exception nevertheless hits both bad singleton components.
    assert stable_formula(['M'],[],[{'b':1,'c':1}],{0}) == 1
    assert literal_loss(['M'],[],[{'b':1,'c':1}],{0},True) == 1

    nonattainment = []
    for m in range(1,41):
        types = ['L']*m+['M']*m
        edges = [(s,m+s,'b') for s in range(m)]+[(s,m+(s+1)%m,'b') for s in range(m)]
        q = [{'a':0,'b':1} for _ in range(m)]+[{'b':0,'c':0} for _ in range(m)]
        D = set(range(2*m))
        assert stable_formula(types,edges,q,D) == 0
        assert literal_loss(types,edges,q,D,False) == 1
        nonattainment.append({'cover_degree':m,'stable_loss':0,'finite_minimum_exceptions':1})

    out = {'scope':'fixed graph relative exception density only',
           'author_json_reproduced_identically':True,'author_stdout':result.stdout.strip(),
           'independent_checks':counts,'private_singleton_absence_case_passed':True,
           'cyclic_nonattainment':nonattainment,'all_checks_passed':True}
    (HERE/'independent_matching_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
