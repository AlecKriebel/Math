# Quotient criticality excludes the opposite-tilt obstruction

## Exact reduction

The rank-two path in
`agent_n3_pair_centered_7over3_tilt_nogo.md` disproves the universal
coefficient-\(7/3\) purity inequality.  It does **not** survive the
quotient Euler equations.

Retain
\[
\begin{aligned}
 u_0&=|000\rangle+|101\rangle+|202\rangle,\\
 u_1&=|010\rangle+|111\rangle+|212\rangle,\qquad
 x=|021\rangle,\\
 C(t)&=\frac13\left[
 (u_0+tx)(u_0-tx)^\dagger+u_1u_1^\dagger
 \right].
\end{aligned}
\]
Put
\[
 q(t)=Q_3(C(t)),\qquad
 D(t)=\Pi_2C(t),\qquad c(t)=\|D(t)\|_2^2,
\]
and clear the quotient denominator:
\[
 S(t)=c(t)L^{\otimes3}(C(t))-q(t)D(t).                 \tag{1}
\]
If \(C(t)\) were quotient-critical, its left and right factor frames
would obey
\[
 (u_0+tx)^\dagger S(t)=0,\qquad
 S(t)(u_0-tx)=0.                                       \tag{2}
\]

Exact contraction with the single leakage vector \(x\) gives
\[
\boxed{
\begin{aligned}
 \langle u_0+tx,S(t)x\rangle
 &=\frac{-56t-4t^3+2t^5}{81},\\
 \langle x,S(t)(u_0-tx)\rangle
 &=\frac{56t+4t^3-2t^5}{81}.
\end{aligned}
}                                                       \tag{3}
\]
In particular, the opposite tilt leaves the critical locus
transversely, with nonzero linear Euler coefficient \(-56/81\).
This is the smallest first-order condition which excludes the exact
quartic no-go.

## Quotient-Hessian decomposition

At \(t=0\), write \(C_0=C(0)\) and
\[
\begin{aligned}
 D_L&=\frac13xu_0^\dagger,\\
 D_R&=\frac13u_0x^\dagger,\\
 T&=D_L-D_R,\qquad
 N=-\frac13xx^\dagger.
\end{aligned}
\]
Then
\[
 C(t)=C_0+tT+t^2N.
\]
Since \(q(0)=0\), the shifted quotient operator at the base is simply
\({\cal W}=L^{\otimes3}\), with normal residual
\(R={\cal W}C_0\).  Exact evaluation gives
\[
\begin{aligned}
 \langle D_L,{\cal W}D_L\rangle
 &=\langle D_R,{\cal W}D_R\rangle=\frac29,\\
 \langle D_L,{\cal W}D_R\rangle&=0,\\
 \langle R,N\rangle&=-\frac1{36}.
\end{aligned}                                           \tag{4}
\]
Therefore the constrained quotient Hessian along this path is
\[
\boxed{
 \langle T,{\cal W}T\rangle+2\operatorname{Re}\langle R,N\rangle
 =\frac49-\frac1{18}
 =\frac7{18}>0.
}                                                       \tag{5}
\]
Indeed
\[
 Q_3(C(t))=\frac7{18}t^2+\frac1{72}t^4.
\]
Thus the negative curvature of the repaired purity deficit occurs in
a direction which is strictly positive for the quotient itself.

## Smallest live critical Hessian

For a genuine quotient minimizer, put
\[
 \lambda=\frac{Q_3(C)}{\|\Pi_2C\|^2},\qquad
 {\cal W}_\lambda=L^{\otimes3}-\lambda\Pi_2,\qquad
 R={\cal W}_\lambda C.
\]
Criticality says \(R\) is in the normal block.  For coherent left and
right graph motions \(D_L,D_R\), with their common normal second
fundamental form \(N\), the zero-compatible condition is
\[
\boxed{
\langle D_L-D_R,{\cal W}_\lambda(D_L-D_R)\rangle
+2\operatorname{Re}\langle R,N\rangle\geq0.
}                                                       \tag{6}
\]
Allowing independent complex amplitudes gives the sharper
phase-optimized \(2\times2\) determinant form: if
\[
\begin{aligned}
 A&=\langle D_L,{\cal W}_\lambda D_L\rangle,\\
 B&=\langle D_R,{\cal W}_\lambda D_R\rangle,\\
 p&=\langle D_L,{\cal W}_\lambda D_R\rangle,\qquad
 r=\langle R,N\rangle,
\end{aligned}
\]
then
\[
\boxed{(|p|+|r|)^2\leq AB.}                            \tag{7}
\]
Unlike a sum of six separate pair-centered purities, (6)--(7) retain
the coherent left--right cross term and the normal residual pairing.
They also hold at the flag--Bell zero.

The remaining strictly smaller problem is to fuse (7), \(q<0\), and
the common pair-sector geometry into the desired global inequality.
The exact tilt computation proves that omitting either criticality or
the normal pairing admits false boundary continuations.

The formulas are checked using rational arithmetic by
`verification/verify_n3_pair_centered_tilt_critical_exclusion.py`.
