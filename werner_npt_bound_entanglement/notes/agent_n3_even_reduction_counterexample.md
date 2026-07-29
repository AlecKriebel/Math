# Exact counterexample to the uncorrected three-copy even-reduction inequality

## Status

For arbitrary rank-two coefficient matrices, the proposed cyclic
inequality
\[
 E(C):=\sum_{1\leq i<j\leq3}
 \langle C,{\cal R}_i{\cal R}_j(C)\rangle\geq0             \tag{1}
\]
is false.  A rank-two integer matrix has
\[
 \boxed{\qquad E(C)=-2.\qquad}                             \tag{2}
\]
The example nevertheless has \(Q_3(C)=0\).  It therefore exposes the
exact trace/nuclear-norm slack omitted from (1), rather than refuting
three-copy endpoint positivity.

For every rank-two \(C\), the sharp proposed three-copy estimate is
equivalent to the corrected inequality
\[
 \boxed{\qquad
 E(C)+\frac12\left[
 (s_1(C)+s_2(C))^2-|\operatorname{Tr}C|^2
 \right]\geq0.
 \qquad}                                                   \tag{3}
\]
This note proves the counterexample and the equivalence (3).  It does
not prove (3) for arbitrary rank-two matrices.

## 1. The witness

On one qutrit let
\[
 A=|0\rangle\langle1|,\qquad
 Q=|0\rangle\langle0|+|1\rangle\langle1|,
\]
and on three qutrits put
\[
 \boxed{\qquad C=A\otimes A\otimes Q.\qquad}               \tag{4}
\]
Equivalently,
\[
 C=|000\rangle\langle110|
  +|001\rangle\langle111|.                                \tag{5}
\]
Its two summands have orthogonal left vectors and orthogonal right
vectors.  Hence
\[
 \operatorname{rank}C=2,\qquad
 s_1(C)=s_2(C)=1,\qquad
 \|C\|_2^2=2,\qquad
 \operatorname{Tr}C=0.                                   \tag{6}
\]

For the qutrit reduction map
\[
 {\cal R}(X)=\operatorname{Tr}(X)I_3-X,
\]
we have
\[
 {\cal R}(A)=-A,\qquad
 \langle A,{\cal R}(A)\rangle=-1,                         \tag{7}
\]
and
\[
 {\cal R}(Q)=2I_3-Q,\qquad
 \langle Q,{\cal R}(Q)\rangle=2,\qquad
 \|Q\|_2^2=2.                                             \tag{8}
\]
The Hilbert--Schmidt form factorizes over tensor factors.  Therefore
\[
\begin{aligned}
 \langle C,{\cal R}_1{\cal R}_2(C)\rangle&=2,\\
 \langle C,{\cal R}_1{\cal R}_3(C)\rangle&=-2,\\
 \langle C,{\cal R}_2{\cal R}_3(C)\rangle&=-2.
\end{aligned}                                             \tag{9}
\]
Summing (9) proves (2).

This counterexample is genuinely nonnormal: its right singular plane
\(\operatorname{span}\{|110\rangle,|111\rangle\}\) is orthogonal to its
left singular plane
\(\operatorname{span}\{|000\rangle,|001\rangle\}\).

## 2. Why the true endpoint form is still zero

The \(n=3\) even-reduction identity is
\[
 Q_3(C)=
 \frac18\left(2\|C\|_2^2-|\operatorname{Tr}C|^2\right)
+\frac14E(C).                                             \tag{10}
\]
Substituting (2) and (6) gives
\[
 Q_3(C)=\frac18(4)+\frac14(-2)=0.                         \tag{11}
\]
Since the two singular values agree, the conjectured sharp lower bound
\(\frac18(s_1-s_2)^2\) is also zero.  Thus (4) is an equality case of
the desired theorem.

## 3. The exact slack-corrected inequality

For a rank-two matrix,
\[
 \|C\|_2^2=s_1^2+s_2^2.
\]
Subtract the conjectured sharp lower bound from (10):
\[
\begin{aligned}
 Q_3(C)-\frac18(s_1-s_2)^2
 &=
 \frac14E(C)
+\frac18\left[
 2(s_1^2+s_2^2)-|\operatorname{Tr}C|^2
 -(s_1-s_2)^2\right]\\
 &=
 \frac14\left\{
 E(C)+\frac12\left[
 (s_1+s_2)^2-|\operatorname{Tr}C|^2
 \right]\right\}.
\end{aligned}                                             \tag{12}
\]
This proves the equivalence (3).

The correction is nonnegative by
\[
 |\operatorname{Tr}C|\leq\|C\|_1=s_1+s_2.                \tag{13}
\]
For the witness (4), its global trace is zero, so the correction in
(3) equals \(2\) and cancels \(E(C)=-2\) exactly.

Consequently no proof of the sharp three-copy theorem may discard this
trace/nuclear-norm slack: a mandatory exact equality family uses all of
it.

## 4. A tensor-product equality family

