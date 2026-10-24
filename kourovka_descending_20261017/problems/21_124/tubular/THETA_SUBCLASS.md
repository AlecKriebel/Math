# A two-vertex theta subclass of Kourovka 21.124

UTC: 2026-10-24T22:21:12Z. **Partial result, awaiting independent adversarial review.** This does not resolve the full problem. Originality of this subclass has not been established.

## Claim and exact scope

Let G be the fundamental group of a graph of groups with two vertex groups Z² and exactly three edges joining the two vertices. Suppose G is CAT(0) and admits a homomorphism h:G→Z nonzero on every edge group. Then there is a homomorphism

    Φ:G→R²⋊C₂

whose restriction to each vertex group is injective and discrete; C₂ acts as reflection in a line. Consequently G has (VRC), and is virtually special, by Merladet Urigüen–Minasyan, *Virtual retractions in free constructions*, Theorem 1.6 and Proposition 1.10 (appendix), https://arxiv.org/html/2505.18054v3.

The height hypothesis is the standard tubular free-by-cyclic criterion, stated precisely in Button, *Tubular free by cyclic groups and the strongest Tits alternative*, Theorem/Proposition 2.1, https://arxiv.org/abs/1510.05842. The theorem above is written with the explicit height hypothesis so that this external criterion is not silently substituted for a definition. Graphs with more edges, arbitrary theta subdivisions, or arbitrary CAT(0) free-by-cyclic groups are not covered.

## Rational normalization

Name the vertices L,R and the edges e₀,e₁,e₂. Orient all edges from L to R. Let uᵢ∈G_L and vᵢ∈G_R be the corresponding images of a common edge generator; write nᵢ=h(uᵢ)=h(vᵢ)≠0. Use e₀ as spanning tree edge. The vertex rational vector spaces have bases (x,τ_L) and (y,τ_R), with x,y nonzero in the respective height kernels and τ_L=u₀/n₀, τ_R=v₀/n₀ of height1. Thus, for rational pᵢ,qᵢ,

    uᵢ=nᵢ(τ_L+pᵢx),  vᵢ=nᵢ(τ_R+qᵢy),  i=1,2,

and p₀=q₀=0. This is only rational linear notation for constructing homomorphisms from the integral vertex lattices; no roots in G are assumed.

We seek nonzero rational a,b, rational c, and signs ε₁,ε₂∈{±1} such that

    pᵢ a+c=εᵢ(qᵢ b+c),  i=1,2.                 (1)

Given these, take an orthonormal basis E,H of R², reflection R(E)=−E, R(H)=H, and define translation images

    x↦aE, y↦bE, τ_L↦cE+H, τ_R↦cE+H.

Each non-tree stable letter is sent to 1 or R according to εᵢ. Equation(1) verifies its edge relation, and e₀ is verified by the common image of τ_L,τ_R. Hence the graph-of-groups presentation gives Φ. Both vertex linear maps are invertible, because a,b≠0 and H is independent of E, so they inject the vertex lattices discretely. Multiplying by nᵢ does not change the edge check, regardless of its sign.

## Elementary sign lemma

For any rational p₁,p₂,q₁,q₂, equation(1) has a solution with a,b≠0 unless precisely one of the lists (0,p₁,p₂), (0,q₁,q₂) is constant and the other has three distinct entries.

Proof: For signs (+,−), the first equation is p₁a=q₁b. It admits nonzero a,b exactly when p₁,q₁ are both zero or both nonzero; the second equation then determines c. Signs (−,+) work under the analogous condition for p₂,q₂. If either possibility applies, we are done.

Otherwise pᵢ=0 if and only if qᵢ≠0, for i=1,2. Signs (−,−) give

    (p₁−p₂)a+(q₁−q₂)b=0,

and then determine c. They admit nonzero a,b exactly when p₁−p₂ and q₁−q₂ are both zero or both nonzero. If the zero locations of p₁,p₂ differ, both differences are nonzero, so this case works. If p₁=p₂=0, failure requires q₁,q₂ nonzero and distinct. If q₁=q₂=0, failure requires p₁,p₂ nonzero and distinct. These are exactly the exceptional configurations. In them signs (+,+) also force a=0 or b=0, and every other sign choice has already been excluded. This proves the lemma.

## CAT(0) rules out the exceptional configuration

In a geometric CAT(0) action, each rank-two vertex group has a flat translation lattice by the Flat Torus Theorem. Let ||·||_L and ||·||_R be the positive-definite Euclidean norms on its rational vector spaces. Conjugate elements have equal translation length, and so do the copies of a tree-edge element identified in G. Dividing the three edge length equalities by |nᵢ| gives

    ||τ_L+pᵢx||_L=||τ_R+qᵢy||_R,  i=0,1,2.

If all pᵢ vanish and 0,q₁,q₂ are distinct, the strictly convex quadratic

    f(q)=||τ_R+qy||_R²

would have the same value at three distinct real arguments. That is impossible because y≠0 gives a positive quadratic coefficient. The reverse case is identical. Hence the sign lemma applies, completing the claim.

A geometric action is required here: a merely free action on an infinite-dimensional cube complex does not justify these flat metrics.

## Scope and priority check

The theta graph is outside the cycle-disjoint hypothesis of Merladet Urigüen–Minasyan2511.21293v1, Corollary1.4, and outside the one-vertex hypothesis of Wu–Ye2504.14192v2, Theorem4.5. A targeted public primary-source search for tubular theta/three-edge virtual specialness did not locate a separately stated theorem. This bounded search does not establish novelty; the elementary deduction may be implicit in the existing Euclidean-by-finite criterion. No preprint or discovery claim is made.
