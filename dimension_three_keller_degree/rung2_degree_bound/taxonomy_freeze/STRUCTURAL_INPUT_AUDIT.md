# Structural-input audit for the quartic leading taxonomy

**Checked (UTC):** 2026-07-25T19:30:28Z.

## Primary source

Michiel de Bondt, *Rational maps \(H\) for which \(K(tH)\) has
transcendence degree 2 over \(K\)*, Theorem 2.7,
[arXiv:1501.06046v4](https://arxiv.org/pdf/1501.06046), pp. 15--17.

The clauses used here are:

1. a map of the relevant transcendence degree has a representation
   \(H=gA(p,q)\), with \(A\) a homogeneous primitive binary vector and
   \(p,q\) a primitive nonconstant polynomial pair;
2. primitivity is preserved under the substitution;
3. a homogeneous substituted vector has a homogeneous pair \(p,q\);
4. degree multiplies under the substitution; and
5. a pair of minimal degree generates a relatively algebraically closed
   subfield \(K(p/q)\subset K(x)\).

These are Theorem 2.7(i)--(ix), not a consequence of the quartic
exclusions.  The theorem is stated for an arbitrary field; the present
taxonomy uses it only over \(\mathbb C\).

## Specialization to a polynomial homogeneous map

For the quartic polynomial vector \(H_4\), Theorem 2.7 gives
\[
H_4=gA(p,q).
\]
The substituted vector \(A(p,q)\) is primitive in the polynomial ring.
Since every component of \(H_4\) is polynomial, the denominator of the
rational scalar \(g\) would divide every component of \(A(p,q)\);
primitivity makes that denominator a unit.  Thus \(g\) is polynomial and,
up to a scalar, equals the component gcd \(h\).  Homogeneity of \(H_4\)
and of \(A(p,q)\) makes \(h\) homogeneous.

Writing
\[
e=\deg h,\qquad a=\deg(p,q),\qquad b=\deg A
\]
therefore gives
\[
e+ab=4.
\]
Minimality supplies the relative-algebraic-closure clause used to prevent
composite presentations from being counted twice.

## Outer curve degree

The basepoint-free binary vector
\[
A:\mathbb P^1\longrightarrow\mathbb P^2
\]
has image an irreducible rational curve \(C\).  A generic target line
pulls back to a divisor of degree \(b\).  If
\[
\delta=\deg C,\qquad
\nu=[\mathbb C(\mathbb P^1):\mathbb C(C)],
\]
then the same divisor has degree \(\delta\nu\), proving
\[
b=\delta\nu.
\]

No exclusion theorem, Jacobian-Conjecture hypothesis, or numerical
experiment enters this enumeration.

## Audit boundary

This check validates the fourteen **leading rows** after the elementary
integer enumeration.  It does not validate the candidate 68-leaf
incidence manifest.  That manifest uses additional orbit,
Hilbert--Burch, and boundary classifications and remains subject to the
blinded comparison.

The source inspection and this note were prepared with AI assistance.
This is not peer review.
