# A phase contraction for the stationary standard inverse-rank response

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

This note closes the **stationary standard irreducible sector** of the
fitness-two complete-refresh Hessian.  It does not prove the symmetric
sector, the finite-time standard coefficient, or the global fitness-two
inequality.

The result is exact.

> **Theorem.**  For every `N>=2`, the stationary standard-sector
> inverse-rank response of the complete active chain is strictly positive.

The proof uses the signed two-label quotient from
`FIRST_Q_EXCURSION_BUDGET.md`, but it does not assume positivity of any
marked-cache PGF coefficient.  That stronger assertion is false.  Instead,
one complete bad-channel excursion is treated as a phase, and all repeated
re-entries are bounded by an explicit positive phase majorant.

## 1. The exact signed scalar

Order the good channels as

\[
 {cal S}=(P_1,\ldots,P_{N-1},R_1,\ldots,R_{N-1})
\]

and the bad channel as

\[
 {cal Q}=(Q_1,\ldots,Q_N).
\]

The exact two-label quotient has block form

\[
 H=\begin{pmatrix}S&C\\-D&Q\end{pmatrix},                    \tag{1}
\]

where all four blocks are entrywise nonnegative.  Their entries are the
ones in equations (2)--(4) of `FIRST_Q_EXCURSION_BUDGET.md`.  The binomial
source is

\[
 s(R_k)={\binom{N-2}{k-1}\over2^{N-2}},\qquad s(P_k)=0.       \tag{2}
\]

Combining the Hausdorff atoms with weights `1/[j(j+1)]` gives the true
inverse-rank reward.  On the good channel,

\[
\begin{aligned}
 g(P_k)&={1\over k(k+1)},\\
 g(R_1)&={N\over2},\\
 g(R_k)&={N\over k^2(k+1)}+{N+1\over(k-1)k^2}\quad(k\ge2).
                                                               \tag{3}
\end{aligned}
\]

Write `g(Q_k)=-q_k`.  Then

\[
 q_1={N-1\over2},\qquad
 q_k={2(N+1)k+1-k^2\over(k-1)k^2(k+1)}\quad(k\ge2).           \tag{4}
\]

The stationary standard response, up to the positive normalization in the
standard embedding, is

\[
 \mathcal R_N=s(I-H)^{-1}g.                                  \tag{5}
\]

Thus the theorem is the strict sign `mathcal R_N>0`.

## 2. The inverse-rank coboundary

Define a debt on the bad channel by

\[
 W_1=N^2,\qquad W_k={2N\over k(k-1)}\quad(2\le k\le N),       \tag{6}
\]

and put `f=0` on the good channel and `f=-W` on the bad channel.
Direct substitution in (1), (3), and (4) gives

\[
 \widetilde g=g+Hf-f\ge0.                                    \tag{7}
\]

More precisely,

\[
\begin{array}{c|c}
\text{channel}&\widetilde g\\ \hline
P_k&0\\
R_1&0\\
R_k&\displaystyle {2N\over(k-1)k(k+1)}\quad(k\ge2)\\
Q_1&N^2-N+1\\
Q_k&\displaystyle {N-1\over k(k-1)}\quad(k\ge2).
\end{array}                                                    \tag{8}
\]

This proves positivity for one phase, but not for arbitrary re-entry,
because the exit block in (1) carries a minus sign.

Put

\[
 R_S=(I-S)^{-1},\qquad R_Q=(I-Q)^{-1}.                         \tag{9}
\]

Both inverses are entrywise nonnegative.  Let `r^S,r^Q` be the good and bad
parts in (8), and define

\[
 h=R_Qr^Q,qquad
 \bar g=r^S+Ch,qquad
 f_0=R_S\bar g,qquad
 A=R_SC R_QD.                                                  \tag{10}
\]

The identity behind (8) is

\[
 (I-Q)W=q+r^Q.
\]

Consequently

\[
 r^Q\le h\le W,                                               \tag{11}
\]

because `R_Q=I+Q+Q^2+...` and `W-h=R_Qq`.

Schur elimination of the bad block in `I-H` gives the exact all-reentry
formula

\[
 \boxed{\mathcal R_N=s(I+A)^{-1}f_0.}                          \tag{12}
\]

This is the key change from a first-excursion argument: every completed bad
excursion is one factor of the nonnegative operator `A`, and its sign is
recorded by the alternating resolvent `(I+A)^{-1}`.

## 3. An explicit phase majorant

For `1<=k<N`, define

\[
 V_1=N,\qquad
 V_k={4N\over k^2}+{2\over N}\quad(k\ge2),                    \tag{13}
\]

and put

