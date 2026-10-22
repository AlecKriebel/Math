# Independent audit: uniform advection–diffusion control

Problem 30003759 / OWR-16157-001, rank 739. Audit date: 2026-10-05.

## Verdict and queue gate

**REVISE_REQUIRED for an unqualified full-resolution disposition.** The mathematics retained in the frozen packet and its precise prior-preprint source match pass this audit. No mathematical defect was found in those elementary proofs. The source match does not resolve the positive critical endpoint, which the original report's attained-minimum wording includes.

Recommended queue status: **unsolved**, **1/5**. Recommended Findings: “Koike–Laheurte (2026 preprint) determines the sharp infimum thresholds 2L/M for M>0 and (2+2√2)L/|M| for M<0; the negative critical endpoint has vanishing cost. Positive critical endpoint boundedness remains open. Independent source match, elementary proofs and scoped proof-chain review passed; no new full solution or priority claim.”

This verdict distinguishes publication of useful qualified findings from a solved marker. It does not reject the cited preprint's threshold theorem. If a separate field specifically records the infimum-only subproblem, that field may say `prior_resolution_preprint` with its limitations. It must not replace the overall status above.

## Mandatory disposition corrections

1. Do not label the entire catalog problem `already_solved`, `solved`, or unqualified `prior_resolution_preprint`. Retain the positive endpoint as unresolved.
2. The packet's statement that no further campaign is warranted is not a mathematical conclusion about the original endpoint-inclusive problem. It may describe the author's stopping decision for infimum research only. The overall queue must retain the remaining question.
3. Describe this review as an **independent AI mathematical proof review**. It is not human peer review, journal acceptance, formal verification, or a machine-checked proof of continuum observability.
4. If stronger H⁻¹-unit-ball cost claims are later proposed, prove that extension separately. The verified cost normalization is L², even though the state well-posedness discussion permits H⁻¹ data.

The author freeze was not edited. These corrections can be supplied as an explicit overarching audit/disposition document while preserving the frozen historical author packet.

## Source and exact-problem verification

The full public catalog statement was read locally. Its UTF-8 SHA-256 matches the descriptor exactly. The separate inspected research-results corpus has no target-key, ID, or target-title match; this is not a claim of universal prior-work absence. The dated catalog literature assessment predates the September 2026 manuscript.

The original scholarly source is Arnaud Münch's contribution in [Oberwolfach Report 16/2018](https://publications.mfo.de/bitstream/handle/mfo/3638/OWR_2018_16.pdf?isAllowed=y&sequence=1), printed pp. 951–952. Both page images were inspected, in addition to reading the complete contribution. Its equation (3) normalizes the initial datum in L² and minimizes the L² time norm of a Dirichlet control at the left endpoint. The right endpoint is homogeneous. The viscosity is positive and tends to zero, and both signs of the nonzero constant transport coefficient are in scope. Sphere versus ball is immaterial by linearity. The prose does use attained-minimum and endpoint-inclusive language, so that question cannot silently become an infimum-only problem.

