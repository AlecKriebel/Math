# Working theorem: the quadratic-component exit

**Status:** proved and independently adversarially audited.  This is not peer
reviewed.  A source-specific search found no exact prior statement, which is
not a guarantee of worldwide priority.

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
Choose \(v\in\ker H\) with \(b^Tv\ne0\), and make a linear source change
taking \(v\) to the third coordinate direction.  Since \(Hv=0\), the
quadratic part has no term involving \(X_3\).  Thus
\[
f=g(X_1,X_2)+\beta X_3,\qquad \beta\ne0,
\]
after absorbing affine-linear terms in \(g\).  The triangular map
\[
T(X_1,X_2,X_3)=(X_1,X_2,f)
\]
has inverse
\[
T^{-1}(Y_1,Y_2,Y_3)=
\left(Y_1,Y_2,\frac{Y_3-g(Y_1,Y_2)}{\beta}\right).
\]
Both degree bounds and the constant-Jacobian assertion follow.
\(\square\)

## 3. Reduction to low-degree plane fibres

Apply a target linear change whose third row is \(\lambda\), and keep the
notation \(F\) for the changed map.  Since \(JF\) is invertible at every
point, the row
\[
\nabla F_3=\lambda^TJF
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
is Keller and has degree at most \(8\).  The unconditional plane lower bound
for a counterexample is at least \(100\), so every \(G_c\) is a polynomial
automorphism.

If two points have the same image under \(G\), their third coordinates are
equal and they lie in the same fibre.  Injectivity of \(G_c\) then makes the
two points equal.  Hence \(G\), and therefore \(F\), is injective.
Ax--Grothendieck makes \(F\) a polynomial automorphism.
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
and with constants.
