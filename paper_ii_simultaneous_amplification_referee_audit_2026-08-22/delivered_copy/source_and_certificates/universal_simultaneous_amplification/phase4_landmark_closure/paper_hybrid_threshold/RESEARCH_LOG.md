# Research log: simultaneous amplification beyond fitness 3/2

## 2026-08-20 — Paper II journal package opened

- Chose the robust simultaneous-amplification lower bound as Paper II's sole
  headline: one fitness-independent graph sequence works for every fixed
  `1<r<R_hyb`, with `R_hyb>3/2` the isolated sextic root.
- Fixed the scope boundary: `R_hyb` is optimal only among fixed positive
  `(sigma,lambda)` in the displayed first-order dilute pair--pendant response
  model; no unrestricted upper bound is claimed.
- Removed the logically redundant finite affine-separator result and its
  replay dependency.  Simultaneous amplification at fitness `3/2` already
  gives the relevant endpoint consequence.
- Fixed the computational boundary: exact programs audit labelled lumping and
  algebraic identities, while the weak-cut and population-asymptotic estimates
  remain analytic proofs in the manuscript.
- Began an isolated deterministic public archive and private human handoff for
  bioRxiv (Evolutionary Biology, New Results), the *Journal of Mathematical
  Biology*, and the fallback *Theoretical Population Biology*.
- Preserved DOI `10.5281/zenodo.21852072` as a v1 source/software-archive
  disclosure rather than reusing it as the identifier for this revision.

## 2026-08-20 — package boundary implemented

- Copied the three exact scientific certifiers into a paper-local
  `certificates/` directory: leading-response/tangency algebra, labelled
  hybrid lumping, and hybrid coefficient/rational-edge-family algebra.  The replay
  is now self-contained and adds a paper-level integration audit.
- Restricted the public archive to an exact 17-source-file whitelist (19
  members after synthetic metadata and manifest).  Excluded older proof notes
  and wrappers, discovery searches, sparse numerical diagnostics, the retired
  affine program, venue metadata, cover letters, and portal checklists.
- Added a paper-root pinned Python 3.14.6/SymPy 1.14.0/mpmath 1.3.0 bootstrap, normalized
  archive timestamps and ownership, an internal SHA-256 manifest, and private
  static submission checks.  Removed the historical root-level v1 bootstrap
  so `bootstrap_replay.sh` is the single clean-extraction entry
  point.
- Clean extraction, internal-manifest verification, pinned replay, and a
  byte-identical PDF rebuild all passed before the final review cycle.

## 2026-08-20 — theorem and journal framing closed

- Replaced the reciprocal-invasion sketch by an explicit two-pass
  renewal/truncation argument at the required `o(C^-1)` scale and subjected
  the center, gate, and sweep proofs to independent hostile review.
- Tightened the journal manuscript around its main theorem, moved the finite
  replay boundary into Data and Code Availability, and added the vanishing
  gain, large internal-weight, small weak-cut, and nonquantitative finite-size
  limitations.
- Made contribution and AI-assistance language factual without attributing an
  unperformed personal replay to the human author.  Human confirmation of
  funding, competing-interest, contact, and portal fields remains required.

## 2026-08-20 — final literature and priority audit

- Re-ran a primary-source search through 20 August 2026 for simultaneous
  pure-Bd/pure-dB amplification, weighted Moran fixation, transient dB
  amplification, and mixed update-order processes.  No paper found improves
  the simultaneous interval of Svoboda et al. (2024), reaches fitness
  `3/2`, uses the pair--pendant asymptotic mechanism, or changes the stated
  open problems.
- Added Bhaumik--Masuda (2024) as directly relevant weighted-network context,
  Richter (2023) for transient dB amplifier design, and Brewster et al.
  (ITCS 2026, doi:10.4230/LIPIcs.ITCS.2026.29) to distinguish random mixing of
  update steps from simultaneous amplification under the two pure endpoint
  rules.
- Kept the priority language theorem-specific and avoided claiming an
  unrestricted first result beyond what the cited literature supports.

## 2026-08-20 — adversarial major-revision pass

- Classified the external adversarial report point by point.  The center
  probability objection, fixed-parameter scope, workstream chronology,
  revision-specific archive pointer, title, wording, CRediT statement, and PDF
  metadata were valid and worth revising.  The effective dyadic construction
  was already logically present but was promoted to a named exact-computability
  lemma.  An explicit numerical upper bound on the dyadic exponent was not
  needed for constructivity.
- Split the center argument into five stopped-process lemmas and replaced
  hidden-state birth--death shorthand by conditional-intensity couplings,
  exponential generator estimates, explicit pendant waiting/cleanup bounds,
  killed-Green tail estimates, and rule-specific reciprocal renewal
  inequalities at the required `o(C^-1)` scale.
- Narrowed response optimality to fixed positive parameters in the displayed
  first-order model and added exact endpoint signs plus Sturm isolation above
  `R_hyb`.  Added the fixed-graph quantifier contrast and version-specific
  provenance for all predecessor research releases.
