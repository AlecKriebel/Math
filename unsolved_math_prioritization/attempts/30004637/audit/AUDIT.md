# Independent audit of branching Brownian transport components

Problem 30004637, OWR-4990379-007, rank 560. Reviewed 4 October 2026.

## Verdict

**Pass as an explicitly unresolved, limited-results attempt. The general fast-algorithm question is not solved.** The analytic claims in the frozen packet withstand the checks below on their stated domains. No mathematical blocker to publishing this limited-result packet was found. This is an adversarial technical review, not peer review, a formal proof certificate, or an exhaustive assessment of the literature.

The required queue disposition is **`unsolved`, `5/5`**. The artifact's descriptive label `partial` accurately describes its limited results and may remain. Two frozen publication instructions are stale: `STATUS.json` gives `queue_authorized_delta.status = partial`, and the publication paragraph of `SOURCE_GATE.md` also requests `partial`. Those instructions must not determine the queue edit. This separate audit records the override to `unsolved`, `5/5`; it does not alter the frozen files.

The reviewed `FROZEN_MANIFEST.json` SHA-256 is:

`4cb91682ffaec4cbd318ad91059c57246fff5285308eaa51abc9ce81b8caab8a`

All nine listed file sizes and hashes match. All four cited source-document hashes and sizes also match the source manifest. The author replay is byte-for-byte equal to its frozen `checks.json`.

## Source scope and attribution

