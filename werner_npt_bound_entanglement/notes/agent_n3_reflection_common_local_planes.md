# The reflection bound on tensor products of local two-planes

## Status

This note proves the corrected three-copy reflection inequality on the
complete tensor-product support boundary.  It also identifies the exact
mechanism behind the large numerical equality manifold.

Let
\[
 {\mathfrak r}(A)=A-\frac23\operatorname{Tr}(A)I_3 .
 \tag{1}
\]
If a coefficient matrix \(C\) has its row and column spaces contained
in tensor products of (not necessarily equal) local subspaces of
dimension at most two, then
\[
 \boxed{\qquad
 \langle C,{\mathfrak r}^{\otimes3}(C)\rangle_{\rm HS}
 \frac13\|C\|_2^2\geq0 .
 \qquad}
 \tag{2}
\]
No rank assumption on \(C\) is needed in this theorem.

Equivalently, if \(w_k\) denotes the squared norm of the component with
exactly \(k\) traceless qutrit factors, then
\[
 w_0+w_2\leq\frac23\|C\|_2^2.
 \tag{3}
\]

Equality is completely classified by the compressed local trace
directions.  In particular, when the row and column support at every
site is the same two-plane, equality consists of the components having
one local scalar factor and two local traceless factors.  The rank-two
matrix
\[
 C=
 (|0\rangle\langle0|+|1\rangle\langle1|)
 \otimes|0\rangle\langle1|
 \otimes|0\rangle\langle1|
 \tag{4}
\]
is an explicit equality point.

The result explains why unrestricted descent for the reflection
functional repeatedly reaches \(-1/3\) on local-support boundary
planes.  It does not exclude a full-qutrit-support violation, so the
unrestricted reflection inequality remains open.

The dependency-free exact checker is
`verification/verify_n3_reflection_common_local_planes.py`.

## 1. Precise support hypothesis

For \(i=1,2,3\), let
\[
 E_i,F_i\subseteq\mathbb C^3,\qquad
 p_i=\dim E_i\leq2,\quad q_i=\dim F_i\leq2.
 \tag{5}
\]
Choose isometries
\[
 U_i:\mathbb C^{p_i}\longrightarrow\mathbb C^3,\qquad
 V_i:\mathbb C^{q_i}\longrightarrow\mathbb C^3
 \tag{6}
\]
with ranges \(E_i,F_i\).  The hypothesis is
\[
 C=(U_1\otimes U_2\otimes U_3)\,
 C_0\,
 (V_1\otimes V_2\otimes V_3)^\dagger
 \tag{7}
\]
for some
\[
 C_0\in
 \bigotimes_{i=1}^3 M_{p_i\times q_i}(\mathbb C).
 \tag{8}
\]
Thus the left and right support planes may differ at every site.

## 2. The compressed one-site reflection

Fix one site and omit its index.  Put
\[
 J(A)=UAV^\dagger,\qquad M=V^\dagger U.
 \tag{9}
\]
For \(A,B\in M_{p\times q}\), direct contraction gives
\[
\begin{aligned}
 \langle J(A),{\mathfrak r}(J(B))\rangle_{\rm HS}
 &=
 \operatorname{Tr}(A^\dagger B)
 -\frac23\,
 \overline{\operatorname{Tr}(MA)}
 \operatorname{Tr}(MB).
\end{aligned}
 \tag{10}
\]
Consequently the compressed Hermitian form is represented on
\(M_{p\times q}\) by
\[
 K_M=I-\frac23|m\rangle\langle m|,
 \tag{11}
\]
where \(m\) is the Riesz vector of the functional
\(A\mapsto\operatorname{Tr}(MA)\).  Its squared norm is
\[
 \|m\|^2=\|M\|_2^2.
 \tag{12}
\]
The spectrum is therefore
\[
 \operatorname{spec}K_M
 =
 \left\{
 1\ \text{with multiplicity }pq-1,\quad
 \kappa_M:=1-\frac23\|M\|_2^2
 \right\},
 \tag{13}
\]
with the evident deletion of the first part if \(pq=1\).

