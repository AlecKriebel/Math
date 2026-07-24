# A universal positive-quarter link bound

## Result

Let \(x\) be one point of a five-dimensional kissing configuration, and let

\[
Y_x=\{y\ne x:\langle x,y\rangle\geq1/4\}.
\]

Then

\[
\boxed{|Y_x|\leq23.}
\]

This is a local necessary condition for every configuration; it assumes no
centering, symmetry, rigidity, or finite inner-product alphabet.

## Projection to four dimensions

For \(y\in Y_x\), put \(u=\langle x,y\rangle\).  The kissing constraint
against \(x\) gives \(1/4\leq u\leq1/2\), and

\[
\widehat y=\frac{y-ux}{\sqrt{1-u^2}}\in S^3\subset x^\perp.
\]

For distinct \(y,z\), write \(v=\langle x,z\rangle\).  Then

\[
\langle\widehat y,\widehat z\rangle
\leq
\frac{1/2-uv}{\sqrt{(1-u^2)(1-v^2)}}.                 \tag{1}
\]

For fixed \(v\in[1/4,1/2]\), differentiation of the right side of (1)
with respect to \(u\) has the sign of \(u/2-v\), which is nonpositive on
the square \([1/4,1/2]^2\).  The same holds after exchanging \(u,v\).
Thus its maximum is attained at \(u=v=1/4\), where it equals

\[
\frac{1/2-1/16}{1-1/16}=\frac7{15}.                   \tag{2}
\]

Consequently the projected points form a spherical code in \(S^3\) with
maximum inner product \(7/15\).

## Exact Delsarte certificate

Use the normalized Gegenbauer polynomials for \(S^3\),

\[
P_0=1,\quad P_1=t,\quad
(k+1)P_k=2ktP_{k-1}-(k-1)P_{k-2}.
\]

Set

\[
\begin{aligned}
f(t)={}&(t-\tfrac7{15})
\cdot(t+\tfrac{179}{200})^2
\cdot(t+\tfrac{67}{125})^2\\
&\quad\cdot(t+\tfrac{223}{1000})^2
\cdot\left((t-\tfrac{27}{25})^2+\tfrac14\right).
\tag{3}
\end{aligned}
\]
This is a product of the five displayed factors.

The factorization makes \(f(t)\leq0\) on \([-1,7/15]\): the first factor is
nonpositive, the three doubled factors are nonnegative, and the final
quadratic is strictly positive.  Exact expansion in the \(P_k\) basis has
strictly positive coefficients in every degree \(0,\ldots,9\).  They are
stored in
`certificates/a4_7_15_delsarte.json` and independently reconstructed by the
verifier.

The exact Delsarte objective is

\[
\frac{f(1)}{f_0}
=
\frac{162458260679981924352}{6933123990242908417}
<24.
\]

The standard positive-kernel argument therefore gives
\[
A(4,7/15)<24.
\]
Since cardinality is integral, \(A(4,7/15)\leq23\).  Combining this with
(1)--(2) proves the claimed local bound.

## Boundary audit

- Heights \(u=1/4\) and \(u=1/2\) are included.
- The projected code retains the contact boundary \(7/15\).
- The auxiliary polynomial is nonpositive on the full closed interval.
- All Gegenbauer coefficients and the strict objective gap are rational.
- No floating-point result is used by the proof.

Reproduce the exact checks with

```sh
python3 verifiers/verify_a4_7_15_bound.py
python3 -O -m unittest -v tests.test_a4_7_15_bound
```
