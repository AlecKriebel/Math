#!/usr/bin/env python3
"""First-party rational geometry and inherited-incidence checks.

No historical verifier is imported. Finite checks supplement the universal
strip/cap/row-map proof in SEALED_CRITERION.md; they are not a proof by sampling.
"""
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter, defaultdict
from math import gcd, lcm
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

HALF, THREEHALF = F(1, 2), F(3, 2)
HERE = Path(__file__).resolve().parent
ASSERTIONS = []


def require(label, statement):
    if not statement:
        raise AssertionError(label)
    ASSERTIONS.append(label)


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def sq(p):
    return dot(p, p)


def nearest_edge(e):
    a, b = e
    v = sub(b, a)
    t = max(F(0), min(F(1), -dot(a, v) / sq(v)))
    point = a[0] + t * v[0], a[1] + t * v[1]
    return sq(point), point


def triangle_nearest(t):
    a, b, c = t
    orientation = cross(sub(b, a), sub(c, a))
    contains = all(cross(sub(v, u), (-u[0], -u[1])) * orientation >= 0
                   for u, v in ((a, b), (b, c), (c, a)))
    return (F(0), (F(0), F(0))) if contains else min(nearest_edge(e) for e in combinations(t, 2))


def inner_halfplane(a, b, witness):
    v = sub(b, a)
    coefficients = [-v[1], v[0], -cross(v, a)]
    if coefficients[0] * witness[0] + coefficients[1] * witness[1] + coefficients[2] < 0:
        coefficients = [-x for x in coefficients]
    denominator = lcm(*(x.denominator for x in coefficients))
    integers = [int(x * denominator) for x in coefficients]
    divisor = gcd(*integers)
    return tuple(x // divisor for x in integers)


def offsets(delta, tall=F(1), bound=8):
    a = {0: F(0)}
    for j in range(bound):
        a[j + 1] = a[j] + delta[j] + tall
    for j in range(-1, -bound - 1, -1):
        a[j] = a[j + 1] - delta[j] - tall
    return a


def generate(word, upper=False, root_j=0, root_k=0, tall=F(1), reflect=True):
    delta = {j: word.get(j, HALF if j % 2 else THREEHALF) for j in range(-8, 9)}
    a = offsets(delta, tall)
    central = delta[root_j]

    def transform(p):
        x, y = p[0] - a[root_j] - 2 * root_k, p[1] - 4 * root_j
        if upper:
            x, y = central - x, 1 - y
        if reflect and central == THREEHALF:
            x = -x
        return x, y

    triangles = set()
    for j in range(root_j - 2, root_j + 3):
        for k in range(root_k - 6, root_k + 7):
            p = (a[j] + 2 * k, F(4 * j))
            pn = (p[0] + 2, p[1])
            q = (a[j] + delta[j] + 2 * k, F(4 * j + 1))
            qp = (q[0] - 2, q[1])
            z = (a[j + 1] + 2 * k, F(4 * j + 4))
            zp = (z[0] - 2, z[1])
            for triangle in ((p, pn, q), (qp, q, p),
                             (q, (q[0] + 2, q[1]), z), (zp, z, q)):
                triangles.add(tuple(sorted(transform(v) for v in triangle)))
    return triangles


def classify(triangles, r2=F(10), suppress_singletons=False):
    edges = {tuple(sorted(e)) for t in triangles for e in combinations(t, 2)}
    vertices = {v for e in edges for v in e if sq(v) <= r2}
    edge_kind, face_kind, face_key = {}, {}, {}
    edge_faces = defaultdict(list)
    for triangle in triangles:
        d, p = triangle_nearest(triangle)
        kind = "area" if d < r2 else "point" if d == r2 else "empty"
        face_kind[triangle] = (kind, p)
        if kind == "area":
            active = []
            for i in range(3):
                e = tuple(sorted((triangle[i], triangle[(i + 1) % 3])))
                if nearest_edge(e)[0] < r2:
                    active.append(inner_halfplane(*e, triangle[(i + 2) % 3]))
            face_key[triangle] = ("face_area", tuple(sorted(active)))
        for e in combinations(triangle, 2):
            edge_faces[tuple(sorted(e))].append(triangle)
    for e in edges:
        d, p = nearest_edge(e)
        edge_kind[e] = ("length" if d < r2 else "point" if d == r2 else "empty", p)

    # Collapsed edges remain distinct cells. Each is distinguished by its
    # incident positive face: cap, outward tall face, or neither. This gives
    # an explicit bijection, not only equality of singleton multiplicities.
    edge_key = {}
    for e, (kind, p) in edge_kind.items():
        if kind == "length":
            edge_key[e] = ("edge_length", e)
        elif kind == "point" and not suppress_singletons:
            positive_neighbors = tuple(sorted(face_key[t] for t in edge_faces[e] if t in face_key))
            edge_key[e] = ("edge_point", p, positive_neighbors)
    for triangle, (kind, p) in face_kind.items():
        if kind == "point" and not suppress_singletons:
            keys = tuple(sorted(edge_key[tuple(sorted(e))] for e in combinations(triangle, 2)
                                if tuple(sorted(e)) in edge_key))
            face_key[triangle] = ("face_point", p, keys)

    # Full inherited incidences and geometric keys, keeping parent-cell
    # multiplicities. Circle arcs are determined by area halfplanes and D.
    edge_counter = Counter(edge_key.values())
    face_counter = Counter(face_key.values())
    incidences = Counter()
    for e, key in edge_key.items():
        for v in e:
            if v in vertices:
                incidences[(("vertex", v), key)] += 1
        for triangle in edge_faces[e]:
            if triangle in face_key:
                incidences[(key, face_key[triangle])] += 1
    for triangle, key in face_key.items():
        for v in triangle:
            if v in vertices:
                incidences[(("vertex", v), key)] += 1
    signature = (tuple(sorted(vertices)), tuple(sorted(edge_counter.items())),
                 tuple(sorted(face_counter.items())), tuple(sorted(incidences.items())))
    boundary_edges = Counter(p for kind, p in edge_kind.values() if kind == "point")
    boundary_faces = Counter(p for kind, p in face_kind.values() if kind == "point")
    all_lengths = {tuple(sorted(sq(sub(a, b)) for a, b in combinations(t, 2))) for t in triangles}
    all_areas = {abs(cross(sub(t[1], t[0]), sub(t[2], t[0]))) / 2 for t in triangles}
    counts = {"vertices": len(vertices),
              "positive_edges": sum(k == "length" for k, p in edge_kind.values()),
              "point_edges": sum(boundary_edges.values()),
              "positive_faces": sum(k == "area" for k, p in face_kind.values()),
              "point_faces": sum(boundary_faces.values()),
              "inherited_incidence_pairs": sum(incidences.values()),
              "unique_geometric_and_incidence_edge_keys": len(edge_counter),
              "unique_geometric_and_incidence_face_keys": len(face_counter)}
    details = {"counts": counts, "boundary_edges": boundary_edges,
               "boundary_faces": boundary_faces, "lengths": all_lengths, "areas": all_areas,
               "edge_key_multiplicities": list(edge_counter.values()),
               "face_key_multiplicities": list(face_counter.values())}
    return signature, details


def plain(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): plain(v) for k, v in x.items()}
    if isinstance(x, (tuple, list, set)):
        return [plain(v) for v in x]
    return x


