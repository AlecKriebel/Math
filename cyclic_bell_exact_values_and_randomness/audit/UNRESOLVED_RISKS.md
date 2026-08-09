# Unresolved risks

Audit date: 2026-08-08

The central mathematical verdict is positive.  The following items remain release or specialist-review risks; none authorizes a stronger claim than the claims ledger.

| Priority | Risk | Present evidence | Required closure |
|---|---|---|---|
| High | Convention drift could reintroduce a missing adjoint or conjugation. | The source has a nearby main-text/appendix Bob-adjoint discrepancy and a briefly omitted Alice conjugation in the second-family discussion.  The merged formulas currently use one explicit convention and the SOS-annihilating \(A_\ell=\overline{D_\ell}\). | Ensure every verifier and web summary uses the same convention; retain Appendix `app:conventions`; run the unified reproduction command after final edits. |
| High | The second-family all-dimensional phases are algebraically dense and easy to damage during copyediting. | The geometric sum, parity exponent, and exact \(d=4\) independent replay currently agree. | Freeze equations `eq:lambda`, `eq:second-A`, and `eq:Fourier-compression`; rerun both all-dimensional regressions and the independent exact \(d=4\) SOS check after any edit. |
| Medium | Endpoint robustness could again be read with an exact-deficit rather than tolerance convention. | The merged corollary now explicitly quantifies strategies whose deficit is **at most** \(\varepsilon\), making the proof valid. | Preserve that sentence and mirror it exactly in abstract, website, and reviewer summary. |
| Medium | Scalar equality may be mistaken for a full equality-face classification. | The merged text explicitly restricts vector conclusions and calls the permutation theorem sufficient. | Preserve these boundaries in theorem summaries, claims tables, and website copy; seek specialist review of support/invariance language. |
| Medium | The \(q_c\) theorem may be presented as numerically validated. | Its proof is analytic in commuting von Neumann algebras; finite tests are only type-I direct sums. | The verification report must label \(q_c\) as analytic and never infer it from sampled matrices. |
| Medium | The guessing bound may be mistaken for the exact worst case. | The text defines a supremum and states only a lower bound. | Keep “lower bound” and “not worst possible” adjacent to every displayed value-only conclusion. |
| Medium | Priority may have shifted in a later source version or contemporaneous preprint. | A dated primary-source audit is being maintained separately. | Freeze claims only after the final search log; revise manuscript wording immediately if any priority conflict appears. |
| Medium | Verification implementations are not fully independent. | The exact \(d=4\) certificate has two routes, and the canonical merged verifier adds a genuine nonunitary-partial-isometry case.  The standalone exact-value unit test still imports its primary verifier. | Preserve both exact \(d=4\) routes and the merged hostile suite.  Do not present any finite replay as proving the analytic all-dimensional or commuting-operator theorem. |
| Medium | Scoped setting obstructions could be promoted rhetorically into a universal no-go claim. | CBR-020--022 are explicitly narrow; only CBR-019 is universal. | Keep secondary setting results in the appendix and reproduce their hypotheses in summaries. |
| Release | The manuscript may change after this audit. | The audit is keyed to the 2026-08-08 merged `main.tex`. | Rerun theorem-label, reference, PDF, and verifier checks after final content freeze; review the diff against this claims ledger. |
| Release | Website redirects, historical artifact URLs, hashes, and sitemap may fail even if the mathematics passes. | These are outside the analytic review. | Run the canonical link checker against all four routes, all three historical PDFs, source links, `noindex,follow`, canonical tags, and sitemap membership. |
| Release | No external specialist has reviewed the manuscript. | This is a fresh internal adversarial reconstruction only. | Describe the paper as unrefereed and present the focused questions; do not imply endorsement or collaboration. |

## Closed during this audit

- The polar proof does not require a unitary extension of the partial isometry and has no inverse-on-kernel gap.
- The commuting-operator upper bound uses only cross-party commutation; no tensor-product step was found.
- The first-family final-two swap has a strictly nonzero lag-two autocorrelation for every \(d\geq4\).
- The second-family candidate is tied to a complete SOS upper bound, so saturation is not inferred merely from selected vanishing residuals.
- The robustness statement now uses deficit **at most** \(\varepsilon\), resolving the earlier logical ambiguity.
- `CHANGELOG.md` and `MERGE_REPORT.md` now record the deliberate omission and preservation paths for the valid historical equal-supported-multiplicity and private-MUB composition results; neither was silently dropped.
