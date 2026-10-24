# Homological/analytic family — consolidated report

**Outcome:** no residual implication and no counterexample proved. Two precisely specified filters are exhausted for all four pairs, with proofs and exact arithmetic certificates. These are deductions from established arrangement results, not promoted as novel theorems.

## Verified mechanisms and status

| Mechanism | Verified result | Status / exact gap |
|---|---|---|
| Reduced L2 cohomology of Q_T | One positive degree d=rank(T)−1 for every type | **Exhausted as a support filter.** Numerical dimensions differ but are not claimed QI invariants. |
| L2 cohomology of P_T | All degrees vanish because P_T=Q_T×Z | **Exhausted as a support filter.** |
| Full-Laplacian heat decay of P_T in top degrees | Exact product identity; Θ_d and Θ_(d+1) are asymptotic to c_T/√(4πt) | **Exhausted as an exponent filter.** Both normalized exponents are 1 in every residual type, even without spectral gaps for Q_T. |
| Compact-support/coarse cohomology groups and cup-product rings of EQ_T | Countably infinite free abelian only in degree d; multiplication zero | **Exhausted as a graded-ring filter.** All rank-matched pairs agree. |
| Lower-degree spectral tails of Q_T | Not computed by reduced L2 vanishing | **Unresolved.** Need actual spectral estimates and a valid nonamenable QI-invariance mechanism. |
| Dualizing module with group action / arrangement cohomology algebra | Ordinary quotient cohomology and module action can contain extra type data | **Blocked in this form.** Bare QI supplies neither ordinary cohomology preservation nor an equivariant group isomorphism. |

## Checkable artifacts

- SPECTRAL_FILTER.md: exact heat-trace tensor identity, elementary asymptotic proof, convention/indexing safeguards, and failed-filter consequence.
- COARSE_COHOMOLOGY_FILTER.md: rank-ℵ0 argument from the ambient-flat term of the repaired diagonal spectral sequence; distinction between abelian and group-ring rank.
- PROFILE_TABLE.md: eight exact values and the H4 root-selection certificate.
- compute_profiles.py and profiles.json: standard-library exact arithmetic; matrices, exact orders, cyclotomic characteristic-polynomial checks, Poincare coefficients, and Euler products. The run completed successfully for all eight types.
- sources/SOURCE_MANIFEST.json: five cached primary PDFs with retrieval timestamps, SHA-256 hashes, exact theorem uses, and the visually checked Brieskorn formula page.
- RESEARCH_LOG.md: timestamped checkpoints and estimates.

## Validation received and source cautions

The independent scope adversary reported PASS on the exact product calculation and its top-degree consequences, checking Koszul cancellation, constants, dominated convergence, the absence of a spectral-gap hypothesis, the decone center, finite models, and boundary-map indexing. The root researcher separately checked the spectral proof and the ambient-flat poset orientation. The compact-support proof was strengthened by checking DJLO Theorem 1 and Remark 6 directly.

The local finite-abelian-rank phrase in the 2015 repair is explicitly excluded; a Z×F2 example shows it cannot be read literally. Only concentration/freeness and the ambient-point term are used. The DJL/DJLO spectral-sequence arguments are used together with the 2015 repair. Sauer's amenable Novikov–Shubin theorem is not imported for these nonamenable groups. No spectral gap is inferred from zero reduced cohomology, and no numerical L2 or ordinary Betti number is treated as a QI invariant.

**Strongest verified result:** the two failure filters above. **Exact discovery gap:** still establish or refute the four residual quasi-isometry⇒commensurability implications. Full-goal discovery estimate remains **5%**. This family's bounded filter-audit deliverable is **100%** complete, subject to the root researcher's final independent review. No Git operation, publication, outreach, or immutable release was performed.
