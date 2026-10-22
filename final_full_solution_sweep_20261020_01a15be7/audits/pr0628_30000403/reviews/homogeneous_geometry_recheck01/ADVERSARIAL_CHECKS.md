# Adversarial checks and controls

These checks were performed after the independent derivation checkpoint. They test the implication rather than treating the old priority disposition as evidence.

| Potential failure | Check and result |
|---|---|
| The Hurwitz fiber is not literally H/E as a scheme. | Use the Galois-stable reduced geometric orbit descended to k; a point of that orbit still lies over x. The proof needs no assertion about possible extra scheme-fiber structure. Closed: no gap. |
| A coarse rational x need not yield a Galois-stable orbit. | A geometric quotient has one geometric orbit in each geometric fiber, and x is fixed by Galois. Hence the orbit is fixed. Closed: the geometric-quotient hypothesis is essential and is included in the candidate. |
| The wrong stabilizer is used. | E is the stabilizer of the inner coarse cover point in target PGL2. It is contained in, but may differ from, the branch-divisor stabilizer. The auxiliary construction uses E. Closed. |
| The actual cover stack has an ineffective center. | R is formed from the coarse orbit, so its inertia is exactly E⊂PGL2. No actual-cover descent assertion is deduced. Closed within the stated scope. |
| A general algebraic structure is not really present. | U→R is a finite-gerbe family with geometric fiber P1 and faithful inertia. These are the precise inputs of the authenticated 2023 Lemma 6. The normality/separatedness assumptions hold for P1. Closed. |
| The genus-zero compression may not descend or may be singular. | The explicit semilinear action on P1/E gives effective descent of a smooth projective curve. It also descends the nonfree divisor. Closed. |
| A rational point of a coarse space may not lift to a stack object. | Only Y0, the nonempty locus of trivial inertia, is used. Over Y0 the stack is an algebraic space and is its own coarse space. Closed. No claim is made for an arbitrary excluded point. |
| Gerbe neutrality might leave a nontrivial PGL2 torsor. | Correct as an objection to a weaker argument. The object of U also has a point on the associated conic; this kills the particular torsor. Negative control below confirms why this extra datum matters. Closed for the actual argument. |
| No low-degree point avoids the exceptional locus. | A general k-line of the anticanonical plane model avoids all excluded points and tangencies. Such lines form a nonempty open in a projective plane over an infinite field. Closed. |
| V4 has a twisted S3 action with no split normalizer section. | The auxiliary branch divisor still has degree three and descends as a whole. It splits the conic even when its Galois action is transitive. No normalizer section is assumed. Closed. |
| Noncyclic quotient branch count secretly uses classification. | Riemann–Hurwitz gives b≤3; b≤1 is impossible, and b=2 forces E to fix a point and therefore be cyclic in characteristic zero. Thus noncyclic means b=3 without the subgroup classification. Closed. |
| The branch divisor used is confused with the original cover branch divisor. | The degree-three divisor is the branch locus of auxiliary P1→P1/E. It is distinct from the original r-point branch set. Closed. |
| A conic has odd-degree divisor but no rational point. | Riemann–Roch applied to O(B)⊗ω, degree one, gives a rational effective divisor of degree one. Closed. |
| The cocycle may carry an E-valued defect. | It does before marking q. At a free q the joint stabilizer of (p0,q) is trivial, so bσ σ(bτ)=bστ exactly. The displayed calculation checks directions and removes the defect. Closed. |
| Arbitrary characteristic-zero k could invalidate continuity or open-point existence. | All finite-type descent data are defined over a finite extension; k is infinite and perfect. No arithmetic finiteness assumption is used. Closed. |
| Bounding [K:k] does not bound the closed-point degree. | The image residue field embeds in K, so its degree is at most [K:k]. Closed. |
| The primary source only proves a divisor-specific claim. | 2022 Proposition 2 states arbitrary finite étale gerbes; 2023 Lemma 6 and Theorem 2 provide the general-family framework. Their full bodies were read. Closed for the upper-bound implication. |
| Prior literature may not contain the exact sharpness example. | This review does not certify historical sharpness priority or coordinate novelty. It must be combined with the separate original-source sharpness audit for an all-parts priority verdict. Explicit scope limitation, not a gap in the upper-bound proof. |

## Negative control: gerbe neutrality alone is insufficient

Let k=R and C be the smooth conic X²+Y²+Z²=0. It has no real point because a sum of three squares of real numbers can be zero only when all coordinates vanish. Let F=Isom(P1,C), a nontrivial PGL2-torsor. Then E=1 and [F/PGL2]≅Spec R is neutral, but F(R) is empty. The associated family U is C itself, so it has no free-open real point. This control falsifies the tempting shortcut “neutral residual gerbe implies an ordinary point of F” and verifies that the extra conic-point step does real work. C splits over C, a degree-two extension, consistent with the theorem.

## Exact V4 control

On P1 take E={z,−z,1/z,−1/z}. Its quotient is represented by t=z²+z^(-2). Substituting −z,1/z,−1/z leaves t unchanged. The four zeros of dt/dz=2(z⁴−1)/z³ have images 2 and −2; the poles at 0 and infinity have order two, with image infinity. Thus the auxiliary quotient has precisely the three branch values {−2,2,infinity}, each with inertia two. Riemann–Hurwitz reads 2−2/4=3(1−1/2). The value t=0 is outside the branch locus, and its four preimages satisfy z⁴+1=0 with trivial E-stabilizers.

After arbitrary twisting, the three branch values may be permuted, but the whole reduced degree-three divisor remains defined. This is exactly the Galois-invariant datum the proof needs; individual rational branch values are unnecessary. This control checks the V4 geometry, not the general descent theorem by numerical sampling.

## Deliberately unsupported extensions

No conclusion is drawn for actual marked cover objects, non-faithful families before rigidification, positive characteristic with wild stabilizers, a quotient whose fibers contain several geometric orbits, pointwise optimality, or optimal bounds after fixing every data set. Changing to any of those targets would require new work and could invalidate a bridge used here.
