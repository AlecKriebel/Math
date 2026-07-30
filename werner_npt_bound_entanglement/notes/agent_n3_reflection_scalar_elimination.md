# Exact scalar elimination in the three-copy reflection target

## Status

The reflection formulation of unrestricted three-copy positivity asks
for
\[
 \left\langle C,M^{\otimes3}(C)\right\rangle_{\rm HS}
 \geq-\frac13\|C\|_2^2,\qquad \operatorname{rank}C\leq2,
 \tag{1}
\]
where
\[
 M(A)=A-\frac23\operatorname{Tr}(A)I_3.
 \tag{2}
\]
This note gives a lossless dual reduction of (1).  It eliminates the
global scalar component exactly and leaves the strictly smaller
pair-sector stability inequality
\[
 \boxed{\qquad
 \|BV\|_2^2+
 \frac1{16}\left|\operatorname{Tr}(V^\dagger BV)\right|^2
 \leq\frac23\|B\|_2^2 .
 \qquad}                                                   \tag{3}
\]
Here \(B\) has exact local traceless degree two and
\(V:\mathbb C^2\to(\mathbb C^3)^{\otimes3}\) is an arbitrary
isometry.

The additional trace term in (3) is not an estimate: it is exactly the
Schur complement left by optimizing the scalar coefficient.  The note
also proves (3) when only one of the three pair components of \(B\) is
present.  The global three-component inequality remains open, so this
is a strict reduction and a positive boundary theorem, not a proof of
(1).

The dependency-free checker is
`verification/verify_n3_reflection_scalar_elimination.py`.

## 1. Reflection is the even-degree projection bound

On one qutrit operator space, \(M\) is the Hilbert--Schmidt reflection
which is \(-1\) on the scalar line and \(+1\) on the traceless
subspace.  If
\[
 C=C_0+C_1+C_2+C_3
\]
is the orthogonal decomposition by the number of traceless local
factors, put \(w_k=\|C_k\|_2^2\).  Then
\[
 \left\langle C,M^{\otimes3}(C)\right\rangle
 =-w_0+w_1-w_2+w_3
 =\|C\|_2^2-2(w_0+w_2).                                  \tag{4}
\]
Consequently (1) is exactly
\[
 \boxed{\qquad
 \|(\Pi_0+\Pi_2)C\|_2^2\leq\frac23\|C\|_2^2,
 \qquad\operatorname{rank}C\leq2 .
 \qquad}                                                   \tag{5}
\]

Let \({\cal E}=\operatorname{Ran}(\Pi_0+\Pi_2)\).  Ordinary
rank-two Hilbert-space duality makes (5) equivalent to
\[
 \boxed{\qquad
 s_1(D)^2+s_2(D)^2\leq\frac23\|D\|_2^2
 \quad(D\in{\cal E}).
 \qquad}                                                   \tag{6}
\]
For completeness, if (6) holds and \(D=(\Pi_0+\Pi_2)C\), then
\[
 \|D\|_2^2=\langle D,C\rangle
 \leq\sqrt{s_1(D)^2+s_2(D)^2}\,\|C\|_2
 \leq\sqrt{\frac23}\|D\|_2\|C\|_2.
\]
This proves (5).  Conversely, for \(D\in{\cal E}\), take \(C\) to be
the sum of its first two singular dyads.  Then
\[
 \langle D,C\rangle=\|C\|_2^2=s_1(D)^2+s_2(D)^2,
\]
and (5), followed by Cauchy--Schwarz against \(D\), proves (6).

Every \(D\in{\cal E}\) has the unique orthogonal form
\[
 D=cI_{27}+B,\qquad B\in\operatorname{Ran}\Pi_2.          \tag{7}
\]
In particular,
\[
 \operatorname{Tr}B=0,\qquad
 \|D\|_2^2=27|c|^2+\|B\|_2^2.                            \tag{8}
\]

## 2. Lossless scalar Schur complement

The Ky--Fan variational formula gives
\[
 s_1(D)^2+s_2(D)^2
 =\max_{V^\dagger V=I_2}\|DV\|_2^2.                      \tag{9}
\]
Fix \(B\) and an isometry \(V\), and put
\[
 t=\operatorname{Tr}(V^\dagger BV).
\]
Equations (7)--(8) give
\[
\begin{aligned}
 &\|(cI+B)V\|_2^2
 -\frac23\left(27|c|^2+\|B\|_2^2\right)\\
 &\qquad
 =-16|c|^2+2\operatorname{Re}(\overline c\,t)
 +\|BV\|_2^2-\frac23\|B\|_2^2.                           \tag{10}
\end{aligned}
\]
The first two terms have the exact maximum
\[
 \max_{c\in\mathbb C}
 \left[-16|c|^2+2\operatorname{Re}(\overline c\,t)\right]
 =\frac1{16}|t|^2,                                      \tag{11}
\]
attained at \(c=t/16\).

It follows from (9)--(11), in both directions, that (6) is equivalent
to (3).  Thus there is no remaining scalar variable and no loss of
sharpness.  The reflection target is precisely the assertion that the
ordinary pair-sector Ky--Fan deficit controls the square of the
two-dimensional compression trace:
\[
 \boxed{\qquad
 \frac23\|B\|_2^2-\|BV\|_2^2
 \geq
 \frac1{16}\left|\operatorname{Tr}(V^\dagger BV)\right|^2.
 \qquad}                                                   \tag{12}
\]

