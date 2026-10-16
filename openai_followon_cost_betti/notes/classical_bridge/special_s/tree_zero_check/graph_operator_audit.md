# Adversarial audit of the bipartite graph and convolution conventions

Target: the graph and operator legs of `../PROOF.md`.

## Verdict

Both legs are correct under the stated assumption that `h_1,...,h_99`
freely generate the group `F`. No counterexample or proof gap was found.

## Graph check

For the edges `g_L -- (g a_i)_R`, a label `i` determines a unique edge
incident to any prescribed endpoint. Thus two successive equal labels
in an edge walk mean immediate reversal of the same edge. A finite
simple cycle consequently has unequal consecutive labels, including at
the cyclic join.

Following a supposed cycle from a left vertex yields the product

`a_i1 a_j1^(-1) ... a_ik a_jk^(-1) = e`.

The signs alternate before identities are removed. An identity factor
has label zero. There are no consecutive zero labels. Between any two
consecutive surviving factors there can therefore be either no deleted
factor or exactly one:

- With no deleted factor, the signs are opposite and the indices are
  distinct by the nonbacktracking condition. Cancellation is impossible.
- With one deleted factor, the signs agree. Cancellation is impossible.

At least one factor survives, since an all-zero label sequence would
backtrack. Hence the surviving word is nonempty and freely reduced,
contradicting freeness. This argument does not silently assume that
cyclic reduction is required; ordinary nonempty free reduction suffices.

The neighbor count is exactly 100 on both sides. The zero edge connects
the two copies of each coordinate. On left vertices, the label sequence
`i,0` multiplies the coordinate by `h_i`, and `0,i` multiplies it by
`h_i^(-1)`. These paths prove connectedness.

## Operator check

For `T f(g) = sum_i f(g a_i)`, its Hilbert-space adjoint is
`T* f(r) = sum_i f(r a_i^(-1))`, by the substitution `r = g a_i`.

Graph adjacency on `ell²(F_L) ⊕ ell²(F_R)` evaluates the right component
at `g a_i` on the left, and the left component at `r a_i^(-1)` on the
right. It is therefore exactly `A(u,v)=(Tv,T*u)`.

The inversion map `Jf(x)=f(x^(-1))` is a complex-linear unitary
involution, with `J*=J`. Direct evaluation gives

`JTJ f(x) = sum_i f((x^(-1) a_i)^(-1))
          = sum_i f(a_i^(-1) x)`.

Thus left convolution by `S` is `JTJ`, and right convolution by `S` is
`T*`, with the definitions in the proof. Their adjoints are respectively
`JT*J` and `T`. All four are injective because both `T` and `T*` were
already shown injective. Merely knowing one operator injective would not
justify injectivity of its adjoint; the existing proof supplies the
additional fact needed. Explicitly writing these two adjoint identities
would avoid ambiguity in the phrase “Taking adjoints gives injectivity.”

## Extension to an ambient group

If these elements freely generate a subgroup `H` of a larger discrete
group `G`, injectivity extends to `ell²(G)`:

- Left convolution by `S` preserves each right coset `Hx`. Identifying
  `hx` with `h` identifies the restriction with left convolution on `H`.
- Right convolution by `S` preserves each left coset `xH`. Identifying
  `xh` with `h` identifies the restriction with right convolution on `H`.

The corresponding coset decompositions of `ell²(G)` are orthogonal
direct sums. A vector in the global kernel would restrict to a kernel
vector on every coset, so all restrictions vanish. The same argument
applies to the adjoints.

This extension requires the precise free-subgroup hypothesis. Distinct
elements alone do not suffice. For example, in the cyclic group of order
100, listing all 99 nonidentity elements gives `S=sum_{g in G} g`; its
convolution annihilates every function with zero total sum. The graph in
that case is finite and has cycles.

Strongest verified result: both graph/operator legs, including their
free-subgroup extension. Exact remaining gap for this audit: none.
