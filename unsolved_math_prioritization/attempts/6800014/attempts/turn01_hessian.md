# Attempt 1: a non-solvsoliton critical family and its full Hessian

This is a substantive algebraic attempt, not a literature-retrieval turn.

The exact family tested below already appears as `D_t` in Lauret–Will I, §6.4, printed p. 20, where its value `1/3` is computed. The present calculation concerns its local behavior; the family itself is not new.

## Approach

The exceptional almost-abelian critical points identified in Lauret–Will are sums `N+C`, with `N` a nilsoliton, `C` skew-symmetric, and `[N,C]=0`. Test the smallest simple disjoint-block model

\[
A_u=J\oplus uE_{12},\qquad
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad u>0.
\]

Set `s(A)=||S(A)||²`, `q(A)=||[A,Aᵀ]||²`, and `R(A)=q(A)/s(A)²`. Since `tr A=0`,

\[
F(A)=\frac1{1+R(A)/4}.
\]

Here `s(A_u)=u²/2`, `q(A_u)=2u⁴`, and hence `R(A_u)=8`, `F(A_u)=1/3`.

## Exact second variation

For a symmetric matrix `B=(b_ij)` and `A(t)=exp(tB) A_u exp(-tB)`, direct differentiation gives `R'(0)=0` and

\[
R''(0)=\frac{64}{u^4}\left[
(4-2u^2)\big((b_{11}-b_{22})^2+4b_{12}^2\big)
+b_{13}^2+b_{14}^2+b_{23}^2+b_{24}^2
+4u(b_{13}b_{24}-b_{14}b_{23})
\right].
\]

This is positive semidefinite of rank six for `0<u<1/2`. Its kernel consists of `b11=b22`, arbitrary `b33,b34,b44`, and zero remaining off-block entries. The two mixed two-variable forms have eigenvalues `1±2u`.

Skew conjugation directions preserve the functional exactly. Because `A_u` is critical, the Hessian has zero mixed terms with those symmetry directions. Thus the calculation is compatible with a local minimum of `R`, not merely positivity on a selected subset of perturbations.

The four-dimensional symmetric-kernel preimage includes centralizer and orthogonal-orbit redundancy as well as the constant-value `u` direction. This warns against using a negative-semidefinite Hessian for `F` as a standalone maximum certificate.

## Outcome and next step

The explicit candidate is promising. A Morse–Bott argument could work after verifying the kernel equals the tangent space of the constant-value critical family, but that geometric identification is a separate obligation. Attempt 2 replaces that obligation with an explicit normal form covering every nearby conjugate and a uniform Taylor estimate.

`check_hessian.py` independently differentiates `s` and `q`, checks the displayed formula exactly, and computes the Hessian eigenvalues. The exploratory floating-point scan was only a discovery aid; all displayed claims were subsequently checked symbolically.
