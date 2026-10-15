#!/usr/bin/env python3
"""Own-code finite controls for a source-classification audit, never a certificate.

Only source mathematics is reconstructed. No other review's code is imported.
The floating midpoint replay has NO quadrature or rounding error certificate.
"""
from fractions import Fraction
from pathlib import Path
import cmath
import datetime
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
ROOT = CASE.parents[2]
W_EXP = ((0, 1), (0, 2))
LETTERS = [(g, d) for g in range(4) for d in range(2)]

def subst(a):
    g, d = a
    return [((g + W_EXP[d][r]) % 4, r) for r in range(2)]

def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def square_letter(a):
    g, d = a
    return (g % 2, d)

def subst_squared(a):
    g, d = a
    return [((g + W_EXP[d][r]) % 2, r) for r in range(2)]

def numeric_integrals(grid):
    """Display-order cocycle B(x)B(2x)..., using midpoint quadrature."""
    totals = {n: 0.0 for n in (10, 11, 12, 13)}
    for j in range(grid):
        x = (j + 0.5) / grid
        a, b, c, d = 1+0j, 0j, 0j, 1+0j
        for n in range(1, 14):
            z = cmath.exp(2j * math.pi * ((2 ** (n-1) * x) % 1))
            a, b, c, d = a + b*z, 1j*a - b*z, c + d*z, 1j*c - d*z
            if n in totals:
                norm2 = abs(a)**2 + abs(b)**2 + abs(c)**2 + abs(d)**2
                totals[n] += math.log(norm2)/n
    return {str(n): totals[n]/grid for n in totals}

