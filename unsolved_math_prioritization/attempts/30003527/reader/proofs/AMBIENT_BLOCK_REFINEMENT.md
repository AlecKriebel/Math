# Ambient block refinements without a finite-rank assumption

Problem 30003527 / OWR-15575-006, queue row 1767. Authored 13 October 2026 in shared substantive pass 4. These are partial restrictions and block refinements, not a solution of the invariant-enlargement question. No novelty claim is made. Independent audit is required before these newly authored deductions are treated as accepted.

## Results

1. Every isolated invariant compactum in R³ has finitely many complementary components. Thus its integral second Čech cohomology has finite rank.
2. Isolated invariant compacta with infinitely generated first Čech cohomology do exist: a stationary planar Hawaiian earring is an elementary example. It is movable.
3. If an isolated invariant compactum K has finitely many connected components, it has arbitrarily small tame manifold isolating blocks B such that Ȟ⁰(B;Z)→Ȟ⁰(K;Z) is an isomorphism and Ȟ¹(B;Z)→Ȟ¹(K;Z) is a split injection. No finiteness of Ȟ¹(K;Z) is assumed. The proof uses actual surface cuts lifted along flow tubes.

Result 3 does not supply the neighborhood homotopies required for movability. In particular it does not assert a splitting on fundamental groups, a homotopy retraction, or a finite-shape model of K.

## 1. Elementary complementary-component bound

Let N be a compact isolating neighborhood, so K=Inv(N)⊂int N. Choose δ>0 with the closed δ-neighborhood of K contained in int N. Fix a closed ball of radius R containing K in its interior. There is exactly one unbounded component of R³\K, because the exterior of this ball is connected; all other components lie inside the ball.

Each component Ω of R³\K is invariant. Indeed, for x∈Ω the path t↦φ(t,x) never meets K, by invariance of K and invertibility of the flow. A continuous path cannot change its component of the complement.

If Ω is bounded and Ω⊂N, every point of Ω has its full orbit in N. This contradicts Inv(N)=K. Hence Ω contains a point x outside N. Such an x has dist(x,K)>δ. Since ∂Ω is nonempty and contained in K, Ω also contains points arbitrarily close to K. The open connected set Ω is path connected, so the distance function takes the value δ on a path inside Ω. Choose a point yΩ with dist(yΩ,K)=δ.

The open ball of radius δ/2 about yΩ is disjoint from K and belongs to Ω. Balls corresponding to different components are disjoint. They all lie in the ball of radius R+δ/2. Volume comparison therefore gives

number of bounded complementary components ≤ ((R+δ/2)/(δ/2))³.

Only finiteness matters. Alexander duality in S³ now gives Ȟ²(K;Z)≅H̃₀(S³\K;Z), a finite-rank free abelian group. This argument does not use block existence, differentiability, connectedness, or finite cohomology. The same packing argument works for isolated compact invariant sets in Rⁿ, n≥2, with the corresponding top-degree cohomology conclusion.

This also clarifies why an infinite shrinking collection of stationary 2-spheres cannot itself be isolated: sufficiently small enclosed complementary regions would be invariant inside every isolating neighborhood.

## 2. Infinite first-cohomology rank really is realized

Let C be any nonempty compact subset of the horizontal plane z=0, and define the bounded globally Lipschitz vector field

F_C(x,y,z)=min(1,dist((x,y,z),C)) e₃.

It generates a continuous full flow. Horizontal coordinates are constant. Each vertical fiber of C is either empty or the singleton {0}. Thus every nonstationary full orbit is either a complete vertical line or one of its two unbounded half-lines separated by a point of C. To justify the orbit description: on a complementary interval of a fiber the scalar velocity is strictly positive; the orbit cannot stop at an interior point, and uniqueness prevents finite-time arrival at a zero of the field. Boundedness of the vector field prevents finite-time escape to infinity.

Consequently no nonstationary full orbit is bounded. For every compact neighborhood N of C one has Inv(N)=C. In particular C is isolated for this flow.

For a specific connected example, let C be the Hawaiian earring consisting of circles in z=0 of radii 1/n, centered at (1/n,0,0), n≥1. Its finite-bouquet expansion collapses all circles after the first m to their common point. The inverse limit of these bouquets with the extra-circle collapse maps is C: a compatible sequence either remains the common point at every stage or specifies a point of exactly one retained circle. The compact-to-Hausdorff identification is a homeomorphism. This is a polyhedral shape expansion. Therefore

