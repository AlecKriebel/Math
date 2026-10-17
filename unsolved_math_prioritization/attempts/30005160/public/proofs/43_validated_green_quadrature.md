# Proof 43  Validated circular Green quadrature

Included dependencies: [Radial Green kernels and the bisubharmonic comparison cone](10_radial_green_reduction.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## 1. The exact cutoff and its regularity

Normalize the unperturbed centered-cross polynomials by the common coefficient-sum bound `R`, so `|P|<=1`. Let `0<rho<1` be the circle-noise radius after this normalization. The accepted radial Green formula permits subtracting a common affine function of `s=|P|^2`, leaving

`g_rho(s)=0` for `s<=rho^2`,

`g_rho(s)=(1/2)(s+rho^2)log(s/rho^2)+rho^2-s` for `s>rho^2`. (1)

Thus the Green gap with added independent noise `rho Z` equals the gap in expectations of `g_rho(|P|^2)`. Constants and quadratics cancel because the compared sign polynomials have equal second moments. The input is [Radial Green kernels and the bisubharmonic comparison cone](10_radial_green_reduction.md), SHA-256 `b7f61e95c8244cc2c67142f82b0c6af2d25fba2349cd926c5b73fa27360b5eb8`.

Write `g=g_rho`. On the exterior branch,

`g'=(1/2)[log(s/rho^2)+rho^2/s-1]`,

`g''=(s-rho^2)/(2s^2)`,

`g'''=(2rho^2-s)/(2s^3)`,

`g''''=(s-3rho^2)/s^4`.

On `rho^2<=s<=1` the following safe bounds hold:

`|g'|<=G1=(1/2)[log(1/rho^2)+rho^2-1]`,

`|g''|<=G2=1/(8rho^2)`,

`|g'''|<=G3=1/(2rho^4)`,

`|g''''|<=G4=2/rho^6`. (2)

The first bound uses monotonicity. For the others set `t=s/rho^2>=1` and maximize or bound the resulting rational functions. At `s=rho^2`, `g=g'=g''=0`; the third derivative has a finite jump from zero to `1/(2rho^4)`. Therefore `g` is `C^2` and piecewise smooth.

## 2. A uniform fourth-derivative-measure bound for each angle

Fix all but one of the independent angles and write

`P(theta)=w+a exp(i theta)+b exp(-i theta)`, with `L=|a|+|b|`.

Assume the uniform support bound `|P|<=1`. Since `|P^(k)|<=L` for every integer `k>=1`, the real trigonometric polynomial `s(theta)=|P(theta)|^2` satisfies

`|s'|<=S1=2L`,

`|s''|<=S2=2L^2+2L`,

`|s'''|<=S3=6L^2+2L`,

`|s''''|<=S4=14L^2+2L`. (3)

The fourth derivative identity uses `s''''=2 Re(P'''' conjugate(P))+8 Re(P''' conjugate(P'))+6|P''|^2`.

Let `F(theta)=g(s(theta))`. Away from the threshold, the chain rule gives

`F''''=g''''(s)(s')^4+6g'''(s)(s')^2s''`

`+3g''(s)(s'')^2+4g''(s)s's'''+g'(s)s''''`.

Its absolute value is at most

`M4=G4 S1^4+6G3 S1^2 S2+3G2 S2^2+4G2 S1 S3+G1 S4`. (4)

At a threshold crossing the jump of `F'''` has absolute value at most

`J=G3 S1^3`. (5)

Indeed the terms involving `g'` and `g''` vanish at the threshold. A tangency with `s'=0` has zero third-derivative jump.

The function `s(theta)-rho^2` is a real trigonometric polynomial of degree at most two. Unless it vanishes identically, it has at most four distinct zeros on the circle, by multiplying its Laurent form by `exp(2i theta)` and using the resulting polynomial of degree at most four. If it vanishes identically, `F` is identically zero and the bounds hold trivially. Hence the distributional fourth derivative of the periodic function `F` is a finite signed measure whose total variation is at most

`T=2pi M4+4J`. (6)

There are no derivatives of point masses: `F,F',F''` are continuous at every transition. The bound is uniform in every other angle and in the pair signs.

## 3. Periodic midpoint error, with its constant

For a continuous `2pi`-periodic function with fourth distributional derivative a finite signed measure of total variation at most `T`, integration by parts in distributions gives

`|F_hat(k)|<=T/(2pi |k|^4)` for `k!=0`.

The Fourier series is absolutely summable. The `N`-point midpoint average differs from its integral average only in aliased frequencies `k=mN`, with phases `(-1)^m`. Therefore its absolute error is at most

`sum_(m!=0) T/(2pi |mN|^4)`

`=pi^3 T/(90N^4)`, (7)

using `sum_(m>=1) m^(-4)=pi^4/90`. A weaker elementary bound for this convergent series could also be substituted.

For a two-angle tensor midpoint rule, the error is at most the sum of (7) for the two coordinates, by telescoping the expectation and quadrature operators. Both are norm-one averaging operators. For a sign gap, double that sum. This yields a global explicit error of order `N^-4`, even when the threshold curves cross the quadrature cells.

## 4. Interval code and exact rational example

[certify_green_quadrature.py](../certificates/certify_green_quadrature.py) implements (1)-(7) using the real interval primitives and exact-rational outward reporting helpers from the included entropy quadrature code. All sampled trigonometric values, cutoff evaluations, and error constants are enclosed at 45 decimal digits. It uses simultaneous complex conjugation of both angles to evaluate only half the tensor grid; this preserves squared modulus for all real coefficients and maps midpoint nodes to midpoint nodes.

For the exact rational coefficients

`c=39/200`, `(a_0,b_0)=(1,197/200)`,

`(a_1,b_1)=(99/100,19503/20000)`,

flip only pair 0, and choose the noise radius to be `17/20` times the unperturbed coefficient-sum support bound `R=82903/20000`. With `N=128` per angle, the normalized Green gap is certified inside

`(0.00003169,0.00003266)`.

The unnormalized gap is certified inside `(0.00054452,0.00056104)`. Exact interval endpoints and each bound are in [green_rational_certificate.json](../certificates/green_rational_certificate.json). This certifies the individual displayed positive-radius comparison; it is not a negative witness or an all-radii certificate.

Run `python certificates/certify_green_quadrature.py --N 128` to reproduce. As for the earlier validated calculation, the trusted numerical dependency is mpmath's real interval arithmetic, not a formal verification of that library.
