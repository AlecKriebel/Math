# Dependency ledger — complete candidate

| ID | Exact necessary assertion | Source and checkable basis | Status and boundary |
|---|---|---|---|
| D1 | Hilb A=∏(1+t+⋯+t^(d_i−1)); perfect A_j×A_(c−j)→A_c; symmetric unimodal Hilbert function | Regular-sequence exact sequences, CI Koszul duality, explicit bounded-product symmetric chains in manuscript | Direct downstream derivation checked; Gorenstein duality is standard CI theory |
| D2 | Every homogeneous overideal of a full regular sequence of degrees≥2 over C has a monomial pure-power overideal with the same entire quotient Hilbert function | OpenAI companion Theorem1.1/Corollary1.2; exact pinned TeX/PDF hash inventory; notes/companion_audit.md, picard_subaudit.md and root_dependency_check.md | Central construction scrutinized, no material gap identified; substantial external unrefereed theorem, not formalized; integrated fresh review pending |
| D3 | D2 applies over every characteristic-zero field | Finite coefficient field over Q embeds in C; faithful flatness and identical monomial exponents; manuscript Section2; upstream Corollary1.3 | Independently checked. No embedding of arbitrary k into C assumed; no partial-length Artinian reduction needed |
| D4 | The exact fixed-CI EGH hypothesis implies matching and then Sperner | HWW Theorem11, arXiv1601.06928v1 and DOI10.1090/proc/13347; independently reproduced in notes/downstream_proof.md and manuscript | Sound known mechanism; publisher PDF inaccessible, arXiv full text checked; no Betti comparison needed |
| D5 | μ(I)≤μ(in_m I) for arbitrary ideals; linear elimination preserves target; μ and Hilbert layers preserved by field extension | Finite associated grading with m in(I)⊂in(mI); graded coordinate elimination; tensor quotient identity | Direct proofs checked with correct inequality; empty/all-linear/unit-ideal boundaries explicit |

D2 is the only novel upstream breakthrough used. Both family200 manuscript-specific citations are preserved in manuscript/references.bib. LPP filtered extraction was independently checked; any later Betti-only flaw would not affect the required HF theorem. Genuine division is essential, as the matrix-only counterexample in lpp_audit.md shows.

No applicable lean/docs/200.md, relevant catalogue entry or actual declaration was found. Unrelated Lean names containing200 are excluded. Neither compilation nor existence of a Lean directory is treated as proof verification. Source clone remained read-only; cosmetic metadata wrappers were used only in pinned local copies for source builds.

Audit scope and limits are retained in the individual dated reports. No unsupported equivalent theorem is used as a substitute for the EGH proof. Publication readiness requires fresh review of the integrated candidate and exact files.
