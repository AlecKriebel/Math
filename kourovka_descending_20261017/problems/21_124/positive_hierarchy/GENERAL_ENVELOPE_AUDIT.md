# Finite-rank envelopes: one exact positive case and the general gap

UTC: 2026-10-24. Supporting deductions only; full21.124 discovery estimate remains **3%**. No full virtual-specialness theorem is claimed.

## 1. An invariant finite core gives a genuine reduction

Suppose a finitely generated free-by-Z group G=𝔽⋊_ψ< t > comes with a free product decomposition

    𝔽=A * (*_{i∈Z} C_i),    C_i=ψ^i(C_0),

where A,C_0 have finite rank, and assume additionally that **ψ(A)=A**. Then

    G ≅ (A⋊_(ψ|A) Z) * C_0.

Proof: use a free basis of A together with bases of all C_i. The mapping-torus relations for the C_i allow elimination of every C_i with i≠0, leaving only the defining relations of A⋊Z and no relation on the C_0 generators. The inverse map sends the remaining generators to the stated subgroups, so this is an isomorphism, not merely an epimorphism. Equivalently, the kernel of the natural height on that free product is exactly A * (*_{i∈Z}t^i C_0 t^-i), with its shift automorphism.

Let H=A⋊Z. Then **G virtually embeds in a finite RAAG if and only if H does**. One direction follows by restriction to H. For the other, take a finite-index normal H_0≤H embedding in a RAAG, and map H*C_0 to H/H_0 by killing C_0. Its kernel has finite index and, by the free-product subgroup theorem, is a free product of finitely many conjugates of H_0 and a finite-rank free group. Embed those factors in RAAGs; their free product is the RAAG on the disjoint union of the corresponding finite defining graphs. Thus the kernel embeds in a finite RAAG.

There is a necessary geometric step in making this an exact reduction of21.124, rather than only an algebraic equivalence. If G is CAT(0), then H is CAT(0) **because it is a free factor in this splitting**: apply Hruska–Ruane1705.00784v3, Theorem1.3 (Convex Splitting Theorem), to G=H*C_0. Its edge group is trivial, and the trivial group stabilizes a singleton closed convex subspace and acts cocompactly on it. Hence the theorem makes H a convex vertex group, acting geometrically on a closed convex CAT(0) subspace. The theorem has no isolated-flats or one-endedness hypothesis; those occur in other results of the same paper. If C_0=1, H=G and the conclusion is immediate. Conversely, if H is CAT(0), G is CAT(0), since free products of CAT(0) groups admit the usual geometric tree-of-spaces action.

Consequently, under this **additional invariant-core hypothesis**, the broader possible-infinite-fiber version of21.124 reduces exactly to a finite-fiber CAT(0) problem. This uses the cited convex-splitting theorem and no compact-special convention. It does not silently infer CAT(0) from arbitrary subgroup inclusion. We have not asserted that an arbitrary G in Linton's decomposition has ψ(A)=A; Linton's theorem supplies the free product decomposition without this invariant-core hypothesis.

## 2. A CAT(0)-preserving finite-rank envelope in this subclass

Retain ψ(A)=A. If the original G is CAT(0), Section1 now proves that H=A⋊Z is CAT(0). Let P=D⋊_φ Z be the **chosen retract cover** in Linton's finite-rank construction: P is hyperbolic compact special, it contains the quasiconvex free subgroup S=<C_0,t> realizing the shift orbit of C_0, and an actual retraction P→S has already been chosen. Compact specialness and quasiconvexity alone produce a virtual retract, so passing to that particular finite cover is part of this setup.

Finite-cover bookkeeping is as follows. If the initial special cover Q contains a positive power u^m of the original stable letter, replace Q by Q∩η^-1(mZ). This is a finite-rank-free-by-Z group with the height-one stable letter u^m after renormalizing height. Rename u^m as t. Choose C_0 inside its free fiber as in the construction, and pass to the retract cover containing S; that cover still contains t and is (P∩D_initial)⋊<t>, so its free fiber has finite rank. The later retraction need not preserve height. Then

    E=H *_{<t>} P

