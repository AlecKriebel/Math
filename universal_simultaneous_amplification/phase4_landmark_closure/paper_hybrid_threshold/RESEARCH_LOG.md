# Research log: simultaneous amplification beyond fitness 3/2

## 2026-08-20 — Paper II journal package opened

- Chose the robust simultaneous-amplification lower bound as Paper II's sole
  headline: one fitness-independent graph sequence works for every fixed
  `1<r<R_hyb`, with `R_hyb>3/2` the isolated sextic root.
- Fixed the scope boundary: `R_hyb` is optimal only in the displayed pair--
  pendant leading-order architecture; no unrestricted upper bound is claimed.
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
  hybrid lumping, and hybrid coefficient/rational-family algebra.  The replay
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
