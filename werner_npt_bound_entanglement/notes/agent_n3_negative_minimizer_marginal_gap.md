# Quantitative marginal gap at a negative three-copy minimizer

## Status

This note proves an exact necessary condition for an unrestricted
qutrit three-copy counterexample.  It does **not** prove that such a
counterexample exists.

If a normalized rank-at-most-two matrix is a global minimizer of
\(Q_3\) with value
\[
 q=-\delta<0,
\]
then all six one-site densities of its left and right singular
geometry are quantitatively positive:
\[
 \boxed{\qquad
 \rho_i^L,\rho_i^R
 \succeq
 \frac{\delta}{1+2\delta}I_3
 \qquad(i=1,2,3).
 \qquad}                                                   \tag{1}
\]
The proof uses only:

1. global minimality on the rank-two determinantal variety;
2. the established one-sided local-support boundary theorem;
3. the exact spectral upper bound
   \(L^{\otimes3}\preceq I\).

Thus any negative witness gives a negative minimizer which is
uniformly separated from the complete local-support boundary.  This
complements the sitewise strict Haar theorem: at fixed negative depth,
neither the marginal gap nor the Haar slack can collapse to zero.

## 1. Critical compression

Let
\[
 {\cal L}(A)=A-\frac12\operatorname{Tr}(A)I_3
\]
and normalize a rank-at-most-two matrix \(C\) by
\(\|C\|_2=1\).  Suppose
\[
 Q_3(C)=\langle C,{\cal L}^{\otimes3}(C)\rangle
 =q=-\delta<0                                             \tag{2}
\]
is the global minimum over normalized rank-at-most-two matrices.

Fix a physical site \(i\).  For local matrices \(A,B\in M_3\), define
\[
 G_i^L(A,B)
 =
 \left\langle A^{(i)}C,
 \bigl({\cal L}^{\otimes3}-qI\bigr)
 \bigl(B^{(i)}C\bigr)\right\rangle .                      \tag{3}
\]
Every \(A^{(i)}C\) still has matrix rank at most two.  Global
minimality therefore gives
\[
 G_i^L(A,A)\geq0
 \qquad(A\in M_3).                                       \tag{4}
\]
Moreover \(G_i^L(I,I)=0\).  A positive semidefinite Hermitian form
vanishes against every vector at a kernel vector, so
\[
 G_i^L(A,I)=0
 \qquad(A\in M_3).                                       \tag{5}
\]

Let
\[
 \rho_i^L=\operatorname{Tr}_{\widehat i}(CC^\dagger).
                                                               \tag{6}
\]
It has trace one.  For a unit vector \(z\), put
\[
 P=|z\rangle\langle z|,\qquad A=I-P,\qquad
 r=\langle z,\rho_i^Lz\rangle.                            \tag{7}
\]
Then
\[
 \|P^{(i)}C\|_2^2=r,\qquad
 \|A^{(i)}C\|_2^2=1-r.                                   \tag{8}
\]
Equation (5) gives the exact complement identity
\[
 G_i^L(P,P)=G_i^L(A,A).                                  \tag{9}
\]

## 2. Boundary lower bounds and the spectral upper bound

The range of \(P^{(i)}C\) has one-dimensional local support at site
\(i\), while the range of \(A^{(i)}C\) has local support of dimension
at most two.  The established one-sided local-support theorem gives
\[
 Q_3(P^{(i)}C)\geq0,\qquad
 Q_3(A^{(i)}C)\geq0.                                     \tag{10}
\]
Since \(q=-\delta\), equations (3), (8), and (10) imply
\[
 G_i^L(P,P)\geq\delta r,\qquad
 G_i^L(A,A)\geq\delta(1-r).                              \tag{11}
\]

The eigenvalues of \({\cal L}^{\otimes3}\) on the local
scalar/traceless sectors are
\[
 -\frac18,\quad\frac14,\quad-\frac12,\quad1.
\]
Consequently
\[
 Q_3(D)\leq\|D\|_2^2                                     \tag{12}
\]
for every \(D\).  Applying this to \(P^{(i)}C\) gives
\[
 G_i^L(P,P)
 =Q_3(P^{(i)}C)+\delta r
 \leq(1+\delta)r.                                        \tag{13}
\]

Combine (9), the second inequality in (11), and (13):
\[
 \delta(1-r)
 \leq G_i^L(A,A)
 =G_i^L(P,P)
 \leq(1+\delta)r.
\]
Therefore
\[
 \boxed{\qquad
 r\geq\frac{\delta}{1+2\delta}.
 \qquad}                                                  \tag{14}
\]
This holds for every unit \(z\), proving the left-density part of
(1).  Applying the identical argument to right multiplication, or
to \(C^\dagger\), proves the right-density part.

## 3. Consequences for the unweighted singular planes

Write a thin singular-value decomposition
\[
 C=USV^\dagger,\qquad
 U^\dagger U=V^\dagger V=I_2,\qquad
 S=\operatorname{diag}(s_1,s_2),\qquad
 s_1^2+s_2^2=1.                                          \tag{15}
\]
Let
\[
 \sigma_i^U=\operatorname{Tr}_{\widehat i}(UU^\dagger),
 \qquad
 \sigma_i^V=\operatorname{Tr}_{\widehat i}(VV^\dagger).
                                                               \tag{16}
\]
Since \(0\preceq S^2\preceq I_2\),
\[
 \rho_i^L
 =\operatorname{Tr}_{\widehat i}(US^2U^\dagger)
 \preceq\sigma_i^U,
 \qquad
 \rho_i^R\preceq\sigma_i^V.                              \tag{17}
\]
Thus (1) also gives
\[
 \sigma_i^U,\sigma_i^V
 \succeq\frac{\delta}{1+2\delta}I_3.                     \tag{18}
\]
In particular, because these unweighted plane densities have trace
two,
\[
 \det\sigma_i^U,\det\sigma_i^V
 \geq
 2m^2(1-m),
 \qquad
 m=\frac{\delta}{1+2\delta}.                             \tag{19}
\]
Indeed, among three numbers at least \(m\) with sum two, the minimum
of their product is \(m^2(2-2m)\).

The established Haar bound gives \(q\geq-1/8\), hence
\[
 0<\delta\leq\frac18,\qquad
 0<m\leq\frac1{10}.                                      \tag{20}
\]

## 4. Exact limitation

The bound (1) is a necessary condition, not a sign proof.  As
\(\delta\downarrow0\), its right-hand side tends to zero, consistently
with the exact zero manifolds on the local-support boundary.  To
finish unrestricted three-copy positivity one still needs either:

1. a quantitative Haar/determinantal slack inequality strong enough
   to contradict (2); or
2. the lossless one-plane/positive-Segre inequality.

The value of (1) is that the first route can now work on a compact
well-conditioned interior set at every fixed hypothetical negative
depth; no uncontrolled support degeneration remains there.