def main():
    outputs = {}
    incidence = [[0 for _ in LETTERS] for _ in LETTERS]
    for j, a in enumerate(LETTERS):
        for b in subst(a):
            incidence[LETTERS.index(b)][j] += 1
    powers = []
    current = [[int(i == j) for j in range(8)] for i in range(8)]
    for n in range(1, 11):
        current = matmul(current, incidence)
        powers.append({"power": n, "minimum": min(map(min, current)),
                       "maximum": max(map(max, current))})
        if powers[-1]["minimum"] > 0:
            break
    assert powers[-1]["minimum"] > 0
    outputs["incidence_matrix_child_rows_parent_columns"] = incidence
    outputs["primitivity_checks"] = powers
    outputs["squared_substitution"] = {
        str(a): [list(b) for b in subst_squared(a)]
        for a in [(g, d) for g in range(2) for d in range(2)]}
    outputs["square_intertwines_substitution_all_8_letters"] = all(
        [square_letter(b) for b in subst(a)] == subst_squared(square_letter(a))
        for a in LETTERS)
    assert outputs["square_intertwines_substitution_all_8_letters"]
    w = [[1, 1j], [1, -1]]
    w2 = [[1, -1], [1, 1]]
    outputs["chi2_gram_matrix"] = matmul(w2, [[1,1],[-1,1]])
    assert outputs["chi2_gram_matrix"] == [[2,0],[0,2]]
    diagonal = [[1,0],[0,1j]]
    inverse = [[1,0],[0,-1j]]
    similarity = matmul(matmul(diagonal, w), inverse)
    assert similarity == [[1,1],[1j,-1]]
    outputs["orientation_guard"] = {
        "identity": "W^T = diag(1,i) W diag(1,-i)",
        "exact_check_passed": True,
        "consequence": "diag(1,z) W and diag(1,z) W^T have unitarily conjugate cocycles"}
    group = (1, 1j, -1, -1j)
    weights = [3 + ((1+2j)*g).real for g in group]
    assert weights == [4,1,2,5]
    assert len(set(weights)) == 4
    lookup = {4:1, 1:-1, 2:1, 5:-1}
    assert all(lookup[wgt] == g*g for wgt,g in zip(weights,group))
    assert all(wgt == 3 + (1+2j)*g/2 + (1-2j)*g**3/2
               for wgt,g in zip(weights,group))
    outputs["positive_real_specialization"] = {
        "status": "reviewer-verified direct inference from published character-sector results; not a literal prior-paper formula",
        "group_order": ["1","i","-1","-i"],
        "weights": weights,
        "injective": True,
        "minimum_weight": min(weights),
        "squared_spin_lookup": lookup,
        "character_decomposition_checked": True,
        "mean": str(sum(Fraction(wgt) for wgt in weights)/4),
        "mean_square": str(sum(Fraction(wgt)**2 for wgt in weights)/4),
        "singular_spectral_measure_formula": "9 delta_0 + (5/4) sigma_F1 + (5/4) sigma_F3",
        "chi3_cocycle_reflection": "Bchi3^(N)(x) = conjugate(Bchi1^(N)(-x)); identical Frobenius integrals"}
    # Prolongable fixed ray: every substitution first column leaves g unchanged.
    ray = [(0,0)]
    for _ in range(16):
        ray = [b for a in ray for b in subst(a)]
    q = [(-1)**(g % 2) for g,d in ray]
    recurrences = all(q[2*n] == q[n] and
                      q[2*n+1] == (-1)**(n+1)*q[n]
                      for n in range(len(q)//2))
    assert recurrences
    outputs["fixed_ray_length"] = len(ray)
    outputs["squared_fixed_ray_recursion_checked"] = recurrences
    outputs["aperiodicity_analytic_argument"] = (
        "An eventual period 2r implies eventual period r using q(2n)=q(n). "
        "Reduce to an odd p. Apply q(2n+1)=(-1)^(n+1)q(n) at n and n+p: "
        "periodicity equates both q(n) and q(2n+1), but the sign flips, impossible. "
        "Primitive minimality excludes any periodic point in the squared spin factor "
        "and thus in its parent. This does not invoke the chi-unitary spectral theorem.")
    outputs["numeric_midpoint_replay"] = {
        "certified": False,
        "cocycle_order": "B(x)B(2x)...B(2^(N-1)x)",
        "normalization": "(1/N) integral_0^1 log(norm_F(B^(N)(x))^2) dx",
        "grids": {str(g): numeric_integrals(g) for g in (4096,16384,65536)},
        "error_bound": None,
        "meaning": "diagnostic only; neither convergence across grids nor IEEE arithmetic certifies the source error claim"}
    lower_log2 = 2 * sum(Fraction(1, (2*k+1)*3**(2*k+1)) for k in range(3))
    conservative_source_upper = Fraction(689006, 1000000)
    assert lower_log2 > conservative_source_upper
    outputs["historical_error_budget_implication"] = {
        "conditional_on_source_error_assertion": True,
        "reported_value": "0.688005",
        "reported_error_less_than": "0.001",
        "conservative_upper_including_rounding": str(conservative_source_upper),
        "exact_lower_bound_log2": str(lower_log2),
        "exact_margin": str(lower_log2-conservative_source_upper),
        "independent_integral_error_certificate": False}
    frozen = CASE / "source_snapshot/unsolved_math_prioritization/attempts/30002737"
    paths = list(sorted(frozen.rglob('*')))
    outputs["frozen_input_bindings"] = [{
        "path": str(p.relative_to(ROOT)),
        "bytes": p.stat().st_size,
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in paths if p.is_file()]
    primary = [
        ("original_target", CASE / "private_sources/owr2014.pdf"),
        ("precursor", CASE / "private_sources/van_enter2013v2.pdf"),
        ("published_spin", CASE / "private_sources/root_priority/spin_2022_published.pdf")]
    outputs["primary_source_bindings"] = [{
        "role": role, "path": str(p.relative_to(ROOT)),
        "bytes": p.stat().st_size,
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        for role,p in primary]
    outputs["at_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (HERE / "CONTROL_RESULTS.json").write_text(json.dumps(outputs, indent=2)+"\n")
    print(json.dumps({"primitivity": powers[-1],
                      "square_check": outputs["square_intertwines_substitution_all_8_letters"],
                      "recurrence_check": recurrences,
                      "numeric_replay": outputs["numeric_midpoint_replay"]["grids"],
                      "certified_integral": False}, indent=2))

if __name__ == '__main__':
    main()
