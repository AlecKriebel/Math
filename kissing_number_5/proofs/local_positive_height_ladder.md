# Exact nested positive-height link bounds

Let \(C\subset S^4\) be a five-dimensional kissing code and fix
\(x\in C\).  The following four bounds hold:

\[
\begin{array}{c|cccc}
h&3/10&1/3&3/8&2/5\\ \hline
\#\{y\ne x:\langle x,y\rangle\ge h\}&22&21&20&19.
\end{array}
\]

These statements are universal.  They assume no symmetry, centering,
rigidity, or finite inner-product alphabet.

## Tangent projection

Write \(u=\langle x,y\rangle\) and
\[
\widehat y=\frac{y-ux}{\sqrt{1-u^2}}\in S^3.
\]
For two selected points at heights \(u,v\in[h,1/2]\),
\[
\langle\widehat y,\widehat z\rangle
\le
\frac{1/2-uv}{\sqrt{(1-u^2)(1-v^2)}}.                 \tag{1}
\]
For fixed \(v\), the derivative of the right side with respect to \(u\)
has the sign of \(u/2-v\).  Since \(h\ge3/10>1/4\), this is negative
throughout the square; the same is true after interchanging \(u,v\).
Thus (1) is at most
\[
s(h)=\frac{1/2-h^2}{1-h^2}.
\]
At the four heights, these values are respectively
\[
\frac{41}{91},\quad\frac7{16},\quad\frac{23}{55},
\quad\frac{17}{42}.                                  \tag{2}
\]

## Exact Delsarte polynomials

For each value \(s=s(h)\), the certificate stores a polynomial
\[
f(t)=\sum_\ell c_\ell
(t-s_\ell)\prod_j(t-r_{\ell j})^2
\bigl((t-a_\ell)^2+b_\ell\bigr),                     \tag{3}
\]
where the displayed expression is parsed as the product of the factors
following each positive scale \(c_\ell\).  Every \(c_\ell,b_\ell\) is
positive and every \(s_\ell\ge s\).  Consequently every component, and
hence \(f\), is nonpositive on the full closed interval \([-1,s]\).

The verifier reconstructs (3), expands it exactly in the normalized
dimension-four Gegenbauer basis, and checks that every coefficient is
strictly positive.  The four exact Delsarte objectives are
\[
\begin{array}{c|c}
h&f(1)/f_0\\ \hline
3/10&
\frac{649480820252437761818391}{29281140791071025155091}<23\\
1/3&
\frac{458395635434395435876881}{21375372411490317209837}<22\\
3/8&
\frac{13374151861670393389505568}{651358196862764803307473}<21\\
2/5&
\frac{1544041716137767095970464}{78187962775800789058919}<20.
\end{array}
\]
The positive-kernel argument gives \(A(4,s)<23,22,21,20\),
respectively.  Integrality and (1)--(2) prove the table.

## Boundary and reproduction audit

The height threshold, contact inequality, and projected endpoint are all
closed.  Each sign proof covers all of \([-1,s]\); there is no sampled
polynomial check.  All coefficients and objectives are rational.

Run

```sh
python3 verifiers/verify_local_positive_height_ladder.py
python3 -O -m unittest -v tests.test_local_positive_height_ladder
```
