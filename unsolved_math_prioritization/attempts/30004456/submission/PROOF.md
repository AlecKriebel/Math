# Literature resolution of the Gardam–Kielak HNN-complexity conjecture

Record: 30004456, OWR-1703863-005, queue rank 612.
Date checked: 2026-10-04 UTC. Classification proposed: **already_solved, 1/5**.

This is a verification of a theorem's applicability, not a new proof of the theorem or a claim of a new mathematical discovery. The decisive source is the preprint by Andrei Jaikin-Zapirain, Monika Kudlinska and Pablo Sánchez-Peralta, *Thurston norm, polytopes and splitting complexity*, arXiv:2606.31774v2, 31 August 2026. The version is not described here as peer reviewed. All credit for the general resolution belongs to those authors.

## 1. Exact statement and necessary conventions

Let G=F_n ⋊_α Z, where n is finite and α is an automorphism, and let φ:G→Z be **nonzero**. Write φ(G)=dZ, d>0, and φ₀=φ/d. An admissible splitting is an isomorphism

G = < A,t | t⁻¹bt=θ(b), b∈B >,

where A and B are finitely generated, B≤A, θ:B→A is injective, A≤ker φ, and φ(t)=d. Equivalently its canonical exponent homomorphism is φ₀. For an epimorphism d=1. Reversing the stable letter handles the opposite orientation.

Then the intended conjecture is

−χ⁽²⁾(ker φ) = min { −χ(A) : admissible splittings as above }.

Here χ(A) is the ordinary group Euler characteristic of a finite classifying space. Such spaces exist for the indicated finitely generated subgroups. We do not assume the kernel itself is finitely generated or that A is free.

The source report's unqualified word “character” needs this convention. If “inducing φ” specifically means stable letter ↦1, φ must instead be explicitly required to be surjective. These formulations agree after identifying the image dZ with Z.

The zero character is excluded, as in the resolving paper. Every canonical HNN exponent character is onto Z, so it cannot be zero. If the catalogue is read literally as including φ=0 with that definition, the set over which its minimum is taken is empty. For example, G=Z² has χ⁽²⁾(G)=0 but has no HNN exponent character equal to zero. This is a wording defect, not an unresolved mathematical case or a new counterexample to the intended conjecture.

## 2. Inputs used

[JKS] is https://arxiv.org/abs/2606.31774v2. Its Corollary 1.5 (p. 3; proof p. 31) supplies an admissible splitting G=A*B with b₁⁽²⁾(ker φ)=b₁⁽²⁾(B). Its Theorem 3.3(ii) (p. 12, proof pp. 12–16) supplies, for every admissible splitting of a finitely presented G with b₁⁽²⁾(G)=0,

b₁⁽²⁾(ker φ) ≤ b₁⁽²⁾(A) ≤ b₁⁽²⁾(B).

[FH] Feighn–Handel, *Mapping tori of free group automorphisms are coherent*, Ann. Math. 149 (1999), 1061–1077, Theorem 1.2, p. 1063, gives finite classifying spaces for finitely generated subgroups of G. Primary copies: https://annals.math.princeton.edu/articles/12500 and https://arxiv.org/abs/math/9905209.

[Gab] Gaboriau, *Invariants ℓ² de relations d’équivalence et de groupes*, Publ. Math. IHÉS 95 (2002), 93–150, Théorème 6.6, p. 146, gives this degreewise vanishing implication: in an extension with infinite amenable quotient, finiteness of a kernel's L²-Betti number in a given degree implies vanishing for the whole group in that degree. Primary source: https://www.numdam.org/item/PMIHES_2002__95__93_0/.

We also use basic free-group subgroup theory, b₀⁽²⁾(S)=0 for infinite S, and the L² Euler–Poincaré identity for a finite classifying space.

## 3. Complete application proof

First suppose n≥1, and let ψ:G→Z be the original free-by-cyclic projection. The group G is torsion free: a finite-order element projects trivially under ψ and would then be a finite-order element of F_n. It has a finite classifying space, obtained as the mapping torus of a graph homotopy equivalence representing α. In particular it is finitely presented.

