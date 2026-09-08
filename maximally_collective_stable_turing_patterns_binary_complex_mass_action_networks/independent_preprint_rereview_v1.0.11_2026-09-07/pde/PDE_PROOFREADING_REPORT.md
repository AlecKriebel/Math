# Focused nonlinear/PDE proofreading: v1.0.11

Target: 137ffa9f1a340f621651395ad0236cf1bdadb51c.
Comparison: v1.0.10, 953c836a12b9d9d474521feb4a96e218c1155203.

**No actionable finding. The nonlinear/PDE display repairs preserve the mathematical content.**

This is a focused proofreading conclusion. It does not replace the parent referee's PDF inspection, release verification, or certificate-reader audit. The unchanged broad algebraic campaigns were not rerun.

## Repaired displays

- In Supplement S10, the SIADS branch splits the operator and the two spaces into separate displays. The operator remains \(L_0=A_m+D_m\partial_{\xi\xi}:X_c\to Y_c\); \(X_c\) retains Neumann \(H^2\) regularity and the zero integrated-mass constraint; \(Y_c\) retains \(L^2\) regularity and the same constraint. No covector, transpose, sign, integration limit, or domain was changed. The surrounding cosine-mode, Fredholm, high-frequency, and nonlinear-stability arguments remain consistent with these definitions.
- In the reference-coefficient sign display, the SIADS branch now displays \(P_R(m)\) and the rational definition of \(R_m\) separately. Every integer coefficient, alternating sign, exponent, parameter, and denominator factor agrees with the canonical branch and v1.0.10. The adjoining conclusion still uses the positive shifted coefficients and positive denominator for \(m\ge3\); the negative external factor relevant to \(C_m\) remains attached to that separate coefficient. There is no change to the cubic-sign argument.
- The SIADS verifier-command wrap retains the complete directory and filename. The table-spacing adjustment is conditional on SIADS review mode and changes no table entry. Neither introduces a new mathematical claim or condition.

## Checkable evidence

The included proofread_display_equivalence.py passes and writes DISPLAY_EQUIVALENCE_RESULTS.json. It:

1. Confirms the audited source snapshot matches the target commit.
2. Selects the canonical TeX branches and establishes that the main nonlinear/PDE body and Supplement S5–S10 are unchanged apart from whitespace.
3. Compares the mathematical tokens of both repaired displays across the journal and canonical branches, removing only their explicit layout commands and sentence punctuation.
4. Confirms the canonical sign table is unchanged apart from whitespace.
5. Checks all three packaged main/supplement source pairs against the canonical text, allowing only the intended relative paths for local figures and data.

The displayed expressions were also read in context rather than accepted solely from token equality. In particular, the split function-space display still places the integral constraint on the spatial mean, not pointwise concentrations, and the sign display still has the correct domain and rational denominator.

Run the focused check from the repository root:

    .venv/bin/python maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks/independent_preprint_rereview_v1.0.11_2026-09-07/pde/proofread_display_equivalence.py

The script uses only the Python standard library and reads the two Git objects and supplied snapshot. It does not modify manuscript source, generate publication assets, or import the submitted verifiers.

No new missing assumption, indexing error, sign error, or claim/proof inconsistency was found in this lane. Scientific acceptance within the nonlinear/PDE scope is unchanged.
