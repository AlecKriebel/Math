# An exact half-density theorem for a heterogeneous dB-dual regime

Date: 2026-08-02 (America/Los_Angeles)

## Status

The theorem in Section 2 is **PROVED**.  It establishes the desired
`r=2` half-density ceiling for a broad, explicitly checkable class of
weighted graphs.  It does **not** prove the all-graph ceiling: the
complementary regime in (13) remains open.

Section 3 gives a second exact reduction of the all-graph question to a
chi-square information inequality.  The reduction is **PROVED**; the final
upper bound in (21) is **OPEN**.  Complete graphs attain equality in that
open bound, and finite tests have found no violation, but those tests are
not a proof.

Throughout, `P` is any loopless row-stochastic kernel.  Symmetry of the
underlying edge weights is not needed for the proved subtheorem.

## 1. Exact linear drift in hole coordinates

At fitness `r=2`, put

\[
 H_{vi}=\frac{2P_{vi}}{1+P_{vi}},\qquad
 T_i=\sum_v H_{vi}.
 \tag{1}
\]

Let `D` be the generator of the exact geometric-union dB dual and let
`x_i(A)=1_{i\in A}`.  A target `v` is updated only when `v\in A`; then it is
removed, while a hole `i\notin A` is inserted with probability `H_vi`.
Consequently, for arbitrary coefficients `z_i`,

\[
 g(A)=-\sum_i z_i x_i(A)
 \tag{2}
\]

has exact drift

\[
 \mathcal Dg(A)
 =\sum_{v\in A}z_v-
   \sum_{v\in A,\ i\notin A}H_{vi}z_i.
 \tag{3}
\]

Write `C=V\setminus A`, `h=|C|`, and `Z=\sum_i z_i`.  Expanding (3) in
the hole indicators gives

\[
 \boxed{
 \mathcal Dg(V\setminus C)-(n-2h)
 = Z-n+
   \sum_{i\in C}\{2-z_i(1+T_i)\}
   +\sum_{\{i,j\}\subseteq C}
       (z_iH_{ji}+z_jH_{ij}).}
 \tag{4}
\]

This is a quadratic polynomial in the holes with nonnegative pair
coefficients whenever `z_i>=0`.

## 2. Proved heterogeneous-temperature theorem

Define

\[
 S_H=\sum_{i=1}^n\frac1{1+T_i}.
 \tag{5}
\]

### Theorem 2.1

Let `n>=3`.  If

\[
 \boxed{S_H\ge \frac n2,}
 \tag{6}
\]

then every stationary law `Pi` of the exact geometric-union dB dual at
`r=2` satisfies

\[
 \boxed{E_\Pi|A|\le\frac n2.}
 \tag{7}
\]

Hence the uniformly initialized dB fixation probability obeys

\[
 \rho_{\rm dB}(G,2)\le\frac12.
 \tag{8}
\]

#### Proof

Every row of `P` sums to one, and `H_vi>=P_vi`; hence
`sum_i T_i>=n`.  Also `H_vi<2P_vi` on positive entries, so
`sum_iT_i<2n`.  Cauchy--Schwarz therefore gives

\[
 S_H\ge\frac{n^2}{n+\sum_iT_i}>\frac n3\ge1,
 \tag{9}
\]

with strictness at `n=3`.  Thus the following coefficients are positive:

\[
 \lambda=\frac{n-2}{S_H-1},\qquad
 z_i=\frac{\lambda}{1+T_i}.
 \tag{10}
\]

They obey `z_i(1+T_i)=lambda` and `Z=lambda S_H`.  Substitution in
(4) yields

\[
 \mathcal Dg(V\setminus C)-(n-2h)
 =-(h-1)(Z-n)+
   \sum_{\{i,j\}\subseteq C}(z_iH_{ji}+z_jH_{ij}).
 \tag{11}
\]

Indeed, the constant and linear part on a one-hole set vanishes because

\[
 Z-n+2-\lambda
 =\lambda(S_H-1)-(n-2)=0.
\]

Condition (6) is exactly the assertion `Z<=n`:

\[
 Z\le n
 \Longleftrightarrow
 \frac{(n-2)S_H}{S_H-1}\le n
 \Longleftrightarrow 2S_H\ge n.
 \tag{12}
\]

Both terms on the right of (11) are therefore nonnegative for every
nonempty hole set `C`.  The full dual state is transient on a loopless
graph, so these are all states in stationary support.  Stationarity gives
`E_Pi Dg=0`; averaging (11) proves
`0>=E_Pi(2|A|-n)`, which is (7).  The exact duality identity
`rho_dB=E_Pi|A|/n` proves (8).  QED.

The unresolved complementary regime is

\[
 \boxed{S_H<\frac n2.}
 \tag{13}
\]

It includes dense near-regular kernels, in particular sufficiently large
complete graphs.  Thus Theorem 2.1 is not by itself the desired universal
obstruction.

There is an exact probabilistic reading of the same threshold.  If
`q_i=Pi(i notin A)` and `q_ij^00=Pi(i,j notin A)`, the stationary singleton
equation is

