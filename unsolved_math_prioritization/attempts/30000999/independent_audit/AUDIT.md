# Independent audit: inverse Wasserstein stability of equator averaging

Problem **30000999 / OWR-2042-008**. Reviewed 3 October 2026.

## Disposition

**PASS. No mathematical correction is required in the frozen author package.**

The package gives a complete negative answer to the literal, unrestricted
probability-measure question. Its stronger theorem is also correct: for each
fixed ambient dimension `n >= 3`, each fixed real `1 <= p < infinity`, and each
fixed `0 < a < 1`, the specified smooth, strictly positive, even densities have
an unbounded input/output Wasserstein-distance ratio. The exceptional even
circle case is correctly identified as an isometry.

This is an independent adversarial **AI review**, not human verification,
formal proof-assistant certification, or journal peer review. It certifies the
scope and reasoning described here for the exact bytes below. It does not
certify originality or historical priority, authorize publication, or change
repository or queue state.

## 1. Frozen object and replay

Reviewed author manifest:

`9aad6a1d1eca15937701fcce5969be07ad5a1b901fe3b75bdfb7c1f13744006e`

All six file sizes and SHA-256 digests in that manifest were checked against
the actual files. The proof digest is:

`f9dcfdcf391b9e6e64cd3dabd6604fbd7ced18c66078279a7e86a3cb2b5d899c`

The unchanged author script was run directly with Python 3.12.14. Its standard
output is stored as `author_replay.json`; `cmp` confirmed byte-for-byte equality
with the frozen `exact_results.json`, including formatting and final newline.
The replay digest is:

`0a8f8bbcd8ecb1af717fca4134a3a94a532a81b83faa0ce135cd31757b0b7a95`

All **591 author assertions** passed. I read the script as well as running it:
it uses exact rational polynomial and spherical-moment arithmetic, not a
numerical optimal-transport solver. The author correctly labels these as
finite algebra/transcription controls. They do not prove smooth-flow
existence, all-degree identities, or limits. All author files were left
unchanged, and their hashes were rechecked after the audit.

The complete hash binding and machine-readable result are in
`disposition.json`; the audit's own file manifest is `AUDIT_MANIFEST.json`.

## 2. Source and literature gate

