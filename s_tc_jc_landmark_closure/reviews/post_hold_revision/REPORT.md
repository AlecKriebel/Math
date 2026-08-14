# Post-HOLD adversarial revision report

Status: **VERIFIED — REPAIRED, INDEPENDENT ADVERSARIAL RE-REVIEW PASSED**

The external adversarial report supplied on 2026-08-14 has SHA-256
`106155f3e918f343ea79091d250a44edbc870f2f1c3afdf9179d396a4535da9e`.
The Figure 4 screenshot has SHA-256
`c3ef4e4a5eae3fd4ba53b7ce92fce1be8ef8d8a303b7e0ad2a5fd245da9ff9a5`.

## Disposition of findings

| Finding | Disposition | Active repair |
|---|---|---|
| Primitive-core degree count | **VALID LOAD-BEARING DEFECT; REPAIRED** | The false `3v<=2e` step was removed.  The proof now uses `sum(deg_B-2)=2(r-1)` on the unsuppressed biconnected subcubic blob, then records source/sink events and ordered port words. |
| Public repository mismatch | **VALID RELEASE DEFECT; REPAIR PENDING FINAL TAG** | The manuscript now names immutable tag `stc-jc-sharp-boundary-v1.0.0`; the tag is created and pushed only after all revised bytes pass clean replay. |
| Crossing-quartet reduction | **VALID LOAD-BEARING OMISSION; REPAIRED** | A graph-theoretic lemma now exhausts one-active and two-active quartet marginals and states the submatrix rank transfer. |
| Complete bridge fibre | **EXPOSITION GAP; HARDENED** | The manuscript now gives sector scales, the leaf-peeling induction, the incidence assignment, anchor exponent matrices, stabilizer exclusion, and no-holonomy argument. |
| Root reduction | **EXPOSITION GAP; HARDENED** | The proof now treats directed cycles, retained reticulation arrowheads, literal one-step suppression, LSA validity, parent complementation, and open edge splitting. |
| Omega rank-nine upper bound | **EXPOSITION GAP; HARDENED AND EXACTLY REPLAYED** | Edge/parameter order, the `14 x 10` core Jacobian, rank six, determinant `-723/8589934592`, and the Euler tangent identity are explicit.  `omega_audit/independent/verify_omega_rank_readability.py` regenerates them. |
| Observational relations and blob definition | **EDITORIAL AMBIGUITY; REPAIRED** | The source-regular neighborhood definition and maximal nontrivial biconnected-block definition are now explicit. |
| Real-algebraic citations | **EDITORIAL GAP; REPAIRED** | Exact Bochnak--Coste--Roy proposition/theorem numbers replace broad section citations. |
| Authorship and AI disclosure | **VALID DISCLOSURE ISSUE; REPAIRED** | The text no longer claims sole implementation/validation and explains that an independent replay is code-independent, not a human review. |
| Figure 4 overlap | **VALID VISUAL DEFECT; REPAIRED** | Panel spacing was increased and the figure rescaled; the revised page is included in the final two-renderer audit. |
| ORCID in title block | **OPTIONAL STYLE CHOICE; REMOVED** | ORCID remains in bioRxiv metadata and upload instructions, but not in the printed author block. |

No reported issue supplied a counterexample to the classification theorem or
the Omega/Theta sharpness theorems.  The submission HOLD is lifted only after
the revised clean-clone, mutation, PDF, archive, and public-tag gates pass.

## Independent theorem-level re-review

A code-independent adversarial reviewer first classified the primitive-core
degree count and crossing-quartet omission as the only two load-bearing
defects among the mathematical findings.  After the revisions, the same
reviewer re-read the current source and returned `PASS`: the unsuppressed
degree-excess proof correctly retains source/sink events and port words; the
quartet alternatives are exhaustive and rank transfers through a genuine
Fourier-flattening submatrix; and no new false statement was found in the
expanded bridge, root, Omega, observational-relation, or blob passages.

This was an AI-assisted adversarial mathematical review, not a human
specialist review.  The clean replay and public-tag conditions are tracked by
the release envelope rather than asserted by this pre-seal report.
