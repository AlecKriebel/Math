# Research log

All timestamps use America/Los_Angeles. Percentages are best-effort estimates
of completion toward the requested merged publication package.

## 2026-08-08

- **Initial checkpoint (5%).** Fetched `origin/main` at commit
  `ab2c116b0b5e19931dd93a222c528720ab6f2b91`. The primary checkout was on a
  divergent research branch with unrelated modifications, and the local
  `main` ref was checked out in another heavily modified worktree. To preserve
  all unrelated work, created the clean detached worktree
  `/Users/alec/Documents/Math-cyclic-merge` directly from `origin/main`. No
  feature branch was created. The final scoped commit will be pushed directly
  as `HEAD:main` after a fresh remote check.
- Confirmed that the three historical source directories and three historical
  website PDFs are present. Began independent mathematical inventories of the
  exact-value proof, the nonuniform-maximizer construction, the second-family
  extension, and the setting-complexity results.
- Started a clean-slate adversarial audit rather than importing the conclusions
  of the earlier project reviews. No mathematical claim has yet been frozen.
- **Mathematical checkpoint, 20:20 PDT (45%).** Three independent
  reconstructions accepted the exact operator theorem, the phase-permutation
  counterexamples for both families, and the scoped setting results. Frozen
  the main theorem set with four qualifications: no full-face classification,
  no worst-case optimality claim for the final-two swap, nonuniformity only
  for (d\ge4), and no general low-setting impossibility. Added the exact
  state-level positive-factor equality conditions and separated the source's
  dagger convention by Bob outcome inversion.
- **Priority checkpoint, 20:27 PDT (60%).** Inspected raw arXiv v1--v3 source
  for the originating paper and current primary papers on neighboring cyclic,
  randomness, SOS, and rigidity questions. No later originating version or
  family-specific priority conflict was found. Classified the first exact
  upper bound and biased maximizers as plausibly new, the commuting bound as a
  new strengthening, and the general scalar/full-statistics distinction as
  prior art.
- **Implementation checkpoint, 20:38 PDT (78%).** The unified 17-page
  manuscript and exact two-page summary build without layout or reference
  warnings. A dependency-free hostile verifier passes nine groups, including
  scalar tests through (d=20), 125 strategies per family, failing controls,
  exact rational one-input reconstructions, and a genuine nonunitary polar
  partial isometry. The canonical website and three redirect stubs are in
  place; historical PDF hashes are unchanged. Final artifact copying,
  manifests, full reproduction, visual PDF inspection, reports, and push
  remain.

## 2026-08-09

- **Surgical final-edit checkpoint, 10:53 PDT.** Fast-forwarded the isolated
  Bell-paper worktree to current `origin/main`. Standardized the exact scope
  of support rigidity across the canonical materials, expanded the omitted
  cyclic-diagonal calculation in Proposition F.1 without changing its
  statement, added the two requested Appendix B clarifications, adopted
  neutral source-v3 SOS wording, recorded the operator-model asymmetry, and
  sharpened only the minimal-support subcase of Open Problem 1. No theorem,
  mathematical verifier, historical artifact, redirect, or contribution
  boundary was changed.

- **Author-ready revision opened (10%).** Received a multi-reviewer revision
  directive and treated every item as a hypothesis. Fast-forwarded the clean
  Bell worktree to current `origin/main`; intervening changes were unrelated.
  Froze version 1.0 by immutable commits and SHA-256 hashes before editing.
- **Source crosswalk and proof audit (45%).** Re-read all named results in the
  three historical TeX sources. Confirmed that equal supported
  multiplicities, the private-MUB composition lemma, and the full binary
  benchmark are valid and should be restored. Confirmed the (qc) theorem
  after expanding the bicommutant/strong-limit step. Narrowed support rigidity
  to exact finite-dimensional tensor-product maximizers of the first
  augmented family.
- **Attribution and convention audit (65%).** Verified from primary source
  material that Perito et al. proved the (d*sqrt(2)) bound and reported NPA
  evidence through (d=6); reconstructed the source Fourier observables and
  qutrit formula; verified official Coccia/Padovan initials; and retained the
  precise scalar-value/full-behavior distinction around Conjecture 2.
- **Mathematical integration checkpoint (80%).** Added the support-rigidity
  theorem/proof, model-indexed guessing quantities, behavior nonuniqueness,
  exact four-outcome entropy, binary privacy proof, private-MUB criterion,
  low-setting status table, exact radical table, and coefficient-normalization
  proof. Three new deterministic hostile suites pass. The intermediate
  manuscript builds to 25 pages; final packet, website, manifest, visual QA,
  and release validation remain.

- **Referee-explication checkpoint, 20:52 PDT.** Re-derived each proposed
  repair against the current notation. Accepted the kernel-extension,
  target-table/Fourier-flatness, nonzero-corner, correlator-trace, root-reference,
  overbar, attribution, model-definition, and reproducibility clarifications.
  Removed the redundant manuscript-front status notice while retaining the
  end disclosure. Rejected a new DOI and a structural supplement split; neither
  is needed for correctness and both exceed this scoped final pass. The central
  theorem statements, section order, mathematical verifiers, redirects, and
  historical artifacts remain unchanged.
- **Website-validator repair, 21:06 PDT.** The first full replay passed every
  mathematical, certificate, historical-integrity, and PDF-build stage, then
  exposed three stale assertions left by the newer portfolio redesign. The
  site validator no longer mistakes the author's ORCID JSON-LD identifier for
  a DOI, accepts the current AI/unrefereed wording, and checks the current
  selected-papers section rather than a retired homepage count. No deployment
  configuration or website route changed.
- **Scientific-source freeze, 21:12 PDT.** Committed the complete substantive
  referee-explication revision as
  `609f8c6ffc083b665804890dd82fc739d414ea9d` after the 11-stage replay and
  full visual PDF inspection. The publication-facing data-and-code statement
  now points to that immutable scientific snapshot. This provenance-only
  follow-up changes no theorem, proof, or verifier.
