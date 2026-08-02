# Route C: optimized affine--Voronoi high-radius band

**Scope:** exact optimization of the affine pullback method in
`route_c_explicit_high_radius_band.md`, using the full weighted Jung defect.
No literature or web search was used.

## 1. Result and method boundary

Let \(K\subset\mathbb R^4\) be compact, let
\(D=\operatorname {diam}K>0\), and let \(R\) be its circumradius.  The
affine--Voronoi method proves the following clean rational band:

\[
 \boxed{
 R^2>\left(\frac25-\frac1{728}\right)D^2
 \quad\Longrightarrow\quad
 K\text{ has five parts of diameter below }D.}            \tag{1}
\]

The contraction at the rational endpoint is explicit.  Put

\[
 \begin{aligned}
 T_0&=\frac{25}{713},&
 \sigma_-&=\frac{25}{713},&
 \sigma_+&=\frac{15}{713},&
 t_0&=\frac7{17}.
 \end{aligned}
\]

Then the five parts in (1) have squared diameter at most

\[
 \Gamma_{728}^2=
 4\frac{728}{713}
 \left(
  \frac{5766141}{6462040}
  -\frac25\sqrt{\frac{15323}{5848}}
 \right)<1.                                               \tag{2}
\]

Numerically, only for orientation,
\(\Gamma_{728}^2\approx0.999910319\).  The exact positive square margin
proving (2) is displayed in Section 5.

There is also an exact algebraic supremum for the fully optimized
**scalar spectral version** of this method.  Define

\[
 \delta_{\rm aff}=0.0013742502821037648302\ldots .         \tag{3}
\]

exactly as the unique root in \((1/728,1/727)\) of

\[
\begin{aligned}
 \mathcal K(d)={}&
 -12150000000000000d^{10}
 +3786750000000000d^9
 -453330000000000d^8\\
 &+23578200000000d^7
 +129195000000d^6
 -87853600000d^5\\
 &+3469325000d^4
 +41036875d^3
 -3800875d^2
 +49525d-61.                                               \tag{4}
\end{aligned}
\]

For every Jung defect \(\delta<\delta_{\rm aff}\), the optimized certificate
is strict; at \(\delta=\delta_{\rm aff}\), its diameter upper bound is exactly
one.  The root is irrational, so no largest rational number equals this
supremum.  The convenient value \(1/728\) is the largest reciprocal integer
below it, while \(1/727\) is already beyond the method boundary.
Equivalently, the largest band certified by this relaxation is

\[
 R^2>\left(\frac25-\delta_{\rm aff}\right)D^2.             \tag{4a}
\]

The boundary is a limitation of a precisely identified relaxation: after
pullback, retain only the sharp scalar spectral bounds on the affine metric,
then enclose each Voronoi cell by a ball centered on its model anchor ray.
It is not evidence that nearest-anchor cells or the Borsuk assertion fail
beyond (3).  An anisotropic analysis retaining the whole perturbation matrix
could improve the band.

## 2. Full weighted defect and the exact metric budget

Scale to \(D=1\), translate the circumcenter to zero, and set

\[
 \delta=\frac25-R^2.
\]

Choose a balanced contact representation and pad it to five contact anchors
\(a_i\) and weights \(\lambda_i\):

\[
 |a_i|^2=R^2,\qquad
 \lambda_i\ge0,\qquad
 \sum_i\lambda_i=1,\qquad
 \sum_i\lambda_i a_i=0.
\]

The padding may initially have zero weights; the defect estimate below will
prove that every weight is above \(1/8\) in the range used here.  Put

\[
 h_i=\lambda_i-\frac15,qquad
 W=\frac12\sum_i h_i^2,qquad
 \alpha_{ij}=1-|a_i-a_j|^2\quad(i\ne j),                  \tag{5}
\]

and set \(\alpha_{ii}=0\).  The Jung defect identity is

