# Proof 28  Elliptical disk differentiation and anisotropic Hessians

Included dependencies: [Balanced flips against an arbitrary aligned ellipse group](24_balanced_flip_alignment.md); [Angular order under a common rotation](15_common_rotation.md); [Radial Green kernels and the bisubharmonic comparison cone](10_radial_green_reduction.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## 1. On-axis anisotropic Hessian

Let `S` be a sum of independent aligned ellipse variables, with all major axes horizontal. Let `Phi` be smooth, radial, and distributionally bisubharmonic. Independent bounded radial noise may be absorbed into `Phi`. Put

`F(w)=E Phi(w+S)`.

Then, for every real `c`,

`F_xx(c,0)-F_yy(c,0)>=0`.                                         (1)

For `c>0`, write `F(r,theta)` in polar coordinates. Center-square convexity says that `s -> F(sqrt(s),0)` is convex, so

`F_rr(c,0)-F_r(c,0)/c>=0`.

The common-rotation theorem says that `theta=0` is a global angular maximum at each fixed radius, so

`F_(theta theta)(c,0)<=0`.

The polar Hessian identity on the positive real axis is

`F_xx-F_yy=F_rr-F_r/r-F_(theta theta)/r^2`.

Both terms on its right side are nonnegative. This proves (1) for `c>0`; smoothness gives the result at zero, and central symmetry gives it for negative `c`.

The same assertion holds if one independently adds any positive mixture of scaled aligned ellipses, by conditioning on the mixing parameter. In particular, it holds after adding a uniform aligned elliptical-disk variable, whose representation is `R(A cos(theta)+iB sin(theta))`, with independent uniform `theta` and `R` having density `2r` on `[0,1]`.

For continuous nonsmooth tests, smooth radial positive mollification preserves the hypotheses. The pointwise Hessian assertion is made for the mollified functions; no unsupported pointwise Hessian at a singularity is asserted. Integrated inequalities below pass to the locally uniform limit.

## 2. Exact elliptical-disk differentiation

Fix `alpha>0` and `-alpha<beta<alpha`. Let

`M(beta)=E Phi(c+S+sqrt(alpha+beta)cos(theta)+i sqrt(alpha-beta)sin(theta))`.

Let `D_beta` be an independent variable uniform in the elliptical disk with semiaxes `sqrt(alpha+beta)` and `sqrt(alpha-beta)`. For smooth `Phi`,

`M'(beta)=(1/4) E [(partial_x^2-partial_y^2)Phi(c+S+D_beta)]`.       (2)

To verify the constants, if `A,B>0`, differentiation of the circle average with respect to `A^2` gives

`(1/(2A)) E_theta [cos(theta) Phi_x(c+S+Acos(theta)+iBsin(theta))]`.

The divergence theorem on the unit disk, followed by the linear map `(u,v)->(Au,Bv)`, identifies this with one quarter of the uniform elliptical-disk average of `Phi_xx`. The same argument gives the `B^2` derivative as one quarter of the average of `Phi_yy`. Along `A^2=alpha+beta`, `B^2=alpha-beta`, subtraction gives (2).

For `beta>=0`, `D_beta` is an aligned elliptical disk. Its mixture representation and (1) therefore give

`M'(beta)>=0` for `0<=beta<alpha`.                                (3)

Hence **increasing the nonnegative anisotropy of one aligned ellipse at fixed squared-semiaxis sum cannot decrease the expectation of a radial bisubharmonic test against any independent aligned ellipse background and real center**. Continuity includes the endpoint `beta=alpha`. For continuous tests, integrate (3) between two parameters before passing to radial mollifier limits. This proves the finite monotonicity statement without requiring unregularized pointwise derivatives.

The proof supplies no sign for the integrand in (2) when `beta<0`: that disk is vertically elongated and the aggregate background is genuinely mixed. Consequently (3) does not prove `M(beta)>=M(-beta)`.

## 3. Exact infinitesimal consequence for the Green kernel

Take `Phi(w)=E K(w+rho Z)` for any fixed `rho>=0`. For `K`, the distributional anisotropic Hessian is represented by the bounded function

`(partial_x^2-partial_y^2)K(z)=2 Re(z^2/|z|^2)` for `z!=0`.          (4)

Its value at zero is immaterial to planar integration. There is no point-mass contribution: the weak second derivatives of `K` are locally integrable (its first derivatives vanish at zero), and the logarithmic radial terms cancel in this difference.

For a nondegenerate elliptical disk, convolution against (4) is continuous and bounded. One may justify (2) for this `Phi` by mollifying `K`: the mollified anisotropic Hessians are uniformly bounded by `2`, and converge away from zero. Conditional on `S` and the radial noise, an independent nondegenerate elliptical-disk variable has a planar density, so the translated argument equals zero with probability zero. Dominated convergence passes the derivative formula to the limit. Equivalently, first integrate (2) on compact beta intervals within `(-alpha,alpha)` and use continuity of the resulting disk convolutions.

In particular, at `beta=0`,

`M'(0)=(1/4) E [(partial_x^2-partial_y^2)K(c+S+D_0+rho Z)]>=0`,       (5)

where `D_0` is uniform on the disk of radius `sqrt(alpha)`. Therefore the sign gap

`G(beta)=M(beta)-M(-beta)`

satisfies `G(0)=0` and `G'(0)=2M'(0)>=0`. This is an exact favorable first derivative at a circular pair. A zero first derivative gives no local sign conclusion; a positive one gives local positivity by differentiability. Neither case establishes finite-eccentricity comparison throughout the interval.

## 4. Exact obstruction to using only angular order and ray-square convexity

The preceding arguments crucially retain bisubharmonicity and the special ellipse-sum structure. Angular maximality and convexity in squared radius alone do not imply general finite ellipse replacement.

For an explicit auxiliary example, set

`Phi(z)=(|z|^2-t)_+`, `0<t<2/3`.

This test is radial, and it is convex as a function of squared radius. It therefore has trivial common-rotation angular order. Take center `c=1` and one ellipse with semiaxes `A=2`, `B=1`. With `u=cos(theta)`, the aligned squared modulus is

`S_+=(1+2u)^2+(1-u^2)=2+4u+3u^2>=2/3`.

After a quarter-turn and a harmless phase reparametrization, the squared modulus is

`S_-=(1+u)^2+4(1-u^2)=5+2u-3u^2`.

It reaches zero at `u=-1`, and `P(S_-<t)>0` by continuity and the arcsine law. The two second moments agree. Therefore

`E(S_+-t)_+-E(S_--t)_+ = -E(t-S_-)_+<0`.

This is an exact failure in the larger auxiliary convex-stop-loss class. The test is not radial bisubharmonic, so it is not a Green-kernel or power-majorant counterexample. It explains why the Jensen/common-rotation proof for balanced flips must not simply be asserted for arbitrary ellipse flips.

The comparison proved here concerns increasing nonnegative aligned anisotropy. The full signed path under strong-center conditions is treated in [Proof 40](40_strong_center_green_cone.md).
