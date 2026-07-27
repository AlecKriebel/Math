# Research log

All timestamps use America/Los_Angeles.

## 2026-07-26

- **17:44 PDT - Independent release audit opened (10% complete).**
  Imported the proposed counterexample package into a dedicated worktree based
  on public `main`. The supplied SHA-256 manifest verifies without error.
  Opened separate first-principles audits of the all-dimensional cycle
  construction, the claimed structure theorem for every maximizer, and the
  exact/numerical verification package. No mathematical claim has yet been
  accepted for publication, and no outside researcher has been contacted by
  this counterexample workstream.

- **18:12 PDT - Core theorem independently validated and simplified (55% complete).**
  Separate proof audits confirmed the all-dimensional counterexample,
  probability normalization, phase conventions, exact maximality, Fourier
  autocorrelation, and guessing gap. Replaced the original
  permutation-plus-gauge presentation by the direct sparse construction
  `A0=X`, `A1=X*diag(z_kappa)`. Replaced the dense `d=4` witness by monomial
  weight exponents over `Q(zeta_16)`. The exact verifier now reads the JSON
  certificate and independently reconstructs the observables, Bell value,
  projector probabilities, Fourier probabilities, uniform marginals, and
  strict gap. Numerical regressions pass for canonical dimensions 2 through
  12 and nonuniform dimensions 4 through 12.

- **18:12 PDT - Structural appendix repaired (65% complete).**
  The equal-multiplicity conclusion survived review, but two proof gaps were
  found and corrected: cancellation of a possibly singular polar factor now
  uses its final support range, and spectral projections of
  `U=A0^dagger A1` are introduced only after proving that `U` preserves the
  state-supported Alice space. The result is labeled supplementary and is
  restricted to finite-dimensional exact maximizers of the augmented
  functional.

- **18:12 PDT - Source and novelty audit checkpoint (70% complete).**
  Confirmed from arXiv v3 that Conjecture 2 asserts maximal global randomness,
  while Appendix B.1 fixes the full canonical behavior rather than only the
  Bell maximum. Recorded the preprint's apparent extra-factor-`d`
  normalization inconsistency and used the displayed operator plus Eq. (17)
  as authoritative. Related same-day papers concern different protocols or a
  three-outcome robustness study. No equivalent public counterexample was
  found in the targeted search; absolute novelty remains unestablished. No
  outside researcher was contacted as part of this audit.

- **18:26 PDT - Manuscript, exact package, and presentation audit complete
  (90% complete).**
  A second adversarial proof pass found and corrected a missing plus sign,
  one missing operator-sum plus sign, unnumbered equation labels, and an
  implicit Fourier constant cancellation. The rewritten ten-page manuscript
  now compiles without layout or reference warnings. Every PDF page was
  rendered to PNG and inspected; the sparse exponent table was widened for
  readability. The local paper page and homepage were rendered in a browser,
  MathJax and navigation were checked, one raw second-display delimiter was
  corrected, and the page, PDF, homepage, and sitemap return the expected
  content types. Exact and numerical suites pass. Publication hashes and the
  public timestamp remain to be frozen.

- **18:34 PDT - Public release verified (100% complete).**
  Released the complete note, source package, exact certificate, and paper
  page to public `main` in commit
  `e188fca8fb6f19a30e5c18363cf9b78ddc5ed312`. GitHub Pages successfully built
  and deployed that exact revision. Retrieved the live page, source path, and
  ten-page PDF; the served PDF SHA-256 is
  `73c2e2ab39de79357d7b441a2a4c30f901a13e99e15bf086540783041f7d6051`,
  identical to the frozen artifact. The public record preserves the
  unreviewed and AI-assisted status, the qualified novelty language, and the
  unresolved cases and classification questions. The counterexample note was
  not sent to an outside researcher by this workstream.

- **21:03 PDT - Post-release framing and proof audit opened.**
  Adversarial feedback prompted three independent checks: the exact wording
  and conditioning of Conjecture 2, the reflection-product and adjacent-phase
  Appendix arguments, and a direct full-behavior comparison with Eqs. (13),
  (15), and (45) of the originating preprint. The construction and strict
  counterexamples remain valid. The source supports a Bell-value reading of
  Conjecture 2, but Appendix B.1 separately fixes the canonical full behavior.
  The revision will state that distinction near the theorem, reproduce the
  printed conjecture and prove its factor-\(d\) normalization inconsistency,
  and qualify robustness claims as Bell-value-only. Alec reports that he
  previously emailed Ignacio Perito about the companion Conjecture 1 result
  and had received no reply by this checkpoint; the counterexample note had
  not yet been sent.

- **21:18 PDT - Adversarial-feedback revision verified (95% complete).**
  The construction survived the review. The revised twelve-page manuscript
  now distinguishes the Bell-value implication from the narrower
  fixed-canonical-full-behavior calculation, reproduces the printed
  conjecture and documents its internal normalization mismatch, and places
  the exact \(d=4\) behavior comparison next to the theorem. The polar
  certificate is stated for bounded operators on arbitrary Hilbert spaces;
  the reflection-product and adjacent-phase computations are written out;
  and the robustness conclusion is explicitly limited to Bell-value-only
  bounds. A new exact \(d=4\) check and a direct implementation of the
  originating paper's formulas confirm that the canonical and root-swapped
  maximizers have identical Bell-visible first harmonics but different full
  behaviors. All exact, numerical, JSON, syntax, PDF, and local-site checks
  pass. Public revision hashes and deployment remain to be frozen.

- **21:21 PDT - Adversarial-feedback revision published (100% complete).**
  Published commit
  `0055250a009b5f7f0a8283cba4e8813c98b700f8` to public `main`. GitHub Pages
  deployed that exact revision successfully. The live paper page exposes the
  narrowed Bell-value claim and the new source-comparison verifier. The served
  twelve-page PDF SHA-256 is
  `3bef4205ead0c1629cc78120dd701f2464ab3a38f855c8f01891412ce7b38975`,
  identical to the frozen local manuscript. The construction remains exact;
  the revision changes framing, proof exposition, and verification coverage,
  not the counterexample family.
