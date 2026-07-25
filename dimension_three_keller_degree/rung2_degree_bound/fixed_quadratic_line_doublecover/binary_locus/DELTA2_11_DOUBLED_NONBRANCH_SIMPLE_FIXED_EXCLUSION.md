# Provisional exclusion of the doubled-nonbranch simple-fixed
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T19:15:08Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

Put
\[
h=(p+q)^2,\qquad
R=(p+q)(Ap^2+Bpq+Cq^2).                         \tag{1}
\]
There is no Keller counterexample in this binary fixed-quadratic
line-double-cover leaf on the exact open
\[
(A-2B)(2B-C)(A-B+C)\ne0.                        \tag{2}
\]

The only nontrivial stabilizer of the marked branch pair and the
doubled nonbranch root is \(p\leftrightarrow q\).  It swaps \(A,C\)
and fixes \(B\), so (1)--(2) cover the coefficient projective plane
without an unrecorded modulus.

For
\[
P=hp^2,\qquad Q=hq^2,\qquad
\alpha=[Q,R],\quad\beta=-[P,R],\quad\gamma=[P,Q],
\]
one has
\[
\gcd(\alpha,\beta,\gamma)=2(p+q)^2.              \tag{3}
\]
Each removed divisor is a genuine deeper-incidence mutation:
\[
\begin{array}{c|c}
A=2B&2q(p+q)^2\\
C=2B&2p(p+q)^2\\
A-B+C=0&2(p+q)^3.
\end{array}                                      \tag{4}
\]
Thus none is silently included in the exact-\(\delta=2\) theorem.

## Generic contact chart

Set
\[
\Delta=4AC-B^2.                                  \tag{5}
\]
The \(E_7\) coefficient matrix for
\[
\alpha U+\beta V+\gamma W=0,\qquad
\deg(U,V,W)=(2,2,1),
\]
has a rank-six minor
\[
-768(A-2B)(2B-C)\Delta(A-B+C)^2.                \tag{6}
\]
On \(\Delta\ne0\), a polynomial-scaled basis for its two-dimensional
kernel is
\[
\begin{aligned}
N_1={}&\big(
-2(B-8C)p^2+12Cpq,\\
&\qquad -6Bpq-4(2B-C)q^2,\ 3\Delta p\big),\\
N_2={}&\big(
4(A-2B)p^2-6Bpq,\\
&\qquad 12Apq+2(8A-B)q^2,\ 3\Delta q\big).
                                                               \tag{7}
\end{aligned}
\]
The two syzygies in (7) are checked literally, so (6) proves that
they span the complete \(E_7\) tangent kernel.

Write a tangent as \(sN_1+tN_2\), and lift the \(r\)-coefficient of
\(E_6\) to the linear contact map in
\[
(X,Y,Z,x_5,y_5)=(s^2,st,t^2,x_5,y_5).
\]
A selected five-by-five minor is
\[
26542080(A-2B)(2B-C)\Delta^3(A-B+C)^3.           \tag{8}
\]
It is nonzero on (2) when \(\Delta\ne0\).  Therefore the contact
equation forces
\[
s=t=x_5=y_5=0.                                  \tag{9}
\]

## Fresh \(\Delta=0\) chart

The divisor \(\Delta=0\) is internal to the exact open and cannot be
discarded or reached by specializing (7).  On this divisor,
\[
A=\frac{B^2}{4C}.                                \tag{10}
\]
Exactness implies \(C\ne0\): if \(C=0\), then \(\Delta=0\) gives
\(B=0\), contradicting \(2B-C\ne0\).

A fresh polynomial tangent basis is
\[
\begin{aligned}
N'_1={}&\big(
(B-8C)p^2-6Cpq,
3Bpq+2(2B-C)q^2,\ 0\big),\\
N'_2={}&\big(
10Cp^2+8Cpq,\ -2Cpq,
(2B-C)(Bp+2Cq)\big).                            \tag{11}
\end{aligned}
\]
The fresh \(E_7\) rank-six minor is
\[
-\frac{16B(B-8C)(B-2C)^4(2B-C)^2}{C^3}.        \tag{12}
\]
The corresponding contact determinant is
\[
-\frac{3840B(B-8C)(B-2C)^6(2B-C)^4}{C}.        \tag{13}
\]
These factors are exactly controlled by (2), because on (10)
\[
A-2B=\frac{B(B-8C)}{4C},\qquad
A-B+C=\frac{(B-2C)^2}{4C}.                      \tag{14}
\]
Thus (12)--(13) are nonzero throughout the exact
\(\Delta=0\) chart.  There is no contact survivor on the internal
pivot divisor.

## Constant \(E_6\) block and exit

After (9), or its primed analogue, the remaining constant part of
\(E_6\) is the coefficient map with columns
\[
\alpha p,\quad\alpha q,\quad
\beta p,\quad\beta q,\quad\gamma.
\]
Its first five coefficient rows have determinant
\[
-512(A-2B)(2B-C)(A-B+C)^2.                      \tag{15}
\]
Hence every nonlinear \(r\)-coefficient vanishes.  All nonlinear
terms are binary.

The established all-binary exit now applies.  Triangularize a
nonzero \(r\)-coefficient of the invertible linear part to the third
target coordinate.  Over the resulting one-variable function field,
the first two components form a plane Keller map of degree at most
four.  The unconditional plane low-degree theorem, generic-degree
descent, and the birational Keller theorem imply that the original
map is a polynomial automorphism.  This uses no form of the full
plane Jacobian Conjecture.

Because both contact charts have full rank, there is no nonzero
\(E_6\) survivor and therefore no lower-coefficient branch requiring
an \(E_5,E_4,\ldots\) solve.

## Verification

Run

```text
./verify_delta2_11_doubled_simple_fixed_strict.sh
```

The strict wrapper requires exact whitelisted transcripts from:

- SymPy, reconstructing all boundary gcds, the residual stabilizer,
  both \(E_7\) bases, both contact determinants, and the constant
  block;
- an independent PARI/GP expansion of the same objects, with the
  \(\Delta=0\) chart recomputed rather than specialized.

The field/descent input for the all-binary exit is recorded in
`../../WORKING_FIXED_CUBIC_LINE_ROW.md`, Section 4.

The note and programs were prepared with AI assistance.  They are not
peer reviewed, and the exact checks certify only the algebra encoded
in the scripts.
