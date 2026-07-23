# Exact Lower Bound: \(\tau(5)\geq40\)

## Proposition

Let

\[
R=\{r\in\{-1,0,1\}^5:\#\{i:r_i\ne0\}=2\}
\quad\text{and}\quad
C=\{r/\sqrt2:r\in R\}.
\]

Then \(C\subset S^4\), \(|C|=40\), and
\(\langle x,y\rangle\leq1/2\) for all distinct \(x,y\in C\).

## Proof

Choose the support of \(r\) in \(\binom52=10\) ways and choose the two nonzero
signs in \(2^2=4\) ways.  These choices are unique, so \(|R|=40\).

Every \(r\in R\) has \(r\cdot r=2\).  Hence \(r/\sqrt2\) is a unit vector.

Take distinct \(r,s\in R\).

- If their supports are disjoint, then \(r\cdot s=0\).
- If their supports meet in exactly one coordinate, then \(r\cdot s\in
  \{-1,1\}\).
- If their supports agree, distinctness means at least one of the two signs
  differs.  Thus \(r\cdot s\) is \(0\) (one sign differs) or \(-2\) (both
  differ).

In every case \(r\cdot s\leq1\).  Therefore

\[
\left\langle \frac r{\sqrt2},\frac s{\sqrt2}\right\rangle
=\frac{r\cdot s}{2}\leq\frac12.
\]

Equality is allowed by the problem statement, so pairs with one common
coordinate and matching sign satisfy the boundary condition exactly.  Thus
\(C\) is a 40-point kissing configuration in \(S^4\), proving
\(\tau(5)\geq40\). \(\square\)

## Independent exact check

`verifiers/verify_d5.py` reads the explicit coordinate certificate and checks
the same assertions using only integer arithmetic.  It does not evaluate
\(\sqrt2\) numerically.