Let \(A_1,A_2\) be normalized traceless rank-one matrices on the first
two local spaces and let \(H\) have rank at most two on the third.
For
\[
 C=A_1\otimes A_2\otimes H                               \tag{14}
\]
one has
\[
 E(C)=3\|H\|_2^2-2|\operatorname{Tr}H|^2,\qquad
 \operatorname{Tr}C=0.                                   \tag{15}
\]
Indeed, \({\cal R}(A_i)=-A_i\), so the three pair terms are
\[
 \|H\|_2^2,\quad
 -\bigl(|\operatorname{Tr}H|^2-\|H\|_2^2\bigr),\quad
 -\bigl(|\operatorname{Tr}H|^2-\|H\|_2^2\bigr).
\]

If the singular values of \(H\) are \(s_1,s_2\), the corrected defect
on this family is
\[
\begin{aligned}
 E(C)+\frac12(s_1+s_2)^2
 &=
 \frac32(s_1-s_2)^2
+2\left[(s_1+s_2)^2-|\operatorname{Tr}H|^2\right]\geq0.
\end{aligned}                                             \tag{16}
\]
Thus equality holds precisely when \(s_1=s_2\) and equality holds in
\(|\operatorname{Tr}H|\leq\|H\|_1\); equivalently, up to a scalar
phase, \(H\) is a scalar multiple of a rank-two orthogonal projection.
The witness (4) is the smallest integer member of this family.

## 5. Exact conclusion

What is resolved:

1. the uncorrected cyclic even-reduction conjecture (1) is false;
2. the obstruction occurs already for a two-term product singular-value
   decomposition and has the exact value \(E=-2\);
3. the omitted correction is exactly the trace/nuclear-norm slack in
   (3);
4. the counterexample saturates, rather than violates, the sharp
   three-copy endpoint conjecture.

What remains:

1. prove or refute (3) for arbitrary rank-two \(C\);
2. characterize whether every equality case is generated from the
   tensor family (14), the already known self-adjoint families, and
   their local-unitary/permutation images.

## 6. Exterior-sector form of the corrected residual

There is a compact four-party Plücker formulation of (3).  Write a
singular-value decomposition
\[
 C=\sum_{r=1}^2s_r|u_r\rangle\langle v_r|
\]
and introduce an auxiliary qubit \(K\):
\[
 |\mathsf A\rangle
 =\sum_{r=1}^2\sqrt{s_r}|r\rangle_K|u_r\rangle,\qquad
 |\mathsf B\rangle
 =\sum_{r=1}^2\sqrt{s_r}|r\rangle_K|v_r\rangle.            \tag{17}
\]
Put \(z=\mathsf A\otimes\mathsf B\).  The two auxiliary marginals
coincide and equal \(\operatorname{diag}(s_1,s_2)\).

Let \(F_K,F_1,F_2,F_3\) be the local swaps on two replicas and put
\(A_i^-=(I-F_i)/2\).  The standard factor contraction gives
\[
 \langle C,{\cal R}_i{\cal R}_j(C)\rangle
 =4\langle z,F_KA_i^-A_j^-z\rangle.                       \tag{18}
\]
Moreover,
\[
\begin{aligned}
 \|z\|^2&=(s_1+s_2)^2,\\
 \langle z,F_KF_1F_2F_3z\rangle
 &=|\langle\mathsf A,\mathsf B\rangle|^2
 =|\operatorname{Tr}C|^2.
\end{aligned}
\]
Therefore the correction in (3) is exactly the global exterior mass:
\[
 \frac12\left[(s_1+s_2)^2-|\operatorname{Tr}C|^2\right]
 =
 \left\langle z,
 \frac{I-F_KF_1F_2F_3}{2}z\right\rangle.                 \tag{19}
\]
Combining (18)--(19), the surviving theorem is equivalent to
\[
 \boxed{\quad
 \left\langle z,\left[
 4F_K\sum_{i<j}A_i^-A_j^-
 +\frac{I-F_KF_1F_2F_3}{2}
 \right]z\right\rangle\geq0,
 \quad}                                                    \tag{20}
\]
for decomposable \(z=\mathsf A\otimes\mathsf B\) whose two auxiliary
marginals agree.

If \(k\in\{0,1\}\) records whether the auxiliary pair is antisymmetric
and \(r\in\{0,1,2,3\}\) is the number of antisymmetric physical pairs,
the operator in (20) has sector eigenvalue
\[
 4(-1)^k\binom r2+\mathbf1_{\{k+r\ {\rm odd}\}}.           \tag{21}
\]
Thus its coefficient rows are
\[
\begin{array}{c|rrrr}
 &r=0&r=1&r=2&r=3\\ \hline
 k=0&0&1&4&13\\
 k=1&1&0&-3&-12 .
\end{array}                                                \tag{22}
\]
This isolates the remaining nonlinear task: the positive
auxiliary-symmetric sectors must dominate the two negative
auxiliary-antisymmetric sectors, using both decomposability and equality
of the auxiliary marginals.  Dropping the exterior correction deletes
the parity term in (21), and the witness (4) then violates the resulting
statement.