\[
 \boxed{
 \delta=W+\sum_{i<j}\lambda_i\lambda_j\alpha_{ij}}.        \tag{6}
\]

The common contact norm and the balance relation give the additional row
identities

\[
 \boxed{
 \sum_{j\ne i}\lambda_j\alpha_{ij}
 =\frac15+2\delta-\lambda_i}.                             \tag{7}
\]

Indeed,

\[
 \sum_j\lambda_j|a_i-a_j|^2=2R^2=\frac45-2\delta,
\]

and expanding the left side gives (7).

Let

\[
 T=\sum_{i<j}\alpha_{ij}.                                 \tag{8}
\]

The next estimate optimizes over the weights rather than replacing every
weight by an arbitrary coarse lower bound.

**Lemma 1 (sharp weighted edge budget).**  If
\(0\le\delta\le1/727\), then

\[
 \boxed{T\le\Phi(\delta):=\frac{25\delta}{1-15\delta}}.   \tag{9}
\]

The bound is attained by a genuine balanced contact simplex.

**Proof.**  The case \(\delta=0\) follows immediately from (6), so suppose
\(\delta>0\).  Let \(x\le y\) be the two smallest weights and put
\(p=xy=\min_{i<j}\lambda_i\lambda_j\).  Since
\(W\le\delta\le1/727\),

\[
 |h_i|^2\le2W\le\frac2{727}<\frac9{1600},
\]

so every weight is above \(1/8\).  In particular
\(2\sqrt p>1/4\) (and \(x+y>1/4\)), which is exactly what is needed for
the monotonicity down to the endpoint \(s=2\sqrt p\) in the next step.

For fixed \(x,y\), Cauchy--Schwarz on the other three weights gives

\[
 W\ge\frac12\left(
 x^2+y^2+\frac{(1-x-y)^2}{3}-\frac15
 \right).                                                 \tag{10}
\]

Write \(s=x+y\).  At fixed \(p=xy\), the right side of (10) has derivative
\((4s-1)/3>0\) with respect to \(s\).  Since \(s\ge2\sqrt p\), it is at
least its value when \(x=y=\sqrt p\).  The product of the two smallest
weights is at most \(1/25\): if \(x\le y\), then \(1\ge x+4y\), and
maximizing \(xy\) under these inequalities gives \(x=y=1/5\).  Thus write

\[
 \sqrt p=\frac15-u,\qquad u\ge0.
\]

Substitution in (10) yields

\[
 W\ge\frac53u^2.                                         \tag{11}
\]

On the other hand, (6) and the definition of \(p\) give

\[
 pT\le\sum_{i<j}\lambda_i\lambda_j\alpha_{ij}
 =\delta-W.
\]

Consequently

\[
 T\le
 \frac{\delta-\frac53u^2}{(\frac15-u)^2}.                \tag{12}
\]

The derivative of the right side has the sign of
\(\delta-u/3\).  Equations (11) and \(W\le\delta\) give
\(0\le u\le\sqrt{3\delta/5}\).  Since \(\delta<1/15\), one has
\(3\delta<\sqrt{3\delta/5}\), so the maximum over this interval is at
\(u=3\delta\), and its value there is

\[
 \frac{\delta-15\delta^2}{(\frac15-3\delta)^2}
 =\frac{25\delta}{1-15\delta}.
\]

This proves (9).

Sharpness is important for identifying the eventual barrier.  Take

\[
 \lambda_0=\lambda_1=\frac15-3\delta,qquad
 \lambda_2=\lambda_3=\lambda_4=\frac15+2\delta,           \tag{13}
\]

and let the only nonzero edge defect be

\[
 \alpha_{01}=\frac{25\delta}{1-15\delta}.                \tag{14}
\]

Then \(W=15\delta^2\), while

\[
 \lambda_0\lambda_1\alpha_{01}
 =\delta(1-15\delta),
\]

so (6) is an equality.  Also