Ȟ¹(C;Z)=colim(Z^m → Z^(m+1))=⊕_(n≥1) Z,

with standard coordinate inclusions. The bouquet bonding maps have sections given by inclusion of the earlier circles. Their inverse-system movability criterion is therefore immediate: for each stage m and any later stage k use the section from the m-bouquet to the k-bouquet. Thus C is movable. Equivalently, one can use the classical movability theorem for planar compacta.

This corrects only the earlier lack of a concrete infinite-rank realization in the present investigation. It does not contradict the proven freeness of Ȟ¹ for isolated compacta, nor does it give an infinite-rank nonmovable isolated example. A stationary planar Cantor set similarly realizes infinitely generated Ȟ⁰.

## 3. Primary geometric inputs

We use J. J. Sánchez-Gabites, *Using an invariant knot of a flow to find additional invariant structure*, arXiv:2403.18805v1, https://arxiv.org/html/2403.18805v1 . The inputs are: arbitrarily small tame manifold blocks (§5.4); Ȟ^q(N,K)≅Ȟ^q(E,L), for entry surface E=Nⁱ and trace L=n⁺ (Proposition 5(iii)); realization of a disk removal or proper strip cut in E\L by shaving a flow tube (Propositions 11 and 12); and the exact sequence for those surface cuts (Proposition 30). These statements and the relevant proofs were inspected directly.

The author’s finite-type argument first removes every internal complementary surface component and then cuts relative 1-cycles. The modified argument below interleaves only the disk removals needed by the finitely many 1-cycle cuts. It does not require the number of complementary surface regions to be finite.

## 4. A finite-cut surface lemma

Let S be a compact orientable surface, and L⊂Int S compact. Assume Ȟ⁰(S,L;F₂)=0 and r=dim Ȟ¹(S,L;F₂)<∞. Then a finite succession of the following operations, supported away from L, gives a compact surface P containing L in its interior:

- remove an interior disk;
- cut along a thin strip around a properly embedded arc.

The resulting pair satisfies Ȟ⁰(P,L;F₂)=Ȟ¹(P,L;F₂)=0. At most r strip cuts and r disk removals are needed.

Proof. Surface Alexander–Lefschetz duality identifies Ȟ^q(S,L;F₂) with H_(2−q)(S\L,∂S;F₂). Write M=S\L. The hypotheses say H₂(M,∂S)=0 and dim H₁(M,∂S)=r.

If r>0, a nonzero relative 1-class has a representative that is a finite disjoint union of embedded polygonal circles and properly embedded arcs. At least one member γ has nonzero class.

If γ is an arc, cut directly along a sufficiently thin strip about it. If γ is a circle in a component of M that meets ∂S, choose a simple path from γ to ∂S, disjoint from γ except at its initial endpoint. A thin band along this path changes γ into a properly embedded arc. Over F₂, the band changes the cycle only by a relative boundary; the resulting arc still has the same nonzero relative class. The path and band can be chosen compact and disjoint from L.

If γ instead lies in a component of M not meeting ∂S, first remove a small closed disk D in that component and disjoint from γ. The exact sequence for removing the disk contains

0 → H₁(M,∂S) → H₁(M\Int D,∂S∪∂D) → H₀(D) → H₀(M,∂S).

The final arrow is injective: its generator is the nonzero basis element of the chosen component, which has not met ∂S. Thus the displayed map between relative H₁ groups is an isomorphism. Relative H₂ is also unchanged. The component containing γ now meets a boundary circle, so the preceding band construction applies.

For a proper-arc strip T, the exact sequence for removal has

0 → H₂(M,∂S) → H₂(M',∂S') → H₁(T,T∩∂S) → H₁(M,∂S) → H₁(M',∂S') → 0.

Here H₁(T,T∩∂S)=F₂ maps to the nonzero class of γ. Hence it is injective. Relative H₂ stays zero and the relative H₁ dimension drops by exactly one. This uses no finite-dimensional assumption on H₀(M,∂S), which may have infinite rank.

Repeat r times. Each iteration uses one strip and at most one disk. Duality gives the conclusion. ∎

The band argument can also be described chain-theoretically: join the circle to the boundary by a thin corridor; travel along one side of the corridor, once around the cut-open circle, and back along the other side. The two corridor sides cancel modulo the corridor boundary, while the two endpoints lie on ∂S. This prevents the mistaken inference that a closed curve itself was already a relative arc.

