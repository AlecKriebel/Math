# Independent PASS4 structural and exact-law audit

Shared PASS4, 14 October 2026. Exact reviewed proof hashes and byte counts are pinned in `PASS4_ACCEPTANCE_RECEIPT.json`. This is an independent structural review.

## Verdict and scope

The six pinned notes below are accepted within their explicit scope. Their exact-class encodings, canonical normalizations, reconstruction and fiber bounds are sound. The adaptive-window theorem is conditional on the specified divergence hypothesis, which remains unproved. The deterministic spatial examples have no established positive probability under uniform avoidance. The universal target and the uniform 1324 limit remain unresolved.

No accepted PASS1, PASS2 or PASS3 artifact was changed by this review.

## 1. Terminal strips and the pointwise incoming-to-outgoing map

Reviewed: `pass4_two_sided_mark/TERMINAL_MARK_AND_POINTWISE_LIFT.md`, final hash beginning `18af51f2`. Structural Sections 1–3 are accepted.

An even terminal cell is the sole cell in the lowest occupied row, so it contains precisely the globally smallest a values. Reverse-complement takes it to the top a-value interval. Its actual pattern was S(A), and rc(S(A))=A^{-1}. An odd terminal cell is the sole cell in the rightmost occupied column, so it consists of the final a positions. Inversion again produces a top a-value interval with pattern A^{-1}. Inversion preserves Av(213), and both global symmetries preserve Av(1324).

Thus the terminal size is bounded by a first-cell statistic under one of two size-preserving class bijections. This is containment, not equality or reversal of the whole canonical chain. Forgetting parity creates at most two preimages.

The three-point prefix guard applies even when the remaining lower region is arbitrary. Old points retain all comparisons. The first and third new points cannot occur in a new 1324, respectively by value and by the number of predecessors. If the middle guard point is used, it must start the occurrence; its remaining three points must then be old top-interval points forming 213. That is impossible. The top a+2 values induce exactly P(A)=12 skew-sum A^{-1}, and adding the next value creates the required 213 witness. The first canonical state is therefore exactly P(A).

Removing the first three positions and choosing the parity recovers the input. P is injective. The exact sizes give the formal coefficient inequality `z ell_A <= 2 h_(P(A))`, hence the stated positive-z pointwise bound. The summed incoming mark has factor `2/(u^2 z^3)`, as obtained by replacing |A| with |P(A)|-2. This changes neither the exact finite uniform law nor the unresolved need to bound a product of completion factors.

The independent script `check_terminal_strips.py` tests all 19203 nonempty avoiders through size eight. It verifies both terminal strips, their symmetry containment, guarded avoidance, exact first state, inverse recovery, and the at-most-two fiber count. Its output is `TERMINAL_STRIP_CHECKS.json`. These are finite diagnostics; the preceding geometry establishes the all-size map.

## 2. General-alpha deletion count and actual spatial barriers

Reviewed: `pass4_general_alpha/GROWTH_PACKING_AND_SPATIAL_BARRIER.md`, hash beginning `c0e18d22`. The structural encoding, perfect-packing examples and metric calculation are accepted; the general growth/entropy argument was also checked independently.

For a fixed successful deletion size h, the canonical deleted position set, its value set, and the two standardized induced permutations recover every entry uniquely. The deleted pattern remains in Av(alpha skew-sum 1) by hereditary avoidance. The retained pattern is alpha-free by the chosen deletion. Thus the ambient count `binom(n,h)^2 a_h b_(n-h)` is a genuine upper count, not a false conditional uniform law.

The needed supermultiplicativity is justified: a pattern ending in its minimum is sum indecomposable, and an arbitrary nontrivial pattern cannot be both sum and skew decomposable. At least one sum operation therefore preserves each single-pattern avoidance class. The accepted frontier bound applies to alpha-free members, whose frontier sentinel is n+1, and gives the strict growth gap used by the deletion entropy estimate. Every successful deletion meets each occurrence in a disjoint packing. Conversely, the union of a maximum, or merely inclusion-maximal, disjoint packing meets every occurrence. These facts give the stated packing/deletion inequalities and event containment.

For alpha distinct from I_m, increasing-block inflation preserves the number of descents. A selected pattern cannot have more descents than its containing permutation, since every descent between successive selected entries requires one in a disjoint intervening segment. The inflated alpha therefore avoids alpha skew-sum 1, which has one more descent. Adding the prefix direct sum of k copies of alpha preserves avoidance. The prefix copies and the equal-level selections across the inflated blocks partition all entries into alpha occurrences.