\[
 \lambda_1\alpha_{01}=5\delta
 =\frac15+2\delta-\lambda_0,
\]

and the other row equations in (7) are zero on both sides.

To see that these data are Euclidean, use the metric construction in the
next section.  Its least eigenvalue is \(1-\alpha_{01}>0\) in the present
range, so it realizes five points with the prescribed distances.  Center
them at their \(\lambda\)-weighted barycenter.  Equations (7) then imply
that all five squared norms are \(2/5-\delta\).  Positive balance makes this
sphere the minimum enclosing sphere.  All distances are at most one and
nine of them equal one, so the resulting set has diameter one. \(\square\)

## 3. Sharp asymmetric spectral control

Let

\[
 H=\{z\in\mathbb R^5:\mathbf1^{\mathsf T}z=0\},\qquad
 P=I-\frac15J,
\]

and use the regular unit-edge model vertices

\[
 v_i=\frac1{\sqrt2}Pe_i.
\]

Translate the actual anchors to their unweighted centroid, and let
\(A:H\to\mathbb R^4\) be the linear map sending \(v_i\) to those centered
anchors.  If \(M=A^{\mathsf T}A\) is its pulled-back metric, the centered
distance-Gram identity gives

\[
 \boxed{M-I_H=(P\mathcal A P)|_H,}                         \tag{15}
\]

where \(\mathcal A=(\alpha_{ij})\).  One can also verify (15) on every model
edge: for \(r=(e_i-e_j)/\sqrt2\),

\[
 r^{\mathsf T}P\mathcal A Pr=-\alpha_{ij}.
\]

The following asymmetric estimate is sharper than bounding both signs by
the same operator norm.

**Lemma 2 (sharp spectral interval).**  For every \(z\in H\),

\[
 -T|z|^2\le z^{\mathsf T}P\mathcal A Pz
 \le\frac35T|z|^2.                                       \tag{16}
\]

Both constants are attained by the single-edge family (14).

**Proof.**  Normalize \(|z|=1\).  Since the off-diagonal entries of
\(\mathcal A\) are nonnegative,

\[
 z^{\mathsf T}\mathcal A z=2\sum_{i<j}\alpha_{ij}z_i z_j.
\]

For every pair, \(-2z_i z_j\le z_i^2+z_j^2\le1\), proving the lower
bound.  For a same-sign pair \(z_i,z_j\), the other three coordinates sum
to \(-(z_i+z_j)\).  Hence

\[
 1\ge z_i^2+z_j^2+\frac{(z_i+z_j)^2}{3}
 \ge\frac{10}{3}z_i z_j,
\]

so \(2z_i z_j\le3/5\), proving the upper bound.

If only \(\alpha_{01}=T\) is nonzero, \(e_0-e_1\) is an eigenvector of
\(P\mathcal A P\) with eigenvalue \(-T\).  The vector
\((3,3,-2,-2,-2)\) is an eigenvector with eigenvalue \(3T/5\).
\(\square\)

Combining Lemmas 1 and 2, every contact simplex with defect \(\delta\) has

\[
 (1-\sigma_-)|z|^2\le|Az|^2\le(1+\sigma_+)|z|^2,          \tag{17}
\]

where it is valid to take

\[
 \sigma_-=\Phi(\delta),\qquad
 \sigma_+=\frac35\Phi(\delta).                           \tag{18}
\]

This implication is sharp: (13)--(14) attains both endpoint eigenvalues.

## 4. Optimized asymmetric Voronoi-cell lemma

Suppose a pulled-back metric \(Q(z)=|Az|^2\) satisfies (17), and every point
under consideration lies within actual distance one of every anchor.  For a
point \(z\) in the actual nearest-\(v_i\) cell, put

\[
 d_j=|z-v_j|^2.
\]

Then \(Q(z-v_i)\le Q(z-v_j)\le1\).  The two sides of (17) give the sharper
comparison