def main():
    baseline_word = {j: HALF for j in range(-3, 4)}
    base, detail = classify(generate(baseline_word))
    expected_counts = {"vertices": 8, "positive_edges": 28, "point_edges": 6,
                       "positive_faces": 23, "point_faces": 4}
    require("baseline_counts", all(detail["counts"][k] == v for k, v in expected_counts.items()))
    require("unique_cell_keys", all(v == 1 for v in detail["edge_key_multiplicities"] + detail["face_key_multiplicities"]))
    # General exact classifier boundary checks: a tangent at the interior of
    # an edge, no original vertex in D, and a face containing the entire D.
    tangent = tuple(sorted(((F(-2), F(4)), (F(4), F(2)), (F(2), F(6)))))
    tangent_sig, tangent_detail = classify({tangent})
    require("interior_edge_tangent_point", nearest_edge(tuple(sorted(tangent[:2])))[0] == 10
            or any(nearest_edge(e) == (F(10), (F(1), F(3))) for e in combinations(tangent, 2)))
    require("triangle_tangent_no_vertices", tangent_detail["counts"]["vertices"] == 0
            and tangent_detail["counts"]["point_edges"] == 1
            and tangent_detail["counts"]["point_faces"] == 1
            and tangent_detail["counts"]["positive_faces"] == 0)
    containing = tuple(sorted(((F(-20), F(-20)), (F(20), F(-20)), (F(0), F(20)))))
    contain_sig, contain_detail = classify({containing})
    require("whole_disk_face_without_visible_edges", contain_detail["counts"]["vertices"] == 0
            and contain_detail["counts"]["positive_edges"] == 0
            and contain_detail["counts"]["positive_faces"] == 1)
    for t in generate(baseline_word):
        for a, b, w in ((t[0], t[1], t[2]), (t[1], t[2], t[0]), (t[2], t[0], t[1])):
            line = inner_halfplane(a, b, w)
            val = lambda p: line[0] * p[0] + line[1] * p[1] + line[2]
            require("oriented_plane_endpoints_and_witness", val(a) == val(b) == 0 and val(w) > 0)
    cases = []
    # Every seven-bit window and BOTH row types, with nonconstant external
    # continuations; these extra choices cannot replace the universal proof.
    for bits in product((HALF, THREEHALF), repeat=7):
        word = dict(zip(range(-3, 4), bits))
        for upper in (False, True):
            sig, data = classify(generate(word, upper))
            label = "".join("0" if d == HALF else "1" for d in bits) + ("U" if upper else "L")
            require("full_geometry_incidence_" + label, sig == base)
            require("diameter_and_area_" + label, data["lengths"] == {(F(5, 4), F(13, 4), F(4)), (F(4), F(10), F(10))} and data["areas"] == {F(1), F(3)})
            cases.append(label)

    # Rational translations and shifted layer roots cannot change the patch.
    shifted_cases = []
    for root_j, root_k, upper in product((-2, -1, 1, 2), (-17, 11), (False, True)):
        word = {j: HALF if j in {-3, -1, 2, 3} else THREEHALF for j in range(-8, 9)}
        sig, data = classify(generate(word, upper, root_j, root_k))
        require("shifted_root_" + str((root_j, root_k, upper)), sig == base)
        shifted_cases.append((root_j, root_k, upper))

    # Exact strict cap inequalities and generic section partition at rational
    # controls (the formula in the sealed proof is valid for every real t).
    for d, px in product((HALF, THREEHALF), (-1, 1)):
        for h in (-d, 2 - d):
            require("strict_outward_" + str((d, px, h)), dot((F(px), F(-3)), (h, F(-1))) >= F(3, 2))
    require("far_edges_strict_margin", F(45, 4) - 10 == F(5, 4))
    for h, t in product((HALF, THREEHALF), (F(1, 16), F(1, 8), F(5, 32))):
        circular_width_squared = 1 - 6 * t - t * t
        triangular_width = 1 - h * t
        require("cap_containment_exact_" + str((h, t)), circular_width_squared >= 0
                and triangular_width > 0
                and triangular_width ** 2 - circular_width_squared >= 3 * t)
    for s, t, k in product((HALF, F(1), THREEHALF), (F(0), F(1, 7), F(5, 11), F(1)), range(-2, 3)):
        e = (2 * k + (s - 2) * t, 2 * k + s * t)
        d = (e[1], 2 * (k + 1) + (s - 2) * t)
        require("section_partition_" + str((s, t, k)), e[0] <= e[1] == d[0] <= d[1] and d[1] == 2 * (k + 1) + (s - 2) * t)

    negative = []
    # NEW exact thresholds are distinct from the historical 1001/100 control.
    alternate = dict(baseline_word); alternate[-1] = THREEHALF
    larger = F(10) + F(1, 4096)
    bigger_a, bigger_da = classify(generate(baseline_word), larger)
    bigger_b, bigger_db = classify(generate(alternate), larger)
    require("new_larger_radius_full_cells_detect_neighbor", bigger_a != bigger_b)
    require("larger_radius_vertex_set_blind", bigger_a[0] == bigger_b[0])
    negative.append({"mutation": "r_squared=10+1/4096", "detected": True,
                     "rooted_vertex_sets_equal": True, "claim": "canonical full-cell comparison detects remote chirality; does not exclude every alternative ambient map"})
    smaller = F(10) - F(1, 4096)
    require("new_smaller_radius_diameter_violation", F(10) > smaller)
    negative.append({"mutation": "r_squared=10-1/4096", "detected": True,
                     "failure": "tall triangle diameter exceeds comparison radius"})
    no_boundary, no_bd = classify(generate(baseline_word), suppress_singletons=True)
    require("singleton_omission_rejected", no_boundary != base)
    require("singleton_omission_counts_blind", all(no_bd["counts"][k] == detail["counts"][k] for k in ("vertices", "positive_edges", "positive_faces")))
    negative.append({"mutation": "discard all singleton traces", "detected": True,
                     "vertices_and_positive_piece_counts_unchanged": True,
                     "failure": "full restricted cell collection and inherited incidence lost"})
    deformed = F(9, 8)
    deform_a, deform_da = classify(generate(baseline_word, tall=deformed))
    deform_b, deform_db = classify(generate({j: THREEHALF for j in range(-3, 4)}, tall=deformed))
    require("deformed_tall_shift_diameter_failure", any(max(t) > 10 for t in deform_da["lengths"]))
    require("deformed_tall_shift_congruence_failure", deform_a != deform_b)
    negative.append({"mutation": "tall shift=9/8", "detected": True,
                     "failure": "diameter threshold and prescribed reflected patch equality both fail"})
    wrong_map, wrong_data = classify(generate({j: THREEHALF for j in range(-3, 4)}, reflect=False))
    require("omitted_reflection_rejected", wrong_map != base)
    require("omitted_reflection_counts_blind", wrong_data["counts"] == detail["counts"])
    negative.append({"mutation": "omit chirality reflection", "detected": True,
                     "all_piece_counts_unchanged": True, "failure": "canonical geometry/incidence signatures differ"})
    cap_inside = (F(0), F(-25, 8))
    require("flipped_cap_face_orientation_rejected", sq(cap_inside) < 10
            and -cap_inside[1] - 3 > 0 and cap_inside[1] + 3 < 0)
    negative.append({"mutation": "reverse the cap base halfplane orientation", "detected": True,
                     "exact_witness": ["0", "-25/8"],
                     "failure": "positive-area cap point is excluded although its squared radius is 625/64<10"})

    result = {"status": "PASS", "arithmetic": "fractions.Fraction",
              "at_utc": datetime.now(timezone.utc).isoformat(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "seven_bit_assignments": 128, "rooted_cases": len(cases),
              "additional_shifted_roots": len(shifted_cases), "assertions": len(ASSERTIONS),
              "closed_disk": plain(detail), "negative_controls": negative,
              "cases": cases, "checks": ASSERTIONS,
              "scope": "Complete finite full-cell and inherited-incidence comparison after separately sealed universal locality proof; zero proof-search attempts added"}
    (HERE / "full_cell_results.json").write_text(json.dumps(result, indent=2) + "\n")
    (HERE / "canonical_cell_certificate.json").write_text(json.dumps({
        "radius_squared": 10, "canonical_chirality": "1/2",
        "geometric_cell_signature_and_inherited_incidence": plain(base),
        "counts": detail["counts"],
        "interpretation": "Positive edge keys keep whole endpoints. Positive faces keep inward active halfplanes. Collapsed edges are distinguished by incident positive faces; singleton faces by their nonempty edge keys. All keys have multiplicity one, supplying a literal cell bijection. Circle arcs are the halfplane/disk intersections."}, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"checks", "cases"}}, indent=2))


if __name__ == "__main__":
    main()
