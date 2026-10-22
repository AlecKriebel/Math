# Mathematical correction C1 and simplification S1

**Read this correction together with the preserved [proof](artifacts/PROOF.md) and [independent audit](audit/INDEPENDENT_AUDIT.md). The general problem remains unsolved.**

The audited original files are preserved unchanged for reproducibility. This correction supersedes the assertion in PROOF.md §4 that the linking-sphere generator condition is essential as an extra hypothesis. The same qualification applies to the descriptions of that condition in the original research log and status.

## C1. Punctured homology S³ already forces acyclicity

Let Z be a compact topological 4-manifold with nonempty boundary, let p be an interior point, and set E = Z minus {p}. Suppose E has the integral homology of S³. Then Z is acyclic, and a small linking sphere about p automatically represents a generator of H₃(E).

**Proof.** Since E is connected and dense in Z, Z is connected. Local excision identifies Hᵢ(Z,E) with Z in degree four and zero in all other degrees. The long exact sequence gives H₁(Z) = H₂(Z) = 0. By the universal coefficient theorem H¹(Z; Z/2) = 0, so Z is orientable. A connected compact manifold with nonempty boundary has H₄(Z) = 0. Therefore the relevant part of the pair sequence is

    0 → Z → H₃(E) = Z → H₃(Z) → 0.

The first map is induced by a small linking sphere. Its injectivity makes it multiplication by a nonzero integer k, so H₃(Z) is finite. On the other hand, integral Poincaré–Lefschetz duality gives

    H₃(Z) ≅ H¹(Z, ∂Z).

The relative universal coefficient theorem identifies this group with Hom(H₁(Z, ∂Z), Z), because H₀(Z, ∂Z) = 0. It is thus torsion-free. Being both finite and torsion-free, H₃(Z) vanishes. Hence k = ±1. All reduced homology of Z is zero, and the linking sphere is a generator. Duality and the boundary pair sequence then show that ∂Z is an integral homology 3-sphere. □

The original sufficient implication was valid; its assertion that the extra generator condition was independent or essential was not.

### Corrected remaining gap

In a smoothing of M minus a point p, find a compact smooth codimension-zero submanifold Y whose complementary closed side Z is a compact topological manifold containing p, with Z minus {p} having the integral homology of S³. That would suffice: C1 supplies acyclicity and the homology-sphere boundary automatically.

Quinn's punctured-smoothing theorem does not provide this finite smooth cross-section or its end-side homology. In particular it does not force vanishing of the complementary end neighborhood's H₁ and H₂. The linking-sphere generator is not an additional obstruction once the compact-manifold and punctured-homology hypotheses hold. No equivalence for every fixed punctured smoothing is claimed.

## S1. The compact counterexample already embeds in standard S⁴

The compact obstruction X in PROOF.md §6 is defined as the exterior of a locally flat slice disk in B⁴. Therefore X is already a topological codimension-zero submanifold of B⁴, and hence of the standard smooth S⁴. Its locally flat boundary is handled using collars and corner rounding.

S⁴ has the desired decomposition. Thus the failure of inheritance to X is immediate, without the valid but unnecessary doubling-and-surgery argument in Proposition 6. A locally flat topological boundary in a smooth manifold need not be smooth; consequently this inclusion does not give X a compatible smoothing up to its boundary.

These corrections and simplifications do not produce a general proof or a closed counterexample. The substantive positive classes, compact obstruction, and cyclic-cover calculations pass the independent audit; no novelty claim is made.
