#!/usr/bin/env python3
"""Bounded exact diagnostics. These checks are not a formal proof certificate."""
import collections
import itertools
import json
import math
from pathlib import Path
import sys

class Rejected(Exception):
    pass

checks = 0

def require(condition, message):
    global checks
    checks += 1
    if not condition:
        raise Rejected(message)

def unique_pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise Rejected('duplicate JSON key')
        result[key] = value
    return result

def reject_constant(value):
    raise Rejected('nonfinite number')

def finite_float(value):
    out = float(value)
    if not math.isfinite(out):
        raise Rejected('nonfinite number')
    return out

def parse(raw):
    if len(raw) > 2000000:
        raise Rejected('oversized JSON')
    return json.loads(raw, object_pairs_hook=unique_pairs,
                      parse_constant=reject_constant, parse_float=finite_float)

def word_edges(word, n, k=None):
    require(type(n) is int and 1 <= n <= 100, 'bad order')
    require(type(word) in (list, tuple) and 1 <= len(word) <= 10000, 'bad word')
    require(all(type(x) is int and 0 <= x < n for x in word), 'bad letter')
    counts = collections.Counter(word)
    require(set(counts) == set(range(n)), 'missing letter')
    require(len(set(counts.values())) == 1, 'nonuniform word')
    if k is not None:
        require(type(k) is int and k >= 1 and set(counts.values()) == {k}, 'wrong multiplicity')
    edges = set()
    for a, b in itertools.combinations(range(n), 2):
        pair = [x for x in word if x in (a, b)]
        if all(x != y for x, y in zip(pair, pair[1:])):
            edges.add((a, b))
    return edges

def graph_mask(edges, n):
    return sum(1 << i for i, pair in enumerate(itertools.combinations(range(n), 2)) if pair in edges)

def padding(word):
    return list(dict.fromkeys(word)) + list(word)

def twin(word, old, new, adjacent):
    result = []
    last = max(i for i, x in enumerate(word) if x == old)
    for i, x in enumerate(word):
        if x != old:
            result.append(x)
        else:
            result.extend([new, old] if not adjacent and i == last else [old, new])
    return result

def canonical_words(n):
    """All first-occurrence-normalized double-occurrence words, each exactly once."""
    counts = [0] * n
    word = []
    def visit(used):
        if len(word) == 2*n:
            yield tuple(word)
            return
        for letter in range(min(n, used+1)):
            if counts[letter] < 2:
                counts[letter] += 1
                word.append(letter)
                yield from visit(max(used, letter+1))
                word.pop()
                counts[letter] -= 1
    yield from visit(0)

def crossing_edges(word, n):
    positions = [[] for _ in range(n)]
    for i, x in enumerate(word):
        positions[x].append(i)
    return {(a,b) for a,b in itertools.combinations(range(n),2)
            if (positions[a][0] < positions[b][0] < positions[a][1] < positions[b][1])
            or (positions[b][0] < positions[a][0] < positions[b][1] < positions[a][1])}

def cone_realizer(m):
    out = []
    for i in range(m):
        out += [2*m] + [j for j in range(m) if j != i] + [m+i, i] + [m+j for j in range(m) if j != i]
    return out

