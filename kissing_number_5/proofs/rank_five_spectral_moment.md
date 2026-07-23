# A sharp rank-five spectral-moment constraint

## Status

This note proves a new necessary condition for any putative 41-point code
and shows that the exact all-harmonic three-point pseudo-distribution in this
repository violates it.  It is a **rank-aware relaxation cut**, not an upper
bound for the kissing number: a separate numerical reoptimization on the
same finite support can evade the cut.

The result is useful because it isolates information genuinely missing from
the complete ordinary and Bachoc--Vallentin three-point harmonic
inequalities.  It also records the exact six-cycle Newton identity forced by
rank five.

## A sharp spectral lemma

Let \(M\succeq0\) have rank at most \(r\), and write
\[
 p_j=\operatorname{tr}(M^j),\qquad
 m=\frac{p_1}{r},\qquad
 V=p_2-\frac{p_1^2}{r}.
\]
Pad the nonzero spectrum of \(M\) by zeros to obtain \(r\) nonnegative
eigenvalues \(\lambda_1,\ldots,\lambda_r\), and put
\(z_i=\lambda_i-m\).  Then
\[
 \sum_i z_i=0,\qquad \sum_i z_i^2=V
\]
and
\[
 p_3-\frac{p_1^3}{r^2}-\frac{3p_1}{r}V
 =\sum_i z_i^3.                                      \tag{1}
\]

For any \(z\in\mathbb R^r\) with zero sum,
\[
\left|\sum_i z_i^3\right|
\leq \frac{r-2}{\sqrt{r(r-1)}}
          \left(\sum_i z_i^2\right)^{3/2}.            \tag{2}
\]
To prove (2), normalize \(\sum z_i^2=1\).  The compact intersection of the
unit sphere and the zero-sum hyperplane has a maximizer.  Lagrange
multipliers show that every coordinate of a maximizer is a root of one
quadratic, so there are at most two coordinate values.  If the positive
value occurs \(k\) times, the constraints determine the two values and give
\[
 \sum_i z_i^3
 =\frac{r-2k}{\sqrt{r\,k(r-k)}}.
\]
For \(1\leq k\leq r-1\), this is maximized at \(k=1\), where it equals the
coefficient in (2).  Applying the same maximum bound to \(-z\) supplies the
lower bound and hence the absolute value.  Scaling proves the assertion.
The same argument covers a stationary point having only one coordinate
value, because then \(V=0\).

For \(r=5\), define
\[
 V=p_2-\frac{p_1^2}{5},\qquad
 D=p_3-\frac{p_1^3}{25}-\frac{3p_1}{5}V.
\]
Equations (1)--(2) give the sharp necessary inequality
\[
\lvert D\rvert\leq\frac{3}{2\sqrt5}V^{3/2}.          \tag{3}
\]
The equivalent entirely rational form is
\[
20D^2\leq9V^3.                                      \tag{4}
\]
No strict-positivity or full-rank hypothesis is used; zero eigenvalues are
included by padding.  Equality in (3), when \(V>0\), has one centered
eigenvalue \(2\sqrt{V/5}\) and four centered eigenvalues
\(-\sqrt{V/20}\), provided the resulting eigenvalues are nonnegative.

The cubic correction in (3) cannot be omitted.  The exact 11-point code
\[
 \{\pm e_1,\ldots,\pm e_5\}
 \ \cup\
 \left\{\frac{(1,1,1,1,1)}{\sqrt5}\right\}
 \subset S^4                                             \tag{5}
\]
has maximum inner product \(1/\sqrt5<1/2\).  Its frame operator is
\[
 2I+\frac15J,
\]
with spectrum \(3,2,2,2,2\).  Hence \(V=4/5\) and \(D=12/25>0\), and
(3) is an equality.

## Translation to fixed-cardinality three-point moments

For a code of size \(N\), use the normalization of
`fixed41_three_point_formulation.md` and put
\[
 A=\int q^2\,d\alpha(q),\qquad
 T=\int uvt\,d\nu(u,v,t).
\]
Expanding closed walks of lengths two and three in its Gram matrix \(G\)
gives
\[
 \operatorname{tr}(G^2)=N(1+A),\qquad
 \operatorname{tr}(G^3)=N(1+3A+T).                  \tag{6}
\]
The three terms \(3A\) are the three ways exactly two indices in a
length-three closed walk can coincide.

