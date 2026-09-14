# Adversarial debt-bound check and repair

Checkpoint: 2026-09-14 14:55 UTC. Stage 2 contribution: left occupation and bad debt.

The Appendix A.28 barrier is `Y_k = 2(k+1)/(3k(k-1))`, for bad ranks `2 <= k < N`. With the actual A.16 rewards, the direct consequence of the occupation bound is

`D <= Y^T(-g^b) = sum_{k=2}^{N-1} 4(k+1)/(3k(N-2)) g^a_k`.

This is not the printed A.31 upper bound

`sum_{j=1}^{N-2} 4(j+2)/(3(j+1)(N-2)) g^a_j`.

The two sums differ; the first exceeds the second at N=4 by exactly 1/360. This falsifies the implicit identification of these sums, but does not falsify A.31 itself. The existing exact verifier checks the bad/good reward ratio and Y residual separately; these checks do not supply the missing inequality.

A sharper supersolution repairs the implication while preserving the printed beta certificate:

`Z_k = 2/(3(k-1))`.

For the actual `B = Q^T`, subtracting the upper bound `1/[k(k-1)]` on the actual bad source gives the residuals:

- Interior, `2 < k < N-1`: `(2k-3)/(3Nk(k-1))`.
- Bottom, `k=2`: `1/(3N)`.
- Top, `k=N-1`: `(N-3)/(3N(N-2)(N-1))`.

These are positive for every N>=4. The bottom and top formulas use the actual absent-neighbor conventions. The Lean proof checks the concrete matrix actions and rational residuals, proves the actual recursive source bound through `gradient_bounds`, and transfers the inequality through the proven nonnegative true inverse. It obtains

`(s^b)^T (I-Q)^(-1) <= Z^T <= Y^T`.

The sharper barrier has the exact reward pairing

`Z_k (-g^b_k) = 4/[3(N-2)] g^a_k`.

Binomial reflection gives equality of the sum of good rewards over ranks 2..N-1 and 1..N-2. Since `(j+2)/(j+1) >= 1`, this proves the printed A.31 debt upper bound. The same sharper occupation inequality also proves the printed A.30 lower bound on the actual Schur occupation, including the top good rank at which the D transition is absent.

This is an alternative proof within the manuscript assumptions. It is not an axiom or a conditional replacement of the desired bound. The principal code is `SymmetricSector/LeftDebt.lean`.

Exact diagnostic comparisons (discovery checks, not proof dependencies) used the independently reconstructed rational Q block and exact linear solves. The values of actual debt / printed bound, rounded only for display, were 0.4668907563 at N=4, 0.5405272816 at N=5, 0.6866728310 at N=10, 0.7315396629 at N=40, and 0.7421061932 at N=100. Every comparison was made before rounding. The sharper Z bound divided by the printed bound was respectively 0.72, 0.7567567568, 0.8488053850, 0.9535452323, and 0.9805863708.

Independent cross-check of `BlockActions.lean`: the Q transpose row has diagonal `(N(k-2)+k)/(2kN)`, lower coefficient `(k-1)(k-2)/(2kN)`, and upper coefficient `(N-k-2)/(2N)`. These agree with the actual `coefficientK` bad/bad restriction. At k=N-1 the formal upper coefficient is negative, but the absent coordinate is identically zero; no proof replaces it by a nonnegative coefficient. At k=2 the lower coefficient vanishes. D transpose selects the same zero-based bad coordinate at coefficient 1/N, so it connects good physical rank j to bad physical rank j+1, and the top good rank has no such coordinate. The S/C/D/Q action proofs expand the finite selector sums and depend on no computed-answer axioms. No translation discrepancy was found in those actions.

Verified checkpoint: 2026-09-14 14:55:19 UTC. `lake env lean -o .lake/build/lib/lean/SymmetricSector/LeftDebt.olean SymmetricSector/LeftDebt.lean` succeeded. Every principal theorem (`leftBarrier_supersolution`, `leftOccupation_le_barrier`, `phaseEll_lower`, `phaseDebt_le_printed`) reports exactly `[propext, Classical.choice, Quot.sound]`. Completion estimate for this bounded Stage 2 left-occupation/debt subtask: 100%. This estimate does not assert completion of the parent all-order positivity proof or the physical quadratic-form identity.
