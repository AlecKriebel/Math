# The coefficient-\(7/3\) pair-centered repair is also false

## Status correction

The flag--Bell obstruction in
`agent_n3_pair_centered_purity_nogo.md` suggested the repaired
inequality
\[
 {\cal X}(C)\stackrel{?}{\geq}
 \frac73c^2-\frac12Q_3(C)c,                            \tag{1}
\]
where
\[
\begin{aligned}
 D&=\Pi_2C,\qquad c=\|D\|_2^2,\\
 {\cal X}(C)
 &=\sum_{i=1}^3\sum_{\bullet=L,R}\|X_i^\bullet\|_2^2,\\
 X_i^L&=\operatorname{Herm}\operatorname{Tr}_{\widehat i}
 (CD^\dagger),\\
 X_i^R&=\operatorname{Herm}\operatorname{Tr}_{\widehat i}
 (D^\dagger C).
\end{aligned}
\]

Equation (1) is false for rank-two matrices.  This note supersedes
the “live candidate” status of equation (24) in the earlier note.
The obstruction lies on the \(Q_3>0\) side, so it does not disprove a
strictly-negative, quotient-critical refinement.

## Exact opposite-tilt family

Use the unnormalized vectors
\[
\begin{aligned}
 u_0&=|000\rangle+|101\rangle+|202\rangle,\\
 u_1&=|010\rangle+|111\rangle+|212\rangle,\\
 x&=|021\rangle.
\end{aligned}
\]
The flag--Bell zero is
\[
 C(0)=\frac13(u_0u_0^\dagger+u_1u_1^\dagger).
\]
Tilt its left and right logical-zero columns in opposite directions:
\[
\boxed{
 C(t)=\frac13\left[
 (u_0+tx)(u_0-tx)^\dagger+u_1u_1^\dagger
 \right].
}                                                        \tag{2}
\]
The displayed two-column factorization proves
\(\operatorname{rank}C(t)\leq2\) for every \(t\).

Let
\[
 \Delta_{7/3}(C)
 ={\cal X}(C)-\frac73c^2+\frac12Q_3(C)c.
\]
Exact expansion gives
\[
\boxed{
\begin{aligned}
 \Delta_{7/3}(C(t))
 ={}&
 -\frac8{2187}t^2
 -\frac{118}{19683}t^4\\
 &+\frac{952}{19683}t^6
 +\frac{731}{78732}t^8.
\end{aligned}
}                                                        \tag{3}
\]
Thus the constrained second variation is already negative.  In the
two one-sided tangent coordinates, the diagonal curvatures are both
\(32/729\), while their coherent cross curvature is \(100/2187\).
The opposite-tilt eigenvector has curvature
\[
 2\left(\frac{32}{729}-\frac{100}{2187}\right)
 =-\frac8{2187}.
\]

At the rational value \(t=1/2\),
\[
\begin{aligned}
 Q_3(C(t))&=\frac{113}{1152}>0,\\
 c&=\frac{401}{324},\\
 {\cal X}(C(t))&=\frac{61463}{17496},\\
 \Delta_{7/3}(C(t))
 &=-\frac{10021}{20155392}<0.
\end{aligned}
\]
These claims are checked using exact rational arithmetic by
`verification/verify_n3_pair_centered_7over3_tilt_nogo.py`.

## Consequence

Neither coefficient \(3\) nor its sharp-at-the-flag--Bell-zero
replacement \(7/3\) yields a universal quartic separator.  The
failure of (1) is specifically a common-code, nonnormal left--right
interaction: each one-sided curvature is positive, but their
coherent cross term is larger.

The remaining viable target must use information absent from (1),
most naturally both
\[
 Q_3(C)<0
\quad\text{and}\quad
 (L^{\otimes3}-\lambda\Pi_2)C
 \in U^\perp\otimes V^\perp.
\]
In particular, a critical Hessian inequality must include the normal
second-fundamental-form pairing and vanish on the flag--Bell orbit;
separate left and right purity bounds cannot do this.
