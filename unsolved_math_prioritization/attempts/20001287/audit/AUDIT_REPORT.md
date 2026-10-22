# Independent adversarial audit of the spherical simplex volume product

Date: 2026-10-03 UTC. Problem: **20001287 / AIM-CONVEX_GEOMETRY-0019**, rank 510.

## Verdict

**PASS_FULL_PRIOR.** The frozen package proves the complete intended spherical-simplex inequality, in every ambient dimension, with the correct equality cases. It is a valid deduction from established functional inequalities. No novelty, priority, or newly discovered theorem is certified. The original question is mathematically answered by the cited machinery; the first historical explicit attribution of this application remains unverified.

For every full-dimensional pointed simplicial cone C in R^n, the normalized spherical-angle product satisfies

`ω(C) ω(C*) ≤ 4^(-n)`,

with equality exactly when C is an orthogonal image of the positive orthant. The positive dual is used. Degenerate convex chambers have zero product. The one-dimensional counting-measure convention is consistent.

No blocking mathematical or source defect was found. Two nonblocking editorial observations appear below. No frozen author file was changed and no remote mutation was performed.

## Frozen inputs and reproduction

The author manifest is frozen at `2026-10-03T17:55:23Z`; its SHA-256 is

`f8f59ad75dcd339d00d7a1fefaef95c88e20bc58f1d8340f00c64b961524f730`.

All seven listed files match both their manifest byte lengths and hashes. They were rechecked after all audit work. The author script writes a results file beside itself, so it was copied to a temporary directory before execution. The replayed result is byte-for-byte identical to the frozen `exact_results.json`.

The accompanying `audit_controls.py` uses exact rational arithmetic for its independent matrix tests and coefficient enumeration for the Hessian tests. Only replaying the author script requires SymPy. Run

`python3 audit_controls.py ../public`

from an audit directory alongside the public author directory, or pass any relocated author-directory path. A separate isolated run containing only these allowlisted files, launched from an unrelated working directory, reproduced the audit JSON byte-for-byte. Neither source downloads nor retrieval material are needed to run the controls.

These finite controls support the algebra and integrity claims. They do not substitute for the analytic inequality, its equality theorem, or the universal mathematical arguments below.

## Target and source recovery

