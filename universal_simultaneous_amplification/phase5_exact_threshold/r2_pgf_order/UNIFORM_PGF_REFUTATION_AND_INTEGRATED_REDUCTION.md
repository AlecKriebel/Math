# Exact refutation of the uniform stationary PGF order

Date: 2026-08-08 (America/Los_Angeles)

## Status

- **EXACTLY REFUTED:** the stationary marked-cache PGF need not dominate
  the uniform-binomial PGF pointwise on `[0,1]`.
- **PROVED:** had that PGF order held, stationary parity and the exact
  `psi` integral would have implied the fitness-two collision theorem.
- **PROVED:** the remaining collision sign has the coefficient, active-rank,
  and signed integration-by-parts forms below.
- **EXACTLY REFUTED:** the pointwise derivative shortcut used to force the
  PGF order.
- **EXACTLY REFUTED:** the residual active-CDF assertion `c_j>=0` for all
  `j>=1`; a fifteen-vertex weak-module family has `c_1<0` at small coupling.
- **OPEN:** the separate mean--singleton sign and the weighted integrated
  collision inequality.

## 1. The proposed order and its exact implication

Let `mu` be the normalized stationary law of the exact marked one-sample
chain on pairs `(C,v)`, put `K=|C|`, `N=n-1`, and define

\[
 F(t)=E_\mu t^K,
 \qquad B_N(t)=\left({1+t\over2}\right)^N,
 \qquad D(t)=F(t)-B_N(t).
\]

The proposed weaker envelope was

\[
                  D(t)\ge0\quad(0\le t\le1).       \tag{1}
\]

It compares stationarity only with the uniform marked law.  It is therefore
strictly different from the previously refuted comparison of stationarity
with the two-step marked law.

One marked step annihilates rank parity.  Stationarity consequently gives

\[
 E_\mu(-1)^K=0.                                    \tag{2}
\]

For the alternating observable

\[
 \psi_j=2\int_0^1{t^j-(-1)^{N-j}t^N\over1+t}\,dt,
\]

(2) removes the second term after averaging.  The uniform binomial law has
the same zero parity.  Hence

\[
 {1\over m}-{1\over m_K}
 =E_\mu\psi-E_U\psi
 =2\int_0^1 {D(t)\over1+t}\,dt.                    \tag{3}
\]

Thus (1) would indeed imply `m<=m_K`, with strictness unless `D` vanished
identically.

## 2. Exact reversible counterexample

Take the complete weighted graph on six vertices with lexicographically
ordered edge weights

```text
(01,02,03,04,05,12,13,14,15,23,24,25,34,35,45)
=
(1,3,3,1000,30,1000,300,3,1,10,1,30,1,300,30).
```

The independent verifier directly builds the `6*2^5=192` state marked
chain and solves its invariant law over `QQ`.  It obtains

\[
 D(0)=\Pr_\mu\{K=0\}-{1\over32}
      =-0.0007316650347359885\ldots<0.              \tag{4}
\]

The exact rational numerator and denominator are printed by the verifier.
This refutes (1) already at `t=0`.  On the same graph,

\[
 {1\over m}-{31\over80}
 =0.04628470486879076\ldots>0.                      \tag{5}
\]

Therefore the witness refutes only the pointwise PGF route, not the desired
collision theorem.

## 3. Exact factorization and active-rank coefficients

Normalization gives `D(1)=0`, while (2) gives `D(-1)=0`.  There is therefore
an exact polynomial factorization

\[
                    D(t)=(1-t^2)Q(t),               \tag{6}
\]

where `deg Q<=N-2`.  Let `q_k` be the stationary active-event rank law.
The marked/active identity is

\[
 \eta_k:=\Pr_\mu\{K=k\}={q_k+q_{k+1}\over2},
 \qquad q_0=q_{N+1}=0.                              \tag{7}
\]

If

\[
 q_k^K={\binom{N-1}{k-1}\over2^{N-1}}
\]

is the complete active law, then (7) gives

\[
 F(t)={1+t\over2t}\sum_{k=1}^Nq_kt^k.
\]

Writing `Q(t)=sum_(j=0)^(N-2)c_jt^j` and dividing by `t(1-t)` yields the
exact coefficients

\[
 \boxed{
 c_j={1\over2}\left[
       \Pr_q\{K\le j+1\}-\Pr_{q^K}\{K\le j+1\}
      \right].}                                    \tag{8}
\]

Equation (3) becomes the weakest coefficient sign actually needed:

\[
 \boxed{
 {1\over m}-{1\over m_K}
 =2\sum_{j=0}^{N-2}{c_j\over(j+1)(j+2)}.}           \tag{9}
\]

For the counterexample (4), the exact verifier finds

\[
                 c_0<0,\qquad c_1,c_2,c_3>0.        \tag{10}
\]

Thus `D` crosses once from negative to positive on `(0,1)`, while its
weighted integral remains positive.

The following residual statement survived the original finite screens:

\[
 c_j\ge0\quad(1\le j\le N-2).                       \tag{PCDF}
\]

