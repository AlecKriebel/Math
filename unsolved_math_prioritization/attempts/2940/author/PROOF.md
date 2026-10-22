# KP-4.64: ordinary Bauer–Furuta separation and the irreducibility gap

**Disposition: unsolved after five substantive approaches.** This note gives credited reductions, excluded construction routes, and a precise sufficient realization problem. It does not construct the requested manifold, refute its existence, or claim a new invariant theorem.

## 1. Target and conventions

Problem 4.64 of Baykur–Kirby–Ruberman's *K3: A New Problem List in Low-Dimensional Topology*, printed p. 242, asks for an irreducible closed smooth four-manifold with nonzero Bauer–Furuta invariant and zero Seiberg–Witten invariant. Its proposer is M. Stoffregen and its scribe is I. Dai. The source's discussion explicitly excludes the familiar connected-sum examples by requiring irreducibility. Its 2026 preliminary version still describes the irreducible case as unknown. This is a dated source assessment, not proof that no later result exists.

We use the ordinary S¹-equivariant Bauer–Furuta invariant of a single oriented spinᶜ four-manifold. “SW vanishes” means vanishing for **every** spinᶜ structure and every ordinary integer-valued insertion, not just vanishing at one chosen structure. A family invariant, a relative invariant, a Pin⁻(2) variant, or an invariant of a diffeomorphism cannot be substituted. Pin(2) symmetry is used below only through a theorem that proves nonvanishing after restriction to the ordinary S¹ invariant.

The explicit deductions below take place in the chamber-independent range b⁺>1. Most also impose b₁=0. These are **subclasses studied**, not extra assumptions inserted into the original question. No conclusion is drawn about the whole b₁>0 range or about choices of chamber when b⁺=1. Irreducibility is smooth connected-sum irreducibility, with the conventional allowance for a homotopy-sphere summand; every connected sum rejected below has summands of positive second Betti number, so that convention does not affect the rejection.

For a spinᶜ structure s, write c=c₁(s), r=indℂ Dₛ, and k for its expected Seiberg–Witten dimension. The standard index identities are

    r = (c²−σ)/8,
    k = (c²−2χ−3σ)/4 = 2r−(1−b₁+b⁺).

Here χ=2−2b₁+b⁺+b⁻ and σ=b⁺−b⁻. The second equality follows by subtracting 2r=(c²−σ)/4 and using (χ+σ)/2=1−b₁+b⁺.

### Lemma 1: the parity mechanism

If b₁=0 and b⁺ is even, every ordinary integer-valued SW invariant is zero.

**Proof.** The index r is an integer, so k=2r−1−b⁺ is odd for every spinᶜ structure. Ordinary SW insertions are taken from Z[U]⊗Λ*(H₁(X;Z)/torsion), with U of degree two and H₁ generators of degree one. When b₁=0 there are no free degree-one generators, hence no monomial of odd degree. None can match k; negative dimensions also contribute zero. This proves vanishing of all ordinary numerical invariants. It proves nothing about the BF class, which may be torsion. ∎

This is the ordinary invariant convention used in Bauer–Furuta I, Proposition 3.3 and its proof; it is not a claim about variants with other coefficient systems.

## 2. Attempt 1: connected sums and their exact failure

Let K denote a standard K3 surface in its complex orientation and Xₘ=#ᵐK. The connected-sum identities give

    χ(Xₘ)=22m+2, σ(Xₘ)=−16m,
    b⁺(Xₘ)=3m, b⁻(Xₘ)=19m.

For the spin structure, c=0, r=2m and k=m−1.

Bauer's connected-sum theorem [B2, Theorem 1.1] identifies BF of a connected sum with the equivariant smash product. For K, the spin structure has SW=±1 and all other SW invariants vanish [B2, proof of Corollary 1.4]. Its underlying nonequivariant BF class is the Hopf class η [B2, Proposition 4.4]. Thus two and three copies give η² and η³, which are nonzero. Four copies still have nonzero **equivariant** BF: the four-summand criterion applies because each b⁺=3 and total b⁺=12≡4 (mod 8) [B2, Proposition 4.5]. One must not infer the fourth case from η⁴, which is zero nonequivariantly.

