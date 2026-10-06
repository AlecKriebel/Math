# Second independent review: fixed Wu-manifold free-action witness

Problem 30001522 / OWR-4413-005 / catalog rank 828. Reviewed 6 October 2026.

## Verdict and scope

**ACCEPT the complete theorem as written. No mathematical correction is required.**

For the single fixed space W = SU(3)/SO(3), with the real orthogonal inclusion, the actual continuous free-action ranks are

- free toral rank 0;
- free 2-rank 0;
- free p-rank 1 for every odd prime p.

The same construction gives a smooth free cyclic action of every odd order. The author proof and first independent audit have not been modified. This report is a separate second mathematical/source review, not formal proof-assistant verification, peer review, an exhaustive literature search, or certification of novelty or present-day open status.

The two exact reviewed archives and key documents are bound in INPUT_BINDINGS.json. Every archive member was checked against the corresponding manifest and the supplied archive hashes before this acceptance. The author proof, first AUDIT.md, and INDEPENDENT_LEMMAS.md were all read in full. This review did not repeat the first audit's full-corpus arithmetic or claim a new full-corpus inspection.

## 1. The target is the actual space

The official report's printed page 1912 was reopened online and independently rendered and visually read. Its ranks use free actions on the given X. The hypothesis on total rational homotopy is retained. No optimization over rationally equivalent replacements is present. This fixes the precise scope of the answer. [1]

The quotient is a closed smooth five-manifold, so one finite triangulation identifies its underlying space with a fixed finite complex. Continuous actions need not preserve that triangulation. The fibration SO(3) -> SU(3) -> W yields pi_1(W) = 0 and pi_2(W) = Z/2. Hurewicz gives H_2(W;Z) = Z/2. Orientation, integral Poincare duality, and the universal coefficient theorem then give integral homology Z in degrees 0 and 5, Z/2 in degree 2, and zero in all other degrees.

Simple connectivity directly satisfies both fundamental-group conditions. Rational homotopy finiteness also follows from the Lie-group fibration, regardless of the map in degree three. For the sharper assertion, rational Hurewicz first produces a nonzero degree-five sphere map; since the other rational homology groups are zero, this map is a rational homology equivalence. Rational Whitehead applies to these simply connected finite-type spaces. Thus W is rationally S^5. None of this changes the underlying space on which the ranks are measured.

## 2. Odd-order actions, including the prime three

The circle homomorphism D(z) = diag(z,z,z^(-2)) lies in SU(3). A point g SO(3) is fixed only when D(z) is conjugate into SO(3). Any element of the latter has eigenvalue 1, so the displayed spectrum forces z = 1 or z = -1. An odd-order cyclic subgroup contains no -1, proving freeness for every one of its nonidentity elements and for every odd order at once.

There is no central-kernel exception when 3 divides the order: the scalar matrices associated to primitive cube roots have no eigenvalue 1. They are therefore not conjugate into SO(3) and do not fix a point. The map from the circle is injective because its first diagonal entry is z. At -1, D(-1) is itself in SO(3), so the identity coset really is fixed. The argument proves a circle action with finite stabilizers and actual free actions of its odd-order subgroups; it never mistakes the full circle action for a free action.

The fixed space and fixed embedding precede the choice of prime. The assertion therefore has the correct quantifier order. Yeroshkin's circle-isotropy calculation is compatible context, but the elementary eigenvalue proof establishes the needed fact without depending on that calculation. [3]

## 3. The continuous-category obstruction is valid

Suppose an arbitrary continuous involution h acted freely. Such an action is by homeomorphisms. Around any x choose a coordinate neighborhood U small enough that U and h(U) are disjoint. Its image under the quotient map is open and is homeomorphic to U. The quotient N is consequently a closed Hausdorff topological five-manifold and q:W -> N is a two-sheeted covering. No smoothness or local linearity of h has been assumed.

The tangent microbundle of a topological manifold is defined near the diagonal. In covering neighborhoods, the map (x,y) -> (x,q(y)) identifies the tangent microbundle of W with the pullback of that of N. The mod-two Thom-class definition of Stiefel-Whitney classes is natural under this isomorphism and agrees with the smooth tangent-bundle definition on W. Hence w_i(W) = q^*w_i(N).

Using mod-two fundamental classes, q_*[W] = 2[N] = 0. Therefore every top-degree product of the pulled-back tangent classes evaluates to zero. This argument also works when N is nonorientable; it neither needs an integral orientation nor a triangulation of N.

The actual tangent number on W is <w_2(W)w_3(W),[W]> = 1. This is stated by the published tangent-class and cohomology calculation, independently reopened in publisher HTML and visually checked in the stored PDF. The separate class of the principal SO(3)-bundle is not being substituted for the tangent bundle. [2] The contradiction excludes every free continuous involution. Every positive-rank torus contains a subgroup of order two, and restriction of a free action remains free. Thus both claimed zero ranks follow.

This argument does not need the orbit space of a free topological circle action to be a manifold. It only forms the finite-group quotient, for which the local covering proof is enough.

## 4. Independent reconstruction of the characteristic number

The tangent isotropy representation is SO(3) acting by conjugation on real symmetric traceless three-by-three matrices. Rotate the first two coordinates. The two mixed terms with the third coordinate form a weight-one plane; the traceless quadratic terms in the first two coordinates form a weight-two plane; diag(1,1,-2) spans a fixed line. A full rotation thus represents 1 + 2 = 1 modulo two in pi_1(SO(5)).

