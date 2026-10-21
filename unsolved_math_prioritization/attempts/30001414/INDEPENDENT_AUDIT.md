# Independent mathematical audit

## Reviewed versions and verdict

**PASS AS SCOPED PARTIAL RESULTS; NOT A COMPLETE CLASSIFICATION.** Independently reviewed on 2026-10-21. This acceptance applies to precisely these file versions:

- File: `BOUNDARY_CONSTANTS_ANALYSIS.md`
  - SHA-256: `9c1dd546f3d91c937aa349eec3433e86eb5f34f1bae1c972153bd706325385ec`
  - Byte count: 19599
- File: `LOCAL_THIRD_ORDER_HARDY.md`
  - SHA-256: `d349a175b5cbbf65aa489b4ba8643ec72132101599394f7eb0d8a07ea7ad7b53`
  - Byte count: 6255

This is a human-readable mathematical audit, not a formal proof certificate or a novelty claim. Subsequent changes to either file require renewed review of the changed claims.

The transparent-extension theorem, first-order mixed-boundary obstruction, finite-codimensional obstruction lemma, flat-patch second-order Robin construction, and centered-ball third-order Hardy-only proposition are valid under their stated hypotheses. No substantive counterexample or fatal gap was found. The global homogeneous-space requirement, exact parity of the energy operator, and restricted scope are essential. The reviewed main report explicitly justifies Hardy-denominator finiteness and Robin coercivity.

## 1. Homogeneous realization and exact exterior operator

The relevant completion is that of smooth compactly supported functions in the norm `||L_m U||_p`. For `1<p<infinity` the Riesz-transform estimates identify this norm with the full order-m derivative norm. The subcritical hypothesis `mp<n` fixes a unique representative in `L^{np/(n-mp)}`; polynomial ambiguity is therefore absent.

The report correctly uses exactly these exterior conditions:

- Even `m=2k`: `Delta^k U=0` almost everywhere outside the domain.
- Odd `m=2k+1`: `gradient Delta^k U=0` almost everywhere outside the domain.

In the odd case, `Delta^k U` is constant on each connected exterior component. Merely assuming `Delta^{k+1} U=0` would not suffice: already `U=x_1^3` locally satisfies `Delta^2 U=0` while `gradient Delta U=6 e_1`. This local example diagnoses the false inference; it is not asserted to belong to the global homogeneous space. The report does not make that inference.

A piecewise classical exterior solution is not enough. The single global continuation must lie in `D^{m,p}`. This excludes interface measures from unmatched traces. The report's definition imposes that requirement before the energy identity is used.

## 2. Restriction, injectivity, closedness, and cavities

Global homogeneous Sobolev bounds give, for `0<=j<m`,

`||D^j U||_{L^{np/(n-(m-j)p)}(R^n)} <= C ||L_m U||_p`.

Holder's inequality on the bounded domain then controls every lower local `L^p` derivative. Together with the Riesz-transform estimate at order m, restriction is continuous from `D^{m,p}` into `W^{m,p}(Omega)`.

The zero-exterior-energy subspace is closed because its image under `L_m` is supported in the fixed measurable set Omega. Restriction is injective: if its interior restriction vanishes, the distributional derivatives vanish in the interior, while the defining condition makes `L_m U` zero outside. Thus the entire homogeneous norm vanishes. This argument is unaffected by bounded complementary cavities.

For every lift, the exact identity is

`||U||_D^p = ||L_m u||_{L^p(Omega)}^p`.

It supplies a bounded inverse on the image and makes lifts of a convergent `W^{m,p}` sequence Cauchy in the complete homogeneous space. The closedness proof is therefore valid and does not incorrectly assume that an arbitrary continuous image of a closed subspace is closed.

Zero extension gives the inclusion of `W_0^{m,p}`. On the stated smooth domains, membership in `X_ext` is genuinely trace-determined: adding any `W_0^{m,p}` function preserves membership. No hidden equation is being imposed on the interior source.

## 3. Sharp constants and non-Navier examples

The energy identity and monotonicity of both denominator integrals yield the lower bounds by the whole-space sharp constants. The direction of both inequalities is correct. No equality between interior and global denominators is required or claimed.

The opposite bounds follow from the contained zero-trace space. Equivalently, compactly supported whole-space near-minimizers can be dilated into an interior ball. Dilation must be centered at the singularity for the Hardy quotient, which is why `0 in Omega` is essential. Both constants are consequently sharp.