is finite-rank-free-by-Z: its free fiber is A*D, with automorphism (ψ|A)*φ. It is CAT(0) by the standard gluing of geometric CAT(0) actions along axes of the common infinite cyclic subgroup. Rescale one metric to equalize the one marked translation length. The graph of spaces is compact, and its universal tree of spaces has closed convex line gluings. The subgroup <H,C_0> is H*C_0≅G by the amalgam normal form, and the retraction P→<C_0,t> induces a retraction E→G. Thus this is an explicit CAT(0)-preserving form of the finite-rank envelope **in the invariant-core subclass**.

This is a reduction/control lemma, not a new solution: deciding virtual specialness of all finite-rank CAT(0) H is the original unresolved task.

## 3. Why the unrestricted envelope does not settle the target

Without ψ(A)=A, the finite-rank construction has the algebraic form

    E ≅ G *_{S} P,       S=<C_0,t>≅C_0*Z,

with P hyperbolic compact special and S a quasiconvex retract of P after the chosen finite cover. On the G side the subgroup S need not have a demonstrated convex cocompact geometric model. A free subgroup, a group-theoretic retraction elsewhere, or an undistorted orbit is not an isometric convex attachment. Even if such a model were available, its marked metric must agree with an S-invariant convex model in P before the CAT(0) gluing theorem applies. Free-group gluing has many marked translation lengths, unlike a cyclic edge, whose one length can be matched by rescaling.

A minimal metric counterexample to automatic matching is an abstract F(a,b) acting on two marked rose universal trees with edge lengths(1,1) and(1,2). No rescaling makes both marked translation lengths agree, so there is no equivariant isometry between these prescribed convex models. This does not exclude a redesigned envelope; it identifies the missing geometric construction.

Nor can S automatically be declared Morse. For the eligible CAT(0) example G=<a,t |[a,t]=1>*<c>≅Z²*Z, the infinite free kernel for the height χ(t)=1,χ(a)=χ(c)=0 is

    <a> * (*_{i∈Z}<t^i c t^-i>).

Here S=<c,t> is free and convex in the standard Salvetti model. Nevertheless it is not Morse: in the Z² factor the path a^n t^n a^-n joins1 to t^n, is a(3,0)-quasigeodesic for the standard word metric, and reaches distance n from S. Thus this candidate stable-subgroup shortcut fails even in a RAAG example.

## 4. An explicit invalid projection shortcut

One tempting proof that a Morse subset in an arbitrary CAT(0) space has a nearby convex hull uses convexity of inverse images of intervals under nearest-point projection to a segment. That intermediate assertion is false.

Let T be a four-pronged unit tree with center o and branches named A,B,C,D, and let X=T×R with the Euclidean product metric. Let p(s), -1≤s≤1, run at unit speed from the A endpoint through o to the B endpoint. Set I(s)=(p(s),s). Let x=(C_endpoint,1) and x'=(D_endpoint,1). Both project to I(0). Indeed, for s≥0 their squared distance to I(s) is(1+s)²+(1-s)²=2+2s²; for s≤0 it is2(1-s)². Their midpoint is m=(o,1), whose squared distance to I(s) is s²+(1-s)², minimized at s=1/2. Therefore π_I^-1(I([-1,0])) is not convex. This invalidates that particular proof step; it does not establish that the final Morse-convex-hull assertion, or CAT(0) inheritance for peripherals, is false in every setting.

## 5. Relative hierarchy route: exact unresolved input

The superlinear cyclic-hierarchy cubulation methods of Hagen–Wise1605.07879v3 prove free actions under specific bottom-level and wall-independence hypotheses. Their definition explicitly allows nonlocally finite and infinite-dimensional cube complexes and does not demand metric properness. Replacing that conclusion by a finite-dimensional special action would be unsupported. For the full target, a route through relatively hyperbolic polynomial submapping tori still requires a new theorem producing the required finite-index RAAG injection; assuming all eligible polynomial peripherals are virtually special transfers the central difficulty, including the unresolved Hydra cases, rather than solving it.

Primary references (the convex-splitting theorem is also used as a proof premise): M.Linton, arXiv2510.10178v2, Theorems1.1,1.2 and Section4.4, https://arxiv.org/html/2510.10178v2; M.Hagen–D.T.Wise, arXiv1605.07879v3, Introduction and Corollary6.8, https://arxiv.org/html/1605.07879v3. G.C.Hruska–K.Ruane, arXiv1705.00784v3, Theorem1.3 and Section7, https://arxiv.org/html/1705.00784v3. The invariant-core algebra, explicit CAT(0) envelope, and countermodels above are independently checkable deductions using the stated prior inputs; priority is not asserted.
