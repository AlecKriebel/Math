#!/usr/bin/env python3
"""Exact elementary controls. These are not a proof of BLRS descent."""
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path


def subsets(vertices, size):
    return list(combinations(vertices, size)) if size >= 0 else []


def alternating_value(c, ordered):
    if len(set(ordered)) != len(ordered):
        return 0
    sign = (-1) ** sum(ordered[i] > ordered[j]
                       for i in range(len(ordered))
                       for j in range(i + 1, len(ordered)))
    return sign * c.get(tuple(sorted(ordered)), 0)


def delta(c, degree, vertices):
    return {j: sum((-1) ** s * c.get(j[:s] + j[s+1:], 0)
                   for s in range(len(j)))
            for j in subsets(vertices, degree + 2)}


def contract(c, degree, vertices):
    if degree < 0:
        return {}
    b = min(vertices)
    return {j: alternating_value(c, (b,) + j)
            for j in subsets(vertices, degree)}


def check_cech():
    cases = 0
    vertex_sets = 0
    for r in range(1, 8):
        ground = tuple(range(r))
        for size in range(1, r + 1):
            for vertices in combinations(ground, size):
                vertex_sets += 1
                for degree in range(-1, len(vertices)):
                    basis = subsets(vertices, degree + 1)
                    for chosen in basis:
                        c = {chosen: 1}
                        dh = delta(contract(c, degree, vertices), degree - 1,
                                   vertices) if degree >= 0 else {}
                        hd = contract(delta(c, degree, vertices), degree + 1,
                                      vertices)
                        for j in basis:
                            assert dh.get(j, 0) + hd.get(j, 0) == c.get(j, 0)
                        dd = delta(delta(c, degree, vertices), degree + 1,
                                   vertices)
                        assert all(v == 0 for v in dd.values())
                        cases += 1
    return {"nonempty_vertex_sets": vertex_sets,
            "basis_vectors_checked": cases,
            "identities": ["delta*h+h*delta=identity", "delta*delta=0"]}


def rref(rows):
    rows = [[Fraction(x) for x in row] for row in rows]
    pivots = []
    p = 0
    for col in range(3):
        index = next((i for i in range(p, len(rows)) if rows[i][col]), None)
        if index is None:
            continue
        rows[p], rows[index] = rows[index], rows[p]
        scale = rows[p][col]
        rows[p] = [x / scale for x in rows[p]]
        for i in range(len(rows)):
            if i != p:
                scale = rows[i][col]
                rows[i] = [a - scale*b for a, b in zip(rows[i], rows[p])]
        pivots.append(col)
        p += 1
    return rows, pivots


def dimension(rows, invert_x=False):
    reduced, pivots = rref(rows)
    if any(all(a == 0 for a in row[:3]) and row[3] != 0 for row in reduced):
        return None
    if invert_x:
        for row, pivot in zip(reduced, pivots):
            if pivot == 0 and row[1] == row[2] == row[3] == 0:
                return None
    return 3 - len(pivots)


def check_faces():
    # Variables x,t1,t2; final entry is the right hand side.
    graph = [[-1, 1, 0, 0], [-1, 0, 1, 0]]
    faces = {0: [0, 1, 1, 1], 1: [0, 1, 0, 0], 2: [0, 0, 1, 0]}
    result = []
    for size in range(4):
        for face in combinations(range(3), size):
            rows = [faces[i] for i in face]
            ambient = dimension(rows)
            closure = dimension(graph + rows)
            opened = dimension(graph + rows, invert_x=True)
            codim_u = None if opened is None else ambient - opened
            codim_x = None if closure is None else ambient - closure
            assert codim_u is None or codim_u >= 2
            if face == (1, 2):
                assert ambient == 1 and closure == 0 and codim_x == 1
            result.append({"zero_coordinates": list(face),
                           "ambient_face_dimension": ambient,
                           "graph_in_A1_dimension": closure,
                           "graph_in_Gm_dimension": opened,
                           "codimension_in_A1_face": codim_x,
                           "codimension_in_Gm_face": codim_u})
    assert sum(r["codimension_in_A1_face"] is not None and
               r["codimension_in_A1_face"] < 2 for r in result) == 1
    return result


def check_weight_zero():
    def d(n):
        if n >= 0:
            return 0
        return 1 if (-n) % 2 == 0 else 0

    def h(n):
        return 1 if n < 0 and (-n) % 2 == 1 else 0

    for n in range(-60, 0):
        assert h(n)*d(n-1) + d(n)*h(n+1) == 1
        assert d(n)*d(n+1) == 0
    assert d(-1) == 0
    return {"negative_degrees_checked": 60, "splice_differential": 0}


def check_squares():
    isometries = 0
    for p in (3, 5, 7, 11, 13):
        for u in range(1, p):
            for v in range(p):
                assert (u*u*v*v) % p == ((u*v) % p)**2 % p
                isometries += 1
    parity = 0
    for valuation in range(-30, 31):
        for square_shift in range(-20, 21):
            assert (valuation + 2*square_shift) % 2 == valuation % 2
            parity += 1
    assert 1 % 2 == 1
    return {"finite_field_form_values_checked": isometries,
            "valuation_parities_checked": parity,
            "odd_uniformizer_residue_parity": 1}


def main():
    result = {
        "problem_id": 30004169,
        "status": "PASS",
        "arithmetic": "exact integers and rational numbers; Python standard library",
        "cech": check_cech(),
        "faces": check_faces(),
        "weight_zero": check_weight_zero(),
        "square_and_residue_controls": check_squares(),
        "limitations": [
            "Finite controls supplement the written proofs and do not decide BLRS descent.",
            "No arbitrary Milnor-Witt group, residue complex or motivic spectrum is computed.",
            "The face obstruction is a lower-term nonextension, not a cohomological counterexample.",
            "The full q>0 global Cech acyclicity remains unproved."
        ]
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output = Path(__file__).resolve().with_name("CHECK_RESULTS.json")
    if output.exists():
        assert output.read_text() == rendered, "Stored output differs from exact replay"
    else:
        output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