All ordinary SW invariants of Xₘ vanish for m≥2 by the usual positive-b⁺ connected-sum vanishing, recovered in [B2, p. 2]. For m=2 or 4 Lemma 1 is an independent check. For m=3, parity does **not** prove this vanishing; the connected-sum theorem is needed.

Nevertheless Xₘ=K#Xₘ₋₁ is visibly reducible for every m≥2: both factors have nonzero H₂. For m≥5 the familiar K3 connected sums also lose every ordinary BF invariant, by [B, Theorem 8.5(4)] and the smash-product formula. Merely adding more summands does not help.

**Exact gap:** replacing this differentiable connected sum by an irreducible smooth structure requires an additional construction and proof. Knowing its intersection form, homeomorphism type, or nonzero BF alone does not remove its displayed smooth splitting.

## 3. Attempt 2: which low-dimensional target groups can hide SW?

Suppose b₁=0, b⁺>1, and r≥2. Bauer–Furuta I, Propositions 3.3–3.4, identify the relevant group and comparison as

    BF(X,s) ∈ πₛ^(b⁺−1)(CP^(r−1)),
    h: πₛ^(b⁺−1)(CP^(r−1)) → H^(b⁺−1)(CP^(r−1);Z).

The multiplicity of h(BF) is SW. In particular SW=0 forces BF into ker h. If k<0, the target degree exceeds the dimension of CP^(r−1); the stable cohomotopy group is zero. For 0≤k≤4, [B1, Lemma 3.5] computes the kernel:

| k | ker h |
|---|---|
| 0 | 0 |
| 1 or 2 | Z/gcd(2,r) |
| 3, r even | Z/gcd(24,r) |
| 3, r odd | Z/(gcd(24,r−3)/2) |
| 4 | 0 |

Z/1 means the trivial group. The theorem is invoked only in the stated r≥2, b⁺>1 range, so no negative-dimensional projective space occurs.

### Proposition 2: necessary conditions within this range

If BF(X,s)≠0 but SW(X,s)=0, then k is not negative, zero, or four. If k=1 or two, r is even. In those two cases respectively b⁺≡2 or 1 (mod 4).

**Proof.** Negative k gives the zero group. At k=0 and four the comparison is injective by the displayed calculation. At k=1 and two its kernel is nonzero precisely when r is even. Substituting in b⁺=2r−k−1 gives the congruences. ∎

The k=0 injectivity also has a direct explanation: the top cell of CP^(r−1) has dimension b⁺−1, and the lower skeleton is too small to contribute in that degree. Stable maps in that degree are classified by their integral degree. The k=1, two, three and four entries use the published stable-homotopy calculation, not a finite numerical computation made here.

**Exact gap:** a nonzero torsion target is only a possible value. It is not a realization theorem for monopole maps, and it supplies no irreducibility proof. This route gives a useful rejection test, not a candidate.

## 4. Attempt 3: replacing an S³ neck by a −2-sphere gluing

Let X₀ and X₁ contain embedded spheres C₀,C₁ with Cᵢ²=−2. Remove their disk-bundle neighborhoods and identify the RP³ boundaries by the orientation-reversing gluing in Bauer's construction; denote the result X₀#₂X₁.

The relevant theorem is not the unrestricted connected-sum formula. [B, Theorem 8.4] says that for each spinᶜ structure on this result there are inducing structures on X₀,X₁ whose Chern-class evaluations on the two spheres are respectively 0 and 2, in one order, and whose BF classes smash to the BF class of the result. The incompatibility arises from interchange of the two boundary spin structures.

### Proposition 3: a credited gluing obstruction

If every BF-supported Chern class on each Xᵢ evaluates to zero on Cᵢ, then every ordinary BF class on X₀#₂X₁ is zero.

**Proof.** Fix any spinᶜ structure on the glued manifold. In the factorization above, one inducing class has evaluation 2. That factor cannot be BF-supported under the hypothesis, so its BF class is zero. The smash product is zero. This holds for every structure. ∎

