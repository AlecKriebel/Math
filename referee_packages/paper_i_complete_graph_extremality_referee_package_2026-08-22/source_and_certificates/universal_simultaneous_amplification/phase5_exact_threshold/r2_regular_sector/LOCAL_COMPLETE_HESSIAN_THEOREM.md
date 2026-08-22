# Exact local theorem in the regular fitness-two sector

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

**PROVED, with an exact symbolic certificate.**  Let

\[
 \mathcal P_n=\{P=P^{\mathsf T}:P_{ii}=0,\ P_{ij}\geq 0,
                    \ \sum_jP_{ij}=1\}
\]

be the polytope of symmetric stochastic loopless kernels, and let
\(\Phi_n(P)\) be death--Birth fixation probability at fitness \(r=2\),
averaged uniformly over singleton initial mutants.  Write \(J_n\) for the
complete kernel, \((J_n)_{ij}=1/(n-1)\) for \(i\ne j\).

> **Theorem.**  For every \(n\geq4\) and every nonzero symmetric matrix
> \(\Delta\) with zero diagonal and zero row sums,
> \[
> \left.\frac{d}{d\epsilon}\Phi_n(J_n+\epsilon\Delta)\right|_{\epsilon=0}=0,
> \qquad
> \left.\frac{d^2}{d\epsilon^2}\Phi_n(J_n+\epsilon\Delta)
> \right|_{\epsilon=0}<0.
> \]
> Consequently, \(J_n\) is a strict local maximizer of \(\Phi_n\) inside
> \(\mathcal P_n\).

This proves the all-\(n\) local transposition curvature statement at the
complete kernel.  It does **not** prove concavity along an entire
transposition orbit, the global transposition-midpoint inequality, or any
claim for nonregular weighted graphs.

## 1. Generator and complete-chain data

The harmless common death-rate factor \(1/n\) is suppressed.  For a mutant
set \(S\), put \(x_v=P_{vS}\) and

\[
 h(x)=\frac{2x}{1+x}.
\]

A resident target \(v\notin S\) becomes mutant at rate \(h(x_v)\); a mutant
target \(v\in S\) becomes resident at rate \(1-h(x_v)\).  At \(J_n\), the
rank process has per-target rates

\[
 a_k=\frac{2k}{n-1+k},\qquad b_k=\frac{n-k}{n+k-2}.
\]

Let \(\varphi_k\) denote complete-graph fixation from rank \(k\), and put

\[
 \rho=\varphi_1=\frac{(n-1)2^{n-2}}{n(2^{n-1}-1)}.
\]

Direct substitution in the one-dimensional harmonic recurrence gives

\[
 d_k:=\varphi_{k+1}-\varphi_k
 =\rho\frac{n+k-1}{(n-1)2^k},\qquad 0\leq k\leq n-1.
\]

The expected total time \(w_k\) spent at rank \(k\), starting from a uniform
singleton, is

\[
 w_k=\rho\frac{(n+k)-n2^{k+1-n}}{k(n-k)},\qquad1\leq k\leq n-1.
\]

Indeed, with
\(U_k=2k(n-k)/(n-1+k)\) and
\(D_k=k(n-k)/(n+k-2)\), these numbers satisfy the exact current equations

\[
 w_kU_k-w_{k+1}D_{k+1}=\rho.
\]

## 2. The first derivative is one killed cut mode

For a fixed tangent \(\Delta\), define

\[
 y_v(S)=\sum_{u\in S}\Delta_{vu},\qquad
 q(S)=\sum_{v\notin S}y_v(S),\qquad
 E=\sum_{i<j}\Delta_{ij}^2.
\]

Zero row sums imply \(\sum_{v\in S}y_v=-q(S)\).  Differentiating the
generator once and using the displayed complete increments gives, for
\(|S|=k\),

\[
 L'\varphi(S)=-f_kq(S),\qquad
 f_k=\rho\frac{2(n-1)(n+k)}{2^k(n+k-1)(n+k-2)}>0.
\]

Adding a vertex \(v\notin S\) changes \(q\) to \(q-2y_v\), while removing
\(v\in S\) changes it to \(q+2y_v\).  It follows exactly, without an
approximation, that the first committor derivative is