At \(N=41\), set
\[
 \delta=A-\frac{36}{5},\qquad
 E=T-\frac{1116}{25}-\frac{108}{5}\delta.
\]
The Welch inequality is precisely \(\delta\geq0\), while (3) becomes
\[
\lvert E\rvert\leq\frac32\sqrt{\frac{41}{5}}\,
                 \delta^{3/2}.                      \tag{7}
\]
Its equivalent rational squared form is
\[
 20E^2\leq369\delta^3.                               \tag{8}
\]

For the exact all-harmonic pseudo-distribution
`fixed41_bv_fullradial_k16_pseudodistribution.json`, direct rational
summation gives
\[
\begin{aligned}
 A&=\frac{5767796592200083}{800000000000000},\\
 T&=\frac{143604943059355723}{3200000000000000},\\
 \delta&=\frac{7796592200083}{800000000000000},\\
 E&=\frac{416587466342759}{16000000000000000}>0.
\end{aligned}
\]
It violates (8) by the strictly positive rational number
\[
 20E^2-369\delta^3
 =
 \frac{
 6766924411210776056912808275188861748410597
 }{
 512000000000000000000000000000000000000000000
 }>0.                                                \tag{9}
\]
Equivalently, in unnormalized spectral variables the violation is
\[
 20D^2-9V^3
 =
 \frac{
 11375199935245314551670430710592476599078213557
 }{
 512000000000000000000000000000000000000000000
 }>0.                                                \tag{10}
\]
Thus the pseudo-distribution cannot be the two- and three-point marginals
of any common rank-five Gram matrix, despite satisfying all of the harmonic
conditions proved in `fixed41_bv_all_harmonics.md`.

The same cut also rejects the stronger integral triple pseudo-incidence in
`weighted_residual_barrier.md`.  For that witness the exact values are
\[
\begin{aligned}
A&=\frac{5933759}{820000},&
T&=\frac{117553701249}{2562500000},\\
V&=\frac{29759}{20000},&
D&=\frac{1154968749}{62500000},
\end{aligned}
\]
and
\[
20D^2-9V^3
=\frac{170004739142977028253}{25000000000000000}>0.
\]
Thus the rank-five cut supplies a common-source obstruction that neither
triangle PSD nor the complete total-degree-two BV blocks detect.

## The six-point trace identity

For any symmetric matrix with eigenvalue power sums \(p_j\), the sum of all
principal \(6\times6\) minors is the elementary symmetric polynomial
\(e_6\).  Newton's identities give
\[
\begin{aligned}
720e_6={}&p_1^6-15p_1^4p_2+40p_1^3p_3
 +45p_1^2p_2^2-90p_1^2p_4\\
&-120p_1p_2p_3+144p_1p_5-15p_2^3
 +90p_2p_4+40p_3^2-120p_6.                         \tag{11}
\end{aligned}
\]
Every rank-five Gram matrix has every principal \(6\times6\) determinant
zero, so both sides of (11) vanish.

Identity (11) is exact but does not by itself close the kissing problem.
The quantities \(p_4,p_5,p_6\) are respectively four-, five-, and six-cycle
moments.  They are not determined by a pair distribution or by a
three-point pseudo-distribution.  Moreover, their coefficients in (11)
have mixed signs, so replacing each independently by a one-sided trace
bound is invalid.  A successful use of (11) needs a common-source
higher-point certificate controlling these cycle moments jointly.

## Exact scope and remaining gap

The proved contribution is:

1. the sharp universal rank-five inequality (3);
2. its exact fixed-41 form (7);
3. the exact rational refutation (9) of the stored all-harmonic
   three-point pseudo-distribution;
4. the exact six-cycle identity (11).

This does **not** prove that every fixed-41 three-point measure satisfying
the harmonic constraints violates (7).  A discovery-only numerical
reoptimization on the same seven-point radial grid, imposing harmonic
blocks through degree 16, found a feasible direction from the stored
pseudo-distribution along which \(E\) changes sign.  Convex interpolation
therefore gives a numerical finite-degree feasible point with \(E=0\), which
satisfies (7).  This observation has not been rationalized and no theorem
relies on it.  The exact remaining gap is to combine (7) or (11) with a
further universal geometric constraint that rules out every 41-point
marginal system, rather than only the stored pseudo-distribution.

## Reproduction

From the project directory run

```sh
python3 verifiers/verify_rank_five_spectral_moment.py
python3 -m unittest tests.test_rank_five_spectral_moment -v
```

The verifier uses only the Python standard library and exact
`fractions.Fraction` arithmetic.
