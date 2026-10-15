#!/usr/bin/env python3
"""Exact rational controls for a bounded-intensity, non-Poisson process.

All mathematical checks use fractions.Fraction; decimals in the receipt are
display aids only. This is a finite stress control, not a proof of the theorem.

On (0,1], let the first arrival have defective density p=1/2, and,
conditional on a first arrival s, let the second arrival have defective
density q=1/2 on (s,1]. Stop after the second arrival. In its natural
filtration the intensity is p/(1-p*t) before the first arrival and
q/(1-q*(t-s)) between the first and second arrivals, hence at most 1.

The exact-count subdensities are j_1(s)=(1+s)/4 and j_2(s,t)=1/4 for
0<s<t<1. The process is not Poisson (it has at most two arrivals).

Test the full-field weight H=1_{S2>=1/2, S2-S1>=1/4} on N1=2 and the
two-phase rectangle [0,1/3] x [1/5,4/5]. The weighted original mass is
1/16 and the independent-uniform limit is 1/80. Polygon clipping
computes each prelimit integral exactly, including incomplete mesh cells.
"""

from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import platform


def clip(poly, a, b, c):
    """Intersect a rational polygon with a*x+b*y<=c."""
    if not poly:
        return []
    out = []
    old = poly[-1]
    f_old = a * old[0] + b * old[1] - c
    for new in poly:
        f_new = a * new[0] + b * new[1] - c
        if (f_old <= 0) != (f_new <= 0):
            t = f_old / (f_old - f_new)
            out.append((old[0] + t * (new[0] - old[0]),
                        old[1] + t * (new[1] - old[1])))
        if f_new <= 0:
            out.append(new)
        old, f_old = new, f_new
    return out


def area(poly):
    if len(poly) < 3:
        return F(0)
    cross = sum(x * v - y * u
                for (x, y), (u, v) in zip(poly, poly[1:] + poly[:1]))
    return abs(cross) / 2


weighted_polygon = [(F(0), F(1, 2)), (F(1, 4), F(1, 2)),
                    (F(3, 4), F(1)), (F(0), F(1))]
assert area(weighted_polygon) == F(1, 4)


def exact_phase_mass(delta):
    cells = (delta.denominator + delta.numerator - 1) // delta.numerator
    mass = F(0)
    for i in range(cells):
        lo_x, hi_x = delta * i, delta * (i + F(1, 3))
        if lo_x >= F(3, 4):
            continue
        for j in range(cells):
            lo_y, hi_y = delta * (j + F(1, 5)), delta * (j + F(4, 5))
            if hi_y <= F(1, 2) or lo_y >= 1:
                continue
            poly = weighted_polygon
            for a, b, c in [(F(-1), F(0), -lo_x),
                            (F(1), F(0), hi_x),
                            (F(0), F(-1), -lo_y),
                            (F(0), F(1), hi_y)]:
                poly = clip(poly, a, b, c)
            mass += F(1, 4) * area(poly)
    return mass


def main():
    p0 = F(1, 2)
    p1 = F(1, 4) + F(1, 8)  # integral_0^1 (1+s)/4 ds
    p2 = F(1, 4) * F(1, 2)  # constant j_2 times simplex area
    assert p0 + p1 + p2 == 1
    assert p2 == F(1, 8) and p1 == F(3, 8)
    target = F(1, 4) * area(weighted_polygon) * F(1, 3) * F(3, 5)
    assert target == F(1, 80)
    phase_rectangle = [(F(0), F(1, 5)), (F(1, 3), F(1, 5)),
                       (F(1, 3), F(4, 5)), (F(0), F(4, 5))]
    ordered_phase_area = area(clip(phase_rectangle, F(1), F(-1), F(0)))
    assert ordered_phase_area == F(43, 225)
    ordered_controls = []
    for n in (1, 2, 3, 7, 23, 97):
        # Off-diagonal macroscopic cells have unconstrained phases. Only
        # the n diagonal cells retain u<v. This equality is exact.
        phase_mass = F(1, 4) * (F(n - 1, 2 * n) * F(1, 5)
                                + F(1, n) * ordered_phase_area)
        error = phase_mass - F(1, 40)
        assert error == F(41, 1800 * n)
        ordered_controls.append({"n": n, "mass": str(phase_mass),
                                 "error": str(error)})
    meshes = [F(1, n) for n in (1, 2, 3, 7, 11, 23, 47, 97)]
    meshes += [F(2, 11), F(3, 29), F(5, 73)]
    rows = []
    for delta in meshes:
        mass = exact_phase_mass(delta)
        error = abs(mass - target)
        assert 0 <= mass <= F(1, 16)
        # A loose finite check, not an asserted general rate theorem.
        assert error <= delta
        rows.append({"mesh": str(delta), "weighted_phase_mass": str(mass),
                     "absolute_error": str(error),
                     "display_absolute_error": float(error)})
    receipt = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "arithmetic": "fractions.Fraction; all assertions exact",
        "random_sampling": False,
        "process": "bounded intensity <=1; at most two events; non-Poisson",
        "probabilities": {"N=0": str(p0), "N=1": str(p1), "N=2": str(p2)},
        "full_field_weighted_mass": "1/16",
        "independent_uniform_target": str(target),
        "ordered_diagonal_control": {
            "phase_triangle_area": str(ordered_phase_area),
            "unweighted_N2_target": "1/40",
            "exact_error_for_mesh_1_over_n": "41/(1800*n)",
            "checks": ordered_controls,
        },
        "controls": rows,
        "status": "PASS",
        "scope": "finite rational stress controls only; analytical proof required",
    }
    destination = Path(__file__).with_name("exact_phase_controls_receipt.json")
    destination.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
