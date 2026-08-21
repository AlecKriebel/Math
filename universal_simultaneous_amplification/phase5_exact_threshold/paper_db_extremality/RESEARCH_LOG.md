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
  checked every population-size polynomial identity and boundary inequality, and
  replayed the final exact verifier.  No mathematical objection remained.
- Restored the full row-stochastic directed local theorem and integrated all
  three physical tangent sectors into the manuscript.

## 2026-08-20 — journal package and provenance pass

- Converted references to author--year form, expanded the graphical-duality
  context, and made the full-versus-finite verification boundary explicit.
- Disclosed the public v1.0.0 strong-selection/low-order archive and separated
  its previously released results from the fitness-two coverage, collision,
  and all-sector Hessian theorem introduced in this manuscript.
- Added exact standard and symmetric normalization bridges, explicit channel
  ranges, journal-style declarations, and a readable quantifier ledger.
- Best-guess completion: 75% of Paper I.  Remaining work is the standalone
  bundle, final clean-room replay, full-page visual audit, and repeated
  adversarial manuscript review.

## 2026-08-20 — Paper I frozen after clean-room and hostile review

- Expanded the symmetric-sector appendix to include the every-order labelled
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

## 2026-08-20 — external adversarial-review revision

- Adjudicated twelve detailed reviewer comments against the labelled chains,
  exact certificates, source, and primary literature.  No headline theorem
  was withdrawn.  The review correctly identified an ambiguous phase order in
  the collision interpretation, an overly compressed antisymmetric coupling,
  and several explicitness and positioning gaps.
- Rewrote the collision statement in the stationary sample--then--retarget
  chain, with the two conjugate stationary laws displayed.  Expanded the
  strict rank-Poisson monotonicity argument into a four-chain heat-bath
  coupling and made the finite symmetric-sector calculation a formal exact
  computer-assisted lemma with its case ranges, minimum margin, expected
  output, and verifier hash.
- Added proofs of dual irreducibility and aperiodicity, strict positivity near
  the complete kernel, the standard-sector Frobenius normalization, and
  fitness monotonicity.  Retitled the paper to foreground local optimality,
  sharpened the boundary with the Tkadlec et al. theorem, and added a neutral
  new-versus-released result ledger.
- Expanded the ancestry and contemporary amplification context using primary
  literature.  Replaced unverifiable human-execution language by a precise
  responsibility statement and instructions for independent replay.
- Hardened the release command so that it replays the exact suite and rebuilds
  the PDF before packaging.  A new clean-room replay, deterministic archive,
  and final hostile review remain before this revision is frozen.
- Best-guess completion: 90% of the adversarial-review revision; the proof and
  presentation edits are complete, while clean-room and final-review gates
  remain.

## 2026-08-20 — adversarial revision clean-room checkpoint

- Replayed the complete exact suite after the accepted review changes; every
  load-bearing assertion passed.  The paper-level integration audit now also
  checks the standard-sector Frobenius conversion introduced in the revision.
- Generated two byte-identical deterministic archives from the same inputs.
  In a new extraction, all manifest hashes passed, the pinned Python 3.14.6
  environment with SymPy 1.14.0, python-flint 0.9.0, and mpmath 1.3.0
  installed cleanly, and the full exact replay exited zero.
- Rebuilt the 29-page PDF inside that extraction.  It matched the repository
  PDF byte for byte, with SHA-256
  `3af20b4648c6a69e1946e6cdd32f5df9557ca55a2ec1a1c16b29a8dbb6e92d98`.
- Inspected every rendered page at full-page resolution.  No clipping,
  malformed equations, unreadable certificate text, or bibliography/layout
  defect was found.
- Best-guess completion: 97% of the adversarial-review revision.  Only the
  final independent hostile review, any resulting repair, and the final
  commit/push remain.
