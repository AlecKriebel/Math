# Falling-factorial depth/cap hierarchy

## 1. Exact sampling transform

Fix a base edge and let \(X\) be a subset of its 39 residual vertices.
If a uniformly sampled local \(K_{m+2}\) retains \(m\) residual
vertices and \(x\) of them lie in \(X\), then

\[
\mathbb E\binom{x}{t}
=\frac{\binom mt}{\binom{39}t}\binom{|X|}{t}.
\]

Consequently, if a polynomial has the binomial-basis expansion

\[
F(X)=\sum_{t=0}^d c_t\binom Xt,\qquad d\le m,
\]
its unbiased local estimator is

\[
\widehat F_m(x)=
\sum_{t=0}^d c_t
\frac{\binom{39}t}{\binom mt}\binom xt.              \tag{1}
\]

This identity is exact and uses sampling without replacement.  It
applies base by base before averaging.

For two disjoint residual sets of sizes \(H,\Gamma\), with sampled sizes
\(h,g\),

\[
\mathbb E\!\left[\binom ha\binom gb\right]
=\frac{\binom m{a+b}}{\binom{39}{a+b}}
 \binom Ha\binom\Gamma b.                            \tag{2}
\]

Thus every polynomial in the joint binomial basis through total degree
\(m\) has an exact local estimator.

## 2. Full univariate families

An integer cap bound \(0\le\Gamma\le M\) gives, for every
\(a,b\ge0\) with \(a+b\le m\),

\[
\binom{\Gamma}{a}\binom{M-\Gamma}{b}\ge0.            \tag{3}
\]

A robust depth bound \(r\le H\le39\) similarly gives

\[
\binom{H-r}{a}\binom{39-H}{b}\ge0.                  \tag{4}
\]

Expand (3) or (4) in the binomial basis and apply (1).  These linear
rows strictly strengthen the first-moment cap/depth rows.  They are
valid without a finite inner-product alphabet; the alphabet is used
only to audit particular pseudodistributions.

The exact audit gives:

| witness | sample \(m\) | cap rows | cap violations | depth rows | depth violations |
|---|---:|---:|---:|---:|---:|
| 74-atom K6 | 4 | 98 | 11 | 7,840 | 292 |
| 53-atom K7 | 5 | 140 | 19 | 11,200 | 647 |

## 3. Smallest cap separator

For a base with \(q=-1/4\), common threshold \(1/2\), and the proved
capacity \(M=3\),

\[
F(\Gamma)=\binom{3-\Gamma}{2}
=3-2\Gamma+\binom{\Gamma}{2}\ge0.                   \tag{5}
\]

For K6, \(m=4\), and twice the estimator in (1) is

\[
6-39g+247\binom g2.
\]

Summed over the base edges of the 74-atom K6 mixture, its exact slack is

\[
-\frac{
2140627536537754284359159627634757733160323647
}{
541912518143754136926852222590400000000000000
}<0.                                                 \tag{6}
\]

For K7, \(m=5\), ten times the estimator is

\[
30-156g+741\binom g2.
\]

The exact slack on the 53-atom K7 mixture is

\[
-\frac{
6736085935767064980586375943764744500321533
}{
1055807876370816511457923512000000000000000
}<0.                                                 \tag{7}
\]

Thus both earlier product-valid local mixtures fail a degree-two
consequence of the same geometric capacity theorem.

## 4. Two-row exact obstruction to the available K7 pool

This subsection is deliberately pool-scoped.  The authenticated
1,782-column pool is not a complete list of rank-five quarter-grid K7
configurations.

Use base color \(q=0\), high color \(1/2\), and \(M=6\).  Consider

\[
F_1(\Gamma)=\Gamma\binom{6-\Gamma}{3},\qquad
F_2(\Gamma)=\binom{6-\Gamma}{5}.                     \tag{8}
\]

Both are nonnegative for every integer \(0\le\Gamma\le6\).  Their
binomial expansions are

