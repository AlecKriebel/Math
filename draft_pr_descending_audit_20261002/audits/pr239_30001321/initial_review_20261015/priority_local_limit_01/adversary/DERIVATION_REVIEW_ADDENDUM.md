# Adversarial checkpoint review of implication derivations

Reviewed: `../IMPLICATION_DERIVATIONS.md`, exact input hash and UTC recorded in
`DERIVATION_REVIEW_INPUT_PIN.json`. Scope is mathematical correctness of these
implications, not validity of the target i.i.d.-RWRE proof.

**Verdict:** no substantive mathematical error found in the parity shear,
stationary covariance calculation, weighted-measure bound (J), or hypothetical
pointwise-L2 residual summation. An initial imprecise polynomial-exponent sentence
was corrected in the pinned revision. A small variable-clock formula in the
newly added Section 8 needs the correction recorded in item 8 below; its main
balance obstruction remains valid.

1. **Parity and odd cell lengths.** `Y_t=(X_t+t)/2` has increments zero or one;
   the coordinate map is injective and preserves the i.i.d. scalar law. Each
   original real interval of length `M` becomes one real interval of length
   `M/2`. For odd integer `M`, lattice cardinalities alternate between the two
   adjacent integers. This causes no loss in (J). Directly counting geometric
   intervals gives at most `4R sqrt(N)/M+3` cells meeting the closed central
   window, with an absolute endpoint allowance. This formulation avoids any
   need to treat the sheared cells as equal-integer-length cells. For the
   asymptotic claim one may assume `M>=2` eventually; empty cells at smaller
   lengths contribute zero.

2. **Covariance parameters.** The displayed characteristic functions give the
   constant ratio `delta/a`, including its limit at zero. Thus the JRS
   covariance formula indeed yields variance `Var(p)/delta` and zero covariance
   at distinct sites in the sheared model. A deterministic environment has
   `Var(p)=0`, and then `F_(N,y)=1` almost surely at each of the finitely many
   relevant sites, so the stated zero case is valid.

3. **Unnormalized stationary ansatz.** (J) does not require `nu_N` to be a
   probability measure. Its support is contained in the finite support of the
   binomial weights, and `E nu_N(J)=b_N(J)`. The covariance identity gives
   `Var(nu_N(J))=c sum_(y in J)b_N(y)^2`. Consequently the single-cell inequality
   follows from Cauchy–Schwarz exactly as stated. No normalization factor is
   missing. For perspective, its total mass itself satisfies
   `E nu_N(Z)=1` and `Var(nu_N(Z))=c sum_y b_N(y)^2=O(N^-1/2)`, but that additional
   observation is not needed in the argument being reviewed.

4. **Central and tail cells.** If `A` is the number of central cells, their
   variance sums are at most `c sum_y b_N(y)^2`. Therefore
   `sum_central sqrt(c sum_J b_N^2) <= sqrt(A c sum_y b_N^2)`, giving exactly
   `C sqrt(R/M+N^-1/2)`. Cells outside this collection have every lattice site
   outside the central window, so their combined expected absolute discrepancy
   is at most twice the binomial tail. Chebyshev gives `C/R^2`. There is no
   double counting problem: central cells may straddle the boundary, but are
   charged fully in the central estimate. Constants can depend on the fixed law.

5. **Residual summation and tail interpretation.** The hypothetical pointwise
   second-moment bound gives `C R N^(-eta/2)` on the central sites. On other
   sites, positivity and the exact averaged law imply
   `E sum_outside |mu_N-nu_N| <= E mu_N(outside)+E nu_N(outside)
   =2 b_N(outside)`.
   Thus the global residual expectation is bounded by
   `C R N^(-eta/2)+C/R^2`, exactly as written. This remains valid even though
   `nu_N` has random total mass. Coarsening contracts the norm of a signed
   measure and requires no additional assumptions on cells or independence.

   The initial draft's sentence that Markov for a fixed-epsilon error costs the
   polynomial `N^(-eta/2)` should be read as a **central-window** statement. The
   pinned revision now makes this distinction explicitly. If only the
   displayed Chebyshev tail is used, optimizing the global bound with
   `R=N^(eta/6)` gives `O(N^(-eta/3))`. Alternatively the known binomial
   exponential tail allows `R=sqrt(A log N)`, giving
   `O(N^(-eta/2) sqrt(log N))+O(N^(-2A))`. Both are fixed polynomial rates;
   neither yields every power by this direct argument. With DG's extra log
   factor in the second-moment estimate, the analogous global discrete
   hypothetical bound is `O(N^(-1/6) log N)` plus an arbitrarily small polynomial
   tail. The report's stated `C R N^(-1/6) sqrt(log N)` is the correct central
   contribution.

6. **Continuum covariance.** Integrating the absolute `C/(1+|x-y|)` covariance
   over a length-`M` interval gives at most
   `2C[(M+1)log(M+1)-M]=O(M log(2+M))`. The continuum averaging statement is
   therefore correct and does not assert concentration beyond its evidence.

7. **Finite-valued approximation, added Section 7.** While the coupled paths
   coincide, the one-step disagreement probability is at most `h`; the union
   bound gives path disagreement at most `Nh`. Endpoint L1 distance is at most
   `2Nh`, and centering by the two corresponding annealed laws costs another
   `2Nh`. Thus the displayed `4Nh` discrepancy comparison is correct. Its
   distinction between a fixed approximating law and an `N`-dependent law is
   also correct; a fixed-law asymptotic theorem supplies no triangular-array
   uniformity without another argument.

8. **Variable clocks, added Section 8.** The uncentered local drift
   `c_(t,x)(2p_(t,x)-1)` and the direct balance obstruction are correct. For
   variable clocks, subtracting one deterministic velocity `v` produces exactly
   `c_(t,x)(2p_(t,x)-1)-v`. This is not generally a multiple of `p_(t,x)-q`;
   that simplification is correct for constant clocks, when
   `v=c(2q-1)`. Restrict the simplified formula to constant clocks, and use the
   exact expression otherwise. With fixed deterministic positive clocks and
   a nonconstant i.i.d. scalar law the centered drift remains random, so the
   claimed failure to establish pointwise balance still follows. The symmetric
   edge-identity objection with fixed deterministic clocks is also valid.

The exponent clarification and clock-formula correction do not affect the
report's principal conclusion or the proof of (J). The crucial distinction
between the stationary ansatz and the single-origin endpoint law is stated
correctly. No target-model counterexample is inferred from any of these estimates.

Final correction check: the subsequent revision now explicitly separates constant clocks (centered drift `2c(p−q)`) from arbitrary fixed deterministic clocks (centered drift `c_(t,x)(2p−1)−v`). This resolves item 8. The corrected revision hash and UTC are in `final_clock_correction_review` of the input-pin record. No mathematical correction remains outstanding in the reviewed implications.
