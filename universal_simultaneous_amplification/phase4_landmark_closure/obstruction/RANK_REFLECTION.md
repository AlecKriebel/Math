# Occupied-event rank reflection for the dB dual

Date: 2026-08-02 (America/Los_Angeles)

Status: the event-chain reformulation and the complete-reference rank
calculation are **PROVED**.  The stationary reflection inequality remains
**OPEN**.  All finite tests described below are diagnostics, not a proof.

## 1. The occupied-event chain

Let `D` be the continuous-time generator of the geometric-OR dB dual and
let `G_v(A,B)` be the probability of the burst at target `v`, including a
null burst.  On nonempty sets define

\[
 T(A,B)={1\over |A|}\sum_{v\in A}G_v(A,B).
 \tag{1}
\]

If `Pi` is the stationary law of `D` and `m=E_Pi |A|`, then

\[
 \nu(A)={|A|\Pi(A)\over m}
 \tag{2}
\]

is stationary for `T`.  Indeed, stationarity of the continuous-time chain,
with its null bursts restored, says

\[
 \sum_A\Pi(A)\sum_{v\in A}G_v(A,B)=|B|\Pi(B).
\]

Put `a=r-1` and

\[
 \eta(A)={\nu(A)\over a^{|A|}}.
\]

The proposed complementary-level inequality is exactly

\[
 \boxed{\eta_k\le \eta_{n-k}\quad(k>n/2),\qquad
 \eta_k=\sum_{|A|=k}\eta(A).}
 \tag{3}
\]

Thus the factors `k` and `n-k` are not mysterious: they are the Palm bias
created by observing the dB dual at an occupied-target event.

At `r=2`, no fitness tilt remains.  In that case (3) asserts that the rank
law of the actual stochastic event kernel `T` is biased toward the lower
member of every complementary pair.

## 2. Exact complete-reference calculation

Write `N=n-1` and fix a target `v`.  Let `U` be the nonempty union in its
geometric burst and put `s=|U|`.  Consider the complete-graph reference event
mass

\[
 M_a(A)=|A|(n-|A|)a^{|A|}.
 \tag{4}
\]

Write the source as `A=H union {v}`, with `H subseteq V\{v}`.  After the
burst the state is `H union U`.  Dividing output mass by
`a^{|H union U|}`, and including the target-selection factor `1/|A|`, gives

\[
 (N-|H|)a^{1-|U\setminus H|}.
\]

Consequently the tilted output rank polynomial conditional on `|U|=s` is

\[
 \boxed{
 F_{s,a}(z)=
 a^{1-s}(1+a)^{s-1}z^s(1+z)^{N-s-1}
 \{N+a(N-s)+sz\}.}
 \tag{5}
\]

The apparent negative exponent of `1+z` at `s=N` cancels against the last
factor.  Formula (5) follows by writing
`X=H cap U`, `Y=H\setminus U` and summing first over `X`:

\[
 \sum_{X\subseteq U}a^{|X|}(N-|X|-|Y|)
 =(1+a)^{s-1}\{(N-|Y|)(1+a)-sa\}.
\]

Before the burst, the same target contributes the symmetric polynomial

\[
 I(z)=Nz(1+z)^{N-1}.                                  \tag{6}
\]

For the uniform row `P_vu=1/N`, averaging (5) over the geometric union gives
exactly (6), as it must from the complete-graph invariant law

\[
 \Pi_K(A)\ \propto\ (n-|A|)a^{|A|}.
\]

At `r=2`, (5) becomes

\[
 F_s(z)=2^{s-1}z^s(1+z)^{N-s-1}\{2N-s+sz\}.           \tag{7}
\]

If `ell(x)=x/(2-x)` and

\[
 E_j(p)=\sum_{|L|=j}\ell\left(\sum_{i\in L}p_i\right)
\]

for the row `p=P_v*`, then inclusion-exclusion gives the coefficient of
level `l` after this target event as

\[
 \boxed{
 O_l(p)=\sum_{j=1}^l(-1)^{l-j}2^{j-1}(2N-j)
 {N-j\choose l-j}E_j(p).}                             \tag{8}
\]

This is an exact finite formula involving only subset sums of one row.  The
complete row makes `O_l=O_(n-l)`.

For `n=3` and `n=4`, the one-step complementary-rank inequality follows
universally from convexity of `ell`.  The only nontrivial differences are

\[
 O_1-O_2=6\sum_i\ell(p_i)-4\ge0\quad(n=3),
\]

and

\[
 O_1-O_3=8\sum_{|L|=2}\ell(p_L)-12\ge0\quad(n=4).
\]

Their equality cases are the uniform row.  Beginning at `n=5`, (8) has
genuinely alternating coefficients; ordinary Jensen convexity no longer
proves the sign.

## 3. Candidate stronger cone at `r=2`

Besides (3), every tested iterate of `M_1` under `T` obeyed all factorial
complement inequalities

\[
 \boxed{
 \sum_A\mu(A){n-|A|\choose j}
 \ge
 \sum_A\mu(A){|A|\choose j},
 \qquad 1\le j<n.}                                    \tag{9}
\]

The starting measure has equality in (3) and (9), and its iterates converge
to `nu` on every tested irreducible chain.  This suggests a
variation-diminishing cone built from complementary ranks and their
binomial transforms.

Several tempting simplifications are **false**:

* pointwise complement comparison `nu(A)<=nu(A^c)`;
* Boolean stochastic domination of `nu` by its complement;
* ultra-log-concavity of the event rank sequence on arbitrary directed
  kernels;
* invariance of the coarse rank-reflection cone alone;
* invariance of the coarse factorial cone (9) alone;
* invariance of their intersection for arbitrary input measures.

Thus a successful invariant cone must retain more within-level information,
probably through graph-sensitive subset transforms.  Formula (8) is the
current exact entry point: it shows that the first image of the symmetric
reference is governed by one-row subset-sum transforms, while later images
require their nonexchangeable analogues.

## 4. Consequence if the stationary reflection is proved

At `r=2`, (3) implies

\[
 E_\Pi |A|^2\le {n\over2}E_\Pi|A|.
\]

Jensen then gives

\[
 \rho_{\rm dB}(G,2)={E_\Pi|A|\over n}\le {1\over2}.
\]

This is a genuine all-graph density ceiling, but it is still weaker than the
finite complete-graph baseline.  A final simultaneous-amplification
obstruction would therefore require either a finite-size strengthening or a
quantitative cross-rule stability theorem near equality.
