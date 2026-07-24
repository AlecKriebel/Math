# Harmonic-combination centered-skew rank cuts

## Status and scope

This note proves a universal rank inequality for real symmetric matrices and
applies it exactly to zonal harmonic kernel matrices.  Two low-degree
instances refute the degree-four local-hybrid pair/triple
pseudodistribution.

This is rank information visible in pair and triple moments.  It is not a
genuinely four-point constraint, and it is not an upper bound for the
five-dimensional kissing number by itself.

The exact instance data are in
[`../certificates/harmonic_combination_centered_skew_instances.json`](../certificates/harmonic_combination_centered_skew_instances.json).
They are checked, without an optimizer or floating-point arithmetic, by
[`../verifiers/verify_harmonic_combination_centered_skew.py`](../verifiers/verify_harmonic_combination_centered_skew.py).

## 1. A sharp centered-skew inequality

Let \(K\) be a real symmetric matrix of rank at most \(r\), where \(r\ge2\).
Put
\[
 V=\operatorname {tr}K^2-\frac{(\operatorname {tr}K)^2}{r}
\]
and
\[
 D=\operatorname {tr}K^3
   -\frac{3}{r}\operatorname {tr}K\,\operatorname {tr}K^2
   +\frac{2}{r^2}(\operatorname {tr}K)^3.
\]

**Lemma 1 (centered-skew rank inequality).**
\[
\boxed{\quad
r(r-1)D^2\le (r-2)^2V^3.
\quad}                                                   \tag{1}
\]

**Proof.**
Pad the nonzero eigenvalues of \(K\) with zeros to obtain
\(\lambda_1,\ldots,\lambda_r\).  Let
\[
 m=\frac1r\sum_i\lambda_i,\qquad z_i=\lambda_i-m.
\]
Then
\[
 \sum_i z_i=0,\qquad V=\sum_i z_i^2,\qquad D=\sum_i z_i^3.
\]
If \(V=0\), then every \(z_i=0\), and (1) is immediate.  Otherwise divide
the \(z_i\) by \(\sqrt V\).  It remains to maximize
\(\left|\sum_i z_i^3\right|\) subject to
\[
 \sum_i z_i=0,\qquad \sum_i z_i^2=1.                    \tag{2}
\]
The constraint set is compact.  At an extremum, Lagrange multipliers give
\[
 3z_i^2=\alpha+2\beta z_i
\]
for every \(i\).  Thus the \(z_i\) assume at most two distinct values.
If one value occurs \(p\) times and the other \(q=r-p\) times, direct use
of (2) gives
\[
 \left(\sum_i z_i^3\right)^2
 =\frac{(q-p)^2}{pqr}
 =\frac{(r-2p)^2}{rp(r-p)}.                             \tag{3}
\]
For \(1\le p\le r/2\), the last expression decreases with \(p\): the
derivative of \((r-2p)^2/[p(r-p)]\) has numerator
\[
 -r^2(r-2p).
\]
Hence (3) is largest at \(p=1\) or \(p=r-1\), where it equals
\[
 \frac{(r-2)^2}{r(r-1)}.
\]
Rescaling by \(V^{3/2}\) proves (1). \(\square\)

No positivity hypothesis on \(K\) is used.

## 2. Zonal harmonic combinations

For a code \(x_1,\ldots,x_N\subset S^4\), let
\[
 H_k=\bigl(P_k(\langle x_i,x_j\rangle)\bigr)_{i,j=1}^N,
\]
where \(P_k(1)=1\) is the dimension-five normalized Gegenbauer
polynomial.  The addition theorem gives
\[
 \operatorname {rank}H_k\le h_k,\qquad
 h_k=\binom{k+4}{4}-\binom{k+2}{4}.                     \tag{4}
\]
Consequently, for arbitrary real coefficients \(a_k\),
\[
 K=\sum_{k\in S}a_kH_k
\quad\Longrightarrow\quad
\operatorname {rank}K\le\sum_{k\in S}h_k.               \tag{5}
\]
The coefficients need not be nonnegative: the image of \(K\) is contained
in the sum of the harmonic evaluation spaces, and Lemma 1 applies to every
real symmetric matrix.

