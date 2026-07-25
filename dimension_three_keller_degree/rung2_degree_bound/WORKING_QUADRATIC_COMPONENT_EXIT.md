# Working theorem: the quadratic-component exit

**Status:** proved and independently adversarially audited.  The standalone
hostile report is `audit_quadratic_component_exit/REPORT.md`.  This is not
peer reviewed.  A source-specific search found no exact prior statement,
which is not a guarantee of worldwide priority.

**Recorded:** 2026-07-24T23:59:52Z.

## 1. Statement

### Theorem

Let
\[
F:\mathbb A^3_{\mathbb C}\longrightarrow\mathbb A^3_{\mathbb C}
\]
be a Keller map of total polynomial degree at most \(4\).  If a nonzero
target linear combination
\[
f=\lambda_1F_1+\lambda_2F_2+\lambda_3F_3
\]
has degree at most \(2\), then \(F\) is a polynomial automorphism.

Equivalently, a total-degree-four counterexample cannot have a
degree-at-most-two polynomial in the target-linear span of its components.

The proof uses the established plane lower bound only as a black box.  It
does not assume the plane Jacobian Conjecture and does not undertake new work
in dimension two.

## 2. A quadratic submersion is a coordinate

### Lemma

If \(f\in\mathbb C[X_1,X_2,X_3]\) has degree at most \(2\) and
\(\nabla f\) vanishes nowhere, then there is a polynomial automorphism
\[
T=(Y_1,Y_2,f)
\]
such that
\[
\deg T\le2,\qquad \deg T^{-1}\le2,\qquad
\det JT\in\mathbb C^\times.
\]

### Proof

Write
\[
\nabla f=HX+b
\]
with \(H\) a constant symmetric matrix.  If \(b\in\operatorname{im}H\),
then \(HX=-b\) has a solution and gives a critical point.  Hence
\[
b\notin\operatorname{im}H=(\ker H)^\perp.
\]
Choose \(v\in\ker H\) with \(b^Tv\ne0\), complete \(v\) to a linear
source-coordinate basis, and call the resulting coordinates
\((Y_1,Y_2,Y_3)\), with \(v\) in the \(Y_3\)-direction.  Since \(Hv=0\),
the quadratic part has no term involving \(Y_3\).  Thus
\[
f=g(Y_1,Y_2)+\beta Y_3,\qquad \beta\ne0,
\]
after absorbing affine-linear terms in \(g\).  The triangular map
\[
T(Y_1,Y_2,Y_3)=(Y_1,Y_2,f)
\]
has inverse
\[
T^{-1}(Z_1,Z_2,Z_3)=
\left(Z_1,Z_2,\frac{Z_3-g(Z_1,Z_2)}{\beta}\right).
\]
Both degree bounds and the constant-Jacobian assertion follow.
\(\square\)

## 3. Reduction to low-degree plane fibres

Let \(F^0\) denote the original map.  Apply a target linear change whose
third row is \(\lambda\), and call the changed map \(F\).  Since \(JF^0\)
is invertible at every point, the row
\[
\nabla F_3=\lambda^TJF^0
\]
never vanishes.  The lemma supplies \(T\) with third component \(F_3\).
Set
\[
G=F\circ T^{-1}.
\]
Then
\[
G=(G_1,G_2,X_3),\qquad
\det JG\in\mathbb C^\times,\qquad
\deg G\le4\cdot2=8.
\]

For every \(c\in\mathbb C\), the fibre map
\[
G_c:\mathbb A^2\longrightarrow\mathbb A^2,\qquad
(X_1,X_2)\longmapsto
\bigl(G_1(X_1,X_2,c),G_2(X_1,X_2,c)\bigr)
\]
is Keller and has degree at most \(8\).  Vistoli states on journal p. 80
the unconditional theorem that an étale polynomial self-map of
\(\mathbb A^2\) of degree at most \(12\) is an isomorphism (citing Moh).
Since \(8\le12\), every \(G_c\) is a polynomial automorphism.  This is a
proved bounded-degree theorem, not an assumption of the plane Jacobian
Conjecture.

If two points have the same image under \(G\), their third coordinates are
equal and they lie in the same fibre.  Injectivity of \(G_c\) then makes the
two points equal.  Hence \(G\), and therefore \(F\), is injective.
The injective-étale theorem quoted by Vistoli makes \(F\) surjective; an
étale universally injective morphism is an open immersion, so a surjective
one is an isomorphism.  Equivalently, this last step is the
Ax--Grothendieck theorem together with the Keller étaleness.
\(\square\)

## 4. Immediate quartic consequences

1. In the primitive line-type theorem, the branch
   \((H_3)_3=0\) is entirely impossible for a counterexample, whether or not
   \((H_2)_3\) vanishes.  Thus a counterexample in that stratum must have
   \[
   (H_3)_3=\lambda L^3
   \]
   and a leading pencil member \(L^4\).
2. In the genuine line-image \((2,2)\) stratum, a quadratic pencil with no
   double-line member forces \((H_3)_3=0\).  The theorem then excludes the
   whole no-double-line stratum, not merely the subcase
   \((H_2)_3=0\).

## 5. Verification boundary

The only nonlinear coordinate change in the proof and its inverse both have
degree at most \(2\); therefore \(8\), not \(16\), is the correct worst-case
plane-fibre degree.  The proof works with an arbitrary invertible linear part
and with constants.  The exact coordinate and fibre identities are replayed
in `audit_quadratic_component_exit/verify_quadratic_component_exit_exact.py`;
the cited plane theorem itself is a literature input, not a computational
claim.
