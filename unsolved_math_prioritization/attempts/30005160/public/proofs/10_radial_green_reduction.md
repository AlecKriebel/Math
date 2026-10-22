# Proof 10  Radial Green kernels and the bisubharmonic comparison cone

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Proof dependencies included in this package: [Circuit obstructions and positive uncentered blocks](01_circuit_obstructions.md); [Arithmetic progressions with radial noise and joins](09_robust_ap_and_joins.md).

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

## 1. Precise local representation, with all boundary terms accounted for

Set

`K(z)=|z|^2 log|z|`, with `K(0)=0`.

In the plane,

`Delta K=4 log|z|+4`, and `Delta^2 K=8pi delta_0`.                  (1.1)

The first equality is distributional with no point mass: the radial flux `2pi r K'(r)` tends to zero at the origin. The second uses the distributional identity `Delta log|z|=2pi delta_0`. This latter identity follows directly by integration by parts outside a disk of radius epsilon and passage to the limit; its limiting normal-flux contribution is `2pi` times the test function's value at zero.

**Local Green representation.** Let `Phi` be a real continuous radial function on an open disk of radius `R_0`, and suppose `Delta^2 Phi` is a nonnegative distribution there. Fix `0<R<R_0`. Then there are real constants `a,b` and a finite positive rotationally invariant Borel measure `mu_R` supported in the closed disk of radius `R` such that

`Phi(z)=a+b|z|^2 + (1/(8pi)) integral K(z-w) dmu_R(w)`             (1.2)

for every `|z|<R`.

### Proof

A positive distribution is a locally finite positive Radon measure. Write `mu=Delta^2 Phi`, and let `mu_R` be its restriction to the closed disk of radius `R`. It is finite because that disk is compactly contained in the domain, and it is rotationally invariant because `Phi` is radial.

The potential

`P_R(z)=(1/(8pi)) integral K(z-w) dmu_R(w)`

is continuous: `K` is continuous and uniformly continuous on every compact set, while `mu_R` has finite mass and compact support. Its bi-Laplacian is `mu_R` in distributions by (1.1). Thus `u=Phi-P_R` is continuous, radial, and satisfies `Delta^2 u=0` on the open disk of radius `R`.

To identify the remainder without assuming boundary data, set `v=Delta u`. It is a harmonic distribution, so the distributional Weyl lemma makes it a smooth harmonic function. It is radial and smooth across zero, hence constant. Subtracting the corresponding multiple of `|z|^2` from `u` leaves a harmonic distribution; Weyl's lemma again makes it a smooth radial harmonic function, hence constant. Therefore `u=a+b|z|^2`.

For the elementary final assertion, a radial smooth harmonic function `v(r)` solves `(r v'(r))'=0` for `r>0`; smoothness at zero rules out the logarithmic term. There are no uncontrolled logarithmic, singular, or boundary terms. All contributions from the discarded part of `mu`, as seen inside the disk, are absorbed into the two stated constants. We do not assert a globally convergent potential representation when the original measure has infinite mass or growth at infinity.

## 2. The exact circular Green kernels

Let `Z` be a uniform unit complex number, and define

`k_rho(r)=E K(r+rho Z)`, for `r,rho>=0`.

For positive `r,rho`,

`k_rho(r)=(r^2+rho^2) log max(r,rho) + min(r^2,rho^2)`.           (2.1)

At a zero radius this is interpreted continuously, so `k_0(r)=r^2 log r` and `k_rho(0)=rho^2 log rho`.

### Derivation

When `0<=r<rho`, use the uniformly convergent Fourier expansion on every strict subrange `r/rho<1`:

`log|rho+r exp(it)|=log rho + Re sum_(n>=1) (-1)^(n+1) (r/rho)^n exp(int)/n`.

The squared modulus is `rho^2+r^2+2rho r cos(t)`. On multiplying and averaging, the constant term gives `(rho^2+r^2)log rho`; only the `n=1` Fourier term contributes in the cross product, giving `r^2`. Symmetry between `r` and `rho` yields the other case, and continuity of `K` gives the formula when `r=rho`.

For `rho>0`, subtract the harmless affine function of `r^2`:

`k_rho(r) - [(r^2+rho^2)log rho + r^2] = rho^2 f(r^2/rho^2)`,    (2.2)

where

`f(u)=0` for `0<=u<=1`,

`f(u)=(1/2)(u+1)log u + 1-u` for `u>1`.

This normalized kernel is nonnegative, increasing, and convex. For `u>1`,

`f'(u)=(1/2)(log u+1/u-1)`,

`f''(u)=(u-1)/(2u^2)>=0`.

Both derivatives join continuously to zero at `u=1`. Thus it is a `C^2` convex cutoff kernel. Near `u=1`, `f(u)=(u-1)^3/12+O((u-1)^4)`. This exact formula can be useful in analysis or certification, but convexity alone does not settle arbitrary centered-cross sign comparison.

The normalization in (2.2) is used one radius at a time. Its subtracted quadratic contains `log rho`; integrating its separate terms over a measure accumulating at zero may diverge, even though the original unnormalized Green potential is finite and continuous. Accordingly (1.2) and the positive-mixture proof below always use the unnormalized kernels. A normalized-tail mixture requires either an integrability condition on the logarithmic quadratic terms or truncation away from zero with cancellation performed before taking the limit. The atom at zero is retained as `K` itself. For equal-second-moment comparison, the difference of the two unnormalized expectations equals the difference of the normalized expectations for each positive radius; the former difference stays bounded as the radius tends to zero and is the safe object to integrate.

## 3. A one-parameter characterization of radial bisubharmonic comparison

Let `U,V` be bounded complex random variables satisfying

