# Stable pseudoisotopy and the endpoint obstruction

## Outcome and target

Problem 2950 is K3 Problem 4.74. It asks for a smooth closed four-dimensional manifold X and a self-diffeomorphism f smoothly pseudo-isotopic to its identity, but with no smoothly trivial stabilization. Here stabilization means choosing an isotopic representative fixing a four-ball, summing there with k copies of S² × S², and extending by the identity. Failure must hold for every permitted representative and every finite k. A relative-boundary example alone is insufficient. [K3, p. 251]

Let I = [0,1]. A smooth pseudo-isotopy from the identity to f is a diffeomorphism F of X × I with bottom restriction id and top restriction f; for manifolds with boundary it also fixes the side boundary. A level-preserving such map is an isotopy. The word concordance below refers only to this diffeomorphism notion, not knot concordance, smooth-structure concordance, or a general cobordism.

The argument below is for **closed connected oriented smooth four-manifolds**. K3's printed question does not explicitly impose orientation. Gabai's theorem does. No nonorientable extension or reduction of that remaining case is asserted. An oriented example would still answer the existence question affirmatively.

## External inputs and their exact scope

[G] Gabai, Theorem 2.5 of arXiv:2212.02004v2 (PDF p. 7): for a compact oriented smooth four-manifold, an endpoint homotopic to id is stably isotopic to id exactly when it admits a smooth pseudo-isotopy with first Hatcher–Wagoner obstruction Σ equal to zero. His Diff₀ means homotopic to id, not the identity component. Remark 2.12 and Corollary 2.13 (p. 10) cover free and free-abelian fundamental groups through vanishing of Wh₂. The theorem concerns the endpoint; it does not say every chosen pseudo-isotopy becomes trivial.

[S] Singh's arXiv:2111.15658v3 defines the endpoint obstruction in Wh₂(π₁X)/Σ(J(X)), with J(X) the pseudo-isotopies whose top map is id (Section 9, p. 42). Lemma 9.3 characterizes zero by the existence of a zero-Σ representative. Theorem E realizes each Wh₂ element after some S² × S² stabilization. Proposition 9.11 supplies the inclusion a + ā ∈ Σ(J(X)) for a ∈ Σ(P(X)), where P(X) is the pseudo-isotopy group. These are cited inputs, not new theorems of this packet. Section numbering here is pinned to the inspected 2022 preprint, not asserted for the 2025 published version.

## A group lemma identifying the missing information

Let P and E be groups, e: P → E a homomorphism, and s: P → A a homomorphism to an abelian group A. Set J = ker(e), R = s(P), and L = s(J). For an endpoint y in e(P), choose p with e(p) = y.

**Lemma.** The set s(e⁻¹(y)) is exactly s(p) + L. Consequently it contains zero if and only if s(p) lies in L.

**Proof.** For any q with e(q) = e(p), q p⁻¹ belongs to J, so s(q) − s(p) belongs to L. Conversely, if l = s(j) for j in J, then e(jp) = y and s(jp) = l + s(p). Both inclusions follow. Since L is a subgroup, zero belongs to s(p) + L precisely when s(p) belongs to L. □

Applied to pseudo-isotopies and top restriction, this is the algebra behind Singh's already known endpoint quotient. For an isotopic change of endpoint, concatenate with the trace of that isotopy; its first obstruction is zero. Thus the quotient class is unchanged. Pseudo-isotopy also implies homotopy of the endpoint to id, by projecting F(x,t) to X. Hence Gabai's homotopy hypothesis is satisfied.

Combining the lemma with [G], the desired oriented example is exactly a geometric realization with **s(p) ∈ R \ L**. Nonvanishing in A alone is insufficient.

**Logical countermodel to the realization shortcut.** Take P = A = Z and s = id. With E the trivial group and e the zero map, s is surjective but J = P, so L = A and every endpoint fibre contains zero. With E = Z/2 and e reduction modulo 2, the same surjective s has J = 2Z; the endpoint 1 has only odd s-values. Surjective realization therefore does not determine the answer without the kernel image. These are abstract algebraic models, not constructions of four-manifolds.

## A conditional norm reduction

Suppose an abelian group R has an involution τ and L is a subgroup satisfying

(1 + τ)R ⊆ L ⊆ R.

Then R/(1 + τ)R maps surjectively to R/L, by sending a coset represented by r to the coset r + L. The inclusion makes this well defined, and every target class has a representative in R. If τ = id, this says R/L is a quotient of R/2R; in particular, twice every element of R/L is zero. If additionally multiplication by two on R is surjective, then R = 2R ⊆ L, so R/L = 0.

