# Independent adversarial audit: nonabelian diagonal parabolic obstruction

Reviewer: `/root/p21126_superexp/double_adversary`; UTC: 2026-10-24T21:23:37.731431+00:00. Inputs: `../DIAGONAL_PARABOLIC_OBSTRUCTION.md` and `../DIAGONAL_SHARPNESS_EXAMPLE.md`; exact hashes in REVIEWED_INPUTS.json.

**Outcome: PASS for the explicitly stated diagonal/parabolic construction filter.** I found no outstanding substantive objection after independently reconstructing the factor separation and checking the cited primary structural inputs. This does not certify priority, an obstruction to every embedding of a factor-diagonal amalgam, or a solution of 21.126.

## Exact source audit

I directly inspected the cached primary Duncan–Kazachkov–Remeslennikov text, arXiv:math/0702431. Equation (1.1) states the block centralizer formula. Definition 3.1 gives canonical quasiparabolic subgroups; Definition 3.2 and Lemma 3.3 give the standard form with nonsingleton root blocks and an external parabolic factor. Theorem 3.12 implies that ANY centralizer is conjugate to such a standard form. Its additional closed-set requirements on Y are stronger information than the application needs; omitting those unused requirements does not invalidate the weaker consequence used here. Lemma 2.7 explicitly gives

    G(E) ∩ G(F)^g = G(E∩F∩T)^{g2},  with g2∈G(E).

Thus the internal-conjugator property for an intersection inside a standard parabolic really is supplied by the cited theorem. Merely knowing an intersection is parabolic somewhere in A would not have been sufficient for the factorwise step.

## Independent reconstruction

Put U=α(H), V=β(H), with elementwise commutation. After simultaneous conjugation write C_A(U)=B×A(Y), where B is the product of cyclic root-block groups on support S and Y is contained in the external link L(S). The same simultaneous conjugation preserves the hypothesis that P is parabolic.

Let w be the product of the independent root blocks. The centralizer of B equals the centralizer of w: each is B×A(L(S)), by the block formula (every element of the displayed product centralizes every block). Centralizing the standard parabolic A(Y) is equivalent to belonging to A(Y^⊥). Since S⊆Y^⊥, all of B belongs to the latter subgroup, and uniqueness of the disjoint-support product coordinates gives

    C_A(C_A(U)) = B × A(L(S)∩Y^⊥).

This verifies the potentially dangerous intersection step: it does not assert that a cyclic block subgroup is itself a full parabolic. For k=0, w=1 and B=1, so the same calculation gives A(Y^⊥), as required.

Let T=L(S)∩Y^⊥ and C=Y∩T. Because Y⊆L(S), C=Y∩Y^⊥. Any two distinct vertices of C commute, so A(C) is free abelian. C commutes with Y by its defining centrality and with T because T⊆Y^⊥. The sets S, Y\C, T\C, C are pairwise disjoint and commute across sets. Hence their union defines the genuine standard join subgroup

    K=A(S) × A(Y\C) × A(T\C) × A(C).

No abelianness of A(S) is assumed. Only B and A(C) are abelian. U lies in B×A(T\C)×A(C), and V lies in B×A(Y\C)×A(C). Thus [U,U] lies purely in the T\C factor and [V,V] purely in the Y\C factor. This is the required separation of derived coordinates; whole original generators can retain shared abelian/root coordinates.

By Lemma 2.7, R=P∩K is a parabolic of K with conjugator IN K. Every standard parabolic of the join K splits as a product of its intersections with the displayed factors; conjugating by a K-element preserves that factorwise form. Therefore if x in the T\C factor and y in the Y\C factor satisfy xy∈R, each factor lies in R separately.

Apply this to γ=[h,k]. Homomorphicity gives α(γ) in the T\C factor and β(γ) in the Y\C factor, while the hypothesis gives their product in R. Hence α(γ),β(γ)∈P. As such commutators generate H′, both derived images lie in P. Arbitrary H, infinite derived generation, trivial images, absent root blocks, empty Y, and central/parabolic degenerate factors cause no exception.

For an injective j:H×H→A with nonabelian H, take 1≠c∈H′. Then j(c,1) lies in P and in j(H×H), but injectivity prevents it from lying in j(ΔH). This proves the asserted impossibility of exact diagonal intersection. It does not prove that a larger amalgam has no other RAAG embedding.

## Independent sharpness check

In the supplied example A=F2×F2×Z, the maps α and β commute because their noncentral coordinates occupy distinct factors. Projection to the first two free factors proves injectivity of the combined map. Its z-coordinate is ε_a(h)−ε_a(k), so the inverse image of P is exactly the equality fiber product of those two integer exponent maps. It contains the diagonal strictly, for example ([a,b],1). Neither whole factor lies in P, whereas both derived factors do. This directly falsifies the tempting stronger whole-image conclusion and confirms why shared abelian coordinates must be retained.

For H=Z, the unimodular map (x,y)↦(x−y,y) sends its diagonal to a standard coordinate subgroup. Thus the nonabelian hypothesis in the impossibility conclusion is necessary. The reviewed theorem states it correctly.

No finite search was substituted for these arguments. No complete novelty audit or full research-problem resolution is claimed.

## Fresh final delta: finite-index robustness

The final input adds the finite-index statement. It also survives adversarial reconstruction. For J of finite index in H×H, take H0 to be the intersection of the two coordinate subgroups {h:(h,1)∈J} and {h:(1,h)∈J}. These have finite index, and H0×H0≤J because J is a subgroup. If R and j(ΔH) are commensurable AS SUBGROUPS (their intersection has finite index in each), the inverse image of R∩j(ΔH) under the diagonal map is finite index in H. Intersect it with H0 to obtain K. Then ΔK maps into P and K×K≤J. The derived-image theorem puts L=j(K′×1) inside R. Since H is not virtually abelian, K is nonabelian; a nonidentity element of K′ has infinite order under the RAAG injection. Thus L is infinite while L∩j(ΔH)=1. But intersecting L with any finite-index subgroup of R must have finite index in L, contradiction.

No assumption that J itself is a direct product is made: only its finite-index product subgroup is used. The statement concerns actual subgroup commensurability, not mere abstract isomorphism or abstract commensurability. The specified restriction to parabolic-intersection models remains essential. This final delta has no outstanding substantive objection.
