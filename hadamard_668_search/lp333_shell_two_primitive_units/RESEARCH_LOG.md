# Research log: shell-two primitive-unit reduction

All times are `PDT` on 2026-07-25.  This work remained in the dedicated
research package before promotion.

## 05:30-06:00 — invariant selection

- Re-read the five-orbit shell-two classification, the failed physical-digit
  lift, and the prime-167 factorization.
- Chose to test a complete finite invariant rather than another
  lambda-adic digit: whether either recombined channel word can vanish in a
  primitive prime-167 factor.
- Derived the exact class-local alphabet.  A physical residue fiber of
  count one or two contributes one trit; counts zero and three are fixed.
  This makes single-channel primitive vanishing a complete finite
  zero-sum problem with at most 30 trits.
- In parallel, derived the physical-margin-conditioned additive summaries
  `T1,T2` in characteristic 37 and an exact six-sequence convolution.

## 06:25 — second primitive-factor block completed

- Completed all five canonical profiles, both channels, factors `3,4,5`.
- Exact cases: 30.
- Total primitive-zero assignments: 0.
- Semantic hash:
  `b3615a722e65b437edebf886bfdc5c4c54f81acca81656f974b8e41613e1fc34`.
- External wall time: 432.34 seconds.
- Maximum resident set size: 1,835,106,304 bytes.

## 06:29 — action-scope correction

- Audited the order-24 formal profile action against the normalized zero
  column.
- Found that the physical labelled lift subgroup is only
  `C6 rotations x B-star`, of order 12.  The B zero word is fixed by the
  affine reflection `r -> 3-r`; the A zero word has trivial affine
  stabilizer.
- Exact profile enumeration split the 84 formal images into ten disjoint
  physical lift orbits.  The five additional seeds are the A-star images
  of the five canonical representatives.
- Decided that action closure requires 60 canonical channel/factor audits
  plus 30 A-star A-channel audits.  B is unchanged on the A-star seeds.

## 06:37 — first primitive-factor block completed

- Completed all five canonical profiles, both channels, factors `0,1,2`.
- Exact cases: 30.
- Total primitive-zero assignments: 0.
- Largest instance: 30 trits split `15+15`, or two lists of
  `14,348,907` entries.
- Semantic hash:
  `e424fbcb8b9b7808d45dc095c22fef246a18f6c8cfee2e499b68af6e4c085816`.
- External wall time: 615.73 seconds.
- Maximum resident set size: 1,850,195,968 bytes.

## 06:39 — exact physical-margin plus T1/T2 audit completed

- Audited all 405 exact margin targets of the five canonical profiles.
- Reconstructed every physical-margin multiplicity from the six
  conditioned one-sequence distributions.
- Used exact 2D transforms modulo five primes and integer CRT with combined
  modulus greater than `3^54`.
- Targets excluded: 0 of 405.
- Physical-margin assignments:
  `1,538,710,506,610,661,125,476`.
- Exact `T1/T2` survivors:
  `1,123,966,766,238,638,605`.
- Reduction factor: `1369.0000032296`, essentially `37^2`.
- Semantic hash:
  `23946700aa96c5d8088dfb346172e38dbf74d59c9e185e29ba3fca8d34d8150b`.
- External wall time: 4.86 seconds.
- Maximum resident set size: 156,712,960 bytes.
- Decision: this exact propagator is not evidence of convergence; every
  target has at least `1,390,973,035,036,734` survivors.

## 06:44 — independent maximal-case replay completed

- Replayed the maximal canonical instance
  `h2-422220-1`, channel A, factor 0.
- Used a pinned linear map to `Z/(2^64)`, independent of the main full-key
  sort.  The physical left and target hash sets were disjoint.  Since exact
  equality implies hash equality, this is an exact nonintersection proof,
  not a collision-free-hash assumption.
- Guaranteed-positive control succeeded.
- Semantic hash:
  `95a229cbf7661182d09bd033c612f1e4419aa5ded62f344b11425c1218a683a0`.
- External wall time: 38.64 seconds.
- Maximum resident set size: 1,583,038,464 bytes.

## 06:49 — A-star closure audits completed

- Completed the five A-star seeds, A channel, all six primitive factors.
- Exact cases: 30.
- Total primitive-zero assignments: 0.
- Semantic hash:
  `743087674c409ced113b3a298fe140a74295045255c25ccc17930b0c2ea51525`.
- External wall time: 749.69 seconds.
- Maximum resident set size: 1,856,667,648 bytes.

## 06:50 — 84-image theorem closed

- Detached verifier reconstructed all 84 formal images from the promoted
  five-orbit certificate.
- Verified ten disjoint physical lift orbits with sizes
  `12,6,6,6,12,12,6,6,6,12`.
- Verified the physical profile transport, zero-word stabilizers, exact
  primitive `q`-orbit partition, and factor permutations under every
  rotation and B-star action.
- Loaded and semantically replayed all 90 MITM records.  Every exact
  primitive-zero count is zero.
- Final theorem: every physical placement over all 84 images has both
  recombined channels nonzero in all six primitive factors.
- Corollary: both channels are primitive units, so the norm cone admits
  the global ratio normalization `R=W_B/W_A`, `RR*=-1`, with
  `R_(r+3)=(-R_r^(-1))^(167^9)`.
- Action-closure semantic hash:
  `d89f8fce094dfc826749489a5dbff72f657ef07687a7f3e2eb1e25f5db0ed516`.
- Detached verifier wall time: 0.05 seconds.
- Maximum resident set size: 24,068,096 bytes.

## 06:51 — release decision

- Froze scripts, exact certificates, documentation, resource measurements,
  and reproduction commands.
- Honest classification: the primitive-unit theorem is a new structural
  lemma and a useful strengthening of the five-orbit result, but it
  excludes no profile or margin target and does not construct an
  `LP(333)` object or H(668).
- Recommended continuation only if a nontrivial multiplicative
  character/resultant/local-coset sieve can be derived on the ratio torus.
  One-candidate-at-a-time higher-digit lifting is not justified by the
  remaining `1.124e18` candidates.
- Stopped further search as requested.
