# Independent full review: Ohtsuki Problem 7.24 / 10400139

## Verdict

**PASS_FULL_CREDITED_SOURCE_CONVENTION_BRIDGE.** The unchanged mathematical proof establishes the stated relationship for the literal 2001 definition:

\[
K_N^{\mathrm{old}}(S^3,L)=N^{-2N}J_N(L)^N
\]

for every nonempty link and every odd integer \(N>1\), with the specified original ambient-orientation convention and the normalized enhanced Jones evaluation at \(\exp(2\pi i/N)\). The recommended campaign disposition is **already_solved, 1/5**, as a credited consequence of the published Kashaev, Murakami–Murakami and Baseilhac–Benedetti results, with an explicit convention dictionary. This review does not certify novelty or settle an adjacent phase-refinement or volume-conjecture problem.

No mathematical revision is required. A source-locator discrepancy was corrected during review: the cached Ohtsuki **print** PDF corresponds to `024p.pdf`, not `024s.pdf`. The author retained the old snapshot and issued a metadata-only refreeze. This verdict binds:

- `PROOF.md`: `9122fb651354fb8eb6700d42b30cfc4368296aa709d0dc645bc52774ad6bc4b1`
- corrected `FROZEN_MANIFEST.json`: `36a3818d212ffb581c8676e59e73c45e75dd8a87e8ac1b3215b5bc6cbdbe9c04`
- the 21 files listed by that manifest, including the preserved source-locator history

The earlier mathematical hash is unchanged. The reviewer independently downloaded the corrected print URL and obtained the same 3,957,038 bytes and SHA256 as the cached primary PDF.

## Independence and method

The reviewer did not contribute to the author proof or its checks. This was a full mathematical and source/convention audit, rather than a numerical approval. It included reading the complete proof, original target and defining state sums; reconstructing the scalar basis change and its face cancellation; checking both tensor signs and the mirror dictionary; inspecting the relevant printed formulas visually; verifying every author/source hash; replaying all three author checkers; and writing a separate checker without importing author code.

The separate checker has **36,444 exact controls** and **3,594 non-interval 85-digit complex diagnostics**. Its complex part reconstructs 6j coefficients directly by solving the Clebsch–Gordan intertwiner equations, rather than evaluating the finite-rho formulas used by the author's gauge checker. Finite controls support the audit but do not prove the all-link or arbitrary-N assertions.

## 1. Original target and admissible data

The full Ohtsuki Section 7.4, printed pp.485–487, explicitly introduces a nonempty link in a compact closed oriented three-manifold, a flat Borel bundle and odd \(N>1\). It defines \(K_N=H_N^N\) and points to reference [43], the 2001 paper. On \(S^3\) the bundle is trivial. Problem 7.24 asks for the actual Jones relationship; the following proposed equality is a guess, not part of the definition.

The proof properly binds the word “old” to the literal equation (2) of the 2001 paper. That equation has \(N^{-V}\), the negative off-link edge exponent, and an outer Nth power. The long 2002 paper, equation (7) and Theorem 5.2, confirms these conventions. This is an appropriate exact interpretation of the source, provided the old-normalization qualification remains visible in any result summary.

A globally ordered, quasi-regular distinguished triangulation with a Hamiltonian link subcomplex is an admissible specialization. An injective complex vertex cochain gives a full unipotent coboundary: every relevant edge value is nonzero and all edge parameters for each ordered triangular face agree between its two incident tetrahedra. Published existence and invariance permit this choice. The proof does not require every presentation or arbitrary cocycle to have this form. Generic choices avoid the finitely many local singular parameters; identities then extend where the source construction is defined. No division by a link invariant occurs.

Integral charges reduce by division by two modulo N. This is legitimate for every odd N, including composite N. Their local and global conditions become the half-charge conditions in Kashaev's formulation. The choice of a total ordering avoids a nontrivial face-identification gauge issue: the same ordered face carries the same pair of cyclic parameters from either adjacent tetrahedron.

