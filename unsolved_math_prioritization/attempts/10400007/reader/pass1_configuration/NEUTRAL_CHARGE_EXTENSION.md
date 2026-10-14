# Minimal neutral charge configurations still have knot-independent graded groups

Authored continuation of the configuration-space audit, 14 October 2026. This is a scoped computation, not a Jones construction or a novelty claim. Use the conventions `M=S³\K`, `k=Q(u)`, `L_r`, `F_n(M)` and `A_w` from the main audit.

## Theorem

Let `n≥2` and let the integer charge vector `w=(w₁,…,w_n)` satisfy

- `Σ_i w_i=0`;
- `Σ_{i∈B} w_i≠0` for every nonempty proper subset `B⊊{1,…,n}`.

Such vectors exist for every `n`: take `(1,…,1,−(n−1))`. Define `Σ_n` to be the full simplex whose vertices are the `binom(n,2)` possible edges of a graph on the labeled vertex set `{1,…,n}`. Let `Disc_n⊂Σ_n` be the subcomplex consisting of disconnected graphs, and define

`T_n = H^{n−2}(Σ_n,Disc_n;k)`.

For `n=2`, the relative pair is a point relative to the empty space, so `T₂=k`. Then

`H_i(F_n(M);A_w) ≅ H_{i−2(n−1)}(M;k) ⊗ T_n`.

Moreover, `dim_k(T_n)=(n−1)!`. Therefore the only nonzero ordinary groups are in degrees `2n−2` and `2n−1`, with dimension `(n−1)!` in each degree. The only nonzero Borel–Moore groups are in degrees `n+1` and `n+2`, also of dimension `(n−1)!` each.

The vector space `T_n` is defined canonically from labeled graph cohomology. No preferred basis for it, and no distinguished pairing giving a knot polynomial, is asserted. In particular, the above graded-vector-space isomorphism does not replace the extra operations required for a Jones construction.

## Proof

Let `X=Mⁿ`, let `D` be the union of pairwise collision diagonals, and let `A=L_{w₁}⊠⋯⊠L_{w_n}` on `X`.

All individual charges are nonzero, so `H_c^*(X;A)=0`. A nonempty collection `J` of pairwise diagonals can be viewed as an edge set on `{1,…,n}`. The intersection `D_J` is the partial diagonal whose blocks are the connected components of that graph. There are two cases.

1. If the graph is disconnected, each component is a nonempty proper subset. Its charge is nonzero by hypothesis. Hence `D_J` has compact-support-acyclic coefficients, by the complement acyclicity lemma and Künneth.
2. If the graph is connected, `D_J` is the full diagonal `M`, and the restricted coefficient is `L_{Σ_iw_i}=L₀=k`, canonically trivialized by multiplying the tensor factors.

Use the finite closed-cover Čech spectral sequence justified in the main audit. In Čech degree `p`, its first page is a sum over edge sets of size `p+1`. Only connected graphs remain, each contributing a copy of `H_c^q(M;k)`. Between two connected edge sets, the restriction map is the identity on `H_c^q(M;k)`, with the Čech alternating sign.

This is exactly

`C^p(Σ_n,Disc_n;k) ⊗ H_c^q(M;k)`.

Indeed relative simplicial cochains are cochains on the full edge simplex that vanish on the disconnected-graph subcomplex; equivalently, they have a basis indexed by connected edge sets. The simplicial coboundary adds one edge, with the same alternating incidence signs. The local-system trivializations on the full diagonal are the same, so no additional coefficient matrices enter these differentials.

For `n≥3`, the standard disconnected-graph-complex theorem states that `Disc_n` has reduced cohomology only in degree `n−3`, of dimension `(n−1)!`. Since `Σ_n` is contractible, its relative cohomology with `Disc_n` is concentrated in degree `n−2`, where it is `T_n`. The `n=2` case is the point/empty-space calculation above. Thus the Čech spectral sequence has just one nonzero column from its second page onward, so it collapses with no extension ambiguity in the column filtration. It gives

`H_c^j(D;A|_D) ≅ H_c^{j−(n−2)}(M;k) ⊗ T_n`.

Because the ambient compact-support cohomology is zero, open/closed localization shifts once more:

`H_c^j(F_n(M);A_w) ≅ H_c^{j−(n−1)}(M;k) ⊗ T_n`.

Now use oriented Poincaré duality in dimensions `3n` and `3`:

`H_i(F_n(M);A_w)`
`≅ H_c^{3n−i}(F_n(M);A_w)`
`≅ H_c^{2n+1−i}(M;k)⊗T_n`
`≅ H_{i−2n+2}(M;k)⊗T_n`.

This proves the ordinary statement. The dual charge vector `−w` satisfies the same conditions. Ordinary cohomology with `A_w` is the linear dual of ordinary homology with `A_{−w}`. Applying Borel–Moore duality in dimension `3n` then puts its nonzero groups in degrees `3n−(2n−2)=n+2` and `3n−(2n−1)=n+1`. ∎

## Small checks and consequence

- For `n=2`, charges `(1,−1)` yield the main audit's ordinary degrees `2,3`, each of dimension one.
- For `n=3`, charges `(1,1,−2)` give a connected-graph Čech differential `k³→k`. Its kernel has dimension two in Čech degree one. Ordinary homology is consequently two-dimensional in each of degrees `4,5`.
- For `n=4`, charges `(1,1,1,−3)` give dimension six in ordinary degrees `6,7`.

Thus moving from nonzero total charge to a minimal neutral charge vector evades vanishing but still yields the same graded vector spaces for every knot. A construction based on these particular groups alone cannot recover Jones. This result does not cover arbitrary neutral vectors with proper neutral subsets, secondary operations, torsion, relative classes, or higher-rank systems.

## Primary source for the graph-complex input

Eric Babson, Anders Björner, Svante Linusson, John Shareshian, and Volkmar Welker, *Complexes of not i-connected graphs*, Proposition 2.1(i), arXiv:math/9705219v1, pp.3–4. The proposition records the disconnected-graph result and explains its partition-lattice/crosscut origin. [Primary manuscript](https://arxiv.org/pdf/math/9705219), [record](https://arxiv.org/abs/math/9705219). The relative-cochain reduction and local-system calculation above are supplied explicitly rather than attributed to that paper.
