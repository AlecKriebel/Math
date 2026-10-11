# Symmetric degeneration target for problem 30005126

The intended question compares ordinary and symmetric geometric degenerations. It does not compare ordinary degeneration with the Hom-order.

## Duality-compatible precise formulation

Work over the complex numbers. Let Q be a finite quiver with an arrow-reversing involution σ, let I be an admissible σ-stable ideal, and let A = C Q/I be representation-directed. Here representation-directed has its usual module-theoretic meaning: there is no cyclic chain of nonzero nonisomorphisms between finite-dimensional indecomposable A-modules.

To make the intended self-dual module setup explicit, also assume that I is preserved by the signed path anti-involution ρ defined on vertices by ρ(eᵢ) = eσ(i) and on arrows by ρ(α) = -σ(α), with reversal of products. Then the twisted dual (∇M)ᵢ = (Mσ(i))* and (∇M)α = -Mσ(α)* preserves A-modules. This is the compatibility required for that duality; the distinction from the report's shorter printed hypotheses is stated below.

Fix ε in {+1, -1}, a finite-dimensional Q₀-graded vector space V = ⊕ᵢ Vᵢ, and a nondegenerate bilinear form B such that

- B(v,w) = ε B(w,v);
- B(Vᵢ,Vⱼ) = 0 unless j = σ(i).

In particular dim Vᵢ = dim Vσ(i), and when ε = -1 every fixed-vertex space Vᵢ has even dimension. Let R(A,V) be the affine variety of arrow maps satisfying I. Define Rε(A,V,B) by the additional, arrowwise equations

B(Mα v,w) + B(v,Mσ(α) w) = 0

for every arrow α:i→j, v in Vᵢ, and w in Vσ(j). This is the source's skew-adjoint convention. The sign ε concerns the bilinear form; the displayed arrow-adjoint relation has a minus sign for both choices of ε.

Put G = ∏ᵢ GL(Vᵢ), acting by (g·M)α = gⱼ Mα gᵢ⁻¹, and H = {g in G : B(gv,gw) = B(v,w)}. The group H is the full graded isometry group, not a replacement by its identity component or by special orthogonal factors.

For M,N in Rε(A,V,B), define

M ≤deg N  ⇔  N belongs to the Zariski closure of G·M,

M ≤degε N  ⇔  N belongs to the Zariski closure of H·M.

Does M ≤deg N imply M ≤degε N for every such choice of A, ε, V, B, M, and N?

Equivalently, is closure(H·M) = closure(G·M) ∩ Rε(A,V,B) for every M in Rε(A,V,B)? Closures may be taken in their corresponding representation varieties. Since Rε(A,V,B) is closed and H·M ⊆ G·M, the reverse implication always holds.

## Source-literal distinction

The OWR report prints an admissible σ-stable ideal and defines the symmetric locus by skew-adjoint arrow maps. Taken literally as an orbit question, those arrowwise equations remain meaningful even without the additional signed-stability assumption. The report also uses the twisted self-duality ∇. The formulation above makes the compatibility needed for that self-dual interpretation explicit. We do not claim that unsigned σ-stability alone implies signed stability, or that the unrestricted source-literal arrowwise question and the duality-compatible question are identical. This clarification is not a claimed error in the published type-A theorem, whose relation ideal is zero.

Here “symmetric” refers to the quiver involution and compatible representation theory, rather than the separate notion of a symmetric Frobenius algebra.

## Attribution and status

This is the conjectural extension described by Magdalena Boos, joint with Giovanni Cerulli Irelli, in “Approaching symplectic/orthogonal orbit closure relations,” Oberwolfach Report 23/2022, printed pp.1300–1302, especially the final paragraph on p.1302. The report is in Oberwolfach Reports 19 (2022), no.2, pp.1239–1312, DOI [10.4171/OWR/2022/23](https://doi.org/10.4171/OWR/2022/23); the publisher's publication date is 14 April 2023. [Official report PDF](https://ems.press/content/serial-article-files/46962).

Boos and Cerulli Irelli prove the type-A quiver case in Theorem 7.1 of “On degenerations and extensions of symplectic and orthogonal quiver representations,” Arkiv för Matematik 63 (2025), 61–115, DOI [10.4310/ARKIV.2025.v63.n1.a3](https://doi.org/10.4310/ARKIV.2025.v63.n1.a3). The published theorem on p.107 assumes A = C Q with Q a symmetric type-A quiver. The representation-directed extension is still explicitly conjectured on p.69. [Published PDF](https://iris.uniroma1.it/retrieve/7e049881-5a31-4c23-b75f-3ea79f4d19e4/Cerulli_degenerations_2025.pdf).

The ordinary Ext, degeneration and Hom orders already coincide for representation-directed algebras by Bongartz's 1996 work. The correct bibliographic DOI is [10.1006/aima.1996.0053](https://doi.org/10.1006/aima.1996.0053). This attribution relies on the published literature, rather than a new reconstruction of Bongartz's proof.

A bounded primary-source literature check on 11 October 2026 located no general resolution of the symmetric representation-directed target. That is a dated search result, not proof that no resolution exists. The present work establishes a source-target correction and does not solve the general conjecture.