The first m entries already form alpha, so the frontier is exactly m. Every smallest o(n) values eventually lies in the direct-sum prefix, where positions differ from values by at most m-1. At a cut corresponding to an alpha prefix with a crossing entry, the exact crossing count is k times that fixed prefix-crossing count, giving a fixed positive normalized mass.

For alpha=I_m, the separate construction `I_((m-1)k) direct-sum J_k` is valid. Any increasing m-subsequence must use the smaller-valued prefix; no later point can complete it with a new terminal minimum. Consecutive groups of m-1 prefix points paired with distinct tail points form a perfect partition into increasing m-subsequences. The frontier is m, including k=1, and smallest sublinear sets of values remain in identical prefix positions. A tail-midpoint cut has the claimed limiting crossing mass.

The metric constant is correct. For a permuton, c(t)=t-F(t,t) is 1-Lipschitz because an increment of the joint CDF on its diagonal lies between zero and twice the increment of t. A peak M therefore gives area at least M^2 under c. The identity `integral |x-y| = 2 integral c(t) dt` and the admissible test `|x-y|/sqrt(2)` give `d_BL >= sqrt(2) M^2`, yielding the displayed lower constant. The listed inversion-density limits are consistent with direct counts.

Finally, the upper-left crossing subset must itself avoid alpha: an equally numerous lower-right crossing set supplies a later smaller point which would complete any such occurrence to alpha skew-sum 1. This is an actual avoidance restriction, and explains why global perfect packings do not settle spatial localization. None of these deterministic examples is asserted to have nonnegligible uniform probability.

## 3. Quantitative fixed-window counts from the accepted one-point map

Reviewed: `pass4_window_gaps/QUANTITATIVE_WINDOW_GAPS.md`, corrected hash beginning `c66d6b4b`. The finite profile-union counting argument is accepted.

For each complete size vector, choose one maximizing local penalty deterministically. The maximum is positive because its first positive coordinate has predecessor zero. Consequently a trailing padded zero cannot be the selected coordinate. The actual selected cell is either first, handled by the uniform absolute frontier bound, or noninitial, handled by the accepted one-point rerooting with omitted-shuffle cost `binom(p+q,p)`.

The selected marked-object count dominates the subset with that full size vector; the output need not retain the input vector. All other old edge data are already preserved by the accepted inverse argument. There is no missing factor for the marked location or cell patterns. At most `(n+1)^K` padded size vectors exist, giving the displayed finite bound with prefactor `A_eta lambda (n+1)`.

The original submitted version cited the provisional three-point rerooting note. During review this was replaced by the actually accepted one-point proof and the corresponding sharper prefactor. The pinned derivative incorporates that correction.

The minimax recurrence has the right domain: its scalar penalty first decreases and then strictly increases, so a positive-level sublevel set is exactly the interval from zero to the positive root. Monotonicity of that root in its predecessor and entropy homogeneity give the inductive coordinate bound and the matching saturating vector. The exponential-in-K upper and lower bounds are consistent with the recurrence. Most importantly, only fixed-K growth is inferred; the growing-K vector factor and the coefficient-growth defect have not been dropped.

## 4. Adaptive-window exact entropy and conditional transfer

Reviewed: `pass4_adaptive_profiles/ADAPTIVE_WINDOW_ENTROPY.md`, hash beginning `3d1308f9`. The geometric entropy identity, marked-block count and conditional implication are accepted.

The two rays of boundaries of centered expanding intervals cover every adjacent edge exactly once. Each mass occurs in at most two edge endpoints, so total boundary entropy is at most 2 log 2. Zero padding agrees with clipped windows, including repeated full-profile windows whose boundary entropy is zero. A fixed finite divergent-partial-sum test therefore selects a block with a positive uniform score, if the stated certified-gap divergence hypothesis holds.

Cutting at the selected block gives three homogeneous canonical path fragments. Their counts retain both exterior factors `a_p` and `a_q` and the internal factor `b_(m,K)`. The prefix path determines the marked location. Restoring the two edges has cost at most `binom(a+l,l) binom(b+r,r)`, including a repeated endpoint for a singleton and factor one for a missing neighbor. Eligibility is determined by these three pieces, so it may be enforced before summing, or removed only after the uniform eligible-edge bound is taken. No interior-state uniformity is assumed.