The complete Baradat contribution in [OWR 10/2021](https://doi.org/10.4171/OWR/2021/10), printed pp. 552–555, was inspected. The specific question on p. 555, section 3.2, was also checked visually. It concerns the preceding diffusive RUOT model for nonnegative finite measures, with a growth penalty induced by an offspring distribution. It does not give a computational input model, accuracy norm, rate, or definition of fast. A finite-grid operation count is therefore useful but does not by itself answer the question.

The complete numerical section 6.3, printed pp. 115–122, of [Baradat–Lavenant v2](https://arxiv.org/abs/2111.01666v2) was inspected. It already describes dynamical convex optimization, proximal splitting, affine projections, and the local projection mechanism. Its direct Sinkhorn discussion concerns nonlinear propagation and lack of the usual time symmetry. Remark 6.14 explicitly leaves continuum convergence of the discretization outside its treatment. The packet gives appropriate credit and does not repackage this established numerical method as a new solution.

The displayed derivative after Lemma 6.17 and the monotonicity wording on preprint p. 122 were visually inspected. The numerator lacks the square needed by the chain rule, and the wording gives the wrong monotonicity direction. The packet's corrected squared derivative and strictly decreasing scalar residual are correct. This finding is confined to that inspected preprint version.

For the [2025 Astérisque monograph](https://doi.org/10.24033/ast.1247), the available official sample establishes publication and describes numerical convex optimization. It is not the complete 2025 numerical chapter. The audit does not claim to have inspected the full published chapter or to know whether its typographical errors were corrected. The packet's source gate accurately distinguishes this from the full preprint read.

Sections 4.6 and 7, Appendix B.3, and Appendix C.11 of [Ying et al. v2](https://arxiv.org/abs/2605.00545v2) were inspected. They explicitly use a WFR approximation to the RUOT semi-coupling. The additional small numerical comparisons do not supply a uniform approximation theorem or an exact solution of the OWR target. In particular, the second-order penalty approximation and the move to ordinary WFR must not be conflated with retaining the original diffusion constraint. The packet makes this distinction.

These conclusions concern the supplied, hash-verified source versions. No fresh remote search or independent verification of current repository state was performed in this audit. Prior-work absence claims remain bounded checks recorded by the author, not a proof of nonexistence of another solution or attempt.

## Mathematical review

### 1 Endpoint propagation

For the allowed pure-birth case, the probability generating function solves the scalar branching equation and has the stated rational form. Its second derivative is strictly positive when time is positive and the input lies between zero and one. A fixed linear kernel cannot produce that nonlinear dependence on a constant input.

This rules out the unchanged linear endpoint-propagation step, not all Sinkhorn-like methods, nonlinear updates, alternate representations, or fast algorithms. The packet maintains this scope. The scalar example also does not purport to derive a complete endpoint solver.

### 2 Binary perspective and proximal operation

The critical-binary Legendre transform, first two derivatives, and perspective Hessian are correct. The closed extension at zero density is essential: finite cost at vacuum requires both momentum and source to vanish. Maximization over the dual sublevel set gives exactly the stated support function, including at zero and negative density. This verifies the conjugate without assuming differentiability at vacuum.

For the local projection, the inner scalar map has derivative at least one and a unique root between zero and the input. Differentiation yields a squared first derivative in the numerator. Consequently, the outer residual has derivative at most minus one. Its initial value supplies the finite outer bracket. The normal-cone condition proves that the candidate is the Euclidean projection, and the support-function argument proves the stated Moreau formula for every positive proximal parameter.

The outer bisection count presumes exact inner signs. The pointwise Lipschitz bound and inner residual-to-root bound are valid, but are not a validated floating-point implementation. Large input divided by small diffusion may overflow ordinary hyperbolic-function evaluation or make the bounds unusable. The packet expressly declines uniform conditioning and bit-complexity claims.

These formulas are not a general-offspring routine. For example, the law concentrated at one offspring has zero conjugate penalty and a growth cost that is an indicator of zero growth. Heavy-tailed laws may have an extended-valued exponential generating function with restricted domain. Smooth binary formulas cannot be silently used in those cases. The binary restriction and separate general-law gap are adequate.

### 3 Affine projection and grid boundaries

The prescribed one-dimensional periodic backward-Euler constraint has the correct diffusion sign. The endpoint right-hand side is correct both for a single time step and for multiple time steps. Eliminating only interior densities gives the two neighboring temporal coefficients used in the Gram matrix. Free sources give a negative identity block, so the matrix has full row rank and its Gram matrix is bounded below by the identity. This is why no mean-zero compatibility condition or constant-mode nullspace occurs here. Removing or restricting the source block would change that conclusion.

The spatial symbol, temporal diagonal blocks, and adjacent off-diagonal blocks are correct. Spatial periodicity is necessary for the FFT diagonalization as written. Fixed temporal endpoints are not being treated as periodic; they produce the distinct first and last temporal diagonals. The one-time-step, one-spatial-cell, and zero-diffusion cases are included. The positive-definite tridiagonal systems admit elimination with positive pivots.

The arithmetic cost and storage bound are justified for local stencil application plus FFTs and tridiagonal solves. They are not a bit-complexity, numerical-stability, or total-solver result. The verification program intentionally constructs dense small reference matrices and applies dense difference matrices; it is not an implementation demonstrating the advertised asymptotic runtime.

Mass accounting is consistent: summing the constraint over a periodic spatial grid gives the discrete mass difference equal to the summed source. It does not impose balanced mass when growth is allowed.

Affine projection does not preserve positivity. A new exact control gives a concrete witness with two time steps, one spatial cell, and both endpoint densities equal to one. Starting with interior density minus ten and zero momenta and sources, the affine projection has interior density **minus two ninths**, while satisfying every affine equation exactly. Thus it cannot be substituted for a positive-density projection. The packet already states this limitation.

### 4 Restricted rate and dual certificate

The Hessian quadratic form is correct. The stated bound follows by bounding the two rank-one quadratic forms, using the positive lower density bound and the global binary bound on the growth-cost second derivative. Taking the largest cell weight is appropriate because the cell blocks are disjoint in the Euclidean norm. Segment integration on the convex set justifies the descent bound. The projected-gradient telescoping argument and monotonicity give the claimed inverse-iteration objective rate.

No strong convexity is available from this Hessian on a general domain. Positive homogeneity supplies a radial null direction: the Hessian annihilates the vector consisting of density, momentum, and source themselves. An independent exact symbolic control confirms this. The packet does not claim strong convexity, a unique optimizer, or a linear global convergence rate.

The projection onto the compact convex set is an explicit oracle assumption. Intersecting the affine set with positivity and magnitude bounds does not make the projection equal to the affine formula. The lower-density parameter cannot be sent to zero while retaining the stated Lipschitz constant. The theorem therefore does not handle vacuum or arbitrary singular endpoint measures uniformly.

The dual condition has the correct sign and weight normalization for the stated all-variable perspective objective with equality constraints. Summing the support-function inequalities proves weak duality and the upper bound on the primal gap. Strong duality and attainment are not needed for this inequality. A new exact, nonzero, weighted one-cell witness attains equality and checks the scaling convention.

For a usable certificate, primal feasibility must include finite objective value, in addition to the affine equality. This is the standard domain interpretation of primal feasible. If it meant only the equality, an infinite objective and infinite infimum could make the displayed subtraction undefined. Similarly, both primal and dual constraints must be exact or have certified corrections; small residuals alone do not certify the claimed gap. Endpoint elimination, an interpolated objective, or additional boxes changes the conjugate/dual bookkeeping and requires its own derivation. The packet correctly presents the certificate separately as an all-variable statement rather than identifying it with the preceding reduced-variable grid.

### 5 Quadratic surrogate

The global one-sided quartic bound follows from the second-derivative inequality and two integrations. The coefficient is correct and is sharp to leading order at zero; an independent exact Taylor coefficient confirms it. Evenness covers negative growth. The large-growth asymptotic establishes that the two penalties are not uniformly relatively equivalent.

The value bound requires the same admissible class, the same diffusion constraint, bounded growth, and bounded integrated mass. For a finite difference of infima, the class must admit a finite-cost competitor. Under those assumptions, taking infima in the two objective inequalities is valid. The result does not imply closeness of minimizers.

The growth restriction has a substantial zero-endpoint consequence. On the torus, bounded growth implies that total mass obeys the absolute derivative bound by the growth bound times mass. Gronwall's inequality then prevents a curve with a zero endpoint mass and a positive opposite endpoint mass. Thus this surrogate estimate cannot supply a uniform bound for the source question's full endpoint class. This is a limitation of the stated restricted class, not a counterexample to the restricted inequality.

Replacing the penalty and dropping diffusion are two different changes. The packet quantifies only the former on a shared admissible class and correctly does not transfer its estimate to ordinary diffusion-free WFR or to the full USB pipeline.

## Reproducibility results

The original verification program was run without changes. Its output is stored as `replay_checks.json` and is identical to the frozen reference.

- Three symbolic check groups passed: Legendre derivatives, perspective Hessian, and pure-birth second derivative.
- All 144 local projection/proximal cases passed, including 36 inside-set and 108 outside-set cases. The largest KKT stationarity residual was about 6.71e-16; the largest relative Moreau gradient residual was about 1.49e-14.
- All 60 affine projection cases passed. The largest relative dense-projection error was about 1.91e-14, and the largest relative feasibility error was about 2.41e-14.
- All 33 surrogate checks passed.

The additional `independent_checks.py` supplies 18 exact rational grid controls for temporal boundary blocks, full row rank, mass telescoping, and the identity lower bound on the Gram matrix. It also checks the negative-density witness, Hessian radial degeneracy, corrected projection derivative, weighted tight dual witness, and sharp quartic Taylor coefficient. Results are stored in `independent_results.json`.

The floating-point replay is regression evidence only. The finite symbolic controls also do not prove continuum convergence or establish an unrestricted solver. The mathematical arguments, including their domain restrictions, determine the verdict.

## Publication conditions and remaining target

Publish only with the unresolved classification and the explicit queue override above. Do not describe the attempt as an exact, general, fast RUOT solver or an impossibility theorem. Do not claim the 2025 full chapter was reviewed, import the 2026 numerical comparisons as a uniform error guarantee, or convert arithmetic cost for one affine operation into total time to solve the continuum problem.

A full algorithmic answer still needs a suitable input and error model, treatment of relevant offspring domains and endpoint measures, a finite-cost discretization with positivity, implementable global optimization and stopping guarantees, inexact-arithmetic control, and a quantitative connection to the continuum objective. The five approach families supply limited tools and identify these gaps. The frozen packet acknowledges them adequately.

No frozen author file or remote state was modified. The audit contains original commentary, source references, and verification code/results; no source-document copies or extracts are included.

AI-assisted and unrefereed. No novelty or priority claim.
