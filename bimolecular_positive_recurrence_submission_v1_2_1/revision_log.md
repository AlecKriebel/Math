# Revision log

Historical sections describe their own immutable release directories; paths
named there need not be present in the current Version 1.2.1 directory.

## Version 1.2.1 submission patch — 16 August 2026

Version 1.2.1 is a separate patch-release directory and supersedes Version 1.2
for preprint and journal use. It leaves the Version 1.2 directory, tag, PDFs,
archive, and validation record unchanged and carries its verifier component
Version 1.2.0 byte-for-byte.

### Referee-facing corrections

- Replaced version-dependent Anderson--Cappelletti--Kim theorem, lemma, and
  equation numbers with stable references to published Section 6 and Section
  6.1. The prior locators were exact for arXiv Version 2 but not for the
  published JAP typesetting.
- Defined the divergent-species set in the top-complex proof explicitly and
  displayed the exhaustive bimolecular trichotomy inside the proof.
- Renamed the residual to `rho`, the one-jump drift to `delta`, the top set to
  `mathcal T`, and the top divergent-species set to `mathcal J`; also removed
  the most distracting local `L` and `J` collisions.
- Added concise self-channel/minimal-CTMC, population-projection autonomy, and
  residual-integrability sentences. The theorem and proof strategy are
  unchanged.

### Submission-facing corrections

- Spelled out Anderson--Cappelletti--Kim in reader-facing text, removed the
  editorial `[sic]` from the exact current Xu title, and kept the earlier
  Geneva priority citation rather than adding a later Cornell item.
- Removed the repository release number from the bioRxiv/arXiv and
  supplementary-note title-page dates, and made the preprint-status paragraph
  durable after posting.
- Retained the two-page note for bioRxiv/archival use but removed it from the
  planned JAP upload unless an editor requests it.

## Version 1.2 submission candidate — 16 August 2026

Version 1.2 is a separate release directory and supersedes Version 1.1 for
preprint and journal use. It does not alter any earlier directory, tag,
artifact, or audit record.

### Referee-facing hardening

- Reworded both abstract variants so weak reversibility explicitly governs
  reachable-class closure and the one-linkage/bimolecular hypotheses govern
  positive recurrence.
- Restricted the displayed ACK Example 4.1 asymptotic formula involving
  `log(n-1)` to `n >= 2`.
- Expanded the stationary-occupation paragraph to state expected-return and
  numerator finiteness, Tonelli normalization, regeneration, and uniqueness.
- Kept the theorem, all load-bearing lemmas, and the exact rate scope
  unchanged after a fresh adversarial proof reconstruction.

### Submission materials

- Made bioRxiv Systems Biology / New Results the primary preprint route and
  arXiv a mutually exclusive fallback.
- Added a journal-routing note recommending the joint Applied Probability
  submission route, naturally JAP, and recording the separate SPA conversion
  requirements.
- Updated status, availability, disclosure, cover-letter, and metadata text
  through 16 August 2026 and disclosed all public repository versions plainly.
- Replaced the Markdown-only reviewer appendix pointer with a polished,
  standalone supplementary-note PDF while keeping the main proof
  self-contained.

### Reproducibility and provenance

- Added `REPRODUCIBILITY.env` and made the canonical four-PDF build require
  Tectonic 0.16.9, an explicit bundle, deterministic mode, and a fixed epoch.
- Made repeated regular-wheel builds byte-identical and added a standard-library,
  manifest-driven deterministic ZIP builder with a byte-comparison check.
- Added a complete clean-checkout release replay, supported Python 3.11--3.14
  matrix, pinned CI actions, and an immutable Version 1.1 provenance record.
- Regenerated the Version 1.2 report, PDFs, complete manifest, validation
  records, archive, and public-site hashes from their declared sources.
- Preserved historical Version 1.1 module, test, and audit filenames because
  they record when those materials were introduced.

## Version 1.1 submission candidate — 10 August 2026

Version 1.1 is a separate release directory. It does not mutate Version 1.0,
its Git tag, its tagged commit, or any Version 1.0 PDF, source, verifier, or
manifest artifact.

### Preservation and versioning

- Recorded the Version 1.0 tagged commit and tag object, canonical source and
  PDF hashes, verification-report digest, manifest digest, and package-archive
  digest in `preservation/PRE_REVISION_PROVENANCE.md`.
- Prepared the separate directory
  `bimolecular_positive_recurrence_submission_v1_1/` for the intended
  `bimolecular-positive-recurrence-v1.1` annotated tag.
- Retained the Version 0.3 preservation record and all prior Git history.

### State-space closure and theorem scope

- Added the elementary lifted state-cycle lemma: a directed complex return
  path supplied by weak reversibility lifts with fixed residual population to
  enabled population transitions.
- Checked the lemma at the zero complex and boundary states, with lattice and
  parity restrictions, parallel channels, coincident population
  displacements, and absorbing singletons.