The finite candidate set of caps K is chosen before n grows. Hence fixed-K coefficient upper bounds can be made uniform over that finite list and over m at least epsilon n. The entropy score cancels the certified internal loss with a fixed remaining margin. All location, mass and endpoint refinements cost only polynomial factors. The proof is a valid conditional exponential-tail theorem. It does not establish the divergence of the actual gaps or justify inserting growing K into a fixed-K asymptotic.

## 5. Actual canonical mountains and every bounded window

Reviewed: `pass4_adaptive_profiles/EXACT_CANONICAL_WINDOW_OBSTRUCTION.md`, hash beginning `e302b0e4`. Its actual realization and all-window quantifiers are accepted.

The increasing-state edge word puts all lower points in one consecutive block between the first upper point and the remaining upper points. It is 1324-free and supplies the greedy witness. Therefore the specified mountain is an actual canonical path, not merely a gridding. Its size is `3*2^m-4` and its central fraction exceeds and tends to 1/3.

For a fixed cap B and m>B, every center-containing window of width at most B has both exterior neighbors. Its endpoint/neighbor ratios agree exactly with the infinite geometric profile. The common normalization cancels in E/M. The stated AM–GM estimate and the geometric test vector show its boundary cost is strictly greater than the sharp local-reroot certificate V_K.

A window wholly on one side has an inward neighbor twice its inward endpoint mass a and total mass less than 2a. Its inward edge alone gives `E/M > H(1/2)`, even when the outer end is clipped by the finite staircase. Thus the note truly covers every nonempty bounded-width window, not only those containing the center. Zero-padding makes V_K nonincreasing, validating the larger-cap comparison.

The full mountain window is longer than the fixed cap and has zero boundary cost; it is correctly excluded from the bounded-window obstruction. The argument bounds what this particular lower certificate can pay. It does not upper-bound the true gap delta_K and does not imply a uniform-probability counterexample. The increasing central cell supplies the stated deterministic non-anti-diagonal witness.

## 6. Fixed-width calibration and the credited source construction

Reviewed: `pass4_window_gaps/FIXED_WIDTH_CALIBRATION.md`, hash beginning `f831a975`. Its labeled-path sandwich, two-cell growth and fixed-width use of the source construction are accepted.

A canonical path embeds in a K-state unrestricted path by appending empty states. Conversely, applying `P(A)=12 skew-sum A` to every state and the symmetric four-point guard to every edge gives a genuine canonical K-state path of size n+2K. The normalized pattern used at each common state is identical on its two incident edges; those edges interleave different coordinates, so they are compatible. The identity `S(P(A))=12 skew-sum S(A)` handles even edges. Canonical reconstruction and deletion of the fixed state and edge guards recover the full labeled input, including empty states. Thus the sandwich is exact, and constant shifts preserve growth for fixed K.

For K=2 the unrestricted path count is the domino count including empty cells. The primary Theorem 2 formula and its growth 27/4 therefore give g_2 exactly. The sharper three-point guard is also valid but unnecessary for this equality.

I independently inspected the primary PDF pages 13–14 for Theorem 9. The gridded count separates the number k of domino/connector units from their point scale. Holding k fixed and using an independent scale m preserves every component-interleaving restriction. There are k internal domino choices, k connector choices, and 2k-1 external interleavings, exactly as in the displayed formula. The fixed-width guard converts these distinct labeled records to distinct canonical permutations, so no division by the original gridding multiplicity is needed.

The balanced-domino rate, connector formula, binomial entropy and size `36mk+6k` yield the stated lower bound on g_(3k). The resulting upper bound on the true finite-width gap retains its positive constant term and does not falsely prove gap summability or adaptive sufficiency.

The credited source is Bevan, Brignall, Elvey Price and Pantone, *A structural characterisation of Av(1324) and new bounds on its growth rate*, Theorem 2, Proposition 7, Theorem 8 and the Theorem 9 construction. The retained PDF has 627368 bytes and SHA-256 `1264749e17f01005277e8acf1a7782e6c4e448fe1733ac6fbb29ec8bd125f26d`. Source formulas were checked directly; no priority claim is made for the new adaptation.

[Primary author manuscript, Theorem 9 proof](https://oro.open.ac.uk/68534/1/1324-staircase-els.pdf#page=13)
