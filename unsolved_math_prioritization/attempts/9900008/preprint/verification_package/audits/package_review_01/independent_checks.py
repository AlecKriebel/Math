"""Independent exact finite diagnostics; the universal proof is analytic."""
from fractions import Fraction as F
import json


def require(condition):
    if not condition:
        raise ValueError("independent finite diagnostic failed")


result = {
    "method": "Independent rational residue enumeration and half-open vertical-window enumeration; diagnostic only",
    "grids": [],
}
for m in (2, 4, 8, 16, 32, 64, 128, 256):
    preserving = []
    for i in range(m):
        for j in range(m):
            received = {}
            for residue, weight in ((i, 1), ((m // 2 + j) % m, 2)):
                received[residue] = received.get(residue, 0) + weight
            if received == {0: 1, m // 2: 2}:
                preserving.append([i, j])
    require(preserving == [[0, 0]])
    for k in range(m):
        u = F(k, m)
        light = [F(n) for n in range(-2, 3) if -u <= n < 1 - u]
        heavy = [F(n) + F(1, 2) for n in range(-2, 3)
                 if -u <= F(n) + F(1, 2) < 1 - u]
        require(len(light) == len(heavy) == 1)
    result["grids"].append({
        "m": m, "tested_residue_pairs": m * m,
        "preserving_pairs": preserving, "window_phases": m,
        "window_mass": 3, "heavy_probability": "2/3",
    })
require((F(1) * 0 + F(2) * F(1, 2), F(1) * 1 + F(2) * F(1, 2)) == (1, 2))
result["markov_matrix"] = [["0", "1"], ["1/2", "1/2"]]
result["weight_row_times_matrix"] = ["1", "2"]
print(json.dumps(result, indent=2))
