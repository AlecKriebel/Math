# An initialized all-depth robust-predecessor criterion

Status: PASS5 conditional reduction. The quantitative hypotheses in Section 2 are unproved beyond the already accepted first cases. This is not a proof of the unrestricted conjecture.

## 1. Exact state notation

A state is taken immediately before an Angel move, with the current position translated to zero. Its finite pending set B consists of distinct pairs (p,t), where t>=1 is relative target time. Let W_k(B) be the exact unrestricted online predicate that the Angel can survive the next k moves against every intervening adaptive one-announcement-per-round Devil. The accepted recursion gives

    W_(k+1)(B) iff some immediately safe move has every Devil successor in W_k.

For an actual maximum-lead-H game, every before-move state satisfies the age-tail inequalities

    #{(p,t) in B : t>=j} <= H-j+1   for 1<=j<=H,
    no pair has t>H.                                  (1)

Indeed, any pair with target time at least n+j-1 before actual move n was announced in one of the H-j+1 rounds n+j-1-H,...,n-1. Distinct effective pairs have distinct announcement witnesses. In particular |B|<=H. Call states satisfying (1) H-admissible.

The W_k predicate depends only on pairs with relative target at most k and within their reachable cone. Ignoring later or unreachable pairs does not replace the adaptive quantifiers by an offline statement.

## 2. A quantitative geometric hypothesis

A simple sufficient all-depth hypothesis would be:

    (C_k) For every finite B with |B|<=k+14,
          W_k(B) implies W_(k+1)(B), for every k>=1.

Equivalently, every critical state satisfying W_k and failing W_(k+1) would require at least k+15 pending pairs.

The following weaker version is enough:

    (A_k) For every (k+14)-admissible state B,
          W_k(B) implies W_(k+1)(B), for every k>=2.

Here (C_k) implies (A_k), but the converse is not claimed. The age profile materially narrows the required geometry. For example, in (A_k) the old bombs at the newly inspected layer k+1 total at most fourteen, even though the complete pending set may have k+14 members.

Accepted base information:

- C_1 holds: with at most fifteen pending pairs, immediate viability implies two-move viability, by the accepted neighborhood expansion argument.
- C_2 holds: with at most sixteen pending pairs, W_2 implies W_3, proved in ../pass4_devil/EXACT_TWO_MOVE_INVARIANT.md and independently accepted.

These two cases do not establish any later case or an induction in k. No claim of A_k or C_k for all k is made here.

## 3. The nonvacuous initialization induction

**Conditional theorem.** If A_k holds for every k>=2, then the unrestricted Time-Bomb conjecture follows.

Start with the accepted infinite win for maximum lead fifteen. Proceed by induction on H>=16, assuming a deterministic win for maximum lead H-1. Put

    k=H-14.

First establish W_k(empty). In the unrestricted game through move k, every relevant effective announcement has target t<=k and is made at a round r>=1 with r<t. Its lead is t-r<=k-1<=H-1. Announcements with t>k or with unreachable positions have no effect on this horizon and can be replaced by harmless announcements. Thus the previously established maximum-lead-(H-1) strategy proves W_k(empty).

Now consider the maximum-lead-H game. Maintain W_k before every move. Each actual state is H-admissible by (1), so A_k upgrades it to W_(k+1). Choose a witnessing immediately safe move from the exact recursion. After every permitted new announcement the successor again satisfies W_k, because the recursion quantified over all announcements, an even larger set than the maximum-lead-H choices. The successor is again H-admissible by the actual announcement chronology. This establishes the invariant indefinitely and gives an infinite online maximum-lead-H strategy.

The induction proves a win for every finite H. Finally, each finite unrestricted horizon N only involves effective leads at most N-1. The maximum-lead-N strategy therefore wins that horizon. The accepted finite-horizon/finite-Angel-action compactness extraction produces one deterministic infinite strategy for the unrestricted game.

This proof does not require the H-dependent strategies to agree or have uniformly bounded memory. It does require the all-depth geometric hypothesis, which is presently missing.

## 4. Why an uninitialized large-depth claim is insufficient

It is not enough to show that, for each H, some unspecified large r has W_r=>W_(r+1) on the relevant states, or that a minimum critical-preload cardinality tends to infinity. The initial state must also satisfy W_r. If the empty game had a finite losing horizon, all W_r could be empty beyond it; implications and minima over empty critical classes would then be vacuous.

The previous-lead induction in Section 3 supplies initialization at the specified r=k=H-14. It cannot be omitted or replaced by numerical evidence at the first two depths.

## 5. Remaining obstruction

Known small-state geometry controls current/next layer bad-center sets. At higher depth the robust successor predicate contains repeated adaptive unions over new announcements and intersects them with earlier viable-move sets. It is not the static iteration of a single spatial majority operator. The separate FIXED_DEPTH_MASS_OBSTRUCTION.md rules out a universal unweighted mass-contraction bound even at arbitrary fixed depth and within age-admissible preload histories. It does not refute A_k or C_k.
