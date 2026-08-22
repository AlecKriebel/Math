# Version 1.2.4 editorial-feedback audit

**Audit dates:** 19--20 August 2026 (America/Los_Angeles)

**Scope:** adjudication of a further frontier-model review; live primary-source
checks; stationary-law, corollary-location, and worked-example clarity; release
and rendering validation.

## Accepted changes

- Replaced the claim of “no explicit stationary formula” by distinguishing the
  regenerative occupation representation already displayed in the paper from
  a closed-form or product-form stationary distribution.
- Added a forward pointer after Corollary 2.3 to its regenerative proof at the
  end of Section 7.
- Stated explicitly that the initial expected reward at the marked state
  \((x_n,A)\) in the Anderson--Cappelletti--Kim example is zero. The only
  enabled sources are \(A\) and \(A+B\), and both target/source ratios equal
  one at \(x_n=(n,1,0)\).
- Defined \(\mathcal C\) as the complexes that actually occur in reaction
  channels, qualified the deterministic motivation by strictly positive
  initial conditions, removed “candidate” from the bioRxiv PDF metadata, and
  removed a repeated limitations clause while retaining the distinct
  unbounded-moment warning.
- Updated the live ConStRAINeD access statement and material AI-use chronology
  through 20 August 2026, without claiming a new journal or repository-policy
  recheck.

## Suggestion rejected

- The proposed replacement of Xu's title by *Non-explosivity of endotactic
  stochastic reaction systems* was rejected. On 20 August 2026, the official
  current arXiv record, Atom entry, and Version 2 PDF still display *On the
  Regulary of Reaction Systems*, with Version 2 revised 9 May 2026. The
  proposed replacement is the superseded Version 1 title.

Primary records:

- <https://arxiv.org/abs/2409.05340>
- <https://arxiv.org/abs/2409.05340v1>
- <https://constrained.polito.it/publications/>
- <https://arxiv.org/abs/1104.4992>
- <https://epubs.siam.org/doi/10.1137/19M1248431>

## Mathematical verdict

The theorem, hypotheses, marked-target identity, path recursion, scalar
envelope, top-complex trichotomy, Foster argument, trace conversion,
nonexplosion argument, and regenerative stationary law remain unchanged. No
theorem-breaking defect was found in this review.

## Release validation

All four PDFs rebuilt twice to byte-identical files. All 50 rendered pages were
visually inspected; no clipping, overlap, broken glyph, or layout regression
was found. The 57 verifier tests passed with Python 3.11 and 3.14, the four
release-safety tests passed, both 82-file manifests agree, and the deterministic
archive contains 84 canonical members. Local hashes are recorded in the release
manifest and reproduction record. Hosted main- and tag-workflow validation is
supplied by the release workflows after publication.
