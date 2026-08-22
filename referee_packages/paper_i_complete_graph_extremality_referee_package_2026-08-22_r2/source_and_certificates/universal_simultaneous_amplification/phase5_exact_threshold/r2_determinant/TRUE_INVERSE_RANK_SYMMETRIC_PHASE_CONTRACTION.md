# A phase contraction for the stationary symmetric inverse-rank response

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

This note closes the **stationary symmetric row-zero irreducible sector** of
the fitness-two complete-refresh Hessian.

> **Theorem.**  For every `N>=3`, the stationary symmetric-sector
> inverse-rank response of the complete active chain is strictly positive.

The theorem is exact.  Together with the antisymmetric theorem in
`FIXED_COUNT_TWO_REPLICA.md` and the standard theorem in
`TRUE_INVERSE_RANK_PHASE_CONTRACTION.md`, it closes all three nonradial
irreducible sectors of the **stationary Hessian**.

It does **not** prove finite-time positivity in the standard or symmetric
sector, any fixed-count coefficient with three or more perturbation colours,
or the global fitness-two inequality `F0`.

## 1. The exact two-channel scalar

Put `n=N+1`.  For a symmetric row-zero perturbation `delta`, use the features

\[
 x(B,v)=\sum_{i\in B}\delta_{vi},\qquad
 z(B)=\sum_{w\ne i\in B}\delta_{wi}.
\]

Write a sector function as `a_k x+b_k z`, with `1<=k<N` in the `a`
channel and `2<=k<N` in the `b` channel.  Equations (27)--(29) of
`FIXED_COUNT_TWO_REPLICA.md` give a signed rank operator `K` and a positive
source

\[
 s^a_k={d_k\over2},\qquad s^b_k={d_{k-1}\over2k}.             \tag{1}
\]

The radial differences satisfy

\[
 (N-k)d_k-(k-1)d_{k-1}
 =2N\left({1\over k}-c_0\right),\qquad
 c_0={2^N-1\over N2^{N-1}},                                  \tag{2}
\]

with `d_0=d_N=0`.

The averaged second perturbation in equation (31) has good and bad rewards

\[
 g^a_k=\omega_k
 ={\binom{N-2}{k-1}\over2^{N-1}(N+1)},                       \tag{3}
\]

and, for `2<=k<N`,

\[
 g^b_k=-q_k,qquad
 q_k={\binom{N-3}{k-2}\over2^{N-2}(N+1)}.                    \tag{4}
\]

Thus the desired scalar is

\[
 \mathcal S_N=g^T(I-K)^{-1}s
 =s^T(I-K^T)^{-1}g.                                          \tag{5}
\]

Transpose `K` and split it into good and bad channels:

\[
 H=K^T=\begin{pmatrix}S&C\\-D&Q\end{pmatrix}.               \tag{6}
\]

All four displayed blocks are entrywise nonnegative.  The nonzero entries
needed below are

\[
\begin{aligned}
 S_{k,k}&={k\over2N},&S_{k,k-1}&={N-k\over2N},\\
 Q_{k,k}&={N(k-2)+k\over2kN},
 &Q_{k,k-1}&={N-k-1\over2N},\\
 Q_{k,k+1}&={k(k-1)\over2(k+1)N},
 &D_{k,k-1}&={1\over N},                                    \tag{7}
\end{aligned}
\]

and

\[
 C_{k-1,k}={k-1\over2kN},\qquad
 C_{k,k}={N-k\over2kN}.                                     \tag{8}
\]

Absent boundary entries are zero.

## 2. Schur elimination and the re-entry phase

Let

\[
 R_S=(I-S)^{-1},\qquad R_Q=(I-Q)^{-1}.                        \tag{9}
\]

Both are entrywise nonnegative.  Define

\[
\begin{aligned}
 W&=R_Qq,&r&=g^a-CW,&f_0&=R_Sr,\\
 A&=R_SCR_QD,&
 \ell&=s^a-s^bR_QD,&
 \mathcal D&=s^bW.                                          \tag{10}
\end{aligned}
\]

Solving the bad equation first and substituting it into the good equation
gives the exact identity

\[
 \boxed{\mathcal S_N
 =\ell(I+A)^{-1}f_0-\mathcal D.}                              \tag{11}
\]

One factor of the nonnegative matrix `A` is one completed visit to the bad
channel.  The inverse in (11) alternates the signs of successive re-entries;
the proof below controls its entire tail rather than only the first visit.

## 3. Radial and binomial preliminaries

Put `e_k=2/k-d_k`.  Solving (2) gives

\[
 e_k=
 {2^{2-N}\displaystyle\sum_{r=k}^{N-1}\binom{N-1}{r}
  \over
  (N-1)\binom{N-2}{k-1}}.                                   \tag{12}
\]