For even order, the potential image `I_{2k}(f 1_Omega)` is valid for `1<p<n/(2k)`. The inverse normalization concerns `(-Delta)^k`; its sign relative to `Delta^k` does not affect the space or energy. Uniqueness in the homogeneous space proves the converse representation.

The positive compactly supported source witnesses are valid for all stated orders. For odd order `m=2k+1>=3`, the chosen `I_{2k} f` has order-m derivatives decaying as `|x|^{-n-1}`. Cutting it off at radius R incurs norm error `O(R^{n/p-n-1})`, which tends to zero for every `p>1`. Thus the claim of actual homogeneous-space membership is justified, rather than inferred solely from its differential equation. Positivity of its boundary value proves failure of the zeroth Navier trace.

For `m=1`, the hole-constant characterization is correct under the stated smoothness and finite-component assumptions. The unbounded exterior constant is forced to be zero by global `L^q` integrability. Matching traces permits extension by the chosen constants in the holes. Connected exterior therefore reduces this particular first-order family to the usual zero-trace space.

## 4. First-order mixed-boundary obstruction

A nonempty relatively open free patch admits a boundary-centered half-bubble whose trace is supported inside that patch. A normalized boundary chart has identity metric at the concentration point, so the numerator and the qth-power denominator approach one half of their full-space values. Their quotient factor is

`(1/2) / (1/2)^{p/q} = 2^{-p/n}`.

Radial whole-space near-minimizers are available by first-order rearrangement and compact approximation. The strict upper bound follows for every `1<p<n`. No Hardy result is needed to rule out simultaneous preservation.

The classification is valid only for the declared partition into relatively open Dirichlet/free pieces with negligible interface. It is not a result about arbitrary exceptional boundary sets, capacity conditions, or nonlocal trace coupling. The report respects that limitation.

## 5. Finite-codimensional correction

The lemma is valid even when the underlying linear space Y is not closed. Linear independence of the restricted functionals makes their finite-dimensional evaluation map onto; therefore fixed dual correction vectors exist in Y. Weak convergence of the bubbles makes all correction coefficients tend to zero. The corrected sequence changes by a term converging strongly to zero in `W^{m,p}` and hence in critical `L^q`.

Because the original sequence is bounded and its denominator stays bounded away from zero, the energy and denominator perturbations imply convergence of the quotient difference to zero. Separate convergence of the individual numerator and denominator is unnecessary.

The mixed and Robin bubbles meet the weak-null hypothesis. Their highest derivatives have bounded `L^p` norm and shrinking supports, while their lower derivatives converge strongly to zero. Testing the highest derivatives against `L^{p'}` functions proves weak convergence directly by absolute continuity of integrals.

## 6. Second-order positive Robin construction

For `m=p=2`, `n>4`, the stated smooth domain with a flat patch exists, and smooth positive beta has a positive minimum on the compact boundary. Green's identity proves the kernel is trivial.

With the outward normal `nu=-partial_t`, the multiplier `exp(beta(y)t)` has the correct sign: at `t=0`, radial evenness of the bubble gives `partial_t u=beta u`, hence `partial_nu u+beta u=0` exactly. Compact support avoids all other boundary pieces.

After scaling, the multiplier becomes `exp(epsilon beta(epsilon z') z_n)`, converges to 1 in every needed derivative on fixed supports, and produces only lower-order errors. The half-space quotient factor is exactly

`(1/2) / (1/2)^{2/q} = 2^{-4/n}`.

Smooth radial compact near-minimizers for the whole-space Hilbert biharmonic Sobolev constant are legitimate. The strict upper bound and its persistence under finite continuous linear side constraints follow.

For the additional coercivity statement, one may combine the smooth Robin elliptic estimate `||u||_{W^{2,2}} <= C (||Delta u||_2+||u||_2)` with the trivial kernel and compactness. Alternatively, the positive Robin quadratic form controls the `W^{1,2}` norm, and Green's identity first yields `||u||_2 <= C ||Delta u||_2`; the elliptic estimate then yields full `W^{2,2}` coercivity. The sharp loss is therefore compatible with coercivity, not only with absence of a kernel.

## 7. Prior-work guardrail

The even-order potential-image boundary class is prior Kac/polyharmonic Newton-potential territory. It must not be presented as a newly invented boundary class.

