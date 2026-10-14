# Final shared PASS5: concentration audit receipt

14 October 2026. This records the final analytic review.

## Verdict and exact target

**Accept the nine final proof notes with the scopes below. The universal fixed-alpha diagonal-permuton theorem remains unresolved. The equivalent uniform 1324 anti-diagonal case also remains unresolved. No uniform-law counterexample has been established.**

`REVIEWED_INPUT_PINS.json` lists the exact current proof hashes and byte counts. The accompanying detailed acceptance reports record the all-size checks. `CROSS_REVIEW_PINS.json` verifies the complementary nine-note structural acceptance packet and every embedded dependency hash. The law remains exact uniform sampling from Av_n(alpha skew-sum 1), with alpha fixed before n. The topology remains weak convergence in probability of square-spread permutons. Rates or deterministic examples are not substituted for that target.

## 1. Positive actual-kernel results

`LOW_CHAIN_ACCEPTANCE.md` accepts the exact count 2^(c-1) of Av(213) states of size c with LIS at most two, and the positive weighted contraction giving growth at most eight for canonical paths of arbitrary length restricted to those states. The generating function is bounded for every z<1/8 by (t-1)/(2-t), with t=C(2z).

The two-boundary cut estimate keeps both full exterior counts. Therefore a consecutive low-chain run of mass at least epsilon*n and boundary mass at most delta times its mass has upper exponential rate

    -epsilon*[log(lambda/8)-Phi(delta)]

whenever the bracket is positive. The number of cells in the run is unrestricted; its entire internal path is already counted. The actual normalization factor lambda^n/a_n is retained as exp(o(n)). No conditional uniformity is imposed on a deleted remainder.

The immediate whole-path corollary is accepted: taking m=n and delta=0 gives

    limsup (1/n)log P(all canonical states have LIS<=2)
        <=-log(lambda/8)<=-log(81/64)<0.

This is exponential rarity of an actual restricted family, not a bound on unrestricted pair density.

The exact dense-edge family has K_inc=(pq/2)K between two height-two endpoint states. Thus small endpoint LIS cannot be used to dismiss their adjacent interaction. The proof retains actual allowed shuffles; their conditional uniformity given the complete state chain follows from the exact reconstruction, not from an independent-cell approximation.

`HEIGHT_THREE_ACCEPTANCE.md` accepts growth at most 6+2sqrt(5) for arbitrary-length paths whose cells have LIS at most three. Its generating series is finite even at the endpoint of the displayed contraction domain. Exact actual-kernel rows also prove that every pure exponential size weight fails to give a bounded transition operator beyond that domain. This is a sharp limitation of that weight family, not a lower bound on the restricted-path growth and not an obstruction to every possible operator norm.

## 2. Rectangle deletion, geometry and the unresolved sparse branch

`RECTANGLE_ACCEPTANCE.md` accepts the exact deletion of an occupied increasing-pair rectangle to a marked empty skeleton. Reconstruction has two binomial allocation choices and an essential avoidance indicator. Dropping that indicator yields only an upper bound; the supplied invalid insertion example verifies why it cannot be omitted in an equality or sampling law.

For every fixed c>0, the probability that some marked pair satisfies

    m log(lambda)-e(m,p)-e(m,q)>=c*n

is at most exp(-c*n+o(n)). This bound is uniform over all locations and sizes. In particular, macroscopic interiors with p+q<=m have a strict exponential penalty using lambda>27/4. This is a genuine new partial concentration estimate.

The fixed coarse-grid lemma gives a finite family of endpoint-cell witnesses for positive increasing-pair density. It covers an occupied core branch and a branch with quadratically many small-interior pairs, with Q fixed before n. Its constants and half-open boundary conventions check. It does not imply favorable strip contamination in the occupied branch.

The canonical comb family makes that distinction substantive: every rectangle with at least 20 interior points has unfavorable raw-allocation entropy, while the permutations have positive limiting increasing-pair density. This blocks the uncharged allocation shortcut; it leaves room for a sharper estimate of the true admissibility-weighted fibers.

`NEAR_EMPTY_ACCEPTANCE.md` accepts the final sparse supplement. Its actual canonical family has negligible fixed endpoint-cell prefixes, sublinear LIS, and Z_0=o(n^2) exactly empty increasing rectangles, yet Inc/n^2 tends to 2/25. Every pair has at most k+1=o(n) interior points. Therefore for every fixed theta>0 the normalized number of pairs with at most theta*n interior points still tends to 2/25. An estimate only at m=0, even combined with sublinear LIS, cannot close the sparse branch. These are deterministic insufficiency results; the examples may be exponentially rare under the exact uniform law.

## 3. General alpha: exact cut states, but no linear-width control

