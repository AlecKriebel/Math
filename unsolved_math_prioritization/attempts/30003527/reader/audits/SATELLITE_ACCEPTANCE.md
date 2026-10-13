# Independent acceptance: the satellite-circle obstruction

Date: 13 October 2026 UTC. Target context: row 1767 / 30003527 / OWR-15575-006. This is adversarial verification within the existing substantive pass 1, not a new proof-search pass. The verdict is limited to the auxiliary topology below. It does not resolve the invariant-enlargement question.

## Verdict

**Accepted after the already-applied inward-collar correction.** There exists an embedded dyadic solenoid Σ and pairwise disjoint tame circles C_n disjoint from Σ, with C_n → Σ in Hausdorff distance, for which X = Σ ∪ ⋃_{n≥1} C_n is compact and nonmovable. Neither connectedness of a candidate neighborhood nor any requirement that the homotopy follow a flow is used.

The proof is stronger than an obstruction detected by the total homology images of the neighborhoods: a cofinal neighborhood system has surjective integral homology bonding maps, and the integral first Čech cohomology of X is free abelian of countably infinite rank. The obstruction remembers which connected component contains the image of a connected loop.

No flow with the necessary invariant-set or all-enlargements properties is constructed. In particular, the result is not a counterexample to row 1767.

## 1. Explicit geometry, including the solenoid identification

Let D be the closed complex unit disk and choose a smooth embedding h_0:S¹×D→R³ with image T_0. Inductively, after h_n is chosen, select 0 < b_n < 1/4 sufficiently small that each disk

h_n({z²}×(z/2+b_nD)), z∈S¹,

has Euclidean diameter less than 2^{-(n+1)}. Such a uniform choice exists by uniform continuity on the compact parameter domain. Define

h_{n+1}(z,w) = h_n(z²,z/2+b_nw),   T_{n+1}=h_{n+1}(S¹×D).

This is an embedding. The two possible z-values with the same square have transverse centers separated by 1 and disk radii b_n < 1/4, so their transverse disks do not meet. The local rank is full. Since |z/2+b_nw|≤1/2+b_n<1, T_{n+1}⊂int T_n. The longitudinal degree is +2. The meridional fibers of h_n have diameters tending uniformly to zero.

For x∈Σ=⋂T_n, let p_n(x) be its first coordinate in h_n. Then p_n(x)=p_{n+1}(x)². Conversely, for a compatible sequence (z_n) with z_n=z_{n+1}², the disks h_n({z_n}×D) are nested nonempty compact sets with diameters tending to zero. Their intersection is exactly one point. Thus x↦(p_n(x)) is a continuous bijection from compact Σ to the Hausdorff inverse limit of the degree-two circle maps, and hence a homeomorphism. This verifies that Σ really is the dyadic solenoid, rather than merely relying on degree-two winding to identify an arbitrary nested intersection.

Fix r=7/8. For n≥1 put

C_n = {h_n(e^{3it},r e^{it}):t∈R/(2πZ)}.

These are smooth embedded circles: equality of the second coordinates already forces equality of t modulo 2π. They lie in int T_n and outside T_{n+1}, because the latter has transverse modulus at most 1/2+b_n<3/4. Their longitudinal winding in T_n is +3. Distinct circles lie in disjoint nested shells, so are disjoint from one another and from Σ. This fixed-radius construction also avoids the former boundary-circle issue.

For every point of T_n there is a point of C_n with the same longitudinal coordinate, so their distance is bounded by the meridional fiber diameter ε_n. Nested nonempty compact sets T_n converge in Hausdorff distance to Σ: otherwise a sequence of points staying a positive distance from Σ has a convergent subsequence in T_0, and its limit belongs to every T_m, a contradiction. Consequently

d_H(C_n,Σ) ≤ max{ε_n,d_H(T_n,Σ)} → 0.

To check compactness of X, a sequence in X either has a subsequence in the union of Σ and finitely many C_n, or has circle indices tending to infinity. In the latter case, every accumulation point lies in Σ by Hausdorff convergence. Thus X is closed in compact T_1 and is compact.

## 2. The complete movability obstruction

The ambient definition under audit is: for every open O⊃X there is an open V with X⊂V⊂O such that for every open W⊃X the inclusion V→O is homotopic in O to a map with image in W. Requiring W⊂V gives an equivalent formulation.

Fix O=int T_0 and identify H₁(O;Z) with Z, choosing the orientation inherited from h_0. Then a core loop of T_j represents 2^j and C_n represents 3·2^n.

Let V be any open set with X⊂V⊂O. Since Σ⊂V and the T_n are nested compact sets with intersection Σ, some T_j⊂V; increase j if necessary so j≥1. Let α:S¹→T_j⊂V be a positively oriented core loop. Its class in H₁(O;Z) is 2^j.

Choose k>j. For 1≤n<k the compact circles C_n are pairwise disjoint and disjoint from T_k. Choose pairwise disjoint sufficiently small open tubular neighborhoods Q_n of these circles, all contained in O and disjoint from T_k. They can additionally be taken inside V if desired, since their core circles lie in V. Set

W=int T_k ∪ Q_1 ∪ ··· ∪ Q_{k-1}.

