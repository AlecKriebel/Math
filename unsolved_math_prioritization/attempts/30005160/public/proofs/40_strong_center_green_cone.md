# Proof 40  Strong center regions for the entire radial Green cone

Included dependencies: [Radial Green kernels and the bisubharmonic comparison cone](10_radial_green_reduction.md); [Elliptical disk differentiation and anisotropic Hessians](28_anisotropic_hessian.md); [Angular order under a common rotation](15_common_rotation.md); [A uniform center dominant coefficient region](13_dominant_center_boxes.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## 1. A paired Hessian lemma valid for every Green radius

Let `k_rho(z)=E K(z+rho Z)`, where `K(z)=|z|^2 log|z|`, `K(0)=0`, and `Z` is uniform on the unit circle. Put `D=partial_x^2-partial_y^2`. The exact formula is

`D k_rho(z)=2 cos(2 arg z) f_rho(|z|^2)`,

`f_rho(s)=(1-rho^2/s)_+`.                                       (1)

For `rho>0`, the expression is set to zero at `z=0`; it is continuous there and across `|z|=rho`. At `rho=0`, take `f_0=1` away from zero. Then (1) is the bounded weak derivative, with no point-mass term. The circular Green formula and this weak-derivative fact are accepted inputs. Alternatively, (1) follows directly from `D f(r)=(f''(r)-f'(r)/r) cos(2 arg z)` and the two explicit pieces of `k_rho`.

**Paired Hessian lemma.** Suppose a complex random variable `W` is centrally symmetric, so `W` and `-W` have the same law, and `|W|<=R<c`. Then, for every `rho>=0`,

`E D k_rho(c+W)>=0`.                                            (2)

At zero radius it also obeys

`E D K(c+W)>=2(c^2-R^2)/(c^2+R^2)`.                             (3)

### Proof

It is enough to pair a fixed `w=x+iy` with `-w`. Exchange the two if necessary to take `x>=0`. Put

`r^2=x^2+y^2`, `d_+=(c+x)^2+y^2`, `d_-=(c-x)^2+y^2`,

`h_+=((c+x)^2-y^2)/d_+`, `h_-=((c-x)^2-y^2)/d_-`.

Then `d_+>=d_-`, `h_+>=0`, and the exact unweighted half-sum is

`(h_++h_-)/2`

`=((c^2-r^2)(c^2-x^2+y^2))/((c^2+r^2)^2-4c^2 x^2)>=0`.          (4)

All denominators are positive because `c>r`. If `h_->=0`, the weighted sum `h_+ f_rho(d_+)+h_- f_rho(d_-)` is plainly nonnegative. If `h_-<0`, the function `f_rho` is nonnegative and nondecreasing, so

`h_+ f_rho(d_+)+h_- f_rho(d_-)`

`>=f_rho(d_-)(h_++h_-)>=0`.

By (1), twice this sum is `D k_rho(c+w)+D k_rho(c-w)`, proving (2).

For (3), at fixed `r`, the right side of (4) is nondecreasing in `x^2` on `[0,r^2]`. Its derivative with respect to `x^2` is

`2(c^2-r^2)^2(c^2+r^2)/((c^2+r^2)^2-4c^2 x^2)^2>=0`.

It is therefore at least its value at `x=0`, namely `(c^2-r^2)/(c^2+r^2)`, which is at least `(c^2-R^2)/(c^2+R^2)`. Pairing and the factor two in (1) prove (3).

The lemma requires only central symmetry and a support-radius bound. It does not assume that `W` is aligned or even an ellipse sum.

## 2. Full signed-anisotropy monotonicity when the center dominates total support

Let independent uniform angles define aligned ellipse variables

`X_j=A_j cos(theta_j)+i B_j sin(theta_j)`, `A_j>=B_j>=0`,

and put

`R=sum_j A_j`, `alpha_j=(A_j^2+B_j^2)/2`, `beta_j=(A_j^2-B_j^2)/2`.

**Theorem A.** If `c>=R`, the all-positive pattern dominates every quarter-turn sign pattern for every circle Green kernel, every continuous radial planar bisubharmonic test, and after arbitrary independent bounded radial noise.

### Proof

Initially take `c>R`. Fix all ellipses except `j`, allowing the others to have arbitrary mixed signs. Let the varying ellipse have squared semiaxes `alpha_j+t`, `alpha_j-t`, where `-beta_j<=t<=beta_j`. The exact elliptical-disk derivative is

`d/dt E k_rho(c+S_(not j)+X_(j,t))`

`=(1/4) E D k_rho(c+S_(not j)+D_(j,t))`,                         (5)

where `D_(j,t)` is uniform on the corresponding elliptical disk.

Every fixed ellipse is centrally symmetric. So is the independent disk. Their sum `W` is therefore centrally symmetric. Each fixed ellipse has modulus at most its `A_k`, and throughout this parameter interval the disk has modulus at most `A_j`. Hence `|W|<=R`. The paired lemma makes the derivative in (5) nonnegative on the entire signed interval, including its negative half.

Replace the flipped ellipses one at a time by increasing `t` from `-beta_j` to `beta_j`. This proves the Green inequality for `c>R`. Continuity of bounded Green expectations in `c` extends it to `c=R`.

The two compared second moments agree. The accepted local radial Green representation then gives the entire radial bisubharmonic cone. That cone is closed under convolution with bounded independent radial noise, proving the robustness assertion.

### Explicit zero-noise lower bounds away from the boundary

If `c>R`, (3)--(5) give the entropy bound

`E K(c+sum X_j)-E K(c+sum_(j not in T) X_j+i sum_(j in T) X_j)`

`>= (c^2-R^2)/(c^2+R^2) sum_(j in T) beta_j`.                    (6)

For every `p>2`, the same argument yields

`E |c+sum X_j|^p-E |c+sum_(j not in T) X_j+i sum_(j in T) X_j|^p`

`>= [p(p-2)/2] (c-R)^(p-2) (c^2-R^2)/(c^2+R^2)`

`      * sum_(j in T) beta_j`.                                   (7)

To verify (7) without differentiating a Green representation, use

`D |z|^p=p(p-2)|z|^(p-2) cos(2 arg z)`.

In the pairing above, the farther argument has the nonnegative angular factor and receives the larger radial weight. Both radii are at least `c-R`. Thus the paired expectation is bounded below by

`p(p-2)(c-R)^(p-2)(c^2-R^2)/(c^2+R^2)`.

Apply the disk derivative and integrate over a parameter interval of length `2beta_j`. This gives (7). No strict quantitative lower bound at `c=R` is claimed in (6)--(7).

## 3. A smaller center threshold for a specified mixed pattern

The nonnegative-anisotropy theorem in [Proof 28](28_anisotropic_hessian.md) can be used for the positive half of a simultaneous path, reducing the center bound further.

Let `T` be the flipped group and `U` its complement. Define

`R_T=max( sum_(j in U) A_j+sum_(j in T) sqrt(alpha_j),`

`         sum_(j in U) sqrt(alpha_j)+sum_(j in T) A_j )`.         (8)

**Theorem B.** The same full Green-cone and bounded-radial-noise comparison holds for this specified pattern whenever `c>=R_T`.

### Proof

For `-1<=s<=0`, keep the `U` ellipses aligned, and give every ellipse `j in T` squared semiaxes `alpha_j+s beta_j`, `alpha_j-s beta_j`. At `s=-1` this is the signed pattern; at `s=0` the flipped group consists of circles. First suppose `c>R_T`.

For a direction angle `theta`, write `q=cos(2theta)`. An ellipse or its filled disk with squared semiaxes `alpha+t`, `alpha-t` has support function `sqrt(alpha+t q)` in that direction. If `q>=0`, each `U` support is at most `A_j`, and each `T` support is at most `sqrt(alpha_j)` because `s<=0`. If `q<=0`, the respective upper bounds are `sqrt(alpha_j)` and `A_j`. Thus the support function of the sum, with any one differentiated ellipse replaced by its disk, is at most `R_T` in every direction. Equivalently its Euclidean support radius is at most `R_T`.

Differentiating in `s` gives a sum of terms of the form (5), with nonnegative coefficients `beta_j`. Every disk-background sum is centrally symmetric and has the stated support radius. The paired lemma makes each term nonnegative. Consequently the expectation cannot decrease between `s=-1` and `s=0`.

Between `s=0` and `s=1`, every ellipse is aligned with nonnegative anisotropy. The finite aligned-anisotropy theorem in [Proof 28](28_anisotropic_hessian.md) makes each increase nonnegative, for every radial bisubharmonic test including `k_rho`. Combining the two halves proves the Green comparison for `c>R_T`. Continuity in the center gives equality of the allowed threshold. The cone and noise extensions are the same as in Theorem A.

For a proper nonempty mixed pattern with at least one noncircular ellipse in each group, `R_T<R`. This genuinely enters part of the region where the center is smaller than the total major-axis support bound.

## 4. Full coefficient-box consequences and a two-pair example

For endpoint magnitudes `a_j,b_j>=0`, set

`A_j=a_j+b_j`, `B_j=|a_j-b_j|`, `alpha_j=a_j^2+b_j^2`.

Theorem A gives the full prescribed real coefficient-box majorant property for every `p>=2` under the simple condition

`c>=sum_j(a_j+b_j)`.                                            (9)

To use Theorem B for a full box, it suffices that its threshold hold for each relevant sign vertex. The all-flipped pattern is already covered for arbitrary `c` by the accepted common-rotation theorem; the all-positive vertex is equality. For exactly two noncircular ellipses, both proper mixed thresholds have the same convenient bound

`c>=max(A_1+sqrt(alpha_2), A_2+sqrt(alpha_1))`.                   (10)

Thus (10) gives a full prescribed coefficient box for all `p>=2`, with arbitrary bounded independent radial noise. As usual, real sign gauges reduce every sign vertex to a quarter-turn pattern, and convexity in the real coefficient vector fills in the box. No center inequality is imposed again at an interior point of that box.

For a concrete genuinely unequal two-pair example, take endpoint pairs

`(a_1,b_1)=(2,1)`, `(a_2,b_2)=(3/2,1/2)`, `c=23/5`.

Here `A_1=3`, `A_2=2`, `alpha_1=5`, `alpha_2=5/2`. The right side of (10) is

`max(3+sqrt(5/2), 2+sqrt(5))<23/5`,

because `5/2<(8/5)^2` and `5<(13/5)^2`. Yet `c=23/5<5=A_1+A_2`. This certifies the entire radial cone and the full prescribed power box in a genuinely mixed unequal example outside the simple center-dominant bound (9).

Circular pairs can be absorbed into the independent radial noise before applying these results. The bounds need only include the remaining noncircular ellipses. If at most one noncircular ellipse remains, the prior one-pair/common-rotation results already cover every center.

## 5. Regularity, endpoint cases, and comparison with previous results

Formula (5) is initially used only for nondegenerate disks, with the parameter in the open interval `(-alpha_j,alpha_j)`. For `rho=0`, `D K` is bounded by two and the disk has a planar density, so a translated disk argument equals zero with probability zero. Smooth positive mollification and dominated convergence justify the identity, or it may be integrated first before taking the smooth limit. For `rho>0`, (1) is already continuous and bounded. The inequality extends continuously to line-segment endpoints. Zero ellipses are omitted, and circular ones require no anisotropy change.

The simultaneous path in Theorem B is differentiated only in its open negative half; continuity handles `s=-1` when a line degeneracy occurs and `s=0` where the path is joined. All variables have a common compact support throughout every limit. If every ellipse vanishes, the assertions are equality. No assertion about an undefined pointwise Hessian at zero is needed.

The earlier accepted [A uniform center dominant coefficient region](13_dominant_center_boxes.md) assumed `c>=3 sum_j(a_j+b_j)`, proved an explicit bound only for `2<p<=3`, and did not establish arbitrary radial-noise robustness. Theorem A improves its coefficient threshold to a factor of one and supplies the full Green cone; Theorem B additionally supplies part of the region below that support threshold. These results do not replace the earlier certificate's particular numerical lower bound where one wants to use that bound verbatim.
