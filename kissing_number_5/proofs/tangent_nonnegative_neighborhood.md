# Tangent projection of every nonnegative neighborhood

## Result

Let \(C\subset S^4\) be an \(N\)-point kissing code.  For every \(x\in C\),
put
\[
 C_x^+=\{y\in C\setminus\{x\}:\langle x,y\rangle\geq0\},\qquad
 r(x)=\#\{y\in C\setminus\{x\}:\langle x,y\rangle<0\}.
\]
Then
\[
 \boxed{|C_x^+|\leq33,\qquad r(x)\geq N-34.}       \tag{1}
\]
In particular, if \(N=41\), every vertex has at least seven strictly
negative neighbors and the graph of negative pairs has at least
\[
 \left\lceil\frac{41\cdot7}{2}\right\rceil=144
\]
edges.

This strengthens the previously recorded tradeoff \(d(x)+r(x)\geq7\):
contacts no longer contribute to the lower bound.  It is a universal local
condition; it assumes neither a common hemisphere nor rigidity, symmetry, or
maximality.

## Exact projection lemma

Fix \(x\in C\).  Every \(y\in C_x^+\) has height
\[
 z_y=\langle x,y\rangle\in[0,1/2].
\]
The upper endpoint is included: it consists precisely of the contacts of
\(x\).  Define the normalized tangent projection
\[
 \pi_x(y)=\frac{y-z_yx}{\sqrt{1-z_y^2}}\in S^3.
\]
The denominator is at least \(\sqrt3/2\), including at a contact, and is
therefore never zero.

For distinct \(y,y'\in C_x^+\), write \(z=z_y\), \(w=z_{y'}\).  The kissing
inequality gives
\[
 \langle\pi_x(y),\pi_x(y')\rangle
 \leq
 R(z,w):=\frac{1/2-zw}
 {\sqrt{(1-z^2)(1-w^2)}}.                         \tag{2}
\]
The numerator is at least \(1/4\), so both sides in the following
comparison are nonnegative.  Squaring shows that
\[
 R(z,w)\leq\frac1{\sqrt3}
\]
is equivalent to
\[
 D(z,w):=\frac14-z^2-w^2+3zw-2z^2w^2\geq0.       \tag{3}
\]
For fixed \(z\in[0,1/2]\), \(D\) is a concave quadratic in \(w\), because
its \(w^2\)-coefficient is \(-(1+2z^2)<0\).  Its minimum on the closed
interval therefore occurs at an endpoint, where
\[
 D(z,0)=\frac14-z^2\geq0,\qquad
 D(z,1/2)=\frac32z(1-z)\geq0.                    \tag{4}
\]
This proves (3) on the entire closed square.  It also identifies the sharp
cases: equality occurs only at
\[
 (z,w)=(0,1/2)\quad\hbox{or}\quad(1/2,0).
\]
Thus equatorial heights \(0\), contact heights \(1/2\), and their mixed
boundary are all retained.  When \(z=w=0\), (2) gives the stronger bound
\(1/2\); when \(z=w=1/2\), it gives the stronger bound \(1/3\).

The projection is injective.  Indeed, coincident projected unit vectors
would have inner product \(1\), contradicting the just-proved bound
\(1/\sqrt3<1\).  Consequently \(\pi_x(C_x^+)\) is an
\((4,1/\sqrt3)\)-spherical code.

The exact degree-11 certificate in
[`one_sided_tukey_bound.md`](one_sided_tukey_bound.md) proves
\[
 A(4,1/\sqrt3)\leq33.
\]
Therefore \(|C_x^+|\leq33\).  Since the other \(N-1-|C_x^+|\) points have
strictly negative inner product with \(x\), (1) follows.

## Consequences and limitations

For a hypothetical 41-code the negative-pair graph has minimum degree at
least \(7\), not merely an average-degree constraint.  For any 38-point code
contained in a closed hemisphere, the induced negative-pair graph has
minimum degree at least \(4\) and at least \(76\) edges.

These conclusions do not themselves rule out either configuration.  A
generic collection of points can have many mildly negative inner products,
and the lemma does not force any pair below \(-1/2\).  In particular it
cannot be substituted for the separate deep-negative graph analysis.

## Boundary and dependency audit

- The code condition is \(\langle y,y'\rangle\leq1/2\), and every equality
  case is retained.
- The neighborhood uses \(\langle x,y\rangle\geq0\); height \(0\) is not
  lost.
- Contacts have height exactly \(1/2\) and are projected without a limiting
  argument.
- The optimization is proved on the full closed square
  \([0,1/2]^2\), not on a mesh.
- No rank, contact-graph, rigidity, or maximality hypothesis is used.
- The only imported non-elementary input is the independently exact
  \(A(4,1/\sqrt3)\leq33\) certificate.

```text
exact D(z,w) endpoint factorization on [0,1/2]^2
                         |
                         v
 tangent projection C_x^+ -> (4,1/sqrt(3))-code, injectively
                         |
        exact A(4,1/sqrt(3)) <= 33 certificate
                         |
                         v
              |C_x^+| <= 33 and r(x) >= N-34
```
