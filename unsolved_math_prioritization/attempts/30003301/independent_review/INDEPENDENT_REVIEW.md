# Independent adversarial review: 30003301

## Mathematical verdict

**PASS for the five-turn partial claims; the original target remains UNSOLVED after 5/5 author turns.** No claimed positive identity relation without an allowed pointed lift, no universal lifting theorem, and no certified nonabelian obstruction for the 48-factor genus-nine example are present. Those gaps are accurately disclosed.

The mathematical files TURN_1.md through TURN_5.md were frozen before review and are not revised by this audit. The reviewer did not coauthor their proof routes. The exact author-file hashes and final packaging-manifest hash are bound in REVIEW_MANIFEST.json. No novelty or priority is certified.

The portable manifest correctly excludes the complete pinned record, which remains only in the local working directory. I rechecked the exact manifest after initially confusing that local inventory with the publication list; no author correction was needed.

## 1. Exact target and source reading

The original OWR Question 13, printed p. 3189, and Korkmaz's fuller Problem 2.8 agree on independently lifting the prescribed individual positive twists to a surface with one marked point. The older statement explicitly assumes genus at least two. The target is not a boundary-fixed mapping class group, an arbitrary lift of the product, a simultaneous homomorphic splitting, or an achiral factorization.

For genus at least two the Birman kernel is the surface group and the point-pushing formulation used in the packet is appropriate. The comments on low-genus **mapping-class relations** do not establish a separate universal statement about all genus-one fibrations and their possible gluing data; no such extra geometric assertion is needed or certified here. An inessential curve has trivial twist in the point-marked setting, while a boundary-fixed convention would be different.

I read the April 2026 Hillman–Pedrotti preprint, including the local smooth/continuous arguments and ordered concatenation criterion, and visually checked its theorem page. The reversal bar on the conjugating loop is essential and is present in the source. Its inverse monodromy is also correct under the mapping-torus convention. The packet uses the smooth criterion existentially over all valid representations, rather than treating one displayed integer outside {0,1} as automatically decisive. The September seminar announcement is not used as an unqualified theorem.

Smith's Theorem 6.2 was checked with its sphere-base, nontrivial relatively minimal Lefschetz setting. Baykur–Hamada's primary published text was checked for the actual pointed relation, the positive 48-factor relation, Proposition 8, the seven needed table rows, the cap class and the spin/primitive-fiber facts. The signs in the relevant table were visually verified.

## 2. Point-pushing corrections and the integral lattice

The group expansion is correct before abelianization. Moving the point push past a twist applies that twist's automorphism, so the correction factors have exactly the displayed **prefix** action order. Abelianizing gives [w] plus the sum of prefix images of (I−A_i)[x_i].

For a nonseparating curve, the primitive integral homology vector and unimodularity of the surface pairing imply Im(I−A_i)=Z v_i. Every integral coefficient is realizable by a based loop. The prefix-transformed vectors are obtained from the original list by an integral triangular matrix with diagonal one. This proves equality of the two integral lattices, without assuming the vectors are linearly independent. Rational span or saturation cannot replace this lattice.

The transitivity statement for nonseparating curve lifts is valid: an ambient isotopy taking one curve to the other can be followed by an isotopy supported in the connected complement to return the image of the marked point to its original position. The resulting mapping class lies in the point-pushing kernel. The packet explicitly does not extend this argument to the disconnected complement of a separating curve. Its coset conclusion remains exact within the specified conjugation family and gives only a commutator residual, not a pointed identity.

## 3. Relative Heisenberg obstruction

The surface-group homomorphism is valid. In an independent upper-triangular-matrix calculation, [X,Y]=Z and [Y,X]=Z^−1, so the genus-two relator maps to the identity. The separating-cycle image is central of infinite order. Conjugation of the other handle generators by v or v^−1 therefore becomes trivial in the quotient, for either consistent twist-action convention.

Consequently every allowed twisted conjugate of v^m has image Z^m. The boundary class v² maps to Z², excluding **all** smooth possibilities m=0 and m=1, not merely one choice of conjugating path. The local map in xy coordinates is obtained from the preprint's sum-of-squares model by the stated linear change. It is continuous at the node, has the prescribed boundary winding and composes to the identity on the base. A smooth section cannot meet the critical point because differentiating its defining identity would force an identity differential through a zero differential.