Since \(M=V^\dagger U\) is a contraction,
\[
 0\leq\|M\|_2^2\leq\min(p,q)\leq2.
 \tag{14}
\]
It follows that
\[
 \boxed{\qquad -\frac13\leq\kappa_M\leq1.\qquad}
 \tag{15}
\]
Moreover,
\[
 \kappa_M=-\frac13
 \quad\Longleftrightarrow\quad
 p=q=2,\ \|V^\dagger U\|_2^2=2
 \quad\Longleftrightarrow\quad E=F.
 \tag{16}
\]
The last equivalence follows because both singular values of the
two-by-two contraction \(V^\dagger U\) must equal one.

## 3. Tensor-product proof

Applying (10) independently at the three sites shows that the
restriction of the quadratic form
\({\mathfrak r}^{\otimes3}\) to the supported operator space (8) is
represented by
\[
 K_{M_1}\otimes K_{M_2}\otimes K_{M_3},
 \qquad M_i=V_i^\dagger U_i.
 \tag{17}
\]
Every eigenvalue of (17) is a product of three numbers, each of which
is either \(1\) or one of the \(\kappa_{M_i}\in[-1/3,1]\).

If such a product is negative, it contains an odd number of negative
factors.  With one negative factor its modulus is at most \(1/3\);
with three negative factors its modulus is at most \(1/27\).  Hence
every eigenvalue of (17) is at least \(-1/3\).  This proves (2).

Because \({\mathfrak r}\) is \(-1\) on the scalar qutrit direction and
\(+1\) on the traceless directions,
\[
 \langle C,{\mathfrak r}^{\otimes3}(C)\rangle
 =\|C\|_2^2-2(w_0+w_2).
 \tag{18}
\]
Thus (2) and (3) are equivalent.

## 4. Equality classification

Let
\[
 {\cal T}_i=\ker\!\left[A\mapsto\operatorname{Tr}(M_iA)\right],
 \qquad
 {\cal S}_i={\cal T}_i^\perp.
 \tag{19}
\]
The local form \(K_{M_i}\) is \(1\) on \({\cal T}_i\) and
\(\kappa_{M_i}\) on the at-most-one-dimensional space
\({\cal S}_i\).  The eigenspace of (17) at \(-1/3\) is therefore the
orthogonal direct sum, over sites \(i\) satisfying \(E_i=F_i\), of
\[
 {\cal S}_i\otimes{\cal T}_j\otimes{\cal T}_k,
 \qquad \{i,j,k\}=\{1,2,3\}.
 \tag{20}
\]
Indeed, equality requires exactly one factor equal to \(-1/3\) and
the other two factors equal to \(1\); three negative factors have
product at least \(-1/27\).

When all \(E_i=F_i\) are common two-planes, \(M_i\) is unitary.  After
using compatible coordinates, \({\cal S}_i\) is the scalar direction
and \({\cal T}_i\) is the traceless \(2\times2\) operator space.
Thus (20) says exactly: one local scalar factor and two local
traceless factors.

For (4), the first factor is scalar on the common two-plane and the
last two factors are traceless.  Its ordinary matrix rank is
\[
 2\cdot1\cdot1=2,
 \tag{21}
\]
and (17) gives
\[
 \langle C,{\mathfrak r}^{\otimes3}(C)\rangle
 =-\frac13\|C\|_2^2.
 \tag{22}
\]

## 5. Remaining frontier

The theorem settles the entire tensor-product local-support boundary,
including the observed equality manifold, but it does not provide a
dimension reduction.  A hypothetical strict violation must escape
the support hypothesis (7); in particular the common numerical
boundary mechanism cannot yield one.

The unrestricted problem remains equivalently the scalar-eliminated
three-component inequality
\[
\begin{aligned}
 &\left\|
 \left(
 I_1\otimes B_{23}
 +I_2\otimes B_{13}
 +I_3\otimes B_{12}
 \right)V
 \right\|_2^2\\
 &\quad+\frac1{16}
 \left|
 \operatorname{Tr}V^\dagger
 \left(
 I_1\otimes B_{23}
 +I_2\otimes B_{13}
 +I_3\otimes B_{12}
 \right)V
 \right|^2\\
 &\qquad\leq
 2\sum_{i<j}\|B_{ij}\|_2^2.
 \tag{23}
\end{aligned}
\]
The new equality classification says that any proof by critical-point
reduction must either force the maximizing code onto (7), or establish
a strict gap in the genuinely full-qutrit-support interior.
