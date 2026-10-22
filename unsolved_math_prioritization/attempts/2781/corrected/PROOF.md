# KP-2.33: surface actions, scoped partial results

**Disposition: unsolved after five substantive approaches.** No finitely generated torsion-free group is proved here to lack every faithful homeomorphism action on a prescribed closed surface. No universal embedding theorem for all such groups is proved either. The results below are elementary constructions, consequences of credited literature, and exact boundaries on attempted obstructions. No novelty claim is made. This is AI-assisted, unrefereed work. An independent audit accepts the scoped partial results after the Section 5 wording correction recorded in CORRECTIONS.md; this is not formal verification.

## 0. Exact scope

Fix a nonempty closed topological surface S. The target asks for a finitely generated torsion-free abstract group G with no injective homomorphism G → Homeo(S). In particular the action need not preserve a measure, be differentiable, have any freeness or properness, or be locally moving. The source does not impose orientability. Our positive disk-supported constructions apply on every surface, including nonorientable ones. The obstruction is allowed to depend on S.

The primary source is Baykur–Kirby–Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology*, Problem 2.33, printed pp. 112–113, scribed by T. Koberda. The complete statement, all five remarks, and the transition to Problem 2.34 were inspected. The disk-boundary version and the closed-surface problem are related but not asserted equivalent. The current inspected K3 source presents the problem as open. That dated source assessment and this bounded search do not certify worldwide open status.

Source: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

## 1. Orderability route: an explicit universal disk construction for left-orderable groups

**Proposition 1.** Every countable left-orderable group embeds in Homeo(D², ∂D²), and hence in Homeo(S) for every nonempty surface S.

Here Homeo(D², ∂D²) fixes the boundary pointwise. We give the construction rather than infer a two-dimensional action from one-dimensional terminology.

Let < be a left-invariant total order on G. Order the countable set G × Q lexicographically. It is dense without endpoints: within one G-fiber use density of Q; between different fibers insert a larger rational in the lower fiber. Every countable dense total order without endpoints is order-isomorphic to Q. One can obtain that isomorphism by alternating finite order-preserving extensions along enumerations of the two sets: each new element has a nonempty rational interval in which to be placed. Left multiplication on the first coordinate is a faithful order-preserving action of G on G × Q, so after conjugacy it acts on Q.

An increasing bijection h of Q extends uniquely to an increasing homeomorphism of R by

    h̄(x) = sup { h(q) : q ∈ Q, q < x }.

The cut has a finite supremum because there are rational upper and lower bounds around x. The extension is strictly increasing, continuous and onto: a jump or missing interval would contradict density and surjectivity on Q. The extension of h⁻¹ is its inverse. Uniqueness on the dense subset Q proves that extension respects composition. Thus G embeds in Homeo₊(R). Conjugate R to (−1,1) and fix both endpoints to obtain G ≤ Homeo₊([−1,1]).

Use the closed diamond

    D = { (u,t) : |t| ≤ 1, |u| ≤ 1−|t| }.

For f ∈ Homeo₊([−1,1]), put r(t)=1−|t| and define

    E(f)(u,t) = ( r(t) f(u/r(t)), t )       when |t|<1,
    E(f)(0,±1) = (0,±1).

This is continuous at the two tips since the first coordinate has absolute value at most r(t), regardless of f. Elsewhere continuity follows by composition. Every boundary point is fixed because f(−1)=−1 and f(1)=1. The inverse is E(f⁻¹); composition is E(f)E(g)=E(fg); and the equatorial restriction t=0 is f, so E is faithful. The diamond is a topological closed disk.

Choose a closed disk in a coordinate chart of S. Conjugate E into that disk and extend by the identity on its complement. The definitions agree on the boundary, giving a homeomorphism and a faithful homomorphism. This also gives a common fixed nonempty open set after taking the chosen disk small enough.