\[
 d_i-d_j\le
 \frac1{1-\sigma_-}-\frac1{1+\sigma_+}=:q,                \tag{19}
\]

because

\[
 d_i\le\frac{Q(z-v_i)}{1-\sigma_-}
 \le\frac{Q(z-v_j)}{1-\sigma_-},
 \qquad
 d_j\ge\frac{Q(z-v_j)}{1+\sigma_+}.
\]

The unit-ball inequalities also give \(d_j\le1/(1-\sigma_-)\).  Here is the
coordinate-interval calculation with the new slack.  Put

\[
 r^2=|z|^2,\qquad s=z_i,\qquad
 a=\frac{\sigma_-}{1-\sigma_-}.
\]

Since \(|v_j|^2=2/5\) and
\(\langle z,v_j\rangle=z_j/\sqrt2\), the ball and Voronoi inequalities give

\[
 z_j\ge\ell:=\frac{r^2-\frac35-a}{\sqrt2},\qquad
 z_j\le U:=s+\frac q{\sqrt2}.                              \tag{19a}
\]

All five model coordinates sum to zero, so \(U\ge0\).  Summing the five
nonnegative products \((U-z_j)(z_j-\ell)\) yields

\[
 0\le-r^2-5U\ell,
\]

and hence, with \(B=3+5a\),

\[
 r^2\le\frac{BU}{\sqrt2+5U}.                              \tag{19b}
\]

For a center parameter \(t>0\), use \(s=U-q/\sqrt2\) to obtain

\[
\begin{aligned}
 |z-tv_i|^2
 &=r^2-\sqrt2ts+\frac25t^2\\
 &\le\frac{BU}{\sqrt2+5U}-\sqrt2tU+tq+\frac25t^2.
\end{aligned}
\]

For \(0<t\le B/2\), the maximum over \(U\ge0\) of the first two terms is

\[
 \frac{B+2t-2\sqrt{2Bt}}5.
\]

Thus

\[
 |z-tv_i|^2\le\rho^2(\sigma_-,\sigma_+,t),                 \tag{20}
\]

where, for \(0<t\le B/2\),

\[
\begin{aligned}
 a&=\frac{\sigma_-}{1-\sigma_-},
 &B&=3+5a,\\
 q&=\frac1{1-\sigma_-}-\frac1{1+\sigma_+},
 &\rho^2&=
 \frac{B+2t-2\sqrt{2Bt}}5+qt+\frac25t^2.                 \tag{21}
\end{aligned}
\]

Mapping the ball in (20) forward gives

\[
 \operatorname {diam}(C_i)^2
 \le4(1+\sigma_+)\rho^2(\sigma_-,\sigma_+,t).             \tag{22}
\]

Now write \(T=\Phi(\delta)\), and insert the sharp values

\[
 \sigma_-=T,qquad \sigma_+=\frac35T.
\]

Then

\[
 B=\frac{3+2T}{1-T},qquad
 q=\frac{8T}{(1-T)(5+3T)}.                                \tag{23}
\]

For fixed \(T\), the right side of (21) has a unique minimizing \(t\) in
\((0,B/2)\).  Its derivative vanishes exactly when

\[
 2+5q+4t=\sqrt{\frac{2B}{t}}.                             \tag{24}
\]

The derivative is strictly increasing from \(-\infty\), and at \(B/2\) it
is positive.  Thus (24) really identifies the global minimum, including the
branch \(t\ge B/2\), where the preceding one-variable maximum occurs at its
boundary and the radius bound increases.

For \(0\le T\le25/712\), the minimizer is below \(1/2\): at \(t=1/2\),
the derivative is positive because \(B<4\).  On this common interval,
the combined first term in (21) is
\[
 \frac{(\sqrt B-\sqrt{2t})^2}{5},
\]
which increases with \(T\) because \(B>2t\).  The slack \(q\) and the
forward factor \(1+3T/5\) also increase with \(T\).
Hence the optimized squared-diameter bound