The exact PDE, boundary location, signs, cost, and fixed-parameter quantifiers match [Koike–Laheurte, arXiv:2609.35355v1](https://arxiv.org/abs/2609.35355). Theorems 1.3–1.4 distinguish strict positive-speed inequalities from an included negative-speed endpoint; the sentence after Theorem 1.3 expressly leaves positive critical boundedness open. The arXiv record was checked live: submission 2026-09-28, v1 only in the inspected record, and no journal-reference field. “Preprint” is the supported publication description.

The OWR omission of interval-length factors and its conflicting negative-speed numeric comparison are genuine printed features, not extraction artifacts. They do not change the displayed PDE/cost and are not accepted as valid estimates. The new theorem is not obtained by importing those historical prose assertions.

Fresh independent downloads of both PDFs matched the author's byte counts and SHA-256 values exactly. Public hashes and inspection scope appear in SOURCE_AUDIT.json; PDFs, extracts, catalog contents and image renders are excluded from this deliverable.

## Retained elementary proofs

All five sections were read in full and independently checked.

- Homogeneity of the minimal control norm gives equality of unit-sphere and unit-ball costs. A finite limsup is equivalent to an eventual uniform bound; an arbitrarily enlarged constant handles an infimum not known to be attained.
- With a=|M|, spatial coordinate x/L, time at/L, and amplitude √L, initial L² norm is unchanged and squared control norm is multiplied by a. Therefore the cost factor is a^(-1/2), and the threshold time factor is L/a. No missing √L remains.
- Extension of a null control by zero proves monotonicity in the terminal time. An upward-closed set with positive infimum need not contain that infimum. The two elementary endpoint countermodels correctly establish only this logical distinction.
- The forward-time adjoint has drift +M. The observed quantity is ε times the derivative at the controlled endpoint. The integration-by-parts identity has the stated sign; the sign does not affect Cauchy–Schwarz. The numerator is the adjoint state at final time, not its initial state.
- The gauge eigenfunction is exp(-M x/(2ε)) sin(kx), and its decay rate is M²/(4ε)+εk². The single-mode integral and cancellation are exact. At normalized negative speed the largest individual-mode lower bound tends to infinity below time 2, to 1 at time 2, and to zero above time 2. At positive speed it tends to zero at every fixed positive time. Maximization over all single modes still selects n=1, even for an ε-dependent mode choice. This is never an upper bound on the full control cost.
- The ℓ² projection example correctly separates pointwise convergence from operator-norm convergence.

Additional scope controls: forward gauging removes transport but introduces M²/(4ε); its spatial multiplier is not uniformly bounded with bounded inverse as ε tends to zero. Reflection reverses drift while moving the controlled endpoint, so it does not identify the two original fixed-endpoint costs. Neither shortcut can settle the threshold.

## Main-preprint proof-chain review

The complete mathematical argument in Sections 2–7 was read. The following describes independent checks, not a claim that merely reading theorem statements verifies their proofs. Standard Hardy-space, Fourier, transposition, and semigroup foundations were used at their ordinary mathematical level rather than reconstructed from axioms.

### Positive lower bound

The finite Blaschke factors have unimodular boundary values. For N=floor(ε^(-2)), the reciprocal spectral sum tends to 1 by upper and lower integral comparison, while the cubic reciprocal sum tends to zero. Thus their boundary phases converge to the delay of length 2. Multiplication operators and their adjoints converge strongly by dominated convergence, giving convergence of the model-space projections. This step correctly concerns each fixed test function, not operator-norm convergence.

Choose a smooth nonnegative temporal function supported strictly between T and 2. Its projection supplies finite exponential boundary fluxes with vanishing observation before T. The elliptic resolvent test is essential: it provides a bound of the discounted future flux by the interior L² norm with constant 1 independent of ε. The maximum principle, zero boundary values on the resolvent state, and left boundary value 1 on the test function give the correct boundary sign and uniform constant. The limiting future integral is positive. This prevents the interior state from disappearing and yields divergence of the true observability constant. Large or badly conditioned modal coefficients cause no admissibility issue, since each ε uses a finite smooth sum and the observability ratio is homogeneous.

### Negative lower bound

The inverse Cauchy Gram matrix has alternating signs, including the boundary-flux weights. The chosen first inverse column has boundary energy equal to its first entry. On the terminal interval of width ε², all retained sine terms have the same sign because n≤floor(ε^(-2)); dropping every term except the first is consequently a valid lower bound there.

The spatial integral contributes order ε⁶ times exp(1/ε), and temporal decay contributes exp(-T/(2ε)) at the squared-norm level. The infinite-product computation and bounded truncation factor give the reciprocal-square product contribution exp(√2/ε), with the stated polynomial factor. Combining these yields the squared lower ratio ε⁹ exp((2+2√2-T)/(2ε)). The powers, signs and resulting strict threshold agree. Finite exact rational Gram inversions provide independent regression checks of the formula; they are not a proof for all sizes.

### Finite-to-infinite-time reduction

The crucial derivative estimate has constant 1, not an unspecified multiplicative constant. It was independently checked against Theorem 5.2 and its proof in the published [Baranov–Jaming–Kellay–Speckbacher paper](https://afm.journal.fi/article/download/143957/91131/329482), printed p. 177. Its assumptions apply to the finite Blaschke products. Rotating the half-plane preserves the derivative and boundary norms. The derivative bound is at most 2, so the temporal second moment is at most four times the energy. Splitting at T gives the valid factor T²/(T²-4) exactly when T>2. No bound at T=2 is supplied by this argument.

### Boundary-to-interior map and infinite-dimensional limit

The kernel interpolation, conjugation signs and Hilbert–Schmidt identity were checked against the independent matrix expression tr(G^(-1)B). The sine reflection accounts for the alternating derivative of the Blaschke product. The finite-dimensional maps are consistent restrictions of one another. Their Hilbert–Schmidt norms increase under subspace inclusion; this is not an assertion that the oscillatory integrand is pointwise monotone. For fixed positive ε and T, Gaussian decay supplies a summable bound uniform in truncation size. Dominated convergence justifies the infinite series formula. Constants allowed to depend on ε at this passage do not enter as purported uniform final bounds.

### Positive upper bound

The Fourier convention yields the stated Poisson factor 1/π. The scaled hyperbolic-sine quotient is entire; its apparent square-root singularities are removable. Gaussian decay on fixed horizontal strips justifies contour shifting and differentiation. With 0<a<1/2 and q=√(1/2-a²), the estimates |s/√(s²+1/2)|≤1 and Re√((r-ia)²+1/2)≤q+2r² hold. The remaining Gaussian is integrable for t>2. The periodic image sum is controlled uniformly for ε≤1.

The inequality q<1-a follows by squaring: (1-a)²-q²=2(a-1/2)². After spatial and temporal integration the squared-cost exponent is 2-4a-(1/2-2a²)T. Setting a=1/T produces -(T-2)²/(2T), with a prefactor of order ε before taking the square root. The positive exponent, √ε factor, and strict T>2 scope agree. The singular constants and strict integrability assumptions prevent passage to the critical endpoint by substitution.

### Negative upper bound and endpoint

The elementary square-root bound on the hyperbolic-sine series leaves a Gaussian with time t-1/√2. Squaring and integrating gives a bound proportional to ε exp(-(T-2-2√2)/(2ε)). Combining with the finite-to-infinite-time factor is valid at T=2+2√2, since that time is strictly above 2. Taking the square root yields a √ε bound at equality, so the included negative endpoint is supported by the proof, not merely by an imprecise theorem summary.

The extension from finite sums to H²∩H¹₀ initial adjoint states is performed at fixed ε. Gauge-transformed sine partial sums converge in H², and the derivative boundary trace is continuous in that topology. No uniform-in-ε density approximation is required at this step because the established bound is independent of truncation.

## Evidence boundary

No fatal defect was found in the reviewed threshold argument. The source attribution is verified; the elementary retained mathematics is independently validated; the nontrivial main proof chain was substantively reviewed as above. That is stronger than an abstract-only source match, but remains an AI review relying on standard analytic foundations and one independently checked non-elementary external inequality. No proof assistant was used. Historical literature exhaustiveness, all cited foundational proofs, journal acceptance, and positive endpoint boundedness are not certified.

## Executable and integrity results

The author's normal and optimized executions reproduce CHECK_RESULTS.json byte for byte. The independent checker also has identical normal and optimized output. Exact checks cover gauge coefficients, Cauchy inverses with signs and normalization, scaling, single-mode prefactors, and exponent optimization. Numerical quadrature and contour samples are explicitly labelled consistency tests. Deliberate wrong-gauge, wrong-Gram-sign, and missing-flux-factor mutations are rejected.

The author's archive and manifest match the externally supplied hashes. All eight archive files match the frozen directory; the seven manifest payload entries form a closed regular-file set. No source PDFs, extracts, raw corpus records, or private coordination files occur in the safe payload. A stricter independent integrity checker rejects symlinks, duplicate manifest paths, and nested unlisted manifest files. The original checker has weaker hardening in those respects, but this did not invalidate the actual clean frozen payload.

To reproduce from the common parent directory:

    python advection_control_30003759_independent_audit/independent_verify.py
    python -O advection_control_30003759_independent_audit/independent_verify.py
    python advection_control_30003759_independent_audit/verify_integrity.py

No remote state was changed by this audit.
