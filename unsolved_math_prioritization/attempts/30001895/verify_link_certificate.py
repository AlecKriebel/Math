"""Independently enumerate all normal forms and check each obstruction witness."""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys


def verify(path):
    raw = Path(path).read_bytes()
    data = json.loads(raw)
    assert data["format"] == "nine-edge-link-obstruction-v1"
    received = {}
    for internal, u, v, counts, bad in data["records"]:
        key = (internal, u, v, tuple(counts))
        assert key not in received
        assert len(counts) == 7 and all(type(x) is int and 0 <= x <= 3 for x in counts)
        received[key] = tuple(bad)

    # This enumeration uses a Cartesian product, not the builder's recursive
    # residual-capacity search. Each pattern count is <=3 from vertex degrees.
    profiles = []
    for counts in product(range(4), repeat=7):
        degrees = tuple(sum(counts[s - 1] for s in range(1, 8) if s & (1 << i))
                        for i in range(3))
        if max(degrees) <= 3:
            profiles.append((counts, degrees, sum(degrees)))
    visited = set()
    triple_checks = 0
    for internal in (0, 1):
        for u, v in product(range(8), repeat=2):
            if u.bit_count() > 2 or v.bit_count() > 2:
                continue
            for counts, extra_degrees, cross in profiles:
                if 1 + internal + u.bit_count() + v.bit_count() + cross != 9:
                    continue
                cover_degrees = [extra_degrees[i] + int(bool(u & (1 << i)))
                                 + int(bool(v & (1 << i))) + int(internal and i < 2)
                                 for i in range(3)]
                if max(cover_degrees) > 3:
                    continue
                key = (internal, u, v, counts)
                assert key in received
                visited.add(key)
                edges = {frozenset((3, 4))}
                if internal:
                    edges.add(frozenset((0, 1)))
                neighborhoods = [u, v]
                for pattern in range(1, 8):
                    neighborhoods += [pattern] * counts[pattern - 1]
                for vertex, mask in enumerate(neighborhoods, 3):
                    for i in range(3):
                        if mask & (1 << i):
                            edges.add(frozenset((i, vertex)))
                n = 3 + len(neighborhoods)
                assert len(edges) == 9
                assert max(sum(vtx in e for e in edges) for vtx in range(n)) <= 3
                bad = frozenset(received[key])
                assert len(bad) == 2 and bad in edges
                for cover in combinations(set(range(n)) - bad, 3):
                    triple_checks += 1
                    assert any(not set(cover).intersection(e) for e in edges - {bad})
    assert visited == set(received)
    return {"certificate_sha256": hashlib.sha256(raw).hexdigest(),
            "normal_forms": len(visited), "cover_triples_checked": triple_checks, "verified": True}


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("turn4_link_certificate.json")
    print(json.dumps(verify(path), indent=2))
