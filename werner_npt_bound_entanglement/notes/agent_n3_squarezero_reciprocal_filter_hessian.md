# Reciprocal-filter Hessian at the sharp full-support frame

## Status

This note proves a local, orbit-only result for the proposed
square-zero determinant inequality.  It does **not** prove the global
inequality.

For an orthonormal four-frame
\[
 Z=(U,W)=(u_0,u_1,w_0,w_1)
 \in\operatorname{St}(4,27),\qquad U^\dagger W=0,
\]
let \(H(U,W)\) be the \(4\times4\) endpoint Gram on
\(\operatorname{Hom}(W,U)\), and let
\[
 \rho_i^U=\operatorname{Tr}_{\widehat i}UU^\dagger,\qquad
 \rho_i^W=\operatorname{Tr}_{\widehat i}WW^\dagger .
\]
On the full-local-rank locus define
\[
 {\cal R}(U,W)
 =\log\det H
 -\sum_{i=1}^3\bigl(\log\det\rho_i^U+\log\det\rho_i^W\bigr). \tag{1}
\]
The conjectured sharp determinant inequality is
\[
 {\cal R}(U,W)\geq
 \log\frac{3^{18}}{2^{22}}.                              \tag{2}
\]

We compute the exact Hessian of (1) along reciprocal local filters at
one sharp equality frame.  Put
\[
 |g_{a,b,k}\rangle
 =\frac1{\sqrt3}\sum_{j=0}^2
 \omega^{kj}|j,j+a,j+b\rangle,\qquad
 \omega^3=1,\quad \omega\ne1,                            \tag{3}
\]
with all qutrit labels read modulo three, and take
\[
\begin{aligned}
 U&=(g_{0,0,0},g_{0,0,1}),\\
 W&=(g_{1,2,2},g_{2,1,2}).                               \tag{4}
\end{aligned}
\]
Direct contraction gives
\[
 H(U,W)=\frac12I_4,\qquad
 \rho_i^U=\rho_i^W=\frac23I_3\quad(i=1,2,3),              \tag{5}
\]
so equality holds in (2).

Fix one physical site and let \(A=A^\dagger\in M_3\) be traceless.
Apply the reciprocal filter
\[
 \widetilde U(t)=e^{tA}U,\qquad
 \widetilde W(t)=e^{-tA}W,                               \tag{6}
\]
on that site, followed by independent logical whitening,
\[
\begin{aligned}
 U(t)&=\widetilde U(t)
       \bigl(\widetilde U(t)^\dagger\widetilde U(t)\bigr)^{-1/2},\\
 W(t)&=\widetilde W(t)
       \bigl(\widetilde W(t)^\dagger\widetilde W(t)\bigr)^{-1/2}.
                                                               \tag{7}
\end{aligned}
\]
Reciprocity preserves \(U(t)^\dagger W(t)=0\).  Write
\(A=A_{\rm diag}+A_{\rm off}\) in the computational basis of the
filtered qutrit.

## Theorem

At the frame (4), for a filter on any one of the three sites,
\[
\boxed{
 \frac{d}{dt}{\cal R}(U(t),W(t))\bigg|_{t=0}=0,}
                                                               \tag{8}
\]
and
\[
\boxed{
 \frac{d^2}{dt^2}{\cal R}(U(t),W(t))\bigg|_{t=0}
 =
 9\|A_{\rm diag}\|_2^2
 +\frac{104}{9}\|A_{\rm off}\|_2^2.}                    \tag{9}
\]
Thus the sharp frame is a strict local minimum of \({\cal R}\) along
every nonunitary one-site reciprocal-filter direction.  The
anti-Hermitian filter directions are common local unitaries and leave
\({\cal R}\) unchanged.

The theorem is deliberately local.  It neither shows that every
reciprocal-filter orbit contains a balanced frame nor proves convexity
of \({\cal R}\) away from (4).

## 1. Exact normalized-frame derivatives

The following formulas hold at an arbitrary orthonormal pair of
two-frames.  Suppress the identity factors on the two unfiltered
sites and put
\[
\begin{aligned}
 a&=U^\dagger AU,& b&=U^\dagger A^2U,\\
 c&=W^\dagger AW,& d&=W^\dagger A^2W.
\end{aligned}                                             \tag{10}
\]
Expanding
\[
 (U^\dagger e^{2tA}U)^{-1/2}
 =I-ta+t^2\left(\frac32a^2-b\right)+O(t^3)
\]
and its \(W\)-analogue gives
\[
\begin{aligned}
 \dot U&=AU-Ua,\\
 \ddot U&=A^2U-2AUa+U(3a^2-2b),\\
 \dot W&=-AW+Wc,\\
 \ddot W&=A^2W-2AWc+W(3c^2-2d).                          \tag{11}
\end{aligned}
\]