This is an open neighborhood of X. In particular C_k⊂int T_k, not on its boundary; all later circles and Σ are also in int T_k. Its components are precisely int T_k and the Q_n. Their inclusion-induced H₁ images in H₁(O;Z) are

2^k Z and 3·2^n Z,  1≤n<k.

No one of these subgroups contains 2^j. The first fails because k>j; every other one consists of integers divisible by 3.

Suppose H:V×[0,1]→O were a homotopy from the inclusion with H(V,1)⊂W. Then t↦H(α(t),1) is a connected loop lying entirely in one component of W. It is homotopic in O to α and therefore has the same integral homology class 2^j, contradicting that component's subgroup restriction.

No connectedness assumption on V occurs. Only the connectedness of S¹ is used. If the definition requires W⊂V, either choose k still larger with T_k⊂V and the Q_n⊂V as above, or replace W by W∩V. Intersecting may split components, but cannot enlarge any component's homology image. Thus

there exists O such that for every V there exists W for which no required H exists.

This is the exact negation of movability.

## 3. Independent check of the cohomology and homology claims

Choose a nested cofinal neighborhood system

N_m=int T_m ∪ ⋃_{1≤n<m} Q_{n,m},  m≥1,

where Q_{n,m} is a shrinking tubular neighborhood of C_n in int T_n\T_{n+1}; for fixed n these tubes are nested, and every Q_{n,m} is contained in the Euclidean 1/m-neighborhood of C_n. The new tube Q_{m,m+1} lies inside int T_m. Thus N_{m+1}⊂N_m. Cofinality follows from compactness of X, shrinking tube widths, and T_m→Σ.

Write s_m for the tail torus generator and c_{n,m} for the early-circle generators. Then

H₁(N_m;Z)=Z s_m ⊕ (⊕_{1≤n<m} Z c_{n,m}),

where the sum is an ordinary direct sum. The inclusion N_{m+1}→N_m induces

s_{m+1}↦2s_m,
c_{m,m+1}↦3s_m,
c_{n,m+1}↦c_{n,m}  (n<m).

This is surjective, since −2+3=1. The H₀ maps are also surjective: every component at stage m contains one or two components at stage m+1. In higher degrees the groups vanish. Thus every integral homology bonding map in this neighborhood system is surjective, including H₁; the inverse system satisfies the Mittag–Leffler condition.

Dually, H¹(N_m;Z)→H¹(N_{m+1};Z) fixes the old-circle coordinates and sends s_m* to 2s_{m+1}*+3c_{m,m+1}*. The vector (2,3) is primitive. The vectors (2,3) and (1,1) have determinant −1, so each map is a split injection with infinite-cyclic cokernel. The direct limit is therefore free abelian of countably infinite rank. By continuity over this cofinal system of ANR neighborhoods,

Čech H¹(X;Z) ≅ ⊕_{q≥0} Z,

with ⊕ denoting the direct sum of groups.

There is no contradiction with Section 2. Homology surjectivity permits a formal sum using cycles in two different components. An endpoint map of one connected loop must land in one component and cannot implement that sum. Ordinary unpointed neighborhood homology has discarded exactly this component constraint. Freeness of Čech H¹ is therefore also insufficient to infer movability here.

## 4. Primary-source scope

K. Kuperberg, *Periodicity generated by adding machines* (2013), printed pp.140–147:

- [Publisher page](https://trim.imath.kiev.ua/index.php/trim/en/article/view/310)
- [Public proceedings PDF](https://www.imath.kiev.ua/~topology/publications/proceedings.2013.6.6.pdf)

I independently read the extracted article and visually inspected printed p.145. Section 4 gives ordinary neighborhood-homotopy movability. The p.145 paragraph first introduces a nonsingular ambient flow, then asserts movability for a solenoid union pairwise disjoint circles disjoint from it and converging in Hausdorff distance. It states no longitudinal-degree condition and does not expressly require these sets to be invariant. Subsequent Questions 1–3 expressly discuss invariance and invariant approximating circles.

The construction refutes this unrestricted topological implication. Merely supplying an unrelated nonsingular ambient flow, such as translation on R³, cannot alter the topology. An intended interpretation requiring simultaneous invariance is a materially stronger hypothesis and is not refuted here. The correct source-scoped verdict is an auxiliary topological counterexample to the unqualified implication, not a claim that the paper's adding-machine theorem or invariant-enlargement questions have been resolved.

The inspected public PDF has 16,393,363 bytes and SHA-256 faa28bfeca574bd2a37340858a09011ff25ac717ecdc7d80b5eebc93363c2499. The source body and page images are not part of this authored report.

## 5. Scope exclusions and required next theorem

This audit does not independently certify the separate general theorem about first Čech cohomology of isolated invariant sets; it verifies that the satellite example is consistent with that theorem's free-cohomology conclusion. It also makes no novelty claim for the satellite example.

Even a flow preserving Σ and the C_n would not by itself give a negative answer to row 1767. That answer requires a concrete full flow, compact invariant A, and prescribed neighborhood U, and must exclude every compact invariant movable B with A⊆B⊆U, including other supersets and B=A. None of those missing realization and all-enlargements requirements is supplied by this topological acceptance.
