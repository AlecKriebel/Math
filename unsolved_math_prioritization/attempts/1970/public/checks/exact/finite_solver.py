#!/usr/bin/env python3
"""New reconstruction: exact finite smooth-prefix triple hitting, integer arithmetic only.
This is not a recovery of the bytes of any earlier unpublished certificate.
"""
from __future__ import annotations
from functools import lru_cache
import heapq

class VerificationError(RuntimeError):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def smooth_prefix(count):
    require(type(count) is int and count >= 1, 'positive integer prefix count required')
    heap, seen, result = [1], {1}, []
    while len(result) < count:
        x = heapq.heappop(heap)
        result.append(x)
        for y in (2*x, 3*x):
            if y not in seen:
                seen.add(y)
                heapq.heappush(heap, y)
    return result

def heights(X):
    require(type(X) is int and X >= 1, 'positive integer X required')
    result, power2 = [], 1
    while power2 <= X:
        h, value = 0, power2
        while value <= X:
            h += 1
            value *= 3
        result.append(h)
        power2 *= 2
    return result

def vertices(X):
    return sorted((2**a * 3**b, a, b) for a, h in enumerate(heights(X)) for b in range(h))

def triples(X):
    return [(n, 2*n, 3*n) for n, _, _ in vertices(X) if 3*n <= X]

def validate_hitting(X, selected, expected_size=None):
    require(type(selected) is list and all(type(n) is int and n >= 1 for n in selected), 'witness must contain positive integers')
    require(len(selected) == len(set(selected)), 'witness must be a distinct list')
    domain = {v for v, _, _ in vertices(X)}
    require(set(selected) <= domain, 'witness contains nonvertex')
    if expected_size is not None:
        require(len(selected) == expected_size, 'witness cardinality mismatch')
    hits = [sum(n in selected for n in edge) for edge in triples(X)]
    require(all(h >= 1 for h in hits), 'unhit complete triple')
    return sum(h-1 for h in hits)

def masks_to_selected(ms):
    return sorted(2**a * 3**b for a, m in enumerate(ms) for b in range(m.bit_length()) if m >> b & 1)

@lru_cache(None)
def _requirements(h):
    low = (1 << max(h-1, 0)) - 1
    return tuple(low & ~(m | (m >> 1)) for m in range(1 << h))

@lru_cache(None)
def _popcounts(h):
    return tuple(m.bit_count() for m in range(1 << h))

def solve(X, count_optima=False):
    """Column transfer with subset-min transform. Optional exact optimal count."""
    hs = heights(X)
    inf = sum(hs)+1
    dp = list(_popcounts(hs[0]))
    counts = [1] * len(dp) if count_optima else None
    histories = []
    for h, k in zip(hs, hs[1:] + [0]):
        size = 1 << k
        best, args = [inf]*size, [-1]*size
        ways = [0]*size if count_optima else None
        for m, r in enumerate(_requirements(h)):
            # h<=k+1 is guaranteed by adjacent exact column heights.
            require(r < size, 'required next-column bit is out of range')
            if dp[m] < best[r]:
                best[r], args[r] = dp[m], m
                if count_optima:
                    ways[r] = counts[m]
            elif dp[m] == best[r]:
                if count_optima:
                    ways[r] += counts[m]
        for bit in range(k):
            flag = 1 << bit
            for n in range(size):
                if n & flag:
                    other = n ^ flag
                    if best[other] < best[n]:
                        best[n], args[n] = best[other], args[other]
                        if count_optima:
                            ways[n] = ways[other]
                    elif best[other] == best[n]:
                        if count_optima:
                            ways[n] += ways[other]
        dp = [best[n] + pc for n, pc in enumerate(_popcounts(k))]
        counts = ways
        histories.append(args)
    chosen, n = [], 0
    for args in reversed(histories):
        n = args[n]
        require(n >= 0, 'missing transfer predecessor')
        chosen.append(n)
    chosen.reverse()
    selected = masks_to_selected(chosen)
    defect = validate_hitting(X, selected, dp[0])
    return {'tau': dp[0], 'selected': selected, 'defect': defect,
            'optimal_count': counts[0] if count_optima else None, 'heights': hs}