\[
 F_{\rm opt}(T)=
 \min_t 4\left(1+\frac35T\right)\rho^2(T,t)               \tag{25}
\]

is continuous and strictly increasing in the range containing its crossing
of one.  Explicitly, for \(T_2>T_1\), evaluate the \(T_1\) envelope at the
minimizer for \(T_2\): pointwise strict increase makes the \(T_2\) value
larger, while the \(T_1\) minimum can only be smaller.

## 5. Exact rational certificate at \(\delta=1/728\)

At the weak endpoint \(\delta=1/728\), (9) gives

\[
 T=\frac{25}{713},\qquad
 \sigma_-=\frac{25}{713},\qquad
 \sigma_+=\frac{15}{713}.
\]

Consequently

\[
 a=\frac{25}{688},\qquad
 B=\frac{2189}{688},\qquad
 q=\frac{3565}{62608}.
\]

Choose the rational center parameter \(t=7/17\).  Equation (21) becomes

\[
 \rho^2=
 \frac{5766141}{6462040}
 -\frac25\sqrt{\frac{15323}{5848}}.                       \tag{26}
\]

To prove \(4(728/713)\rho^2<1\), move the radical to the right.  The positive
rational side is

\[
 \frac{5766141}{6462040}-\frac{713}{2912}
 =\frac{117149693}{180937120}>0.
\]

The exact squared margin is

\[
 \frac4{25}\frac{15323}{5848}
 -\left(\frac{117149693}{180937120}\right)^2
 =\frac{186180822731}{6547648278778880}>0.                \tag{27}
\]

This proves (2).  Under the strict radius hypothesis (1), the actual defect
is below \(1/728\), so every preceding metric and cell bound is no larger
than this endpoint calculation and the contraction remains uniform.

## 6. Exact algebraic optimum of the scalar certificate

This section proves that (3)--(4) are the exact boundary of the quantified
method, not a numerical guess.

Let \(x=T\), let

\[
 L=(1-x)(5+3x),\qquad
 c=L+20x+2tL.                                              \tag{28}
\]

After clearing the positive denominators in the optimality equation (24),
one obtains

\[
 \mathcal D(x,t)=
 2tc^2-(3+2x)(1-x)(5+3x)^2=0.                             \tag{29}
\]

At a crossing of one in (25), use (29) to replace

\[
 \sqrt{2Bt}=\frac{(3+2x)(5+3x)}{c}.
\]

If

\[
\begin{aligned}
 E_0={}&(3+2x)(5+3x)c+2tLc
       -2(3+2x)(5+3x)L\\
     &+40xtc+2t^2Lc,
\end{aligned}
\]

then the threshold equation is

\[
 \mathcal E(x,t)=4(5+3x)E_0-25Lc=0.                      \tag{30}
\]

The exact resultant in \(t\) is

\[
 \operatorname {Res}_t(\mathcal D,\mathcal E)
 =2560(x-1)^6(2x+3)(3x+5)^{10}\mathcal H(x),              \tag{31}
\]

where

\[
\begin{aligned}
 \mathcal H(x)={}&23328x^{10}+500580x^9+3918240x^8
 +12827745x^7\\
 &+15615705x^6+1329277x^5-22203875x^4
 -7724125x^3\\
 &+11336875x^2+5046875x-190625.                           \tag{32}
\end{aligned}
\]

An exact Sturm calculation gives one positive root of \(\mathcal H\).  It is

\[
 x_{\rm aff}=0.0350793746604411442876\ldots .             \tag{33}
\]

The verifier independently forms the \(6\times6\) Sylvester determinant in
(31) and performs this Sturm count with rational arithmetic.

For an exact crossing bracket, \(x=25/713\), corresponding to
\(\delta=1/728\), lies below the root by (27).  At
\(x=25/712\), corresponding to \(\delta=1/727\), the unique minimizer of
(21) lies in

