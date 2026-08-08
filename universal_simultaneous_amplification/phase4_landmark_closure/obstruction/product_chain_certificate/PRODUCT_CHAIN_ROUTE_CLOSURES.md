# Exact barriers to coarse product-chain certificates at `r=3/2`

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.

## Status

The universal fixation-product conjecture

\[
 \rho_{\rm Bd}(G,3/2)\rho_{\rm dB}(G,3/2)
 \le
 \rho_{\rm Bd}(K_n,3/2)\rho_{\rm dB}(K_n,3/2)       \tag{1}
\]

remains **OPEN**.  This note proves three exact route closures:

1. no pointwise product-chain Poisson certificate depending only on the two
   ranks and their overlap can prove the normalized arithmetic strengthening
   of (1), already on the unweighted three-path;
2. the sum of the two stationary dual ranks is not stochastically dominated
   by its complete-graph counterpart; and
3. the natural all-`z` coverage-product inequality whose `z -> 1` endpoint
   is (1) is false.

All counterexamples below leave (1) strict in the conjectured direction.
They close proof architectures, not the fixation-product statement.

## 1. Exact product dual and the normalized target

Let `L` be the exact Bd branching--coalescing dual and `D` the exact
geometric-union dB dual at `r=3/2`.  Their atomic transitions are derived
directly from the update rules:

* in `L`, a neutral arrow into an occupied target moves the particle to its
  source, and a selective arrow of rate `1/2` retains the target and adds the
  source;
* in `D`, an occupied target is removed and replaced by the union of `K`
  row-neighbor samples, where

  \[
    \Pr(K=k)={2\over3}\left({1\over3}\right)^{k-1}.
  \]

If their stationary means are `m_L,m_D`, then uniform-singleton fixation is
`m_U/n`.  Write `m_L^K,m_D^K` for the complete means.  The normalized
arithmetic inequality

\[
 {m_L\over m_L^K}+{m_D\over m_D^K}\le2             \tag{2}
\]

would imply (1) by AM--GM.  On the independent product chain

\[
 Q=L\otimes I+I\otimes D,                            \tag{3}
\]

the centered target is

\[
 T(A,B)={|A|\over m_L^K}+{|B|\over m_D^K}-2.         \tag{4}
\]

A pointwise Lyapunov certificate

\[
 Q\Psi(A,B)\ge T(A,B)                                \tag{5}
\]

would prove (2) after stationary averaging.

## 2. Five-atom Farkas obstruction on the three-path

Take the unweighted path whose center is vertex `2` and whose leaves are
`0,1`:

\[
 W=\begin{pmatrix}0&0&1\\0&0&1\\1&1&0\end{pmatrix}. \tag{6}
\]

For `n=3`, direct solution of the complete dual count chains gives

\[
 m_L^K={27\over19},\qquad m_D^K={6\over5}.           \tag{7}
\]

The full dB-dual state is transient and cannot be re-entered, so use
`A in {1,...,7}` and `B in {1,...,6}` in bit-mask notation.  Define the
following probability law `Lambda` on five product states:

| `A` | `B` | `Lambda(A,B)` |
|---:|---:|---:|
| `001` | `011` | `133/284` |
| `011` | `011` | `77/568` |
| `100` | `011` | `361/2272` |
| `101` | `011` | `209/1136` |
| `111` | `011` | `121/2272` |

All masses are positive and sum to one.  Exact substitution in the atomic
product generator proves

\[
 \mathbb E_\Lambda Q\,
 \mathbf1\{(|A|,|B|,|A\cap B|)=(i,j,k)\}=0          \tag{8}
\]

for every one of the ten feasible triples `(i,j,k)`.  Hence

\[
 \boxed{\mathbb E_\Lambda Q\Psi(|A|,|B|,|A\cap B|)=0} \tag{9}
\]

for every real function `Psi` of the two ranks and their overlap.  On the
other hand,

\[
 \boxed{\mathbb E_\Lambda T={571\over852}>0.}        \tag{10}
\]

Averaging (5) under `Lambda` would give `0 >= 571/852`, a contradiction.
Therefore:

> **Theorem 2.1.** On the unweighted three-path, no product-chain Poisson
> potential depending only on `(|A|,|B|,|A cap B|)` can prove (2) through the
> pointwise inequality (5).

This permits an arbitrary value of the potential at each feasible triple;
it is not a bounded-degree restriction.  What fails is the loss of
within-rank information distinguishing the center from the leaves.

The separating law is not stationary.  The actual three-path dual laws
satisfy (2) strictly, with exact slack

\[
 2-{m_L\over m_L^K}-{m_D\over m_D^K}={19\over504}>0. \tag{11}
\]

Thus Theorem 2.1 does not refute either (2) or (1).

## 3. Rank-convolution domination is false

For a stationary dual rank law define

\[
 F_U(z)=\mathbb E_{\pi_U}z^{|A|}.                    \tag{12}
\]

The product `F_L(z)F_D(z)` is the probability generating function of the
sum of two independent stationary dual ranks.  A tempting strengthening of
the cross-rule tradeoff is stochastic domination of this sum by its
complete counterpart.  It would imply

\[
 F_L(z)F_D(z)\ge F_L^K(z)F_D^K(z),\qquad0<z<1.       \tag{13}
\]

Take the connected weighted graph

\[
 W=\begin{pmatrix}
 0&7&2&3\\
 7&0&3&0\\
 2&3&0&7\\
 3&0&7&0
 \end{pmatrix}.                                      \tag{14}
\]

Exact stationary solves give the factorization

\[
 F_LF_D-F_L^KF_D^K=z^2(1-z)Q(z),                     \tag{15}
\]

where

\[
 \boxed{Q(0)=
 -{6470085667377135548\over28216589762863303936875}<0.} \tag{16}
\]

Thus (13), and equivalently the required lower-tail comparison at total
rank two, is false.  Yet `Q(1)>0`, so the mean-rank sum has the conjectured
strict sign on this same graph.  The failure occurs away from the endpoint
needed for fixation.

## 4. The all-`z` coverage-product route is false

By exact set duality,

\[
 C_U(z):=1-F_U(z)                                    \tag{17}
\]

is the forward fixation probability when every vertex is initially mutant
independently with probability `1-z`.  Moreover

\[
 \lim_{z\uparrow1}{C_L(z)C_D(z)\over(1-z)^2}=m_Lm_D. \tag{18}
\]

Consequently the all-`z` inequality

\[
 C_L(z)C_D(z)\le C_L^K(z)C_D^K(z),\qquad0<z<1,       \tag{19}
\]

would prove (1) by taking `z -> 1`.

It is false.  On

\[
 W=\begin{pmatrix}
 0&0&7&0\\
 0&0&1&7\\
 7&1&0&1\\
 0&7&1&0
 \end{pmatrix},                                      \tag{20}
\]

put

\[
 C_L^KC_D^K-C_LC_D=z(1-z)^2R(z).                     \tag{21}
\]

The exact constant term is

\[
 \boxed{R(0)=
 -{60733866936691239552155\over
 10628249467345628376063975}<0.}                     \tag{22}
\]

Thus (19) reverses for all sufficiently small positive `z`.  Nevertheless

\[
 R(1)=m_L^Km_D^K-m_Lm_D>0,                           \tag{23}
\]

so the fixation-product comparison itself is strict in the conjectured
direction on (20).  Any coverage-transform proof must therefore be local
near `z=1` or use additional non-rank information; global positivity on the
Bernoulli initialization parameter is unavailable.

## 5. Exact scope

**PROVED / EXACTLY COMPUTED.**  Equations (8)--(11), (15)--(16), and
(21)--(23), directly from the two dual Markov rules over rational arithmetic.

**ROUTES CLOSED.**  Coarse radial/overlap pointwise Poisson certificates,
stationary rank-sum stochastic domination, and global all-`z`
coverage-product domination.

**OPEN.**  The endpoint inequality (1), the normalized arithmetic
strengthening (2), and product-chain potentials retaining graph-sensitive
within-rank information.

## 6. Verification

Run

```text
python verify_product_chain_barriers.py
```

The verifier independently builds both exact dual generators, solves the
stationary systems, checks all ten Farkas balance equations, and reconstructs
the two rational polynomial counterexamples.