## 3. Exact theorem for one pair component

### Theorem

Let \(A\in M_9(\mathbb C)\) satisfy \(\operatorname{Tr}A=0\), put
\[
 B=A\otimes I_3,
\]
and let \(V:\mathbb C^2\to\mathbb C^9\otimes\mathbb C^3\) be an
isometry.  Then
\[
 \boxed{\qquad
 \|BV\|_2^2+
 \frac1{16}\left|\operatorname{Tr}(V^\dagger BV)\right|^2
 \leq2\|A\|_2^2
 =\frac23\|B\|_2^2 .
 \qquad}                                                   \tag{13}
\]

In particular, (3) holds whenever \(B\) has only one nonzero exact
pair component.  The doubly traceless condition on that component
implies the trace hypothesis on \(A\).

### Proof

Let
\[
 P=VV^\dagger,\qquad
 \rho=\operatorname{Tr}_{\mathbb C^3}P.
\]
Then
\[
 \rho\succeq0,\qquad\operatorname{Tr}\rho=2,              \tag{14}
\]
and the spectator identity gives
\[
\begin{aligned}
 \|BV\|_2^2&=\operatorname{Tr}(A^\dagger A\rho),\\
 \operatorname{Tr}(V^\dagger BV)&=\operatorname{Tr}(A\rho).
                                                               \tag{15}
\end{aligned}
\]

First take \(\rho=2|x\rangle\langle x|\), with \(\|x\|=1\).
Extend \(x\) to an orthonormal basis
\((x,e_2,\ldots,e_9)\).  Since \(\operatorname{Tr}A=0\),
\[
 \langle x,Ax\rangle
 =-\sum_{j=2}^9\langle e_j,Ae_j\rangle.
\]
Cauchy--Schwarz, followed by the diagonal-to-column estimate, gives
\[
\begin{aligned}
 |\langle x,Ax\rangle|^2
 &\leq8\sum_{j=2}^9|\langle e_j,Ae_j\rangle|^2\\
 &\leq8\sum_{j=2}^9\|Ae_j\|^2
 =8\left(\|A\|_2^2-\|Ax\|^2\right).                     \tag{16}
\end{aligned}
\]
Therefore
\[
 2\|Ax\|^2+\frac14|\langle x,Ax\rangle|^2
 \leq2\|A\|_2^2.                                        \tag{17}
\]

For general \(\rho\) in (14), write
\[
 \frac{\rho}{2}
 =\sum_\alpha p_\alpha|x_\alpha\rangle\langle x_\alpha|
\]
as a convex combination of pure states.  Equations (15), Jensen's
inequality for the squared modulus, and (17) give
\[
\begin{aligned}
 &\operatorname{Tr}(A^\dagger A\rho)
 +\frac1{16}|\operatorname{Tr}(A\rho)|^2\\
 &\quad
 =2\sum_\alpha p_\alpha\|Ax_\alpha\|^2
 +\frac14\left|
       \sum_\alpha p_\alpha\langle x_\alpha,Ax_\alpha\rangle
       \right|^2\\
 &\quad
 \leq\sum_\alpha p_\alpha
 \left(
 2\|Ax_\alpha\|^2
 +\frac14|\langle x_\alpha,Ax_\alpha\rangle|^2
 \right)\\
 &\quad\leq2\|A\|_2^2.
\end{aligned}                                             \tag{18}
\]
This proves (13). \(\square\)

The constant \(1/16\) in this proof is the reciprocal of twice the
eight-dimensional orthogonal complement in (16).  It is exactly the
same constant forced globally by the scalar Schur complement (11);
it was not chosen after the fact.

## 4. Remaining exact lemma

Write the general pair-sector operator as
\[
 B=I_1\otimes B_{23}
  +I_2\otimes B_{13}
  +I_3\otimes B_{12},                                    \tag{19}
\]
with each \(B_{ij}\) traceless on both of its qutrit factors.  The
reflection formulation, and hence the corresponding map-collapse
route to unrestricted three-copy positivity, is now exactly (3), or
\[
\boxed{
\begin{aligned}
 &\left\|
 \left(
 I_1\otimes B_{23}
 +I_2\otimes B_{13}
 +I_3\otimes B_{12}
 \right)V
 \right\|_2^2\\
 &\quad+
 \frac1{16}\left|
 \operatorname{Tr}\left[
 V^\dagger
 \left(
 I_1\otimes B_{23}
 +I_2\otimes B_{13}
 +I_3\otimes B_{12}
 \right)V
 \right]\right|^2\\
 &\qquad\leq
 2\left(
 \|B_{23}\|_2^2+\|B_{13}\|_2^2+\|B_{12}\|_2^2
 \right).
\end{aligned}}                                           \tag{20}
\]
The one-component theorem proves every coordinate axis of this
three-component inequality.  A complete proof must control the
common cyclic interference of the three \(B_{ij}V\) together with the
single coherent trace in (20).  Bounding those four contributions
independently would discard exactly the shared qutrit geometry.