def solve_defect_cap(X, cap=1):
    """Independent constrained recurrence, no subset-min transform.
    Each complete triangle has nonnegative excess. Enumerate next masks whose
    cumulative excess is at most cap; cap is explicitly limited to 0 or 1.
    """
    require(type(cap) is int and cap in (0, 1), 'defect cap must be 0 or 1')
    hs = heights(X)
    dp = {(m, 0): (m.bit_count(), 1, (m,)) for m in range(1 << hs[0])}
    for h, k in zip(hs, hs[1:] + [0]):
        nd = {}
        for (m, old_d), (cost, count, path) in dp.items():
            required = 0
            already_extra = 0
            optional_extra = []
            for b in range(h-1):
                pair = ((m >> b) & 1) + ((m >> (b+1)) & 1)
                if pair == 0:
                    required |= 1 << b
                elif pair == 1:
                    optional_extra.append(1 << b)
                else:
                    already_extra += 1
            remaining = cap-old_d-already_extra
            if remaining < 0:
                continue
            low_options = [(required, 0)]
            if remaining:
                low_options += [(required | bit, 1) for bit in optional_extra]
                # pair==2 plus a selected next vertex has excess 2, hence excluded.
            high_options = (0, 1 << (h-1)) if k == h else (0,)
            for low, extra in low_options:
                for high in high_options:
                    n = low | high
                    require(n < 1 << k, 'defect recurrence next mask out of range')
                    d = old_d+already_extra+extra
                    key, newcost = (n, d), cost+n.bit_count()
                    prev = nd.get(key)
                    if prev is None or newcost < prev[0]:
                        nd[key] = (newcost, count, path+(n,))
                    elif newcost == prev[0]:
                        nd[key] = (newcost, prev[1]+count, prev[2])
        dp = nd
    finals = [(cost, d, count, path) for (m, d), (cost, count, path) in dp.items() if m == 0]
    require(finals, 'no bounded-defect solution')
    cost, d, _, path = min(finals)
    selected = masks_to_selected(path[:-1])
    require(validate_hitting(X, selected, cost) == d, 'defect witness mismatch')
    return {'minimum': cost, 'defect': d, 'selected': selected,
            'optimal_count': sum(count for c, _, count, _ in finals if c == cost)}

def colors(X):
    vs, es = vertices(X), triples(X)
    active = set(n for e in es for n in e)
    counts = [0, 0, 0]
    isolated = []
    for n, a, b in vs:
        if n in active:
            counts[(a+2*b) % 3] += 1
        else:
            isolated.append(n)
    return counts, isolated

def color_candidate(X):
    cs, isolated = colors(X)
    adjusted = cs[:]
    power, m = 1, 0
    patch = None
    while 24*power <= X:
        if X < 27*power:
            adjusted[(m+2) % 3] -= 1
            patch = m
        m += 1
        power *= 2
    return {'colors': cs, 'isolated': isolated, 'q0_candidate': min(cs),
            'q1_candidate': min(adjusted), 'adjusted_colors': adjusted, 'patch_m': patch}

def brute_force(X):
    """Direct all-subset enumeration, independent of column transfer."""
    vs = [n for n, _, _ in vertices(X)]
    require(len(vs) <= 20, 'brute force capped at 20 vertices')
    index = {n:i for i,n in enumerate(vs)}
    edges = [sum(1 << index[n] for n in edge) for edge in triples(X)]
    best, ways, witness = len(vs)+1, 0, None
    for mask in range(1 << len(vs)):
        size = mask.bit_count()
        if size > best:
            continue
        if all(mask & e for e in edges):
            if size < best:
                best, ways, witness = size, 1, mask
            else:
                ways += 1
    selected = [n for i,n in enumerate(vs) if witness >> i & 1]
    validate_hitting(X, selected, best)
    return {'tau': best, 'optimal_count': ways, 'selected': selected}

def branch_exact(X):
    """Independent edge-deletion recurrence for minimum hitting set cardinality."""
    vs = [n for n, _, _ in vertices(X)]
    index = {n:i for i,n in enumerate(vs)}
    edges = tuple(sorted(sum(1 << index[n] for n in edge) for edge in triples(X)))
    calls = 0
    @lru_cache(None)
    def visit(remaining):
        nonlocal calls
        calls += 1
        if not remaining:
            return 0
        # Every hit of this edge is exhaustively covered by one of three branches.
        e = remaining[0]
        choices = []
        while e:
            bit = e & -e
            e -= bit
            choices.append(1+visit(tuple(f for f in remaining if not f & bit)))
        return min(choices)
    return {'tau': visit(edges), 'states': calls}

def all_optima(X, limit=1000000):
    """Enumerate every optimum by exhaustive compatible-column backtracking."""
    hs = heights(X)
    dp = {m:m.bit_count() for m in range(1 << hs[0])}
    histories = []
    for h, k in zip(hs, hs[1:] + [0]):
        nd, preds = {}, {}
        for n in range(1 << k):
            best, previous = sum(hs)+1, []
            for m, cost in dp.items():
                if _requirements(h)[m] & n != _requirements(h)[m]:
                    continue
                c = cost+n.bit_count()
                if c < best:
                    best, previous = c, [m]
                elif c == best:
                    previous.append(m)
            nd[n], preds[n] = best, previous
        dp = nd
        histories.append(preds)
    solutions = []
    def visit(level, n, path):
        if level < 0:
            selected = masks_to_selected(list(reversed(path)))
            validate_hitting(X, selected, dp[0])
            solutions.append(selected)
            require(len(solutions) <= limit, 'all-optima enumeration limit exceeded')
            return
        for previous in histories[level][n]:
            visit(level-1, previous, path+[previous])
    visit(len(histories)-1, 0, [])
    return {'tau': dp[0], 'optimal_count': len(solutions), 'solutions': solutions}