Since F_n is infinite and has finite first L²-Betti number n−1, [Gab] applied to 1→F_n→G→Z→1 gives b₁⁽²⁾(G)=0. Thus the hypotheses of both cited [JKS] results hold. Corollary 1.5 applies directly because G is torsion-free and (finitely generated free)-by-cyclic; “virtually” includes the index-one case.

We next justify every Euler-characteristic conversion. For an arbitrary subgroup S≤G, put D=S∩F_n. If ψ(S)=0, S is a free group, so b_j⁽²⁾(S)=0 for j≥2. If ψ(S)≠0, it is infinite cyclic and

1→D→S→ψ(S)→1

is exact. The subgroup D is free, possibly infinitely generated. If D=1, S is cyclic and the same higher-degree vanishing follows. Otherwise, b_j⁽²⁾(D)=0<∞ for each j≥2, so [Gab] gives b_j⁽²⁾(S)=0 in those degrees. Consequently **every infinite subgroup S≤G has L²-homology concentrated in degree 1**. This argument does not incorrectly assume that b₁⁽²⁾(D) is finite.

The group G cannot be infinite cyclic: its nontrivial normal subgroup F_n would then have finite-index image in a cyclic group, contrary to G/F_n≅Z. Thus N=ker φ is nontrivial (otherwise G embeds in Z), hence infinite by torsion freeness. For every admissible splitting, A is nontrivial: A=1 would force B=1 and G≅Z. Hence A is infinite too.

Choose the splitting provided by Corollary 1.5. Since its edge group B is finitely generated, b₁⁽²⁾(B) is finite. Therefore b₁⁽²⁾(N) is finite, and the preceding vanishing proves that χ⁽²⁾(N) is well-defined and

−χ⁽²⁾(N)=b₁⁽²⁾(N).

For any admissible base A, [FH] gives a finite classifying space. Euler–Poincaré and the vanishing already proved give

−χ(A)=−χ⁽²⁾(A)=b₁⁽²⁾(A).

Theorem 3.3(ii), now for an arbitrary admissible splitting, proves

−χ⁽²⁾(N) ≤ −χ(A).

For the splitting supplied by Corollary 1.5 the same inequalities read

b₁⁽²⁾(N) ≤ b₁⁽²⁾(A) ≤ b₁⁽²⁾(B)=b₁⁽²⁾(N).

They force equality. Thus the lower bound is attained; the assertion is a **minimum**, not merely an infimum. This also resolves the apparent mismatch between the report's **base** complexity −χ(A) and the preprint's **edge** complexity b₁⁽²⁾(B).

If n=0 is allowed, G=Z and every nonzero φ is injective. Thus N=1 and −χ⁽²⁾(N)=−1. An admissible base lies in N, so A=B=1 and G=1*1, with the prescribed stable letter. Its complexity is −χ(1)=−1. This elementary case must be handled separately: replacing −χ⁽²⁾(1) by b₁⁽²⁾(1)=0 would be wrong.

Finally, multiplying a nonzero character by a nonzero integer does not change its kernel or the class of admissible normalized splittings (up to orientation). Hence the proof for φ₀ gives the stated nonprimitive formulation. In contrast, the homogeneous Thurston norm scales with d; it should not be confused with the unscaled invariant of the kernel. This completes the application proof.

## 4. Independent consistency check on base versus edge

Both A and B have finite classifying spaces. The usual graph-of-spaces construction for the HNN extension gives

χ(G)=χ(A)−χ(B).

The mapping-torus model of G has χ(G)=0. Thus χ(A)=χ(B) for every admissible splitting. For n≥1, B also cannot be trivial: that would give χ(A)=1, contradicting χ(A)=−b₁⁽²⁾(A)≤0. So −χ(A)=b₁⁽²⁾(A)=b₁⁽²⁾(B). This gives another check of the base/edge translation; the main proof needs only the squeeze above.

## 5. Scope of the verification

The full target follows by the written argument from the precisely identified existing results. The internal proof architecture of [JKS] was inspected, especially Theorem 3.3, the enlargement argument proving Theorem 1.3(ii), and the closure argument proving Theorem 1.4. The separate ledger records dependencies. This packet does not claim a fresh reproof or formal verification of all ring-theoretic and L²-homological results used inside that 38-page preprint. There is no newly proved general splitting theorem here, no human peer review supplied by this packet, and no computational proof of the infinite family.