**Consequence.** Left-orderable candidates cannot answer KP-2.33. A common fixed point, indeed a common fixed open set, is compatible with faithfulness. This is a standard dynamical-realization consequence with an explicit extension formula, not a new universal theorem for torsion-free groups. Torsion-free does not imply left-orderable.

## 2. Non-orderability route: why its converse fails in the exact category

We tried to reverse Proposition 1 and use failure of left-orderability as a surface-action obstruction. Hyde's theorem rules out that strategy even among finitely generated torsion-free groups.

**Proposition 2.** There exists a finitely generated torsion-free non-left-orderable group that embeds in Homeo(S) for every nonempty surface S.

Hyde explicitly constructs a finitely generated non-left-orderable subgroup H of Homeo(D², ∂D²). This is the imported non-orderability theorem; the present report does not claim a new construction or an independent proof of its six-generator order contradiction. By Constantin–Kolev, Proposition 3.2, a finite-order disk homeomorphism fixing its boundary pointwise is the identity. Hence the whole disk-boundary group, and H in particular, is torsion-free. Extend H by the identity outside a disk in S as in Proposition 1.

References:
- J. Hyde, *The group of boundary fixing homeomorphisms of the disc is not left-orderable*, Ann. of Math. 190 (2019), 657–661, Theorem 3.2 in the inspected author version. https://doi.org/10.4007/annals.2019.190.2.5 ; https://arxiv.org/abs/1810.12851
- A. Constantin and B. Kolev, *The theorem of Kerékjártó on periodic homeomorphisms of the disc and the sphere*, Proposition 3.2. https://arxiv.org/abs/math/0303256

The analytic point behind Hyde's planar realization can also be checked independently. Let B be the group of plane homeomorphisms h with sup_x ||h(x)−x|| finite. Composition stays in B by adding displacement bounds, and the inverse has the same bound. Under radial compactification c(x)=x/(1+||x||), each h extends to the identity on the boundary circle. Indeed, if ||h(x)−x||≤C and ||x||→∞, then ||h(x)||→∞ and their unit directions differ by at most 2C/||x||. The radial norms of both c(x) and c(h(x)) tend to one. The same argument for h⁻¹ verifies a homeomorphism. Thus B embeds in Homeo(D², ∂D²).

This applies to the bounded-displacement generators in Hyde's realization. It does not apply to every plane homeomorphism. For example the polar twist (r,θ) ↦ (r,θ+r) has no continuous extension to the radial boundary: sequences of radii 2πn and 2πn+π approaching the same radial endpoint have image directions differing by π. A plane action always extends to the *one-point* compactification S², but that different construction does not give a disk-boundary action.

## 3. Higher-rank candidate: a rigorous smooth obstruction with the C⁰ gap retained

Let

    Γ = ker( SL(4,Z) → SL(4,F₃) ).

**Proposition 3.** Γ is infinite, finitely generated and torsion-free. Every C² action of Γ on every closed surface has finite image, so none is faithful. This does not establish the corresponding C⁰ assertion.

The elementary integer row operations show SL(4,Z) is generated by the finite collection I±Eᵢⱼ, i≠j: the Euclidean algorithm reduces a primitive first column, and induction reduces the remaining block; the determinant-one signed exchanges used in the algorithm are products of elementary matrices. The reduction map has finite image, so Γ has finite index. Schreier rewriting then gives finite generation of Γ. The matrices I+3kE₁₂, k∈Z, are distinct elements of Γ, proving infinitude.

Here is a self-contained torsion argument. A nontrivial finite-order element would have a power A of prime order p, still in Γ. Write A=I+3ᵏB, where k≥1 is maximal and B is an integer matrix not zero modulo 3. Expanding Aᵖ=I and dividing by 3ᵏ, reduction modulo 3 gives pB=0. Thus p=3. For p=3 the expansion, divided instead by 3ᵏ⁺¹, gives

    B + 3ᵏB² + 3²ᵏ⁻¹B³ = 0.

