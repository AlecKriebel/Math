# Attempt 5: a standard geometric representation of the automorphism group

## Target and outcome

The Coxeter group's standard reflection representation does not automatically extend, even virtually, to an orthogonal implementation of its automorphism group. The exact obstruction below blocks this particular geometric route. It is not a counterexample to the Coxeter-quotient conjecture.

## Proposition

For the universal rank-three Coxeter group

W=⟨s,t,u | s²=t²=u²=1⟩,

let ρ be its standard geometric representation on V with basis e_s,e_t,e_u and symmetric bilinear form

B(e_i,e_i)=1,    B(e_i,e_j)=−1 for i≠j.

There is no finite-index subgroup H≤Aut(W) such that every f∈H can be implemented by a B-isometry T_f satisfying

T_f ρ(w) T_f⁻¹=ρ(f(w)) for every w∈W.

The conclusion excludes even a choice of implementing isometries; it does not merely exclude a coherent homomorphism f↦T_f.

Proof. Define α∈Aut(W) by

α(s)=s,    α(t)=t,    α(u)=(st)u(st)⁻¹.

The inverse is obtained by conjugating u by (st)⁻¹ and fixing s,t. Reduced free-product normal forms show that α has infinite order. Consequently every finite-index H contains αⁿ for some integer n≥1.

Use column vectors. In the indicated basis,

ρ(s) = ((−1,2,2),(0,1,0),(0,0,1)),
ρ(t) = ((1,0,0),(2,−1,2),(0,0,1)),
ρ(st)= ((3,−2,6),(2,−1,2),(0,0,1)).

Induction on n gives

v_n=ρ(st)ⁿe_u=(2n(2n+1), 2n(2n−1), 1).

In particular B(v_n,v_n)=1 and B(e_t,v_n)=−4n−1.

Suppose a B-isometry T implements αⁿ. Because αⁿ fixes t, T conjugates the reflection ρ(t) to itself. Its one-dimensional negative eigenspace is therefore preserved, so T(e_t)=ε_t e_t with ε_t∈{±1}. Likewise, because αⁿ sends u to (st)ⁿu(st)⁻ⁿ, the negative eigenspace of the image reflection is the line Rv_n. Thus T(e_u)=ε_u v_n with ε_u∈{±1}; the normalization follows from B(e_u,e_u)=B(v_n,v_n)=1.

But preservation of B would imply

1=|B(e_t,e_u)|=|B(T(e_t),T(e_u))|=|−4n−1|,

which is impossible for n≥1. Therefore αⁿ cannot be implemented, contradicting the assumed property of H. ∎

The integer matrix identities are checked by the accompanying standard-library-only script. The displayed induction and eigenspace argument are the proof; a finite list of computational checks is not substituted for them.

## Exact gap

An abstract automorphism can preserve involutions and all finite product orders while changing the Gram data of pairs whose product has infinite order. Thus the standard Coxeter representation cannot simply be normalized to produce the desired automorphism quotient. One would need a different invariant geometric object and a separately proved epimorphism from its action image onto an infinite Coxeter group. A nontrivial action, nonamenability, or failure of property (T) is not that epimorphism.

The test group here is itself an even Coxeter group, so its automorphism group already has the required quotient by known results. This deliberately demonstrates failure of the proposed construction on a positive case, not failure of the conjecture.

## Source

- O. Varghese, Coxeter quotients of the automorphism group of a Coxeter group, Algebraic & Geometric Topology 26 (2026), 2353–2362, Corollary 1.5 for the even-Coxeter conclusion. https://doi.org/10.2140/agt.2026.26.2353

The obstruction proof and matrix calculations above are authored deductions from the stated presentation and reflection matrices.
