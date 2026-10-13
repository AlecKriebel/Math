"""Exact audit control: even concentric Poncelet does not suffice for k403,b.

This is not a counterexample to the confocal billiard target.  It isolates the
extra geometric information needed beyond Chavez-Caliz's Theorem 6.
"""
from fractions import Fraction as F
import json


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def area(p):
    return sum(cross(p[i], p[(i + 1) % len(p)]) for i in range(len(p))) / 2


def intersection(n, d, m, e):
    det = cross(n, m)
    assert det != 0
    return ((d * m[1] - n[1] * e) / det,
            (n[0] * e - d * m[0]) / det)


def polygon_from_lines(lines):
    return [intersection(*lines[i], *lines[(i + 1) % len(lines)])
            for i in range(len(lines))]


def derived(p, pole):
    pedal = []
    for i, v in enumerate(p):
        direction = sub(p[(i + 1) % len(p)], v)
        t = dot(sub(pole, v), direction) / dot(direction, direction)
        pedal.append(add(v, (t * direction[0], t * direction[1])))
    anti_lines = [(sub(v, pole), dot(sub(v, pole), v)) for v in p]
    outer_lines = [((v[0] / 25, v[1] / 9), F(1)) for v in p]
    return pedal, polygon_from_lines(anti_lines), polygon_from_lines(outer_lines)


def sample(name, p):
    inner_a2, inner_b2 = F(9), F(144, 25)
    assert 0 < inner_a2 < 25 and 0 < inner_b2 < 9
    assert inner_a2 / 25 != inner_b2 / 9  # not homothetic; no shared infinity points
    assert 25 - inner_a2 != 9 - inner_b2  # not confocal
    for x, y in p:
        assert x*x / 25 + y*y / 9 == 1
    for i, v in enumerate(p):
        direction = sub(p[(i + 1) % len(p)], v)
        n = (-direction[1], direction[0])
        d = dot(n, v)
        assert inner_a2 * n[0]**2 + inner_b2 * n[1]**2 == d**2
    pedal, anti, outer = derived(p, (F(4), F(0)))
    return {
        "name": name, "original_vertices": [[str(x), str(y)] for x,y in p],
        "original_area": str(area(p)), "outer_area": str(area(outer)),
        "classical_product": str(area(p) * area(outer)),
        "focal_pedal_area": str(area(pedal)),
        "focal_antipedal_area": str(area(anti)),
        "target_form_product": str(area(pedal) * area(anti)),
    }


def main():
    rows = [sample("axial diamond", [(F(5), F(0)), (F(0), F(3)),
                                     (F(-5), F(0)), (F(0), F(-3))]),
            sample("axis rectangle", [(F(3), F(12,5)), (F(-3), F(12,5)),
                                       (F(-3), F(-12,5)), (F(3), F(-12,5))])]
    assert rows[0]["classical_product"] == rows[1]["classical_product"]
    assert rows[0]["target_form_product"] != rows[1]["target_form_product"]
    print(json.dumps({"scope": "nonconfocal concentric general-position control",
                      "outer_axes": ["5", "3"], "inner_axes": ["3", "12/5"],
                      "pole": ["4", "0"], "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
