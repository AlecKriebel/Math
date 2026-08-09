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