An algebraic way to check the hypothesis is useful. Let Vᵢ be the rational span of all BF-supported Chern classes. If the intersection pairing restricted to Vᵢ is positive semidefinite, all such classes are perpendicular to Cᵢ. Indeed the local sphere reflection is a diffeomorphism, acts by

    R_C(c)=c+(c·C)PD(C),

and preserves BF support. If c·C≠0, the difference R_C(c)−c puts PD(C) in Vᵢ. Its square −2 contradicts positive semidefiniteness. This is Bauer's proof of [B, Theorem 8.6(3)], restated to show the exact mechanism.

In particular, standard K3 surfaces satisfy the zero-evaluation hypothesis: their only BF-supported structure has c=0, by [B2, §4.3 and proof of Corollary 1.4]. Consequently gluing two standard K3 surfaces along −2 spheres has **all BF classes zero**. The conclusion does not depend on resolving its irreducibility.

The elementary topology also differs from a connected sum. A −2 disk bundle has χ=2 and signature −1; RP³ has Euler characteristic zero and is a rational homology sphere. Euler characteristic and signature additivity, and rational Mayer–Vietoris, give for the two-K3 gluing

    χ=44, σ=−30, b₁=0, b⁺=6, b⁻=36.

For b₁=0, Mayer–Vietoris first shows that removing the disk bundle does not change rational H₁: the boundary H₁ vanishes and its H₀ map to the two pieces is injective. Applying the same sequence to the final gluing gives H₁=0. The displayed b± then follow from χ and σ. Lemma 1 gives SW vanishing, but Proposition 3 kills precisely the BF nonvanishing needed by the question.

**Exact gap:** a different cut-and-paste construction would need a verified ordinary-BF gluing mechanism with nonzero compatible factors and an independent irreducibility argument. The present one does not work.

## 5. Attempt 4: spin rational-cohomology K3#K3

This route removes both invariant computations from a sharply specified realization problem.

### Theorem 4: sufficient realization criterion (credited consequence)

If there exists an irreducible closed smooth **spin** oriented four-manifold X whose oriented rational cohomology ring is that of K3#K3, then X solves KP-4.64.

**Proof.** The ring and orientation imply b₁=0, b⁺=6, b⁻=38, χ=46 and σ=−32. Lemma 1 proves vanishing of every ordinary SW invariant, including all structures other than the spin structure. For each spin structure, Furuta–Kametani–Minami [FKM, Theorems 1 and 19] prove that its ordinary S¹ stable-homotopy invariant is nonzero. Hence the ordinary BF invariant is nonzero. Closedness, smoothness and irreducibility are hypotheses, so all requirements hold. ∎

The spin hypothesis is essential and is not inferred from the rational cohomology ring. A rational ring does not detect w₂. In the simply connected integral-form case, a manifold with form 4(−E₈)⊕6H is spin, but no irreducible realization of that form is constructed here.

For the spin structure the index calculation is r=4 and k=1, placing the invariant in the Z/2 kernel from §3. FKM's nonvanishing is more than a Pin(2)-class being nonzero. Their δ is defined on the **S¹** stable homotopy set, δ(0)=0, and Theorem 19 gives δ(BF)=1. Their proof checks the explicit two-Hopf-factor model (Lemma 13), independence and stabilization of δ (Lemmas 2–7), and invariance of δ under changing a Pin(2)-equivariant representative (Proposition 16). Thus the restriction relevant to this problem remains nonzero.

A tempting numerical extension fails for the spin structure. For spin X with b₁=0, b⁺=4n−2 and b⁻=20n−2, n≥3, one still has r=2n and k=1. The target group is again Z/2. But [FKM, Theorem 20] gives δ(BF)=0; δ is bijective in this range by their Lemma 12. Thus the BF class of **every spin structure** is zero in this family. This does not prove vanishing for non-spin spinᶜ structures.

**Exact gap:** construct and prove irreducible a spin rational-cohomology K3#K3. FKM supplies no such realization. The ordinary connected sum satisfies the invariant conditions but fails irreducibility. This criterion is sufficient, not equivalent to the unrestricted original question.

## 6. Attempt 5: finite quotients of the known connected-sum models

