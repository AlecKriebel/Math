"""Independent finite controls. Standard library only; no input audit code used."""
from itertools import combinations, product
import json
from pathlib import Path

def adjacency(n, es, mask):
    a = [0] * n
    for i, (x, y) in enumerate(es):
        if mask >> i & 1:
            a[x] |= 1 << y
            a[y] |= 1 << x
    return a

def colorable(a, deleted=None):
    vs = sorted((v for v in range(len(a)) if v != deleted), key=lambda v: -a[v].bit_count())
    classes = [0, 0, 0]

    def dfs(j):
        if j == len(vs):
            return True
        v = vs[j]
        for i in range(3):
            if not a[v] & classes[i]:
                was_empty = not classes[i]
                classes[i] |= 1 << v
                if dfs(j + 1):
                    return True
                classes[i] ^= 1 << v
                if was_empty:
                    break
        return False
    return dfs(0)

def property_p(a):
    n = len(a)
    if any((all((a[x] >> y & 1 for x, y in combinations(q, 2))) for q in combinations(range(n), 4))):
        return False
    return colorable(a) or any((colorable(a, v) for v in range(n)))

def hamming_transform(vals, m):
    vals = vals.copy()
    for bit in range(m):
        b = 1 << bit
        for s in range(len(vals)):
            vals[s] = min(vals[s], vals[s ^ b] + 1)
    return vals

def run():
    out = dict(graphs=0, positive_c3_distance_graphs=0, partial_colorings=0, feasible_W_color_steps=0, p_vertex_deletion_checks=0, p_edge_deletion_checks=0, isolated_extension_checks=0, exact_color_assignment_optima=0)
    partial_by_n = {}
    for n in range(1, 7):
        es = list(combinations(range(n), 2))
        m, lim = (len(es), 1 << len(es))
        aa = [adjacency(n, es, s) for s in range(lim)]
        c3 = [colorable(a) for a in aa]
        pp = [property_p(a) for a in aa]
        if not all((not c or p for c, p in zip(c3, pp))):
            raise AssertionError('verification failed at original line 68')
        d3 = hamming_transform([0 if c else m + 1 for c in c3], m)
        dp = hamming_transform([0 if p else m + 1 for p in pp], m)
        starts = out['partial_colorings']
        for s, a in enumerate(aa):
            out['graphs'] += 1
            if not d3[s] >= dp[s]:
                raise AssertionError('verification failed at original line 74')
            out['positive_c3_distance_graphs'] += bool(d3[s])
            if pp[s]:
                if not property_p(a + [0]):
                    raise AssertionError('verification failed at original line 77')
                out['isolated_extension_checks'] += 1
                for v in range(n):
                    vs = [w for w in range(n) if w != v]
                    b = [sum((1 << j for j, y in enumerate(vs) if a[x] >> y & 1)) for x in vs]
                    if not property_p(b):
                        raise AssertionError('verification failed at original line 84')
                    out['p_vertex_deletion_checks'] += 1
                for bit in range(m):
                    if s >> bit & 1:
                        if not pp[s ^ 1 << bit]:
                            raise AssertionError('verification failed at original line 88')
                        out['p_edge_deletion_checks'] += 1
            if n <= 5:
                exact = min((sum((s >> bit & 1 and cs[x] == cs[y] for bit, (x, y) in enumerate(es))) for cs in product(range(3), repeat=n)))
                if not exact == d3[s]:
                    raise AssertionError('verification failed at original line 94')
                out['exact_color_assignment_optima'] += 1
            if not d3[s] or (n > 5 and (not pp[s])):
                continue
            for cs in product(range(4), repeat=n):
                if any((s >> bit & 1 and cs[x] and (cs[x] == cs[y]) for bit, (x, y) in enumerate(es))):
                    continue
                out['partial_colorings'] += 1
                ls = [0] * n
                for v in range(n):
                    if not cs[v]:
                        ls[v] = 7
                        for w in range(n):
                            if a[v] >> w & 1 and cs[w]:
                                ls[v] &= ~(1 << cs[w] - 1)
                u = sum((not cs[v] and (not ls[v]) for v in range(n)))
                delta = {}
                for v in range(n):
                    if not cs[v] and ls[v]:
                        delta[v] = min((sum((not cs[w] and bool(ls[w]) and a[v] >> w & 1 and ls[w] >> col & 1 for w in range(n))) for col in range(3) if ls[v] >> col & 1))
                wset = [v for v, d in delta.items() if 2 * n * d >= d3[s]]
                if not d3[s] <= n * u + sum(delta.values()):
                    raise AssertionError('verification failed at original line 120')
                if not 2 * n * (u + len(wset)) >= d3[s]:
                    raise AssertionError('verification failed at original line 121')
                phi = sum((l.bit_count() for l in ls))
                for v in wset:
                    for col in range(3):
                        if ls[v] >> col & 1:
                            after = sum(((ls[w] & ~(1 << col) if a[v] >> w & 1 else ls[w]).bit_count() for w in range(n) if w != v and (not cs[w])))
                            if not phi - after >= delta[v]:
                                raise AssertionError('verification failed at original line 129')
                            if not 2 * n * (phi - after) >= d3[s]:
                                raise AssertionError('verification failed at original line 130')
                            out['feasible_W_color_steps'] += 1
        partial_by_n[n] = out['partial_colorings'] - starts

    def eval_graph(n, edges):
        es = sorted({tuple(sorted(e)) for e in edges})
        a = adjacency(n, es, (1 << len(es)) - 1)
        return {'C3': colorable(a), 'P': property_p(a)}
    wheel = [(0, i) for i in range(1, 6)] + [(i, 1 + i % 5) for i in range(1, 6)]
    shared = wheel + [(x + 5 if x else 0, y + 5 if y else 0) for x, y in wheel]
    disjoint = wheel + [(x + 6, y + 6) for x, y in wheel]
    labels = [v for v in range(6) for _ in range(2)]
    wheelset = {frozenset(e) for e in wheel}
    expansion = [(i, j) for i, j in combinations(range(12), 2) if frozenset((labels[i], labels[j])) in wheelset]
    mutations = {'one_wheel': eval_graph(6, wheel), 'two_shared_center_wheels': eval_graph(11, shared), 'two_disjoint_wheels': eval_graph(12, disjoint), 'doubled_wheel_occurrence_expansion': eval_graph(12, expansion)}
    if not mutations == {'one_wheel': {'C3': False, 'P': True}, 'two_shared_center_wheels': {'C3': False, 'P': True}, 'two_disjoint_wheels': {'C3': False, 'P': False}, 'doubled_wheel_occurrence_expansion': {'C3': False, 'P': False}}:
        raise AssertionError('verification failed at original line 148')
    out['partial_by_n'] = partial_by_n
    out['mutation_controls'] = mutations
    out['result'] = 'PASS'
    return out
if __name__ == '__main__':
    result = run()
    rendered = json.dumps(result, indent=2) + '\n'
    Path(__file__).with_name('controls_results.json').write_text(rendered)
    print(rendered)
