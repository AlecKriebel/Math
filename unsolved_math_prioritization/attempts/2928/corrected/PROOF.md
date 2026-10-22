# Normal invariant reduction for Kirby 4.52

## Scope and imported facts

The target concerns closed orientable topological four-manifolds with good fundamental group. The two given manifolds are simple-homotopy equivalent and become homeomorphic after connected sums with copies of S² × S². The requested map is existential: some simple equivalence from the second manifold to the first must belong to the Wall orbit of the identity. K3, Problem 4.52, is the source of this formulation [K3]. Fix an orientation on M. For the literal orientable formulation, each candidate map N → M induces the orientation on its domain, so both choices on the underlying N are allowed. If orientations on both manifolds are prescribed instead, the degree-one formulation is a separate, explicitly restricted version.

Write Sˢ_TOP(M) for the simple topological structure set, η for its normal-invariant map, and 0 for the invariant of the identity. The good-group topological surgery sequence gives

Lˢ₅(Z[π₁M]) · [id_M] = η⁻¹(0).

This exactness is an imported surgery theorem, not a consequence proved from the stable-homeomorphism assumption. Normal invariants for an oriented four-manifold have coordinates in H⁴(M; Z) ⊕ H²(M; Z/2); for a homotopy equivalence the signature coordinate is zero [KNV, §2.2].

## Proposition 1 Exact orbit criterion

Fix a simple equivalence f: N → M. Let Autˢ(M) be all simple self-equivalences of M, taken up to homotopy. Use the simple structure set of maps to M, with domain orientations transported by their maps. Then the target conclusion for this pair is equivalent to

0 ∈ {η(h ∘ f): h ∈ Autˢ(M)}.

Proof. Every h ∘ f is a simple equivalence. Conversely, given any other simple equivalence g: N → M, choose a homotopy inverse j of f. Its Whitehead torsion is zero by the inverse formula. The composite h = g ∘ j is consequently simple and satisfies h ∘ f ≃ g. Thus the displayed set is exactly the set of normal invariants of all allowable equivalences N → M. Apply surgery exactness. ∎

For a fixed-oriented version in which f and every allowable g have degree one, the same proof uses precisely the orientation-preserving subgroup Autˢ₊(M). Restricting to this subgroup without fixing the oriented version would silently omit the other orientation branch. No claim that the two branches coincide is needed.

This criterion deliberately avoids treating η as an untwisted additive homomorphism on self-equivalences. In particular, η(f) ≠ 0 for one chosen f cannot refute the question.

## Proposition 2 A restricted positive conclusion

Assume π₁M is good and Wh(π₁M) = 0. Suppose a degree-one homotopy equivalence f: N → M has normal invariant represented by an immersed two-sphere on which w₂(M) vanishes. Then some simple equivalence N → M is in the identity Wall orbit.

Proof. The normal-invariant cancellation lemma of Kasprowski–Land [KL, Lemma 3.3] gives a homotopy equivalence f′ with η(f′) = 0. The condition Wh(π₁M) = 0 ensures f′ is simple. Surgery exactness now applies. Neither stable homeomorphism nor a smooth realization of the Wall action is needed for this conditional conclusion. ∎

One sufficient hypothesis for the spherical condition is that M is almost spin and κˢ₂: H₂(π₁M; Z/2) → Lˢ₄(Z[π₁M]) is injective. Indeed, the surgery obstruction and signature coordinate of f vanish, so the assembly formula gives κˢ₂(c_*PD(kerv(f))) = 0. Injectivity gives c_*PD(kerv(f)) = 0. The low-degree homology sequence of the universal-cover fibration makes this class spherical; almost spin makes w₂ zero on that sphere. These are the standard normal-invariant and pinching arguments underlying [KNV, Proposition 4.3]. The extra hypotheses are not established for every good group.

## Prior consequence for torsion-free three-manifold groups

The proof of [HKPR, Theorem 12.6] establishes a zero-normal-invariant equivalence when the fundamental group is a torsion-free three-manifold group and the Kirby–Siebenmann invariants agree. It also uses Wh(π) = 0. Stable homeomorphism supplies the matching Kirby–Siebenmann invariant. Therefore, whenever such a group is good, surgery exactness proves the requested Wall-orbit conclusion. This is an inference from prior work, not a novelty claim. It includes the solvable torsion-free three-manifold groups identified as good in that source.

## Exact unresolved implication

For a general good group, no argument here proves that the stable-homeomorphism hypothesis forces the set in Proposition 1 to contain zero. Nor is a pair constructed for which that set omits zero. The stable normal-type classification supplies bordism information with normal structures allowed to vary. A normal bordism over M ending in a chosen equivalence is different data. The missing step is the realization or cancellation of the remaining invariant by an unstabilized simple self-equivalence.

The original question remains unresolved by this packet. The conditional statements above are consequences of existing results.

## References

- [K3] *K3: A New Problem List in Low-Dimensional Topology*, Problem 4.52, pp. 231–232. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [KNV] D. Kasprowski, J. Nicholson, S. Veselá, *Stable equivalence relations on 4-manifolds*, arXiv:2405.06637v2; published in Proc. London Math. Soc. 131 (2025), e70101. https://arxiv.org/abs/2405.06637v2
- [KL] D. Kasprowski, M. Land, *Topological 4-manifolds with 4-dimensional fundamental group*, Lemma 3.3, pp. 6–7, arXiv:2007.03399v3; Glasgow Math. J. 64 (2022), 454–461. https://arxiv.org/abs/2007.03399v3
- [HKPR] J. Hillman, D. Kasprowski, M. Powell, A. Ray, *Homotopy classification of 4-manifolds with 3-manifold fundamental group*, §12.3, pp. 60–61, arXiv:2508.07504v1. Public preprint. https://arxiv.org/abs/2508.07504v1
