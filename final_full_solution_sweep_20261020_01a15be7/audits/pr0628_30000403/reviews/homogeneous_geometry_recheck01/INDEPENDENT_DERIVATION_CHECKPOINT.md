# Independent derivation checkpoint (before prior-verdict inspection)

## Exact target and limitations

A geometrically transitive PGL2-homogeneous orbit F over a characteristic-zero field k, with finite faithful geometric stabilizer E, should have F(K) nonempty for some extension of degree at most two. If E is noncyclic, F(k) should already be nonempty. This concerns rational coarse points of F, not descent of an actual marked cover object. Applied to an inner coarse Hurwitz orbit, a faithful finite subgroup of target PGL2 is the cover-point stabilizer; it need not equal the larger stabilizer of the branch divisor.

## Construction and independently reconstructed bridge

Put H=PGL2 and G=[F/H]. Form X=[(F x P1)/H] with the diagonal action. Then X -> G is the universal twisted projective line. Over an algebraic closure, X is [P1/E]. The faithful action has a finite nonfree locus, so X has a nonempty open U with trivial inertia. Its coarse space Y is a smooth proper geometrically rational curve over k, and U identifies with an open Y0 of Y.

A point y in Y0(K) is an actual object of X(K), not merely a point of its coarse space. By the quotient-stack definition, it is an H-torsor P over K, an H-equivariant map P -> F, and a K-point of its associated Brauer-Severi conic C=P x^H P1. That point trivializes the H-torsor because a conic with a rational point is a split projective line. Choose a trivialization P=H: the equivariant map then gives an actual point of F(K). The same y therefore neutralizes the residual gerbe and kills the additional target-conic torsor obstruction. Neutralizing [F/H] alone would not suffice, so keeping the marked point in X is essential.

Every genus-zero curve Y has a point over an extension of degree at most two. More precisely, a k-line intersection in a plane-conic model gives a degree-two zero-cycle; a sufficiently general line avoids Y minus Y0, because k is infinite. A residue field of a point in this zero-cycle has degree one or two and gives y in Y0(K). This proves the upper bound.

For noncyclic E, Riemann-Hurwitz gives exactly three geometric branch points of P1 -> P1/E. Indeed each inertia order is at least two, so there are at most three; two branch points force a cyclic group, since 1/e1+1/e2=2/|E| and ei<=|E| force e1=e2=|E|. One branch point is impossible. The three-point branch divisor of Y is defined over k, regardless of its Galois permutation. Hence Y has an odd-degree rational divisor. A genus-zero curve with a degree-three divisor is split: subtract an anticanonical divisor of degree two to obtain a k-rational divisor class of degree one; Riemann-Roch supplies a rational point. Since k is infinite, Y0(k) is nonempty, and F(k) follows. This includes E=V4 without assuming that its three involutions or the normalizer split over k.

## Adversarial obligations still to inspect

Check existence/effectivity of F and of its quotient stack and coarse compression; verify base change and faithful inertia; ensure the Hurwitz fiber really is a descended geometric orbit and avoid a scheme-theoretic nonreduced-fiber shortcut. Authenticate the stated primary Bresciani bodies and their exact hypotheses. Compare old prior implications only after this checkpoint. Sharpness will not be independently verified in this review unless needed: it is logically distinct from the upper-bound compression mechanism.

No outside individual or agent has been contacted. No source body or prior priority verdict has been read in this review before this checkpoint. The candidate PROOF.md and RELEASE_CLARIFICATIONS.md were read to bind the target scope.
