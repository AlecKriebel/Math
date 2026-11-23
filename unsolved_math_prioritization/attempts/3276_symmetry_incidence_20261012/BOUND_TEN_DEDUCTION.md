# Separate application of the accepted finite bound ten

This is a corollary of separately accepted premises. It does not replace the original structural proof or its through-nine premise, nor the earlier companion proof's historical bound-eight application.

## Premises

1. The [finite proof](FINITE_PROOFS.md), [full independent audit](FINITE_AUDIT.md), and [proof review](FINITE_PROOF_REVIEW.md) establish the target for every nonempty tournament of order at most ten with a common palette of at most three colors.
2. The [earlier incidence-deletion theorem](../3276_tournament_partials_20261012/STRUCTURAL_PROOFS.md), with its [review](../3276_tournament_partials_20261012/STRUCTURAL_PROOF_REVIEW.md), defines K(H) by repeatedly deleting vertices missing an incident color, or having fewer than two incoming colors, or fewer than two outgoing colors. The terminal set is deletion-order independent. Every induced-minimal counterexample in H survives in K(H), using the credited Georgakopoulos–Sprüssel incidence requirements.
3. The [third-edition structural proof](../3276_interval_composition_20261012/STRUCTURAL_PROOFS.md) and [review](../3276_interval_composition_20261012/STRUCTURAL_PROOF_REVIEW.md) give exact uniform colored-substitution reachability, source, and cyclic-rainbow formulas, with a recursive quotient-core theorem parameterized by a known finite bound b.

## Corollary A Whole incidence core at most ten

If H is nonempty, has no directed cyclic rainbow triangle, and |K(H)|<=10, then H has an outgoing universal monochromatic source.

Proof. Otherwise choose a nonempty induced-minimal counterexample D in H. The containment theorem gives V(D) subset K(H), so D has order at most ten. Premise 1 excludes D, contradiction. If K(H) is empty, containment alone is contradictory. The proof does not merely lift an arbitrary source found in the core. QED.

## Corollary B Finite recursive quotient-core certificates

Take a finite rooted uniform colored-substitution tree with singleton leaves. Each internal node has a quotient on at least two vertices, one nonempty child per quotient vertex, and all cross-block arcs uniform in direction and color as prescribed by that quotient. Suppose every internal quotient is cyclic-rainbow-free and has incidence core at most ten. Then the tournament at the root is cyclic-rainbow-free and has an outgoing universal monochromatic source.

Proof. Corollary A supplies a source of each quotient. Leaves are rainbow-free and have a source. Induct upward through the finite tree. Exact cyclic-rainbow transfer preserves the first property. The substitution source formula produces a parent source from a quotient source and a source in the selected child. The induction reaches the root. This is the accepted parameterized theorem at b=10, with its finite premise now supplied separately. QED.

No equal-size blocks, canonical decomposition, or root-order bound is imposed. Empty-core quotient certificates need no finite-search premise. Positive same-color return paths in the quotient can give additional sources according to the exact formula, but the sufficient conditions above need not use that extra possibility.

## Residual necessary conditions

Every induced-minimal counterexample has order at least eleven, is colored-prime, and has its full incidence core. If its color-preserving automorphisms act transitively, the new structural theorem rules it out. If it instead has a fully vertex-transitive group of global-color-permuting automorphisms, its order is odd and divisible by nine, and still at least 27. The original through-nine premise already gives that same lower bound; through ten adds no stronger symmetric divisibility conclusion.

Accepted strict-periodic lengths remain only three, six, and nine. Arbitrary strict periodic length twelve and above remain unexcluded. No relationship between a periodic word and full-tournament symmetry is assumed. General order eleven and above remains unexcluded by the general finite bound, and the unrestricted conjecture is unsolved.