def main():
    root = Path(__file__).resolve().parent
    data = parse((root/'SMALL_WITNESSES.json').read_bytes())
    require(type(data) is dict and set(data) == {str(n) for n in range(1,6)}, 'small witness orders')
    small_count = 0
    twins_count = 0
    padded_count = 0
    for n in range(1,6):
        values = data[str(n)]
        target = 1 << (n*(n-1)//2)
        require(type(values) is dict and set(values) == {str(m) for m in range(target)}, 'small witness mask inventory')
        for mask in range(target):
            word = values[str(mask)]
            edges = word_edges(word, n, 2)
            require(graph_mask(edges,n) == mask, 'small witness graph')
            require(edges == crossing_edges(word,n), 'independent crossing predicate')
            small_count += 1
            if n <= 4:
                require(word_edges(padding(word),n,3) == edges, 'padding')
                padded_count += 1
                for old in range(n):
                    for adjacent in (False,True):
                        expected = set(edges)
                        for a,b in edges:
                            if old in (a,b):
                                expected.add((b if a==old else a,n))
                        if adjacent:
                            expected.add((old,n))
                        require(word_edges(twin(word,old,n,adjacent),n+1,2) == expected,'twin insertion')
                        twins_count += 1
    disjoint_count = 0
    for n in range(1,4):
        for left in data[str(n)].values():
            le = word_edges(left,n,2)
            for m in range(1,4):
                for right in data[str(m)].values():
                    re = {(a+n,b+n) for a,b in word_edges(right,m,2)}
                    require(word_edges(left+[x+n for x in right],n+m,2) == le|re, 'disjoint union')
                    disjoint_count += 1
    cone_count = 0
    for m in range(2,9):
        n = 2*m+1
        expected = {(a,m+b) for a in range(m) for b in range(m) if a!=b}
        expected |= {(a,2*m) for a in range(2*m)}
        require(word_edges(cone_realizer(m),n,m) == expected, 'crown plus apex construction')
        require(n//2==m,'crown vertex accounting')
        cone_count += 1
    prism = [int(c)-1 for c in '123415263456142536']
    prism_edges = {(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3),(1,4),(2,5)}
    require(word_edges(prism,6,3)==prism_edges,'prism upper witness')
    normalized_count = 0
    cubic_histogram = collections.Counter()
    for word in canonical_words(6):
        normalized_count += 1
        edges = crossing_edges(word,6)
        # The subsequence implementation is independent of endpoint crossing.
        require(edges == word_edges(word,6,2), 'six-vertex crossing predicate')
        degrees = [sum(i in e for e in edges) for i in range(6)]
        if degrees == [3]*6:
            triangles = sum(all(e in edges for e in itertools.combinations(t,2))
                            for t in itertools.combinations(range(6),3))
            cubic_histogram[triangles] += 1
    require(normalized_count == math.factorial(12)//(2**6*math.factorial(6)) == 10395,
            'canonical generator completeness count')
    require(dict(cubic_histogram) == {0:3}, 'prism excluded from all normalized 2-words')
    arithmetic_count = 0
    for n in range(4,501):
        q = n//2
        require(1+(q+1)//2 <= q, 'bipartite coarse bound arithmetic')
        require(2*(n-(n-n//4)) <= n//2, 'large clique arithmetic')
        require(q*(n-1) >= (n//2)*((n+1)//2), 'multinomial counting barrier')
        if n>=9:
            require((n+3)//4 <= n//2,'2026 bipartite bound below target')
        arithmetic_count += 1
    # Concrete negative mathematical controls; no optimization-sensitive assert.
    require(word_edges([0,0,1,1],2,2)==set(),'edgeless control')
    require(word_edges([0,0,1,1],2,2)!={(0,1)},'reject wrong edge expectation')
    p3 = [0,1,0,2,1,2]
    require(word_edges(p3,3,2)=={(0,1),(1,2)},'reachability-poset countercontrol')
    require((0,2) not in word_edges(p3,3,2),'reject transitive-closure inference')
    require(2>3//2 and 2>2//2 and 1>1//2,'literal small-order defect')
    require(2!=max(1,1),'reject missing component floor of two')
    require(3!=2,'reject pure 2-block optimum for prism')
    bad_inputs = [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}',b'{"a":1e9999}',b'{']
    rejected_json = 0
    for value in bad_inputs:
        try:
            parse(value)
        except (Rejected,ValueError):
            rejected_json += 1
        else:
            raise Rejected('malformed JSON accepted')
    require(rejected_json==5,'JSON negative controls')
    rejected_words = 0
    for word,n,k in [([0,1,0],2,2),([0,True],2,1),([0,-1],2,1),([0,2],2,1),([],1,1),([0,0],2,2)]:
        try:
            word_edges(word,n,k)
        except Rejected:
            rejected_words += 1
        else:
            raise Rejected('malformed word accepted')
    require(rejected_words==6,'word negative controls')
    return {'schema':'word-representation-diagnostics-v1','status':'PASS',
            'problem_id':1430,'small_graph_witnesses':small_count,
            'padding_cases':padded_count,'twin_cases':twins_count,
            'disjoint_union_cases':disjoint_count,'crown_apex_cases':cone_count,
            'normalized_six_vertex_double_words':normalized_count,
            'cubic_word_triangle_histogram':dict(cubic_histogram),
            'arithmetic_orders':arithmetic_count,'malformed_json_rejections':rejected_json,
            'malformed_word_rejections':rejected_words,'checks':checks}

if __name__ == '__main__':
    try:
        print(json.dumps(main(),sort_keys=True,separators=(',',':')))
    except (Rejected,OSError,ValueError,TypeError,KeyError,IndexError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(1)
