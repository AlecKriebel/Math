# Rank-five fourth and sixth spectral moments

## Status

This note continues `rank_five_spectral_moment.md`.  It gives exact
rank-five constraints involving the four-cycle statistic
\(\operatorname{tr}(G^4)\), and an exact centered sixth-moment identity.
These are universal necessary conditions, but no bound on all possible
four-cycle measures strong enough to exclude 41 points is currently proved.

## Centered notation

Let \(M\succeq0\) have rank at most five.  Pad its spectrum with zeros to
five entries \(\lambda_1,\ldots,\lambda_5\), put
\[
 m=\frac{\operatorname{tr}M}{5},\qquad z_i=\lambda_i-m,
\]
and define
\[
 V=\sum_i z_i^2,\quad D=\sum_i z_i^3,\quad
 C_j=\sum_i z_i^j\quad(j=4,5,6).
\]
Thus \(V,D\) agree with the quantities in
`rank_five_spectral_moment.md`.

## Sharp fourth-moment bounds

For five real numbers of sum zero,
\[
 \frac7{30}V^2\leq C_4\leq\frac{13}{20}V^2.          \tag{1}
\]
When \(V=0\) this is immediate.  Otherwise normalize \(V=1\) and extremize
\(\sum z_i^4\) on the compact intersection
\[
 \sum z_i=0,\qquad \sum z_i^2=1.
\]
The constraint gradients are independent.  At a stationary point every
\(z_i\) is a root of one cubic
\[
 4x^3-2ax-b=0,
\]
so at most three distinct coordinate values occur.

If there are two values, one occurring \(k\) times and the other \(5-k\)
times, direct use of the two constraints gives
\[
 C_4=\frac{(5-k)^3+k^3}{25k(5-k)}.
\]
For \(k=1,4\) this is \(13/20\); for \(k=2,3\) it is \(7/30\).

If all three roots \(a,b,c\) occur, the missing quadratic coefficient gives
\(a+b+c=0\).  The only multiplicity partitions of five into three positive
parts are \(3+1+1\) and \(2+2+1\).  In the first case, comparison with the
weighted zero-sum condition forces the triply occurring root to be zero,
and \(C_4=1/2\).  In the second case the singly occurring root is zero, and
\(C_4=1/4\).  These four stationary values prove (1).  Repeated roots are
already included in the two-value case.

Both endpoints are exact.  The upper endpoint has centered spectrum
proportional to \((4,-1,-1,-1,-1)\); the lower endpoint has centered
spectrum proportional to \((3,3,-2,-2,-2)\).

## Hankel constraints through the fourth moment

The moment Gram matrix of the three functions \(1,z,z^2\) on the five
spectral points is
\[
 H_2=
 \begin{pmatrix}
 5&0&V\\
 0&V&D\\
 V&D&C_4
 \end{pmatrix}\succeq0.                              \tag{2}
\]
Its determinant gives
\[
 5VC_4\geq5D^2+V^3.                                 \tag{3}
\]
Together, the upper half of (1) and (3) recover the sharp cubic constraint
\[
 20D^2\leq9V^3.
\]
This factorization explains why the rank-five cubic inequality is stronger
than a generic PSD trace inequality: it combines a moment-matrix determinant
with the special five-equal-weight bound on \(C_4\).

In uncentered trace notation \(p_j=\operatorname{tr}(M^j)\),
\[
\begin{aligned}
V&=p_2-\frac{p_1^2}{5},\\
D&=p_3-\frac{3p_1p_2}{5}+\frac{2p_1^3}{25},\\
C_4&=p_4-\frac{4p_1p_3}{5}
       +\frac{6p_1^2p_2}{25}-\frac{3p_1^4}{125}.
\end{aligned}                                      \tag{4}
\]
Equations (1), (3), and (4) are rational polynomial inequalities in
\(p_1,p_2,p_3,p_4\).

## The exact centered sixth-moment identity

Apply Newton's sixth identity to the five centered values.  Since
\(C_1=0\) and their sixth elementary symmetric function is zero,
\[
-15V^3+90VC_4+40D^2-120C_6=0.
\]
Therefore
\[
 C_6=-\frac18V^3+\frac34VC_4+\frac13D^2.             \tag{5}
\]
This is the centered form of the vanishing sum of the principal
\(6\times6\) minors.

The moment Gram matrix of \(1,z,z^3\) is also PSD:
\[
\begin{pmatrix}
5&0&D\\
0&V&C_4\\
D&C_4&C_6
\end{pmatrix}\succeq0.
\]
Using (5), its determinant becomes the further exact inequality
\[
-\frac58V^4+\frac{15}{4}V^2C_4+\frac23VD^2-5C_4^2
\geq0.                                               \tag{6}
\]
Unlike a free sixth-moment relaxation, (6) has already eliminated \(C_6\)
using rank five.

More generally, the full spectral moment matrices
\[
 (p_{i+j})_{0\leq i,j\leq3}\succeq0,\qquad
 (p_{i+j+1})_{0\leq i,j\leq2}\succeq0               \tag{7}
\]
encode squares and eigenvalue-weighted squares.  Here \(p_0=5\).
The second matrix uses \(\lambda_i\geq0\).  Equations (5)--(7), together
with the Newton identity for \(e_6=0\), are a compact exact outer
description of the five-eigenvalue moment cone through degree six.  They
are necessary; the displayed low-order minors alone are not asserted to be
sufficient.

