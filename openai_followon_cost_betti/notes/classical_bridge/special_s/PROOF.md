# Injectivity of `1+h_1+...+h_99` on the free group

## Exact claim

Let `F` be the free group on `h_1,...,h_99`, and let
`S=1+h_1+...+h_99` in the complex group algebra. Left convolution and right
convolution by `S` have trivial kernels on `ell^2(F)`. Their adjoints have
trivial kernels as well.

The proof below is elementary. It does not invoke any general analytic
zero-divisor conjecture.

## 1. The bipartite graph is the infinite 100-regular tree

Put `a_0=e` and `a_i=h_i` for `1<=i<=99`. Form a graph with vertex set the
disjoint union `F_L disjoint-union F_R`, and with undirected edges

`g_L -- (g a_i)_R` for every `g in F` and `0<=i<=99`.

Every left vertex has 100 distinct neighbors. Every right vertex `r_R`
has the 100 distinct neighbors `(r a_i^(-1))_L`. Thus the graph is
100-regular and has no multiple edges. It is connected: the edge of label
zero joins `g_L` to `g_R`, and two-edge paths move among left vertices by
right multiplication by `h_i` or `h_i^(-1)`.

To prove acyclicity, suppose a finite cycle exists, and follow it starting
at a left vertex. Let its consecutive edge labels be
`i_1,j_1,i_2,j_2,...,i_k,j_k`. Traversing an edge from left to right
multiplies the group coordinate on the right by `a_i`, and traversing one
from right to left multiplies it by `a_j^(-1)`. Closure would imply

`a_(i_1) a_(j_1)^(-1) ... a_(i_k) a_(j_k)^(-1) = e`.

The cycle has no immediate backtracking, so every two consecutive edge
labels are distinct (including at the cyclic join). Delete each identity
factor `a_0` from the displayed word. There cannot have been two adjacent
identity factors. Whenever an identity is deleted, the two factors it
brings together have the same exponent sign, so cannot cancel. Every
remaining adjacent pair with opposite signs was already adjacent before
the deletion and has distinct generator indices, so also cannot cancel.
At least one nonidentity factor remains. The resulting word is therefore
a nonempty freely reduced word in the free generators, and cannot equal
the identity. This contradiction proves acyclicity.

Hence the connected graph is the infinite 100-regular tree. Equivalently,
it is the universal covering graph of the graph with two vertices and
100 parallel edges, using the label-zero edge as a spanning tree in that
quotient. The direct acyclicity proof supplies the identification without
assuming any covering-space result.

## 2. Elementary no-kernel lemma for regular-tree adjacency

**Lemma.** Let `d>=2`, and let `A` be the adjacency operator of the infinite
`d`-regular tree. If `f in ell^2(V)` satisfies `Af=0`, then `f=0`.

**Proof.** Root the tree at a vertex `o`, put `q=d-1>=1`, and write

`E_n = sum_(dist(o,v)=n) |f(v)|^2`.

All spheres are finite, and `sum_(n>=0) E_n = ||f||_2^2 < infinity`.
For every vertex `v` at distance `n>=1`, let `p(v)` be its parent and
`C(v)` its `q` children. The equation `Af(v)=0` gives

`sum_(w in C(v)) f(w) = -f(p(v))`.

Cauchy–Schwarz consequently yields

`sum_(w in C(v)) |f(w)|^2 >= |f(p(v))|^2 / q`.

For `n>=2`, summing over the vertices `v` on sphere `n` counts each vertex
of sphere `n+1` once on the left. Each vertex of sphere `n-1` is a parent
of exactly `q` vertices of sphere `n`, so the right-hand side sums to
`E_(n-1)`. Thus

`E_(n+1) >= E_(n-1)` for every `n>=2`.

The sequences `E_1,E_3,E_5,...` and `E_2,E_4,E_6,...` are nonnegative and
nondecreasing. Each sequence has a finite sum, so every one of its terms
must be zero. In particular, all values away from the root vanish. At
any neighbor `v` of `o`, the equation `Af(v)=0` then reduces to `f(o)=0`.
Therefore `f=0`. QED.

Adjacency is a bounded operator on `ell^2(V)`: by Cauchy–Schwarz,
`||Af||_2^2 <= d^2 ||f||_2^2`. Thus all operator statements and the local
equations used above have their usual Hilbert-space meaning.

