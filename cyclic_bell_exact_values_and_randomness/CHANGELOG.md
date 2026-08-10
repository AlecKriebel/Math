# Changelog

## Version 1.1 — 2026-08-09

### Referee-explication and arXiv-readiness pass

- Removed the redundant first-page status notice while retaining the detailed
  end-of-manuscript AI-assistance disclosure, and added the author's public
  contact address and ORCID to the author block.
- Made the kernel case in the conditional phase-permutation proof explicit by
  separating the canonical polar partial isometry from its unitary extension.
  Derived the target probability table from its eigenvectors and proved the
  canonical ordering Fourier-flat in every dimension, including the complete
  short argument for dimensions two and three.
- Added representative trace calculations for the second-family correlator
  invariance, the missing nonscalar-implies-nonzero-corner hinge in Proposition
  F.1, and a valid numbered cross-reference for the equality roots. No theorem
  statement or contribution boundary changed.
- Credited the originating score symmetries and narrowed the comparison row to
  nonuniform phase-permuted maximizers. Replaced internal source-version
  shorthand in publication-facing prose by the precise SOS citation to
  Eqs. (22)--(23), and gave a conventional public code-and-data URL.
- Updated only the obsolete website assertions in the existing validator
  after the repository-wide portfolio redesign: an ORCID JSON-LD identifier
  is no longer mistaken for a DOI, and homepage/status checks follow the
  current site structure. Mathematical verification code is unchanged.

### Final proof-presentation pass

- Standardized the support-rigidity scope as attained finite-dimensional
  tensor-product exact maximizers of the first augmented family throughout
  the manuscript, canonical page, summary, README, and reviewer packet.
- Expanded Proposition F.1's cyclic-diagonal argument with the two indexed
  off-diagonal equation families, the exact vanishing range, and the explicit
  Toeplitz corner block. Added the two requested invariance and commuting-
  stabilizer sentences to the support-rigidity proof.
- Replaced correction-implying SOS language by the neutral source-v3
  prefactor convention, explained the operator-model scope asymmetry once,
  and sharpened Open Problem 1 with the minimal-support case.

### Restored and strengthened

- Restored the finite-dimensional support-rigidity theorem for exact
  maximizers of the first augmented family: every equality root occurs with
  equal multiplicity on $\operatorname{supp}\rho_A$, hence $d$ divides the supported
  dimension. Added the complete kernel-safe support and reflection-rank proof.
- Expanded the commuting-operator polar proof with the generated von Neumann
  algebra, strong-limit formulas for the support and canonical partial
  isometry, and the bicommutant commutation step.
- Restored the private-MUB composition lemma as a sufficient operator-valued
  criterion and the complete binary `3*sqrt(3)` benchmark, including two
  private bits and precisely scoped `(2,2)` DI setting minimality.
- Restored the source-observable Fourier identification, explicit qutrit
  formula, exact radical table for `d=2,...,6`, and the cosecant-square proof
  of the second-family coefficient normalization.

### Attribution and randomness scope

- Credited Perito et al.'s proved `d*sqrt(2)` upper bound separately from
  their sharper conjectured value and NPA evidence through `d=6`.
- Identified the intended scalar-value implication of source Conjecture 2 as
  refuted for every `d>=4`, after explaining its printed normalization
  discrepancy; the fixed canonical full-behavior computation remains outside
  the counterexample's scope.
- Replaced the unqualified guessing quantity by model-indexed `q`, `qa`, and
  `qc` quantities. Added behavior-level nonuniqueness modulo output
  relabelings and the exact `d=4` entropy `5-log_2(3)` bits, without claiming
  the worst-case optimum or a complete self-testing classification.
- Corrected one-input wording to DI certification against all compatible
  realizations. Restored a status table separating prior-art, proved,
  conditional, and open low-setting regimes.
- Verified the official names Lorenzo Coccia, Matteo Padovan, and Giuseppe
  Vallone; the canonical `L./M./G.` initials were already correct. Cited the
  formerly unused NPA reference at the numerical-evidence statement.
- Removed the categorical statement that no source author had ever been
  contacted, which was incompatible with the preserved historical record.
  No external review, collaboration, or endorsement is claimed.

