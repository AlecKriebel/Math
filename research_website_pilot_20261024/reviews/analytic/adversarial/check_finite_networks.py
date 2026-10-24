"""Independent exact finite-network checks from main.tex only.

No deposited verifier or prior review is imported/read. Vertices are binary
words below a chosen highest ancestor. Original edges join prefixes at word
distance one or two. A generic rational Schur complement reduces networks.
"""
from fractions import Fraction as F
from itertools import product
import json


def descendants(root, depth):
    return {root + ''.join(t) for d in range(depth + 1)
            for t in product('01', repeat=d)}


def graph(vertices, omit=frozenset()):
    adj = {v: {} for v in vertices}
    for v in vertices:
        for step in (1, 2):
            if len(v) < step:
                continue
            w = v[:-step]
            if w in vertices and frozenset((v, w)) not in omit:
                adj[v][w] = adj[w][v] = F(1)
    return adj


def reduce_network(adj, keep):
    adj = {v: dict(nbrs) for v, nbrs in adj.items()}
    while len(adj) > len(keep):
        # Generic minimum-degree pivot; does not use any branch recurrence.
        v = min((v for v in adj if v not in keep),
                key=lambda v: (len(adj[v]), v))
        nbrs = list(adj[v].items())
        total = sum(c for _, c in nbrs)
        assert total > 0
        for i, (x, cx) in enumerate(nbrs):
            for y, cy in nbrs[i + 1:]:
                c = adj[x].get(y, F(0)) + cx * cy / total
                adj[x][y] = adj[y][x] = c
        for x, _ in nbrs:
            del adj[x][v]
        del adj[v]
    return adj


def triangle(adj, spine):
    t = reduce_network(adj, set(spine[:3]))
    x, y, z = spine[:3]
    return [t[x][y], t[y][z], t[x][z]]


def L(m, n):
    spine = ['0' * (n-j) for j in range(n + 1)]
    vertices = set(spine)
    vertices |= descendants(spine[0] + '0', m)
    vertices |= descendants(spine[0] + '1', m)
    for j in range(1, n):
        vertices |= descendants(spine[j] + '1', m)
    return graph(vertices), spine


def predicted_L(m, n):
    k = F(1, 2)
    for _ in range(m):
        k = (1 + 2*k) / (2 + 2*k)
    a, c = 1 + 2*k, 1 + k
    b = c
    for _ in range(n - 2):
        b = c + b / (1 + b)
    return [a, b, F(1)]


def predicted_induced(n):
    cs = [F(1)]
    for _ in range(2*n):
        cs.append(1 + 2*cs[-1] / (1 + cs[-1]))
    aa = {j: 1 + cs[j-1] / (1 + cs[j-1]) for j in range(1, 2*n)}
    u = aa[2*n-1]
    for j in range(n-2, 0, -1):
        u = aa[n+j] + u / (1+u)
    return [cs[n], u, F(1)]


def main():
    results = {'branches': [], 'first_exhaustion': [], 'induced_exhaustion': []}
    k = F(1, 2)
    for m in range(6):
        vertices = {'', '0'} | descendants('00', m)
        g = graph(vertices, {frozenset(('', '0'))})
        reduced = reduce_network(g, {'', '0'})
        assert reduced['']['0'] == k
        results['branches'].append({'m': m, 'conductance': str(k)})
        k = (1 + 2*k) / (2 + 2*k)
    for m in range(5):
        for n in range(2, 7):
            g, spine = L(m, n)
            actual = triangle(g, spine)
            assert actual == predicted_L(m, n), (m, n, actual)
            results['first_exhaustion'].append(
                {'m': m, 'n': n, 'vertices': len(g), 'triangle': list(map(str, actual))})
    for n in range(2, 6):
        g = graph(descendants('', 2*n))
        spine = ['0' * (n-j) for j in range(n+1)]
        actual = triangle(g, spine)
        assert actual == predicted_induced(n), (n, actual)
        a,b,c = actual
        rt = 1/(a+b*c/(b+c))
        rg = 1/(c+a*b/(a+b))
        results['induced_exhaustion'].append(
            {'n': n, 'vertices': len(g), 'triangle': list(map(str, actual)),
             'tree_resistance': str(rt), 'grandparent_resistance': str(rg)})
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