**Boundary checks.** The proof includes `d=2`, when the tree is the
bi-infinite path and `q=1`. It uses exact regularity beyond the root and
does not automatically extend to irregular trees with leaves. The
constant coefficient sum is essential to the graph identification;
arbitrary weighted sums require a different argument.

## 3. Operator conventions and the deduction

Define on `ell^2(F)`

`(T f)(g) = sum_(i=0)^99 f(g a_i)`.

Each summand is a unitary translation, so `T` is bounded. Its adjoint is

`(T^* f)(r) = sum_(i=0)^99 f(r a_i^(-1))`.

Under the identification of graph functions with
`ell^2(F_L) direct-sum ell^2(F_R)`, the graph adjacency operator is exactly

`A(u,v) = (T v, T^* u)`,

or the block matrix `[[0,T],[T^*,0]]`.

The lemma implies `ker A={0}`. If `T v=0`, then `A(0,v)=0`, so `v=0`.
If `T^* u=0`, then `A(u,0)=0`, so `u=0`. Therefore both `T` and `T^*`
are injective.

To match common group-algebra conventions, define

`(S * f)(x) = sum_(i=0)^99 f(a_i^(-1) x)` (left convolution),

`(f * S)(x) = sum_(i=0)^99 f(x a_i^(-1))` (right convolution).

Right convolution by `S` is `T^*`. Define the unitary inversion map
`(Jf)(x)=f(x^(-1))`, for which `J^2=I`. A direct substitution gives

`J T J f(x) = sum_(i=0)^99 f(a_i^(-1) x) = (S*f)(x)`.

Thus left convolution by `S` is `J T J`, and is injective as well. The
right-convolution adjoint is `T`, and the left-convolution adjoint is
`(J T J)^*=J T^* J`. Since both `T` and `T^*` have already been proved
injective, these two adjoints are injective too. This conclusion uses
both established kernel statements; injectivity of an arbitrary bounded
operator alone would not imply injectivity of its adjoint.
Conventions that define a right translation as `f(g)->f(gh)` simply call
`T` the right operator instead of `T^*`; both are covered by the proof.

## 4. Transfer from a free subgroup to an ambient group

If `F` is a subgroup of any group `Gamma`, the same sum `S` is injective
on `ell^2(Gamma)` for both convolution conventions. No torsion-freeness
assumption on `Gamma` is required.

For right convolution, use the orthogonal decomposition over **left**
cosets `tF`. Right multiplication by every `a_i^(-1)` preserves `tF`.
The unitary identification of the summand `ell^2(tF)` with `ell^2(F)` is
`f_t(h)=f(t h)`, and under it

`(f*S)(t h) = sum_i f(t h a_i^(-1)) = (f_t*S)(h)`.

Thus right convolution is the orthogonal direct sum of copies of the
already-injective right-convolution operator on `ell^2(F)`.

For left convolution, use the orthogonal decomposition over **right**
cosets `Ft`. Left multiplication by every `a_i^(-1)` preserves `Ft`.
With `f_t(h)=f(h t)` one has

`(S*f)(h t) = sum_i f(a_i^(-1) h t) = (S*f_t)(h)`.

Again each summand has trivial kernel, so the full operator does too.
This transfer requires the `h_i` actually to freely generate a subgroup;
merely naming 99 ambient-group elements does not supply that hypothesis.

## Conclusion and scope limit

The proposed tree mechanism is valid, including its two-copy graph and
block-adjacency identification. It proves precisely that the special
free-group operator `1+h_1+...+h_99` and its left/right adjoints are
injective on `ell^2(F)`, and on `ell^2(Gamma)` whenever `F` embeds as a
subgroup of `Gamma`. Injectivity does not assert a bounded inverse or a
positive lower bound on singular values. This does not independently
establish any claim about cost or any general coefficient/operator family.

## Independent adversarial verification

A separate subagent independently reproduced the no-kernel proof and
then audited the reduced-word graph argument, block matrix, inversion
map, and coset conventions. It found no mathematical flaw. Its only
correction concerned the phrasing about adjoints, now made explicit
above. See `tree_zero_check/proof.md` and its accompanying research log.