The fibration boundary pi_2(W) -> pi_1(SO(3)) is an isomorphism. Pulling the tangent bundle back along a sphere representing its generator therefore has the nontrivial SO(5) clutching class and nonzero w_2. The unique nonzero element x of H^2(W;F_2) is accordingly w_2(W).

For the coefficient sequence 0 -> Z/2 -> Z/4 -> Z/2 -> 0, universal coefficients identify the degree-two reduction map with Hom(Z/2,Z/4) -> Hom(Z/2,Z/2). The two homomorphisms to Z/4 send the generator to 0 or 2, both of which reduce to 0. The connecting homomorphism, namely Sq^1, must therefore send x to the nonzero y in H^3(W;F_2). Since w_1(W) = 0 and Sq^1(w_2) = w_1w_2 + w_3, one gets w_3(W) = y. Mod-two Poincare duality forces xy to evaluate to one.

This gives an independent route to the exact tangent number, rather than treating its published value as a black box. DIAGNOSTICS.py checks the five integer matrix commutator identities underlying the two weights, the parity, and the small coefficient-reduction model. These finite checks do not certify the topology.

## 5. The optional exact odd-primary upper bound passes

At any odd prime p, W is an F_p-homology five-sphere. The induced action of an elementary abelian p-group on each of H^0 and H^5 is trivial, since a p-group cannot map nontrivially into F_p^*. Thus for E = (Z/p)^2 the Borel spectral sequence starts as

R tensor H^*(W;F_p), where R = F_p[t_1,t_2] tensor Lambda(s_1,s_2), with the t_i of degree 2 and s_i of degree 1.

There are precisely the fiber rows 0 and 5. The only possible connecting differential is d_6. R-linearity up to the standard grading sign makes its bottom-row image the principal ideal of f = d_6(u). After this differential there is no later differential capable of changing the bottom row, so R/(f) is E_infinity in that row.

Killing the exterior generators gives a surjection onto F_p[t_1,t_2]/(f_bar). If f_bar is zero this is already infinite-dimensional. Otherwise it is homogeneous of polynomial degree three. Multiplication by it injects polynomial degree m-3 into degree m, leaving dimension (m+1)-(m-2) = 3 for every m >= 3. Neither a nonzero polynomial part nor irreducibility has been silently assumed.

A finite free action makes the Borel construction homotopy equivalent to W/E, because the map to the quotient is a numerable associated bundle with contractible fiber EE. The quotient is a closed topological five-manifold. Its cohomology vanishes above dimension five, independently of any triangulability issue. Nonzero associated-graded pieces in arbitrarily high total degrees contradict this; hidden extensions cannot erase them. This proves the exact upper bound one at every odd prime.

## 6. Attribution and outcome

Kuhn-Lloyd Example 2.25 was independently reopened in the journal-hosted manuscript. It already gives the Wu-manifold no-free-involution observation by nonbounding. Its surrounding fixed-point theorem includes an admissibility hypothesis. The reviewed proof does not import that hypothesis or silently claim the theorem covers all continuous actions; it supplies its own covering argument instead. This classical credit should accompany any presentation. [4]

This review neither locates nor rules out a prior explicit combination giving an answer to Hanke's question. Mathematical validity is accepted; novelty and current-open-status claims are not. The first audit's recommended Kuhn-Lloyd addition remains appropriate, without requiring a change to either frozen packet.

## 7. Reproducibility and limitations

INPUT_BINDINGS.json records independent byte/manifest checks of both freezes. SOURCE_REVIEW.json records the particular public sources inspected and stored-PDF hashes where available. No full-corpus reinspection is claimed. Fresh finite diagnostics check the isotropy representation, coefficient reduction, circle spectra through order 257, and selected binary-cubic multiplication maps over F_3, F_5, and F_7. The universal assertions are established by the mathematical arguments, not by those samples.

VERIFY.py validates this packet's exact inventory and manifest, then executes only the just-verified diagnostic source and compares its result to the recorded JSON. Normal and optimized runs and separate damage controls are recorded in VERIFICATION_RESULTS.json. A trusted external archive hash is still necessary: a manifest cannot authenticate its own replacement. Source documents, extracted text, corpus contents, and coordination material are absent from this safe packet.

## References

[1] B. Hanke, *Homotopy Euler characteristic and the stable free rank of symmetry*, in Oberwolfach Report 32/2010, printed pp. 1912-1915. https://ems.press/content/serial-article-files/46287 ; https://doi.org/10.4171/OWR/2010/32 .

[2] A. Debray and M. Yu, *What Bordism-Theoretic Anomaly Cancellation Can Do for U*, Communications in Mathematical Physics 405, article 154 (2024), Lemma 4.41, Corollary 4.44, Proposition 4.45. https://link.springer.com/article/10.1007/s00220-024-04937-4 .

[3] D. Yeroshkin, *Orbifold biquotients of SU(3)*, Differential Geometry and its Applications 42 (2015), 54-76, Proposition 4.2. https://arxiv.org/abs/1401.7565 ; https://doi.org/10.1016/j.difgeo.2015.07.003 .

[4] N. J. Kuhn and C. J. R. Lloyd, *Chromatic fixed point theory and the Balmer spectrum for extraspecial 2-groups*, Example 2.25, manuscript p. 12. https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-kuhn-lloyd-FINAL.pdf ; https://arxiv.org/abs/2008.00330 .
