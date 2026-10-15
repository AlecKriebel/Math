#!/usr/bin/env python3
"""Exact parameter comparison only; this does not compute any period space."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[1]
CANDIDATE = [(F(a), F(b)) for a, b in [(4, 6), (2, 5), (3, 3), (1, 4), (0, 2)]]
EXAMPLES = {
    "OWR2011_p734_Minguez_noninduced_example": [(F(1), F(2)), (F(-1), F(1)), (F(0), F(0))],
    "LM2016_p16_Leclerc_square_reducible_example": [(F(3), F(4)), (F(1), F(3)), (F(2), F(2)), (F(0), F(1))],
    "MOS2017_Example9_4_Langlands": [(F(4), F(4)), (F(3), F(3)), (F(3), F(3)), (F(2), F(2)), (F(1), F(2)), (F(0), F(1))],
    "MOS2017_Example9_4_Zelevinsky_dual": [(F(2), F(3)), (F(1), F(4)), (F(0), F(1))],
    "GMM2016_2018_Definition8_1": [(F(1, 2), F(3, 2)), (F(-1, 2), F(7, 2)), (F(-3, 2), F(-1, 2)), (F(-5, 2), F(5, 2)), (F(-7, 2), F(1, 2))],
    "Sharma2026_Theorem8_1": [(F(0), F(0)), (F(0), F(1)), (F(0), F(1)), (F(1), F(1)), (F(1), F(2))],
}

def dual(m):
    return [(-b, -a) for a, b in m]

def shift(m, c):
    return [(a + c, b + c) for a, b in m]

def canonical(m):
    c = min(a for a, _ in m)
    return sorted(shift(m, -c))

def invariant(m):
    lengths = [b - a + 1 for a, b in m]
    assert all(x.denominator == 1 and x > 0 for x in lengths)
    return {
        "number_of_segments": len(m),
        "total_degree_on_character_line": int(sum(lengths)),
        "segment_length_multiset": sorted(map(int, lengths)),
        "duplicate_multiplicities": sorted(Counter(m).values()),
        "translation_canonical_multiset": [[str(a), str(b)] for a, b in canonical(m)],
        "dual_translation_canonical_multiset": [[str(a), str(b)] for a, b in canonical(dual(m))],
    }

def equivalent(m, n):
    # A common real translation that equates integer-spaced endpoint sets is
    # determined by the difference of their minimal beginnings. Reordering is
    # removed by sorting; both possible contragredient orientations are checked.
    return canonical(m) in [canonical(n), canonical(dual(n))]

rows = []
for name, example in EXAMPLES.items():
    rows.append({"source_example": name, "invariants": invariant(example),
                 "equivalent_under_translation_dual_and_reordering": equivalent(CANDIDATE, example)})
assert not any(row["equivalent_under_translation_dual_and_reordering"] for row in rows)
assert sorted(shift(dual(CANDIDATE), F(6))) == sorted(CANDIDATE)
assert sorted(dual(shift(CANDIDATE, F(-3)))) == sorted(shift(CANDIDATE, F(-3)))
out = {
    "purpose": "Parameter equivalence and priority screening, not mathematical acceptance or novelty proof",
    "candidate": invariant(CANDIDATE),
    "candidate_centered_by_minus_3": [[str(a), str(b)] for a, b in sorted(shift(CANDIDATE, F(-3)))],
    "candidate_contragredient_plus_6_equals_candidate": True,
    "examples": rows,
    "uninspected_Luo_Zha": {
        "parameter_equivalence": "UNKNOWN",
        "unitary_period_consequence": "UNKNOWN",
        "reason": "No complete primary body retrieved; no parameters can be extracted responsibly from abstract metadata",
    },
}
(BASE / "PARAMETER_COMPARISON.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
