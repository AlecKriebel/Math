#!/usr/bin/env python3
"""Finite hypothesis controls, not a verifier of the imported topology theorems."""
import argparse
import hashlib
import itertools
import json
import pathlib
import sys

sys.dont_write_bytecode = True


def require(test, message):
    if not test:
        raise ValueError(message)


def edge(a, b):
    return frozenset((a, b))


def squares(vertices, edges):
    out = []
    for q in itertools.combinations(vertices, 4):
        es = [e for e in edges if e <= set(q)]
        if len(es) == 4 and all(sum(v in e for e in es) == 2 for v in q):
            out.append(list(q))
    return out


def cycle(m):
    require(isinstance(m, int) and m >= 3, "cycle size must be an integer >=3")
    return list(range(m)), {edge(i, (i+1) % m) for i in range(m)}


def flag_dimension_one(vertices, edges):
    return not any(all(edge(a, b) in edges for a, b in itertools.combinations(q, 2))
                   for q in itertools.combinations(vertices, 3))


def run():
    records = []
    for m in range(3, 31):
        vs, es = cycle(m)
        flag = flag_dimension_one(vs, es)
        sq = squares(vs, es)
        require(flag == (m >= 4), "cycle flag classification failed")
        require(bool(sq) == (m == 4), "cycle square classification failed")
        records.append({"cycle_length": m, "flag": flag, "induced_square_count": len(sq),
                        "admissible_circle_nerve": flag and not sq})
    # Barycentric subdivision of the boundary of a tetrahedron: vertices are
    # nonempty proper subsets of four labels; comparability is adjacency.
    subsets = [frozenset(c) for k in range(1, 4) for c in itertools.combinations(range(4), k)]
    bary_edges = {edge(i, j) for i, a in enumerate(subsets) for j, b in enumerate(subsets)
                  if i < j and (a < b or b < a)}
    bary_squares = squares(list(range(len(subsets))), bary_edges)
    witness_subsets = [frozenset([0]), frozenset([1]), frozenset([0,1,2]), frozenset([0,1,3])]
    witness = sorted(subsets.index(x) for x in witness_subsets)
    require(witness in bary_squares, "barycentric square witness missing")
    # The two suspension apices and two nonadjacent base vertices give a square.
    vs, es = cycle(5)
    susp_edges = es | {edge(a, v) for a in (5, 6) for v in vs}
    susp_squares = squares(vs+[5,6], susp_edges)
    require([0,2,5,6] in susp_squares, "suspension square witness missing")
    # The boundary of a tetrahedron has all pairs but omits the four-clique face.
    tetra_vertices = list(range(4))
    tetra_edges = {edge(a,b) for a,b in itertools.combinations(tetra_vertices,2)}
    require(not squares(tetra_vertices,tetra_edges), "tetrahedron graph unexpectedly has square")
    tetra_faces = {frozenset(c) for k in range(1,4) for c in itertools.combinations(tetra_vertices,k)}
    require(frozenset(tetra_vertices) not in tetra_faces, "tetrahedron boundary became simplex")
    # Finite arithmetic sanity: n>=5 gives vertex-link dimension n-1>=4.
    dimension_cases = [{"dimension": n, "vertex_link_dimension": n-1,
                        "obstruction_applies": n-1 >= 4} for n in range(1,65)]
    require(all(x["obstruction_applies"] == (x["dimension"] >= 5) for x in dimension_cases),
            "dimension reduction mismatch")
    return {"schema_version": 1, "all_controls_pass": True,
            "scope": "Finite examples and dimension arithmetic only; imported theorems are not certified.",
            "cycle_cases": records,
            "barycentric_tetrahedron_boundary": {"vertices":14,"edges":len(bary_edges),
                "induced_squares":len(bary_squares),"witness_vertex_subsets":[sorted(x) for x in witness_subsets]},
            "suspension_of_pentagon": {"induced_squares":len(susp_squares),"witness":[0,2,5,6]},
            "tetrahedron_boundary": {"no_induced_square":True,"flag":False},
            "dimension_arithmetic_cases":dimension_cases}


def verify_identity(paths):
    names = ["problems.json", "research_results.json", "catalog.json"]
    expected = ["04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf",
                "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b",
                "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566"]
    objects = []
    for name, file, digest in zip(names, paths, expected):
        b = pathlib.Path(file).read_bytes()
        require(hashlib.sha256(b).hexdigest() == digest, name + " hash mismatch")
        objects.append(json.loads(b))
    problems, reports, catalog = objects
    matches = [r for r in problems if r.get("id") == 6200014]
    require(len(matches) == 1, "target record must be unique")
    record = matches[0]
    require(record["problem_number"] == "AMR-061-0014", "target code mismatch")
    report = reports.get(record["problem_number"], {})
    digest = hashlib.sha256(json.dumps([record, report], sort_keys=True).encode()).hexdigest()
    require(digest == "1ec3eb8a33545c474dae36d4b1ed4c07552f04d21401776d3e67d4c14c057dd6", "review digest mismatch")
    cm = [r for r in catalog if r.get("id") == "6200014"]
    require(len(cm) == 1 and cm[0]["rank"] == 808 and cm[0]["review_hash"] == digest,
            "catalog identity mismatch")
    return {"identity_pass": True,"record_review_sha256":digest,"report_present":bool(report)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--identity", nargs=3)
    args = parser.parse_args()
    result = verify_identity(args.identity) if args.identity else run()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
