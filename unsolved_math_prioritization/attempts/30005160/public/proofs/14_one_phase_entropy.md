# Proof 14  Exact one phase integration of the entropy kernel

This is a reading edition of an accepted authored proof. Its mathematical scope is unchanged. Source and reading-edition hashes are recorded in the [inventory](../CONTENT_AND_DEPENDENCIES.md). No novelty claim is made.

Public analytic inputs and exact attribution are listed in [References](../REFERENCES.md).

This is a reduction formula, not a positivity theorem. In particular, it does not close the mixed-sign centered-cross gap at `2<p<3`.

Let `a>0`, `b` be real, `w` be complex, and let `Z` be uniform on the unit circle. Set

`P(Z)=a Z+b/Z+w`,

`Q(z)=a z^2+w z+b=a(z-r1)(z-r2)`.

Define

`tau(r)=r` if `|r|<=1`, and `tau(r)=1/conjugate(r)` if `|r|>1`,

`L0=log(a)+sum_(j=1,2) log max(1,|rj|)`,

`T1=tau(r1)+tau(r2)`, `T2=tau(r1)^2+tau(r2)^2`.

Then, with the convention `0 log 0=0`,

`E |P(Z)|^2 log|P(Z)|`

`= (a^2+b^2+|w|^2)L0 - Re[(a conjugate(w)+b w) T1] - (ab/2) Re(T2)`.       (1)

The right side is independent of the ordering of the quadratic roots. The formula applies when roots lie on the unit circle by continuity and remains valid for repeated or zero roots.

## Proof

On the unit circle, `|P(z)|=|Q(z)|`. For a root `r`, the constant Fourier coefficient of `log|z-r|` is `log max(1,|r|)`. Its coefficient of `z^(-k)`, for `k>=1`, is

`-tau(r)^k/(2k)`.

For `|r|<1`, this follows from the convergent logarithmic expansion of `log|1-r/z|`; for `|r|>1`, factor out `r` and expand `log|1-z/r|`. At `|r|=1`, the same coefficients follow by the integrability of the logarithmic singularity and radial limits; alternatively, approximate the root from off the circle. Only coefficients through degree two are needed.

Direct multiplication gives

`|P(z)|^2 = a^2+b^2+|w|^2 + (a conjugate(w)+b w) z`

`+ (a w+b conjugate(w)) z^(-1) + ab(z^2+z^(-2))`.

Pair each coefficient of this finite Laurent polynomial with the opposite Fourier coefficient of `log|Q(z)|`. The constant term is exactly (1).

For completeness, continuity at root boundary cases does not require a uniform pointwise bound on `log|Q|`. The original integrand is `|Q|^2 log|Q|`, which is continuous as a function of `Q`, including at zero, and uniformly bounded on compact coefficient sets. Thus its circle integral is continuous. The right side of (1) is also continuous because `tau` and `log max(1,|r|)` are continuous across the unit circle, and symmetric root expressions are continuous under perturbation of polynomial coefficients.

## A particularly simple root regime

If both roots lie in the closed unit disk, their sums are

`T1=-w/a`, `T2=w^2/a^2-2b/a`, `L0=log a`.

Hence (1) simplifies to

`(a^2+b^2+|w|^2) log a + |w|^2+b^2+(b/(2a)) Re(w^2)`.            (2)

For `|b|<a`, the boundary of this root regime is the ellipse traced by `w=-a z-b/z`, `|z|=1`; its semiaxes are `a+|b|` and `a-|b|`, with the long-axis direction determined by the sign of `b`. The formula itself needs no geometric classification of the root regime.

## Centered-cross application

For two endpoint pairs, take

`w(theta)=c+d exp(i theta)+e exp(-i theta)`.

The entropy/Green moment of the full centered-cross polynomial is the remaining one-dimensional angular average of (1). A sign flip in either pair is implemented by changing the corresponding real endpoint coefficient. This gives an exact reduction to logarithms, quadratic roots, and one angular integral. Root-regime transitions must be handled in any later certified quadrature; ordinary floating-point sampling alone is not a certificate.

More generally, the same formula integrates out one phase in any centered-cross dimension. Additional independent circular noise introduces additional remaining phases. No argument here establishes the sign of the remaining integral.