`GENERAL_CUT_ACCEPTANCE.md` accepts the exact diagonal-exposure state consisting of the two crossing endpoint orders and Boolean gridded closed-pattern descriptors of sizes at most |alpha|. The update preserves all comparisons needed to test a newly exposed forbidden occurrence. Its finite transition multiplicities count exposure histories exactly; there is no uniform law on compressed states.

For each fixed crossing-width bound K, the resulting finite transfer gives a rational counting series A_K. Direct-sum decomposition and its positive pole show I_K=1-1/A_K increasing to one. Adding an explicit new sum-indecomposable allowed block of width K+1 yields a strictly earlier pole. Hence

    lambda_K<lambda,       lambda_K nondecreasing,
    sup_K lambda_K=lambda.

Consequently exact uniform permutations have bounded crossing width at most K only exponentially rarely for every fixed K. The conclusion establishes divergence of the width scale, not its behavior divided by n. The rates have no proved uniform approximation as K grows.

The width-one completion example is also accepted: identical crossing coordinates and allocation data, but different closed interiors, give positive completion counts b_N(2143) and one, whose ratio is exponential. The repaired profile distinguishes them. Thus removing closed context can already lose an exponential factor at width one. No false alpha-free assertion for the lower crossing block is used.

## 4. Collective-window method limits

The folding construction has genuine actual canonical inputs and an explicitly exponentially large collision fiber. A clarification was required: identical turnaround-location markings concern the folded output, while original source coordinates can vary. The operative proof is the corrected derivative 0241b9c0…, accepted in `FOLDING_DERIVATIVE_ACCEPTANCE.md`; the earlier report remains preserved and must be read with this correction.

Even retaining all original turnaround coordinates leaves a fiber of size at least 2^(R*a)/binom(n,4R+2)^2. Its entropy rate tends to log 2/9 as first R and then W grow, while turnaround overhead tends to zero. This refutes recovery for the specified fold and retained records. It does not rule out all possible encodings. A successful low-overhead fold would lower-bound g_W and upper-bound the true gap, so it would not itself prove the lower-gap divergence needed by the earlier conditional adaptive criterion.

`QUADRATIC_MODEL_ACCEPTANCE.md` accepts the distinct monotone staircase comparison model. Its exact fixed-width growth is 4cos^2(pi/(K+2)), by an explicit concave entropy maximization. Its genuine gaps relative to growth four are asymptotic to pi^2/(K+2)^2 and hence summable. This proves that staircase geometry and positive boundary shuffles alone do not force harmonic gaps. It gives no estimate on the true 1324 gaps and does not invalidate the conditional adaptive theorem.

## 5. Source-version gate

A fresh primary-source check prevented a false height-three upgrade. Norton's arXiv:2608.20292v3 explicitly withdraws the earlier 10.617 and 10.466425 claims; its surviving stated value is 10.412263, below 6+2sqrt(5). Search indexing still exposed the withdrawn 10.617 abstract. The checked evidence is the versioned abstract, history and comments; this review does not certify the surviving preprint proof. See `NEW_LOWER_BOUND_STATUS.md` and `VERSION_STATUS_METADATA.json`, which contain only public source-status metadata and an authored explanation.

The positive height-two theorem continues to rely on the previously inspected BBEPP bound 81/8, so no new unreviewed external theorem enters its proof.

## 6. Verification and preserved scope

`FINAL_CHECKER_RECEIPT.json` independently compares four normal/optimized/double-optimized author report triples. Three triples are byte-identical. The general-cut triple has identical substantive records after removing its declared elapsed-time and optimization-level metadata. Embedded proof/checker pins are verified where present; the folding diagnostic does not contain an embedded proof pin, and is not represented as certifying the new source-coordinate entropy argument.

The pair checks cover 919 exact row shuffles, 28 dense-edge cases, 56 height-three coefficient comparisons and 216 marked-run bounds. Rectangle checks include 213162 deletion round trips and 30570 allocation records, of which 1524 are rejected by actual avoidance. General-cut checks include 53226 raw histories, 274001 prefix-edge observations and 288 finite observed-transfer coefficient comparisons. The independent geometry diagnostics additionally reconstruct the comb and near-empty examples. All are finite regressions; the all-size claims rest on the proofs, not finite-coefficient radius inference. This reviewer compared the frozen outputs and does not claim to have rerun the author scripts.

All public artifacts in this reviewer's PASS1 through PASS4 manifests were rehashed and remain unchanged. 

The missing result remains an actual completion-weighted bound for linear crossing width, or equivalently in the 1324 specialization an o(n^2*a_n) bound on the full increasing-pair coefficients. The accepted partial tails, exact transfer descriptions and method obstructions do not supply that final estimate.
