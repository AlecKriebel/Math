"""A face-ratio theorem cannot detect even a classical missing-face example.

Enumerate a stellar subdivision of a triangle in boundary(5-simplex),
then add the missing triangle to its 2-skeleton. The result is the complete
2-skeleton on seven vertices. The classical van Kampen--Flores theorem
forbids its embedding in R^4, while f2 <= 4 f1 is easily satisfied.
"""
from itertools import combinations
import json
from pathlib import Path


def subsets(face):
    for size in range(len(face) + 1):
        for subface in combinations(face, size):
            yield frozenset(subface)


def main():
    vertices = set(range(6))
    triangle = frozenset((0, 1, 2))
    apex = 6
    old = {frozenset(c) for size in range(6)
           for c in combinations(vertices, size)}
    new = {face for face in old if not triangle.issubset(face)}
    for face in old:
        if triangle.issubset(face):
            for edge in combinations(triangle, 2):
                new.add(frozenset((face - triangle) | set(edge) | {apex}))
    sphere = {subface for face in new for subface in subsets(face)}
    augmented = {face for face in sphere if len(face) <= 3} | {triangle}
    complete = {frozenset(c) for size in range(4)
                for c in combinations(range(7), size)}
    f1 = sum(len(face) == 2 for face in augmented)
    f2 = sum(len(face) == 3 for face in augmented)
    result = {
        "source": "Boundary of the 5-simplex, stellarly subdivided at triangle {0,1,2}",
        "missing_triangle": sorted(triangle),
        "triangle_absent_in_source": triangle not in sphere,
        "boundary_present": all(triangle - {x} in sphere for x in triangle),
        "augmented_is_complete_2skeleton_on_7_vertices": augmented == complete,
        "f1": f1,
        "f2": f2,
        "face_ratio_bound_rhs": 4 * f1,
        "ratio_bound_satisfied": f2 <= 4 * f1,
        "all_dimensional_formula": (
            "f_d/f_(d-1) = binom(2d+3,d+1)/binom(2d+3,d) "
            "= (d+3)/(d+1) <= d+2 for d>=1"
        ),
    }
    Path(__file__).with_name("FACE_RATIO_COUNTERCHECK.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    if not all(result[key] for key in (
        "triangle_absent_in_source", "boundary_present",
        "augmented_is_complete_2skeleton_on_7_vertices", "ratio_bound_satisfied"
    )) or (f1, f2) != (21, 35):
        raise RuntimeError("Independent construction failed its expected checks")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
