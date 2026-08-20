# Research log: dB extremality paper

## 2026-08-20 — package opened

- Chose a unified paper around the normalized complete-kernel gap, with the
  fixed-graph strong-selection theorem and the full-directed fitness-two
  local theorem as co-headlines.
- Preserved the earlier manuscript as provenance and opened this isolated
  package for the expanded paper.
- Fixed the claim boundary: local maximality is in normalized replacement-
  kernel space; raw incoming-column scalings are dynamical gauge directions.
- Fixed the quantifier boundary: the paper rules out one **fixed finite**
  universal dB amplifier, but does not rule out a fitness-independent graph
  sequence whose population threshold depends on fitness.
- Assigned independent theorem, scope, and reproducibility audits before
  authoring.
- Best-guess completion: 10% of the publication package; theorem components
  are proved, but synthesis, replay integration, rendering, and adversarial
  review remain.

## 2026-08-20 — hostile normalization audit and claim correction

- An independent audit unwound the proposed standard-sector quotient to the
  labelled active chain and found that the previously cited phase theorem
  signs a nearby inverse-rank reward, not the physical Poisson reward in the
  fixation Hessian.  There is no established positive scalar normalization
  between them.
- Removed the unsupported full-directed local-maximality claim.  The exact
  theorem retained here is stronger than the old regular/undirected result:
  the complete kernel is stationary in every normalized tangent direction
  and strictly locally optimal throughout the full directed bistochastic
  subpolytope.  The symmetric-balanced and antisymmetric-balanced sectors are
  both proved for every order; the standard column-imbalance sector is now
  stated explicitly as open.
- Removed the non-load-bearing standard verifier from the paper replay and
  replaced the symmetric quotient's unspecified positive normalization with
  its exact physical identity.
- Best-guess completion: 35% of Paper I.  The claim set is now conservative;
  full certificate integration, rendering, and repeated hostile review
  remain.

## 2026-08-20 — physical standard sector repaired and independently audited

- Replaced the nonphysical auxiliary standard reward by the exact Poisson
  reward induced by the labelled active-chain Hessian.  The quotient scalar
  is
  $\Phi_N=\sigma(I-H)^{-1}\gamma$, with
  $\mathcal R_n^{(2)}(E(\xi))/\|\xi\|^2
  =\Phi_N/[4(N+1)^2(N-1)]$.
- Proved $\Phi_N>0$ for every $N\ge2$: exact Schur elimination, a positive
  first-phase barrier, a uniform completed-phase contraction, and a Neumann
  tail handle $N\ge10$; exact rational values close $2\le N\le9$.
- A hostile audit caught an invalid attempted use of the local $W$ barrier in
  the lower-bound step.  The final proof instead uses the independent global
  resolvent bound $R_Qq\le4N\mathbf1$.  The corrected distinction is explicit
  in the theorem note and verifier.
- Two independent reviewers rebuilt the labelled quotient and normalization,
  checked every all-order polynomial identity and boundary inequality, and
  replayed the final exact verifier.  No mathematical objection remained.
- Restored the full row-stochastic directed local theorem and integrated all
  three physical tangent sectors into the manuscript.

## 2026-08-20 — journal package and provenance pass

- Converted references to author--year form, expanded the graphical-duality
  context, and made the full-versus-finite verification boundary explicit.
- Disclosed the public v1.0.0 strong-selection/low-order archive and stated
  that this manuscript is a major superseding version whose fitness-two
  coverage, collision, and all-sector Hessian theorem are new.
- Added exact standard and symmetric normalization bridges, explicit channel
  ranges, journal-style declarations, and a readable quantifier ledger.
- Best-guess completion: 75% of Paper I.  Remaining work is the standalone
  bundle, final clean-room replay, full-page visual audit, and repeated
  adversarial manuscript review.

## 2026-08-20 — Paper I frozen after clean-room and hostile review

- Expanded the symmetric-sector appendix to include the all-order labelled
  incoming-current normalization, fixed-count sampling identities, channel
  ranges, positive-resolvent premises, and every finite/large-order boundary
  certificate used by the sign proof.
- Replayed the complete exact suite from the development tree and from a
  fresh extraction with Python 3.14.6, SymPy 1.14.0, and python-flint 0.9.0.
  Both replays exited zero.  A first clean-room attempt exposed one omitted
  transitive verifier dependency; the deterministic manifest was corrected,
  and a second genuinely clean extraction passed in full.
- Rebuilt the manuscript reproducibly inside the extracted archive.  Its
  26-page PDF was byte-for-byte identical to the repository build, with
  SHA-256
  `2720d0a5d372330c3c2b3212dcf16c6d74ddedf0e0bd7a2b06cd8946e131184e`.
- Generated the deterministic 92-entry source-and-certificate archive twice
  at the clean-room checkpoint; the copies were byte-for-byte identical, with
  checkpoint SHA-256
  `0993ee6d138508c9bd3e8729dbbad60c1127528690fc695ffb54c94cd8dde217`.
- Three adversarial reviews checked the headline quantifiers, directed dual,
  collision normalization, tangent decomposition, physical normalization of
  all sectors, strong-selection closure, submission metadata, archive
  dependency closure, and every rendered page.  The final verdict was a
  clean pass.  The sole remaining token is the intentionally human-gated
  postal address in cover-sheet material.
- Paper I completion: 100% of the requested manuscript, certificate,
  reproducibility, and submission package.