\[
 v(P_k)=v(R_k)=V_k.                                            \tag{14}
\]

On the bad channel use

\[
 \widehat V_k=V_k\quad(k<N),\qquad
 \widehat V_N=V_{N-1}.                                        \tag{15}
\]

The following three estimates are the phase certificate.

### Lemma 1: bad-phase bound

For every `N>=4`,

\[
 \boxed{R_QDv\le{6\over5}\widehat V.}                         \tag{16}
\]

Indeed,

\[
 {6\over5}(I-Q)\widehat V-Dv\ge0                             \tag{17}
\]

entrywise, so (16) follows by applying the positive inverse `R_Q`.

### Lemma 2: good-phase bound

For every `N>=3`,

\[
 \boxed{R_SC\widehat V\le{2\over N+1}v.}                      \tag{18}
\]

To see the structure, write `z=R_SC\widehat V`.  The `P` subsystem is
upper bidiagonal and obeys

\[
 (2N-k)z(P_k)-(N-k-1)z(P_{k+1})=\widehat V_{k+1}.              \tag{19}
\]

Backward induction, using `V_(k+1)<=V_k`, gives

\[
 z(P_k)\le {V_k\over N+1}.                                    \tag{20}
\]

Substituting (20) in the `R` subsystem, the vector
`2V_k/(N+1)` is an entrywise supersolution.  Applying the positive inverse
of the `R` block proves (18).

Combining (16) and (18) yields

\[
 \boxed{Av\le c_Nv,\qquad c_N={12\over5(N+1)}.}                \tag{21}
\]

### Lemma 3: first-phase sandwich

For every `N>=3`,

\[
 \boxed{0<f_0\le v,\qquad f_0(R_k)\ge {V_k\over3}.}            \tag{22}
\]

For the upper bound, (11) gives `h<=W`.  The `P` recurrence and
`W_(k+1)<=V_k` imply

\[
 f_0(P_k)\le {V_k\over N+1}.                                  \tag{23}
\]

Using (23), `h<=W`, and the exact positive good residual in (8), the vector
`V_k` is a supersolution of the `R` subsystem.  This gives `f_0<=v`.

For the lower bound, use `h>=r^Q`, set the proposed `P` lower bound to zero,
and set the `R` lower bound to `V_k/3`.  Direct substitution makes this an
entrywise subsolution.  Positivity of the `R`-block inverse gives the second
inequality in (22).

## 4. Exact polynomial certificates

Only four local rational inequalities occur in Lemmas 1--3.  The boundary
ranks `k=1,2` reduce to the positive expressions in the following table.

\[
\begin{array}{c|c|c}
\text{certificate}&k=1&k=2\\ \hline
\text{bad phase}
&\displaystyle {N^3+11N^2-12N+12\over10N^2}
&\displaystyle {13N^3+4N^2+6N+78\over30N^2}\\[3mm]
\text{good phase}
&\displaystyle {N^2-2N+4\over N^2(N+1)}
&\displaystyle {10N^3-3N^2+81\over18N^2(N+1)}\\[3mm]
\text{first-phase upper}
&\displaystyle {N+2\over N^2(N+1)}
&\displaystyle {7N^4-14N^3+15N^2+72N+108\over36N^2(N+1)}\\[3mm]
\text{first-phase lower}
&\displaystyle {2N^3-4N^2+5N-4\over6N^2}
&\displaystyle {34N^3+33N^2-63N-144\over216N^2}.
\end{array}                                                     \tag{24}
\]

All are strictly positive for the physical ranges (the bad-phase `k=2`
entry in this table is used for `N>=4`).  The penultimate bad rank
`Q_(N-1)` has the separate boundary expression

\[
 {3N^5-16N^4+26N^3-20N^2-3N-2
  \over5N^2(N-2)(N-1)^3}.                                    \tag{25}
\]

For `N>=4`, its numerator becomes, on writing `N=m+4`,

\[
 3m^5+44m^4+250m^3+676m^2+829m+306>0.
\]

The exceptional `N=3` penultimate value is `131/90>0`.  At the bad-channel
top rank `Q_N`, the remaining boundary expression is

\[
 {(N+2)(N+3)(3N^2-2N+1)\over5N^3(N-1)^2}>0.                  \tag{26}
\]

For `k>=3`, put

\[
 a=k-3,\qquad b=N-k-1.
\]

Thus `a,b>=0`.  After clearing the positive denominators, the four interior
numerators are the following polynomials.  Every displayed coefficient is
positive.

