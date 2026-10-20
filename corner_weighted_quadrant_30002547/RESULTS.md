# Five-attempt research outcome: corner-weighted quadrant loops

Target: Albert–Bousquet-Mélou Conjecture 11, for every fixed real a>=−1. The weight counts linear NW and ES corners, and u marks half-length.

## Full-target status

**Not solved by these arguments.** The two remaining parameter intervals are

    (−1,−1/2) and (−1/2,0).

The negative endpoint a=−1 was already known. The results below must not be represented as a full proof or disproof of Conjecture 11.

## Proved results in this research

1. **All nonnegative parameters:** For every fixed a>=0, the radius is exactly (2+sqrt(2+2a))^(−2). Attempt 1 supplies a finite-state zero-drift argument and an exact weighted mirror injection into quadrant loops. It handles a=0 and proves the ordinary root limit as well.

2. **Signed upper growth bound:** For every −1<=a<0, the radius is at least the conjectured piecewise radius rho_*(a). Attempt 2 proves an exact signed quadratic-pencil identity and uniform complex-disk invertibility, yielding |Q_n(a)|<=e²(n+1)² rho_*(a)^(−n). It also proves a finite critical Abel limit, without asserting ordinary boundary convergence.

3. **Refined positivity assertion (P2) is false:** With fixed vertical projection N^13 S^13 and horizontal half-length 2, the complete quadrant-loop slice is

       13769+27300a+13741a² = 210−182(a+1)+13741(a+1)².

   This disproves the stronger assertion in ABM §6.3.1, not unrefined Conjecture 10 and not radius Conjecture 11. Attempt 3 gives a full family proof and independent exact enumerators. It also proves negative complete fixed-shuffle sums for each −1<a<0 and negative fixed-vertical sums for each −1<a<−3/5 when the vertical mountain is sufficiently long.

4. **Local nonnegative blocking cannot repair the signed model:** For every block length L, retaining the incoming direction N and displacement (−1,L−1) gives exact signed weight La<0. Attempt 4 proves that entrywise positivity of M² after forgetting displacement cannot provide an exact nonnegative block Markov model for any negative a.

5. **The transition point is resolved:** At a=−1/2, the radius is exactly 1/9, the critical Abel value is 3/2, and the first derivative tends to +infinity. Attempt 5 proves this by detecting the critical operator's failure of range at the origin, not merely its bulk noninvertibility. It also gives the exact projection formula for the critical Abel value on the lower branch.

## Files and reproducibility

- ATTEMPT_1.md through ATTEMPT_5.md contain the authored arguments.
- check_transfer_and_mirror.py and transfer_and_mirror_checks.json check local symmetry, mirror injectivity and weights, displacement obstructions, and initial exact Q polynomials.
- check_signed_pencil.py compares direct last-direction enumeration and the contracted macro-step recurrence with exact rational arithmetic.
- verify_attempt_3.py checks the family formulas through n=40 and independently enumerates all 54,810 shuffles of the explicit refined-positivity counterexample.

All scripts were run successfully on 2026-10-20 UTC. Finite checks are normalization controls, not substitutes for the asymptotic or counterexample proofs. No novelty or exhaustive current-literature claim is made.