- Concluded that accessibility is symmetric and that the population set
  reachable from every initial state is already one closed communicating
  class. This closure fact itself needs neither one linkage class nor
  bimolecularity.
- Strengthened the main theorem and its wrappers accordingly: every
  nonabsorbing reachability class in the stated binary one-linkage setting is
  nonexplosive and positive recurrent for every positive rate vector, while
  every absorbing singleton carries its point-mass law.
- Removed the former disclaimer about finite expected entrance from a
  nonclosed initial state. Under weak reversibility the relevant reachability
  class is closed from time zero.

### Prior-work and rate-example corrections

- Replaced the comparison with Anderson, Cappelletti, and Kim (2020) by the
  exact Section 6 chain: Theorem 6.1, tier inclusion (11), Lemmas 6.3--6.5,
  and the sampled-chain assembly in Lemma 6.4.
- Clarified the role of the pure-species hypothesis in Section 6.1, equations
  (19)--(20): it supplies either $S_v$ or $2S_v$; D-tier maximality
  excludes $2S_v$, forcing $S_v$, whose source propensity supplies the
  comparison. No unsupported broader characterization of the earlier
  assumption is made.
- Corrected the fixed-$m$ limit in the rate-dependence example to
  $D_0(m,A)\to a_m(1+p_m)>0$ as \(\kappa_2\downarrow0\), while retaining
  the exact logarithmic coefficient
  \(-\kappa_2/(\kappa_1+\kappa_2)\).
- Retained the qualitative conclusion that no bound on the location or
  diameter of the proof's finite Foster set can depend only on the numbers of
  species and complexes uniformly over positive rate vectors.

### Submission-facing exposition

- Rewrote the technical abstract to lead with positive recurrence, automatic
  reachability-class closure, and the unique stationary-law consequence;
  nonexplosion is described as a recovered conclusion.
- Restored MSC 2020 code 60J27 as primary, with 60J28, 60J74, and 92C42 as
  secondary classifications.
- Preserved Xu's official arXiv title, *On the Regulary of Reaction Systems*
  [sic], and rechecked the Version 2 record on 10 August 2026.
- Updated the ConStRAINeD access date to 10 August 2026 and retained the
  calibrated statement that no public manuscript for the announced
  two-species result was located as of that date.
- Folded the concise biological motivation into the introduction and retained
  the no-formula, no-moment/tail/mixing, and structural-scope limitations.
- Updated the separate 150--200-word Systems Biology significance summary,
  screening note, arXiv and bioRxiv metadata sheets, and journal cover letter.
  None was uploaded or sent.

### Compression, disclosure, and reproducibility

- Moved the former trace-chain and physical-time appendix, together with the
  detailed computational-boundary note, to
  `supplement/reviewer_appendices.md`; the main paper retains the substantive
  propositions and their proofs.
- Shortened the manuscript generative-AI declaration and updated
  `supplement/ai_use_full_statement.md` with known systems, models, access
  routes, dates, and roles through 10 August 2026. Rejected approaches are not
  part of the final proof; no AI system is an author, and no independent
  expert human validation is claimed.
- Added deterministic checks for state-cycle lifting, finite-network
  reachability symmetry, the corrected rate limit, scalar-envelope
  monotonicity, absorbing singletons, and finite-chain stationary
  return-cycle normalization.
- Added `supplement/v1_1_mathematical_audit.md` and
  `supplement/publication_v1_1_literature_audit.md` as the focused mathematical
  and primary-source audit records for this revision.
- Rebuilt all three thin wrappers from one canonical source and reserved
  final report, manifest, clean-clone, toolchain, transcript, PDF-hash, and tag
  records for the separately reproducible Version 1.1 release.

### Scope retained

Version 1.1 does not claim positive recurrence for multiple linkage classes,
molecularity greater than two, the full arbitrary-dimensional weakly
reversible conjecture, product-form or explicit stationary laws, finite
moments without integrability, quantitative tails, mixing rates, exponential
ergodicity, bounded sample paths, or useful general bounds on the Foster set.

## Version 1.0 publication candidate — 9 August 2026

Version 1.0 is a separate publication-candidate directory. It does not mutate
Version 0.3, its Git tag, or its tagged commit.
Paths named in this historical section refer to the immutable Version 1.0
package, not to the Version 1.1 directory.

### Preservation

- Copied the Version 0.3 preprint and journal PDFs, canonical manuscript
  source, bibliography, and verification report into `preservation/`.
- Recorded the annotated tag object, tagged commit, and required Version 0.3
  SHA-256 values in `preservation/VERSION_0.3_PROVENANCE.md`.
- Retained earlier audit and development artifacts in their existing Git
  history while excluding abandoned research history from the Version 1.0
  first-contact archive.

### Mathematical positioning and exposition

- Preserved the exact binary, one-linkage, class-wise positive-recurrence
  theorem and its arbitrary-positive-rate scope.
