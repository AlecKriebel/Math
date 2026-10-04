# Degree-one maps and Heegaard genus: partial results and barriers

Problem: UnsolvedMath 2831 / K3 Problem 3.33. Date: 2026-10-04.

**Verdict: unsolved.** This document contains complete proofs of the stated partial results, not a proof or refutation of the general conjecture. No novelty is claimed for these standard consequences and obstruction arguments. Five substantive approaches have been used; there is no full candidate to submit for verification as a solution.

## Exact target and conventions

For every continuous map of degree one between connected closed oriented 3-manifolds, does

\[
 f:M\longrightarrow N,\quad f_*[M]=[N]
 \qquad\Longrightarrow\qquad g(M)\geq g(N)
\]

hold? Here g is the minimum genus of a Heegaard splitting into two handlebodies. Connectedness is the conventional meaning in the source and is necessary to use this definition of g. Orientations may be selected on the orientable manifolds. No irreducibility, asphericity, geometric structure, or restriction on f is assumed in the target. All such restrictions below are explicit partial cases.

Write r(X) for the minimum number of generators of π₁(X). A finite cover is connected unless specified otherwise. Standard topology used below includes covering-space classification, Poincaré duality, classification of maps to K(G,1), handle decompositions, and the classical additivity of Heegaard genus under connected sum. Published external inputs are separately identified.

## 1. Fundamental-group control, and the failure of a naive counterexample

### Proposition 1.1: degree one implies a π₁ epimorphism

Let H=f_*π₁(M)≤π₁(N), and let p:N_H→N be the connected cover corresponding to H. The lifting criterion supplies \(\widetilde f:M\to N_H\) with p∘\(\widetilde f\)=f. If H has infinite index, N_H is a connected noncompact 3-manifold, so its ordinary top-dimensional homology is zero. Then f_*:H₃(M;Z)→H₃(N;Z) factors through zero, contradicting degree one. If the index is finite, d=[π₁(N):H], orient N_H by the lifted orientation. Multiplicativity of degree gives 1=d·deg(\(\widetilde f\)); hence d=1. Thus H=π₁(N).

A genus-k splitting of M gives a handle decomposition with k one-handles and therefore a presentation of π₁(M) on k generators. Consequently

\[
 g(M)\geq r(M)\geq r(N).
\]

In particular, the full target holds whenever **r(N)=g(N)**. For N=S³ it is automatic. It also holds when g(M)=0: then M=S³, π₁(N)=1, and the Poincaré theorem identifies N with S³. The latter step is an external deep theorem, not a new argument for Poincaré.

### Proposition 1.2: an epimorphism need not have a degree-one realization

