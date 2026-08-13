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
