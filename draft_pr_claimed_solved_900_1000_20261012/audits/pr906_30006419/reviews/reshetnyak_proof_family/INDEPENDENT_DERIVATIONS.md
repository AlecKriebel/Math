# Independent reconstruction before consulting old audits

Reconstructed from the immutable authored proof on 2026-10-13. No old audit
report or old audit code was read to produce this document. The reconstruction
is an analytic verification artifact, not a new proof-search route.

## Claim and exact success criterion

Let `X` be a compact oriented smooth Riemannian sphere with the metric written
below. On the round domain sphere let `u(t,theta)=(h(t),theta)` with `h'=a`,
`0<=a<=1`, `a=t^2` near zero, and `a=1` outside `[-1/2,1/2]`. The claim to
verify is that, for the Reshetnyak energy

\[
E_+(v)=\int \sigma_{\max}(dv)^2\,dA,
\]

every source point has one neighborhood `U` on which every Lipschitz
`Omega` with compact closure in `U` and every `W^{1,2}(Omega,X)` map of the
same trace satisfy `E_+(v)>=E_+(u|Omega)`. In particular no image, continuity,
homotopy, or energy-size constraint may be added to competitors. Simultaneously
`sigma_max/sigma_min` must exceed every fixed finite number on a set of positive
round area. This does not assert harmonicity for Dirichlet energy.

## 1. Scalar calibration reconstructed

Take a sufficiently small target ball `V` entirely inside a flat cylinder
coordinate patch. Choose it strongly geodesically convex in the ambient
Riemannian sphere. Its angular coordinate `y` has `|dy|=1`, and for points
`p,q` in `V`, a minimizing ambient geodesic lies in `V`. Therefore

\[
|y(p)-y(q)|\leq \operatorname{length}(\gamma)=d_X(p,q).
\]

This is the ambient distance assertion; a pointwise gradient bound on an
arbitrary patch alone would not prove it. On the compact target, the McShane
extension `F(q)=inf_{p in V}(y(p)+d_X(p,q))` is finite, 1-Lipschitz, and equals
`y` on `V`.

Shrink a source cylindrical chart `U` so that `u(U)` lies in `V`, and write
its angular coordinate as a real variable `x`. For an unrestricted same-trace
competitor `v`, Lipschitz composition gives `f=F(v)` in scalar `W^{1,2}` with
trace `x` and, almost everywhere,

\[
|\nabla f|\leq \|dv\|_{\mathrm{op}}.
\]

The formula is in the Euclidean chart. A conformal source metric
`lambda^2(dt^2+dx^2)` multiplies the squared norm by `lambda^{-2}` and the area
by `lambda^2`, so both sides of each integrated comparison are unchanged.
Put `w=f-x`. Matching trace implies `w in W^{1,2}_0(Omega)` for every bounded
Lipschitz `Omega`, including disconnected domains and domains with holes.
Approximation by compactly supported smooth functions proves
`int_Omega partial_x w=0`, hence

\[
\int_\Omega |\nabla f|^2
=|\Omega|+\int_\Omega |\nabla w|^2\geq |\Omega|.
\]

On the reference map `du=diag(a,1)`, so its operator norm is 1. This proves
the scalar comparison for every competitor, even a map visiting both poles.
No central comparison problem has been hidden in the extension: its existence
follows directly from the displayed ambient-distance inequality.

## 2. Critical W^{1,2} exact-form argument reconstructed

For a conformal orientation-preserving patch, choose a target cutoff `eta`
with `0<=eta<=1`, `eta=1` near the compact patch image, and
`m=int_X eta dA` satisfying `0<m<A/2`, where `A=Area(X)`. Such a cutoff is
available after shrinking the patch; points have area zero, and arbitrarily
small neighborhoods have arbitrarily small area. Define

\[
b=\frac{m}{A-m}<1,\qquad
\omega=((1+b)\eta-b)dA.
\]

Its scalar coefficient lies in `[-b,1]`, so its comass is at most 1; it equals
`dA` near the reference image; and its integral is
`(1+b)m-bA=0`. On an oriented smooth sphere the only obstruction to exactness
of a smooth two-form is its integral. Thus `omega=d alpha` for a global smooth
one-form. This ordinary de Rham statement neither asserts local energy
minimality nor assumes the desired conclusion.

Here is a scalar proof of the weak differential identity that is valid at
the critical exponent and does not approximate by sphere-valued smooth maps.
Write

\[
\alpha=\sum_{j=1}^N f_j\,dg_j,
\qquad f_j,g_j\in C^\infty(X).
\]

