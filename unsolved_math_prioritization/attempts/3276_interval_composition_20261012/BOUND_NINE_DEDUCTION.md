# A separate deduction from the accepted finite bound nine

This is an authored mathematical consequence of two independently accepted results. It does not replace or rewrite the original structural proof or its historical bound-eight application.

## Premises

1. The separately accepted finite search establishes the target for every nonempty tournament of order at most nine, with a common palette of at most three colors. Its complete proof and independent review are in [FINITE_PROOFS.md](FINITE_PROOFS.md), [FINITE_AUDIT.md](FINITE_AUDIT.md) and [FINITE_PROOF_REVIEW.md](FINITE_PROOF_REVIEW.md).
2. The accepted incidence-deletion theorem defines K(H) by repeatedly deleting a vertex missing an incident color, having fewer than two incoming colors, or having fewer than two outgoing colors. The terminal set is independent of deletion order. Every induced-minimal counterexample contained in H survives in K(H), using the credited Georgakopoulos–Sprüssel incidence results. The [complete earlier proof](../3276_tournament_partials_20261012/STRUCTURAL_PROOFS.md) and [its review](../3276_tournament_partials_20261012/STRUCTURAL_PROOF_REVIEW.md) remain intact.
3. The [complete structural proof](STRUCTURAL_PROOFS.md), Theorems 2–5, gives exact uniform colored-substitution formulas and a recursive quotient-core theorem parameterized by an independently known finite bound b. Its own historical b=8 application remains unchanged. The [independent structural review](STRUCTURAL_PROOF_REVIEW.md) accepted this parameterized statement without using a provisional order-nine premise.

## Corollary A: whole incidence core of size at most nine

If H is nonempty, has no directed cyclic rainbow triangle, and |K(H)|<=9, then H has an outgoing universal monochromatic source.

Proof. Otherwise choose an induced-minimal counterexample D within H. The source-dependent containment theorem gives V(D) subset K(H). Hence D is nonempty and has order at most nine. Premise 1 excludes such a counterexample, contradiction. When K(H) is empty, containment alone is already a contradiction and the finite bound is unnecessary. This reasoning does not infer the result merely from finding a source of the core. QED.

## Corollary B: arbitrary finite recursive quotient-core certificates

Consider a finite rooted colored-substitution tree with singleton leaves. Each internal node has a nonempty colored quotient with at least two vertices, one nonempty child for each quotient vertex, and cross-block arcs uniform in both direction and color according to the quotient. Suppose every internal quotient has no directed cyclic rainbow triangle and incidence core of size at most nine. Then the root tournament has no directed cyclic rainbow triangle and has an outgoing universal monochromatic source.

Proof. Corollary A supplies a source of every quotient. Every leaf is a source and has no cyclic rainbow triangle. Induct from the leaves toward the root. Exact cyclic-rainbow transfer preserves rainbow-freeness, and the uniform colored-substitution source formula supplies a source of each parent from a quotient source and a source in its selected child. The tree is finite, so the induction reaches the root. This is precisely the accepted parameterized theorem with b=9, now justified by the separate finite acceptance. QED.

No equal-size blocks, canonical decomposition, or bound on root order is assumed. If every quotient core is empty, the same proof requires no finite computation. Positive monochromatic quotient return cycles may additionally make vertices sources even when the chosen factor has no internal source, as the exact formula states; the sufficient recursive hypothesis does not require using that extra possibility.

## Residual necessary conditions

Any induced-minimal counterexample has order at least ten and is colored-prime: it has no proper nontrivial module uniform in both direction and color. It has all three incident colors and at least two colors in each direction by the credited source dependencies. These conditions do not exclude colored-prime large-core cases.

The separately accepted periodic cycle lengths are still only 3, 6 and 9. A strict repeated-three-distinct-color obstruction cycle, if one exists, therefore has length at least twelve. This is inherited periodic scope, not a new periodic-length result and not a general-order-twelve result. General order ten and above and periodic length twelve and above remain unexcluded here. The target remains unsolved. No novelty claim is made.
