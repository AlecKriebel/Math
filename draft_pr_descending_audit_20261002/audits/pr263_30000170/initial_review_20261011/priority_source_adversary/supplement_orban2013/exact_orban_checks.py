"""Exact checks of potential Orban2013 priority near-matches.

No claim of global optimality or of literature absence is inferred here.
The rounded displayed matrix is treated as the exact rational decimal matrix.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math


def mul(z, w):
    return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])


def square_norm(z):
    return z[0] ** 2 + z[1] ** 2


tau = F("0.2218")
b = (F("0.9467"), F("-0.0355"))
c = (F("0.0276"), F("-0.0740"))
nu = (F(2, 3), F(1, 2))
nu_conj = (nu[0], -nu[1])
fixed_entries = 2 * tau**2 + square_norm((1 - b[0], -b[1]))
distance_printed_sq = fixed_entries + square_norm((nu[0] - c[0], nu[1] - c[1]))
distance_conj_sq = fixed_entries + square_norm((nu_conj[0] - c[0], nu_conj[1] - c[1]))
distance_J_sq = square_norm(nu)
assert distance_J_sq == F(25, 36)
assert distance_printed_sq == F(378168221, 450000000)
assert distance_printed_sq > distance_J_sq
assert distance_conj_sq < distance_J_sq

# Roots of the displayed candidate are -tau +/- sqrt(b*c).
# Exact strict stability follows from |Re sqrt(q)| < tau:
# q.real < tau^2 and q.imag^2 < 4*tau^2*(tau^2-q.real).
q = mul(b, c)
strict_margin = 4 * tau**2 * (tau**2 - q[0]) - q[1] ** 2
assert tau > 0 and q[0] < tau**2 and strict_margin > 0

# Example14 concerns unitary freedom in EIGENVALUE distance. This freedom
# does not preserve coefficient/Frobenius distance to a fixed input A.
# A=diag(-1,1); X1=diag(-1,0); X2=diag(0,-1) is a unitary swap of X1.
frob_X1_sq = F(1)
frob_X2_sq = F(5)
same_spectra = [-1, 0]
eigenvalue_distance_sq = min(
    sum((a - x) ** 2 for a, x in zip([-1, 1], same_spectra)),
    sum((a - x) ** 2 for a, x in zip([-1, 1], reversed(same_spectra))),
)
assert eigenvalue_distance_sq == 1 and frob_X1_sq != frob_X2_sq

out = {
    "schema": "pr263-cold-orban2013-exact-checks-v1",
    "all_assertions_pass": True,
    "Example22_printed_p66": {
        "displayed_input_nu": "2/3+i/2",
        "candidate_offdiagonals": ["0.9467-i0.0355", "0.0276-i0.0740"],
        "printed_distance": "0.8321",
        "actual_displayed_distance_squared_exact": str(distance_printed_sq),
        "actual_displayed_distance": math.sqrt(float(distance_printed_sq)),
        "distance_to_J_squared_exact": str(distance_J_sq),
        "distance_to_J_exact": "5/6",
        "printed_candidate_is_closer_than_J": False,
        "displayed_rational_candidate_strictly_stable": True,
        "stability_margin_exact": str(strict_margin),
        "conjugating_input_distance": math.sqrt(float(distance_conj_sq)),
        "conjugating_input_matches_printed_distance_rounding": True,
        "intended_correction_verified_from_author_source": False,
    },
    "Example14_unitary_eigenvalue_distance": {
        "A": "diag(-1,1)",
        "X1": "diag(-1,0)",
        "X2": "diag(0,-1)",
        "both_eigenvalue_distance_squared": "1",
        "coefficient_Frobenius_distance_squared": ["1", "5"],
        "unitary_freedom_proves_multiple_nearest_coefficients": False,
    },
    "global_minimum_certified": False,
    "all_metrics_statement_certified": False,
    "literature_absence_certified": False,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
Path(__file__).with_name("EXACT_ORBAN_CHECKS.json").write_text(
    json.dumps(out, indent=2) + "\n"
)
print(json.dumps({"all_assertions_pass": True, "output": "EXACT_ORBAN_CHECKS.json"}))