To justify the representation, take finitely many coordinate patches and a
partition `chi_i` with supports compactly contained in them. Write `alpha`
in local coordinates. Each coefficient `chi_i a_{ik}` extends by zero to a
global smooth `f_{ik}`. Extend the coordinate `x_{ik}` using a cutoff that
is 1 on a neighborhood of `supp chi_i`, obtaining global `g_{ik}`. Then
`f_{ik} dg_{ik}=chi_i a_{ik} dx_{ik}` everywhere. Compactness makes each
`f_j,g_j` bounded and Lipschitz.

For any target-valued `W^{1,2}` map `v`, write `F_j=f_j(v)` and `G_j=g_j(v)`.
They lie in scalar `W^{1,2}` and are bounded. On any smaller Euclidean source
chart, ordinary mollification yields smooth `F_{j,n},G_{j,n}` converging
strongly in `W^{1,2}`; convolution preserves uniform bounds on `F_{j,n}`.
After taking a subsequence the convergence is also almost everywhere. The
following estimates give exactly the needed limiting statements:

\[
\begin{aligned}
\|dF_n\wedge dG_n-dF\wedge dG\|_{L^1}
&\leq \|dF_n-dF\|_{L^2}\|dG_n\|_{L^2}
 +\|dF\|_{L^2}\|dG_n-dG\|_{L^2}\to0,\\
\|F_n dG_n-FdG\|_{L^2}
&\leq C\|dG_n-dG\|_{L^2}
 +\|(F_n-F)dG\|_{L^2}\to0.
\end{aligned}
\]

The final term tends to zero by dominated convergence with dominating
constant times `|dG|^2`. Passing to distributions in the smooth scalar
identity gives `d(F dG)=dF wedge dG`. Therefore `v^*alpha` lies in `L^2` and

\[
d(v^*\alpha)=\sum_j dF_j\wedge dG_j=v^*\omega
\quad\hbox{in distributions, with the right side in }L^1.
\]

The chain rule identifies this with intrinsic differential pullback almost
everywhere. One way to remove any concern about definitions is to embed the
compact smooth target in Euclidean space. Its embedding and inverse (for the
intrinsic metric versus chord distance) are globally Lipschitz. Scalar
composition gives an ordinary Euclidean `W^{1,2}` representative; smooth
defining functions show its weak derivative is tangent to the target almost
everywhere. Smooth extensions of the `f_j,g_j` then give the displayed chain
rule. First-order intrinsic distance expansion identifies its approximate
metric differential with `xi -> |dv(xi)|`. This also verifies that the
Reshetnyak density is the squared tangent operator norm for these competitors.

Now glue `v` on `Omega` to the smooth reference `u` on `U\Omega`. Equal
traces permit componentwise Euclidean Sobolev gluing; the values remain in
the embedded target almost everywhere, and the globally Lipschitz inverse
restores the intrinsic target-valued Sobolev map `vtilde`. The same embedding
argument or Lipschitz trace composition verifies all scalar trace claims.
The one-form

\[
\beta=\widetilde v^*\alpha-u^*\alpha
\]

is `L^2`, vanishes almost everywhere off `Omega`, and has compact support
inside `U`. Pair its distributional differential with a smooth cutoff equal
to 1 near `closure(Omega)`. Integration by parts is zero because the cutoff
derivative is supported where `beta=0`. The `L^1` differential then gives

\[
\int_\Omega v^*\omega=\int_\Omega u^*\omega.
\]

For arbitrary `v`, the signed pullback satisfies
`v^*omega <= |Jac(v)| dA <= sigma_max(dv)^2 dA`; a negative Jacobian causes
no difficulty. For the reference conformal patch the Jacobian is positive
and `omega=dA`, so equality holds throughout. Integrating proves local
minimality. Weak sphere bubbles contribute zero to the integral of an exact
form; using the full nonexact sphere area form instead would be invalid.

## 3. Target, map, seams, and positive-measure failure

The cutoff `chi` in the authored metric makes `rho=1` on `|s|<=2` and
`rho=e^s` for `s<=-3`, `rho=e^{-s}` for `s>=3`. The negative pole coordinate
`z=e^{s+i theta}` gives `rho^2(ds^2+dtheta^2)=|dz|^2`. The positive pole
coordinate `zeta=e^{-s-i theta}` gives `|dzeta|^2`. Both ends are genuine
positive smooth Euclidean metrics at their added origins. The apparent
absolute value at the equator occurs only where the exponent is identically
zero. Thus this is a smooth compact Riemannian sphere, rather than a singular
completion or a surface with boundary.

