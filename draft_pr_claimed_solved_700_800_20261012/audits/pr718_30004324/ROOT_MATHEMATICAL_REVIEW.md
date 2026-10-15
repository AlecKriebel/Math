# Independent root review of PR718 / 30004324

Review date: 2026-10-12 PDT. Immutable candidate head:
`8edfe0bf37d07814c5503107b9029e506b6046ea`.

## Claim and acceptance boundary

For a smooth integral projective n-fold X, n>=1, over an algebraically closed
field of arbitrary characteristic, positivity of the relative tangent-bundle
Seshadri constant at one specified closed point x implies X is projective
n-space. This is the exact conjecture stated in Fulger's OWR53/2019 contribution
(printed p.3289) and Fulger--Murayama Conjecture4.9 in the final-numbering
manuscript. Fano, globally nef tangent bundle, general point, characteristic
zero, and uncountability are not additional assumptions.

The root has read the whole candidate proof and inspected the primary
conjecture and critical imported statements. No historical AI geometry report
was used to substitute for checking the proof. Two fresh reviewers separately
challenge the geometric and numerical mechanisms. Their written verdicts are
required before promotion.

## Step-by-step mathematical assessment

1. **Curve restriction.** FM21 Example3.20 and Corollary3.21 give the
   infimum over normalized curves with the multiplicity denominator. The
   positive-characteristic normalized Frobenius slope is indispensable on
   general curves, but for a split bundle on P1 it equals the smallest degree.
   Therefore each normalization of a rational image through x has every
   tangent splitting degree at least one. The determinant positivity is a
   consequence; it does not replace the least-slope hypothesis.

2. **Rational curve at the specified point.** FM21 Corollary4.6, including
   its proof (p.16), explicitly produces a rational curve through the same
   x, using bend and break. This is stronger than merely taking an arbitrary
   very free curve on a separably rationally connected variety. Only the
   former is used. The final source was retrieved independently and its
   528251 bytes match the candidate's recorded SHA-256.

3. **Absolute ample-degree minimum.** Positive integer degrees have a
   minimum across all rational images through x. Geometric-field stability
   follows from the degree-bounded pointed Hom scheme and existence of a
   closed k-point in a nonempty finite-type scheme over algebraically closed
   k. A specializing map can be a cover, but its image degree is at most
   the map degree, so it still contradicts minimality. No general-position
   or uncountability argument is needed.

4. **Boundary elimination.** A path from the marking through contracted
   components reaches a nonconstant component whose image contains x.
   Degree additivity and the absolute minimum force exactly one nonconstant
   component, birational to its image. Every attached contracted subtree
   with t vertices and at most one marking has at most 2t special points,
   contradicting the stability requirement of at least 3t. This argument
   would fail with two markings, which is explicitly excluded.

5. **Inertia and projectivity in positive characteristic.** A birational
   normalization has trivial geometric automorphisms and no nonzero
   infinitesimal automorphisms killed by its generically injective
   differential. Finite stabilizers are thus the identity even in wild
   characteristic. The finite inertia algebra's split augmentation ideal
   has zero geometric residue fibers and vanishes by Nakayama. Trivial
   inertia gives an algebraic space. The actual proper evaluation fiber
   maps properly and quasi-finitely to the full projective coarse scheme;
   therefore it is a scheme finite over that coarse scheme and projective.
   This does not assume closed-fiber base change for coarse moduli.
   Abramovich--Oort Theorem2.8 and Section2.5 directly supply the proper
   stack and full projective coarse scheme in this characteristic range.

6. **Actual universal curve.** Restriction of the stable-map universal
   curve to an integral reduced projective component gives a smooth
   proper P1-family with a genuine section contracted to x. The section
   is a relative effective Cartier divisor of degree one. Its line bundle
   provides a rank-two pushforward and realizes the family as a projective
   bundle. Smoothness over the reduced base gives a reduced total space;
   flatness and geometrically integral fibers make it integral.

7. **Covering.** Every rational normalization through x is very free.
   Vanishing of H1(f*TX(-0-infinity)) makes the second-point evaluation
   smooth at the chosen map while its value at 0 remains x. This is
   deformation-theoretic smoothness, valid in positive characteristic;
   characteristic-zero generic smoothness is not used. The pointed Hom
   scheme is also smooth there. Its smooth local quotient by Aut(P1,0)
   lies in the unique local stable-map component selected for H.
   Thus the evaluation image contains an open set; properness makes that
   image closed, and irreducibility of X makes it all of X.

8. **Descent and arbitrary curves.** For every Cartier D, the degree b of
   e*D on the P1 fibers is constant. With d=A.C, the pullback of
   L=O(dD) tensor A^(-b) is fiberwise trivial. Proper flat base change,
   h0=1 and h1=0 give e*L=pi*B. The contracted section makes B trivial.
   For every curve Gamma in X, including those avoiding x, a closed point
   in the nonempty generic fiber of e over Gamma has a finite residue-field
   extension. Its closure in the projective total space is a curve
   dominating Gamma. The projection formula gives q deg(L|Gamma)=0
   for a positive integer q. This is an integer equality; divisibility
   of q by the characteristic does not invalidate it.

9. **Ampleness and final imported result.** Every Cartier divisor is
   numerically proportional to A. Taking D=-KX gives a positive ratio,
   since its degree on a rational normalization is a sum of positive
   splitting degrees. Numerical equivalence respects the multilinear
   intersections used in Nakai--Moishezon; hence -KX is ample. FM21
   Proposition4.8(1) (p.16) then applies at the same point in arbitrary
   characteristic. This uses the established Fano clause, not the
   general-point clause or the conjecture being proved.

## Boundary cases and counterexample controls

For n=1, deg(TX)=2-2g makes the assertion immediate. Dimension zero,
if included by convention, is already P0. A normalization of a rational
image has generically nonzero differential because it is birational;
the same is not asserted for an inseparable multiple cover. Such covers
are eliminated in the minimal-degree fiber. Products with two
positive-dimensional factors have zero tangent quotient degree on
rulings, so they do not meet the hypothesis. A positive determinant
with a negative tangent splitting summand does not meet it either.
The use of one mark and the absolute minimum across all families is
essential. Surjectivity on arbitrary curves, not just family members,
is checked in Step8.

## Reproduction and its limits

The frozen 49-file publication packet reproduced with its externally
pinned top-level manifest in normal and optimized Python. Relocated
and zero-fuzz reconstructed versions produced the required outputs;
strict integrity mutations and the historical nested-manifest
regression were reproduced. These certify the stated finite and
integrity computations only. No computational formalization of the
geometric proof is claimed. The full Kollár monograph proofs are
imported through the explicitly checked published FM propositions,
not independently reproved in this audit.

## Provisional root verdict

No mathematical gap or counterexample is identified in the full
argument. Root mathematical assessment: PASS, subject to integration
of the two fresh independent reports. Publication readiness is not
yet established: priority audit, preprint construction, fresh whole
package reviews, and publication records remain unfinished.

Primary inspected sources:

- https://publications.mfo.de/bitstream/handle/mfo/3816/OWR_2019_53.pdf?isAllowed=y&sequence=1
- https://par.nsf.gov/servlets/purl/10198624
- https://arxiv.org/pdf/1903.00610 (preprint numbering is different)
- https://arxiv.org/pdf/math/9808074
- https://stacks.math.columbia.edu/tag/03XX
- https://stacks.math.columbia.edu/tag/0B91
