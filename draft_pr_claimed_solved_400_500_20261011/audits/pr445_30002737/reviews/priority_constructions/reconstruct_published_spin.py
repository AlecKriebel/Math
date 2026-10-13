#!/usr/bin/env python3
"""Finite algebra/arithmetic checks for the published spin example; no proof search.

The source's integral and its stated numerical error are inputs, not independently
certified by this script. This does not compute candidate diffraction or establish
novelty. All output is written in this script's own audit folder.
"""
from pathlib import Path
from datetime import datetime, timezone
import json, math
BASE = Path(__file__).resolve().parent
W = [[1+0j, 1j], [1+0j, -1+0j]]
C4 = [1+0j, 1j, -1+0j, -1j]
W2 = [[z*z for z in row] for row in W]
gram = [[sum(W2[r][j]*W2[s][j].conjugate() for j in range(2))
         for s in range(2)] for r in range(2)]
assert gram == [[2+0j, 0j], [0j, 2+0j]]
assert len(set(C4)) == 4
assert [z*z for z in C4] == [1+0j, -1+0j, 1+0j, -1+0j]
assert all((z*z) == (z**2) for z in C4)
det_W = W[0][0]*W[1][1] - W[0][1]*W[1][0]
assert det_W == -1-1j
uniform_spin_mean = sum(C4)/4
assert uniform_spin_mean == 0j
# Published Definition 3.5: (g,d) -> (g*W[d,0],0)(g*W[d,1],1).
letters = [(g,d) for g in C4 for d in range(2)]
M = [[0 for _ in letters] for _ in letters]
for j,(g,d) in enumerate(letters):
    for digit in range(2):
        M[letters.index((g*W[d][digit],digit))][j] += 1
P = [[int(i == j) for j in range(8)] for i in range(8)]
primitive_power = None
for n in range(1,17):
    P = [[sum(P[i][k]*M[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
    if all(z > 0 for row in P for z in row):
        primitive_power = n
        break
assert primitive_power is not None
assert all(sum(row) == 2 for row in M)
assert all(sum(M[i][j] for i in range(8)) == 2 for j in range(8))
# Thus the uniform 8-letter distribution is the unique PF frequency vector.
reported_2f12 = 0.688005
reported_error_upper_bound = 0.001
upper_2f12 = reported_2f12 + reported_error_upper_bound
margin = math.log(2) - upper_2f12
assert margin > 0.0041
result = {
 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
 'source': 'Frank–Mañibo arXiv:2108.08642v1 Example 5.4 / DCDS 42 (2022) Example 10',
 'source_version_pdf_sha256': '7e4a477cbfc7c43e3384a5c082d30617418c9fd9b027921103664bd27b390954',
 'full_rank_W': True,
 'determinant_W_real_imag': [int(det_W.real), int(det_W.imag)],
 'primitivity_power_with_all_positive_entries': primitive_power,
 'uniform_letter_frequency': '1/8',
 'uniform_spin_frequency': '1/4',
 'mean_chi1_real_imag': [int(uniform_spin_mean.real), int(uniform_spin_mean.imag)],
 'all_scalar_weights_nonzero': True,
 'support_every_integer': True,
 'suspension_phase_recovery': 'support is Z+t, which determines t mod Z',
 'digit_hull_conjugacy_used': False,
 'aperiodicity_independently_proved': False,
 'aperiodicity_evidence': 'the published Example 10 applies the primitive aperiodic spin theorems; no new aperiodicity proof attempted',
 'character_square_hadamard_check': True,
 'character_square_gram': [[int(z.real) for z in row] for row in gram],
 'physical_spin_alphabet_injective_encoding_count': len(set(C4)),
 'pointwise_square_values_real': [int((z*z).real) for z in C4],
 'table_1_reported_2f12': reported_2f12,
 'source_asserted_error_bound': reported_error_upper_bound,
 'upper_2f12_using_source_error': upper_2f12,
 'log_2': math.log(2),
 'positive_margin_using_source_error': margin,
 'integral_independently_certified': False,
 'numerical_error_independently_certified': False,
 'new_original_proof_search_attempt_count': 0,
 'interpretation': 'Checks the finite character algebra and the published error-margin arithmetic only.'
}
(BASE/'PUBLISHED_SPIN_RECONSTRUCTION_CHECKS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
