"""Construct exact link classification and trace-to-packing certificates."""
from itertools import combinations, permutations, product
from pathlib import Path
import json

DIAMOND = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,4),(4,5),(3,5)]
LINKS = [
    ("k5_disjoint", [e for e in combinations(range(5), 2) if e not in [(0,1),(2,3)]]),
    ("k5_adjacent", [e for e in combinations(range(5), 2) if e not in [(0,1),(0,2)]]),
    ("diamond_path", DIAMOND),
]


def small_link_records():
    records = []
    masks = [x for x in range(8) if x.bit_count() <= 2]
    for inside in [[], [(0,1)], [(0,1),(0,2)]]:
        base = [3 - sum(i in e for e in inside) for i in range(3)]
        for u, v in product(masks, repeat=2):
            caps = [base[i] - int(u >> i & 1) - int(v >> i & 1) for i in range(3)]
            left = 7 - len(inside) - u.bit_count() - v.bit_count()
            if min(caps) < 0 or left < 0:
                continue
            def visit(pattern, left, caps, counts):
                if pattern == 8:
                    if left:
                        return
                    extra = [s for s, count in enumerate(counts, 1) for _ in range(count)]
                    edges = [(3,4)] + inside
                    for vertex, mask in [(3,u),(4,v)] + list(enumerate(extra,5)):
                        edges += [(i,vertex) for i in range(3) if mask >> i & 1]
                    n = 5 + len(extra)
                    assert len(edges) == 8
                    for edge in edges:
                        choices = combinations([x for x in range(n) if x not in edge], 3)
                        if not any(all(set(c) & set(f) for f in edges if f != edge) for c in choices):
                            records.append([len(inside),u,v,counts,{"bad_edge":list(edge)}])
                            return
                    assert n == 6
                    original = {frozenset(e) for e in edges}
                    for image in permutations(range(6)):
                        if {frozenset(image[x] for x in e) for e in DIAMOND} == original:
                            records.append([len(inside),u,v,counts,{"diamond_image":list(image)}])
                            return
                    raise AssertionError("unclassified link")
                weight = pattern.bit_count()
                bound = min([caps[i] for i in range(3) if pattern >> i & 1] + [left // weight])
                for count in range(bound + 1):
                    visit(pattern + 1, left - count * weight,
                          [caps[i] - count * int(pattern >> i & 1) for i in range(3)],
                          counts + [count])
            visit(1, left, caps, [])
    return records


def trace_cases():
    cases = []
    for name, graph in LINKS:
        vertices = sorted(set().union(*(set(e) for e in graph)))
        choices, constrained = [], []
        for i, edge in enumerate(graph):
            available = [v for v in vertices if v not in edge]
            if any(all(set(t) & set(f) for f in graph if f != edge)
                   for t in combinations(available, 2)):
                continue
            constrained.append(i)
            choices.append([t for t in combinations(available, 3)
                            if all(set(t) & set(f) for f in graph if f != edge)])
        for system in product(*choices):
            traces = [a for size in range(1,4) for a in combinations(vertices, size)
                      if all(set(a) & set(t) for t in system)]
            packings = []
            for triple in combinations(range(len(traces)), 3):
                for stars in combinations(range(8), 3):
                    if all(sum(v in traces[i] for i in triple)
                           + sum(v in graph[j] for j in stars) <= 3 for v in vertices):
                        packings.append((sum(1 << i for i in triple), triple, stars))
                        break
            pair_covers = [sum(1 << i for i, trace in enumerate(traces) if set(pair) & set(trace))
                           for pair in combinations(vertices, 2)]
            witnesses = []
            for family in range(1 << len(traces)):
                if any(family & ~cover == 0 for cover in pair_covers):
                    continue
                for mask, triple, stars in packings:
                    if family & mask == mask:
                        witnesses.append([family, list(triple), list(stars)])
                        break
                else:
                    raise AssertionError("trace family without a cover or packing")
            cases.append({"link": name, "constrained_edges": constrained,
                          "private_covers": system, "traces": traces, "witnesses": witnesses})
    return cases


if __name__ == "__main__":
    data = {"format":"degree-eight-link-trace-v1", "link_records":small_link_records(),
            "trace_cases":trace_cases()}
    path = Path(__file__).with_name("turn5_degree8_certificate.json")
    path.write_text(json.dumps(data, separators=(",", ":")) + "\n")
    print(json.dumps({"normal_forms":len(data["link_records"]),
                      "trace_systems":len(data["trace_cases"]),
                      "packing_witnesses":sum(len(c["witnesses"]) for c in data["trace_cases"])}))