\[
 h_1(S)=-v_kq(S),
\]

where \(v_1=v_{n-1}=0\), and, for \(2\leq k\leq n-2\),

\[
 \begin{split}
 (-A v)_k={}&[a_k(n-k)+b_kk]v_k\\
 &-a_k(n-k-2)v_{k+1}-b_k(k-2)v_{k-1}=f_k. \tag{2.1}
 \end{split}
\]

The diagonal minus the sum of the absolute off-diagonal entries in row \(k\)
is \(2(a_k+b_k)>0\).  Thus \(-A\) is a nonsingular M-matrix and
\(v_k>0\).

For singleton sets, \(q=0\).  This proves the vanishing of the first
derivative in the theorem.

## 3. Exact Hessian reduction

Uniform averaging over the \(k\)-subsets gives the elementary identities

\[
 \begin{aligned}
 Q_k&:=\frac{\mathbb E_kq(S)^2}{E}
 =\frac{4k(k-1)(n-k)(n-k-1)}{n(n-1)(n-2)(n-3)},\\
 O_k&:=\frac{\mathbb E_k\sum_{v\notin S}y_v(S)^2}{E}
 =\frac{2k(n-k)(n-k-1)}{n(n-1)(n-2)},\\
 I_k&:=\frac{\mathbb E_k\sum_{v\in S}y_v(S)^2}{E}
 =\frac{2k(k-1)(n-k)}{n(n-1)(n-2)}.
 \end{aligned} \tag{3.1}
\]

Put

\[
 p_k=\frac{2(n-1)^2}{(n-1+k)^2},\qquad
 r_k=\frac{2(n-1)^2}{(n+k-2)^2}.
\]

Since \(h''(x)=-4/(1+x)^3\), the direct second-order term divided by \(E\)
is \(-\mathcal D\), where

\[
 \mathcal D=\sum_{k=1}^{n-1}\mathcal D_k,
\]

\[
 \mathcal D_k=w_k\left[
 \frac{4(n-1)^3d_kO_k}{(n-1+k)^3}
 +\frac{4(n-1)^3d_{k-1}I_k}{(n+k-2)^3}
 \right]>0. \tag{3.2}
\]

Differentiating the committor as well as the rates gives the response term

