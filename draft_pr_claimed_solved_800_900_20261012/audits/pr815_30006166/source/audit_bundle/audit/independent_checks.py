"""Independent bounded diagnostics; no assertion is evidence for the infinite theorem."""
from collections import Counter, deque
from itertools import product
from math import factorial


def need(value, label):
    if not value:
        raise RuntimeError(label)


def distances(vertices, adjacency):
    out = {}
    for x in vertices:
        seen = {x: 0}
        todo = deque([x])
        while todo:
            y = todo.popleft()
            for z in adjacency[y]:
                if z not in seen:
                    seen[z] = seen[y] + 1
                    todo.append(z)
        out[x] = seen
    return out


def color_components(vertices, distance, radius, color):
    unseen = set(vertices)
    answer = {}
    while unseen:
        x = min(unseen)
        reached = {x}
        todo = [x]
        unseen.remove(x)
        while todo:
            y = todo.pop()
            add = {z for z in unseen if color[z] == color[y] and distance[y].get(z, float('inf')) <= radius}
            unseen.difference_update(add)
            reached.update(add)
            todo.extend(add)
        for y in reached:
            answer[y] = reached
    return answer


def compute():
    counts = Counter()
    model_rows = []
    # Cursor-fixed lamps are intentionally a different representation from the author code.
    # The subgroup action can have trivial lamps, repeated lamp generators, or other stabilizers.
    for length, period, q in [(2, 1, 1), (3, 1, 2), (4, 2, 2), (6, 2, 3), (6, 3, 2)]:
        states = [(v, b) for v in product(range(q), repeat=period) for b in range(length)]
        def t(x, k=1):
            return (x[0], (x[1] + k) % length)
        def lamp(x, conjugate=0, sign=1):
            f = list(x[0])
            f[(x[1] - conjugate) % period] = (f[(x[1] - conjugate) % period] + sign) % q
            return (tuple(f), x[1])
        widths = [m for m in range(1, length + 1) if length % m == 0]
        graphs = {}
        for m in widths:
            def normal(x):
                r = x[1] % m
                return t(x, -r), r
            base = [x for x in states if x[1] % m == 0]
            graph = {}
            for x in states:
                r = x[1] % m
                adj = {lamp(x), lamp(x, sign=-1)}
                if r + 1 < m:
                    adj.add(t(x))
                if r > 0:
                    adj.add(t(x, -1))
                adj.discard(x)
                graph[x] = adj
                z, r = normal(x)
                need(t(z, r) == x, 'normalization inverse')
                need(normal(lamp(x)) == (lamp(z, -r), r), 'negative conjugation index')
                counts['coordinate_checks'] += 2
                for y in adj:
                    w, s = normal(y)
                    need(abs(s - r) <= 1, 'no hidden residue wrap')
                    counts['edge_level_checks'] += 1
            graphs[m] = graph
            gd = distances(states, graph)
            bg = {z: {lamp(z, -j, sign) for j in range(m) for sign in [-1, 1]} - {z} for z in base}
            bd = distances(base, bg)
            for x in states:
                z, r = normal(x)
                for y in states:
                    w, s = normal(y)
                    small = bd[z].get(w, float('inf'))
                    big = gd[x].get(y, float('inf'))
                    need((small == float('inf')) == (big == float('inf')), 'same orbit components')
                    if small < float('inf'):
                        need(small <= big <= (2*m-1)*small + m-1, 'two-sided coarse slab bound')
                        counts['coarse_distance_checks'] += 1
            # Test threshold chains, including jumps whose connecting paths leave the color.
            samples = [{z: 0 for z in base}]
            samples += [{z: (sum((j+1)*v for j,v in enumerate(z[0])) + z[1] + seed) % k for z in base}
                        for k in [2, 3] for seed in range(2)]
            for coloring in samples:
                lifted = {x: coloring[normal(x)[0]] for x in states}
                for radius in [1, 2, 3]:
                    bcomp = color_components(base, bd, radius, coloring)
                    xcomp = color_components(states, gd, radius, lifted)
                    for x in states:
                        z = normal(x)[0]
                        c = xcomp[x]
                        need({normal(y)[0] for y in c} <= bcomp[z], 'threshold-color projection')
                        need(len(c) <= m * len(bcomp[z]), 'fiber multiplicity bound')
                        if c:
                            diam = max(gd[y][w] for y in c for w in c)
                            need(diam <= radius * (m*len(bcomp[z])-1), 'threshold diameter bound')
                        counts['colored_chain_checks'] += 1
            model_rows.append({'cyclic_height': length, 'lamp_period': period, 'lamp_modulus': q,
                               'slab_width': m, 'points': len(states), 'base_points': len(base)})
        for m in widths:
            for n in widths:
                if n % m == 0:
                    for x in states:
                        need(graphs[m][x] <= graphs[n][x], 'divisor graph inclusion')
                        counts['divisor_checks'] += 1

    # Integer calculations distinguish the persistent -1 boundary from all other integer edges.
    for h in range(-100, 101):
        missing = [h % factorial(k) == factorial(k)-1 for k in range(1, 9)]
        need(all(not missing[j] or missing[j-1] for j in range(1,len(missing))), 'nested cut flags')
        need(all(missing) == (h == -1), 'persistent integer cut identity')
        counts['integer_boundary_checks'] += 2

    # Without a cutoff, even equality on one base point has arbitrarily large pullback classes.
    for extent in [1, 2, 4, 8, 16]:
        heights = list(range(-extent, extent+1))
        need(len(heights) == 2*extent+1, 'uncut pullback grows')
        counts['uncut_pullback_witnesses'] += 1
    need(((-1) % 120) == 119, 'negative boundary retained')
    return {'schema': 1, 'all_diagnostics_passed': True,
            'scope': 'bounded algebra, nonfree models, metric inequalities, and projection diagnostics only',
            'infinite_theorem_verified_by_program': False,
            'counts': dict(sorted(counts.items())), 'models': model_rows}


if __name__ == '__main__':
    import json
    print(json.dumps(compute(), indent=2, sort_keys=True))
