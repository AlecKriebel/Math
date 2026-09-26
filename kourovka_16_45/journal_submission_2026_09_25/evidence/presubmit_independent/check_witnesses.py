"""Fresh finite arithmetic audit, transcribed only from the manuscript.

Python standard library; integer arithmetic reduced mod 29. Enumerates H,
three named pair subgroups, and three affine subgroups of order 58. Does
not enumerate G, or any subgroup lattice.
"""

import hashlib
import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path


P = 29
I = (1, 0, 0, 1)
NEG_I = (28, 0, 0, 28)
A = (0, 28, 1, 0)
B = (2, 7, 12, 28)
R1 = A
R2 = (12, 24, 0, 17)
R3 = (25, 3, 4, 4)


def mm(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return ((a*e+b*g) % P, (a*f+b*h) % P,
            (c*e+d*g) % P, (c*f+d*h) % P)


def mpow(x, n):
    result = I
    for _ in range(n):
        result = mm(result, x)
    return result


def determinant(x):
    a, b, c, d = x
    return (a*d-b*c) % P


def closure(generators, identity, multiply, bound):
    # In a finite ambient group, the generated monoid is the subgroup.
    seen = {identity}
    todo = deque([identity])
    while todo:
        x = todo.popleft()
        for y in generators:
            z = multiply(x, y)
            if z not in seen:
                seen.add(z)
                assert len(seen) <= bound, "Unexpected closure size"
                todo.append(z)
    return seen


def order(x, identity, multiply, bound):
    y = identity
    for k in range(1, bound+1):
        y = multiply(y, x)
        if y == identity:
            return k
    raise AssertionError("Order exceeds explicit finite bound")


def act(m, v):
    a, b, c, d = m
    x, y = v
    return ((a*x+b*y) % P, (c*x+d*y) % P)


def vadd(v, w):
    return tuple((x+y) % P for x, y in zip(v, w))


def affine(x, y):
    v, h = x
    w, k = y
    return (vadd(v, act(h, w)), mm(h, k))


checks = {}


def check(name, actual, expected):
    assert actual == expected, (name, actual, expected)
    checks[name] = actual


H = closure([A, B], I, mm, 120)
check("determinants_A_B_R1_R2_R3", [determinant(m) for m in (A,B,R1,R2,R3)], [1]*5)
check("H_size", len(H), 120)
check("all_H_determinants_one", all(determinant(h) == 1 for h in H), True)
check("A_squared", mpow(A,2), NEG_I)
check("B_cubed", mpow(B,3), NEG_I)
check("AB_fifth_power", mpow(mm(A,B),5), NEG_I)
check("R2_word_BAB2", mm(mm(B,A),mpow(B,2)), R2)
check("R3_word_AR2_AB2", mm(mm(A,R2),mpow(mm(A,B),2)), R3)
check("R_membership_H", all(r in H for r in (R1,R2,R3)), True)
check("R_squares", [mpow(r,2) for r in (R1,R2,R3)], [NEG_I]*3)
check("R_orders", [order(r,I,mm,120) for r in (R1,R2,R3)], [4]*3)
products = [mm(R2,R3), mm(R1,R3), mm(R1,R2)]
check("product_orders_23_13_12", [order(r,I,mm,120) for r in products], [4,3,10])
Z = {I, NEG_I}
check("projective_product_orders_23_13_12",
      [next(k for k in range(1,121) if mpow(r,k) in Z) for r in products], [2,3,5])
pair_groups = [closure(g,I,mm,120) for g in ((R2,R3),(R1,R3),(R1,R2))]
check("pair_subgroup_sizes_23_13_12", [len(j) for j in pair_groups], [8,12,20])
check("triple_generates_H", closure((R1,R2,R3),I,mm,120) == H, True)
check("each_R_missing_from_other_pair", [r not in j for r,j in zip((R1,R2,R3),pair_groups)], [True]*3)
check("first_two_pairs_intersect_in_R3", pair_groups[0] & pair_groups[1] == closure((R3,),I,mm,4), True)
check("triple_pair_intersection_Z", set.intersection(*pair_groups) == Z, True)
check("e1_and_Ae1_span_V", act(A,(1,0)), (0,1))
# Also check the orbit-spanning assertion for each named pair, without G.
check("each_pair_orbit_e1_spans_V", [any(act(h,(1,0))[1] != 0 for h in j) for j in pair_groups], [True]*3)

E = ((0,0),I)
li_gens = [(((1,0),I),((0,0),NEG_I)),
           (((0,1),I),((0,0),NEG_I)),
           (((1,1),I),((2,0),NEG_I))]
Ls = [closure(g,E,affine,58) for g in li_gens]
check("L_sizes", [len(j) for j in Ls], [58]*3)
formulas = [
    {((t,0),m) for t in range(P) for m in (I,NEG_I)},
    {((0,t),m) for t in range(P) for m in (I,NEG_I)},
    {((t,t),I) for t in range(P)} | {(((t+2)%P,t),NEG_I) for t in range(P)},
]
check("L_closed_forms", [j == f for j,f in zip(Ls,formulas)], [True]*3)
expected = [{E,((0,0),NEG_I)}, {E,((2,0),NEG_I)}, {E,((0,27),NEG_I)}]
actual = [Ls[0] & Ls[1], Ls[0] & Ls[2], Ls[1] & Ls[2]]
check("L_pair_intersections_12_13_23", [a == e for a,e in zip(actual,expected)], [True]*3)
checks["L_pair_intersection_elements_12_13_23"] = [sorted(j) for j in actual]
check("L_triple_intersection_identity", set.intersection(*Ls) == {E}, True)
check("G_order_from_semidirect_product", P**2 * len(H), 100920)
check("coset_degree", sum((P**2 * len(H)) // len(j) for j in Ls), 5220)
check("coset_indices_integral", all((P**2 * len(H)) % len(j) == 0 for j in Ls), True)
check("conjugate_of_negative_identity", affine(affine(((1,0),I),((0,0),NEG_I)),((28,0),I)), ((2,0),NEG_I))

manuscript = Path("/Users/alec/Documents/Math/kourovka_16_45/journal_submission_2026_09_25/manuscript/kourovka_16_45.tex")
result = {
    "status": "PASS",
    "timestamp_UTC": datetime.now(timezone.utc).isoformat(),
    "manuscript_sha256": hashlib.sha256(manuscript.read_bytes()).hexdigest(),
    "number_of_named_checks": len(checks),
    "scope": "H, three named matrix pairs, three named order-58 affine subgroups; no G or subgroup lattice enumeration",
    "checks": checks,
}
out = Path(__file__).with_name("results.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