In particular,

\[
 {2(N-2)\over Nk}\le d_k\le{2\over k}.                      \tag{13}
\]

For completeness, the upper bound is immediate from (12).  For the lower
bound it is enough to prove

\[
 Nk\sum_{r=k}^{N-1}\binom{N-1}{r}
 \le2^N(N-1)\binom{N-2}{k-1}.                               \tag{14}
\]

If `k<=N/2`, use the full binomial sum and
`binom(N-2,k-1)>=N-2` away from `k=1`; the endpoint is immediate.  If
`k>N/2`, put `m=N-1-k` and use

\[
 \sum_{r=k}^{N-1}\binom{N-1}{r}
 =\sum_{j=0}^m\binom{N-1}{j}
 \le(N-k){N-1\over k}\binom{N-2}{k-1},                      \tag{15}
\]

together with `N(N-k)<=2^N`.  The finitely smallest values are direct.

Let

\[
 v=R_Sg^a,qquad v_k=t_k\omega_k.                            \tag{16}
\]

The lower-bidiagonal good block makes the ratios independent of the
binomial normalization:

\[
 t_1={2N\over2N-1},\qquad
 t_k={2N+(k-1)t_{k-1}\over2N-k}.                             \tag{17}
\]

They obey the exact upper barrier

\[
 t_k\le {N^2-k\over(N-2)(N-k)}.                              \tag{18}
\]

The base difference is `(5N-1)/[(N-2)(2N-1)]`.  Under one recurrence
step, after putting `m=N-k`, the numerator left over is

\[
 N^3-N^2+2Nm^2+2Nm+2m^3+3m^2+m>0,                           \tag{19}
\]

which proves (18) by induction.

## 4. Three positive barriers

### 4.1 The bad reward debt

For `N>=24` set

\[
 \overline W={7N\over25}q.                                  \tag{20}
\]

Then

\[
 (I-Q)\overline W\ge q,\qquad
 C\overline W\le{14\over25}g^a.                             \tag{21}
\]

The second inequality follows because each of the two terms in a row of
`Cq`, after multiplication by `7N/25`, is at most `7/25` of `omega_k`.

For the first inequality, clearing the positive binomial factors leaves

\[
\begin{aligned}
 P_N(k)={}&21N^2k+14N^2-64Nk^2-57Nk\\
          &+50k^3+36k^2-14k.                                \tag{22}
\end{aligned}
\]

For `N>=25`,

\[
 \operatorname{disc}_kP_N=-8B_N,                             \tag{23}
\]

where `B_(25+M)` has coefficients

\[
 (5733,736211,37934833,982793213,
 12893444604,70866894144,41021531998).                        \tag{24}
\]

Hence `B_N>0`, so `P_N` has one real root.  Since its leading coefficient
and `P_N(0)=14N^2` are positive, that root is negative and `P_N(k)>0` for
`k>=0`.  At `N=24`, the exact minimum over `2<=k<N` is `24`.

Applying the positive inverse `R_Q` in (21) gives `W<=overline W`.  Therefore

\[
 {11\over25}v\le f_0\le v.                                  \tag{25}
\]

### 4.2 A complete bad-phase contraction

Define, for `2<=k<N`,

\[
 \widehat h_k={k\over N-2}\omega_{k-1}.                     \tag{26}
\]

Equations (7) and (18) give

\[
 (I-Q)\widehat h\ge Dv.                                     \tag{27}
\]

Indeed, at an interior rank the left side divided by `omega_(k-1)` is

\[
 {N^2-k+1\over N(N-2)(N-k+1)},                               \tag{28}
\]

and the two boundary expressions are still larger.  On the other hand,

\[
 C\widehat h\le c_Ng^a,qquad
 c_N={2N-5\over2N(N-2)}.                                    \tag{29}
\]

The maximum in (29) is the rank `N-2` ratio.  Consequently

\[
 \boxed{Av\le c_Nv},\qquad c_N\le{1\over12}\quad(N\ge12).   \tag{30}
\]

### 4.3 The left occupation debt

For `2<=k<N` put

\[
 Y_k={2(k+1)\over3k(k-1)}.                                   \tag{31}
\]

A direct substitution gives, at an interior rank,

\[
 [(I-B)Y]_k-{1\over k(k-1)}
 ={4Nk+2N+2k^3-k^2-5k
   \over3Nk^2(k-1)(k+1)}>0,                                  \tag{32}
\]

where `B=Q^T`; the boundary residuals are positive as well.  By (13),
`s^b_k<=1/[k(k-1)]`.  Hence

\[
 y:=s^bR_Q\le Y.                                             \tag{33}
\]

It follows that `ell>=bar ell>0`, where

\[
 \overline\ell_j
 ={3Nj+3N-8j-10\over3Nj(j+1)}.                               \tag{34}
\]

