# Section 9 attribution and frame-clarity adjudication — version 1.2.0

This record covers the final targeted Section 9 pass. The theorem scope,
historical releases, and preceding archived version were held fixed. No
external record was modified and no new theorem search was undertaken.

## Proposal-by-proposal disposition

| Proposal | Disposition | Implementation and verification |
|---|---|---|
| Separate direct, transported, and algorithmic claims in the abstract | Accepted | The abstract now credits finite-image and Clifford properties to known Family III results, the enhancement to the displayed matrix, and polynomial-time evaluation to the Galindo--Rowell metric-family algorithm. |
| Split Theorem 1.3 into direct and transported consequences | Accepted | The enhancement, trace, HOMFLYPT, and branched-cover formulas precede the consequences transferred through Theorem 9.4. No formula changed. |
| Add structural signposting at the start of Section 9 | Accepted | The opening paragraph identifies Propositions 9.1--9.3 as direct calculations, Theorem 9.4 as the all-strand comparison, Corollaries 9.5--9.7 as transfers, and Corollary 9.8 as the classical Lickorish--Millett application. |
| Print a standard-frame non-Clifford witness | Accepted | The eight-term identity for `R_K(XIII)R_K^dagger` was checked exactly against the literal five-word matrix and added to Corollary 9.5. The verifier contains the same literal witness and a one-sign mutation. |
| Retain Turaev's enhancement conditions and explain the missing `mu` factor | Accepted | The conditions are unchanged. The text now states that `mu^{tensor n}` is suppressed because `mu=I_4`; the primary-source locator includes Sections 3.1--3.2. |
| Preserve the order and proof roles of Corollaries 9.7 and 9.8 | Accepted | The Galindo--Rowell algorithm remains the complexity proof. No complexity inference is drawn from the branched-cover formula or tower dimension. |
| Add figure-eight and Borromean exact checks | Accepted | Exact literal five-word calculations give `-4` for the closure of `(sigma_1 sigma_2^{-1})^2` and `2` for the closure of `(sigma_1 sigma_2^{-1})^3`; both are frozen in the supported verifier transcript. |
| Keep Galindo--Rowell citations pinned to arXiv v1 | Accepted | The bibliography remains pinned to `arXiv:2608.16865v1`; all theorem, proposition, equation, and section locators retain their audited meaning. |
| Replace Lechner's minimality input or weaken Corollary 1.2 | Rejected as instructed | The established proof and conclusion are unchanged. |
| Remove the verified Wenzl Equation (3.2) pinpoint | Rejected as instructed | The original typeset source had already been checked directly; the pinpoint remains. |
| Change `mathbf1_{2^m}`, compress Section 9, infer complexity from the cover formula, or identify the exact finite image groups | Rejected as instructed | None of these changes was made. |

## Additional source-precision corrections

The same targeted audit made four non-substantive clarifications: it defined
the imported quaternionic-generator notation `s_i`, called `epsilon_n` the
identity-coefficient functional rather than the scaled coefficient trace,
included Turaev Section 3.2 in the link-invariant locator, and qualified the
Galindo--Rowell finite-image citation by its finite-order scalar normalization.

## Freeze gates

The final release record below is completed only after all five supported
routes, every failure-mode test, the clean TeX build, full-page visual review,
internal checksum verification, deterministic source reconstruction, and the
isolated arXiv rebuild have passed on the final bytes.

The human author subsequently supplied the reserved v1.2.0 version DOI
`10.5281/zenodo.22013710`; it was inserted in the final package without
changing the mathematics. Publication remains a human-only gate. The archived
v1.1.3 DOI `10.5281/zenodo.21971507` is not an identifier for this revision.

## Final exact records

- Five-route transcript SHA-256:
  `108233f563373cc2b3e3e9fb4012f7f8ea52fb1149f58c2f6795344bfc5f3064`.
- Standalone braid-and-link transcript SHA-256:
  `9081354712384deef6043ad15c2d6f28f8a4b7988148fc1d246a77b02ae0042a`.
- Final 20-page PDF SHA-256:
  `a769689a4b5b9c48bf675f79d3b80916a7821ad5a8db0b9ec246df460dffb8de`.

All five supported routes and all 32 failure-mode tests passed in the locked
CPython 3.14.6 / SymPy 1.14.0 / mpmath 1.3.0 environment. The final PDF was
rebuilt with Tectonic 0.16.9, all pages were inspected, and no unresolved
reference, overfull box, clipping, collision, or malformed glyph remains.

## Files modified by this targeted pass

```text
README.md
docs/index.html
docs/papers/exceptional-ybe-d4/index.html
docs/papers/exceptional-ybe-d4/paper.pdf
exceptional_ybe_d4/ARXIV_METADATA.md
exceptional_ybe_d4/CHANGELOG_v1.2.0.md
exceptional_ybe_d4/HIGHLIGHTS.txt
exceptional_ybe_d4/MANIFEST.md
exceptional_ybe_d4/README.md
exceptional_ybe_d4/RELEASE_NOTES_v1.2.0.md
exceptional_ybe_d4/RESEARCH_LOG.md
exceptional_ybe_d4/SECTION9_HARDENING_ADJUDICATION_v1.2.0.md
exceptional_ybe_d4/SHA256SUMS
exceptional_ybe_d4/VERIFICATION_ENVIRONMENT.md
exceptional_ybe_d4/braid_link_output.txt
exceptional_ybe_d4/main.tex
exceptional_ybe_d4/output/pdf/exceptional_ybe_d4.pdf
exceptional_ybe_d4/submission/ARXIV_SHA256SUMS
exceptional_ybe_d4/submission/SHA256SUMS
exceptional_ybe_d4/submission/exceptional-ybe-d4-v1.2.0-arxiv.zip
exceptional_ybe_d4/submission/exceptional-ybe-d4-v1.2.0-source.zip
exceptional_ybe_d4/submission/exceptional-ybe-d4-v1.2.0.pdf
exceptional_ybe_d4/test_failure_modes.py
exceptional_ybe_d4/verification_output.txt
exceptional_ybe_d4/verify_braid_link.py
```

No private communication draft changed in this pass, and no private file is a
source-archive member.
