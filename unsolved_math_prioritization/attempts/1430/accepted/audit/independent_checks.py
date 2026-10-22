#!/usr/bin/env python3
"""Independent bounded audit. No network, writes, imported author code, or asserts."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import json
import math
import sys


class Rejected(Exception):
    pass


checks = 0


def need(condition, message):
    global checks
    checks += 1
    if not condition:
        raise Rejected(message)


def edges(word, n):
    """Works for nonuniform words too; every declared vertex must occur."""
    need(type(n) is int and n > 0, 'invalid order')
    need(type(word) in (list, tuple), 'invalid word container')
    need(all(type(v) is int and 0 <= v < n for v in word), 'invalid letter')
    need(set(word) == set(range(n)), 'missing vertex')
    result = set()
    for u, v in combinations(range(n), 2):
        last = None
        alternating = True
        for x in word:
            if x == u or x == v:
                if last == x:
                    alternating = False
                    break
                last = x
        if alternating:
            result.add((u, v))
    return result


def endpoint_edges(word, n):
    pos = [[i for i, x in enumerate(word) if x == v] for v in range(n)]
    need(all(len(p) == 2 for p in pos), 'not a double word')
    # Exactly one endpoint of b in the open chord interval of a.
    return {(a, b) for a, b in combinations(range(n), 2)
            if sum(pos[a][0] < q < pos[a][1] for q in pos[b]) == 1}


def pairing_words(n):
    """Enumerate perfect matchings of positions, unlike the author's letter DFS."""
    word = [-1] * (2 * n)

    def recurse(remaining, label):
        if not remaining:
            yield tuple(word)
            return
        first = remaining[0]
        for second in remaining[1:]:
            word[first] = word[second] = label
            yield from recurse(tuple(p for p in remaining if p not in (first, second)), label + 1)
            word[first] = word[second] = -1

    yield from recurse(tuple(range(2 * n)), 0)


def uniformize(word, n):
    out = list(word)
    target = max(Counter(out).values())
    while set(Counter(out).values()) != {target}:
        counts = Counter(out)
        prefix = []
        for x in out:
            if counts[x] < target and x not in prefix:
                prefix.append(x)
        out = prefix + out
    need(len(out) == n * target, 'uniformization target')
    return out


def initial(word):
    return {x: word.index(x) for x in set(word)}


def semitransitive(n, arcs):
    # Only numerically increasing arcs are supplied, hence acyclicity is exact.
    for size in range(3, n + 1):
        for path in combinations(range(n), size):
            if (path[0], path[-1]) in arcs and all(e in arcs for e in zip(path, path[1:])):
                if not all(e in arcs for e in combinations(path, 2)):
                    return False
    return True


def star_word(n, arcs, v):
    reach = set(arcs)
    for mid in range(n):
        for a in range(n):
            for b in range(n):
                if (a, mid) in reach and (mid, b) in reach:
                    reach.add((a, b))
    incoming = [u for u in range(n) if (u, v) in arcs]
    outgoing = [u for u in range(n) if (v, u) in arcs]
    before = [u for u in range(n) if (u, v) in reach and u not in incoming]
    after = [u for u in range(n) if (v, u) in reach and u not in outgoing]
    other = [u for u in range(n) if u != v and u not in incoming + outgoing + before + after]
    return before + incoming + other + before + [v] + outgoing + incoming + [v] + after + other + outgoing + after


