#!/usr/bin/env python3
"""Independent exact checker. Standard library only; never reads candidate code."""
import collections
import hashlib
import itertools
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def incidence_beta(lower_count, blocks):
    vertices = [('a', i) for i in range(lower_count)] + [('b', j) for j in range(len(blocks))]
    edges = [(('a', i), ('b', j)) for j, block in enumerate(blocks) for i in block]
    return graph_beta(vertices, edges)


def graph_beta(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        require(u in adjacency and v in adjacency, 'missing graph vertex')
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen = set()
    components = 0
    for v in vertices:
        if v in seen:
            continue
        components += 1
        stack = [v]
        seen.add(v)
        while stack:
            for w in adjacency[stack.pop()]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
    return len(edges) - len(vertices) + components, components


def reflection(previous, r):
    # previous consists of lower-cover sets for each current-rank vertex.
    lower_count = 1 + max((v for block in previous for v in block), default=-1)
    upper = [frozenset(i for i, block in enumerate(previous) if z in block) for z in range(lower_count)]
    upper.extend(frozenset([x]) for x in range(len(previous)) for _ in range(r))
    require(all(upper), 'reflection produced empty lower cover set')
    return tuple(upper)


def extensions(previous, r):
    """Every extension: partition the required pair edges into cliques, then fill singletons.

    The least uncovered edge determines its unique block, so each block multiset
    appears once for the current labeling. This is not an isomorphism enumeration.
    """
    m = len(previous)
    limits = [len(s) + r for s in previous]
    required = frozenset((i, j) for i in range(m) for j in range(i+1, m) if previous[i] & previous[j])
    require(all(len(previous[i] & previous[j]) <= 1 for i in range(m) for j in range(i+1, m)), 'nonlinear input')

    def visit(edges, used, blocks):
        if not edges:
            yield tuple(blocks + [frozenset([i]) for i in range(m) for _ in range(limits[i]-used[i])])
            return
        a, b = min(edges)
        candidates = [i for i in range(m) if i not in (a, b) and (min(a,i), max(a,i)) in edges and (min(b,i), max(b,i)) in edges]
        for bits in range(1 << len(candidates)):
            block = frozenset([a, b] + [v for k, v in enumerate(candidates) if bits >> k & 1])
            if any(used[i] >= limits[i] for i in block):
                continue
            pairs = frozenset(itertools.combinations(sorted(block), 2))
            if not pairs <= edges:
                continue
            next_used = used[:]
            for i in block:
                next_used[i] += 1
            yield from visit(edges - pairs, next_used, blocks + [block])
    yield from visit(required, [0]*m, [])


def is_reflection(previous, upper, r):
    return collections.Counter(upper) == collections.Counter(reflection(previous, r))


def verify(prefix, r, choices_all=True):
    sizes = list(map(len, prefix))
    require(prefix[0] == (frozenset(),), 'bottom not unique')
    require(sizes[1] == r, 'bottom commutator failed')
    witness_trials = 0
    details = []
    betas = [None]
    for k in range(1, len(prefix)):
        require(all(prefix[k]), 'upper vertex without lower cover')
        require(all(0 <= v < sizes[k-1] for s in prefix[k] for v in s), 'invalid incidence')
        deg = [sum(i in s for s in prefix[k]) for i in range(sizes[k-1])]
        require(deg == [len(s)+r for s in prefix[k-1]], 'diagonal commutator')
        up_pairs = collections.Counter(pair for block in prefix[k] for pair in itertools.combinations(sorted(block),2))
        for i, j in itertools.combinations(range(sizes[k-1]), 2):
            down = len(prefix[k-1][i] & prefix[k-1][j])
            up = up_pairs[(i,j)]
            require(down == up and up <= 1, 'off-diagonal commutator')
        beta, components = incidence_beta(sizes[k-1], prefix[k])
        require(components == 1, 'disconnected valid slice')
        require(beta == r*sum(sizes[:k])-sizes[k-1]-sizes[k]+1, 'cycle identity')
        betas.append(beta)
        if k == 1:
            continue
        lower = prefix[k-1]
        upper = prefix[k]
        zcount, xcount = sizes[k-2], sizes[k-1]
        witnesses = {z: [x for x, block in enumerate(lower) if block == frozenset([z])] for z in range(zcount)}
        chosen_z = [z for z in range(zcount) if witnesses[z]]
        h_vertices = [('x', x) for x in range(xcount)] + [('z', z) for z in chosen_z]
        h_edges = [(('z', z), ('x', x)) for z in chosen_z for x, block in enumerate(lower) if z in block]
        q, h_components = graph_beta(h_vertices, h_edges)
        require(0 <= q <= betas[k-1], 'q range')
        require(betas[k] >= q, 'main theorem violated')
        byrnes = 1+r*sum(sizes[:k-1])+(r-1)*sizes[k-1]
        local = r*sizes[k-1]+sizes[k-2]
        require(byrnes-local == betas[k-1], 'Byrnes/local gap')
        require(sizes[k] == byrnes-betas[k], 'Byrnes exact gap')
        require(betas[k]-betas[k-1] == local-sizes[k], 'cycle increment')
        require(local <= byrnes-q <= byrnes, 'between bounds')
        choice_count = 1
        for z in chosen_z:
            choice_count *= len(witnesses[z])
        choices = itertools.product(*(witnesses[z] for z in chosen_z))
        if not choices_all or choice_count > 2000:
            choices = [tuple(witnesses[z][0] for z in chosen_z), tuple(witnesses[z][-1] for z in chosen_z)]
        for witness_choice in choices:
            used_top = set()
            k_edges = set()
            k_vertices = {('x', x) for x in range(xcount)}
            for z, a in zip(chosen_z, witness_choice):
                terminals = {x for x, block in enumerate(lower) if z in block}
                top = {t for t, block in enumerate(upper) if a in block and len(block) > 1}
                require(not (top & used_top), 'internal top shared by two replacements')
                used_top.update(top)
                t_vertices = [('x', x) for x in terminals] + [('t', t) for t in top]
                t_edges = [(('x', x), ('t', t)) for t in top for x in upper[t]]
                require(all(upper[t] <= terminals for t in top), 'tree leaves terminal set')
                require(graph_beta(t_vertices, t_edges) == (0,1), 'replacement is not tree')
                require(set().union(*(set(upper[t]) for t in top), {a}) == terminals, 'terminals not spanned')
                k_vertices.update(t_vertices)
                k_edges.update(t_edges)
            require(graph_beta(list(k_vertices), list(k_edges)) == (q, h_components), 'replacement does not preserve cycle rank and components')
            witness_trials += 1
        if all(witnesses[z] for z in range(zcount)):
            require(q == betas[k-1] and sizes[k] <= local, 'all-S consequence')
        if k >= 3 and all(len(witnesses[z]) >= 2 for z in range(zcount)):
            require((sizes[k] == local) == is_reflection(lower, upper, r), 'two witness equality classification')
        isolated_x = sum(not (set(block) & set(chosen_z)) for block in lower)
        details.append({'n':k,'sizes':sizes[:k+1],'b_previous':betas[k-1],'b_current':betas[k],'q':q,'S_size':len(chosen_z),'z_count':zcount,'isolated_X_in_H':isolated_x,'byrnes':byrnes,'refined':byrnes-q,'local':local})
    return witness_trials, details


def partitions(n, at_most=None):
    if n == 0:
        yield ()
    else:
        for first in range(min(n, at_most if at_most is not None else n), 0, -1):
            for rest in partitions(n-first, first):
                yield (first,)+rest


def young_prefix(n):
    shapes = [list(partitions(k)) for k in range(n+1)]
    out = [(frozenset(),)]
    for k in range(1, n+1):
        blocks = []
        for shape in shapes[k]:
            covers = set()
            for row in range(len(shape)):
                reduced = list(shape)
                reduced[row] -= 1
                reduced = tuple(x for x in reduced if x)
                if reduced in shapes[k-1]:
                    covers.add(shapes[k-1].index(reduced))
            blocks.append(frozenset(covers))
        out.append(tuple(blocks))
    return out


def main():
    output = {'implementation':'independent standard-library set/clique-partition checker','enumeration':{},'examples':{},'negative_controls':{},'witness_trials':0}
    require(graph_beta([('x',i) for i in range(4)],[]) == (0,4), 'empty-S isolated vertices')
    output['negative_controls']['empty_S_four_isolates_beta'] = 0
    for r, maxrank in [(1,7),(2,3),(3,3)]:
        prefixes = [[(frozenset(),), tuple(frozenset([0]) for _ in range(r))]]
        counts = [len(prefixes)]
        for rank in range(2, maxrank+1):
            fresh = []
            histogram = collections.Counter()
            for prefix in prefixes:
                for ext in extensions(prefix[-1], r):
                    p = prefix + [ext]
                    trials, details = verify(p, r)
                    output['witness_trials'] += trials
                    histogram[str(details[-1]['q'])] += 1
                    fresh.append(p)
            prefixes = fresh
            counts.append(len(prefixes))
        output['enumeration'][str(r)] = {'ranks':list(range(1,maxrank+1)), 'labeled_prefix_counts':counts,'top_rank_q_histogram':dict(histogram)}
    for r in range(1,6):
        p = [(frozenset(),), tuple(frozenset([0]) for _ in range(r))]
        for _ in range(4):
            p.append(reflection(p[-1],r))
        trials, detail = verify(p,r,False)
        output['witness_trials'] += trials
        output['examples']['reflection_r'+str(r)] = detail
    p = [(frozenset(),), (frozenset([0]),)*3]
    p.append(tuple(map(frozenset,[(0,1),(0,2),(1,2),(0,),(0,),(1,),(1,),(2,),(2,)])))
    p.append(reflection(p[-1],3))
    trials, detail = verify(p,3)
    output['witness_trials'] += trials
    require(detail[-1]['q'] == 1 and detail[-1]['refined'] == 30 and len(p[-1]) == 30, 'r3 sharp example')
    output['examples']['r3_sharp'] = detail
    require(len(p[-1]) > detail[-1]['byrnes']-2*detail[-1]['q'], 'r3 coefficient-two not falsified')
    output['negative_controls']['r3_coefficient_two_falsified'] = True
    try:
        verify(p[:-1]+[p[-1][:-1]],3)
    except ValueError as e:
        output['negative_controls']['removed_r3_top_vertex_rejected'] = str(e)
    else:
        raise ValueError('removed top vertex accepted')
    p = young_prefix(12)
    trials, detail = verify(p,1)
    output['witness_trials'] += trials
    output['examples']['young_through12'] = detail
    p = young_prefix(5)
    p.append(reflection(p[-1],1))
    p.append(reflection(p[-1],1))
    trials, detail = verify(p,1)
    output['witness_trials'] += trials
    require(detail[-1]['q'] == 1 and detail[-1]['refined'] == 19 and len(p[-1]) == 19, 'r1 sharp example')
    output['examples']['r1_sharp'] = detail
    require(len(p[-1]) > detail[-1]['byrnes']-2*detail[-1]['q'], 'r1 coefficient-two not falsified')
    output['negative_controls']['r1_coefficient_two_falsified'] = True
    # Explicit relaxed local obstruction. Validate two middle identities only;
    # deliberately fail the full-prefix requirement at bottom degree.
    relaxed = [(frozenset(),),(frozenset([0]),)*3,tuple(map(frozenset,[(0,1),(0,2),(1,2)])),tuple(map(frozenset,[(0,1,2),(0,),(0,),(1,),(1,),(2,),(2,)]))]
    for k in (2,3):
        for i in range(len(relaxed[k-1])):
            require(sum(i in s for s in relaxed[k])-len(relaxed[k-1][i]) == 1, 'relaxed middle diagonal')
        for i,j in itertools.combinations(range(len(relaxed[k-1])),2):
            require(sum(i in s and j in s for s in relaxed[k]) == len(relaxed[k-1][i]&relaxed[k-1][j]), 'relaxed middle off diagonal')
    try:
        verify(relaxed,1)
    except ValueError as e:
        output['negative_controls']['relaxed_prefix_rejected'] = str(e)
    else:
        raise ValueError('invalid bottom was accepted')
    require(incidence_beta(3, relaxed[2])[0] == 1 and incidence_beta(3, relaxed[3])[0] == 0, 'relaxed cycle collapse')
    output['negative_controls']['relaxed_middle_valid_b2_b3'] = [1,0]
    output['status'] = 'PASS'
    print(json.dumps(output,sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