One might try to destroy the separating neck by a free finite group action on Xₘ=#ᵐK. A simple necessary condition is already restrictive.

### Proposition 5: quotient-degree obstruction

If a finite group G acts freely, smoothly and orientation-preservingly on Xₘ, then its order q satisfies

    q divides gcd(16,3m+1).

In particular there is no nontrivial such action for even m. Among the BF-nonzero models m=2,3,4, only m=3 can have a nontrivial quotient, and then q=2.

**Proof.** The quotient Y is a closed oriented smooth four-manifold with π₁(Y)=G, since Xₘ is simply connected. Hence b₁(Y)=0. Euler characteristic and signature are multiplicative under finite oriented coverings, so

    χ(Y)=(22m+2)/q, σ(Y)=−16m/q.

The second expression implies q|16m. Also

    1+b⁺(Y)=(χ(Y)+σ(Y))/2=(3m+1)/q

is an integer, so q|3m+1. Since gcd(m,3m+1)=1, the common divisors of 16m and 3m+1 are exactly those of 16 and 3m+1. If m is even, 3m+1 is odd and the gcd is one. For m=3 it is gcd(16,10)=2. ∎

The use of signature multiplicativity here is the standard signature theorem for a finite unbranched oriented covering, not a statement about arbitrary branched quotients. An orientation-reversing or nonfree action is outside the proposition.

For the one surviving small numerical case m=3,q=2, the quotient would have χ=34, σ=−24, b⁺=4 and b⁻=28. It would have zero ordinary SW by Lemma 1. However arithmetic does not prove an action exists, that the quotient is irreducible, or that its BF class is nonzero. Nonzero BF of a covering space does not supply a general descent theorem in this note.

**Exact gap:** the m=3 double-quotient route still needs a concrete free action, an irreducibility proof for its quotient, and an ordinary-BF computation on that quotient. The m=2 and four quotient routes are excluded before those questions arise.

## 7. What is and is not established

The five approaches do not provide a full solution. They establish:

1. The familiar two-, three- and four-K3 separations remain smoothly reducible.
2. Explicit low-dimensional Hurewicz-kernel tests eliminate several possible BF witnesses; a nonzero target group is not geometric realization.
3. The −2-sphere gluing of standard K3s has BF=0 for every structure, even though parity forces SW=0.
4. An irreducible spin rational-cohomology K3#K3 would suffice, by a published theorem plus a proved parity argument; no such manifold is produced.
5. Free oriented finite quotients of even K3 connected sums are arithmetically impossible; the triple-K3 double-quotient possibility remains unproved and uncomputed.

The remaining task is a geometric realization with a rigorous irreducibility certificate and the stated ordinary invariant separation, or a theorem ruling all such realizations out. None of the calculations above constitutes either. No historical novelty, human peer review, or formal proof verification is claimed.

## References

- [K3] R. İ. Baykur, R. C. Kirby, D. Ruberman, *K3: A New Problem List in Low-Dimensional Topology*, 2026 preliminary author version, Problem 4.64, p. 242. https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf
- [B1] S. Bauer and M. Furuta, *A stable cohomotopy refinement of Seiberg–Witten invariants. I*, Invent. Math. 155 (2004), 1–19. https://doi.org/10.1007/s00222-003-0288-5 ; inspected complete author preprint: https://arxiv.org/abs/math/0204340
- [B2] S. Bauer, *A stable cohomotopy refinement of Seiberg–Witten invariants. II*, Invent. Math. 155 (2004), 21–40. https://doi.org/10.1007/s00222-003-0289-4 ; inspected complete author preprint: https://arxiv.org/abs/math/0204267
- [B] S. Bauer, *Refined Seiberg–Witten invariants*, author manuscript, arXiv:math/0312523v1 (2003), especially §§5–6 and 8. https://arxiv.org/abs/math/0312523
- [FKM] M. Furuta, Y. Kametani and N. Minami, *Stable-homotopy Seiberg–Witten invariants for rational cohomology K3#K3's*, J. Math. Sci. Univ. Tokyo 8 (2001), 157–176. https://www.ms.u-tokyo.ac.jp/journal/pdf/jms080109.pdf
