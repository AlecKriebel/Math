# Independent algebraic mechanism and falsifying diagnostics

This body is recorded before candidate or reviewer reading. All examples here are algebraic diagnostics, not realized knots.

## Universal finite graded lemma

Let V and W be finite-dimensional bigraded vector spaces over a field k, and f:V->W a degree-(0,0) linear map. If g f=id_V for some linear g, then f is injective: f(v)=0 implies v=g f(v)=0. In each bigrading b, f restricts to an injection V_b->W_b, so dim(W_b)-dim(V_b)>=0. If the finite total dimensions agree, their sum of nonnegative deficits is zero. Each deficit is zero; every restricted map is surjective, hence f is a bigraded isomorphism. The inverse preserves bigrading. Moreover g must equal f^{-1}, so f g=id_W even if g was not initially assumed graded.

A graded-isomorphism hypothesis implies total-dimension equality, but the latter already suffices under the given degree-zero injection. Conversely, mere abstract equality of the groups does not certify that a specific f is injective: diag(1,0):k^2->k^2 is singular. Split injectivity alone permits a nonzero complement: V=k^2, W=k^3, inclusion and projection give g f=id but f g!=id. These are necessity tests, not counterexamples to the lemma.

Finiteness is essential. On countably generated vector spaces with basis e_n, f(e_n)=e_{n+1} and g(e_0)=0, g(e_{n+1})=e_n give g f=id and equal infinite dimensions, yet f is not onto. The same field/coefficient convention matters. Over Z, multiplication by 2 has equal ranks and is injective but is not onto (and is not split). The split inclusion Z->Z plus Z/2 has equal ranks and still has a nonzero torsion complement. Over finite-dimensional vector spaces these failures disappear. V=W=0 is a valid degenerate lemma instance, but standard knot Floer homology is not thereby asserted zero.

A grading shift also matters: k in degree (0,0) maps isomorphically to k in degree (1,0) as an ungraded space, not by a degree-zero graded isomorphism. The actual annular map's normalization must be read from a primary theorem.

## Inverse linear map does not supply a reverse geometric arrow

Take the two-element partial order a<b. Regard it as a category with identities and one arrow a->b. Send both objects to the same one-dimensional bigraded vector space and every available arrow to the identity linear map. Every represented arrow is a split isomorphism. There is no arrow b->a and the two objects remain distinct. The source relation is already antisymmetric, so that property cannot repair the missing reverse direction.

This functor is even faithful on each hom-set (which is empty or a singleton). Fullness or some other inverse-lifting assertion would be needed to recover a reverse arrow from the linear inverse. That is not implied by split injectivity, equal ranks, equality of groups, or faithfulness alone. Matrix inverses in the target category are not automatically images of admissible source arrows.

For an actual ribbon annulus C, its time reversal always supplies an ordinary smooth concordance. A ribbon movie uses births (index0) and saddles (index1), but no deaths (index2). Reversal changes index j to 2-j, introducing deaths when births occur. The reversed map may supply the split left inverse in Floer theory while the reversed surface is not a ribbon concordance. A different reverse ribbon presentation cannot be inferred from its induced map. If actual ribbon concordances exist both ways, the primary antisymmetry theorem would imply knot isotopy; an algebraic reverse is insufficient.

## Equal homology is not a filtered-chain or geometric classification

Even equal bigraded associated-graded homology need not classify a filtered chain complex. Consider generators x,z of chain degree1 with filtrations1,0 and generator y of chain degree0 with filtration-1. Compare d(x)=y,d(z)=0 with d(x)=0,d(z)=y. Both associated-graded differentials vanish, so the associated-graded homology tables agree. Both total homologies have dimension1 in degree1. In the first complex, the surviving class is born at filtration0; in the second at filtration1. No filtration-preserving chain-homotopy equivalence preserving the inverse exists, since it would identify these induced homology filtrations. This is an abstract complex; no knot-Floer realizability or symmetry conditions are claimed.

Mutation or any other operation must not be substituted for the conjunction of actual ribbon concordance and equal HFK. Equal HFK alone may fail to detect knot isotopy, but a knot example additionally needs the prescribed geometric relation. Ordinary concordance is weaker than ribbon concordance. A mutant pair can have different HFK as well, so no blanket mutation-invariance hypothesis is adopted.

## Exact remaining gap

The strongest deduction from the expected primary split-injectivity theorem and rank equality is that the forward HFK map is an isomorphism and its reverse ordinary-concordance map is the linear inverse. A theorem that such an isomorphism forces reverse ribbon concordance or knot isotopy would address the central geometric difficulty. Without a genuinely new mechanism, transferring to that unsupported rigidity statement is a blocked route, not a solution.
