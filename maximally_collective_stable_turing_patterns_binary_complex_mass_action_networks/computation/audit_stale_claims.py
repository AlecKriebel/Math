#!/usr/bin/env python3
"""Reject obsolete numerical/formula claims without misclassifying raw data.

The old release values can legitimately occur as decimal substrings inside newly
computed concentration CSVs.  This audit therefore scans only claim-bearing
text and source files.  Raw simulation provenance is checked structurally by
``audit_numerical_provenance.py`` instead of by substring matching.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

STALE = {
    "old_eta_decimal": "0.1054",
    "old_amplitude_decimal": "1.306",
    "old_amplitude_rounding": "1.311",
    "old_product_ratio": "57/56",
    "old_contrast_coefficient": "1589m",
    "old_affine_denominator": "227m-451",
    "superseded_all_dimensional_endpoint": r"At $L=1/\sqrt{3(m-2)}$",
    "overscoped_minimax": "universal minimax lower bound",
    "overscoped_tradeoff": "universal trade-off",
    "overscoped_global_optimality": "globally optimal",
    "overscoped_stationary_bound": "universal necessary bound",
    "overscoped_cost": "universal cost",
    "biological_cost_language": "biological cost",
    "concentration_price_language": "price paid in concentrations",
    "mixed_certificate_sign_claim": "All listed coefficients are nonnegative",
    "mislabeled_C_polynomial": "polynomial whose sign gives $S_m<0$",
    "old_transformed_left_vector": "q_m(L)=",
    "harmonic_sum_notation_collision": r"\mathcal H_m",
    "modulus_shift_notation_collision": r"\nu=z+1",
    "dynamic_LS_misattribution": "conservation-compatible Lyapunov--Schmidt reduction has",
    "stale_LS_robustness_coefficients": "Lyapunov--Schmidt coefficients",
    "physical_interval_length_collision": r"q_k^2=(k\pi/L)^2",
    "false_stoichiometric_minor": r"2^{m-2}",
    "old_scaled_state_notation": r"z=\mathsf H_m(L)x",
    "old_chain_ratio_notation": r"r_i=\frac{K_{i-1}}{K_i}",
    "old_exceptional_scalar_notation": r"c=\frac{91L}{90}",
    "misdescribed_network_outline": "The dashed outline marks the principal species set",
    "near_threshold_dimension_variable_typo": r"\nu=1+(2-t)\varepsilon",
    "near_threshold_damping_parameter_collision": r"u=1+(2-t)\varepsilon",
    "threshold_omits_flux_parameters": "s_*(H,D)",
    "full_jacobian_misdescribed_as_two_parameter": "explicit two-parameter Jacobian image",
    "awkward_over_realizations_wording": "topology-wide over-realizations theorem",
    "fixed_mass_covector_called_vector": "physical fixed-mass vector becomes",
    "ambiguous_within_family_minimax": r"reduces $\max(\chi_D,\chi_H)$",
    "ambiguous_discussion_minimax": "reduces the larger of the two contrasts",
    "stale_v108_pending_doi": "The exact v1.0.8 DOI is not asserted",
    "stale_v108_pending_release_record": "the v1.0.8 release record carries its version DOI once minted",
    # r_m and ell_m are scalar X_m components.  These tokens used them as
    # whole critical vectors before the notation repair.
    "component_left_used_as_vector": r"\ell_m^T",
    "component_scaled_left_used_as_vector": r"\widetilde\ell_m",
    "component_right_used_as_kernel_vector": r"\operatorname{span}\{r_m",
    "component_left_used_as_cokernel_vector": r"\operatorname{span}\{\ell_m",
    "component_right_used_in_parameter_direction": r"D_mr_m",
    "component_right_used_in_scaled_direction": r"\Delta_m r_m",
    "component_right_used_in_supplement_direction": r"\Delta r_m",
}

# Only prose, theorem, documentation, and generated claim tables are scanned.
# Exact raw simulation CSVs are intentionally excluded; their provenance is
# checked algebraically and by convergence tests in audit_numerical_provenance.py.
ROOTS = [
    ROOT / "manuscript",
    ROOT / "external_audit",
    ROOT / "submission",
    ROOT / "public" / "repository",
    ROOT / "independent_verifier",
    ROOT / "proof_audit",
]
EXTRA = [
    ROOT / "data" / "contrast_table.tex",
    ROOT / "data" / "current_profile_exact.json",
    ROOT / "data" / "branch_amplitudes.csv",
    ROOT / "data" / "simulation_parameters.json",
]
TEXT_SUFFIXES = {".tex", ".md", ".txt", ".json", ".py", ".sh", ".csv", ".cff"}

# These files deliberately contain stale literals as mutation/audit fixtures.
ALLOW_PARTS = {
    ("computation", "tests"),
}
ALLOW_NAMES = {
    "audit_manuscript.py",
    "audit_numerical_provenance.py",
    "audit_pdfs.py",
    "audit_stale_claims.py",
    "stale_claim_audit.txt",
}
SKIP_DIRS = {
    ".git", ".pytest_cache", "__pycache__", "simulations", "simulations_quick",
    "source",  # submission source duplicates are covered by manuscript/source audit
}


def allowed(path: Path) -> bool:
    if path.name in ALLOW_NAMES:
        return True
    rel = path.relative_to(ROOT)
    parts = rel.parts
    return any(all(piece in parts for piece in group) for group in ALLOW_PARTS)


def candidate_files() -> list[Path]:
    out: set[Path] = set()
    for base in ROOTS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
                continue
            out.add(p)
    for p in EXTRA:
        if p.exists():
            out.add(p)
    return sorted(out)


def main() -> int:
    hits: list[tuple[str, Path, int, str]] = []
    scanned = 0
    for path in candidate_files():
        if allowed(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for line_no, line in enumerate(text.splitlines(), 1):
            for label, token in STALE.items():
                if token.lower() in line.lower():
                    hits.append((label, path.relative_to(ROOT), line_no, line.strip()))
            if "rates, equilibrium coordinates" in line.lower():
                lines=text.splitlines()
                context=" ".join(lines[max(0,line_no-3):min(len(lines),line_no+3)])
                if not (
                    "positive-equilibrium realization manifold" in context.lower()
                    or "equilibrium-realization manifold" in context.lower()
                ):
                    hits.append((
                        "unqualified_rate_equilibrium_perturbation",
                        path.relative_to(ROOT),line_no,line.strip(),
                    ))
    if hits:
        for label, path, line_no, line in hits:
            print(f"STALE {label}: {path}:{line_no}: {line}")
        return 1
    print(f"STALE_CLAIM_AUDIT_PASS files={scanned}")
    print("RAW_SIMULATION_VALUES_CLASSIFIED_CURRENT_BY_STRUCTURAL_PROVENANCE_AUDIT")
    print("MUTATION_FIXTURES_CLASSIFIED_HISTORICAL_BUT_NECESSARY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