def main(packet):
    data = json.loads((packet / 'SMALL_WITNESSES.json').read_bytes())
    witness_count = 0
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        need(set(data[str(n)]) == {str(i) for i in range(2 ** len(pairs))}, 'complete mask inventory')
        for mask in range(2 ** len(pairs)):
            w = data[str(n)][str(mask)]
            expected = {e for j, e in enumerate(pairs) if mask & (1 << j)}
            need(Counter(w) == Counter({v: 2 for v in range(n)}), 'witness multiplicity')
            need(edges(w, n) == endpoint_edges(w, n) == expected, 'witness semantics')
            witness_count += 1
    need(witness_count == 1099, 'witness total')

    pairing_counts = {}
    cubic_hist = Counter()
    rotation_count = 0
    for n in range(1, 7):
        seen = set()
        for w in pairing_words(n):
            need(w not in seen, 'duplicate pairing word')
            seen.add(w)
            e = edges(w, n)
            need(e == endpoint_edges(w, n), 'independent chord predicate')
            if n <= 5:
                for cut in range(len(w)):
                    need(edges(w[cut:] + w[:cut], n) == e, 'uniform rotation')
                    rotation_count += 1
            if n == 6 and all(sum(v in x for x in e) == 3 for v in range(n)):
                triangles = sum(all(p in e for p in combinations(t, 2)) for t in combinations(range(n), 3))
                cubic_hist[triangles] += 1
        need(len(seen) == math.factorial(2*n) // (2**n * math.factorial(n)), 'pairing enumeration count')
        pairing_counts[str(n)] = len(seen)
    need(dict(cubic_hist) == {0: 3}, 'prism lower bound')
    prism = tuple(int(v)-1 for v in '123415263456142536')
    prism_graph = {(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3),(1,4),(2,5)}
    need(edges(prism, 6) == prism_graph and set(Counter(prism).values()) == {3}, 'prism upper bound')

    nonuniform_count = 0
    for n in range(1, 4):
        for length in range(n, 9):
            for w in product(range(n), repeat=length):
                if len(set(w)) != n:
                    continue
                e = edges(w, n)
                u = uniformize(w, n)
                need(edges(u, n) == e, 'max-copy uniformization')
                nonuniform_count += 1
    need(edges((0,1,0),2) != edges((1,0,0),2), 'rotation needs equal counts')
    need(edges((0,1,0,1),2) == edges((1,0,1,0),2) == {(0,1)}, 'edge controls')
    need(edges((0,1,0,1,1,0,1,0),2) == set(), 'incompatible block concatenation destroys edge')
    need(edges((0,1),2) == {(0,1)} and edges((0,0,1,1),2) == set(), 'component floor of two')
    need(edges((0,1),2) == {(0,1)} and edges((0,1,1,0),2) == set(), 'false twin needs padding from k=1')
    need(edges((1,0,1,0),2) == {(0,1)}, 'reject one-sided nonedge occurrence condition')

    star_cases = 0
    oriented_counts = {}
    for n in range(1,6):
        pairs = list(combinations(range(n), 2))
        accepted = 0
        for mask in range(2 ** len(pairs)):
            arcs = {p for i,p in enumerate(pairs) if mask & (1 << i)}
            if not semitransitive(n, arcs):
                continue
            accepted += 1
            for v in range(n):
                w = star_word(n, arcs, v)
                e = edges(w,n)
                order = initial(w)
                need(set(Counter(w).values()) == {2}, 'star multiplicity')
                need(arcs <= e, 'star preserves graph edges')
                need(all(order[a] < order[b] for a,b in arcs), 'star compatibility')
                need(all((min(v,u),max(v,u)) not in e for u in range(n)
                         if u != v and (min(v,u),max(v,u)) not in arcs), 'star covers incident nonedges')
                star_cases += 1
        oriented_counts[str(n)] = accepted
    shortcut = {(0,1),(1,2),(2,3),(0,3)}
    need(not semitransitive(4, shortcut), 'shortcut rejected')
    need(any(not shortcut <= edges(star_word(4, shortcut,v),4) for v in range(4)), 'star hypothesis necessary')

    cover_pairs = 0
    words = sorted({tuple(p[v] for v in w) for w in pairing_words(3) for p in permutations(range(3))})
    allpairs = set(combinations(range(3),2))
    prepared = [(w,edges(w,3),initial(w)) for w in words]
    for choices in product((0,1,2), repeat=3):
        arcs = set()
        for (a,b), choice in zip(sorted(allpairs), choices):
            if choice:
                arcs.add((a,b) if choice == 1 else (b,a))
        graph = {(min(a,b),max(a,b)) for a,b in arcs}
        compatible = [(w,e) for w,e,pos in prepared if graph <= e and all(pos[a]<pos[b] for a,b in arcs)]
        for w,e in compatible:
            for z,f in compatible:
                actual = edges(w+z,3)
                need(graph <= actual <= e & f, 'compatible cover union')
                cover_pairs += 1

    crown_orientation_counts = {}
    for m in (3,4):
        base = [(a,m+b) for a in range(m) for b in range(m) if a != b]
        accepted = 0
        for dirs in product((0,1),repeat=len(base)):
            arcs = {(a,b) if d==0 else (b,a) for (a,b),d in zip(base,dirs)}
            transitive = all((a,c) in arcs for a,b in arcs for b2,c in arcs if b==b2)
            if transitive:
                accepted += 1
                need(all(a<m and b>=m for a,b in arcs) or all(a>=m and b<m for a,b in arcs), 'crown orientation uniqueness up to duality')
        need(accepted==2, 'crown transitive orientation count')
        crown_orientation_counts[str(m)] = accepted

    for n in range(3,501):
        k = n//2
        need(k*(n-1) >= (n//2)*((n+1)//2), 'counting barrier')
        need(math.factorial(n) >= 2**(n-1), 'factorial lower bound')

    bad = [([0,True],2),([0,-1],2),([0,2],2),([],1),([0],2)]
    for w,n in bad:
        try:
            edges(w,n)
        except Rejected:
            pass
        else:
            raise Rejected('malformed independent input accepted')

    return {'schema':'independent-word-representation-checks-v1','status':'PASS',
            'problem_id':1430,'small_witnesses':witness_count,'perfect_matching_counts':pairing_counts,
            'cubic_triangle_histogram':dict(cubic_hist),'uniform_rotation_cases':rotation_count,
            'max_copy_uniformization_cases':nonuniform_count,'star_cover_cases':star_cases,
            'semitransitive_topologically_labeled_graphs':oriented_counts,
            'compatible_block_pairs':cover_pairs,'crown_transitive_orientation_counts':crown_orientation_counts,
            'malformed_word_rejections':len(bad),'checks':checks}


if __name__ == '__main__':
    try:
        need(len(sys.argv)==2, 'usage: independent_checks.py /path/to/packet')
        print(json.dumps(main(Path(sys.argv[1])),sort_keys=True,separators=(',',':')))
    except (Rejected,OSError,ValueError,TypeError,KeyError,IndexError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(1)