## 2. Clebsch–Gordan gauge and both tensor signs

The old Proposition 8.2 and Kashaev (1994), equation (1.13), have identical state-dependent CG entries when the unipotent parameters \(t_p=1\) are used. The difference is a nonzero scalar for each regular pair. Their defining intertwiner equations have the same order of factors. Substitution gives

\[
R_o=\frac{f(p,q)f(pq,r)}{f(q,r)f(p,qr)}R_K.
\]

Thus the direction of the author's \(Df\) is correct. The inverse matrix receives the reciprocal, not the same factor. The old h-normalization in Proposition 8.3 agrees with the CG definition, up to branch roots allowed by the construction. The independent numerical reconstruction also checks this directly in all coefficient states for N=3,5 and two nonsingular parameter triples, followed by independent physical-output intertwiner checks.

Kashaev's positive zero-charge prefactor is \(x_{qr}^{N-1}\), and its negative prefactor is \(x_{pq}^{N-1}\). The old prefactor is \((x_{pq}x_{qr})^{(N-1)/2}\) for both signs. Consequently the positive ratio is \(Df(x_{pq}/x_{qr})^{(N-1)/2}\), and the negative ratio is its inverse. The extra ratio is itself a face coboundary by putting \(g(p,q)=f(p,q)x_{pq}^{(N-1)/2}\).

I checked the charge shifts against the actual equations (4.6)–(4.7) of Kashaev (1995) and Proposition 8.5 of the old paper. The Kronecker condition remains \(\gamma+\delta=\beta\). The two scalar charge conventions differ by \(\zeta^{-ac}\) in the positive case and \(\zeta^{ac}\) in the negative case. These are independent of every face state. In particular, no uncancelled state-dependent diagonal factor or half-root sign was suppressed.

For an ordered tetrahedron, the face factors in Dg occur with the alternating boundary exponents, up to a uniform reversal of all four signs. In an oriented closed triangulation, every face has opposite induced boundary signs on its two incident tetrahedra. Therefore the complete product is exactly one, before summing states. Arbitrary square-root signs in Kashaev's CG bases are just additional face factors and cancel in the same way. This addresses the potentially serious issue that an arbitrary sign would survive an odd Nth power.

The remaining local branch/charge ambiguities are Nth roots, and their product is an Nth root independent of the state. Taking the Nth power consequently removes precisely the allowed ambiguity. It would be invalid to make the same inference from an equality only modulo \(\mu_{2N}\); the proof does not do so.

## 3. Orientation, modern notation and mirror

The 2001 paper defines a positively oriented ordered simplex to have index −1 and assigns it R; its negatively oriented simplex receives the inverse tensor. The long 2002 paper changes the index name to +1 for a positive simplex but keeps this tensor assignment. Reading just the index labels would produce a false mirror.

Kashaev's “right” tetrahedron is defined by viewing the ordered face 012 from vertex 3. In standard positively oriented coordinates, face 012 appears counterclockwise from vertex 3, so the positive tensor and the face-state assignment \((\gamma,\delta,\alpha,\beta)=(\alpha_2,\alpha_0,\alpha_3,\alpha_1)\) agree with the old convention. The edge-coboundary sign is matched by negating the vertex cochain. As N is odd, the associated edge-root sign gives \((-1)^{1-N}=1\) in the off-link factors.

The later 2011 convention must be handled independently. Its Remark 3 explicitly reverses the simplicial sign relative to the earlier BB papers; Figures 1–4 and the incoming/outgoing index rule are consistent with the author's dictionary. Its Remark 10 separately states that the positive and negative Kashaev braid matrices were exchanged relative to Murakami–Murakami. The resulting modern comparison is with the mirror. Reversing the ambient orientation to translate back to the old ordered-simplex tensor assignment cancels that mirror. The old equality is therefore with \(J_N(L)^N\), with no unmentioned reflection of L.

