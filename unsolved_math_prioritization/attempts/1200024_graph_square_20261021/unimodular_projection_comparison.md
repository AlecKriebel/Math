# Square invariance under a unimodular transitive action

Let G be connected, simple, infinite, locally finite, and admit a unimodular transitive automorphism group Γ. Put H=G². The same Γ acts transitively on H. Write E and E' for their unoriented edge sets, choosing one orientation for each edge; automorphisms act by signed permutations. Let Z_G be the closed subspace of square-summable gradients, equivalently the orthogonal complement of finite cycle vectors. Define Z_H analogously.

For a vertex function f, write E_G(f)=sum_(xy∈E)|f(y)−f(x)|². If G has degree d, then

E_G(f) ≤ E_H(f) ≤ (4d−3) E_G(f).

To verify the upper bound, bound every new-edge squared difference by the sum of such differences along all length-two paths joining its endpoints, then apply |a+b|²≤2(|a|²+|b|²). Each old edge occurs in exactly 2(d−1) unoriented nonbacktracking length-two paths. Counting all such paths, including those whose endpoints already are adjacent, can only increase the upper bound.

Thus T(df)=d_H f defines a bounded Γ-equivariant bijection from Z_G to Z_H, with bounded inverse given by restriction to old edges. It is well-defined because a gradient determines f modulo constants. Its polar part U is a Γ-equivariant unitary between Z_G and Z_H. Extend U to be zero on Z_G-perp; then U*U=P_G and UU*=P_H, the respective gradient projections.

Here is the exact mass transport proving equality of rooted projection dimensions. For chosen unit edge coordinates χ_e and χ_f, define

m(x,y)=(1/4) sum_(e incident x) sum_(f incident y) |<Uχ_e,χ_f>|².

The signs from arbitrary orientations disappear under the squared absolute value, so m is nonnegative and Γ-invariant. Each edge has two endpoints. Parseval therefore gives

sum_y m(o,y)=(1/2) sum_(e incident o) <P_Gχ_e,χ_e>,
sum_x m(x,o)=(1/2) sum_(f incident o) <P_Hχ_f,χ_f>.

The sums are finite because these quantities are at most half the respective graph degrees. The unimodular mass-transport principle equates the sums. The transfer-current formula identifies each projection diagonal with the corresponding FUSF edge probability. Hence Edeg_FUSF(G)=Edeg_FUSF(H), and consequently b_F(G)=b_F(H).

This proof does not extend merely by dropping unimodularity. The bounded equivariant isomorphism T and its polar part still exist, but the equality of the two displayed rooted sums is precisely the unavailable ordinary mass-transport identity. One cannot infer equality of those diagonal sums just from unitary equivalence in a nonunimodular equivariant category.

The formula in operator_notes.md was independently checked: with L the new-edge gradient extension and A=(I+L*L)^−1 on Z_G, the difference is tau_new(L A L*)−tau_old(L*L A). Its factors, 1/2 incidence normalization, and energy bound are correct. The terms vanish by the rectangular trace identity above only under the stated unimodular hypothesis.

Primary references inspected: BLPS, *Uniform Spanning Forests*, https://rdlyons.pages.iu.edu/pdf/usf.pdf , Theorem 7.8 and §7; Gaboriau, *Invariant Percolation and Harmonic Dirichlet Functions*, https://arxiv.org/pdf/math/0405458 , Proposition 2.9 and Definition 2.10 (explicit unimodular hypothesis). The proof here is an explicit derivation, not a claim that either source states square invariance in this form.
