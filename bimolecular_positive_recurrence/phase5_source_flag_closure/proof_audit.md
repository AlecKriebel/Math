# Proof audit

## A. Scope and inherited input

The final theorem proves only the one-linkage-class statement.  It does not
claim the arbitrary multiple-linkage theorem.

The only stochastic result inherited without proof is nonexplosion of every
bimolecular weakly reversible stochastic mass-action system.  Standard
countable-chain equivalence between positive recurrence and a stationary
probability may be used after finite mean return is established, but the
proof establishes finite mean return directly.

Phase-I through Phase-IV artifacts are preserved.  No unproved global
source-rate hierarchy statement from Phase III or IV is used.

## B. Every use of compactness or subsequences

1. **Finite target stabilization.**  The carried target lies in the finite
   complex set, so it is constant on a subsequence.

2. **Coordinate dichotomy.**  For each integer coordinate, a bounded
   subsequence has a constant subsubsequence; an unbounded subsequence has a
   subsubsequence tending to infinity.  A finite diagonal extraction gives
   one common subsequence.

3. **Normalized logarithms.**  The vector
   \[
   \left(\log(r_i+1)/R\right)_{i\in I}
   \]
   lies in a compact simplex.  A convergent subsequence defines \(w\).

4. **Uniformization.**  Compactness is used by contradiction only.  An
   infinite failure set gives a divergent sequence.  The terminal source
   probability tends to zero, and the finite episode bound tends to
   \(-\infty\); this supplies a strict, not marginal, contradiction.

No compactness of reaction rates is invoked.  Rates are one fixed arbitrary
positive vector.

## C. Asymptotic-uniformity steps

For a fixed enabled bimolecular complex \(y\),

\[
\log(r+c)_y=R\,w\cdot y+o(R).
\]

This follows coordinatewise:

- a positive-weight divergent coordinate contributes
  \(y_i\log(r_i+1)+o(R)\);
- a zero-weight divergent coordinate contributes \(o(R)\);
- a fixed coordinate contributes \(O(1)\).

Only the selected source \(s\) and terminal \(c\) are used, and both are
proved enabled.  Their strict weight gap implies a falling-factorial ratio
diverging to infinity.  Arbitrary fixed rate constants multiply this ratio
by a finite positive constant and cannot change the conclusion.

## D. Boundary, face, and lattice cases

- The target complex of a fired reaction is present at the new state.
- A designated path is lifted as \(r+y_k\to r+y_{k+1}\); each source is
  therefore exactly enabled.
- Starting in a closed communicating class, every enabled lifted reaction
  remains in that class.
- Permanently absent species simply have fixed residual coordinate zero.
- Parity and other lattice restrictions are preserved because only actual
  reaction paths are used.
- No assumption is made that the whole orthant is irreducible.

## E. Moment, overshoot, and duration audit

- Episode jump count is deterministically at most \(|\mathcal C|\).
- Coordinate overshoot is deterministically at most \(2|\mathcal C|\).
- The current target supplies an enabled outgoing reaction at every live
  phase, so total rate is at least \(\kappa_*\).
- Physical duration is dominated by a Gamma variable of shape
  \(|\mathcal C|\) and rate \(\kappa_*\); all polynomial moments are finite.
- Potential increments are finite because each episode has finitely many
  finite branches.  No uniform third-moment or Lamperti expansion is needed.

## F. Markov-chain theorem audit

No vague random-time Foster theorem is cited.

1. Bounded episode-index inequalities are summed directly.
2. Nonnegativity of \(V\) and monotone convergence give finite expected
   episode count to \(K\).
3. Bounded episode length converts this to finite expected embedded jumps.
4. One jump from each finite-set state plus the hitting estimate gives finite
   mean return to \(K\).
5. The finite trace chain is proved irreducible.
6. A uniform finite-path minorization gives finite expected trace return to
   one state.
7. Uniform mean excursion duration over finite \(K\) converts trace steps to
   original jumps.
8. The lower bound on total CTMC rate converts jump count to physical time.
9. Nonexplosion excludes finite-time jump accumulation.

## G. Rate-monomial audit

The proof never replaces an edge and never compares products of independent
rate constants.  Rates occur only in:

- the fixed constant
  \(C_0=\log|\mathcal C|+\log(\bar\kappa_+/\bar\kappa_-)\);
- positive designated conditional probabilities
  \(q_e=\kappa_e/\bar\kappa_{\mathrm{source}(e)}\);
- exact source probabilities.

The only divergent comparison is between two falling-factorial source
factors whose normalized-log exponents have a proved strict gap.

## H. Common-invalid-argument audit

1. **Nonexplosion is not used as recurrence.**  Finite mean return is proved.
2. **No stationary measure is normalized.**  The proof constructs recurrence
   directly.
3. **No deterministic boundedness or persistence claim is used.**
4. **No bare “quadratic death dominates” assertion is used.**  Boundary
   triggers are encoded by carried targets and exact paths.
5. **Weak reversibility is not replaced by complex balance.**  Only strong
   connectivity of the one linkage graph is used.
6. **Total-count one-step drift is never asserted negative.**
7. **A favorable reaction's mere reachability is insufficient.**  Its
   probability and all competing outcomes enter the exact recursion.
8. **No truncation or simulation is evidence.**
9. **Embedded-to-CTMC conversion is explicitly bounded by
   \(1/\kappa_*\) per jump.**
10. **Coordinate faces are included by the exact lifted-path argument.**

## I. Computer-assisted claims

No computer-assisted assertion is load bearing in the universal proof.
The code verifies exact finite identities and performs adversarial
calibrations:

- exact target/source falling-factorial identity;
- exact source probabilities and entropy rewrite;
- equality of recursive and branch-enumerated episode rewards;
- exact finite top-availability/conservation classification;
- exhaustive 57,288-case three-species atlas;
- 100,000 random four-species cases in the development audit;
- calibration networks and inherited tests.

Floating point is used only to display finite logarithmic expectations in
calibrations, not to certify the universal sign.
