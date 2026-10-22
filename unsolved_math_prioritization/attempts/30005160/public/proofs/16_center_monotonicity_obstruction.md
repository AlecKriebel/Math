# Proof 16  A failure of monotonicity of the entropy gap

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Balanced and circular prescribed coefficient boxes](11_balanced_coefficient_boxes.md); [Exact one phase integration of the entropy kernel](14_one_phase_entropy.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

This result refutes an auxiliary proposed proof route. It is **not** a counterexample to the power-majorant or Green-kernel inequality. Its coefficient array lies in the already accepted all-balanced positive region.

Let theta and phi be independent uniform angles, put `K(z)=|z|^2 log|z|`, and define

`D(c)=E K(c+2cos(theta)+2cos(phi))`

`        -E K(c+2cos(theta)+2i sin(phi))`.

This is the all-positive minus one-pair-flipped entropy gap for the centered cross with all four endpoint magnitudes equal to one. Then `D` is twice continuously differentiable near zero, is even, and

`D''(0)=1-2L<0`,

where

`L=E asinh(|cos(theta)|)>=16/(9pi)>1/2`.                      (1)

Thus `D(c)<D(0)` for every sufficiently small positive `c`. The proposed statement that the mixed-sign entropy gap must be nondecreasing in the center is false even without additional radial noise.

## Calculation

For a nonzero real `x`,

`d^2/dc^2 K(c+x)|_(c=0)=2log|x|+3`.

Write `X=2cos(theta)+2cos(phi)`. The torus change of variables `theta=u+v`, `phi=u-v` pushes uniform Haar measure to uniform Haar measure, so

`X=4cos(u)cos(v)` in law.

Consequently

`E log|X|=log4+2 E log|cos(u)|=0`,

using the elementary circle logarithm integral `E log|cos(u)|=-log2`. Therefore

`d^2/dc^2 E K(c+X)|_(c=0)=3`.                               (2)

For nonzero `z=x+iy`,

`K_xx(z)=2log|z|+1+2x^2/|z|^2`.

Let `V=2cos(theta)+2i sin(phi)`. Its two real coordinates are independent and identically distributed. It has no atom at zero; therefore symmetry gives

`E (Re V)^2/|V|^2=1/2`.

Writing `L=E log|V|`, we obtain

`d^2/dc^2 E K(c+V)|_(c=0)=2L+2`.                            (3)

To evaluate `L`, condition on `x=2cos(theta)` and integrate the second phase. On the unit circle, multiplication by the phase does not change the modulus of

`x+Z-Z^(-1)`.

Its quadratic is `Z^2+xZ-1`. The two roots are real and have product minus one. Their moduli have product one, and the larger modulus is

`(|x|+sqrt(x^2+4))/2`.

Jensen's elementary root formula for the circle logarithmic mean therefore gives

`E_Z log|x+Z-Z^(-1)|=log[(|x|+sqrt(x^2+4))/2]=asinh(|x|/2)`.

This proves `L=E asinh(|cos(theta)|)`. For `0<=t<=1`,

`asinh(t)>=t-t^3/6`,

because its derivative satisfies `(1+t^2)^(-1/2)>=1-t^2/2`. The standard cosine integrals give

`E|cos(theta)|=2/pi`, `E|cos(theta)|^3=4/(3pi)`.

Hence `L>=16/(9pi)>1/2`; for example `pi<22/7<32/9` suffices for the strict final inequality. Equations (2) and (3) yield (1).

## Differentiation at the zeros

The preceding differentiation is not justified by pointwise smoothness at every sample, so we give a convolution argument.

The one-dimensional arcsine density of `2cos(theta)` belongs to `L^r(R)` for every `1<=r<2` and has compact support. Its self-convolution, the density of `X`, belongs to `L^2(R)` by Young's inequality applied with both factors in `L^(4/3)`. On every bounded interval, the distributional second derivative of the real function `x^2 log|x|` is `2log|x|+3`, which is in `L^2`; there is no delta term because its first derivative is continuous through zero. Convolution with the compactly supported `L^2` density has a continuous second derivative: Cauchy-Schwarz and continuity of translation in `L^2` prove continuity of the displayed second-derivative convolution. The values in (2) are therefore legitimate.

The two-dimensional density of `V` is the product of two arcsine densities, hence compactly supported and in `L^r(R^2)` for every `1<=r<2`. Choose any `r>1`. The distributional derivative `K_xx` has the stated locally integrable formula; its logarithmic singularity and bounded angular term lie in every finite local `L^s`. There is again no point mass, since `K` is continuously differentiable at zero and the boundary terms on a shrinking circle vanish. Holder's inequality with conjugate exponents and continuity of translation in local `L^s` show that convolution with this density has a continuous second derivative near zero. This justifies (3).

Both expectations are even in `c`, because both random vectors are centrally symmetric. Thus `D'(0)=0`; Taylor expansion at zero and `D''(0)<0` establish the claimed strict decrease.

## Scope

The all-balanced Green comparison remains nonnegative for every `c`, by the previously accepted balanced-pair theorem and the Green-cone extension. This result only rules out deriving that positivity by monotonic increase from the center-free value. It does not affect any accepted positive result and supplies no negative actual-majorant witness.