`E|U|^2=E|V|^2`.

They need not have radial laws. All the tests in this section are radial.

The following conditions are equivalent:

1. `E Phi(U)>=E Phi(V)` for every continuous radial function `Phi` on the plane with `Delta^2 Phi>=0` distributionally.
2. For every `rho>=0`, with `Z` an independent uniform unit complex number,

   `E K(U+rho Z)>=E K(V+rho Z)`.                            (3.1)

For condition 2 it is enough to test `rho` up to any radius larger than the supports of `U,V`, because condition 1 on those supports follows from the local representation. Conversely, condition 1 gives every radius in condition 2.

### Proof that 2 implies 1

Choose `R` larger than both supports and apply (1.2). Write the finite radial measure `mu_R` as a mixture of uniform measures on the circles of radii `rho`, with a possible atom at zero. This is the polar decomposition of a rotationally invariant finite measure; equivalently, average an independent uniform rotation of a random point with the normalized measure.

The constant in (1.2) cancels because both expectations have total probability one, and the quadratic term cancels by equality of the second moments. Every circular potential contributes a nonnegative difference by (3.1). Fubini is valid because all arguments lie in a fixed compact disk, `K` is bounded there, and `mu_R` is finite. Positive integration proves the claim. The same argument applies to tests defined only on a sufficiently large neighborhood of the two supports.

### Proof that 1 implies 2

For fixed `rho`, the function `z -> E K(z+rho Z)` is continuous and radial. Its bi-Laplacian is `8pi` times the uniform probability measure on the circle of radius `rho`, with the zero-radius case interpreted as a point mass. It is therefore an allowed test in condition 1.

### Robustness follows automatically for this entire cone

If condition 1 holds and `Y` is arbitrary independent bounded rotationally invariant noise, then `Psi(z)=E_Y Phi(z+Y)` is again continuous, radial, and distributionally bisubharmonic for every global test `Phi` in condition 1. Indeed its bi-Laplacian is the convolution of the nonnegative measure `Delta^2 Phi` with the reflected probability law of `Y`. Applying condition 1 to `Psi` proves

`E Phi(U+Y)>=E Phi(V+Y)`.

Thus the one-circle Green-kernel condition is equivalent to the whole-cone comparison, and it also supplies arbitrary radial-noise robustness. The equality of second moments persists after adding such noise, since its mean is zero.

## 4. AP triples satisfy the entire radial bisubharmonic comparison

Let `U,V` be the positive and arbitrary-sign AP polynomials at the same nonnegative coefficient magnitudes, reduced to the major-axis and minor-axis ellipse laws as in the robust AP theorem. The robust power theorem gives, for every bounded independent radial `Y`,

`D(p)=E|U+Y|^p - E|V+Y|^p >=0` for every `p>2`.

At `p=2`, the two moments are equal. This follows from Fourier orthogonality for the AP polynomials, independence of `Y`, and `E Y=0`. The variables are bounded, and on every bounded interval of nonnegative arguments the map

`t -> t^p log t`, with value zero at `t=0`,

is uniformly bounded for `p` in a fixed compact interval containing `2`. Differentiating the moments at `p=2` is therefore justified by dominated convergence. Taking the right derivative of the nonnegative function `D`, with `D(2)=0`, gives

`E K(U+Y) >= E K(V+Y)`.                                     (4.1)

In particular this holds for `Y=rho Z` for every `rho>=0`. Section 3 proves:

**AP cone theorem.** At any fixed nonnegative AP coefficient magnitudes, the all-positive real sign pattern dominates every real sign pattern for every continuous radial planar bisubharmonic test. This comparison remains valid after adding arbitrary independent bounded radial noise.

The stronger cone theorem concerns sign comparison; it does not assert arbitrary coefficient-box monotonicity for an arbitrary bisubharmonic test, because that test need not be convex. For the power tests `p>=2`, the usual coefficient-box convexity supplies full real majorants, as already proved in the robust AP theorem.

The two-layer simplex and center-free cross blocks already satisfy precisely this cone theorem by the circle/disk arguments in [Proof 01](01_circuit_obstructions.md). Thus singletons, AP triples, and those AP-free blocks share the full convolution-stable radial bisubharmonic cone. Their affine joins can be proved positive using this common cone, giving an alternative stronger explanation of the already accepted all-`p>=2` join result.

## 5. Exact remaining centered-cross reduction

Fix the coefficient magnitudes and compare the all-positive centered-cross polynomial with an arbitrary real sign pattern. Fourier orthogonality gives equality of their second moments. Section 3 therefore applies with no missing moment hypothesis.

To establish the centered-cross sign comparison for every radial bisubharmonic test, it is necessary and sufficient to establish the one-parameter family

`E K(U+rho Z) >= E K(V+rho Z)` for every `rho>=0`,              (5.1)

or equivalently the explicit tests `k_rho` in (2.1). Since the quadratic and constant terms cancel, for `rho>0` one may instead use the nonnegative convex cutoff tests `rho^2 f(|z|^2/rho^2)` of (2.2); the zero-radius logarithmic kernel must also be included, or obtained by continuity as `rho` tends to zero.

If proved for all centered-cross coefficient choices and all real sign patterns, this would yield arbitrary radial-noise robustness and every power exponent `p>=2`, because `|z|^p` is distributionally bisubharmonic for `p>2` and quadratic for `p=2`. The same blockwise independent-Haar replacement would then establish affine-join sufficiency for every mass-two-circuit configuration throughout `2<p<4`.

No proof of (5.1) for the general centered cross is supplied here. In particular, neither positivity for a single radius, ordinary isolated `L^p` comparison, nor convexity of the cutoff function is substituted for this missing family of inequalities.
