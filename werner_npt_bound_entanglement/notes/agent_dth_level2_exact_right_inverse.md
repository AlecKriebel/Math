# Exact equivariant right inverse and PSD-control lemma

## Purpose

The complete degree-three fixed-marginal calculation has 519434
real-symmetric source coordinates before physical-site averaging.  A direct
rational reconstruction of every coordinate is possible in principle but is
not the right proof object.  This note isolates a general exact certificate:
one rational right inverse, one residual norm, and blockwise positive margins.

The lemma below is exact finite-dimensional linear algebra.  Applying it to
the DTH map still requires exact construction of the symmetry-reduced
marginal and rigorous numerical bounds.  No degree-three extension theorem is
claimed in this note alone.

## 1. Right inverse

Let

\[
\mathcal X=\bigoplus_{b=1}^N\operatorname{Sym}_{k_b}(\mathbb R),
\qquad
\mathcal Y=\mathbb R^m
\]

be Euclidean spaces, and let

\[
A:\mathcal X\longrightarrow\mathcal Y
\]

be surjective.  Its affine normal operator

\[
G=AA^*
\]

is positive definite.  Define

\[
\boxed{J=A^*G^{-1}.}
\tag{1}
\]

Then

\[
AJ=I_{\mathcal Y},
\qquad
\|J\|_{2\to2}
=\frac1{\sigma_{\min}(A)}
=\frac1{\sqrt{\lambda_{\min}(G)}}.
\tag{2}
\]

The first identity is immediate.  For the norm, use a singular-value
decomposition of (A); (J) has singular values equal to the reciprocals of
the nonzero singular values of (A).

## 2. Exact PSD correction

Let (r\in\mathcal Y) be the required marginal and let

\[
\widetilde X=(\widetilde X_b)_b\in\mathcal X
\]

be any approximate source.  Put

\[
e=r-A\widetilde X,
\qquad
X=\widetilde X+Je.
\tag{3}
\]

Then (AX=r) exactly.  Moreover, for every block,

\[
\begin{aligned}
\lambda_{\min}(X_b)
&\ge
\lambda_{\min}(\widetilde X_b)-\|(Je)_b\|_{\rm op}\\
&\ge
\lambda_{\min}(\widetilde X_b)
-\frac{\|e\|_2}{\sqrt{\lambda_{\min}(G)}}.
\end{aligned}
\tag{4}
\]

The first line is Weyl's inequality.  The second uses

\[
\|(Je)_b\|_{\rm op}
\le\|(Je)_b\|_F
\le\|Je\|_2
\le\|J\|\|e\|_2.
\]

Thus the checkable strict condition

\[
\boxed{
\min_b\lambda_{\min}(\widetilde X_b)
>
\frac{\|r-A\widetilde X\|_2}
{\sqrt{\lambda_{\min}(AA^*)}}
}
\tag{5}
\]

produces an exact positive definite solution of the fixed-marginal equation.

This criterion is conservative.  A sharper blockwise version replaces the
common denominator in (4) by the exactly computable norms

\[
\beta_b=\|P_bJ\|_{2\to F},
\qquad
\lambda_{\min}(X_b)
\ge\lambda_{\min}(\widetilde X_b)-\beta_b\|e\|_2.
\tag{6}
\]

## 3. Rationality

Use rational, not orthonormalized Young, coordinates.  In the DTH problem the
following data are rational:

* integral polytabloid bases and their rational Gram matrices;
* Pluecker and Omega kernel charts;
* permutation-diagram marginal contraction;
* physical-site permutation actions; and
* the exact five-replica pseudomoment.

The Hilbert adjoint in rational nonorthogonal coordinates inserts the inverse
Gram matrices, so (A^*), (G), and (J) are still rational.  Therefore, if

\[
\widetilde X\in\mathcal X(\mathbb Q),
\qquad r\in\mathcal Y(\mathbb Q),
\]

then the corrected (X) in (3) is rational and satisfies the marginal
identity literally over (mathbb Q).

An exact verifier need not store (J) densely.  It may instead solve

\[
Gy=e,
\qquad X=\widetilde X+A^*y,
\tag{7}
\]

using fraction-free or modular reconstruction, then replay (AX=r).  Exact
LDL/Sylvester certificates or rigorous interval Cholesky certify each block
of (X).

## 4. Equivariance and the 761-coordinate reduction

Let a finite group (mathfrak S) act orthogonally on both spaces and suppose

\[
A\rho_{\mathcal X}(g)
=\rho_{\mathcal Y}(g)A
\qquad(g\in\mathfrak S).
\tag{8}
\]

Then (G) commutes with the action on (mathcal Y), and (J) is also an
intertwiner.  If (r) is invariant, averaging any approximate source before
the correction in (3) preserves its marginal residual norm and preserves
positive semidefiniteness.  Equations (1)--(7) may therefore be restricted to
the invariant subspaces without loss.

For physical-site permutations in the complete DTH marginal, this reduces
the 4139 raw five-replica symmetric coordinates to 761 invariant
coordinates.  The source blocks are tied along local-shape orbits and by the
corresponding exact Specht intertwiners.  This is the correct finite system
for an exact right-inverse certificate.

## 5. Weighted right inverse

The unweighted common bound (5) can be poor when source blocks have very
different natural scales.  Let (D\succ0) be a rational block-diagonal
weight on (mathcal X).  The minimum-(D)-norm right inverse is

\[
\boxed{
J_D=D^{-1}A^*(AD^{-1}A^*)^{-1}.
}
\tag{9}
\]

Again (AJ_D=I).  Choosing (D) from rational approximations to the inverse
block margins distributes the exact affine correction away from the weakest
blocks.  The corresponding exact condition is

\[
\lambda_{\min}(\widetilde X_b)
>
\|P_bJ_D\|_{2\to F}\,\|e\|_2
\qquad\text{for every }b.
\tag{10}
\]

This provides a finite optimization target for the discovery layer and a
rational certificate architecture for the verification layer.

## 6. DTH scope

Here (A) is only the positive fixed-marginal map on the post-Omega
holomorphic source.  A certificate from (5) or (10) would prove that the
exact five-replica pseudomoment has a positive degree-three Grassmann
extension.  It would not automatically prove the prolonged mixed-support or
grouped-PPT constraints.  Those are additional linear equations and positive
cones to be imposed after the fixed-marginal decision.

