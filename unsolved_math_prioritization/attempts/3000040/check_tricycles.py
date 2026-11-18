import itertools, json, time

def graph(m):
    edges = []
    transitions = []
    n = 7
    base = [(1, 2), (1, 2), (3, 4), (3, 4), (5, 6), (5, 6)] + [(0, i) for i in range(1, 7)] + [(2, 3), (4, 5), (6, 1)]
    for j, (a, b) in enumerate(base):
        path = [a] + list(range(n, n + m - 1)) + [b]
        n += m - 1
        edges.extend(zip(path, path[1:]))
        if j >= 12:
            transitions.append(path)
    adj = [{} for _ in range(n)]
    for a, b in edges:
        adj[a][b] = adj[a].get(b, 0) + 1
        adj[b][a] = adj[b].get(a, 0) + 1
    return (adj, transitions)

def reaches(adj, D, q):
    D = list(D)
    steps = 0
    while D[q] == 0:
        burned = {q}
        todo = [q]
        incoming = [0] * len(adj)
        while todo:
            u = todo.pop()
            for v, k in adj[u].items():
                incoming[v] += k
                if v not in burned and incoming[v] > D[v]:
                    burned.add(v)
                    todo.append(v)
        if len(burned) == len(adj):
            return (False, steps)
        for v in range(len(adj)):
            if v not in burned:
                for w, k in adj[v].items():
                    if w in burned:
                        D[v] -= k
                        D[w] += k
        if not min(D) >= 0:
            raise AssertionError('verification failed')
        steps += 1
        if steps > 100000:
            raise RuntimeError('nontermination')
    return (True, steps)

def run(m):
    adj, paths = graph(m)
    count = 0
    good = []
    maxsteps = 0
    for pos in itertools.product(*paths):
        D = [0] * len(adj)
        D[0] = 2
        for p in pos:
            D[p] += 1
        count += 1
        ok = True
        for q in range(len(adj)):
            r, s = reaches(adj, D, q)
            maxsteps = max(maxsteps, s)
            if not r:
                ok = False
                break
        if ok:
            good.append([paths[i].index(pos[i]) for i in range(3)])
    return dict(m=m, vertices=len(adj), candidates=count, positive_rank_positions=good, max_burning_rounds=maxsteps)
if __name__ == '__main__':
    results = []
    for m in range(1, 10):
        r = run(m)
        results.append(r)
        print(json.dumps(r), flush=True)
    open(__import__('pathlib').Path(__file__).with_name('TRICYCLE_CHECKS.json'), 'w').write(json.dumps(results, indent=2) + '\n')