There is also a sharp warning about pure spectral continuation.  If
\(D=0\) and \(0\leq V\leq4m^2\), choose
\[
(z_1,\ldots,z_5)=(a,-a,a,-a,0),\qquad
a=\frac{\sqrt V}{2}.
\]
Then all \(m+z_i\) are nonnegative and have exactly the prescribed
\(p_1,V,D\).  Their higher moments automatically satisfy every spectral
Hankel, localizing, and Newton constraint.  Thus, once a three-point
relaxation reaches \(D=0\), no inequality involving only an abstract
completion of the five eigenvalues can reject it.  One must link \(p_4\)
back to the actual four-point Gram statistics.

## Four-cycle expansion for a spherical code

Let \(G\) be the Gram matrix of an \(N\)-point code.  In the normalized
pair and distinct-triple measures of
`fixed41_three_point_formulation.md`, put
\[
\begin{aligned}
A_2&=\int q^2\,d\alpha(q),&
A_4&=\int q^4\,d\alpha(q),\\
T&=\int uvt\,d\nu(u,v,t),&
U&=\int u^2v^2\,d\nu(u,v,t).
\end{aligned}
\]
Let \(\rho\) be the normalized all-distinct ordered quadruple measure,
with mass \((N-1)(N-2)(N-3)\), and define its four-cycle moment
\[
 R=\int
 (a\mathbin{\cdot}b)(b\mathbin{\cdot}c)
 (c\mathbin{\cdot}d)(d\mathbin{\cdot}a)\,d\rho.
\]
Partitioning the four positions of a closed walk by equality pattern gives
\[
 p_4=N\left(1+6A_2+A_4+4T+2U+R\right).              \tag{8}
\]
Indeed:

- the all-equal pattern contributes \(1\);
- the four \(3+1\) patterns and two adjacent \(2+2\) patterns contribute
  \(6A_2\);
- the alternating \(2+2\) pattern contributes \(A_4\);
- the four adjacent-repeat \(2+1+1\) patterns contribute \(4T\);
- the two opposite-repeat \(2+1+1\) patterns contribute \(2U\);
- the all-distinct pattern contributes \(R\).

The exact verifier independently enumerates every ordered quadruple of the
10-point cross polytope and checks (8).

## Integrated \(4\times4\) determinant compatibility

The same notation yields a useful exact constraint that eliminates two
apparently new four-point moments.  Define the disjoint-matching moment
\[
 W=\frac1N\sum_{\substack{a,b,c,d\\\text{all distinct}}}
       (a\mathbin{\cdot}b)^2(c\mathbin{\cdot}d)^2.
\]
Writing
\[
r_a=\sum_{b\ne a}(a\mathbin{\cdot}b)^2
\]
and partitioning pairs of unordered weighted edges into identical,
adjacent, and disjoint pairs gives
\[
 W=NA_2^2-4U-2A_4.                                \tag{9}
\]

For one four-point correlation matrix, permutation expansion gives
\[
\det G_4
=1-\sum_{\text{6 edges}}g_e^2
+2\sum_{\text{4 triangles}}g_{e_1}g_{e_2}g_{e_3}
+\sum_{\text{3 matchings}}g_e^2g_f^2
-2\sum_{\text{3 four-cycles}}\prod_{e\in C_4}g_e. \tag{10}
\]
Let
\[
L=(N-2)(N-3),\qquad
M=(N-1)(N-2)(N-3).
\]
Integrating (10) over the ordered all-distinct quadruple measure gives
\[
I_4:=\int\det G_4\,d\rho
=M-6LA_2+8(N-3)T+3W-6R.                          \tag{11}
\]
Every principal Gram matrix is PSD with diagonal one, so
\[
0\leq\det G_4\leq1.
\]
The upper inequality is Hadamard's determinant inequality and includes
singular boundary cases.  Therefore \(0\leq I_4\leq M\).

Substituting (9) into (11), and then into (8), makes \(A_4\) and \(U\)
cancel.  If
\[
B=1+\bigl(6-L\bigr)A_2+\frac{4N}{3}T
       +\frac N2A_2^2,
\]
then every genuine code satisfies the pair/triple-to-four-cycle interval
\[
\boxed{\quad NB\leq p_4\leq N\left(B+\frac M6\right).\quad} \tag{12}
\]
This is a common-source compatibility inequality: it is not available by
treating the pair, triple, and quadruple measures independently.

For \(N=41\), however, the width \(NM/6\) is too large to meet the sharp
spectral interval (1)--(3) in a contradictory way for the current
near-tight pseudo-moments.  Formula (12) is therefore certified progress,
not a 41-point exclusion.  A stronger route must exploit overlapping
four-point determinants or five- and six-minor identities rather than only
their scalar average.

## What remains

The pair and triple data determine every term of (8) except the
all-distinct four-cycle moment \(R\).  Consequently, even a complete
three-point harmonic relaxation cannot directly enforce (1), (3), or (6)
at the \(p_4\) level.  A useful next certificate must control \(R\) jointly
with its overlapping triples.  Bounding \(R\) independently by its
pointwise range loses precisely the common-source information that rank
five is meant to recover.

No universal bound on \(R\) strong enough to exclude a 41-point code is
proved here.  That is the explicit theorem-strength gap.

## Reproduction

Run

```sh
python3 verifiers/verify_rank_five_spectral_moment.py
python3 -m unittest tests.test_rank_five_spectral_moment -v
```

The checks use exact `fractions.Fraction` arithmetic only.