\[
 \frac{2\langle w,L'h_1\rangle}{E}=\sum_{j=2}^{n-2}\ell_jv_j, \tag{3.3}
\]

with

\[
 \begin{split}
 \ell_j=2\{&w_j(p_j+r_j)Q_j\\
 &+w_{j-1}p_{j-1}[-Q_{j-1}+2O_{j-1}]\\
 &+w_{j+1}r_{j+1}[-Q_{j+1}+2I_{j+1}]\}. \tag{3.4}
 \end{split}
\]

Every \(\ell_j\) is strictly positive.  One transparent check is

\[
 -Q_t+2O_t=\frac{4t(n-t)(n-t-1)(n-t-2)}
 {n(n-1)(n-2)(n-3)}\geq0,
\]

\[
 -Q_t+2I_t=\frac{4t(t-1)(n-t)(t-2)}
 {n(n-1)(n-2)(n-3)}\geq0,
\]

on the indices in (3.4), while the first term there is positive.  Therefore

\[
 \frac{\Phi_n''(J_n;\Delta)}E=-\mathcal D+sum_{j=2}^{n-2}\ell_jv_j. \tag{3.5}
\]

## 4. An all-rank supersolution

Define

\[
 \bar v_k=\frac{21}{20}\frac{n+k}{4n-2k}f_k,
 \qquad2\leq k\leq n-2,
\]

and set the irrelevant boundary values \(\bar v_1=\bar v_{n-1}=0\).  On
writing \(a=k-2\), \(b=n-k-2\), exact expansion gives

\[
 [(-A)\bar v-f]_k=
 \frac{(a+b+3)P(a,b)}{
 80\,2^a(a+2b+5)(a+2b+6)(a+2b+7)(2a+b+3)
 (2a+b+4)^2(2a+b+5)^2(2a+b+6)}, \tag{4.1}
\]

where \(P\) has 45 monomials and every coefficient is a strictly positive
integer.  The exact expansion is generated and checked by
`verify_local_complete_hessian.py`; its smallest coefficient is 16.  Hence
\((-A)\bar v>f\), and M-matrix comparison gives

\[
 0<v_k<\bar v_k. \tag{4.2}
\]

## 5. Closing the sign for every population size

For \(n=6,7,8\), exact rational evaluation of (3.2)--(3.4) gives

\[
 \frac{\sum_j\ell_j\bar v_j}{\mathcal D}=
 \begin{cases}
 265019/275520,&n=6,\\
 32970550983/36455056000,&n=7,\\
 383371803381/446439422000,&n=8.
 \end{cases} \tag{5.1}
\]

All three ratios are strictly below one.

For \(n\geq9\), a pointwise comparison is available:

\[
 \ell_k\bar v_k<\mathcal D_{k-1},
 \qquad2\leq k\leq n-2. \tag{5.2}
\]

Here is the exact positivity certificate.  Put

\[
 q=2^{k-n},\quad
 A_0=kn-3k+n^2-3n+3,
\]

\[
 B_0=k^2+2kn-6k+n^2-4n+5,
\]

\[
 C_j=j^3+3j^2n-3j^2+3jn^2-10jn+6j+n^3-7n^2+12n-6,
 \quad j=k-1.
\]

After cancelling positive factors, (5.2) is equivalent to \(H(q)>0\), where

\[
\begin{split}
H(q)={}&20(n+k-1-nq)C_{k-1}(2n-k)(n-3)(n+k-1)^2\\
&-21n(n-1)(n+k)^2(A_0-qB_0)(n+k-3)^2. \tag{5.3}
\end{split}
\]

Set \(a=k-2\), \(b=n-k-2\).  Then \(a,b\geq0\), \(a+b\geq5\), and
\(q=2^{-b-2}\).  Write \(H(q)=H_0+qH_1\).

* For each \(b=0,1,2,3,4\), substitute \(a=c+5-b\).  The resulting
  polynomial in \(c\) has nine strictly positive rational coefficients.  The
  smallest coefficient is respectively \(784,696,652,630,619\).
* For \(b\geq5\), substitute \(b=c+5\).  Both
  \(H_0(a,c+5)\) and \(128H_0(a,c+5)+H_1(a,c+5)\) have 45 strictly positive
  integer coefficients; their smallest coefficients are 19 and 2413.
  Since \(q\leq1/128\), these two certificates imply \(H(q)>0\), whether
  \(H_1\) is positive or negative at the point.

Thus (5.2) holds.  Summing it leaves two unused positive direct terms:

\[
 \sum_{k=2}^{n-2}\ell_k\bar v_k
 <\sum_{j=1}^{n-3}\mathcal D_j<\mathcal D. \tag{5.4}
\]

Combining (4.2), positivity of the \(\ell_k\), and (5.1) or (5.4) proves
strict negativity in (3.5) for every \(n\geq6\).

For the two remaining sizes, exact solution of (2.1) and substitution in
(3.5) gives

\[
 \frac{\Phi_4''(J_4;\Delta)}E=-\frac{27}{637},\qquad
 \frac{\Phi_5''(J_5;\Delta)}E=-\frac{367616}{7498125}. \tag{5.5}
\]

This completes the theorem.

## 6. Independent checks and hostile boundary

Two exact implementations check different objects.

1. `verify_local_complete_hessian.py` checks the rank/cut proof above using
   exact rational arithmetic and expands every polynomial certificate over
   the integers.
2. `derive_complete_hessian.py` independently builds the exact lumped subset
   chain for the four-cycle direction
   \(\Delta_{02}=\Delta_{13}=1\),
   \(\Delta_{03}=\Delta_{12}=-1\), differentiates the absorbing equations
   twice over \(\mathbb Q\), and agrees with (3.5).  This direction has
   \(E=4\).

The proof uses permutation symmetry only at the complete kernel.  At a
general regular midpoint, the committor is not a rank function, the first
derivative is not a single cut mode, and the response operator need not have
the positive one-dimensional coefficients (3.4).  Therefore no global
midpoint or concavity conclusion is licensed by this theorem.