- G. Rozenblum, M. Ruzhansky, D. Suragan, *Isoperimetric inequalities for Schatten norms of Riesz potentials*, Journal of Functional Analysis 271 (2016), 224-239. DOI: https://doi.org/10.1016/j.jfa.2016.04.023 . Inspected author preprint: https://arxiv.org/pdf/1506.06355 , version 2, pages 2-3, equations (1.8), (1.10)-(1.11), and reference [16]. It explicitly relates the polyharmonic Newton-potential image to nonlocal boundary conditions and states a converse in the Hilbert setting. The paper's main subject is spectral isoperimetry, not the complete classification posed in the source question.
- T. Sh. Kal'menov and D. Suragan, *Boundary conditions for the volume potential for the polyharmonic equation*, Differential Equations 48(4) (2012), 604-608. Verified publisher metadata and abstract: https://link.springer.com/article/10.1134/S0012266112040155 . The full 2012 article was not inspected; the precise boundary formulas were checked in the 2015 preprint above, which cites it.

These sources defeat a novelty claim for the boundary class itself. They do not by themselves establish that the exact all-p simultaneous sharp-constant statement was already published. No priority claim either way is justified by this bounded source check.

## 8. Remaining scope limits

The report gives sufficient classes and restricted counterexamples, not a classification of all higher-order local or nonlocal boundary conditions. The local third-order lower-clamped space is not automatically an energy-preserving extension class. An arbitrary extension with positive exterior energy cannot supply the desired exact lower bound, because the added energy is on the wrong side of that argument.

The companion establishes only a Hardy equality on a centered ball for `m=3, p=2, n>6`. Neither file claims that the critical Sobolev equality holds for that local space. The main report must not be labeled a complete resolution of the original open question.

## 9. Independent audit of the third-order Hardy companion

The companion's calculation was independently rederived, not accepted solely from the main report's cross-reference. Put `a=(n-6)/2`, `c=(n-2)/2`, `lambda=ell(ell+n-2)`, `C=c^2+lambda`, and `d=C-4`. For `u_ell(r)=r^{-a}v(-log r)`, the radial Laplacian formula gives exactly

`Delta(u_ell Y_ell)=r^{-c}(v''-4v'-dv)Y_ell`.

The radial gradient and angular gradient contributions yield `integral ((w'+cw)^2+lambda w^2) dt`, while the Hardy denominator is `integral v^2 dt`. The condition `u=partial_nu u=0` at radius 1 becomes `v(0)=v'(0)=0` with no missing lower-trace condition.

Integration by parts gives the derivative coefficients `3C+8`, `d^2+C(16+2d)`, and `Cd^2` exactly as displayed. The cross term in `integral (w'+cw)^2` contributes `-c|v''(0)|^2`; expansion of `integral |w'|^2` contributes `+4|v''(0)|^2`. Thus the full boundary coefficient really is `4-c`, which can be negative and must not simply be discarded.

The companion correctly absorbs this potentially negative term by

`integral (|f'|^2+A|f|^2) >= sqrt(A)|f(0)|^2`,

applied to `f=v''` and `A=3C+8`. The remaining boundary coefficient `sqrt(3C+8)+4-c` is positive for all `n>6` and all modes. Also `C>4`, so all residual derivative coefficients are nonnegative and `C(C-4)^2` increases with C. The lowest spherical mode therefore gives the constant

`((n-6)(n-2)(n+2)/8)^2`.

Orthogonality correctly diagonalizes both quadratic quantities. Finite harmonic sums preserve the two lower traces; convergence on annuli justifies passage to the smooth class. Smooth density in the trace kernel is valid on the smooth ball. For each smooth function, removal of the origin in `H^3` costs at most order `epsilon^{n/2-3}` in the highest cutoff error, which tends to zero precisely under the sufficient hypothesis `n>6`. Diagonal approximation and Fatou therefore extend the inequality to the whole stated space.

The annular functions determined by `v_T(t)=psi(t/T)` are smooth and compactly supported inside the ball for every finite T. Their denominator is order T and their jth derivative-square integrals are order `T^{1-2j}`. Their quotients approach the claimed constant. On the whole logarithmic line there is no endpoint term, and the same expansion plus origin-cutoff argument proves the corresponding global lower bound. The same annular sequence proves whole-space sharpness. The global constant identification is therefore established within the companion rather than assumed from an unverified formula.

The non-Navier witness `(1-|x|^2/R^2)^2` has zero value and normal derivative on the sphere, but `Delta u=8/R^2` there. Its use is correct. The companion and the main cross-reference consistently state that no critical Sobolev equality is proved for this local space.

## Final acceptance boundary

Accepted: the exact claims in the two hash-bound files, with their assumptions and explicit limitations. Not accepted or asserted: novelty priority; a complete solution to the source classification problem; preservation of both constants for the lower-clamped third-order local space; extension of its Hardy proposition to arbitrary domains; or any replacement of the exact odd-order exterior condition by mere polyharmonicity.