\[
 1-q_i=\sum_vH_{vi}\{q_i-q_{iv}^{00}\},
\]

and hence

\[
 \boxed{
 E_\Pi|V\setminus A|=S_H+E_\Pi W(V\setminus A),\qquad
 W(C)=\sum_{i,v\in C}\frac{H_{vi}}{1+T_i}.}
 \tag{13a}
\]

For `S_H<n/2`, the missing amount is therefore precisely an internal
two-hole mass.  The linear certificate above extends to this regime whenever

\[
 W(C)\ge \frac{n-2S_H}{n-2}(|C|-1)
 \quad\hbox{for every nonempty }C.
 \tag{13b}
\]

Condition (13b) is a fractional spanning-tree/arboricity condition for the
symmetrized edge weights in `W`.  It is not universal: weak modular cuts
give exact counterexamples to (13b), though not to the stationary
half-density conjecture.  This identifies the role of the quadratic
correction in Section 4: it must bridge precisely those deficient cuts.

## 3. Exact chi-square target-information reduction

Restore null target updates and let `K_v` be the one-target stochastic
kernel: if `v` is a hole it is the identity, while if `v` is occupied it
performs the geometric burst.  If `Pi` is stationary for the uniform-target
kernel, define

\[
 \mu_v=\Pi K_v,
 \qquad f_v(B)=\frac{\mu_v(B)}{\Pi(B)}.
 \tag{14}
\]

Stationarity says

\[
 \frac1n\sum_v f_v(B)=1.
 \tag{15}
\]

Every `v`-update leaves `v` absent.  Therefore `f_v(B)=0` for `v\in B`.
For `v\notin B`, the null source `A=B` contributes exactly `Pi(B)`, so

\[
 f_v(B)=1+e_v(B),\qquad e_v(B)\ge0.
 \tag{16}
\]

Writing `k=|B|` and `h=n-k`, (15) gives the pointwise identity

\[
 \boxed{\sum_{v\notin B}e_v(B)=k.}
 \tag{17}
\]

Let `V` be the uniform target and `B` the stationary output.  The order-two
chi-square target information is

\[
 I_2(V;B)=\frac1n\sum_{v,B}\frac{\mu_v(B)^2}{\Pi(B)}.
 \tag{18}
\]

Equations (16)--(17) give exactly

\[
 \boxed{
 I_2(V;B)=1+\frac{E_\Pi k}{n}
 +\frac1nE_\Pi\sum_{v\notin B}e_v(B)^2.}
 \tag{19}
\]

On the other hand, conditional on `B`, the posterior law of `V` is
supported on its `h` holes.  Cauchy--Schwarz and then Jensen imply

\[
 \boxed{
 I_2(V;B)\ge nE_\Pi\frac1{n-|B|}
 \ge\frac{n}{n-E_\Pi|B|}.}
 \tag{20}
\]

Consequently the single information inequality

\[
 \boxed{I_2(V;B)\le2}
 \tag{21}
\]

would prove the all-graph half-density ceiling immediately.  Equivalently,
by (19), (21) is

\[
 E_\Pi\sum_{v\notin B}e_v(B)^2
 \le E_\Pi(n-|B|).
 \tag{22}
\]

The geometric burst has mean sample count two, which makes (21) a natural
sharp contraction statement.  However, idempotence of each `K_v` is not
enough: the same idempotence persists at other fitness values, while the
dual density can exceed one half.  A proof must use the `r=2` geometric
law, not just random-scan structure.

For the complete graph, direct exact calculation gives `I_2=2` for every
`n>=3`, so (21), if true, is sharp.  This equality and the additional
finite rational checks in the companion verifier are diagnostics only.

## 4. Quadratic hole formula for the remaining regime

For reference, the general graph-dependent quadratic

\[
 g(A)=\sum_i c_ix_i+\sum_{i<j}q_{ij}x_ix_j
\]

has an especially small hole expansion.  Put

\[
 b_i=c_i+\sum_jq_{ij},\qquad
 h(x)=\frac{2x}{1+x},
\]

and

\[
 L_{ij}=2-H_{ij}-H_{ji}
 +\sum_{v\ne i,j}h(P_{vi}+P_{vj}).
\]

Then the slack in (4) is a Boolean polynomial of degree at most three with

\[
 \begin{aligned}
 \alpha_0&=-\sum_i b_i-n,\\
 \alpha_i&=b_i(1+T_i)+\sum_v(1-H_{vi})q_{iv}+2,\\
 \alpha_{ij}&=-H_{ij}b_j-H_{ji}b_i-L_{ij}q_{ij},\\
 \beta_{ijk}&=q_{ij}h(P_{ki}+P_{kj})
 +q_{ik}h(P_{ji}+P_{jk})
 +q_{jk}h(P_{ij}+P_{ik}).
 \end{aligned}
 \tag{23}
\]

Thus every nonnegative `q_ij` makes all cubic coefficients nonnegative.
Floating-point searches find half-density certificates with nonnegative
edge-supported `q` very broadly, including graphs in (13), but no universal
choice or feasibility proof is claimed here.