Both latter coefficients are divisible by 3, since k≥1. Again B=0 modulo 3, a contradiction.

Brown–Fisher–Hurtado's *Zimmer's conjecture for actions of SL(m,Z)*, Theorem A, covers finite-index subgroups, C² actions, closed manifolds, and dimension at most m−2. Take m=4 and dim S=2. It gives finite image without a volume-preservation hypothesis. Infinitude of Γ prevents faithfulness. This is a direct application of an existing theorem, not a proof of that deep theorem.

https://arxiv.org/abs/1710.02735 ; DOI 10.1007/s00222-020-00962-x

This arithmetic, nonuniform case uses the SL(m,Z) paper. The different BFH paper cited in K3 is not silently treated as though its cocompact-lattice statement were the same theorem. Brown–Damjanović–Zhang also establish C¹ results with their own lattice hypotheses (Theorem 1 and Corollary A). None is a theorem about all homeomorphisms. https://arxiv.org/abs/1801.04009 ; https://doi.org/10.1112/S0010437X22007278

A simultaneous conjugacy of an arbitrary faithful Γ-action into C² would finish this candidate, but no such conjugacy is proved. Approximating generators individually would not preserve all group relations or guarantee a faithful action.

There is a further concrete reason the known torsion-based topological result cannot be substituted. Ye's Theorem 1.2 treats the full SAut(Fₙ), and hence SL(n,Z), on connected manifolds with the specified nonzero Euler-characteristic residue (modulo 3, or modulo 6 in the orientable case). Its proof depends on torsion and explicitly warns against passage to arbitrary finite-index subgroups.

https://arxiv.org/abs/1707.06788 ; https://doi.org/10.2140/agt.2018.18.1195

For this Γ, reduction is onto since elementary matrices generate SL(4,F₃). Its index is

    |SL(4,F₃)| = ((81−1)(81−3)(81−9)(81−27))/2 = 12,130,560.

Inducing a Γ-action up to SL(4,Z) gives that many disjoint copies of S. This induced space is disconnected, and its Euler characteristic is 12,130,560 χ(S), divisible by 6. Thus this induction does not meet Ye's connectedness or nonzero-residue hypotheses, even if S itself does. No failure of Ye's theorem is claimed.

## 4. Free-planar-action route: an excluded candidate actually acts on every surface

The distinction between a faithful action and a free action can be made at the level of a specific group in the cited literature. Put

    L = <a,b,c | aba⁻¹=b⁻¹, bcb⁻¹=c⁻¹>.

**Proposition 4.** L is finitely generated and torsion-free and has a faithful disk-boundary action, hence a faithful action on every S. Nevertheless it has no free orientation-preserving plane action.

The last conclusion is Le Roux's Corollary 2.1, where L is the group G₂. The paper also states that G₂ is left-orderable. The following group decomposition gives a separate elementary justification of that positive side, avoiding any reliance on interpreting a printed normal-form formula.

Let F be the free group with basis {cᵢ : i∈Z}. Let J be its automorphism cᵢ ↦ cᵢ⁻¹, and let T be the shift cᵢ ↦ cᵢ₊₁. The generator-inversion map is an automorphism defined on the free basis; it does not reverse word order. J²=1 and JT=TJ. Form K=F ⋊⟨b⟩ with b acting by J. The assignments

    b ↦ b⁻¹,       cᵢ ↦ cᵢ₊₁

define an automorphism θ of K: the relation b cᵢ b⁻¹=cᵢ⁻¹ is taken to b⁻¹ cᵢ₊₁ b=cᵢ₊₁⁻¹, which holds since J⁻¹=J. Its inverse shifts the subscripts down and sends b to b⁻¹. Form P=K ⋊θ⟨a⟩. In P, the elements a,b,c₀ satisfy the presentation of L, and generate P because cᵢ=aⁱc₀a⁻ⁱ. Conversely in L the elements aⁱca⁻ⁱ together with b satisfy all the relations defining K and θ. The two maps are inverse on a,b,c₀, so L≅P.