Write
\[
 \kappa(t)=\sum_{k\in S}a_kP_k(t).
\]
Then the traces needed in Lemma 1 depend only on pair and triple data:
\[
\begin{aligned}
\operatorname {tr}K
 &=N\kappa(1),\\
\operatorname {tr}K^2
 &=N\kappa(1)^2+\sum_{i\ne j}\kappa(g_{ij})^2,\\
\operatorname {tr}K^3
 &=N\kappa(1)^3
   +3\kappa(1)\sum_{i\ne j}\kappa(g_{ij})^2\\
 &\qquad
   +6\sum_{\{i,j,\ell\}}
       \kappa(g_{ij})\kappa(g_{i\ell})\kappa(g_{j\ell}).
                                                               \tag{6}
\end{aligned}
\]
Thus (1) is rank information absent from ordinary BV block positivity,
yet it is still only a pair/triple-moment constraint.

## 3. Exact refutation of the degree-four pseudodistribution

Use the five nodes and integer triple counts in
`local_hybrid_degree4_rank_color_clique_pseudodistribution.json`.

### 3.1 The combination \((H_0+5H_1)/6\)

Here
\[
 \kappa(t)=\frac16+\frac56t,\qquad r=h_0+h_1=1+5=6.
\]
Exact evaluation of (6) gives
\[
\operatorname {tr}K=41,\quad
\operatorname {tr}K^2=\frac{8149679}{28800},\quad
\operatorname {tr}K^3=\frac{71571557473}{36000000}.
\]
Therefore
\[
 V=\frac{80879}{28800},\qquad
 D=\frac{289016549}{18000000}.
\]
After dividing (1) by two, the required inequality is
\[
 15D^2\le8V^3.
\]
Instead, the pseudodistribution has the exact residual
\[
 8V^3-15D^2
 =
 -\frac{34431882734317334357}{9331200000000000}<0.       \tag{7}
\]

### 3.2 The pure degree-two kernel \(H_2\)

Since
\[
 P_2(t)=\frac{5t^2-1}{4},\qquad h_2=14,
\]
equation (6) gives
\[
\operatorname {tr}H_2=41,\quad
\operatorname {tr}H_2^2=
\frac{1566584056811}{12800000000},
\]
\[
\operatorname {tr}H_2^3=
\frac{48029489854860834589}{128000000000000000}.
\]
Thus
\[
 V=\frac{207688397677}{89600000000},\qquad
 D=\frac{20244638316825894861}{6272000000000000000}.
\]
The reduced rank-\(14\) inequality is \(91D^2\le72V^3\), but
\[
 72V^3-91D^2
 =
 -\frac{
 5894231556035691703147357630514100177
 }{
 114688000000000000000000000000000000
 }<0.                                                    \tag{8}
\]

Both failures are exact.  They show that the earlier degree-four
pseudodistribution cannot be the pair/triple distribution of a rank-five
spherical configuration, even though it passes the previously imposed
BV, C047, colored-degree, and graph-moment tests.

## 4. Rational linear cuts for the search

For fixed pair data, \(V\) and the non-triple part of
\(\operatorname {tr}K^3\) are constants.  Hence \(D\) is affine in the
triangle counts.  Lemma 1 gives an exact algebraic interval for \(D\).
The discovery MILP uses slightly wider rational intervals:
\[
 |D|\le\frac72
 \quad\text{for }(H_0+5H_1)/6,
\qquad
 |D|\le\frac{157}{50}
 \quad\text{for }H_2.                                  \tag{9}
\]
They are valid outer approximations because
\[
15\left(\frac72\right)^2-8V_{01}^3
=\frac{19611647008561}{2985984000000}>0,
\]
and
\[
91\left(\frac{157}{50}\right)^2-72V_2^3
=\frac{
47450085131380413914603963850403
}{
89915392000000000000000000000000
}>0.
\]
The two pseudodistribution values of \(D\) lie outside these wider bands,
so even the rational linear cuts reject it.

These cuts are implemented in
`experiments/search_local_hybrid_degree3.py`.

## 5. Reproduction and dependency map

From the repository root, run

```bash
PYTHONPATH=. /usr/bin/python3 \
  verifiers/verify_harmonic_combination_centered_skew.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  tests.test_harmonic_combination_centered_skew -v
```

The proof dependency is
\[
\text{addition theorem and harmonic dimensions}
\Longrightarrow \operatorname {rank}K\le r
\Longrightarrow \text{Lemma 1}
\Longrightarrow \text{pair/triple trace inequality}.
\]
The verifier independently performs
\[
\text{stored rational nodes and counts}
\Longrightarrow \text{exact traces}
\Longrightarrow \text{exact negative residuals and outer-band checks}.
\]