The disk has nontrivial separating-twist monodromy, so this is a relative boundary-condition obstruction. No trivial cap is available for that one-twist word. It is correctly not promoted to a counterexample for the original positive identity relation. Adding a second identical positive cycle realizes v² with the two allowed local exponents both equal to one; this verifies the claimed failure of persistence under adding critical points.

## 4. Restricted positive-completion obstruction

The abelianization of the specified Heisenberg quotient has kernel generated by a−d and b−c. Their pairing is zero and their span has half the dimension, so it is Lagrangian. Pointwise invariance under each nonseparating twist forces its homology vector into that plane; primitive vectors can be tested against a class intersecting once. Separating cycles already have zero homology.

All pairwise products of transvection correction matrices then vanish. The product identity reduces to a signed sum of matrices v_i v_i^t equal to zero. Positivity of the twists makes the sign uniform, and positivity of the resulting real Gram sum forces every v_i to vanish. All essential vanishing cycles would be separating. Smith's no-Torelli theorem applies to the resulting nonempty essential positive sphere-base factorization and excludes it. Discarding inessential identity factors does not remove the original essential local twist.

This no-go result concerns exactly the pointwise-invariant quotient strategy. It does not prohibit nontrivial quotient actions, other quotients or all positive completions. The packet preserves those limits.

## 5. Ordered finite-quotient test

The automorphism hypothesis is substantive: the kernel must be invariant and the induced automorphisms must be verified on the surface generators. With those hypotheses, applying the quotient to the full smooth-extension expression yields exactly the displayed finite sets and prefix recursion. I checked the multiplication order independently in a semidirect-product model and in a separate S3 fixture with nontrivial automorphisms.

Both local exponents and all quotient conjugators are included. The quotient is surjective, so no loop-image choices are silently discarded. Exclusion of the actual cap image is a valid necessary-condition obstruction. Membership supplies no lift back to the infinite surface group and cannot establish a section. The author's finite Heisenberg fixtures certify only the recursion, not a mapping-class realization.

The killed-cycle quotient observation is also correct: each genuine twist acts trivially after normally killing its cycle, while the total point push acts by an inner automorphism. The residual image is therefore central. This is a constraint on that particular quotient obstruction; centerlessness or triviality of this image does not solve the stronger ordered smooth-extension equation.

## 6. The actual genus-nine example

The source relation has the form U Push(α) V=1 in the once-pointed group. Algebraically it gives VU=Push(α)^−1. The sign of the residual homology is consequently minus the displayed source class; lattice membership is unaffected by that sign. The cyclic shift is an actual positive identity factorization after forgetting the marked point, not a freely selected relative boundary word.

I independently transcribed the seven required 18-coordinate homology rows from the published table and recomputed the identity

    s = 2[a_3]+2[a_3']−4[w_3]−[z_2]−[b_3]+[b_4']−[b_4].

It holds over Z. Combined with Turn 1, it yields a simultaneous choice of legitimate conjugated twist lifts with zero **complete integral abelianization**. Thus no abelian quotient can exclude every allowed choice for that residual problem. This is an explicit compact certificate of the homological vanishing already established in Baykur–Hamada, not a section theorem or an independent discovery of primitivity.

The source's spin and primitive-fiber results give an integral algebraic dual D with even D² and D·F=1. The class D−(D²/2+1)F indeed has square −2 and pairs once with the fiber. Nothing in that arithmetic supplies an embedded representative of the required kind, much less an embedded section. The packet makes no such claim.

The full nonabelian based words and actions for all 48 vanishing cycles are still absent. A homology table cannot reconstruct those data, particularly the central corrections in a nilpotent quotient. The original universal question therefore remains unresolved.

## Checks and disposition

All four author programs were inspected and replayed. Their outputs reproduce byte-for-byte: 3,484, 2,335, 21,176 and 2,487 assertions, respectively. The independent checker passes 1,102 exact assertions/instances using free-word expansion, integral triangular generators, matrix Heisenberg calculations, a distinct finite-group fixture, the manually transcribed source data and the formal intersection pairing. Finite checks supplement the written proofs and primary-source audit; they do not certify a global monodromy word or settle the original target.

The frozen packet is suitable for a reviewed **partial-result draft**, with queue status **unsolved, 5/5**. Preserve all original-target gaps, the relative-versus-global distinction, the preprint/classical credits and the no-novelty disclaimer. No sixth research turn or new proof route is part of this review.
