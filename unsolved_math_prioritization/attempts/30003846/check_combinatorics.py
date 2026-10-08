# Hardened derivative: explicit guards survive -O/-OO; stdout only.
"""Finite checks of Golan (2026), Section 3 and elementary Section 5 claims.
These are falsification tests, not an all-n proof or a diagram-group oracle.
Only Python standard library; deterministic enumeration of perfect matchings.
"""
import json, time, hashlib, pathlib

def diagrams(n):

    def rec(free, pairs):
        if not free:
            ordered = sorted(pairs, key=lambda p: p[1])
            out = [None] * (2 * n)
            for j, (l, r) in enumerate(ordered):
                out[l] = (j, 0)
                out[r] = (j, 1)
            yield tuple(out)
            return
        l = free[0]
        for p in range(1, len(free)):
            yield from rec(free[1:p] + free[p + 1:], pairs + [(l, free[p])])
    yield from rec(tuple(range(2 * n)), [])

def pos(d):
    ids = sorted({a for a, b in d})
    return {a: (d.index((a, 0)), d.index((a, 1))) for a in ids}

def edges(d):
    p = pos(d)
    ids = list(p)
    return {tuple(sorted((a, b))) for ia, a in enumerate(ids) for b in ids[ia + 1:] if p[a][0] < p[b][0] < p[a][1] < p[b][1] or p[b][0] < p[a][0] < p[b][1] < p[a][1]}

def components(d):
    left = set(pos(d))
    es = edges(d)
    res = []
    while left:
        reach = {min(left)}
        while True:
            new = reach | {b for a, b in es if a in reach} | {a for a, b in es if b in reach}
            if new == reach:
                break
            reach = new
        res.append(reach)
        left -= reach
    return res

def connected(d):
    return len(components(d)) == 1

def perform(d, b, cut):
    l, r = pos(d)[b]
    gap = d[l + 1:r]
    x, y = (gap[:cut], gap[cut:])
    if not not {a for a, _ in x} & {a for a, _ in y}:
        raise AssertionError()
    result = d[:l + 1] + y + x + d[r:]
    if not all((l < r for l, r in pos(result).values())):
        raise AssertionError()
    return result

def peel(d):
    """Apply the paper's merge, recursive peel, and free-lifting procedure."""
    if len(d) <= 4:
        return (d, [])
    last = d[-1][0]
    small = tuple((f for f in d if f[0] != last))
    cs = components(small)
    moves = []
    if len(cs) > 1:
        p = pos(d)
        cross = [a for a in p if p[a][0] < p[last][0] < p[a][1]]
        inner = min(cs, key=lambda s: max((p[a][1] for a in s)) - min((p[a][0] for a in s)))
        gap = d[p[last][0] + 1:p[last][1]]
        x = tuple((f for f in gap if f[0] in inner))
        if not (x and gap[:len(x)] == x):
            raise AssertionError()
        old_edges = edges(d)
        d = perform(d, last, len(x))
        moves.append((last, len(x)))
        if not old_edges <= edges(d):
            raise AssertionError()
        small = tuple((f for f in d if f[0] != last))
        if not (connected(small) and connected(d)):
            raise AssertionError()
    target, smoves = peel(small)
    for b, cut in smoves:
        l, r = pos(d)[b]
        gap = d[l + 1:r]
        count = 0
        fullcut = 0
        while fullcut < len(gap) and count < cut:
            if gap[fullcut][0] != last:
                count += 1
            fullcut += 1
        d = perform(d, b, fullcut)
        moves.append((b, fullcut))
    if not tuple((f for f in d if f[0] != last)) == target:
        raise AssertionError()
    if not (d[-1][0] == last and connected(d)):
        raise AssertionError()
    return (d, moves)

def is_peelable(d):
    ids = [a for a, s in d if s == 1]
    return all((connected(tuple((f for f in d if f[0] in ids[:k]))) for k in range(2, len(ids) + 1)))

def vertex_checks(d, dummies):
    """Each gap receives dummies indexed separately, including multiple edges."""
    seq = []
    for i, f in enumerate(d):
        seq.append(f)
        if i < len(d) - 1:
            seq.extend((('dummy', i, j) for j in range(dummies[i])))
    n = len(d) // 2
    N = len(seq)
    p = list(range(N + 1))

    def root(x):
        while p[x] != x:
            x = p[x]
        return x

    def join(a, b):
        p[root(b)] = root(a)
    positions = {f: i for i, f in enumerate(seq)}
    for b in range(n):
        join(positions[b, 0] + 1, positions[b, 1])
    verts = {root(i) for i in range(N + 1)}
    if not len(verts) == n + sum(dummies) + 1:
        raise AssertionError()
    inner = verts - {root(0), root(N)}
    if not len(inner) == n + sum(dummies) - 1:
        raise AssertionError()
    es = [(root(i), root(i + 1)) for i in range(N)]
    if not all((b != root(0) and a != root(N) for a, b in es)):
        raise AssertionError()
    for start in inner:
        reach = {start}
        while True:
            new = reach | {b for a, b in es if a in reach and b in inner}
            if reach == new:
                break
            reach = new
        if not reach == inner:
            raise AssertionError()

def main():
    begin = time.time()
    rows = []
    for n in range(2, 8):
        total = irreducible = already = max_swaps = vertex_cases = 0
        for d in diagrams(n):
            total += 1
            if not connected(d):
                continue
            irreducible += 1
            already += is_peelable(d)
            target, moves = peel(d)
            if not is_peelable(target):
                raise AssertionError()
            max_swaps = max(max_swaps, len(moves))
            if n <= 6:
                for amounts in ([0] * (2 * n - 1), [1] * (2 * n - 1), [i % 3 for i in range(2 * n - 1)]):
                    vertex_checks(d, amounts)
                    vertex_cases += 1
        rows.append(dict(n=n, all_unlabelled_matchings=total, irreducible=irreducible, already_peelable=already, max_swaps=max_swaps, vertex_partition_cases=vertex_cases))
    result = dict(status='PASS', rows=rows, elapsed_seconds=round(time.time() - begin, 3), limitations='Finite matching enumeration and vertex incidence only; no continuous dynamics, diagram-group isomorphism, or all-n theorem is certified by this computation.')
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
