"""Independent exact SOS referee check, parsing Lean source rather than JSON receipts.

Only the Python standard library is used. Run from any working directory.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / "bell_lean/Bell/SOSCertificate.lean").read_text()

def section(name, following):
    return source.split(f"def {name} :", 1)[1].split(following, 1)[0]

def rows(text):
    return [[F(x.strip()) for x in r.split(",")]
            for r in re.findall(r"!\[([^\[\]]+)\]", text)]

Q = [[v / 600 for v in row] for row in rows(section("numerator", "def Q"))]
L = rows(section("L", "/-- Positive"))
d, = rows(section("d", "theorem pivot_positive"))
assert len(Q) == len(L) == len(d) == 12
assert all(len(row) == 12 for row in Q + L)
assert all(pivot > 0 for pivot in d)
assert all(Q[i][j] == sum(d[k] * L[i][k] * L[j][k] for k in range(12))
           for i in range(12) for j in range(12))

# Free products of involutions on each party, with parties commuting.
# Normal words retain all order information within each party.
def reduce_word(word):
    result = []
    for letter in word:
        if result and result[-1] == letter:
            result.pop()
        else:
            result.append(letter)
    return tuple(result)

words = [((), ()), ((0,), ()), ((1,), ()), ((2,), ()),
         ((), (0,)), ((), (1,)), ((0,), (0,)), ((0,), (1,)),
         ((1,), (0,)), ((1,), (1,)), ((2,), (0,)), ((2,), (1,))]

def gram_coefficients(matrix):
    result = defaultdict(F)
    for i, (ai, bi) in enumerate(words):
        for j, (aj, bj) in enumerate(words):
            key = (reduce_word(ai[::-1] + aj), reduce_word(bi[::-1] + bj))
            result[key] += matrix[i][j]
    return {key: value for key, value in result.items() if value}

# Expand directly from paper: 289/10 I - 10 CHSH
# - 3/5 [(I+A2)/2] tensor [(I+B0)/2]
# - 4/5 [(I-A2)/2] tensor [(I+B1)/2].
target = {((), ()): F(289, 10) - F(3, 20) - F(1, 5),
          ((0,), (0,)): F(-10), ((0,), (1,)): F(-10),
          ((1,), (0,)): F(-10), ((1,), (1,)): F(10),
          ((2,), ()): -F(3, 20) + F(1, 5),
          ((), (0,)): -F(3, 20), ((), (1,)): -F(1, 5),
          ((2,), (0,)): -F(3, 20), ((2,), (1,)): F(1, 5)}
assert gram_coefficients(Q) == target
corrupt = [row[:] for row in Q]
corrupt[0][0] += F(1, 600)
assert gram_coefficients(corrupt) != target

# Ideal discrimination: fixed score matrices, all singleton/pair optima.
# For pair i,j, optimum is (tr Wi + tr Wj + ||Wi-Wj||_1)/2.
# Here all pair differences have nonpositive determinant. Squared trace norm
# therefore equals tr(D)^2 - 4 det(D), permitting rational exact comparison.
W = [((F(3,10), F(0)), (F(0),F(0))),
     ((F(0),F(0)),(F(0),F(3,10))),
     ((F(1,5),F(1,5)),(F(1,5),F(1,5)))]
pair_data = []
for i in range(3):
    assert W[i][0][0] + W[i][1][1] <= F(3,5)
    for j in range(i+1,3):
        D = [[W[i][a][b]-W[j][a][b] for b in range(2)] for a in range(2)]
        det = D[0][0]*D[1][1] - D[0][1]*D[1][0]
        tr = D[0][0]+D[1][1]
        total = sum(W[k][0][0]+W[k][1][1] for k in (i,j))
        assert det <= 0
        slack = F(6,5)-total
        assert slack >= 0 and tr*tr-4*det <= slack*slack
        pair_data.append({"pair": [i,j], "trace_sum": str(total),
                          "trace_norm_squared": str(tr*tr-4*det)})

report = {"source": "bell_lean/Bell/SOSCertificate.lean",
          "ldl_entries_checked": 144, "strictly_positive_pivots": 12,
          "operator_identity": "Exact equality in free involution algebra on both parties",
          "nonzero_target_coefficients": len(target),
          "corruption_rejected": True,
          "ideal_projective_pair_bounds": pair_data,
          "note": "Independent arithmetic evidence; Lean compilation audited by root agent."}
print(json.dumps(report, indent=2))