### Audit and verification

- Added `REVIEW_RESPONSE.md`, a theorem-by-theorem crosswalk, three focused
  restoration audits, and an immutable pre-revision commit/hash record.
- Added deterministic rigidity, exact-benchmark/source-observable, and
  binary/private-MUB hostile verifiers and integrated them into
  `reproduce.sh`.
- Preserved every historical source directory and deployed standalone PDF
  byte-for-byte.

## Version 1.0 — 2026-08-08

### Consolidated

- Rebuilt the three historical Bell manuscripts as one paper with a single
  notation system and theorem hierarchy.
- Integrated the first-family exact value, commuting-operator extension,
  phase-permutation mechanism, nonuniform maximizers, second-family SOS
  saturation, randomness interpretation, and scoped setting consequences.
- Preserved all three historical source packages and deployed PDFs without
  changing their bytes.

### Mathematical repairs and clarifications

- Fixed the authoritative normalization at the operator definition. The
  first augmented value is (2\csc(\pi/(2d))+1); the source's isolated extra
  denominator factor is recorded neutrally as a typographical inconsistency.
- Chose the Hermitian no-adjoint Bob convention used by the originating main
  text and corrected SOS. The appendix dagger convention is related by Bob
  outcome inversion and is not mixed into the formulas.
- Restored the (d\lambda_\ell) factor and Alice entrywise conjugation needed
  by the second-family SOS construction.
- Stated genuine partial-isometry support handling in the polar proof; no
  inverse or unitary polar extension is assumed.
- Replaced any suggestion of a complete maximizing-face classification by a
  conditional phase-permutation theorem with explicit equality and product
  hypotheses.
- Restricted the nonuniformity theorem to (d\ge4). The weighted-shift
  maximizers exist for every (d\ge2), but all permutations in this family
  are target-flat for (d=2,3).
- Made the guessing statement a lower bound from an explicit trivial-Eve
  realization; the displayed permutation is not claimed worst-case.
- Separated scalar Bell-value conditioning from fixed full-behavior
  conditioning throughout.
- Scoped the computational-MUB result to its real operator span,
  coefficientwise common bound, separately bounded term, and computational
  target PVM. No general (2\times3) impossibility is claimed.
- Formulated endpoint non-robustness for strategies whose deficit is at most
  (\varepsilon), closing a quantifier ambiguity.

### Historical theorem disposition

No historical theorem was silently dropped.

- The exact-value theorem, augmented value, phase-permutation construction,
  biased target theorem, exact (d=4) certificate, second-family extension,
  one-input theorem, canonical-table calculation, direct-anchor calculation,
  and scoped MUB obstruction were retained or strengthened.
- The finite-dimensional “equal supported multiplicities” proposition from
  the counterexample note remains valid historical secondary material but is
  not imported into the canonical theorem set: it is not needed for the
  explicit obstruction and would distract from the support-safe equality
  claims. Its source and proof remain in
  `cyclic_randomness_counterexample/manuscript.tex`.
- The private-MUB composition lemma remains valid design guidance but is
  omitted from the canonical paper for focus. It remains in
  `minimum_bell_randomness/manuscript.tex`.
- The binary (d=2) SOS is retained only as a cited prior-art calibration,
  not as a new theorem.
- The numerical power-harmonic repair experiment and a stray binary
  (2\times3) comparison were not imported because they are not proved
  load-bearing results.
- The all-dimensional minimum-setting-pair claim was already marked false in
  the historical ledger and is explicitly not claimed here.

### Verification

- Added a standard-library hostile verifier, including a genuinely
  nonunitary polar partial isometry and failing-hypothesis controls.
- Retained two independent exact (\mathbb Q(\zeta_{16})) implementations at
  (d=4).
- Added one-command build, metadata, hash, and website validation.

### Website

- Added the canonical page and consolidated homepage card.
- Replaced only the three historical landing pages with `noindex,follow`
  compatibility redirects.
- Kept every historical PDF URL and byte sequence unchanged.

No DOI, submission, release, coauthor, or external communication was created.