For the geometric groups above, the duality formula preserves R = Σ(P(X)), and [S]'s doubling inclusion gives the required norm inclusion. Thus, subject to those established inputs, trivial involution plus 2-divisibility of R rules out an oriented example on X. More generally, surjectivity of 1 + τ on R rules one out. No actual manifold with the requisite nonzero quotient R/L is provided, and a nonzero quotient R/(1 + τ)R does not force R/L to be nonzero: L can be larger than the norm image.

## Rejected shortcuts and the precise remaining gap

1. If Wh₂(π₁X) = 0, every first obstruction is zero, so [G] rules out the requested oriented example on X. In particular, the free and free-abelian cases supplied by [G] cannot work. This includes familiar simply-connected candidates.
2. Stable realization of a nonzero a constructs a pseudo-isotopy on a possibly stabilized manifold Y. One must still prove a ∉ Σ(J(Y)). The endpoint is not controlled merely by the value assigned to that pseudo-isotopy.
3. A nonzero secondary obstruction Θ for an endpoint already admitting Σ = 0 can obstruct ordinary isotopy while [G] still forces stable isotopy. Therefore those secondary examples cannot supply this separation. Gluing a relative example into a closed manifold would additionally require a proof that the needed first-obstruction quotient survives that operation. Neither extension of the map nor ordinary non-isotopy proves this.
4. The norm calculation provides a lower bound on L, not the upper bound needed to certify a surviving class. The product-boundary symmetry estimate in [S, Proposition 9.9] has hypothesis X = M³ × I. It is not applied here to arbitrary closed X.

The exact unresolved task is to find a closed oriented smooth X, an actual smooth pseudo-isotopy F, and a rigorous obstruction to Σ(F) lying in Σ(J(X)); alternatively, one would need a universal equality Σ(P(X)) = Σ(J(X)), together with treatment of any nonorientable scope. This packet establishes neither. Four approaches were completed; no fifth approach was spent after all available construction routes reached this same missing geometric computation.

## Current literature boundary

The 2026 paper of Gabai–Gay–Hartman–Krushkal–Powell repairs Quinn's simply-connected pseudo-isotopy argument. Its Theorem 1.1 trivializes a given smooth pseudo-isotopy after stabilization, a stronger statement in that scope than endpoint trivialization; Remark 1.4 distinguishes these assertions. It supplies no general fundamental-group answer here. [GGHKP]

Galvin–Nonino's 2025 preprint constructs topological pseudo-isotopy obstructions and includes stable smoothing of selected realizations (Lemma 6.3). Its Section 9 applications use the secondary obstruction for ordinary isotopy. Neither the category change nor that realization comparison supplies the missing first-obstruction kernel-image exclusion. [GN]

Lin–Xie–Zhang's 2026 abstract establishes infinite-rank ordinary relative mapping-class phenomena for I × Y³ and concordance groups. The abstract is not a theorem about failure of every S² × S² stabilization on closed four-manifolds. Only its abstract and version record were inspected here. [LXZ]

No solution was verified in this bounded review as of 2026-10-06. This is not evidence that no later, unindexed, or differently phrased solution exists.

## References

[K3] R. İ. Baykur, R. C. Kirby, D. Ruberman, *K3 – A New Problem List in Low-Dimensional Topology*, author preliminary version, Problem 4.74, p. 251. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

[G] D. Gabai, *3-Spheres in the 4-Sphere and Pseudo-Isotopies of S¹ × S³*, arXiv:2212.02004v2, 29 May 2024. https://arxiv.org/abs/2212.02004v2

[S] O. Singh, *Pseudo-isotopies and diffeomorphisms of 4-manifolds*, inspected arXiv:2111.15658v3, 14 November 2022. https://arxiv.org/abs/2111.15658v3 Published in *Journal of Topology* 18(4), e70043 (23 December 2025). https://doi.org/10.1112/topo.70043

[GGHKP] D. Gabai, D. Gay, D. Hartman, V. Krushkal, M. Powell, *Pseudo-isotopies of simply connected 4-manifolds*, *Forum of Mathematics, Pi*, published online 3 March 2026. https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/pseudoisotopies-of-simply-connected-4manifolds/76BC09B6D1CF91456A4189800D2B0494

[GN] D. Galvin, I. Nonino, *Pseudo-isotopy versus isotopy for homeomorphisms of 4-manifolds*, arXiv:2506.11905v1, 13 June 2025. https://arxiv.org/abs/2506.11905v1

[LXZ] J. Lin, Y. Xie, B. Zhang, *Pseudo-isotopies of 3-manifolds with infinite fundamental groups*, arXiv:2602.09454v1, 10 February 2026. https://arxiv.org/abs/2602.09454v1