- Re-audited only the proof interfaces touched by the publication revision;
  that replay remains in the separately tagged
  [Version 1.0 package](https://github.com/AlecKriebel/Math/blob/bimolecular-positive-recurrence-v1.0/bimolecular_positive_recurrence_publication_v1/supplement/publication_v1_targeted_proof_audit.md).
- Positioned the residual log-factorial potential as a discrete,
  target-shifted analogue of classical pseudo-Helmholtz/Horn--Jackson entropy,
  while identifying carried-target subtraction and the exact factorial
  increment as the new mechanism in this argument.
- Added a source-specific comparison with Anderson, Cappelletti, and Kim
  (2020), stated that their theorem is a special case, and explained how the
  marked-target method removes the pure-species-complex hypothesis.
- Added deterministic boundedness and permanence motivation and a calibrated
  systems-biology interpretation for low-copy-number biochemical CTMCs.
- Distinguished the proved class-wise conclusion from finite expected entry
  into a closed component and from the larger multiple-linkage and
  higher-molecularity conjectures.

### Proof-interface clarification

- Made scalar-envelope monotonicity explicit and used it in the backward
  induction.
- Removed the redundant top-complex branch and emphasized that divergent
  coordinates with zero limiting normalized weight remain divergent species.
- Defined the stopped-potential supermartingale explicitly in the random-time
  Foster argument.
- Retained, but streamlined, the finite trace-chain, one-state return,
  embedded-chain-to-CTMC, physical-time, and nonexplosion closure.
- Handled absorbing singleton classes by their point-mass stationary law
  rather than by a positive-return convention.
- Cited and briefly justified the regenerative stationary-occupation formula.
- Presented the self-contained nonexplosion argument as a recovery of a known
  conclusion for this subclass, consistent with Xu's more general theorem.

### Quantitative limitations

- Added the exact rate-degeneration calculation for
  \(0\to A\to A+B\to0\), including the coefficient
  \(-\kappa_2(\kappa_1+\kappa_2)^{-1}\log m\).
- Explained that this coefficient can approach zero through positive rate
  ratios, so the analytic finite set \(K\) has no rate-independent bound based
  only on network size.
- Stated that the finite atlas and random tests neither certify \(K\) nor
  replace the analytic compactness proof.

### Public presentation and bibliography

- Adopted the balanced title *Positive Recurrence for Single-Linkage
  Bimolecular Weakly Reversible Stochastic Reaction Networks* and ordinary
  preprint dating.
- Rewrote the abstract and introduction for probability and systems-biology
  readers without changing the theorem.
- Removed the decorative Version 0.3 proof-flow figure; no AI-generated raster
  figure is used in the Version 1.0 manuscript.
- Rechecked titles, versions, DOI metadata, protected capitalization, the
  Agazzi announcement wording, and the status of the Xu preprint against
  primary records current on 9 August 2026.
- Added standard Markov-chain, Foster--Lyapunov, random-time drift, and
  regenerative references without removing the proof's self-contained
  interfaces.

### Verification and release materials

- Added deterministic regression checks for scalar-envelope monotonicity, the
  redundant top-complex case, the rate-degeneration example, a finite
  stationary-return calibration chain, and absorbing singletons.
- Prepared thin arXiv, bioRxiv, and Applied Probability wrappers around one
  canonical mathematical source.
- Added a 150–200-word Systems Biology significance summary, a truthful
  bioRxiv screening note, arXiv and bioRxiv metadata sheets, and a journal
  cover letter. None was uploaded or sent.
- Replaced the manuscript's long AI chronology with a concise declaration and
  moved complete tool, date, access, and use details to
  `supplement/ai_use_full_statement.md`.
- Added a targeted reviewer checklist, expert orientation note, clean-clone
  validation records, stable verification output, and a complete Version 1.0
  manifest.

### Final independent-audit repairs

- Named the marked augmented embedded chain $Z_n$ at its construction and
  wrote the signed invariant explicitly as
  $\ell(x)=\sum_{i\in J}x_i-\sum_{D\in\mathcal D}x_D$, closing two localized
  notation omissions found in the final proof replay.
- Added a nine-line, non-mathematical abstract selected only by the Applied
  Probability wrapper; the canonical technical abstract remains unchanged in
  the arXiv and bioRxiv wrappers.
- Corrected the literature-audit title and mathematics formatting, clarified
  that $q_J(y)=1$ counts one $J$-particle, and separated completed checks
  from submission-day rechecks.
- Extended continuous integration to compare manifest/report copies and to
  reject an unsafe, corrupt, incomplete, or stale first-contact ZIP archive.

### Scope retained

Version 1.0 does not claim multiple linkage classes, molecularity greater than
two, the full Anderson--Kim positive-recurrence conjecture, finite expected
entry into a closed component from an arbitrary nonclosed state, product-form
stationary laws, quantitative tails, explicit mixing rates, exponential
ergodicity, or bounded sample paths.

## Version 0.3 — 9 August 2026

Version 0.3 is preserved verbatim under `preservation/` and at the existing
`bimolecular-positive-recurrence-v0.3` Git tag. Its detailed revision history
remains in the tagged release and is not rewritten here.