\[
 \frac{20583}{50000}<t_*<\frac{41167}{100000}.             \tag{34}
\]

Here

\[
 B=\frac{2186}{687},\qquad
 q=\frac{28480}{499449},\qquad
 \frac1{4(1+3x/5)}=\frac{178}{727}.
\]

For the squared derivative polynomial

\[
 \mathscr D_t(t)=t(2+5q+4t)^2-2B,
\]

the exact endpoint values are

\[
\begin{aligned}
 \mathscr D_t(20583/50000)
 &=-\frac{114498912483142307171}
 {649607561460937500000000}<0,\\
 \mathscr D_t(41167/100000)
 &=\frac{1680911010542506871263}
 {15590581475062500000000000}>0.
\end{aligned}
\]

Over this interval, monotonicity of the rational and radical terms gives an
exact lower bound for \(\rho^2\): evaluate its rational part at
\(20583/50000\) and its radical at \(41167/100000\).  The former minus
\(178/727\) is

\[
 \frac{2021119926251161}{3121556250000000}>0.
\]

After moving the radical, the required positive squared margin is

\[
 \frac{462920369845229531253847921}
 {9744113421914062500000000000000}>0,                     \tag{35}
\]

which proves \(F_{\rm opt}(25/712)>1\).  Thus the crossing lies strictly
between the two reciprocal-integer bands.

Finally substitute

\[
 x=\Phi(d)=\frac{25d}{1-15d}
\]

in (32).  Direct expansion gives

\[
 (1-15d)^{10}\mathcal H\left(\frac{25d}{1-15d}\right)
 =3125\mathcal K(d),                                      \tag{36}
\]

with \(\mathcal K\) exactly as in (4).  Its endpoint signs are

\[
\begin{aligned}
 \mathcal K(1/728)
 &=-\frac{62651547670389194403421}
 {2552077471698829010599936}<0,\\
 \mathcal K(1/727)
 &=\frac{2053339764513756372448918336}
 {41242416955341131537413053649}>0.
\end{aligned}                                             \tag{37}
\]

Modulo \(7\), the coefficients of \(\mathcal K\), in ascending order, are

\[
 (2,0,6,5,1,2,3,2,3,5,2),
\]

and its values at \(0,1,\ldots,6\) are

\[
 (2,3,6,6,1,4,3).
\]

The leading coefficient is nonzero modulo \(7\).  By the rational-root
theorem, the denominator of a rational root divides that leading
coefficient, so such a root would reduce to a root modulo \(7\), which the
displayed list rules out.  Hence
\(\delta_{\rm aff}\) is irrational.

The sharp family (13)--(14) attains

\[
 T=\Phi(\delta),\qquad
 \lambda_{\min}(M-I)=-T,qquad
 \lambda_{\max}(M-I)=\frac35T.
\]

Therefore neither the defect-to-spectral step nor its asymmetric constants
can be improved.  Equation (25) already optimizes every anchor-ray center
allowed by the scalar cell enclosure.  At \(\delta_{\rm aff}\) this envelope
equals one, establishing the claimed barrier for this exact relaxation.

## 7. Strictness and scope audit

1. A strict radius hypothesis with threshold \(\varepsilon\) means
   \(\delta<\varepsilon\); it never asks the endpoint cell bound itself to
   be strict.
2. The rational endpoint nevertheless has the strict integer margin (27),
   yielding a uniform contraction for all \(\delta<1/728\).
3. Metric invertibility is a conclusion: \(T\le25/713<1\) makes the lower
   factor in (17) positive.  No affine-independence assumption is hidden.
4. Every closed nearest-anchor cell obeys the same bound, so arbitrary tie
   breaking is valid.
5. For a bounded nonclosed set, closure preserves diameter and circumradius;
   restrict the compact-set partition.  The uniform factor in (2) preserves
   strictness even when a part does not attain its diameter.