\[
\begin{aligned}
F_1(X)&=10\binom X1-12\binom X2+9\binom X3-4\binom X4,\\
F_2(X)&=6-5\binom X1+4\binom X2-3\binom X3
       +2\binom X4-\binom X5.
\end{aligned}
\]

Let

\[
R_1(g)=\frac{10}{39}\widehat F_{1,5}(g),\qquad
R_2(g)=\frac{10}{3}\widehat F_{2,5}(g).
\]

These positive rescalings are integer-valued for \(g=0,\ldots,5\):

\[
\begin{array}{c|rrrrrr}
g&0&1&2&3&4&5\\ \hline
R_1&0&20&-188&1485&-9724&-65450\\
R_2&20&-110&748&-6545&78540&-1452990.
\end{array}
\]

Every column in the available pool has \(g\le3\) at every zero-colored
base.  On these four values,

\[
\frac{13}{12}R_1(g)+\frac14R_2(g)
=5-\frac{65}{6}g.                                   \tag{9}
\]

The fixed triangle marginal forces the expected local base and common
incidence counts

\[
E=\frac{39881456212194023}{5920000000000000},\qquad
G=\frac{81384983628501}{20800000000000}.
\]

Hence

\[
5E-\frac{65}{6}G
=-\frac{10305950358714927}{1184000000000000}<0.     \tag{10}
\]

Equations (8)--(10) are a two-row exact Farkas contradiction: both
averaged \(R_i\) must be nonnegative, while their positive combination
is the negative rational (10).  No floating solver output is used.

This is not a complete K7 obstruction.  An explicit additional rank-five
K7 atom has a zero-colored base with four common \(1/2\)-neighbors and
therefore lies outside the support property \(g\le3\).

## 5. Repair and first joint obstruction

Adding that explicit atom to the pool numerically repairs:

- all 140 cap-factorial rows;
- all 560 previously encoded depth/cap product rows; and
- the fixed pair/triple marginals.

The HiGHS solution uses the new atom with weight approximately
\(3.1748002936611563\cdot10^{-4}\).  This is numerical discovery only.

For the next level, use the negative-\((y+z)\) tail, which is disjoint
from the positive common-neighbor set.  Equations (2) recover every joint
moment through degree five.  Requiring a representing measure on

\[
\{(H,\Gamma)\in\mathbb Z^2:
H\ge7,\ 0\le\Gamma\le M,\ H+\Gamma\le39\}            \tag{11}
\]
is a finite linear moment extension, not a discretization of the sphere.

Already the stratum
\[
(q,b,M)=(-3/4,1/4,6)
\]
makes the augmented pool infeasible.  A three-multiplier exact Farkas ray
uses:

- coefficient \(-1\) on the triangle marginal of type \((1,5,5)\);
- coefficient \(-1\) on the joint moment equation \((a,b)=(0,1)\);
- coefficient \(2109\) on the joint moment equation \((a,b)=(4,1)\).

The number
\[
2109=\frac{5\binom{39}{5}}{39\binom74}
\]
makes every representing-state column nonnegative because \(H\ge7\).
For every one of the 1,782 pool columns and for the added atom, the
corresponding atom coefficient is exactly zero.  The right side is

\[
-\frac7{312}\nu_{(1,5,5)}
=-\frac{44522548762943617}{22510800000000000000}<0.
\]

This is an exact obstruction to that augmented local pool.  It is not a
proof against all rank-five K7 atoms, so it is not a kissing-number upper
bound.

## 6. What remains

The factorial hierarchy is a material strengthening of the original
product row, and it finds small exact defects in every current local
witness.  The strongest certified conclusion remains local:

- the two named K6/K7 mixtures are refuted;
- the original K7 discovery pool is refuted by a two-row exact ray;
- the once-augmented pool is refuted by a joint-moment exact ray.

A continuous upper bound would require either a complete support theorem
for the relevant K7 atoms or a separator whose atom inequality is proved
for every rank-five K7 Gram matrix on the full interval.
