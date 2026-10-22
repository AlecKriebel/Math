# Focused acceptance: asymmetric-knot core for K3 Problem 1.19

Audit date: 11 October 2026 (UTC).

## Verdict and exact scope

**ACCEPT the core existential argument, as a complete argument using the expressly cited classical theorems.** No mathematical correction is required for the claim that every closed, connected, oriented smooth 3-manifold contains one knot moved, up to ambient isotopy, by every nonidentity orientation-preserving mapping class. Consequently, the stated nontrivial separating-sphere twist is detected by a knot in this category.

The object assessed is the existential core and dependencies 1–5 now preserved in PROOF.md. No mathematical correction is required for that core. The optional stronger route is outside this acceptance. The original authored proof and focused report remain unchanged; ACCEPTANCE.json pins their identities and the distributed documents.

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification. No novelty, priority, or new-solution claim is made. The broader literal K3 scope is not certified.

The complete core argument and its exact classical dependencies are retained. This is not a computational reproduction package: copied source documents, source images, executable code, dataset contents, and raw certificates are not distributed. Classical theorem statements and applicability were audited; their historical proofs were not independently re-proved. Edition preparation performed editorial and byte-integrity checks only, with no new mathematical execution, scholarly-source retrieval, or visual source inspection.

## 1. Asymmetric knot existence

Kawauchi's original 1992 journal paper supplies the needed statement directly. On printed p. 299, a good pair has compact connected oriented ambient manifold and a smooth proper one-dimensional submanifold; its extra condition concerns spherical components of the ambient boundary. Thus a knot in a closed ambient manifold satisfies that condition vacuously.

The Main Theorem on pp. 300–301 produces almost identical imitations in the same ambient manifold. Section 2, especially p. 310, states that the imitation map is a diffeomorphism between neighborhoods of the one-dimensional submanifolds and explains the identification of the ambient manifolds. A one-component closed input therefore gives one knot in the same ambient manifold. This is stronger than mere existence of a hyperbolic link.

For an exterior bounded only by tori, p. 299 defines its hyperbolic structure on its interior and its isometry group to be the hyperbolic isometry group of that interior. This is the full group. Main Theorem (1) supplies a finite upper volume bound, and (2) explicitly makes the group trivial. No inference from orientation-preserving asymmetry alone is used.

Source: A. Kawauchi, *Almost identical imitations of (3,1)-dimensional manifold pairs and the branched coverings*, Osaka J. Math. 29 (1992), 299–327, https://doi.org/10.18910/4930 .

## 2. Rigidity and the compact exterior

Thurston's Chapter 5, Theorem 5.7.2 and Corollary 5.7.4, printed p. 101, concern complete finite-total-volume hyperbolic manifolds, including noncompact ones. The corollary identifies the full isometry group with the outer automorphism group. The remarks on p. 102 explicitly credit Prasad for the noncompact case. Applying this to the interior of the knot exterior therefore gives trivial outer automorphism group. Inclusion of that interior into the compact exterior is a homotopy equivalence by a collar, so the fundamental groups agree.

The compact exterior is connected and orientable, with a single torus boundary. Irreducibility and boundary incompressibility of a compact core of a complete finite-volume cusped hyperbolic 3-manifold are standard background facts explicitly declared in the candidate. They apply here; a theorem about a closed irreducible ambient manifold is not being applied to a reducible connected sum.

Source: W. Thurston, *The Geometry and Topology of Three-Manifolds*, Chapter 5, https://library.slmath.org/books/gt3m/PDF/5.pdf .

## 3. Pointed injectivity really gives the required unpointed isotopy

Hatcher–Wahl define their group on p. 7 using orientation-preserving diffeomorphisms fixing an interior point. Their Proposition 2.1 states injectivity into the automorphism group for irreducible manifolds with incompressible boundary. The definition does not impose boundary-pointwise fixing. Its proof on pp. 7–8 identifies Waldhausen as the applicable source for the Haken case with incompressible boundary. The candidate preserves these qualifications and applies it to the exterior, not the filled manifold.

Source: A. Hatcher and N. Wahl, *Stabilization for mapping class groups of 3-manifolds*, Duke Math. J. 155 (2010), 205–269, arXiv v4 pp. 7–8, https://arxiv.org/abs/0709.2173 .

Here is the independent check of the conversion. First move the image of the chosen interior point back to that point using an ambient isotopy supported in the interior. The endpoint fixes the point, and the induced automorphism is inner because its outer class is unchanged. An interior point-push around any chosen loop has endpoint fixing the point and induces conjugation by that loop, with sign depending on convention. Choosing the loop or its inverse cancels the inner automorphism. The resulting diffeomorphism is orientation-preserving, fixes the point, and induces the identity automorphism, so the proposition applies. Both point-moving modifications were unpointedly isotopic to the identity, giving the desired boundary-unrestricted isotopy of the original exterior map. No assertion that its boundary is stationary follows or is needed.

