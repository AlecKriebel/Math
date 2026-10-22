"""Exhaust normal forms for nine-edge graph links of maximum degree at most 3."""
from itertools import combinations
from pathlib import Path
import json


def first_obstruction(edges, n):
    for edge in edges:
        available = [v for v in range(n) if v not in edge]
        for triple in combinations(available, 3):
            if all(set(triple).intersection(other) for other in edges if other != edge):
                break
        else:
            return list(edge)
    raise AssertionError("A surviving graph requires mathematical investigation")


def build():
    records = []
    masks = [x for x in range(8) if x.bit_count() <= 2]
    for internal in [0, 1]:
        base_capacity = [2, 2, 3] if internal else [3, 3, 3]
        cross_target = 7 if internal else 8
        for u in masks:
            for v in masks:
                capacity = [base_capacity[i] - int(u >> i & 1) - int(v >> i & 1)
                            for i in range(3)]
                if min(capacity) < 0:
                    continue
                remaining = cross_target - u.bit_count() - v.bit_count()

                def visit(mask, left, caps, counts):
                    if mask == 8:
                        if left:
                            return
                        extra = [pat for pat, count in enumerate(counts, 1) for _ in range(count)]
                        edges = [(3, 4)] + ([(0, 1)] if internal else [])
                        rows = [(3, u), (4, v)] + [(5 + j, pat) for j, pat in enumerate(extra)]
                        for vertex, pattern in rows:
                            edges += [(i, vertex) for i in range(3) if pattern >> i & 1]
                        assert len(edges) == 9
                        bad = first_obstruction(edges, 5 + len(extra))
                        records.append([internal, u, v, counts, bad])
                        return
                    weight = mask.bit_count()
                    maximum = min([caps[i] for i in range(3) if mask >> i & 1] + [left // weight])
                    for count in range(maximum + 1):
                        visit(mask + 1, left - count * weight,
                              [caps[i] - count * int(mask >> i & 1) for i in range(3)],
                              counts + [count])

                visit(1, remaining, capacity, [])
    return {"format": "nine-edge-link-obstruction-v1", "records": records}


if __name__ == "__main__":
    output = Path(__file__).with_name("turn4_link_certificate.json")
    data = build()
    output.write_text(json.dumps(data, separators=(",", ":")) + "\n")
    print(json.dumps({"configurations": len(data["records"]), "path": output.name}))