For \(E_{ab}=|u_a\rangle\langle w_b|\), these imply
\[
\begin{aligned}
 \dot E_{ab}
 &=|\dot u_a\rangle\langle w_b|
   +|u_a\rangle\langle\dot w_b|,\\
 \ddot E_{ab}
 &=|\ddot u_a\rangle\langle w_b|
   +2|\dot u_a\rangle\langle\dot w_b|
   +|u_a\rangle\langle\ddot w_b|.                         \tag{12}
\end{aligned}
\]
If \({\cal B}_3\) denotes the polarized endpoint form, then
\[
\begin{aligned}
 \dot H_{\mu\nu}
 &={\cal B}_3(\dot E_\mu,E_\nu)
   +{\cal B}_3(E_\mu,\dot E_\nu),\\
 \ddot H_{\mu\nu}
 &={\cal B}_3(\ddot E_\mu,E_\nu)
   +2{\cal B}_3(\dot E_\mu,\dot E_\nu)
   +{\cal B}_3(E_\mu,\ddot E_\nu).                        \tag{13}
\end{aligned}
\]
Similarly, for \(F=U,W\),
\[
\begin{aligned}
 \dot\rho_i^F
 &=\operatorname{Tr}_{\widehat i}
   (\dot F F^\dagger+F\dot F^\dagger),\\
 \ddot\rho_i^F
 &=\operatorname{Tr}_{\widehat i}
   (\ddot F F^\dagger+2\dot F\dot F^\dagger
      +F\ddot F^\dagger).                                \tag{14}
\end{aligned}
\]

For every positive definite matrix path \(M(t)\),
\[
 \frac{d^2}{dt^2}\log\det M
 =\operatorname{Tr}\left(
 M^{-1}\ddot M-M^{-1}\dot M M^{-1}\dot M\right).          \tag{15}
\]
Equations (11)--(15) are the general exact reciprocal-filter
variation requested by the determinant program.

## 2. Evaluation at the sharp frame

At (4), direct use of (13) gives
\[
 \dot H=0.                                                \tag{16}
\]
Since every marginal in (5) has fixed trace two, the first derivative
of each marginal log determinant also vanishes.  This proves (8).

For the second derivative, take the real Hermitian basis consisting
of
\[
\begin{aligned}
 X_{rs}(z)&=z|r\rangle\langle s|
            +\overline z|s\rangle\langle r|,
 \quad r<s,\quad z\in\{1,\omega\},\\
 D_1&=\operatorname{diag}(1,-1,0),\\
 D_2&=\operatorname{diag}(1,1,-2).                        \tag{17}
\end{aligned}
\]
Exact contraction in the cyclotomic field
\(\mathbb Q(\omega)\) gives, for each of the three unordered pairs
\((r,s)\),
\[
 \operatorname{Hess}{\cal R}\big|_{\{X_{rs}(1),X_{rs}(\omega)\}}
 =\frac1{9}
 \begin{pmatrix}
 208&-104\\
 -104&208
 \end{pmatrix},                                          \tag{18}
\]
while
\[
 \operatorname{Hess}{\cal R}(D_1,D_1)=18,\qquad
 \operatorname{Hess}{\cal R}(D_2,D_2)=54.                \tag{19}
\]
All other cross terms vanish.  Since
\[
\begin{aligned}
 \|X_{rs}(z)\|_2^2&=2|z|^2,\\
 \langle X_{rs}(1),X_{rs}(\omega)\rangle_{\mathbb R}
 &=2\operatorname{Re}\omega=-1,\\
 \|D_1\|_2^2&=2,\qquad \|D_2\|_2^2=6,
\end{aligned}
\]
equations (18)--(19) are exactly (9).

The dependency-free checker
`verification/verify_n3_squarezero_reciprocal_filter_hessian.py`
constructs (4), differentiates (7), evaluates (13)--(15), and checks
the full \(8\times8\) Hessian using exact arithmetic in
\(\mathbb Q(\omega)\).
