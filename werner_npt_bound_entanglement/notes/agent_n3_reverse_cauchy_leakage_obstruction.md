# The reverse-Cauchy defect is not determined by the critical Hessian

## Status

At a hypothetical negative determinant-normalized three-copy
minimizer, the two singular rank-one components have a strict
reverse-Cauchy defect.  The complete Hessian supplies, for every
paired left/right plane leakage, the sharp budget
\[
 (|p|+|q|)^2\leq AB.
\]
It is tempting to try to identify the reverse-Cauchy scalar with
\(p+q\).  This note gives an exact obstruction: even for a
self-adjoint quadratic form which is uniformly positive on every
rank-one matrix, has a negative global determinant-normalized
rank-two minimizer, and satisfies all of the corresponding critical
and Hessian equations, the reverse-Cauchy scalar can be nonzero while
\(p=q=0\) for every leakage pair.

Thus no such identification follows from block positivity,
determinant criticality, or the complete second variation alone.  A
successful argument must use the explicit three-fold partial-trace
structure of \(L^{\otimes3}\).

## 1. An exact abstract model

Let \(N\geq3\), let \(P\) be a rank-two orthogonal projection in
\(\mathbb C^N\), and define the self-adjoint superoperator
\[
 {\cal S}(D)=D-\frac34\operatorname{Tr}(PD)P.
\tag{1}
\]
Its quadratic form is
\[
 {\cal Q}(D)=\|D\|_2^2-\frac34|\operatorname{Tr}(PD)|^2.
\tag{2}
\]

### Proposition 1.1

The form (2) has all of the following properties.

1. Every rank-one matrix obeys
   \[
   {\cal Q}(uv^\dagger)\geq
   \frac14\|u\|^2\|v\|^2.
   \tag{3}
   \]
2. On the rank-two determinant slice
   \[
   \delta(D)=s_1(D)s_2(D)=1,
   \tag{4}
   \]
   the global minimum of \({\cal Q}\) is \(-1\), attained at \(D=P\).
3. At \(C=P\), the critical multiplier is
   \[
   \lambda=\frac12{\cal Q}(P)=-\frac12,
   \qquad {\cal S}(P)=\lambda P.
   \tag{5}
   \]
   In particular the normal residual is zero.
4. If
   \[
   P=e_1e_1^\dagger+e_2e_2^\dagger,
   \qquad C_i=e_ie_i^\dagger,
   \tag{6}
   \]
   then the singular-component data are
   \[
   a={\cal Q}(C_1)=\frac14,\qquad
   b={\cal Q}(C_2)=\frac14,\qquad
   c=\langle C_1,{\cal S}(C_2)\rangle=-\frac34.
   \tag{7}
   \]
   Hence
   \[
   |c|^2-ab=\frac12>0.
   \tag{8}
   \]
5. For every pair of left/right leakage velocities \(X,Z\),
   the complete-Hessian quantities satisfy
   \[
   p=q=0.
   \tag{9}
   \]

### Proof

For \(D=uv^\dagger\),
\[
 |\operatorname{Tr}(PD)|
 =|v^\dagger Pu|
 \leq\|u\|\,\|v\|,
\]
which proves (3).

Now let \(D\) have rank two, singular values \(s_1,s_2\), and
\(s_1s_2=1\).  Von Neumann's trace inequality gives
\[
 |\operatorname{Tr}(PD)|\leq s_1+s_2.
\tag{10}
\]
Therefore
\[
\begin{aligned}
 {\cal Q}(D)
 &\geq s_1^2+s_2^2-\frac34(s_1+s_2)^2\\
 &=\frac14(s_1^2+s_2^2)-\frac32\\
 &\geq-1.
\end{aligned}
\tag{11}
\]
Equality is attained by \(D=P\).  Direct substitution gives
\[
 {\cal Q}(P)=2-\frac34(2)^2=-1,\qquad
 {\cal S}(P)=P-\frac32P=-\frac12P,
\]
which proves (5).  Equations (7)--(8) are equally direct.

Write \(\mathbb C^N=P\mathbb C^N\oplus P^\perp\mathbb C^N\).
At \(C=P\), \(\Sigma=I_2\).  A left leakage \(D_X\) lies in the
lower-left block and a right leakage \(D_Z\) lies in the upper-right
block.  Both have zero \(P\)-trace, so
\[
 {\cal S}(D_X)=D_X,\qquad {\cal S}(D_Z)=D_Z.
\tag{12}
\]
The two blocks are Hilbert--Schmidt orthogonal, and the normal
residual in (5) is zero.  Consequently
\[
 p=\langle D_X,{\cal S}(D_Z)\rangle=0,\qquad
 q=0
\]
for every \(X,Z\).  This proves the proposition. \(\square\)

## 2. Exact obstruction

The model proves that there is no universal consequence of the form
\[
 |c|\leq |p|+|q|
\tag{13}
\]
for some leakage pair, even after imposing:

- a strict positive rank-one floor;
- existence of a negative global minimizer on \(\delta=1\);
- the reciprocal-singular Euler--Lagrange equation;
- the complete determinant-constrained Hessian;
- vanishing normal residual.

Indeed, (7) gives \(|c|=3/4\), whereas (9) makes the right-hand side
of (13) zero for every leakage pair.

This is not a counterexample to the physical Werner endpoint:
\({\cal S}\) is not asserted to equal \(L^{\otimes3}\).  It is an
exact counterexample to a proposed proof mechanism which uses only
the abstract critical and Hessian data.

## 3. The smallest sufficient physical bridge

Return to a hypothetical negative critical point of the physical
form.  To avoid conflicting notation, write
\[
 a_0=Q_3(C_1),\qquad b_0=Q_3(C_2),\qquad
 c_0=\langle C_1,L^{\otimes3}(C_2)\rangle.
\tag{14}
\]
The critical equations give
\[
 |c_0|^2>a_0b_0.
\tag{15}
\]
For leakage directions \(X,Z\), put
\[
\begin{aligned}
 A_X&=Q_3(D_X)-\lambda\|X\|^2,\\
 B_Z&=Q_3(D_Z)-\lambda\|Z\|^2,\\
 p_{X,Z}&=\langle D_X,L^{\otimes3}(D_Z)\rangle,\\
 q_{X,Z}&=\langle R,U_\perp X\Sigma ZV_\perp^\dagger\rangle.
\end{aligned}
\tag{16}
\]
The Hessian says
\[
 (|p_{X,Z}|+|q_{X,Z}|)^2\leq A_XB_Z.
\tag{17}
\]

Consequently, the following explicit tensor bridge would finish the
three-copy theorem:
\[
\boxed{
 \text{there exist }X,Z\text{ such that}\qquad
 \frac{|p_{X,Z}|+|q_{X,Z}|}{\sqrt{A_XB_Z}}
 \geq
 \frac{|c_0|}{\sqrt{a_0b_0}}.
}
\tag{18}
\]
The right-hand side is strictly greater than one by (15), whereas
the left-hand side is at most one by (17).

A stronger but sometimes easier sufficient pair of inequalities is
\[
 |p_{X,Z}|+|q_{X,Z}|\geq|c_0|,
 \qquad
 A_XB_Z\leq a_0b_0.
\tag{19}
\]

The abstract model shows that (18) cannot follow merely from
criticality.  The remaining task is precisely to derive (18), or a
weaker contradiction with (15), from the tensor-product
partial-trace identities specific to \(L^{\otimes3}\).  This is a
strictly smaller target than classifying all nonnormal rank-two
matrices: it compares one core reverse-Cauchy ratio with one
explicitly optimized normal-curvature ratio.