The authored smooth even cutoff gives `a` in `[0,1]`, positive except at 0,
equal to `t^2` on `|t|<=1/4`, and equal to 1 on `|t|>=1/2`. Every nonempty
interval has positive integral of `a`, so `h` is strictly increasing. It is
onto because `h=t-c` at the positive end and `h=t+c` at the negative end.
Both pole maps in the complex coordinates above are multiplication by
`e^c`. Hence `u` is a smooth homeomorphism and belongs to `W^{1,2}` on the
compact round sphere. Its rank defect at `t=0` is allowed for a smooth map
that is a homeomorphism; no smooth inverse is claimed.

For each point with `|t|<1`, continuity puts a small source neighborhood in
a convex ball in the flat belt, so the scalar calibration applies. For
`|t|>1/2` and the poles, `h'=1` and the source and target metrics are scalar
multiples of their cylindrical Euclidean metrics, so the exact-form
calibration applies. The open sets overlap. Points with `|t|=1/2` are in
the first set and points with `|t|=1` in the second. No seam is omitted.

Near zero the source conformal factor is `sech(t)^2`, the target is flat,
and the two singular values are `cosh(t)` and `t^2 cosh(t)`. Their ratio
is `t^{-2}` off the equator. For every finite `Q>=1`, any band
`0<|t|<min(1/4,1/(2 sqrt(Q)))` has positive area and ratio greater than `Q`.
Its exact round area is `4 pi tanh(delta)`, with `delta` the band width.
The equator itself has area zero and is not the reason for essential failure.

## 4. Remaining target and energy assumptions

A compact connected Riemannian manifold is complete and its length metric is
geodesic. Its positive uniform convexity radius puts any sufficiently small
diameter continuous sphere inside a contractible ball. For short Lipschitz
loops, finitely many uniformly biLipschitz charts give one uniform length
threshold. In a smaller convex coordinate ball cone the prescribed loop to
one point of its image. Its coordinate radius from that point is at most
half its coordinate length, so its Euclidean cone area is at most a quarter
of squared coordinate length. With both chart Lipschitz constants bounded
by `L`, the returned area is at most `L^4 ell^2/4`. The cone is Lipschitz,
retains the given parametrization, and is a `W^{1,2}` filling. This verifies
the required local quadratic isoperimetric inequality.

The energy function `I(s)=max_{|xi|=1}s(xi)^2` is continuous, monotone,
quadratically homogeneous, and rotation invariant. In its unit sublevel
each seminorm is bounded by 1 on the circle and is 1-Lipschitz there, since
`|s(xi)-s(zeta)|<=s(xi-zeta)<=|xi-zeta|`. Uniform limits preserve the
seminorm axioms after homogeneous extension. Arzela-Ascoli therefore proves
compactness of the sublevel. For a finite-dimensional normed target `Y`,
the function on matrices `A -> ||A||_{R^2 -> Y}^2` is convex. If a smooth
map agrees with a linear map `L` on the circle, componentwise integration
by parts gives `average_D Dv=L`; Jensen gives
`int_D ||Dv||^2 >= |D| ||L||^2`. This covers the source quasiconvexity test
even without its immersion restriction. No ellipticity, strict convexity,
or Dirichlet minimizer equivalence is used.

## 5. Two nearby assertions falsified by the construction

The global homotopy comparison has the exact difference

\[
E_+(u)-Area(X)=2\pi\int \rho(h(t))^2(1-a(t))dt=4\pi c>0.
\]

The first equality follows from the derivative formula and monotone change
of variables `s=h(t)`; the second uses that `1-a` is supported in the flat
belt. There is a conformal degree-one map `(t,theta)->(t,theta)` of energy
`Area(X)`. Thus the audited map is not a global homotopy minimizer.

In a rectangle with `0<t<1/4`, a nonnegative nonzero compactly supported
variation of the first target coordinate has Dirichlet first variation
`-4 int t psi<0`. This proves the map is not locally Dirichlet minimizing.
For Reshetnyak energy the scalar angular calibration prevents those
same-trace first-coordinate variations from lowering the energy. If a
variation depends on the angular coordinate, its off-diagonal derivative may
increase the largest stretch; the calibration still supplies the required
lower bound. These negative controls isolate the exact energy and locality
of the result.

## Reconstruction verdict

Every analytic step required by the explicit theorem has been reconstructed.
No equivalent unsupported claim, circularity, excluded competitor class,
critical Sobolev defect, metric seam, pole singularity, or null-set-only
distortion argument was found. Source interpretation and historical priority
remain separate questions; this artifact establishes neither first priority
nor the exact wording of an uninspected final publisher version.
