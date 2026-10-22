# Independent adversarial audit: problem 30001522

Date: 6 October 2026. Target: OWR-4413-005, catalog rank 828.

## Verdict

**ACCEPT the full mathematical theorem in the literal fixed-space, actual-free-action scope.** No mathematical correction to the frozen proof is required. For the one fixed Wu manifold W = SU(3)/SO(3), the accepted values are rk_T(W) = rk_2(W) = 0 and rk_p(W) = 1 for every odd prime p. The same displayed action supplies free cyclic actions of every odd order.

This is independent mathematical acceptance, supported by source inspection and finite consistency tests. It is not a formal proof-assistant certificate, a novelty certificate, an exhaustive literature review, or a claim of publication or peer review. The classical manifold, characteristic-class computation, and nonexistence of a free involution must retain attribution. The author freeze remains unchanged, including its historical pending-audit labels; this separate document supplies the subsequent verdict.

## 1. Frozen object and target binding

The reviewed archive is FREE_P_TORAL_30001522_AUTHOR_SAFE_FREEZE.zip, 17,871 bytes, SHA-256 66040253e0072ac532237b7cf70c513b69ae6cabdf4e99e554e96c5f703de7fa. Its 1,543-byte manifest has SHA-256 4d2d1a9b1aa2693d50697b94e2cb47a6bb1d938ad9ac66f6e1eace4042085e81. All 11 flat regular members and every manifest payload hash were independently checked before execution. The proof digest is 392058c15a974959455307875ce12e7453b8ae15d1db5cdf3e6bfb22adf7debc.

All three full supplied corpora were independently read and hashed. The target has exactly one catalog record and one problem record; there is no research-result entry under OWR-4413-005. Serializing the complete problem record together with the empty research object using the specified default sorted Python JSON gives ca5ea39f6f40b6344a17adf507993b7a3aa628f194669943f2b6acb99876e306. The full statement gives c368a8d0a2095496760c49e9393ba1825274ccad544d6cf16acbca830d7ef0a0. Both match the catalog, author provenance, and requested target. No corpus contents are reproduced here.

The official EMS report was independently inspected online and printed page 1912 was independently rendered from the hash-verified PDF and visually read. Its definitions concern free actions on X itself. The subsequent question retains the abelian fundamental group, trivial action on higher homotopy, and finite-dimensional total rational homotopy assumptions. Neither an almost-free action nor a replacement by another space in the same rational homotopy type is the stated invariant. Thus the frozen proof addresses the exact literal question, not a nearby rational-toral-rank problem. [1]

## 2. The finite fixed space and rational homotopy

The real SO(3) subgroup is closed in SU(3), so the quotient is a compact connected smooth manifold of dimension five. Smooth compact manifolds have finite triangulations; using one triangulation of this manifold fixes a single finite complex. The actions constructed later are actions on its underlying space, and need not preserve an arbitrary chosen triangulation.

The homotopy exact sequence of SO(3) -> SU(3) -> W gives pi_1(W) = 0 and pi_2(W) = Z/2. There is consequently no nontrivial fundamental-group action to check. Hurewicz identifies H_2(W;Z) with Z/2. Integral Poincare duality and the universal coefficient theorem give the remaining homology groups stated in the proof. In particular H_3 = H^2 = 0 because H_1 = 0 and Hom(Z/2,Z) = 0; H_4 = H^1 = 0. Orientation follows from simple connectivity.

For the required finiteness assumption, the rational homotopy exact sequence of the compact Lie-group fibration already suffices. Alternatively, the simply connected rational homology five-sphere has its first nonzero rational homotopy in degree five by rational Hurewicz. A sphere map representing a nonzero rational Hurewicz class is a rational homology equivalence. Rational Whitehead then identifies W with S^5 after rationalization. This does not replace W in the definition of the ranks; it verifies a hypothesis about the already fixed space. There is no unsupported inference from rational cohomology to an integral sphere.

## 3. Every odd order, with the bad prime exposed