The top rank has an additional positive margin because there is no bad
state above it.

## 5. The scalar debt comparison

The bad debt is bounded term by term as

\[
 \mathcal D=yq\le Yq
 =\sum_{j=1}^{N-2}
 {4(j+2)\over3(j+1)(N-2)}\,\omega_j.                         \tag{35}
\]

Meanwhile (25), (34), and (16) give the first-phase lower bound

\[
 \ell f_0\ge {11\over25}
 \sum_{j=1}^{N-1}\overline\ell_jt_j\omega_j.                \tag{36}
\]

For `40<=N<=287`, exact rational recurrence (17) verifies

\[
 \beta_N+\varepsilon_N<1,                                   \tag{37}
\]

where

\[
\begin{aligned}
 \beta_N&=\max_{1\le j\le N-2}
 {4(j+2)\over3(j+1)(N-2)}
 \left({11\over25}\overline\ell_jt_j\right)^{-1},\\
 \varepsilon_N&={25\over11}{c_N\over1-c_N}.                 \tag{38}
\end{aligned}
\]

The smallest exact margin in this finite interval is the first one,

\[
 1-\beta_{40}-\varepsilon_{40}
 ={639304267467075678841\over115369588296792467144716}>0.    \tag{39}
\]

This is a finite exact certificate, not a numerical screen.

For all larger orders there is a short analytic certificate.  Put
`r=sqrt(N/2)`.  Induction in (17) gives

\[
 t_j\ge {N\over N-j+r}.                                      \tag{40}
\]

Indeed, substituting the proposed lower barrier leaves
`2r(N-j+r)+r-N`, whose minimum occurs at `j=N-1` and equals `3r`.
For `N>=288`, `r<=N/24`, so

\[
 t_j\ge{24N\over25N-24j}.                                   \tag{41}
\]

The termwise bound `beta_N<=19/20` is equivalent to

\[
 {24N\over25N-24j}
 \ge {2000Nj(j+2)\over
 209(N-2)\{3N(j+1)-8j-10\}}.                                \tag{42}
\]

After clearing positive denominators, (42) is the positivity of

\[
\begin{aligned}
 G_N(j)={}&1881N^2j+1881N^2-6250Nj^2-21278Nj-10032N\\
          &+6000j^3+12000j^2+10032j+12540.                   \tag{43}
\end{aligned}
\]

Its discriminant is `-500D_N`, and `D_(288+M)` has coefficients

\[
\begin{gathered}
 43034652243, 71940715263252, 50075984929826764,\\
 18577025353519361184, 3873653773133773223808,\\
 430447522448513182675968,
 19913301794000751100222464.                                 \tag{44}
\end{gathered}
\]

Thus `G_N` has one real root.  Its leading coefficient and `G_N(0)` are
positive, so the root is negative and (42) holds strictly for `j>=0`.
Also

\[
 \varepsilon_N\le{1\over20}\qquad(N\ge46).                  \tag{45}
\]

Equations (42) and (45) prove (37) for every `N>=288`.

## 6. Completion of the all-reentry sign

By (25), (30), and positivity of `ell`,

\[
\begin{aligned}
 \left|\ell(I+A)^{-1}f_0-\ell f_0\right|
 &\le\sum_{m\ge1}\ell A^mv\\
 &\le {c_N\over1-c_N}\ell v\\
 &\le\varepsilon_N\ell f_0.                                \tag{46}
\end{aligned}
\]

Equation (35) gives `mathcal D<=beta_N ell f_0`.  Therefore (11) and
(37) imply

\[
 \mathcal S_N
 \ge(1-\beta_N-\varepsilon_N)\ell f_0>0                     \tag{47}
\]

for every `N>=40`.

For `3<=N<=39`, the verifier constructs the exact matrix in (5) and solves
it over the rationals.  Every value is positive; the first two are

\[
 \mathcal S_3={3\over208},\qquad
 \mathcal S_4={359\over26660}.                               \tag{48}
\]

This completes the theorem for every population order.

## 7. Independent verification and remaining gap

Run

```bash
../../.venv/bin/python verify_true_inverse_rank_symmetric_phase.py
```

from this directory.  The verifier independently:

1. rebuilds the signed two-channel rank system;
2. checks the Schur identity (11) against direct exact solves;
3. checks (12)--(34) with exact arithmetic;
4. directly solves `3<=N<=39`;
5. verifies every rational margin in `40<=N<=287`; and
6. reconstructs both discriminants and their shifted positive coefficients.

The result closes the stationary quadratic symmetric sector.  The following
remain open:

- finite-time standard and symmetric fixed-count-two coefficients;
- every fixed-count coefficient of order at least three;
- the full stationary determinant/collision sign `F0`; and
- the universal fitness-two upper bound.