- Deliberately omitted a finite amplification table.  Accessible exactly
  audited finite instances did not simultaneously amplify, and the theorem
  supplies no useful finite `t_0(r)`; a trace-only or numerical illustration
  would risk being mistaken for evidence for the asymptotic theorem.
- Exact replay and a clean 20-page build pass at this pre-freeze checkpoint.
  Final independent rereview, visual QA, deterministic archive regeneration,
  and clean-extraction replay remain.  Estimated completion: **88%**.

## 2026-08-20 — adversarial revision closed

- Three independent hostile passes found and then cleared the remaining
  stopped-integral, block-restart, hidden-reseed, and reciprocal-renewal
  seams.  The final verdict found no substantive theorem, scale, quantifier,
  framing, or provenance defect.
- Exact replay, static submission checks, clean compilation, PDF text scans,
  embedded metadata/fonts, and page-by-page visual inspection pass on the
  final 19-page manuscript.  A missing-backslash TeX separator found during
  visual QA was fixed and added to the paper-level regression checks.
- The deterministic archive is ready for final regeneration and independent
  clean extraction.  Human-only address, funding, competing-interest,
  contribution, license, and submission-portal confirmations remain clearly
  separated from the research package.  Research/manuscript completion:
  **100%**; external submission remains a human action.

## 2026-08-21 — targeted referee hardening opened

- Classified the fresh specialist report point by point.  It found no
  counterexample and requested two local proof expansions: an explicit
  stopping-time regeneration for repeated Bd cleanup blocks and a displayed
  exponential-tail calculation for the reciprocal dB immigration comparison.
  Both requests are mathematically valid and improve auditability without
  changing the theorem, construction, or response coefficients.
- Also accepted the low-cost weighted-arrow, two-state monotonicity,
  nonsingular-$M$-matrix, and manuscript-date clarifications.  The request to
  retain the stopped-process lemmas in the main paper requires no change.
  The named deterministic supplement already exists locally; its final bytes
  will be regenerated and clean-tested after the new proof text freezes.
- Added the two stochastic calculations and regression markers.  Exact replay,
  rendering, independent adversarial rereview, and final archive freeze remain.
  Estimated completion of this referee-response cycle: **82%**.

## 2026-08-21 — targeted referee hardening closed

- Formalized each Bd cleanup block with an inner restart set, separated
  $2\delta$/$3\delta$/$4\delta$ escape barriers, explicit entry and terminal
  stopping times, conditional success/escape/duration bounds, and the strong
  Markov geometric estimate.  This removes any implicit independence or
  unsafe boundary-restart reading.
- Coupled the reciprocal dB cloud to a linear immigration--death process and
  supplied a stopped exponential-moment calculation for its finite-horizon
  maximum.  The proof retains the necessary hub-lifetime split and makes no
  false claim about an infinite-horizon maximum of a recurrent process.
- Added the weighted ordered-edge arrow rates, solved two-state pendant
  probabilities and their monotonicities, named the transient nonsingular
  $M$-matrices in the effective diagonal, updated the manuscript date, and
  separated the cleanup-time exponent from the later gate-rate notation.
- Independent probability and full-manuscript adversaries found no remaining
  blocking or substantive defect.  Exact replay and clean compilation pass;
  the deterministic supplement will now be regenerated from these frozen
  sources and tested by fresh extraction.  Research/manuscript completion:
  **100%**; external submission and DOI assignment remain human actions.

## 2026-08-22 — final notation correction and referee handoff freeze

- Accepted the final referee's coefficient-notation objection in the dB
  cleanup proof.  The attempt length is now
  $T=\beta_0(B_0)\log C$, with the two explicit inequalities needed to turn
  $m e^{-T}$ and $R_0e^{-\kappa T}$ into $O(C^{-B_0-2})$.  This records the
  literal exponent calculation without changing the argument or theorem.
- Updated the manuscript date, changed the development-source citation from
  mutable `main` to the planned immutable v2.0.0 tag, and compacted only the
  bibliography so that the revised paper remains readable and closes on page
  20.
- Added regression markers for the corrected coefficient and frozen source
  reference.  The scientific source/PDF checkpoint will be committed and
  tagged before a later wrapper commit adds the copied, neutral AI-referee
  handoff.  Research/manuscript completion remains **100%**; external
  submission and DOI assignment remain human actions.

## 2026-08-22 — isolated release replay hardening

- A package adversary found that the clean bootstrap created
  `.venv-paper2`, while a later standalone `release_bundle.sh` invocation
  reached `replay.sh`'s older `.venv` default.  The bootstrap itself and the
  referee runner passed, but release regeneration in an otherwise bare
  extraction could therefore miss SymPy.
- Changed `replay.sh` to prefer the pinned `.venv-paper2`, then the development
  `.venv`, then system Python, while preserving an explicit `PYTHON` override.
  The referee runner will now rebuild and compare both the PDF and source
  archive from its disposable extraction.
- Advanced the deterministic source epoch to 22 August 2026 UTC and reserved
  the immutable v2.0.1 tag for this superseding reproducibility-only freeze.
  No theorem, proof, certificate identity, or response value changed.
