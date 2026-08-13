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

## 2026-08-13 -- exact stationary deficit generator

- **PROVED:** writing the internal deficit as the symmetric original-edge
  sum `Z(A)=sum_(i<j in A)e_ij`, one fair-geometric dual burst has an exact
  deletion/cross-creation/hole-pair-creation formula.  Its one-hole hit
  coefficient is `q(P_vi)` and its two-hole coefficient is
  `q(P_vi)+q(P_vj)-q(P_vi+P_vj)>=0`.
- **PROVED:** summing occupied targets gives the closed generator identity
  `LZ=-2Z+C1+C2` and stationary pair-renewal balance
  `2 E Z=E(C1+C2)`.
- **PROVED:** for the Green rank weight, the exact product law is
  `L(UZ)=U LZ+R_U`, where
  `R_U=sum_v E[(U_(h')-U_h)Z(A')]`.  Hence the SID left side is exactly one
  half of `E[U(C1+C2)+R_U]`; no frozen-rank replacement is legitimate.
- **EXACT OBSTRUCTION:** original-edge reversibility does not make the dual
  set chain reversible.  Stationary-flow symmetrization splits
  `E[U LZ]` into a mixed symmetric Dirichlet current plus a circulation
  current.  On the weighted three-path these are `-13/5400` and `41/5400`;
  on a regular weighted `K4` they are `43/34440` and `97/57400`.
  Therefore the symmetric mixed term changes sign and circulation is
  nonzero even for a regular original graph.  A plain two-copy
  carre-du-champ interpretation is exactly unavailable.
- **OPEN:** prove the literal circulation-corrected mixed-current inequality
  against the full subset dispersion.  The exact witnesses above still
  satisfy SID with gaps `2/45` and `1/574`, so they refute only the naive
  square representation, not universal fitness-two maximality.

## 2026-08-13 -- exact scalar SID gauge collapse

- **PROVED:** the full subset dispersion has an exact expression using the
  same fair-geometric burst as the dual generator.  With
  `F_h=sum_k c_k binom(h,k)`, `T_h=F_h-F_(h-1)`,
  `G_h=sum_k c_k binom(h,k)q(k/(n-1))`, and
  `Psi_h(y)=F_h-F_(h-y)`, its state integrand is
  `V(A)=U_h Z(A)+|A|G_h-sum_(v in A) E_v Psi_h(|J|)`.
- **PROVED:** for the radial potential `phi(A)=F_(|A^c|-1)`, the burst term
  is its exact generator increment.  The complete killed-Green equation is
  `|A|(G_h-T_h)=rho_K-|A|/n`.  Therefore, pointwise,
  `V(A)-U_hZ(A)=L phi+rho_K-|A|/n`.
- **DECISIVE SCALAR NO-GO:** combining this with the weighted-deficit
  generator gives
  `U(C1+C2)+R_U-2V=L(UZ-2phi)+2(|A|/n-rho_K)`.
  Hence the literal SID mixed current is only a coboundary plus the original
  mean-rank residual.  Any scalar coboundary-plus-PSD proof at this stage
  would already assume exactly the theorem it is meant to prove; no
  independent two-copy square survives the contraction.
- Per direction, stop further SID scalar algebra.  A live upper route must
  retain labelled full-pair information before contraction or switch to a
  different sufficient endpoint theorem.