Free groups are left-orderable. A group extension with left-orderable kernel and quotient is left-orderable: declare an element positive if its quotient is positive, or if its quotient is trivial and it is positive in the kernel. This cone is closed under multiplication and partitions the nonidentity elements into positive elements and their inverses. No conjugation invariance is needed for a left-order. Apply this to F ⋊ Z and then to K ⋊ Z. Thus L is left-orderable, in particular torsion-free, and Proposition 1 gives the asserted faithful actions.

Le Roux's free-action obstruction cannot eliminate this candidate for KP-2.33; its conclusion and these faithful actions coexist. A fixed point of a nonidentity element is allowed in KP-2.33.

F. Le Roux, *Free planar actions of the Klein bottle group*, Geom. Topol. 15 (2011), 1545–1567, Theorem 1, Corollary 2.1 and the following orderability discussion. https://doi.org/10.2140/gt.2011.15.1545 ; https://arxiv.org/abs/1101.3137

## 5. Local-rigidity route: an algebraic consequence and an exact missing hypothesis

A surface action is locally moving if each nonempty open U admits a nonidentity induced homeomorphism whose support is contained in U. Among faithful actions, local moving is an additional condition. Local moving and the existence of a dense global orbit are incomparable; neither follows from faithfulness alone.

**Proposition 5.** If a torsion-free group G acts faithfully and locally moving on a surface, then it contains Zⁿ for every positive integer n.

Choose n pairwise disjoint nonempty open disks Uᵢ. Local moving supplies nonidentity gᵢ supported in Uᵢ. These supports are disjoint, so the gᵢ commute. Each gᵢ has infinite order: faithfulness and torsion-freeness imply that no nonzero power is the identity homeomorphism. If ∏gᵢᵐⁱ=1, restrict to Uⱼ; all other factors are identity there, so gⱼᵐʲ is identity on Uⱼ, hence on the entire surface because its support lies in Uⱼ. Therefore mⱼ=0. This proves the embedding Zⁿ → G.

This proves a real obstruction in the strengthened category. It also proves why that category cannot simply replace the original one. Z embeds in Homeo(D², ∂D²) by Proposition 1 and consequently acts faithfully on every S. Z contains no Z², so it has no faithful locally moving action on any surface, even though it has faithful actions on all of them.

Koberda–Lodha's 2026 paper *Generic torsion-free groups and Rubin actions* gives a different and much deeper obstruction: a generic countable torsion-free group has no nontrivial locally moving image as specified by its Theorem 1.2. The finite-generation requirement and the removal of local moving are both essential unresolved steps when trying to use that theorem here. No inheritance to a finitely generated subgroup is inferred. Their initial discussion explicitly retains the arbitrary-homeomorphism obstruction problem.

https://doi.org/10.1016/j.apal.2025.103704 ; https://arxiv.org/abs/2503.11772

Likewise the dimension/action rigidity in Koberda–de la Nuez González's *Locally approximating groups of homeomorphisms of manifolds* requires locally approximating actions. A hypothetical faithful embedding is not automatically locally approximating. https://arxiv.org/abs/2410.16108

## 6. What remains

The five routes establish neither a witness G nor a universal embedding theorem for arbitrary finitely generated torsion-free G. In particular:

- Γ(3) ≤ SL(4,Z) is a rigorously verified candidate with an existing C² obstruction; an obstruction to its arbitrary C⁰ actions is absent.
- Left-orderability supplies actions, while non-left-orderability supplies no general obstruction, by Hyde's credited example.
- Free planar actions and locally moving surface actions have genuine obstructions that do not obstruct all faithful actions.
- Nothing here identifies the homeomorphism actions of all finitely generated torsion-free groups.

Stop at five approaches. **The target remains unsolved by this investigation.**