\[
\begin{aligned}
P_Q={}&3a^7+7a^6b+68a^6+6a^5b^2+149a^5b+674a^5\\
&+2a^4b^3+140a^4b^2+1349a^4b+3776a^4\\
&+50a^3b^3+1180a^3b^2+6545a^3b+12817a^3\\
&+328a^2b^3+4610a^2b^2+17662a^2b+26034a^2\\
&+820ab^3+8436ab^2+24720ab+28768a\\
&+696b^3+5784b^2+13728b+12960,                              \tag{27}
\end{aligned}
\]

\[
\begin{aligned}
P_G={}&2a^6+4a^5b+35a^5+8a^4b^2+62a^4b+245a^4\\
&+4a^3b^3+98a^3b^2+372a^3b+861a^3\\
&+34a^2b^3+439a^2b^2+1068a^2b+1538a^2\\
&+94ab^3+848ab^2+1440ab+1184a\\
&+84b^3+592b^2+704b+160,                                    \tag{28}
\end{aligned}
\]

\[
\begin{aligned}
P_U={}&3a^7+8a^6b+68a^6+13a^5b^2+154a^5b+641a^5\\
&+12a^4b^3+213a^4b^2+1193a^4b+3218a^4\\
&+4a^3b^4+151a^3b^3+1347a^3b^2+4675a^3b+9080a^3\\
&+34a^2b^4+685a^2b^3+4047a^2b^2+9414a^2b+13668a^2\\
&+92ab^4+1304ab^3+5600ab^2+8352ab+8608a\\
&+76b^4+844b^3+2640b^2+1504b+64,                            \tag{29}
\end{aligned}
\]

and

\[
\begin{aligned}
P_L={}&2a^6+14a^5b+65a^5+8a^4b^2+274a^4b+772a^4\\
&+139a^3b^2+2133a^3b+4557a^3\\
&+12a^2b^3+877a^2b^2+8267a^2b+14480a^2\\
&+80ab^3+2408ab^2+15976ab+23824a\\
&+136b^3+2448b^2+12336b+16000.                              \tag{30}
\end{aligned}
\]

Their exact positive denominators are

\[
\begin{array}{c|c}
P_Q&5(a+2)(a+3)^3(a+4)^2(a+b+4)^2\\
P_G&(a+2)(a+3)^3(a+4)^2(a+b+4)^2(a+b+5)/2\\
P_U&(a+2)(a+3)^3(a+4)^2(a+b+4)^2(a+b+5)\\
P_L&6(a+2)(a+3)^3(a+4)^2(a+b+4)^2.
\end{array}                                                     \tag{31}
\]

Here `P_Q` certifies (17) for `3<=k<=N-2`, `P_G` certifies the `R` supersolution in
Lemma 2, and `P_U,P_L` certify the upper and lower `R` comparisons in
Lemma 3.  Equations (24)--(31) are a coefficientwise exact certificate;
no sampled value of `N` or `k` is used.

## 5. Summing every re-entry

For `N>=9`, (21) gives `c_N<1`.  Since `A,f_0,v,s` are nonnegative,

\[
 A^mf_0\le c_N^m v.                                             \tag{32}
\]

The Neumann series for (12) is absolutely dominated by the right-hand
side of (31).  Therefore

\[
\begin{aligned}
\mathcal R_N
&\ge sf_0-\sum_{m\ge1}sA^mf_0\\
&\ge {1\over3}sv-{c_N\over1-c_N}sv\\
&={5N-43\over3(5N-7)}sv>0.                                   \tag{33}
\end{aligned}
\]

This bound groups all possible numbers and durations of bad-channel
re-entries.  It is the missing phase/age debt absent from the one-excursion
budget.

For `2<=N<=8`, direct exact Schur elimination gives

\[
\begin{array}{c|c}
N&\mathcal R_N\\ \hline
2&12/11\\
3&81/40\\
4&212530/85971\\
5&2934635/1154592\\
6&278688977/116460105\\
7&16076420403337/7482829355520\\
8&5269741961413/2799362256600.
\end{array}                                                     \tag{34}
\]

Every entry is strictly positive.  Equations (33)--(34) prove the theorem.

## 6. What this closes, and what remains

The result proves the stationary inverse-rank sign in every standard
irreducible direction at the complete kernel.  Together with the existing
antisymmetric theorem, two of the three nonradial Hessian sectors are now
closed at stationarity.

It does **not** prove:

1. positivity at every finite time or every fixed-count coefficient;
2. the stationary symmetric irreducible sector;
3. positivity of every higher complete-refresh forest coefficient;
4. the universal fitness-two obstruction for arbitrary weighted graphs.

The independent verifier reconstructs the signed quotient, the
inverse-rank reward, the coboundary, every symbolic coefficient certificate,
the phase inequalities, and all seven exact small-`N` Schur complements.
