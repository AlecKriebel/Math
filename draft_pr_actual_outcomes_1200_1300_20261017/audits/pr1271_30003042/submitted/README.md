# Negative resolution of the Schubert gamma filtration conjecture at n = 8

Problem 30003042 / OWR-14213-008. The nonmembership conjecture in Karpenko’s 2016 Oberwolfach contribution is false at n = 8 as a literature-derived consequence of published results.

In the original setup, an odd quadratic form φ has dimension 17 over F and its even Clifford algebra A has maximal index 256. Put K = F(SB(A)). The published generic Spin₁₈ index bound, transported by generic-index divisibility, combines with Karpenko’s explicit 2016 implication to give e₈ ∈ γ⁵K(X_K). The conjecture excludes precisely that membership.

## Read the argument

- [PROOF_RECONSTRUCTION.md](PROOF_RECONSTRUCTION.md) gives the complete setup, generic-index bridge, parameter-specific transfer argument and computational dependencies.
- [AUDIT.md](AUDIT.md) provides the full literature audit, exact field and parameter matching, characteristic scope, invalid-shortcut warnings, source versions and inspection limits.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json) state the accepted dependency-scoped inference and bind it to these exact public artifact bytes.
- [SOURCE_VERIFICATION.json](SOURCE_VERIFICATION.json) records public citations, source hashes and sizes, retrieval history, exact inspection scopes and the final-preprint/journal agreement.
- [EDITORIAL_MAP.json](EDITORIAL_MAP.json) records exact editorial transformations and unchanged mathematical regions.
- [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) lists the closed public artifact set. Its own identity is bound outside the public manifest to avoid self-referential hashing.

## What carries the conclusion

1. The maximal-Clifford-index model exists before passing to the ordinary Severi–Brauer function field. It meets the original hypotheses with dim φ = 17 and ind C₀(φ) = 256 over F.
2. Karpenko’s published generic Spin₁₈ calculation gives index 8 for the fourth orthogonal Grassmannian. [Devyatov–Karpenko–Merkurjev, Proposition 2.1](https://doi.org/10.1017/fms.2021.30) makes the index of the corresponding Grassmannian for this model divide 8. The two meanings of “generic” are not silently identified.
3. Karpenko’s [2016 final preprint](https://sites.ualberta.ca/~karpenko/publ/a16i5.pdf), p. 12, supplies a pointwise implication: transfer gives 8l₃ in topological codimension 13 on a 16-dimensional quadric; an integral identity gives l₀ in that same term; the even-form incidence correspondence shifts by 8, giving e₈ in T⁵; Theorem 4.3 identifies T with γ in the required model.

The decisive computation is published in [Publicacions Matemàtiques 67(2) (2023), 743–756](https://doi.org/10.5565/PUBLMAT6722310). The final author preprint and published §§5–6 agree on the relevant input. The exact-index lower bound is unnecessary here; the upper bound 8 already suffices.

## Credit and verification limits

This is an AI-assisted analysis and reconstruction of published mathematics. It is not a new Spin index theorem or a novelty claim. Our report has not received external human review, journal acceptance, or formal certification. “Acceptance” names the stated inference and artifact-level consistency checks, not peer review.

The underlying index result depends on the paper’s Maple 2021 computation with Chow ring package version 4.0. That computation was not independently rerun. Appendix A was text-inspected; its program and Schubert output are not redistributed. No independent finite Schubert-ring certificate or proof-assistant verification was performed. The cited K-theory, Chow-theory and quadratic-form results remain literature dependencies.

The sources allow arbitrary characteristic with their stated quadratic-form conventions. A characteristic-zero instance alone refutes the universal assertion; no new characteristic-zero restriction or all-forms exact-index claim is introduced here. No claim is made about every n ≥ 8 or the optimal replacement threshold.

This public artifact set contains only authored analysis and verification metadata. It contains no source copies, extracted source text, source images, datasets, raw programs, computational certificates, private personal information or private coordination material.