## 4. Continuous collar gluing and the residual solid-torus map

Write a boundary-unrestricted isotopy as `u_t`, with `u_0 = id` and `u_1 = g|X`, and put `a_t = u_t|T`. In the inward solid-torus collar, the candidate uses the boundary-level map

`(x,s) -> (a_{t+(1-t)s} a_1^{-1}(x), s)`.

The parameter lies in `[0,1]` and is continuous jointly in `t,s`. Each level map is a homeomorphism. Its inverse is `(x,s) -> (a_1 a_{t+(1-t)s}^{-1}(x),s)`, also jointly continuous. At the inner edge `s=1` it is the identity, so it extends by the identity across the rest of the solid torus. At the outer edge `s=0` it is `a_t a_1^{-1}`; at `t=1` it is the identity on the entire torus. These facts verify a genuine topological isotopy, not just endpoint identities sampled by a finite control.

Gluing `u_t` on `X` to `lambda_t g` on the solid torus is well-defined because their restrictions to `T` both equal `a_t`. Each resulting map preserves the two pieces and is a homeomorphism; continuity of the family and inverse family follows from the same gluing. Its terminal map is `g`. Its initial map fixes `X` pointwise and restricts to a boundary-fixed homeomorphism of the solid torus. That is exactly the remaining kernel. The construction may have a derivative mismatch at the seam; it is correctly presented as topological, and no smoothness at that seam is assumed.

## 5. Relative kernel and return to smooth isotopy

Hatcher's original Appendix, printed p. 605, statement (3), gives the smooth/PL comparison relative to the boundary for any 3-manifold. The following paragraph explicitly permits TOP in place of PL. Printed p. 606, statement (9), gives contractibility of the diffeomorphism group of the solid torus relative to its boundary. Both assertions were read visually from the original scan because extracted text is unreliable there.

These statements supply the exact two consequences used. The residual boundary-fixed solid-torus homeomorphism is isotopic to the identity relative to its boundary, so its isotopy extends by the identity on the exterior. The resulting topological isotopy between diffeomorphisms of the closed ambient 3-manifold implies that they lie in the same smooth isotopy class. Only path-component conclusions are needed. No stronger parametrized smoothing claim about the particular collar family is required.

Source: A. Hatcher, *A proof of the Smale conjecture, Diff(S3) approximately O(4)*, Ann. Math. 117 (1983), 553–607, https://pi.math.cornell.edu/~hatcher/Papers/SmaleConjecture.pdf .

## 6. Target, equivalence relation, and historical limits

If `f(K)` is ambiently isotopic to `K`, smooth isotopy extension gives an identity-isotopic correction making the map preserve the knot setwise. Tubular-neighborhood uniqueness and another identity-isotopic correction make it preserve a chosen solid torus. These operations require neither knot orientation nor a framing. The preceding steps then prove `[f]=1`. Contraposition gives setwise ambient-isotopy detection, which is sufficient for the target and is stronger than detecting oriented parametrized knots.

A sphere twist is orientation-preserving. Hence every instance satisfying the target's nontriviality hypothesis in the stated category follows, without restrictions on the prime summands. Equivalence by an arbitrary diffeomorphism is not the conclusion: the original map already gives that equivalence.

The preliminary K3 volume's p. 28 asks the separating-sphere question and does not itself explicitly impose closedness or orientability. Its p. 11 supplies the smooth-knot convention. This audit does not infer a missing global closed/oriented convention or certify boundary, noncompact, or nonorientable variants.

Aceto–Bregman–Davis–Park–Ray, arXiv:2007.05796v3, p. 6, records an announced Etnyre–Margalit argument extending to the non-prime case. That written announcement was inspected; the announced proof itself was not. Ferudun's public version 1.1, dated 5 October 2026, is explicitly unrefereed and reports that the Etnyre–Margalit paper is forthcoming. This is reported publication status, not an independently inspected proof or private author confirmation. Ferudun's own verification report is not evidence for this acceptance.

Sources: https://arxiv.org/abs/2007.05796v3 ; https://doi.org/10.5281/zenodo.23165876 ; https://doi.org/10.1090/surv/295 .

## Acceptance boundary

No optional finite-order extension argument, Chen–Tshishiku theorem, classification of separating twists, or claim that every hyperbolic knot detects the twist is certified by this focused report. No third-party source code or candidate checker was executed in that audit, and no author was contacted. The core argument is accepted at exactly the scope stated at the start of this report.
