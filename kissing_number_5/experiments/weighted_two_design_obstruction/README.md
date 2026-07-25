# Weighted spherical 2-design audit

## Question

For a hypothetical 41-point kissing code \(C=\{x_i\}\subset S^4\), must
there be nonnegative weights \(p_i\), summing to one, such that
\[
\sum_i p_i x_i=0,\qquad
\sum_i p_i x_ix_i^{\mathsf T}=\frac15I_5?               \tag{1}
\]

By finite-dimensional separation, failure of (1) is equivalent to a
mean-zero spherical polynomial of degree at most two that is strictly
positive on every point.  This folder records exact evidence for (1) and
two exact barriers to proving it from weaker inputs.  It does not settle
the 41-point question.

## Exact positive evidence at 40 points

The verifier reconstructs the four known exact configurations
\(D_5,L_5,Q_5,R_5\), using rational coordinate rows of squared norm two.
For every one it checks
\[
\sum_{x\in C}x=0,\qquad
\sum_{x\in C}xx^{\mathsf T}=8I_5.
\]
After normalization and division by forty, uniform weights satisfy (1).
Thus every known 40-point model is an exact uniform spherical 2-design,
despite the models being non-isometric and having different pair
distributions.

This is meaningful evidence, but it is not a classification and cannot be
used to infer the statement at 41 points.

## Kissing plus centering is insufficient

Let \(D_5\) denote the forty normalized roots.  Define the traceless
symmetric matrix
\[
A=\begin{pmatrix}
2&0&0&0&-5\\
0&2&0&0&-5\\
0&0&2&0&-5\\
0&0&0&2&5\\
-5&-5&-5&5&-8
\end{pmatrix}.
\]
Direct exact evaluation gives
\[
x^{\mathsf T}Ax\in\{2,-8\}\qquad(x\in D_5),
\]
with value two on 32 roots and value \(-8\) on the other eight.  The
32-point positive subset is antipodal, centered, rank five, and remains a
genuine kissing code.

It cannot admit weights satisfying the covariance equation in (1):
otherwise
\[
\sum_i p_i x_i^{\mathsf T}Ax_i
=\operatorname{tr}\left(A\frac15I\right)=0,
\]
whereas every summand on the left equals two.  Hence even exact kissing
geometry, antipodality, centering, and full rank do not by themselves force
weighted degree-two isotropy.

## The certified depth and frame floor are insufficient

Fix twenty distinct rational parameters \(t\in[-1,1]\) and
\(\epsilon=1/1000\).  Take the forty normalized antipodal points on the
lines
\[
v(t)=(1,t,t^2,t^3,\epsilon t^4)
\]
and append \(e_5\).

Any five lines are independent, by the Vandermonde determinant.  Therefore
every open origin hemisphere contains at least sixteen points, and the
origin remains interior after deleting any six points.  The exact rational
frame matrix also satisfies the repository's certified hypothetical-code
floor
\[
\sum_i x_ix_i^{\mathsf T}\succ\frac{15059}{40000}I.
\]
The verifier proves this by exact Sylvester minors.

Nevertheless,
\[
q(x)=1-5x_5^2+5x_5
\]
has spherical mean zero and is strictly positive on all 41 points.  At
\(e_5\), \(q=1\).  On every paired point, \(|x_5|\leq\epsilon\), so
\[
q(x)\geq1-5\epsilon-5\epsilon^2>0.
\]
Thus this model has no weights satisfying (1).

The construction is deliberately not a kissing code; an adjacent
moment-curve pair has inner product greater than \(1/2\).  It proves that
the exact \(B(5)\)-derived deletion property and the current frame floor,
even with substantially stronger hemisphere depth, cannot establish (1)
without a genuinely pairwise kissing-code input.

## Exact remaining gap

A successful proof must show that the positive locus of every nonzero
mean-zero quadratic-plus-linear polynomial contains at most forty points of
a five-dimensional kissing code.  Neither hemisphere depth nor unweighted
frame conditioning controls such a general quadratic locus.

The known configurations suggest that the statement is plausible.  The
32-point example shows that any proof must use the cardinality-41 geometry,
not merely centering or scalability folklore.

## Reproduction

```sh
python3 experiments/weighted_two_design_obstruction/verify.py
python3 -m unittest discover \
  -s experiments/weighted_two_design_obstruction \
  -p 'test_*.py' -v
```

The verifier uses only the Python standard library.

SHA-256 values for the machine-checked core are

```text
b96809297f5f048f77ce2826626e327b93098ca9b8a3f439eb513c4a13911d10  certificate.json
a9d0e9330dc615ced3d6f52d0356a0ed3295d1a0e7123d87d6a71f714869baed  verify.py
d08deab99251ff1e38aa9298db27c85fe12045c0efecb5f1a6440f2c8cfc9119  test_verify.py
```