I independently opened the [official Oberwolfach report](https://ems.press/content/serial-article-files/46174),
read Stephens's contribution on printed pp. 1762–1764, and visually checked
p. 1763. It defines the dual of normalized equator averaging, intrinsic
spherical transport cost, and finite orders `p >= 1`, then asks for a uniform
reverse contraction bound. The passage imposes neither evenness nor a support
restriction. The author's operator and literal quantifiers agree. The forward
formula is naturally meaningful for `n >= 3`; the author's `n = 2` treatment
is a separately justified two-point-equator extension. The report is numbered
31/2008, with the July 2008 workshop date. The inspected local PDF has SHA-256
`15854a33755fcaae9620944f730823932f48c32f6a56b9ce057c0b1b5862e54f`.

The [Quellmalz article](https://link.springer.com/article/10.1007/s13324-020-00383-2)
supports the classical attribution: equation (2.5) is the same normalized
transform; Section 4 identifies the odd nullspace; Proposition 6.1 records
the even Sobolev smoothing degree `(d-2)/2` and credits Strichartz. No result
in the frozen proof depends on importing an unproved Wasserstein theorem
from that article.

An independent bounded duplicate screen found no same-problem repository PR
or indexed code hit. This is not evidence of historical novelty. Exact query
scope, adjacent work, and limitations are recorded in `SOURCE_REVIEW.md` and
`source_checks.json`. The package's repeated disclaimers about classical
parity and unverified priority are appropriate. A solved literal question
must not be described as a newly discovered injectivity failure.

## 3. Operator, probability measures, and unrestricted obstruction

### 3.1 Normalization and duality

For every `u`, normalized equator measure is a probability. Thus `F1 = 1`,
`F` preserves nonnegative functions, and its dual sends probability measures
to probability measures. The kernel is weakly continuous; this follows, for
example, by rotating nearby normal vectors using local continuous rotations.
There is no hidden mass-renormalization factor.

The joint law of an orthonormal pair obtained from the first two columns of
a Haar-distributed orthogonal matrix is exactly
`sigma(du) sigma_u(dx)`. Swapping columns preserves its law. This explicitly
verifies the symmetry argument in Section 3.1 and gives

`integral f Fg d sigma = integral g Ff d sigma`.

Consequently `R(rho sigma) = (F rho) sigma` and `R sigma = sigma`.
The reasoning is valid with normalized measures, and is also valid in
dimension two with the equal-weight, two-point equator.

### 3.2 Antipodal measures

`E(u) = E(-u)` as measured sets, hence `R delta_u = R delta_-u`.
The only input coupling is concentrated at `(u,-u)` and has cost `pi^p`.
Thus every finite reverse constant fails. There is no issue of nonattainment,
absolute continuity, or moments: the sphere is compact and Dirac masses are
admissible. The same argument rules out any unrestricted inverse modulus
vanishing at zero, and also works with the essential-supremum definition of
`W_infinity`.

The smooth odd perturbation check is correct as well. Each of `1 +/- a x_1`
integrates to one and is bounded below by `1-a`; odd cancellation kills their
difference under `F`. Coordinate `x_1` has tangential gradient bounded by one,
so its use as a Lipschitz test is legitimate. The difference in its integrals
is `2a integral x_1^2 d sigma = 2a/n > 0`.

These arguments settle the source's unrestricted question without using
Theorem 2. They are applications of the classical odd kernel, rather than a
new injectivity statement.

## 4. Explicit even harmonic: detailed checks

Put `z = x_1 + i x_2`, `H_k = Re z^k`, and let `k = 2m >= 2`.

### 4.1 Harmonicity, gradient, parity, and mass

Differentiating in the first two coordinates gives

`partial_1 H_k = k Re z^(k-1)`,

`partial_2 H_k = -k Im z^(k-1)`.

The two second derivatives cancel, and the remaining coordinate derivatives
vanish. Hence the ambient polynomial is harmonic and homogeneous of degree
`k`. Applying the Euclidean polar Laplacian to `r_ambient^k H_k` gives exactly
`-Delta_S H_k = k(k+n-2) H_k`. There is no sphere/ambient dimension shift.

A useful independent identity is

`|grad_Rn H_k|^2 = k^2 (x_1^2+x_2^2)^(k-1)`.

Euler's homogeneous identity gives `x dot grad_Rn H_k = k H_k`. Therefore,
on the unit sphere,

`|grad_S H_k|^2 = k^2 (r^(2k-2) - H_k^2) <= k^2 r^(2k-2)`.

This proves the claimed gradient estimate, including points where `r=0`,
without invoking polar angle coordinates at their singular set. Also
`|H_k| <= r^k <= 1`. Rotation by `pi/k` in the first coordinate plane changes
the sign of `H_k`, so its mean is zero. Even degree gives antipodal symmetry.
Thus `rho_k = 1+a H_k` is a normalized, smooth, even probability density with
the stated uniform bounds. Fixing `a` independently of `k` is essential and
is done in the theorem. No uniform derivative bound is silently assumed.

### 4.2 Equatorial eigenvalue

For a standard Gaussian vector `G` in a real `d`-dimensional Euclidean space,
write `G = T X`, with uniform unit vector `X` independent of radius `T`.
For real `v`,

`E(v dot G)^(2m) = (2m-1)!! |v|^(2m)`,

`E T^(2m) = d(d+2)...(d+2m-2)`.

Dividing proves the author's spherical moment formula for every degree.
Both sides are polynomials in the real coordinates of `v`; their polynomial
identity therefore holds over complex coordinates with the bilinear dot
product. It would be incorrect to insert a Hermitian norm, but the author
explicitly avoids that error.

For the real orthogonal projection `P = I-u u^T` and complex vector
`w = e_1+i e_2`, the identities `P^T P = P`, `w dot w = 0` give

`(P w) dot (P w) = -(w dot u)^2`.

Use the moment formula in `u`-perpendicular space of dimension `n-1`, then
take real parts. This yields precisely

`lambda_(2m) = (-1)^m product_(j=0)^(m-1) (2j+1)/(n-1+2j)`.

All factors have positive finite denominators. The eigenvalue is nonzero;
its modulus is at most one, strictly below one for `n>=3`. Both its sign and
normalization are correct. Special checks are `lambda_2=-1/(n-1)`,
`lambda_4=3/((n-1)(n+1))`, and in ambient dimension four
`lambda_k=(-1)^(k/2)/(k+1)`.

## 5. Radial moments and transport bounds

### 5.1 Radial distribution

For `n>=3`, normalized independent Gaussian coordinates give
`r^2 = (G_1^2+G_2^2)/(G_1^2+...+G_n^2)` with beta parameters
`1` and `alpha=(n-2)/2`. The second parameter is positive, including `1/2`
when `n=3`. Thus for real `q>=0`, beta integration gives

`M(q) = Gamma(alpha+1) Gamma(q/2+1) / Gamma(q/2+alpha+1)`.

The planar angle is uniform and independent of the radius; `r=0` is a
null set and introduces no integration ambiguity. Its cosine-square average
is `1/2` for every positive integer `k`, so `integral H_k^2 = M(2k)/2`.
Integrating the pointwise gradient estimate gives the stated `L^p` bound for
every real finite `p>=1`, not merely integer orders.

As an independent normalization check, integration of the exact gradient
identity gives

`integral |grad_S H_k|^2 = k^2 (M(2k-2)-M(2k)/2)`

`= k(k+n-2) M(2k)/2`.

The equality follows from `M(2k-2)/M(2k)=(k+alpha)/k`, and matches the
Laplace energy identity exactly.

### 5.2 Input lower bound

On a sphere, integrating a tangent-gradient bound along a minimizing
geodesic proves the corresponding global intrinsic Lipschitz bound.
Therefore `H_k/k` is an admissible 1-Lipschitz function. For every coupling,
its integral difference is at most the integral distance. This gives

`W_1(mu_k,sigma) >= a M(2k)/(2k)`.

For each probability coupling the `L^p` norm of distance is at least its
`L^1` norm. Taking infima preserves `W_p >= W_1`. No duality attainment or
`p=2`-specific result is needed. The lower bound is strictly positive.

### 5.3 Output upper bound and global flow

Set `L=k(k+n-2)>0`, `b=a lambda_k`, `eta_t=1+t b H_k`, and
`v_t=b grad_S H_k/(L eta_t)`. For the full compact time-space cylinder,
`eta_t >= 1-|b| >= 1-a >0`. Thus `v_t` is a smooth tangent field and has a
global smooth flow of diffeomorphisms for `0<=t<=1`. Large derivatives as
`k` grows do not obstruct existence for each fixed `k`; a uniform-in-`k`
flow theorem is not being used.

The sign is correct:

`partial_t eta_t + div_S(eta_t v_t) = b H_k + b Delta_S H_k/L = 0`.

For an explicit pushforward verification, let `J_t(x)` be the positive
surface Jacobian of the flow `Phi_t`. Its ordinary differential equation is
`J_t'=(div_S v_t)(Phi_t) J_t`. The chain/product rules give

`d/dt [eta_t(Phi_t(x)) J_t(x)] = 0`.

Its initial value is one, so `eta_t(Phi_t(x)) J_t(x)=1`. Change of variables
therefore proves `(Phi_t)_# sigma = eta_t sigma`. This verifies the claimed
transport without assuming a Benamou–Brenier formula or a weak-solution
uniqueness theorem. Negative values of `b` work identically.

The graph of `Phi_1` gives a valid endpoint coupling. For its trajectory,
intrinsic endpoint distance is no more than path length. Jensen on the unit
time interval gives

`d(x,Phi_1(x))^p <= integral_0^1 |v_t(Phi_t(x))|^p dt`.

For `p=1` the length-to-action step is simply equality for the time integral;
no strict-convexity assumption is used. Integrating in `x` and using the
pushforward identity gives the density factor **`eta_t^(1-p)`**, rather than
`eta_t^(-p)`. Since `1-p<=0`, this is at most `(1-a)^(1-p)`.
Taking the `p`th root and inserting the gradient moment cancels the factor
`k` in `L`, yielding exactly the author's bound (2):

`W_p(R mu_k,sigma) <= a |lambda_k| (1-a)^(-(p-1)/p)`

`                         * M(p(k-1))^(1/p)/(k+n-2)`.

The estimate remains valid at `p=1`; its positive-density factor then drops
out. It holds at arbitrary real finite orders. Moreover, `a>0`,
`lambda_k != 0`, and nonzero continuous `H_k` imply that the transformed
measure differs from `sigma`. Thus the actual denominator is strictly
positive, making division legitimate.

## 6. Limit, constants, and all boundary cases

Writing `k=2m`, gamma products give

`|lambda_k| = Gamma(alpha+1/2) Gamma(m+1/2)`

`                    / (sqrt(pi) Gamma(m+alpha+1/2))`.

For fixed parameters, the gamma-ratio asymptotic follows from Stirling:
`Gamma(t+c)/Gamma(t+d) ~ t^(c-d)`. Define

`A = Gamma(alpha+1)`,

`B = 2^alpha Gamma(alpha+1/2)/sqrt(pi)`.

Then `M(2k) ~ A k^(-alpha)`, `|lambda_k| ~ B k^(-alpha)`, and
`M(p(k-1))^(1/p) ~ A^(1/p) (p/2)^(-alpha/p) k^(-alpha/p)`.
Combining the correctly oriented lower and upper bounds gives (3). More
explicitly, its right side is asymptotic to `C(n,p,a) k^(alpha/p)`, where

`C(n,p,a) = sqrt(pi) (1-a)^(1-1/p) Gamma(alpha+1)^(1-1/p)`

`                   * (p/2)^(alpha/p)`

`                   / [2^(alpha+1) Gamma(alpha+1/2)] > 0`.

This independently checks both the factor `k=2m` and the surviving exponent.
The exponent is positive for every fixed finite `p>=1` and `n>=3`. A sequence
of positive quantities bounded below by a quantity tending to infinity also
tends to infinity; no claim about the sharp order of the true ratio is
needed. The lower bound is not asserted uniform as `p` grows with `k`.

Boundary audit:

- **`n=3`:** `alpha=1/2>0`; all beta and gamma expressions are finite and
  the exponent is `1/(2p)`. The smallest permitted dimension is covered.
- **`n=2`:** `R mu=(J_#mu+(-J)_#mu)/2`. On even measures both terms coincide,
  and the remaining quarter-turn is an intrinsic isometry. Pushing couplings
  forward and backward by this rotation gives equality of `W_p` distances,
  including `p=infinity`. The unrestricted antipodal obstruction persists.
  One must not use a beta density with parameter zero here; the author does
  not do so.
- **`n=1`:** no normalized nonempty equator exists; the note excludes it.
- **`p=1`:** both elementary transport inequalities and the zero density
  exponent are valid, with no limiting argument.
- **Noninteger finite `p`:** beta integration, Jensen, and real powers of
  strictly positive quantities are all valid; there is no integrality step.
- **`p=infinity`:** Theorem 2 does not follow from this ratio bound as
  written, and no such claim is made. The point-mass and circle assertions
  have separate direct proofs.
- **`k`:** the sequence uses positive even integers `k>=2`; the constant mode
  and odd modes are not being divided by their Laplace/Funk eigenvalues.
- **`a`:** `a=0` would give a zero-over-zero ratio and `a=1` would remove the
  general strict-density argument. Neither endpoint is included.
- The proof does not establish a failure of every weaker inverse modulus on
  the even class, an optimal rate, derivative-bounded classes, bandwidth
  restrictions, or restricted-support variants. Its stated exclusions are
  correct. The unrestricted zero-data example alone does not extend to the
  even class; that extension is justified by the separate high-frequency
  construction.

The brief remark about antipodal equivalence is consistent with the result.
Even probabilities correspond to probabilities on real projective space.
For the quotient geodesic distance, couplings can be lifted using the cheaper
choice of sign and then symmetrized, so the spherical distance between even
probabilities equals the quotient distance. Conversely, projecting any
spherical coupling can only decrease cost. Thus merely taking that quotient
does not evade the even-family counterexample.

## 7. Additional independent exact controls

`independent_exact.py` is separately authored and imports no author module.
It uses only Python's standard library. All **3,812 exact assertions** passed:

- 40 all-degree ambient gradient-norm polynomial identities
- 40 Euler identities and 40 harmonicity identities
- 600 eigenvalue comparisons against a separate Gegenbauer recurrence,
  600 nonzero/modulus checks, and 600 odd-nullspace checks
- 600 integrated gradient-energy identities, testing the beta and Laplace
  normalizations together
- 50 circle-mode checks
- 45 tangency and 45 exact projected-gradient checks
- 540 expanded continuity-equation identities and 540 positive-density checks
- 72 rational-exponent checks, including noninteger orders

The tests cover polynomial degrees through 40, spherical spectral modes
through 100, ambient dimensions through 14, and several rational amplitudes
including `999/1000`. These ranges are diagnostic, not an exhaustive
verification of infinitely many parameters. The expanded continuity controls
retain the reciprocal density and differentiate its effect algebraically;
they are not a numerical simulation of a transport map. No discrete or
floating-point Wasserstein calculation is used as evidence for a theorem.

Reproduce from this directory:

```sh
python3 ../release/check_exact.py > author_replay.recheck.json
cmp author_replay.recheck.json ../release/exact_results.json
python3 independent_exact.py > independent_exact_results.recheck.json
cmp independent_exact_results.recheck.json independent_exact_results.json
```

## 8. Final gate

Both claimed theorems, the boundary discussion, source interpretation, and
finite-check limitations pass. There are **no required corrections** and no
unresolved mathematical blocker within the stated scope. The audit leaves
the frozen author files intact. Publication wording should retain the
classical attribution, the restriction of the even-density theorem to finite
orders and `n>=3`, and the explicit absence of a novelty or human-review
claim. Bounded search results must not be promoted to an exhaustive
literature-clearance claim.