The supplementary old-to-modern local conversion is also correct. Raising the h identity to N pairs the factors \((1-\zeta^j/u)/(1-\zeta^j)\); the total exponent \(\sum_{j=1}^{N-1}j=N(N-1)/2\) cancels the power of u exactly, with no residual sign. The cyclic omega identity and the negative bracket-ratio telescope give the stated charged shifts for both tensor signs. These checks are compatible with the canonical-flattening roots in the modern equation (1) and the matrix formula in Section 6.2.

## 4. Normalization and the exact published theorem

The only surviving global normalization ratio is

\[
N^{-V}/N^{2-V}=N^{-2}.
\]

Kashaev (1994), equation (4.4), has the latter normalization. Kashaev (1995), immediately after equation (4.19), explicitly distinguishes its boundary partition function from the closed invariant by the additional factor \(N^2\). The 2011 equation (30), together with its normalization remark, confirms this again. Raising to N gives the factor \(N^{-2N}\), independently of V or the link.

Kashaev (1995), Theorem 1(2), supplies the odd-N three-dimensional/planar comparison. Murakami–Murakami, Theorem 4.9, identifies the enhanced planar invariant with the normalized N-color Jones specialization for every link and every N≥2. The author's restriction to odd N comes from the old QHI construction, not an unjustified restriction of that theorem.

The later full 2011 treatment is essential context. It explicitly identifies gaps in the exposition of earlier invariance/comparison claims and supplies the detailed all-link treatment. Corollary 4.2 is root-only for the Kashaev-type sum; Corollary 4.6 explicitly says that its equalities are modulo powers of \(\zeta_N\). The proof does not mistake the paper's more general notation, which can also permit a sign, for this stronger statement. Nor does it identify the Borel/Kashaev symmetrization with the different general quantum-hyperbolic symmetrization on arbitrary three-manifolds.

The 2004 Theorem 5.1 cannot be used by name alone to erase the normalization difference. The packet correctly treats the explicit original equation as controlling and supplies the dictionary instead. Likewise, the short 2002 survey really prints the opposite edge exponent. With these local tensors that exponent fails the scaling cancellation: for a closed distinguished triangulation \(E-|H|=T\), so the tetrahedral and edge scaling powers would add instead of cancel. The packet clearly discloses this printed inconsistency rather than silently relying on it.

## 5. Boundary cases and computational evidence

The unknot has old value \(N^{-2N}\), whereas the normalized Jones value is one. This follows analytically from the normalization comparison. The direct N=3 computation is an additional strong control: the Hamiltonian five-cycle in the boundary of a four-simplex bounds the displayed embedded fan; its integer charges satisfy the required edge totals; the old tensor contraction over all 59,049 states gives H=1/9 and K=1/729 to the stated precision.

Split-link zeros do not cause a gap because no step divides by the state sum or Jones invariant. All components carry the same N-color and the enhanced ambient-isotopy normalization. Component orientations can be chosen as in the standard link theorem; the old unoriented invariant agrees with the resulting Nth power. The packet makes no unsupported claim about orientation independence of an arbitrarily normalized unpowered multicomponent quantity.

Even N, the empty link, arbitrary three-manifold Jones comparisons, and neighboring phase/asymptotic questions are outside this verdict.

All three author outputs replay byte-for-byte: 412,133 exact controls, 33,600 separately labelled complex diagnostics across two scripts, and the direct 59,049-state unknot contraction. The independent controls verify cellular cancellation on nine successively subdivided oriented 3-spheres, including arbitrary signed face gauges; finite-field powered-h, omega and negative-scalar identities for odd N=3 through31; and the direct CG reconstruction described above. Their exact and floating-point roles remain distinct.

## Publication conditions

Retain the literal-old normalization, original orientation, odd-N/nonempty-link scope, root-only phase argument, and full literature credit. Include the locator correction/history and this review unchanged. A claimed new invariant or a universal equality with no convention qualifier would go beyond this verdict. Publication remains the parent's decision.
