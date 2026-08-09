# Changelog

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
