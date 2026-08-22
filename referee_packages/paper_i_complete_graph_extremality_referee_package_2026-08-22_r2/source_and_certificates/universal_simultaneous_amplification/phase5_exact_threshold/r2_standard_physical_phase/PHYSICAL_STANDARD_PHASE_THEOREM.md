# The physical standard-sector phase theorem at fitness two

Date: 2026-08-20 (America/Los_Angeles)

## Status and scope

This note proves the missing **physical standard-sector** sign in the
stationary fitness-two Hessian at the complete replacement kernel.  The
proof is exact and valid in every population order.

The reward used here is the one obtained from the radial Poisson solution
in the stationary perturbation formula.  It is not the different reward in
`../r2_determinant/TRUE_INVERSE_RANK_PHASE_CONTRACTION.md`.

Put `n=N+1`.  The main result is:

> **Theorem.**  For every `N>=2`, let `d_0=d_N=0` and let
> `d_1,...,d_(N-1)` be the complete-rank Poisson gradients defined in
> (2) below.  For the signed standard quotient `H`, binomial source
> `sigma`, and physical reward `gamma(d)` defined below,
> \[
>  \Phi_N(d):=\sigma(I-H)^{-1}\gamma(d)>0.                 \tag{1}
> \]
> Consequently, for every nonzero standard tangent `delta=E(xi)`,
> \[
>  \mathcal R_2(E(\xi))
>  ={\|\xi\|^2\over4(N+1)^2(N-1)}\Phi_N(d)>0.             \tag{2}
> \]

Together with the already proved symmetric-balanced and
antisymmetric-balanced signs, (2) makes the inverse-mean Hessian positive
definite on the full loopless row-stochastic tangent space.

## 1. The radial Poisson gradient

The complete active rank has stationary law

\[
 \pi_k={\binom{N-1}{k-1}\over2^{N-1}},\qquad1\le k\le N,
\]

and rank kernel

\[
 R_{k,k+1}={N-k\over2N},\qquad
 R_{k,k-1}={k-1\over2N}.
\]

Put

\[
 c_0={2^N-1\over N2^{N-1}}.
\]

If `h` solves `(I-R)h=1/k-c_0` modulo constants and
`d_k=h_k-h_(k+1)`, subtraction of adjacent equations gives

\[
 \boxed{(N-k)d_k-(k-1)d_{k-1}
 =2N\left({1\over k}-c_0\right),}
 \qquad d_0=d_N=0.                                      \tag{3}
\]

Solving (3) gives

\[
 {2\over k}-d_k
 ={2^{2-N}\displaystyle\sum_{r=k}^{N-1}\binom{N-1}{r}
   \over
   (N-1)\binom{N-2}{k-1}}.                               \tag{4}
\]

In particular,

\[
 \boxed{{2(N-2)\over Nk}\le d_k\le{2\over k}}
 \qquad(1\le k<N).                                      \tag{5}
\]

For completeness, the lower bound in (5) is equivalent to

\[
 Nk\sum_{r=k}^{N-1}\binom{N-1}{r}
 \le2^N(N-1)\binom{N-2}{k-1}.                            \tag{6}
\]

If `k<=N/2`, bound the tail by the full binomial sum.  The endpoint
`k=1` is immediate; for `k>=2`, use
`binom(N-2,k-1)>=N-2` and
`Nk<=N^2/2<=2(N-1)(N-2)` for `N>=4`.  If `k>N/2`, put
`m=N-1-k`; the lower half of the binomial row is increasing, so

\[
 \sum_{r=k}^{N-1}\binom{N-1}{r}
 =\sum_{j=0}^{m}\binom{N-1}{j}
 \le(N-k){N-1\over k}\binom{N-2}{k-1}.
\]

Now (6) follows from `N(N-k)<=2^N`.  The remaining order `N=2` is
direct.  Thus (5) is an all-order inequality, not a finite screen.

## 2. The signed quotient and the physical reward

Distinguish labels `x,y`.  The positive orientation channels are

\[
\begin{array}{c|l|c}
P_k&v=x,\ x,y\notin B&1\le k<N,\\
Q_k&v=x,\ y\in B&1\le k\le N,\\
R_k&v\notin\{x,y\},\ x\in B,\ y\notin B&1\le k<N.
\end{array}
\]