By (8), this says that the active law has at least the complete cumulative
mass at every cut `2,...,N-1`; only the singleton cut may fail.  This is a
precise weakening of the fully refuted event-rank stochastic order.
It is now **EXACTLY REFUTED**.  Five weakly coupled copies of a weighted
three-vertex path give, in an exact singular limit,

\[
 \Pr_q\{K\le2\}-{7\over4096}
 =-{6530729\over10532745216}<0.
\]

Continuity gives connected rational counterexamples at every sufficiently
small positive rational coupling.  See `WEAK_MODULE_PCDF_REFUTATION.md`.

## 4. Signed integration by parts

For a marked state `(C,v)`, put `x=P_{vC}`.  Applying stationarity to the
exact radial drift gives, first for `t>0` and then polynomially at `t=0`,

\[
 E_\mu[t^{K-1}x]={F(t)\over1+t}.                    \tag{11}
\]

Define

\[
 A(t)=E_\mu[t^{K-1}(Nx-K)]
     ={NF(t)\over1+t}-F'(t),                        \tag{12}
\]

and normalize the PGF by

\[
 R(t)={2^NF(t)\over(1+t)^N}.
\]

Then

\[
 R'(t)=-{2^NA(t)\over(1+t)^N}.                     \tag{13}
\]

Using `R(1)=1`, substituting `R(t)-1=-int_t^1 R'(s)ds` into (3), and
reversing the order of integration proves

\[
 \boxed{
 {1\over m}-{1\over m_K}
 ={2\over N}\int_0^1
   \left[1-(1+t)^{-N}\right]A(t)\,dt.}              \tag{14}
\]

This is the exact signed integration-by-parts target.  The tempting
pointwise sufficient inequality `A(t)>=0` is false.  On the five-vertex
complete weighted graph with lexicographic weights

```text
(7,7,7,31,2,31,1,1,31,7)
```

the independent exact solve gives

\[
                         A(1/100)<0.                 \tag{15}
\]

Interestingly, that same graph has every coefficient of `Q` positive, so
even a graph satisfying the full PGF order can violate the derivative
shortcut.

One weaker feature survived the numerical audit:

1. `Q` has at most one sign change, necessarily `c_0<0` followed by positive
   coefficients.

This has not been proved.  A one-crossing statement by itself is also
insufficient; (14) still requires control of the signed areas.

A tempting coefficientwise route to one-crossing is exactly false.  If
`q_k^K` denotes the complete active law and `r_k=q_k/q_k^K`, direct
coefficient comparison in (12) gives

\[
 [t^{k-1}]A(t)
 ={(N-k)q_k-kq_{k+1}\over2}
 ={(N-k)q_k^K\over2}(r_k-r_{k+1}).                 \tag{15a}
\]

Thus nonnegative nonconstant coefficients would assert that the active
likelihood ratio decreases from rank two onward.  This fails exactly on the
six-vertex weighted path

```text
vertex order:       1--0--2--4--5--3
consecutive weights: 30, 4, 64, 1, 1860.
```

Its exact polynomial has coefficient signs

\[
                         (+,-,+,+),                 \tag{15b}
\]

with the negative coefficient at rank two.  The polynomial itself remains
strictly positive on `[0,1]`, so this refutes likelihood-ratio descent but
not a functional one-crossing theorem.  The exact verifier certifies both
claims.

There is, however, a useful exact unweighted identity.  If `pi_1` is the
singleton mass of the original proper-subset stationary dual, then

\[
 \int_0^1A(t)\,dt
 ={N\over2m}-1+\eta_0
 ={N+\pi_1-2m\over2m}.                              \tag{16}
\]

Consequently the following pair of strictly weaker structural lemmas would
have been sufficient for the collision theorem:

\[
 c_j\ge0\quad(j\ge1),                               \tag{17a}
\]

\[
 N+\pi_1-2m\ge0.                                    \tag{17b}
\]

Indeed, if `c_0>=0`, (17a) makes (9) nonnegative.  If `c_0<0`, then
`eta_0<2^{-N}`, and (17b) gives

\[
 {1\over m}\ge {2(1-\eta_0)\over N}
              > {2(1-2^{-N})\over N}={1\over m_K}.
\]

Lemma (17a) is now **EXACTLY FALSE** by the weak-module family above.  The
separate mean--singleton sign (17b) remains **OPEN** and is strictly positive
in that counterexample's singular limit.  Thus any successful replacement
must control the weighted sum (9) or (14) without termwise active-CDF signs.

## 5. Verification

Run

```text
.venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/r2_pgf_order/verify_uniform_pgf_refutation.py
```

The verifier:

1. constructs the marked transition matrix directly from the one-sample
   rule;
2. checks every row sum;
3. solves stationarity over exact rationals;
4. verifies parity and the factorization (6);
5. certifies (4), (5), and the coefficient signs (10);
6. reconstructs the integrated collision value from (9);
7. independently certifies the derivative failure (15).
8. certifies the weighted-path likelihood-ratio failure (15b) while checking
   that its full derivative polynomial stays positive on `[0,1]`.

The floating scripts `search_uniform_pgf.py` and `search_one_crossing.py`
are hostile discovery tools only.  Their output is not a proof of (17).
