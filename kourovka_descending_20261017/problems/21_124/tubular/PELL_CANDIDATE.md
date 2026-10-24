# Four-edge Pell candidate: exact eligibility and a limited holonomy filter

UTC: 2026-10-24T22:21:12Z. **Unresolved candidate, not a counterexample.** Discovery estimate toward a full21.124 resolution: **4%**. The only obstruction presently proved is to elementary abelian2 linear holonomy, which is much weaker than excluding all finite holonomy.

## Presentation and eligibility

Let (pᵢ,qᵢ) be (3,2),(20,14),(119,84), i=1,2,3. Define

    G=⟨a,b,t,s₁,s₂,s₃ | [a,t]=[b,t]=1,
                    sᵢ(a^{pᵢ}t)sᵢ⁻¹=b^{qᵢ}t (i=1,2,3)⟩.

Its tubular graph has two rank-two abelian vertices and four edges. The tree edge identifies t between the vertex groups; the other three give the displayed HNN relations. The height h(t)=1, h(a)=h(b)=h(sᵢ)=0 is nonzero on each edge. Bass–Serre theory gives ker h as the fundamental group of a finite graph of groups with two infinite-cyclic vertices, four trivial edges, hence a free group of rank2+(4−2+1)=5. Explicitly,

    t a t⁻¹=a, t b t⁻¹=b,
    t sᵢ t⁻¹=b^{-qᵢ}sᵢa^{pᵢ}.

These assignments define an automorphism of the free group on a,b,s₁,s₂,s₃: its inverse fixes a,b and sends sᵢ↦b^{qᵢ}sᵢa^{-pᵢ}. Thus G is F₅-by-Z without a dependence on the height criterion.

Use Gram matrices in the respective ordered bases (a,t),(b,t):

    Q_L=[[1,1/2],[1/2,2]], Q_R=[[2,1],[1,2]].

Their determinants are7/4 and3, both positive. Every displayed pair satisfies pᵢ(pᵢ+1)=2qᵢ(qᵢ+1), so

    ||pᵢa+t||²=pᵢ²+pᵢ+2=2qᵢ²+2qᵢ+2=||qᵢb+t||².

The tree edge t also has matching squared length2. Flat tori with these metrics joined by locally isometric Euclidean cylinders therefore give the usual CAT(0) tree-of-flats universal cover and a geometric action of G. The construction can equivalently be certified by the standard tubular translation-length criterion used in Wu–Ye2504.14192v2 §2, https://arxiv.org/html/2504.14192v2.

## Why elementary abelian2 linear holonomy cannot witness (VRC)

Suppose Φ:G→R^N⋊Q is a homomorphism with Q an elementary abelian2 group, and that Φ is injective on both rank-two vertex groups. Choose an even positive M killing the linear parts of all vertex generators. Write A,B,T for the translation vectors of Φ(a^M), Φ(b^M), Φ(t^M). Since a commutes with t and b commutes with t, the edge relations give

    Sᵢ(pᵢA+T)=qᵢB+T,                         (1)

where Sᵢ is the orthogonal linear action of the Q-image of sᵢ. All Sᵢ commute and square to1, so simultaneously decompose R^N into their common real sign eigenspaces. On a space where the three signs are εᵢ, equation(1) gives the scalar-coefficient linear system with rows

    [pᵢ, −εᵢqᵢ, 1−εᵢ]

on the components A,B,T (multiplying by εᵢ if needed). The seven nontrivial sign choices have determinants

    4, −5712, 6528, −28, −816, 28, −4,

in lexicographic sign order starting (−,−,−). Thus A=B=T=0 on each such eigenspace. For signs(+,+,+), the first two rows [3,−2,0],[20,−14,0] have determinant−2 in the first two coordinates, so A=B=0 there too. Hence A=B=0 globally, contradicting vertex injectivity.

This argument permits arbitrary Euclidean dimension. It does not apply when Q has noncommuting elements or commuting elements of order greater than2. A finite quotient of index2, or an elementary abelian2 quotient, cannot supply the necessary vertex-surviving abelianization for this particular presentation; this is not an obstruction to arbitrary virtual specialness.

## Exact current gap and rejected overreach

A negative resolution requires excluding **every** finite linear holonomy group Q, or a different invariant inherited by virtual RAAG embeddings. No such proof is presently available. Infinite holonomy in the specific two-dimensional realization would not suffice, because a vertex-injective witness may require a larger Euclidean dimension (2505.18054v3 Example8.10 explicitly demonstrates this phenomenon). Failure of the sign ansatz is not a negative resolution.

The first numerically suggested pairs (2,1),(14,10),(84,59) were incorrect for this Pell equation. The exact checker rejected them before any promotion; they were replaced throughout accepted computations by the three correct pairs above. The theta-subclass proof does not use these numerical pairs.