The negative orientation exchanges `x,y`.  On these signed channel values,
the complete active operator is

\[
 H=\begin{pmatrix}S&C\\-D&Q\end{pmatrix},                 \tag{7}
\]

where the good order is `(P_1,...,P_(N-1),R_1,...,R_(N-1))`
and the bad order is `(Q_1,...,Q_N)`.  Every block in (7) is
entrywise nonnegative.  The nonzero signed rows are

\[
 P_k\longrightarrow
 {k\over2N}P_k+{N-k-1\over2N}P_{k+1}+{1\over2N}Q_{k+1},  \tag{8}
\]

\[
\begin{aligned}
 Q_k\longrightarrow{}&{k^2-1\over2kN}Q_k+{N-k\over2N}Q_{k+1}\\
 &-{k-1\over2kN}P_{k-1}-{N-k\over2kN}P_k\\
 &-{(k-1)^2\over2kN}R_{k-1}
   -{(k-1)(N-k)\over2kN}R_k,
\end{aligned}                                               \tag{9}
\]

and

\[
\begin{aligned}
 R_k\longrightarrow{}&
 \left\{{k\over2N}+{(k-1)(N-k)\over2kN}\right\}R_k
 +{N-k-1\over2N}R_{k+1}+{(k-1)^2\over2kN}R_{k-1}\\
 &+{1\over2kN}Q_k+{k-1\over2kN}P_{k-1}
   +{N-k\over2kN}P_k.
\end{aligned}                                               \tag{10}
\]

Terms outside their physical ranges are deleted.  The binomial source is

\[
 \sigma(R_k)={\binom{N-2}{k-1}\over2^{N-2}},
 \qquad \sigma(P_k)=0.                                    \tag{11}
\]

The physical reward is

\[
\begin{aligned}
 \gamma(P_k)&=k d_k,\\
 \gamma(R_k)&=N d_k+{(N+1)(k-1)\over k}d_{k-1},\\
 \gamma(Q_k)&=-q_k,
\end{aligned}                                               \tag{12}
\]

where

\[
 q_k=(N-k)d_k+{(N+1)(k-1)\over k}d_{k-1}>0,
 \qquad1\le k\le N.                                      \tag{13}
\]

At `k=N`, only the `Q_N` formula is used.  Notice the pure-standard
relation

\[
 \gamma(Q_k)=\gamma(P_k)-\gamma(R_k)                       \tag{14}
\]

whenever all three channels exist.

## 3. Exact normalization to the physical Hessian

Let `xi` have coordinate sum zero and let

\[
 E(\xi)_{ij}={\xi_i+N\xi_j\over (N+1)(N-1)},
 \qquad i\ne j.                                           \tag{15}
\]

For a radial function with gradient `d`, the first active perturbation in
the direction `E(xi)` has standard feature coordinates

\[
 a_k={k d_k\over2(N+1)(N-1)},\qquad
 b_k={N d_k\over2(N+1)(N-1)}
     +{(k-1)d_{k-1}\over2k(N-1)}.                          \tag{16}
\]

Thus `gamma` in (12) is exactly `2(N+1)(N-1)` times this physical
source.  The signed quotient restricted to the pure-standard feature
subspace is the physical two-feature complete operator: a feature
`a_k xi_v+b_k sum_(i in B)xi_i` has channel values

\[
 P_k=a_k,\qquad R_k=b_k,\qquad Q_k=a_k-b_k.                 \tag{17}
\]

The averaged second perturbation is

\[
 {\nu_0\Delta(a\xi_v+b\sum_{i\in B}\xi_i)\over\|\xi\|^2}
 =\sum_{k=1}^{N-1}\pi_k{N-k\over(N+1)(N-1)}b_k.            \tag{18}
\]

The coefficient of `b_k` in (18) is

\[
 {1\over2(N+1)}
 {\binom{N-2}{k-1}\over2^{N-2}}.
\]

Consequently the source (11) is exactly `2(N+1)` times the physical output
row.  Combining the two factors proves the normalization

\[
 \boxed{
 {\mathcal R_2(E(\xi))\over\|\xi\|^2}
 ={\Phi_N(d)\over4(N+1)^2(N-1)}.}                          \tag{19}
\]

