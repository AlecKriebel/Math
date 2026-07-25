# An exact top-eigenvector cap subregion

Let
\[
q(x)=\sum_{i=1}^5\lambda_i x_i^2+\sum_{i=1}^5b_i x_i,
\qquad
\lambda_1\leq\cdots\leq\lambda_4\leq\lambda_5=1,
\]
with \(b_i\geq0\).  Put
\[
\beta=b_5,\qquad B_\perp=\sqrt{b_1^2+\cdots+b_4^2},
\qquad \varepsilon=\frac1{50}.
\]

## Lemma

If
\[
\beta\geq1
\tag{1}
\]
and
\[
B_\perp\leq
\min\left\{
\beta-1,
\varepsilon\beta-\varepsilon^2
-\lambda_4(1-\varepsilon^2)
\right\},
\tag{2}
\]
then
\[
q(x)\geq0,\quad x\in S^4
\quad\Longrightarrow\quad x_5\geq-\frac1{50}.
\tag{3}
\]
Consequently, the exact enlarged-cap theorem implies that every
five-dimensional kissing code in this quadratic positive locus has at most
39 points.

Condition (2) automatically requires its second right-hand side to be
nonnegative.  Squaring is safe on this stated nonnegative region, so the
condition is semialgebraic:
\[
\sum_{i=1}^4b_i^2\leq(\beta-1)^2
\]
and
\[
\sum_{i=1}^4b_i^2\leq
\left(
\frac{\beta}{50}-\frac1{2500}
-\frac{2499}{2500}\lambda_4
\right)^2.
\]

## Proof

Write \(t=x_5=-s\), where \(s\in[\varepsilon,1]\).  Since the largest
eigenvalue on \(e_5^\perp\) is \(\lambda_4\),
\[
x^{\mathsf T}Ax
\leq\lambda_4(1-t^2)+t^2.
\]
Also
\[
\sum_{i=1}^4b_ix_i\leq B_\perp\sqrt{1-t^2}\leq B_\perp.
\]
Therefore
\[
q(x)\leq
f(s):=\lambda_4+(1-\lambda_4)s^2-\beta s+B_\perp.
\tag{4}
\]
Because \(\lambda_4\leq1\), \(f\) is convex on
\([\varepsilon,1]\), so its maximum occurs at an endpoint.  Conditions
(1)--(2) give
\[
f(1)=1-\beta+B_\perp\leq0
\]
and
\[
f(\varepsilon)=
\lambda_4(1-\varepsilon^2)+\varepsilon^2
-\varepsilon\beta+B_\perp\leq0.
\]
Thus \(q(x)\leq0\) whenever \(x_5\leq-\varepsilon\), proving (3).

## Examples of certified positive-width regions

- If \(\lambda_4\leq0\), \(\beta\geq2\), and
  \(B_\perp\leq99/2500\), then (1)--(2) hold.
- If \(b_1=\cdots=b_4=0\) and \(\lambda_4\leq0\), every
  \(\beta\geq1\) is covered.  This includes the full normalized
  one-positive-eigenvalue axisymmetric transition.
- More generally, the allowed transverse width increases linearly as
  \(\beta/50-(2499/2500)\lambda_4\).

The lemma uses only the top eigendirection.  It does not cover belt-like
quadratics with \(\lambda_4\) near one and a small axial linear term.
