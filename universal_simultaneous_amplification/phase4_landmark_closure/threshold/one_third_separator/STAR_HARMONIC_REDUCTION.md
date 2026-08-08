# Arbitrary weighted stars: an exact dB correction recurrence

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Exact star equations

Let a star have hub `0`, leaves `[m]`, and positive edge weights `w_i`.
Normalize

\[
 p_i={w_i\over\sum_jw_j},\qquad p_A=\sum_{i\in A}p_i,
 \qquad k=|A|.
\]

Write `f_h(A)` for fixation when the hub has type `h` and exactly the leaves
in `A` are mutant.  Direct enumeration of the changing events at `r=3/2`
gives the Bd equations

\[
0={3k\over2}\{f_1(A)-f_0(A)\}
 +\sum_{i\in A}p_i\{f_0(A-i)-f_0(A)\},                 \tag{1}
\]

\[
0={3\over2}\sum_{j\notin A}p_j\{f_1(A+j)-f_1(A)\}
 +(m-k)\{f_0(A)-f_1(A)\},                             \tag{2}
\]

and the dB equations

\[
0={3p_A\over2+p_A}\{f_1(A)-f_0(A)\}
 +\sum_{i\in A}\{f_0(A-i)-f_0(A)\},                  \tag{3}
\]

\[
0={2(1-p_A)\over2+p_A}\{f_0(A)-f_1(A)\}
 +\sum_{j\notin A}\{f_1(A+j)-f_1(A)\}.              \tag{4}
\]

Equations (1)--(4) retain every individual leaf weight.  They are exact
harmonic equations, not a count-lumping assertion.

## 2. Unit-star tangent

Let `u_{h,k}` be the harmonic function of the unit-weight star and put

\[
 d_k=1+{k\over2m},\qquad U_k=u_{1,k}-u_{0,k},\qquad
 a_k={3U_k\over2d_k}.
\]

Multiply each dB equation by `1+p_A/2`; this is a positive statewise time
change.  With

\[
                    D_A=p_A-{k\over m},                \tag{5}
\]

direct substitution of the unit-star equations gives, for either hub type,

\[
                    \widetilde L u(A)=a_kD_A.           \tag{6}
\]

For an exact construction of `u`, define positive increments `v_k` by

\[
 {v_{k+1}\over v_k}
 ={m+1+k/2\over m+2+k/2},\qquad0\le k<m,              \tag{7}
\]

and normalize their common scale so that `u_{1,m}=1`, where

\[
 u_{0,k}={3\over2}\sum_{j=1}^kv_j,qquad
 u_{1,k}=u_{0,k}+m d_kv_k.                              \tag{8}
\]

Then `u_{0,0}=0`, equations (3)--(4) hold at `p_A=k/m`, and
`a_k=(3/2)m v_k`; in particular `a_k` is strictly decreasing.

## 3. Exact correction recurrence

Seek a corrected comparison function

\[
             F_h(A)=u_{h,k}+c_{h,k}D_A.                \tag{9}
\]

Its time-changed dB drift is `D_A B_h(p_A)`, where

\[
\begin{aligned}
B_0(t)={}&a_k+{3t\over2}(c_{1,k}-c_{0,k})\\
 &+(1+t/2)\{(k-1)c_{0,k-1}-kc_{0,k}\},               \tag{10}\\
B_1(t)={}&a_k+(1-t)(c_{0,k}-c_{1,k})\\
 &+(1+t/2)\{(m-k-1)c_{1,k+1}-(m-k)c_{1,k}\}.         \tag{11}
\end{aligned}
\]

Set `c_{0,0}=c_{1,m}=0` and solve the `2(m-1)` rational equations

\[
 B_0(k/m)=B_1(k/m)=0,\qquad1\le k<m.                  \tag{12}
\]

The two affine slopes then agree exactly:

\[
B_0'(t)=B_1'(t)
={\frac32(c_{1,k}-c_{0,k})-\frac12a_k\over d_k}.      \tag{13}
\]

Consequently

\[
 \widetilde L F_h(A)
 ={\frac32(c_{1,k}-c_{0,k})-\frac12a_k\over d_k}
 D_A^2.                                                \tag{14}
\]

If

\[
                    c_{1,k}\le c_{0,k}                \tag{15}
\]

for every interior rank, then `F` is superharmonic.  The correction vanishes
at both absorbing states, and its uniform-singleton average is zero because

\[
 {1\over m}\sum_i(p_i-1/m)=0.
\]

Optional stopping would therefore prove that every positive weighted star
has uniformly initialized dB fixation at most that of the unit star.

## 4. Exact finite verification and open sign

The companion verifier solves (12) over `QQ`.  It proves (15) for every
`2<=m<=20`: equality occurs at `m=2`, and the inequality is strict for every
interior rank when `3<=m<=20`.  It also checks (3)--(8), (10)--(14), and
all subset drifts on deterministic rational weight vectors through six
leaves.

Thus weighted-star dB maximality by the unit star is **PROVED FOR AT MOST 20
LEAVES** by this exact certificate.  The sign (15) for arbitrary `m` is
**OPEN**.  No Bd analogue with a closed recurrence was obtained, so this note
does not prove the one-third affine separator even within all weighted stars.