For the canonical verifier vector `xi=e_x-e_y`, whose squared norm is two,
the unnormalised value is
`mathcal R_2(E(xi))=Phi_N(d)/[2(N+1)^2(N-1)]`.

## 4. Schur reduction

Put

\[
 R_S=(I-S)^{-1},\qquad R_Q=(I-Q)^{-1},qquad
 A=R_SCR_QD.                                               \tag{20}
\]

Both inverses and `A` are entrywise nonnegative.  Let `gamma_S` be the good
part of (12), and define

\[
 h=R_Qq,\qquad
 r_0=\gamma_S-Ch,\qquad
 f_0=R_Sr_0.                                               \tag{21}
\]

Solving the bad equation first in `(I-H)u=gamma` gives

\[
 \boxed{\Phi_N(d)=\sigma(I+A)^{-1}f_0.}                    \tag{22}
\]

One factor of `A` is one complete bad-channel visit.  The remainder of the
proof supplies a positive first phase and controls every alternating
re-entry.

## 5. A bad-reward supersolution

Define

\[
 W_1=2N^2d_1,\qquad W_2=2Nd_1,\qquad
 W_k={4N(k-1)\over k}d_{k-1}\quad(3\le k\le N).             \tag{23}
\]

We claim

\[
 \boxed{(I-Q)W\ge q}\qquad(N\ge6).                         \tag{24}
\]

At `k=1`, the residual is

\[
 2(N^2-N+1)d_1>0.                                         \tag{25}
\]

At `k=2`, it is

\[
 {3N-4\over2}d_1-{7(N-2)\over3}d_2
 \ge {2(N-2)(N-6)\over3N}.                                \tag{26}
\]

For `k>=3`, the residual is

\[
 A_kd_{k-1}-B_kd_k,                                       \tag{27}
\]

where

\[
 A_k={(k-1)(3kN-2k^2-k+2)\over k^2},\qquad
 B_k={(3k+1)(N-k)\over k+1}.                               \tag{28}
\]

Using (5), the right side of (27) is at least

\[
 {2P(N,k)\over Nk^2(k+1)},                                 \tag{29}
\]

with

\[
\begin{aligned}
P(N,k)={}&2N^2k+Nk^3-8Nk^2-5Nk+2N\\
         &+4k^3+6k^2-2k-4.
\end{aligned}                                               \tag{30}
\]

Put `a=k-3` and `m=N-k`.  Then

