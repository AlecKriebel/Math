# Quarter-grid H1 spectral-variance lattice

## Statement

Let \(C=\{x_1,\ldots,x_{41}\}\subset S^4\), and suppose additionally that
every off-diagonal inner product belongs to the quarter grid

\[
\{-1,-3/4,-1/2,-1/4,0,1/4,1/2\}.
\]

For \(m\in\{-4,-3,\ldots,2\}\), let \(n_m\) be the number of unordered
pairs with inner product \(m/4\), and put

\[
Q=\sum_{m=-4}^{2}m^2 n_m\in\mathbb Z.
\]

If \(G\) is the Gram matrix and

\[
E=\frac1{41}\sum_{i\ne j}\langle x_i,x_j\rangle^2,
\qquad
V=\operatorname{tr}(G^2)-\frac{41^2}{5},
\]

then

\[
E=\frac Q{328},
\qquad
V=\frac{5Q-11808}{40}.
\tag{1}
\]

In particular, \(X=40V\) is a nonnegative integer satisfying
\(X\equiv2\pmod5\).  Hence

\[
0\le V\le\frac3{10}
\quad\Longrightarrow\quad
V\in\left\{\frac1{20},\frac7{40},\frac3{10}\right\}.
\tag{2}
\]

The three corresponding values of \(Q\) are \(2362,2363,2364\), and the
next possible variance is \(17/40\).

## Proof

The ordered pair distribution at \(m/4\) has mass \(2n_m/41\).  Therefore

\[
E=\sum_m\frac{2n_m}{41}\frac{m^2}{16}
 =\frac1{328}\sum_m m^2n_m=\frac Q{328}.
\]

The diagonal contributes \(41\) to the squared Frobenius norm of \(G\), so

\[
\operatorname{tr}(G^2)
 =41+\sum_m2n_m\frac{m^2}{16}
 =41+\frac Q8.
\]

Let \(\lambda_1,\ldots,\lambda_s\) be the nonzero eigenvalues of \(G\).
Since \(G\succeq0\), \(\operatorname{rank}G=s\le5\), and
\(\sum_a\lambda_a=41\).  Pad this list with zeros to five entries.  Then

\[
\sum_{a=1}^{5}\left(\lambda_a-\frac{41}{5}\right)^2
 =\operatorname{tr}(G^2)-\frac{41^2}{5}=V\ge0.
\]

Substitution gives the second identity in (1).  Thus

\[
X=40V=5Q-11808\equiv2\pmod5.
\]

The nonnegative integers in this residue class begin
\(2,7,12,17,\ldots\), which proves (2), including the closed endpoint
\(V=3/10\).  Notice that rank strictly below five causes no exception:
the zero-padding argument already covers it.

## Scope

This is an exact arithmetic lemma for quarter-grid configurations.  It does
not justify discretizing a general spherical code, and it does not make a
finite-grid SDP certificate valid on continuous inner-product support.
Its role in discovery is to reject numerical pseudodistributions whose
quarter-grid energy lies between the allowed lattice levels.

## Reproduction

```sh
python3 verifiers/verify_quarter_grid_h1_variance_lattice.py
python3 -m unittest tests.test_quarter_grid_h1_variance_lattice
python3 -O -m unittest tests.test_quarter_grid_h1_variance_lattice
```