For r≥0 put \(M_r=\#_r(S^1\times S^2)\), with M₀=S³. If N is a connected closed oriented aspherical 3-manifold, **every** continuous map M_r→N has degree zero.

Proof. A classifying space for F_r=π₁(M_r) is the graph R_r=∨_rS¹ (a point for r=0). Choose a classifying map c:M_r→R_r. Given f:M_r→N, the homomorphism f_*:F_r→π₁(N) is represented by a map h:R_r→N, by selecting loops for the free generators. Since N is a K(π₁(N),1), f and h∘c are homotopic as based maps after a choice of basepoints. But H₃(R_r;Z)=0. Therefore f_*[M_r]=h_*c_*[M_r]=0 and deg f=0. ∎

Moreover g(M_r)=r: connected summing r standard genus-one splittings gives the upper bound, and H₁(M_r;Z)=Z^r gives the lower bound. Thus choosing r=r(N) gives a π₁ epimorphism from a source of genus r(N), but no nonzero-degree map if N is aspherical. The hypothesis that a generator surjection can always be realized with degree one is false.

**Exact gap.** Rank is not Heegaard genus in general. Li's published examples include closed hyperbolic N with r(N)<g(N), and arbitrarily large difference [Li13]. Proposition 1.1 cannot establish the target on those N; Proposition 1.2 prevents turning those examples directly into counterexamples by taking M_r. Any such construction would need a lower-genus source carrying the correct nonzero fundamental class in H₃(Bπ₁(N);Z), not just a surjection of groups.

## 2. Poincaré transfer and homologically sharp targets

### Proposition 2.1: integral homology is split-surjective

For a degree-one map f:M→N define, using integral Poincaré duality,

\[
 t_i=PD_M\circ f^*\circ PD_N^{-1}:H_i(N;\mathbb Z)\to H_i(M;\mathbb Z).
\]

The cap-product projection formula gives, for α∈H^{3−i}(N;Z),

\[
 f_*\bigl(f^*\alpha\frown[M]\bigr)
 =\alpha\frown f_*[M]
 =\alpha\frown[N].
\]

Hence f_*t_i=id. This holds including torsion, so H_i(N;Z) is a direct summand of H_i(M;Z). The same proof over any field F gives b₁(N;F)≤b₁(M;F). A genus-k Heegaard presentation has k generators; its abelianization tensored with F has dimension at most k. Therefore

\[
 g(M)\geq b_1(N;F)\quad\text{for every field }F.
\]

If b₁(N;F)=g(N) for some F, the target is proved for every source M dominating that N.

### Explicit infinite family

Let N be a connected sum of k copies of S¹×S² and ℓ nontrivial lens spaces L(p_j,q_j), where a single prime p divides every p_j. Standard genus-one splittings, joined along disks, give g(N)≤k+ℓ. Mayer–Vietoris for the connected sum gives

\[
 H_1(N;\mathbb Z)=\mathbb Z^k\oplus\bigoplus_{j=1}^{\ell}\mathbb Z/p_j,
 \qquad b_1(N;\mathbb F_p)=k+\ell.
\]

Thus g(N)=k+ℓ, and every degree-one source has genus at least k+ℓ. This is a direct proof, not an appeal to the conjecture.

### Limitation even among elementary reducible targets

For N=L(2,1)#L(3,1), H₁(N;Z)=Z/2⊕Z/3≅Z/6. Therefore b₁(N;F)≤1 for every field F. Yet π₁(N)=C₂*C₃ is nonabelian: if x and y are the respective nontrivial standard generators, the reduced words xy and yx are distinct by the normal-form theorem for free products. The group is two-generated but not cyclic, so r(N)=2. Standard connected-sum splittings give g(N)≤2 and rank gives g(N)≥2. Thus g(N)=2, and all field-valued b₁ bounds miss one genus already here.

**Exact gap.** The split homology and cohomology-ring constraints do not produce a minimal geometric splitting. The homological method above only resolves targets where its lower bound is sharp. No assertion that an arbitrary homology isomorphism has degree one is made.

## 3. Finite covers: a valid bound with an intrinsic ceiling

### Proposition 3.1: compatible covers preserve degree one

Let q:N′→N have degree d and subgroup K≤π₁(N). Since f_* is surjective, f_*^{-1}(K) has index d in π₁(M). The corresponding connected d-sheeted cover p:M′→M supports a lift f′:M′→N′. Orient the covers by pullback. The commuting square qf′=fp and degree multiplicativity give

\[
 d\deg(f')=\deg(f)d=d,
\]

so deg(f′)=1.

### Proposition 3.2: cover lifting of a Heegaard splitting

If X′→X is connected and d-sheeted, then

\[
 g(X')\leq d(g(X)-1)+1.
\]

Proof. Let X=A∪_S B be a genus-k splitting. The maps π₁(A)→π₁(X), π₁(B)→π₁(X), and π₁(S)→π₁(X) are surjective: on either handlebody side the complementary two-handles impose relations but add no generators, and the boundary generates a handlebody's fundamental group. Therefore each of the inverse images A′, B′ and S′ is connected. A finite cover of a handlebody is a handlebody: lift a spine and its regular neighborhood. Euler characteristic gives χ(A′)=dχ(A)=d(1−k), so its genus is d(k−1)+1, and the lifted decomposition is a Heegaard splitting. Taking k=g(X) proves the inequality. For k=0 only d=1 is possible, because X=S³. ∎

Combining these propositions and Proposition 2.1 gives the genuinely valid necessary bound

\[
 g(M)\geq 1+\frac{b_1(N';F)-1}{d}.
\]

Since g(M) is an integer one may take the ceiling of the right side.

### Proposition 3.3: the entire method cannot surpass rank

Let r=r(N). If K≤π₁(N) has index d, choose an epimorphism F_r→π₁(N). Its inverse image of K is an index-d subgroup of F_r, free of rank d(r−1)+1 by Schreier's formula, and it surjects onto K. Consequently

\[
 b_1(N';F)\leq r(K)\leq d(r-1)+1,
 \quad
 1+\frac{b_1(N';F)-1}{d}\leq r(N).
\]

The same conclusion holds if b₁(N′;F) is replaced by r(N′). For r=0 the only connected cover has d=1. This is a universal obstruction, not a numerical observation about a sampled list of covers.

**Exact gap.** Cover homology can sometimes compute a useful lower bound when rank is hard to compute, but these normalized bounds can never bridge r(N)<g(N). Virtual fibering or a positive virtual Betti number alone does not remove the normalization or reverse a Heegaard cover inequality. Reopening this route requires an invariant or geometric mechanism outside these Schreier-bounded lower bounds.

## 4. Geometric pinching and the amalgamation subcase

The Haken–Waldhausen reduction, as formulated in [Li22, Introduction], represents a degree-one map as a replacement of a bounded region W by a handlebody H. The boundary has a cut system whose curves bound disjoint surfaces in W; those surfaces are not necessarily disks. The general genus inequality for this replacement is equivalent to the original conjecture. This is a reduction, not a solution.

### Proposition 4.1: minimal amalgamation makes replacement harmless

Let M=W∪_T V, where W and V are connected orientable compact 3-manifolds with their only boundary component identified as the connected genus-h surface T. Let N=H∪_T V for a genus-h handlebody H. Suppose **a minimal-genus splitting of M is an amalgamation** of relative Heegaard splittings of W and V, of genera a and b. Then g(N)≤g(M).

Proof. For W, the compression body adjacent to T is obtained from T×I by attaching one-handles, so a≥h. On the V side, write the chosen splitting as V=C∪K, where ∂₋C=T and K is a handlebody. After filling T with H, the union H∪C is H with the one-handles of C attached, hence is a handlebody of genus b. Thus N has a genus-b splitting and g(N)≤b. Handle counting in amalgamation along a connected genus-h boundary gives genus a+b−h: the h generators supplied by the common boundary are counted on both sides and are identified, or equivalently the usual relative handle construction cancels the h redundant handles. By the minimal-amalgamation assumption,

\[
 g(M)=a+b-h\geq b\geq g(N).
\]

This proves the stated conditional result. The filling bound g(N)≤g(V) follows by choosing a minimal relative splitting of V. ∎

The amalgamation genus formula is a standard construction, also used explicitly in [Li22, Remark 2.2]. The calculation is valid for any gluing satisfying the assumptions; the existence of the necessary minimal amalgamation is the substantive missing condition.

**Published special case.** Li's Theorem 1.3 proves the desired inequality when T is a torus and W is a knot exterior in an integral homology sphere, with the longitude mapped to a meridian of the replacing solid torus. This result includes cases not covered by Proposition 4.1. It is a cited theorem, not reproved here; the entire paper was not independently audited in this attempt.

**Exact gap.** A general minimal splitting need not be an amalgamation of the displayed decomposition. Untelescoping and replacing cut surfaces require compatible compression-body structures and genus control; asserting these are always available merely restates the missing argument. The general higher-genus replacement cannot be reduced to Li's torus case without a new construction. Boileau–Wang's small-manifold rigidity theorem [BW05, Theorem 1] requires both manifolds small and additional geometric hypotheses on the pinched region; it supplies no general genus comparison.

## 5. Surgery characterization and a failed componentwise induction

Gadgil's theorem [Gad07, Theorem 1.1] characterizes existence of a degree-one map M→N by obtaining M from N by surgery on a link each of whose components is an unknot in N. The components need not be unlinked or simultaneously confined to disjoint balls. This is a different constructive route to the target, but the surgery description gives no genus estimate by itself.

### Proposition 5.1: the local-link case

Suppose a surgery link L lies entirely in the interior of an embedded 3-ball B⊂N. Perform the same surgery on L in S³, obtaining Q. Surgery changes only B; the surgered B is Q with an open 3-ball removed. Gluing this to N\int(B) gives M≅N#Q. Classical Heegaard-genus additivity under connected sum now gives

\[
 g(M)=g(N)+g(Q)\geq g(N).
\]

The topological identification and the inequality are exact. Additivity is an external classical theorem; it is not derived from degree-one monotonicity. The same argument applies to links contained in several pairwise disjoint balls, by iterating connected sums.

### Why the next induction step fails

A tempting extension is to perform Gadgil's surgeries one component at a time and repeatedly apply the local unknot case. Its hypothesis does not survive preceding surgeries.

Take a Hopf link K₁∪K₂⊂S³, with linking number +1 and both framings zero. In the exterior, let μ₁,μ₂ denote meridians; the preferred longitudes have homology classes λ₁=μ₂ and λ₂=μ₁. Zero surgery on K₁ imposes μ₂=0. After filling the deleted neighborhood of K₂ by its original meridian filling, the intermediate closed manifold has H₁=Z generated by μ₁ (it is S¹×S²). The surviving knot K₂ represents λ₂=μ₁, a nonzero homology class. Hence it is not null-homotopic and cannot be an unknot in the intermediate manifold. There is no right to apply the local-unknot step again.

As an arithmetic cross-check, imposing both zero-framing surgery relations gives the presentation matrix [[0,1],[1,0]], whose determinant is −1; its cokernel is zero. This homology calculation alone is not used to identify the final manifold or determine its genus.

**Exact gap.** To prove the full target through surgery, one must control the genus change of the entire admissible surgery link, including interactions among components. The assertion that surgery on every link with individually unknotted components cannot lower Heegaard genus is equivalent, through Gadgil's theorem, to the original target. Naming it as a lemma would not prove it. No counterexample to that assertion is produced here.

## Final logical status

The verified partial statements do not cover all degree-one maps. In particular, no step addresses general targets with rank below genus and an arbitrary higher-genus pinching region or interacting surgery link. All five routes stop at explicit, unproved geometric requirements or proven limitations. The appropriate full-target status is **unsolved**, with **5/5 substantive attempts used**, not `claimed_solved` or `already_solved`.

## References

- [K3] R. İ. Baykur, R. C. Kirby, D. Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology*, AMS, 2026, Problem 3.33, p.155. Author version: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [Li22] T. Li, *Heegaard genus, degree-one maps, and amalgamation of 3-manifolds*, J. Topol. 15 (2022), 1540–1579, https://doi.org/10.1112/topo.12253 ; author preprint v2: https://arxiv.org/abs/2007.14534v2
- [Li13] T. Li, *Rank and genus of 3-manifolds*, J. Amer. Math. Soc. 26 (2013), 777–829, https://doi.org/10.1090/S0894-0347-2013-00767-5 ; https://arxiv.org/abs/1106.6302v2
- [BW05] M. Boileau, S. Wang, *Degree one maps between small 3-manifolds and Heegaard genus*, Algebr. Geom. Topol. 5 (2005), 1433–1450, https://doi.org/10.2140/agt.2005.5.1433
- [Gad07] S. Gadgil, *Degree-one maps, surgery and four-manifolds*, Bull. Lond. Math. Soc. 39 (2007), 419–424, https://doi.org/10.1112/blms/bdm019 ; https://arxiv.org/abs/0809.3102v1