The [official AIM problem list](https://aimath.org/WWN/mahlerduality/mahlerduality.pdf), printed page 4, was independently reopened. Its rendered page identifies Question 23, attributed to H. Koenig. The scan uses non-strict `≥ 0` in the positive spherical dual and `≤` in the proposed volume-product bound; its text extraction damages both signs. The ambient dimension is n, and the spherical dimension is n−1. The source asserts the n=3 case.

The symbol Δ and the comparison with an orthant support the usual convex spherical-simplex/chamber interpretation. An arbitrary union of hyperplane-arrangement regions is not the audited target. If n independent oriented hyperplanes define a full-dimensional chamber, writing their normals as the rows of an invertible matrix B gives C=B^(-1)R_+^n, so the cone is simplicial. If those normals are dependent, a nonzero common kernel gives lineality and confines the positive dual to a proper subspace. A lower-dimensional chamber itself has zero spherical measure. This verifies the package's treatment of degenerate chambers.

Closing versus opening the dual changes only a finite union of lower-dimensional spherical faces in the nondegenerate case. It does not change the product. The conventional negative polar is the negative of the positive dual and therefore has the same spherical measure.

## Imported analytic results

[Fradelizi–Meyer, Proposition 1](https://arxiv.org/pdf/math/0609553), inspected on printed page 5, is the geometric-mean form of Prékopa–Leindler for unconditional measurable functions. Its equality condition gives reciprocal positive diagonal rescalings and a positive scalar when the third function has the stipulated continuous multiplicative-midpoint-concave representative. No log-concavity of the first two functions is imposed. The [publisher's record](https://doi.org/10.1007/s00209-006-0078-z) confirms Math. Z. 256 (2007), 379–395, with online publication in December 2006. The incidental later date printed in the arXiv PDF is not its submission or journal date.

[Lehec, Lemma 8 and the proof of Theorem 9](https://arxiv.org/pdf/1011.2119), printed pages 4–5, independently supplies the orthant inequality and explicitly applies it to a linear orthant and its inverse-transpose dual. The cone-level estimate is established before summing over a Yao–Yao partition. That local step needs the representation of the cone, not an equipartition assumption. The [arXiv record](https://arxiv.org/abs/1011.2119) identifies the journal publication as Arch. Math. 92 (2009), 89–94, despite the 2010 arXiv deposit.

The audit used the actual primary arXiv statements and proof steps, not abstract-only attribution. A failed fetch of an author-hosted journal copy was not treated as a successful source inspection. The available primary text suffices for the application.

## Universal proof audit

### Gaussian reduction and all linear normalizations

Let the invertible generator matrix be A and put G=A^T A. Positivity of every generator pairing with y is equivalent to A^T y being coordinatewise nonnegative; consequently C*=A^(-T)R_+^n. The dual generator Gram matrix is

`(A^(-T))^T A^(-T) = A^(-1) A^(-T) = G^(-1)`.

This order is essential. In particular A^(-T)A^(-1) is not generally the same matrix.

For an isotropic standard Gaussian Z, its direction is uniform on the sphere and independent of its radius. Thus its cone probability equals normalized spherical measure. Changing variables z=Ax on C and z=A^(-T)y on C* yields respective factors |det A| and |det A|^(-1), and precision matrices G and G^(-1). Multiplication cancels the absolute determinants and gives

`ω(C)ω(C*) = (2π)^(-n) I(G)I(G^(-1))`.

If q denotes a Gaussian orthant probability parameterized by covariance, the individual probabilities are q(G^(-1)) and q(G), respectively. The package correctly reverses covariance and precision in the individual factors and then uses the symmetric product.

No determinant-one restriction, sign of det A, or positivity of the off-diagonal entries is needed. Multiplying individual generating columns by positive numbers leaves the cone unchanged; the proof incorporates the resulting diagonal congruence. It never assumes general linear invariance of spherical measure. Exact reflected-matrix controls explicitly test the absolute-Jacobian issue.

### Pointwise inequality and logarithmic substitution

Completing the square gives

`x^T Gx + y^T G^(-1)y − 2x·y = (y−Gx)^T G^(-1)(y−Gx) ≥ 0`.

For positive x,y this gives the comparison of the two quadratic Gaussian integrands with the square of the isotropic integrand at the coordinatewise geometric mean. After x_i=exp(u_i), every function acquires its Jacobian exp(Σu_i). The square root of the first two Jacobians is precisely the third Jacobian evaluated at (u+v)/2. Therefore ordinary Prékopa–Leindler applies exactly as written in the frozen proof.

All integrals are finite and nonzero: positive definiteness bounds the original integrands by a radially decaying Gaussian; the logarithmic substitution preserves the integrals. Prékopa–Leindler does not require that these transformed functions themselves be log-concave. The comparison integral is `(π/2)^(n/2)`. Squaring and multiplying by `(2π)^(-n)` produces `4^(-n)`, with no missing factor of 2, π, n, or sphere area.

An orthant has Gaussian mass `2^(-n)`, so the constant is attained. Ordinary spherical measure multiplies each normalized angle by σ(S^(n−1)), giving the claimed square of that sphere area.

### Equality branch

The absolute-coordinate extensions of the two integrands are continuous and unconditional. They are integrable because replacing coordinates by their absolute values preserves Euclidean norm and the same positive-definiteness bound applies. The pointwise condition is checked on the positive orthant, exactly the domain needed for Proposition 1. No false convexity assertion about these extensions is used.

For the third function h(x)=exp(−|x|²/2), multiplicative midpoint concavity follows from

`|x|²+|y|² ≥ 2 Σ x_i y_i`.

Its continuous representative is h itself. Whole-space extension multiplies each of the three integrals by 2^n, so equality for their product is equivalent to equality in the positive-orthant estimate. Proposition 1 then makes the first extension almost everywhere a positive scalar times h after a positive diagonal rescaling. Continuity upgrades this equality to pointwise equality. Evaluation at zero, or a limit to zero from the positive orthant, forces the scalar to be one. Equality of the quadratic polynomials on an open orthant forces every mixed coefficient of G to vanish.

Conversely, a positive diagonal G factors into n independent one-dimensional Gaussian integrals and gives equality. A^T A diagonal means the generating columns are pairwise orthogonal, and positive column rescaling does not change the cone. Thus the equality set is exactly the orthogonal orthants, rather than all linear images of the orthant. The proof correctly does not infer equality of integrals from equality at isolated pairs in the pointwise square identity.

### Dimension one and geometric limits

For n=1, a full-dimensional pointed cone is either half-line. C and C* each meet S^0 in one point; with counting measure their normalized angles are 1/2 and their product is 1/4. The entire functional proof and its equality condition also apply. No theorem used here requires n≥2.

Degenerate cones cannot add equality cases because their product is zero while the stated upper bound is positive. There is no hidden compactness or attainment assumption in the proof.

## Auxiliary local expansion audit

The Hessian claim is correct in the normalized zero-diagonal symmetric Gram chart. The audit independently enumerated monomial coefficients using the half-normal moments, rather than merely reusing the author's final coefficient formula.

For an edge variable h_ij, the term X_i X_j has mean a=2/π. Products from identical, incident, and disjoint edges have moments 1, a, and a², respectively. Expanding the determinant and inverse covariance in the Gaussian density cancels every second-order term except a² times the sum over disjoint edge pairs. Applying the first covariance differential to the t²H² term in the inverse matrix contributes a times the sum over incident edge pairs. The resulting normalized product coefficient is

`−(a−a²) E − (a²−a/2) ||H1||²`, where `E=Σ_(i<j) h_ij²`.

Substitution of a=2/π recovers both printed coefficients, including their signs. Their positivity proves a negative-definite Hessian on every nonzero zero-diagonal direction. Since `||H||_F²=2E`, reserving half the leading lower bound gives the particular local stability constant printed in the package, after shrinking the dimension-dependent neighborhood to absorb the cubic remainder.

The uniform Taylor justification is sound: in a fixed-dimensional neighborhood, eigenvalues stay bounded away from zero and covariance derivatives are bounded by polynomial multiples of an integrable fixed Gaussian. It supports a genuine neighborhood estimate, without implying a dimension-uniform radius or a global quantitative stability theorem. The single-edge restriction yields deficit `4t²/π²`, matching the exact planar arcsine formula. No historical novelty for this Hessian is certified or required.

## Obstruction and scope controls

The circular cone with half-angle π/4 in R³ is self-dual under the positive-dual convention. Its normalized angle is `(2−√2)/4`; its squared angle exceeds 1/64. The inequality reduces to `23>16√2`, valid because both sides are positive and `529>512`. This is a valid counterexample to an arbitrary-convex-cone extension and does not contradict the simplicial theorem.

The wedge and orthogonal-product reductions in the earlier partial approach are correct calibrations but are insufficient for the general coupled case. The full proof covers arbitrary positive-definite Gram matrices, so it actually closes that gap. Stopping after the third of five allowed approaches is justified by the complete deduction; the omitted two routes are not being counted as attempted work.

## Exact audit controls and limitations

The portable audit records:

- Seven frozen file checks, before and after testing.
- A byte-identical isolated replay of all author checks.
- Eighteen rational generator test instances in dimensions 1–6, rechecked without SymPy in the independent arithmetic implementation.
- Eighteen additional orientation-reflected instances, plus positive diagonal generator-rescaling checks.
- Full quadratic-form coefficient checks of the Young square certificate.
- Independent density and product coefficient enumeration in every dimension 2–8, with every unordered edge-pair coefficient checked.
- Four diagnostic algebra negative controls and two actual temporary-file integrity corruptions, all rejected.
- A second portable isolated run with byte-identical output.

The matrix list contains **17 distinct matrices among 18 test instances**: the one-dimensional family-0 and family-2 matrices coincide. This is harmless; the author does not depend on finite tests to prove a universal statement. The report uses “instances” to avoid implying uniqueness.

No numerical integration, random sampling, or unrefereed recent preprint is an input to the proof. An absence of search matches is not a historical-priority certificate. This audit did not duplicate account-specific repository-history searches; those bounded author-stage observations do not support, and are not needed for, the mathematical verdict.

## Nonblocking editorial observations

1. The displayed ordinary-volume constant in `PROOF.md` contains `s_{n−1}^{,2}`. The comma is a typographical artifact; the definitions, README, and proof unambiguously require `s_{n−1}²`. A future separately versioned editorial cleanup may remove it.
2. The finite checker description may be sharpened to “18 rational matrix instances, 17 distinct,” as noted above.

Neither issue changes the proof or warrants a mathematical hold. Frozen content was left untouched.

## Release boundary

The appropriate disposition is a complete classical deduction with equality, without a novelty claim. This verdict does not authorize publication and does not establish who first explicitly resolved the AIM formulation.

The audit release allowlist consists only of this report, `audit_controls.py`, `audit_controls.json`, and the audit manifest. Downloaded papers, rendered source pages, full-source extracts, corpus records, private context, and unallowlisted caches are excluded. No remote files, repository state, queue entry, branch, commit, or pull request was changed during this audit.
