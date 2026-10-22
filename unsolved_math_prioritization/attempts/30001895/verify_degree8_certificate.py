"""Check complete normal forms and every eligible edge-trace family independently."""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys


def verify(path):
    raw = Path(path).read_bytes()
    data = json.loads(raw)
    assert data["format"] == "degree-eight-link-trace-v1"
    diamond = {frozenset(e) for e in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,4),(4,5),(3,5)]}
    records = {}
    for internal, u, v, counts, witness in data["link_records"]:
        key = (internal, u, v, tuple(counts))
        assert key not in records
        assert len(counts) == 7 and all(type(c) is int and 0 <= c <= 3 for c in counts)
        records[key] = witness
    profiles = []
    for counts in product(range(4), repeat=7):
        deg = tuple(sum(counts[s-1] for s in range(1,8) if s & (1<<i)) for i in range(3))
        if max(deg) <= 3:
            profiles.append((counts,deg,sum(deg)))
    visited, classified, cover_checks = set(), 0, 0
    for internal in range(3):
        inside = [frozenset(e) for e in [(0,1),(0,2)][:internal]]
        for u, v in product(range(8), repeat=2):
            if u.bit_count() > 2 or v.bit_count() > 2:
                continue
            for counts, deg, cross in profiles:
                if 1 + internal + u.bit_count() + v.bit_count() + cross != 8:
                    continue
                if any(deg[i] + int(bool(u & (1<<i))) + int(bool(v & (1<<i)))
                       + sum(i in e for e in inside) > 3 for i in range(3)):
                    continue
                key = (internal,u,v,counts)
                assert key in records
                visited.add(key)
                neighborhoods = [u,v] + [s for s in range(1,8) for _ in range(counts[s-1])]
                graph = {frozenset((3,4)), *inside}
                for x, mask in enumerate(neighborhoods,3):
                    graph.update(frozenset((i,x)) for i in range(3) if mask & (1<<i))
                n = 3 + len(neighborhoods)
                assert len(graph) == 8
                assert max(sum(x in e for e in graph) for x in range(n)) <= 3
                witness = records[key]
                if "bad_edge" in witness:
                    edge = frozenset(witness["bad_edge"])
                    assert len(edge) == 2 and edge in graph
                    for triple in combinations(set(range(n)) - edge,3):
                        cover_checks += 1
                        assert any(not set(triple) & other for other in graph - {edge})
                else:
                    assert set(witness) == {"diamond_image"}
                    image = witness["diamond_image"]
                    assert n == 6 and sorted(image) == list(range(6))
                    assert {frozenset(image[x] for x in e) for e in diamond} == graph
                    classified += 1
    assert visited == set(records)

    links = {
        "k5_disjoint":[tuple(e) for e in combinations(range(5),2) if e not in [(0,1),(2,3)]],
        "k5_adjacent":[tuple(e) for e in combinations(range(5),2) if e not in [(0,1),(0,2)]],
        "diamond_path":[(0,1),(0,2),(0,3),(1,2),(1,3),(2,4),(4,5),(3,5)],
    }
    supplied = {}
    for case in data["trace_cases"]:
        key = (case["link"],tuple(tuple(t) for t in case["private_covers"]))
        assert key not in supplied
        supplied[key] = case
    systems, families, witnesses_checked = set(), 0, 0
    for name, graph in links.items():
        vertices = set().union(*(set(e) for e in graph))
        choices, constrained = [], []
        for index, edge in enumerate(graph):
            rest = sorted(vertices - set(edge))
            def is_cover(points):
                return all(set(points) & set(other) for other in graph if other != edge)
            if any(is_cover(points) for points in combinations(rest,2)):
                continue
            constrained.append(index)
            choices.append([points for points in combinations(rest,3) if is_cover(points)])
        for private in product(*choices):
            key = (name,private)
            assert key in supplied
            systems.add(key)
            case = supplied[key]
            assert case["constrained_edges"] == constrained
            traces = [points for size in range(1,4) for points in combinations(sorted(vertices),size)
                      if all(set(points) & set(cover) for cover in private)]
            assert [list(t) for t in traces] == case["traces"]
            rows = {}
            for mask, nonstar, stars in case["witnesses"]:
                assert mask not in rows
                rows[mask] = (nonstar,stars)
            required = set()
            for mask in range(1 << len(traces)):
                families += 1
                chosen = [traces[j] for j in range(len(traces)) if mask & (1<<j)]
                if any(all(set(pair) & set(trace) for trace in chosen)
                       for pair in combinations(vertices,2)):
                    continue
                required.add(mask)
                assert mask in rows
                nonstar, stars = rows[mask]
                assert len(nonstar) == len(set(nonstar)) == 3
                assert len(stars) == len(set(stars)) == 3
                assert all(0 <= j < len(traces) and mask & (1<<j) for j in nonstar)
                assert all(0 <= j < len(graph) for j in stars)
                assert all(sum(x in traces[j] for j in nonstar) + sum(x in graph[j] for j in stars) <= 3
                           for x in vertices)
                witnesses_checked += 1
            assert required == set(rows)
    assert systems == set(supplied)
    return {"certificate_sha256":hashlib.sha256(raw).hexdigest(),
            "normal_forms":len(visited), "rejected_forms":len(visited)-classified,
            "diamond_isomorphisms":classified, "cover_triples_checked":cover_checks,
            "trace_systems":len(systems), "trace_families_checked":families,
            "packing_witnesses_checked":witnesses_checked, "verified":True}


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name("turn5_degree8_certificate.json")
    print(json.dumps(verify(path),indent=2))