For z in S^1, D(z) = diag(z,z,z^(-2)) has determinant one, and left multiplication gives a well-defined smooth action on right cosets g SO(3). A fixed coset forces g^(-1)D(z)g into SO(3). A real orthogonal three-by-three matrix with determinant one has eigenvalue one. The eigenvalues of D(z) then force z = 1 or z^2 = 1. This is an exact statement about all circle elements, not a finite-prime experiment.

Hence every stabilizer lies in {1,-1}; each odd-order subgroup intersects every stabilizer trivially. The group C_n is embedded faithfully in this same circle for each odd n. The case n divisible by three causes no exception: a nontrivial scalar cube root has no eigenvalue one and cannot lie in any conjugate SO(3). The element -1 really fixes the identity coset, since diag(-1,-1,1) lies in SO(3). Thus the circle construction is almost free, and its restriction to C_2 fails as it must.

The argument does not need a converse to the eigenvalue criterion. A converse is nevertheless valid for SU(3): once the spectrum contains one, the other two unit eigenvalues are reciprocal, so the spectrum is that of an SO(3) rotation. Any unitary conjugator can have its determinant corrected by a scalar without changing the conjugacy. The independent code tests this through conjugation-symmetric spectra rather than copying the author's fixed-power algorithm. Yeroshkin's published orbifold context is compatible with this specialization. [3]

## 4. The involution obstruction in the continuous category

This is the principal category-sensitive step, and it passes.

Any continuous action of a finite group is by homeomorphisms. If an involution acts freely on a Hausdorff manifold, choose a coordinate neighborhood disjoint from its translate. The quotient map restricts there to a homeomorphism onto an open set. These neighborhoods make the quotient an ordinary topological five-manifold and the projection a two-sheeted covering. Compactness and the Hausdorff property are preserved. Smoothness, local linearity, and a triangulation of the quotient are unnecessary.

The tangent microbundle of a manifold is defined by the diagonal. For a local homeomorphism q, the map (x,y) -> (x,q(y)) identifies the tangent microbundle near its zero section with the pullback of the quotient tangent microbundle. Mod-two Thom classes and Steenrod squares yield natural Stiefel-Whitney classes of these topological microbundles, agreeing with the smooth tangent classes on W. Therefore w_i(W) = q^*w_i(W/C_2).

On mod-two fundamental classes, q_*[W] = 2[W/C_2] = 0. Every top-degree product pulled back from quotient characteristic classes evaluates to zero. This statement does not require the involution or quotient to preserve an integral orientation. Debray-Yu, Corollary 4.44 and Proposition 4.45, gives the ring with degree-two and degree-three generators x,y, nonzero top product xy, and tangent classes w_2 = x, w_3 = y. Thus the actual tangent characteristic number is one, contradicting the covering conclusion. It is not a number of a different auxiliary bundle accidentally substituted for the tangent bundle. [2]

INDEPENDENT_LEMMAS.md also derives the necessary tangent w_2 from the SO(3) isotropy representation and obtains w_3 by the Bockstein. That cross-check agrees with the published computation. Restricting a free positive-dimensional torus action to an involution would give a forbidden free involution. This excludes every continuous free torus action, with no assumption about a circle quotient being a manifold.

## 5. Exact odd-primary rank

The optional sharpening is correct and is accepted as part of the theorem. Integral homology implies that W has only H^0 and H^5 over F_p for odd p. Every p-group acts trivially on these one-dimensional groups: a homomorphism from a p-group into F_p^* must be trivial. No orientation-preservation assumption is silently inserted.

For a hypothetical free E = (Z/p)^2 action, the Borel spectral sequence has only rows zero and five and trivial coefficients. No differential other than d_6 can connect these rows. The bottom-row image is the principal ideal generated by the degree-six transgression f. Therefore R/(f) survives in row zero, for R = F_p[t_1,t_2] tensor Lambda(s_1,s_2). Setting the exterior generators to zero gives a surjection onto F_p[t_1,t_2]/(f_bar).

If f_bar = 0 this quotient is infinite-dimensional. Otherwise it is a binary cubic quotient, whose polynomial degree-m dimension is three for every m >= 3. No irreducibility, regular-sequence assumption, or nonzero polynomial-part hypothesis is required. Hidden multiplicative extensions cannot remove nonzero associated-graded cohomology groups in unbounded degrees.