## 5. Lift the finite cuts to actual isolating blocks

Suppose K has c<∞ connected components. In any prescribed neighborhood choose a tame compact manifold isolating block N, discarding components whose invariant part is empty. Put E=Nⁱ and L=n⁺.

Each component of N meets K, so Ȟ⁰(N,K;F₂)=0. Also Ȟ¹(N,K;F₂) is finite dimensional, from the exact segment

H⁰(N;F₂) → Ȟ⁰(K;F₂) → Ȟ¹(N,K;F₂) → H¹(N;F₂).

Indeed Ȟ⁰(K;F₂)=F₂^c and N has finite type. The block relative-cohomology isomorphism transfers both properties to (E,L). Apply the surface lemma, lifting every disk or strip operation by the actual flow-tube construction. The resulting genuine block B has entry pair homeomorphic to (P,L), and still isolates the same K. The invariant set is untouched since every removed tube is disjoint from it. Tame manifold status and the entry/exit requirements follow at each step from the cited shaving propositions.

Consequently Ȟ⁰(B,K;F₂)=Ȟ¹(B,K;F₂)=0.

For the integral conclusion, first Ȟ⁰(P,L;Z)=0. Every component of P meets L, as witnessed by the mod-2 vanishing. The mod-2 long exact sequence also says H⁰(P;F₂)→Ȟ⁰(L;F₂) is surjective. Therefore L has finitely many components. The integral long exact sequence then makes Ȟ¹(P,L;Z) finitely generated. It is torsion-free: after collapsing L this is a degree-one Čech cohomology group of a compact metric quotient, with the usual disjoint-basepoint convention if L is empty. Degree-one integral Čech cohomology is torsion-free by a finite-polyhedral expansion and the universal coefficient theorem. The coefficient exact sequence shows Ȟ¹(P,L;Z)/2Ȟ¹(P,L;Z) injects into Ȟ¹(P,L;F₂)=0. A finitely generated torsion-free group with zero reduction modulo 2 is zero. Thus Ȟ¹(P,L;Z)=0, and the same is true for (B,K).

The exact sequence of (B,K) now yields an isomorphism H⁰(B;Z)→Ȟ⁰(K;Z) and an injection H¹(B;Z)→Ȟ¹(K;Z). Moreover

Ȟ¹(K;Z)/image H¹(B;Z) ↪ Ȟ²(B,K;Z) ≅ Ȟ²(P,L;Z).

Integral oriented-surface duality identifies the last group with H₀(P\L,∂P;Z), which is free on those complementary components not meeting ∂P. Its subgroups are free. Hence the quotient above is free, and the injection H¹(B;Z)→Ȟ¹(K;Z) splits as a homomorphism of abelian groups. No canonical splitting is asserted.

Because the starting N could lie in any prescribed neighborhood, such B are arbitrarily small. Notice that the finite number of components of K, rather than finite rank of Ȟ¹(K), is what made the cut count finite. ∎

## 6. Where the geometric argument still stops

When Ȟ¹(K) has infinite rank, the remaining group Ȟ²(P,L), and the number of disk regions of P\L not meeting ∂P, can remain infinite. Eliminating finitely many relative 1-cycles does not eliminate these holes. An infinite collection of drillings needs a cofinal, ambiently controlled homotopy argument; the finite-cut proof supplies none.

In particular, a split injection in first cohomology does not give a splitting on fundamental groups. The accepted rank-two inverse-graph example from shared pass 3 already has identity maps on first homology while its nonabelian subgroup images decrease strictly. It is not an isolated-flow realization, but it explains exactly why abelian splitting cannot be promoted to the missing homotopy factorization.

A sufficient missing statement would be this: for a cofinal block expansion {B_i} of K, for each i there exists j≥i such that for every k≥j there is a continuous r:B_j→B_k with inclusion B_j→B_i homotopic in B_i to inclusion B_k→B_i composed with r. That is the actual movability factorization. Neither the finite surface-cut lemma nor the finite-shape quotient D/L establishes it.

Even proving this for every isolated K would not finish the original target: an arbitrary invariant A need not have an isolated invariant enlargement inside its prescribed U. The identity flow gives the elementary warning. No general such enlargement or counterexample excluding all permissible B is established here.