\[
\begin{aligned}
P={}&a^4+a^3m+10a^3+5a^2m+37a^2+60a\\
   &+2am(m-1)+6m^2-22m+32.                                \tag{31}
\end{aligned}

Every term is nonnegative except that the last quadratic has not yet been
split; its discriminant is `-284`, so it is strictly positive.  Since
`a,m` are nonnegative integers, (31) proves (24).

Applying `R_Q` gives `h<=W`.  Moreover,

\[
\begin{array}{c|c}
\text{channel}&\gamma_S-CW\\ \hline
P_1&0\\
P_k&\displaystyle{k(k-1)\over k+1}d_k\quad(k\ge2)\\[1mm]
R_1&0\\
R_2&\displaystyle Nd_2+{N\over2}d_1\\[1mm]
R_k&\displaystyle Nd_k+{k-1\over k}
             \left(N+1-{2\over k}\right)d_{k-1}\quad(k\ge3).
\end{array}                                                \tag{32}
\]

Thus `r_0>=0` and

\[
 \boxed{f_0\ge0}.                                         \tag{33}
\]

## 6. A uniform re-entry contraction

The negative exit mass from every bad row is

\[
 D\mathbf1={N-1\over2N}\mathbf1,                           \tag{34}
\]

while the bad-block row sums are

\[
 (Q\mathbf1)_k={1\over2}-{1\over2kN}.                      \tag{35}
\]

Therefore `R_QD1<=1`.  Define a good vector

\[
 z(P_k)={1\over N},\qquad z(R_k)={2\over N+k}.              \tag{36}
\]

Direct substitution gives

\[
 (I-S)z\ge C\mathbf1.                                     \tag{37}
\]

The `P_k` residual after subtracting `C1` is `1/(2N^2)`.  For
the `R_k` residual, clear the positive denominator and put
`a=k-1`, `m=N-k`.  The numerator is

\[
\begin{aligned}
Z(a,m)={}&4a^4+14a^3m+18a^3+14a^2m^2+40a^2m+30a^2\\
 &+4am^3+24am^2+36am+20a\\
 &+3m^3+8m^2+9m+4>0.                                     \tag{38}
\end{aligned}

Applying `R_S` in (37) proves

\[
 \boxed{A\mathbf1\le {2\over N+1}\mathbf1.}               \tag{39}
\]

## 7. Two-sided first-phase bounds

First, `r_0<=gamma_S`.  The vector

\[
 u(P_k)=4,\qquad u(R_k)=8N                               \tag{40}
\]

is a supersolution of `(I-S)u>=gamma_S`.  On `P_k`, its
left side is `2(N+1)/N>=k d_k`.  On `R_k`, its left side is

\[
 {2(2N^2+4Nk-3N+1)\over Nk},                              \tag{41}
\]

whereas (5) gives

\[
 \gamma(R_k)\le{2(2N+1)\over k}.
\]

The difference is `2(4Nk-4N+1)/(Nk)>0`.  Hence

\[
 \boxed{0\le f_0\le8N\mathbf1.}                           \tag{42}
\]

For the lower bound, (5) gives `q_k<=2N`.  Equation (35) then implies

\[
 h=R_Qq\le4N\mathbf1.                                     \tag{43}
\]

For `N>=7`, set

\[
 \ell(P_k)=0,\qquad \ell(R_k)=2N.                          \tag{44}
\]

Then

\[
 [(I-S)\ell](R_k)=2+{N-1\over k}.                          \tag{45}
\]

At `k=1`, (5) and (43) give

\[
 r_0(R_1)\ge Nd_1-2\ge2N-6\ge N+1.
\]

For `k>=2`, they give

\[
 r_0(R_k)\ge {4N-8-4/N\over k}
 \ge2+{N-1\over k};                                      \tag{46}
\]

the last inequality is weakest at `k=N-1` and follows from
`N-5-4/N>=0`.  The `P` coordinates of `(I-S)ell` vanish and
`r_0(P)>=0`.  Applying `R_S` proves

\[
 \boxed{f_0(R_k)\ge2N,\qquad \sigma f_0\ge2N}
 \qquad(N\ge7).                                           \tag{47}
\]

## 8. Summing every re-entry

Put `c_N=2/(N+1)`.  From (39),
`A^m1<=c_N^m1`.  The Neumann series for `(I+A)^(-1)` is
absolutely convergent.  Equations (22), (42), and (47) give, for `N>=10`,

\[
\begin{aligned}
 \Phi_N(d)
 &\ge \sigma f_0-\sum_{m\ge1}\sigma A^mf_0\\
 &\ge2N-8N\sum_{m\ge1}c_N^m\\
 &=\boxed{{2N(N-9)\over N-1}}>0.                           \tag{48}
\end{aligned}
\]

The remaining orders are exact Schur computations:

\[
\begin{array}{c|c}
N&\Phi_N(d)\\ \hline
2&24/11\\
3&261/40\\
4&343400/28657\\
5&2268275/128288\\
6&5758562957/248448224\\
7&141339691089527/4988552903680\\
8&15468663676289/466560376100\\
9&19782952499295763/524622207176704.
\end{array}                                                \tag{49}
\]

Every entry is positive.  Equations (48)--(49) prove (1), and the exact
normalization (19) proves the physical standard-sector theorem.

## 9. Independent exact verification

Run

```bash
../../.venv/bin/python verify_physical_standard_phase.py
```

from this directory.  The verifier independently reconstructs:

1. the signed `P/Q/R` quotient and its good/bad blocks;
2. the radial Poisson gradient and its closed form;
3. the physical reward and the Schur identity (22);
4. the conjugacy to the physical standard two-feature system and the exact
   normalization (19);
5. every vector barrier in (23)--(47);
6. the shifted integer-polynomial certificates (31) and (38); and
7. every rational value in (49).

No sampled value of `N` is used to establish an all-order inequality.
