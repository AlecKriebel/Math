"""Exact checks for the structural examples in author turn 2 (no solver)."""
from itertools import combinations
import json


def cover_number(edges):
    vertices = sorted(set().union(*edges)) if edges else []
    for k in range(len(vertices) + 1):
        for chosen in combinations(vertices, k):
            if all(set(chosen) & e for e in edges):
                return k
    raise AssertionError("unreachable for nonempty edges")


def packing_report(edges, r):
    edges = [frozenset(e) for e in edges]
    assert len(edges) == len(set(edges)) and all(0 < len(e) <= r for e in edges)
    vertices = sorted(set().union(*edges))
    maximum = -1
    packings = []
    for mask in range(1 << len(edges)):
        chosen = [e for i, e in enumerate(edges) if mask >> i & 1]
        degree = {v: sum(v in e for e in chosen) for v in vertices}
        if max(degree.values(), default=0) > r:
            continue
        size = len(chosen)
        if size > maximum:
            maximum, packings = size, []
        if size == maximum:
            saturated = {v for v in vertices if degree[v] == r}
            incident = [e for e in chosen if e & saturated]
            residual = [e for e in chosen if not e & saturated]
            surplus = len(incident) - len(saturated)
            score = surplus + len(residual) - cover_number(residual)
            packings.append({"mask": mask, "saturated": sorted(saturated),
                             "surplus": surplus, "residual_edges": len(residual),
                             "certificate_saving": score})
    return {"r": r, "vertices": len(vertices), "edges": len(edges),
            "tau": cover_number(edges), "nu_r": maximum,
            "maximum_packings": packings}


def main():
    fano = [{0, 1, 2}, {0, 3, 4}, {0, 5, 6}, {1, 3, 5},
            {1, 4, 6}, {2, 3, 6}, {2, 4, 5}]
    extended = fano + [{0, 1, 7}]
    report = packing_report(extended, 3)
    assert report["tau"] == 3 and report["nu_r"] == 7
    assert len(report["maximum_packings"]) == 2
    assert sorted(p["certificate_saving"] for p in report["maximum_packings"]) == [0, 1]
    assert all(sum(bool(e & set(pair)) for e in fano) == 5
               for pair in combinations(range(7), 2))
    assert all(set([0, 1, 2]) & e for e in extended)
    # This minimal empty-intersection family is tau-critical, has tau=2,
    # and illustrates why tau-criticality alone does not force Delta>r.
    simplex = [set(range(4)) - {i} for i in range(4)]
    simplex_report = packing_report(simplex, 3)
    assert simplex_report["tau"] == 2 and simplex_report["nu_r"] == 4
    assert all(cover_number(simplex[:i] + simplex[i + 1:]) == 1 for i in range(4))
    output = {"extended_fano": report, "simplex": simplex_report,
              "method": "Direct enumeration of vertex transversals and edge packings; exact integer operations."}
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