Because the action is free and finite, W/E is a closed topological five-manifold and the Borel construction is homotopy equivalent to it: the map to the quotient is an associated bundle with contractible fiber EE. The quotient is paracompact and locally contractible; its singular cohomology vanishes above five. The contradiction excludes rank two and, by restriction, higher ranks. No finite CW decomposition of a potentially nontriangulable quotient is assumed. This proves rk_p(W) = 1 for all odd primes, not merely sufficiently large primes.

## 6. Independent literature addition and attribution

The audit located an additional directly relevant primary source: Nicholas J. Kuhn and Christopher J. R. Lloyd, *Chromatic fixed point theory and the Balmer spectrum for extraspecial 2-groups*, Example 2.25, manuscript page 12. It explicitly discusses the Wu manifold and rules out a free involution by its nonbounding property. The surrounding fixed-point theorem has an admissibility hypothesis; the present audit does not borrow that theorem to cover arbitrary continuous actions. Instead it retains the explicit covering/characteristic-number argument above. The source is useful corroboration and attribution. [4]

This addition should accompany any presentation of the result. It does not require changing the frozen proof, which already disclaims novelty and credits classical ingredients. The audit did not establish whether the exact combination was previously published as an explicit answer to Hanke's OWR question. Its validity does not establish that the question was still open in 2026. No priority or first-solution claim is accepted.

## 7. Tests and boundaries

The author verifier was run from a fresh extraction in isolated normal and optimized Python. Its pinned-verifier suite passed the two baseline modes, both relocation runs, and all 28 advertised mutation rejections. Independent diagnostics tested 131,328 fixed-weight spectrum elements, 42,768 general-weight spectrum elements, 2,592 weight/order actions, 8,192 finite-ring identities, and 4,928 multiplication-rank computations covering all 704 nonzero binary cubics over F_3 and F_5 in degrees three through nine. Five explicit semantic controls passed.

The separate audit packet has a stricter fixed inventory and its own pinned-verifier damage tests, recorded in PACKAGE_TEST_RESULTS.json. Normal and optimized execution, relocation, missing/extra members, directories, symlinks including the manifest and root, a FIFO, duplicate JSON keys, unsafe names, malformed counts/digests, altered verifier bytes, and rehashed semantic/binding mutations are exercised. All fixtures are temporary and do not alter the freeze.

The tests explicitly demonstrate that consistently rehashing an exposition-only edit can pass an integrity verifier. Consequently a trusted external archive or manifest digest is essential, and none of these scripts authenticates a theorem merely from prose or validates changed proofs. Arithmetic tests condition on the algebra being the correct model; the source and mathematical arguments establish that model. Source documents and full corpora are not needed for public replay and are not redistributed.

## References

1. B. Hanke, *Homotopy Euler characteristic and the stable free rank of symmetry*, Oberwolfach Report 32/2010, printed pp. 1912-1915. https://doi.org/10.4171/OWR/2010/32 ; official PDF https://ems.press/content/serial-article-files/46287 .
2. A. Debray and M. Yu, *What Bordism-Theoretic Anomaly Cancellation Can Do for U*, Communications in Mathematical Physics 405, 154 (2024), Lemma 4.41, Corollary 4.44, Proposition 4.45. https://doi.org/10.1007/s00220-024-04937-4 .
3. D. Yeroshkin, *Orbifold biquotients of SU(3)*, Differential Geometry and its Applications 42 (2015), 54-76, Proposition 4.2. https://doi.org/10.1016/j.difgeo.2015.07.003 ; https://arxiv.org/abs/1401.7565 .
4. N. J. Kuhn and C. J. R. Lloyd, *Chromatic fixed point theory and the Balmer spectrum for extraspecial 2-groups*, Example 2.25. https://arxiv.org/abs/2008.00330 ; journal-hosted final manuscript https://preprint.press.jhu.edu/ajm/sites/default/files/AJM-kuhn-lloyd-FINAL.pdf .
