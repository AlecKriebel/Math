# Research log: coverage/submodular upper-bound branch

All timestamps are America/Los_Angeles.

## 2026-08-13 -- exact structural closure and profile refutation

- **PROVED:** the actual fitness-two dB fixation committor is the coverage
  function `h(S)=Pr_Pi(A intersects S != empty)` of the stationary exact
  fair-geometric union dual.  No independent-lineage approximation is used.
- **PROVED:** `h` is monotone, submodular, and completely alternating.  Its
  mixed differences are exact joint inclusion/avoidance probabilities under
  the representing stationary law.
- Investigated the proof-first reversible profile candidate

      mean_i h({i}) <= mean_i Phi_n(pi_i),

  where `pi_i=d_i/sum d` and
  `Phi_n(z)=[1-(1+z)2^(-nz)]/[1-2^(1-n)]` interpolates the complete count
  harmonic.  If valid together with the required shape inequality, this
  would have reduced the upper theorem to a scalar vertex-mass extremum.
- **EXACTLY REFUTED:** a six-vertex equitable graph with cells of sizes
  `(3,2,1)` and weights `w_AA=5,w_AH=2,w_BB=73,w_BH=1` has exact dB fixation
  `0.3671048144272996...`, while its degree-profile RHS is strictly smaller.
  A rational enclosure proves a gap greater than `0.0042` without numerical
  evaluation of `2^(1/16)`.
- The witness remains below `rho_dB(K_6,2)=80/189`, so it does not refute the
  universal r=2 theorem.  It proves that coverage/submodularity plus the
  reversible vertex masses cannot be the missing extremal principle.
- **OPEN:** the exact stationary mean bound.  Any continuation of this route
  must use the full stationarity constraints of the representing coverage
  measure or the equivalent two-labelled current/tree cancellation.

## 2026-08-13 -- rank-summed dual/test-set reduction

- **PROVED:** the harmonic edge marginal is exactly
  `Delta_v h(S)=Pr(v in A, A intersects S = empty)`.
- Swapping the finite sums over the stationary dual set `A` and a rank-`k`
  test set `S` recovers the exact rank identities for `D_k` and `W_k` as one
  joint experiment `(A,v,S)`.
- **PROVED:** the centered first moment over uniform test sets collapses to
  `Z_P(A)=|A|(|A|-1)/(n-1)-sum_(u,v in A)P_uv`.  Reversibility turns this
  into a symmetric sum over internal original-graph edges, and its uniform
  average vanishes at each rank.
- Combining this with the exact concavity remainder yields the named
  stationary internal-edge deficit inequality `(SID)`.  It is exactly the
  remaining sign in the Green comparison: the stationary weighted internal
  deficit must be paid by the positive subset-mass dispersion from the same
  `(A,v,S)` coupling.
- **OPEN:** convert the rank-centered internal-edge deficit in `(SID)` into a
  two-copy/internal-edge square using full dual stationarity.  Pointwise and
  reference-only comparisons already fail, so the required cancellation is
  genuinely global.
