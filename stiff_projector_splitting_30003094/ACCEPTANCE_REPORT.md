# Acceptance report: direct stiff projector splitting

Date: **20 October 2026**. Problem ID: **30003094**. Source:
**OWR-14226-001**. Queue row: **1829**. Recorded outcome:
**UNSOLVED, 5/5 substantive mathematical avenues completed**.

## Verdict

Accept the scoped partial results below. The independent mathematical audit
verdict is **PASS_WITH_EXPLICIT_SCOPE_LIMITS**, recorded in
`AUDIT_ACCEPTANCE.json`. The original broad request to extend the error
analysis to spatially discretized PDEs remains unresolved. The short source
does not specify a PDE class, regularity class, spatial method, boundary
conditions, or a complete universal estimate; a counterexample to one
overbroad estimate cannot resolve that unspecified question in full.

The acceptance basis is the complete analytic proofs in
`RESEARCH_REPORT.md`, `SUBCLASS_BOUNDS.md`, and `STRANG_OBSTRUCTION.md`, with
independent derivations in `AUDIT_COUNTEREXAMPLE.md`. The four manuscript
hashes, including the consistent five-avenue summary, are pinned in the
audit JSON. The package preserves those manuscripts and audit byte-for-byte.
No external review, novelty, or literature-priority claim is made.

## Method and norm

The direct fixed-rank method applies the tangent-projector K–S–L splitting
to the **entire** matrix vector field, including stiffness. Its K, negative
S, and L subflows are solved exactly in the mathematical results. The
standard symmetric variant is KSL(τ/2) followed by its adjoint LSK(τ/2),
equivalently K–S–L–S–K after merging the consecutive L subflows. This is
neither a modified physical stiff/nonstiff split nor an approximate stable
replacement of the backward S equation.

Finite-dimensional statements use the Frobenius norm and orthonormal
factors. The PDE embeddings use orthonormal Fourier-Galerkin coefficients,
so the Frobenius norm is exactly the function L² norm. An unweighted sampled
grid norm is not substituted for L². Required QR ranks and intermediate
rank conditions are addressed in the proofs; no assertion of numerical
finite-precision robustness of a large backward S evolution is made.

## Accepted mathematical findings

1. **Exact identities and cancellation.** For F(Y)=YB+C, the direct KSL
   endpoint is P₁Φτ(Y), where P₁ projects onto the K-endpoint column space
   and Φ is the full affine flow. The homogeneous equation Y′=AY+YB is
   integrated exactly. An affine equation is also exact when a fixed
   A-invariant column space contains the forcing columns and the specified
   ranks persist. These identities explain why isolated backward-S
   instability alone is not an error counterexample.

2. **Right-stiff obstruction.** For B=diag(0,−λ), C=ηe₂e₁ᵀ and
   Y₀=e₁(1,1)/√2, direct KSL has error tending to 1/√2 along λ=n² and
   τ=η=1/n. Semigroup contractivity and analyticity, the forcing bound and
   the normal remainder are uniform; initial error is zero. The data are
   spatially rough as the active frequency grows. The result rules out the
   precisely stated norm-only stiffness-uniform estimates, not every
   PDE-compatible estimate.

3. **Smooth target with rough initialization, including Strang.** A fixed
   smooth rank-one exact target, with a norm-small but graph-norm-unbounded
   rank-one numerical perturbation, gives limiting error one for both
   direct KSL and standard Strang while δ+ε+τ tends to zero. The exact
   projected rank-one trajectory exists and its modeling error is small.
   The adjoint LSK bound ‖Ψ*h(Y)−Φh(Y)‖≤2h‖C‖ proves that the second
   Strang half cannot repair the slow component lost by the first half.
   The initialization is **not** the exact Fourier projection of the fixed
   smooth datum. Spatial regularity of the target alone does not control
   these rough numerical initializers.

4. **Two-sided comparison.** For A=B=diag(0,−λ), C=ηI₂ and Y₀=vvᵀ,
   v=(1,1)/√2, direct KSL tends to [[3/8,0],[1/8,0]], with error tending
   to 1/(4√2) along λ=n², τ=η=1/n. The final retained singular value
   tends to √10/8, so a vanishing endpoint singular value is unnecessary.
   The stated 2019 stiff semilinear hypotheses hold uniformly for this
   active block, but that theorem concerns a **different** algorithm that
   splits only G and then applies the full stiff semigroup. Its output has
   no corresponding order-one discrepancy. In the larger Galerkin space,
   √2η is the safe global normal-defect bound; the sharper η bound applies
   on the active block and its trajectory.

5. **Conditional positive subclass theorem.** For F(Y)=AY+C with constant
   dissipative A and constant C, let Pᵢ be the new numerical column
   projector and Qᵢ the old numerical row-complement projector. Suppose
   every step has full required ranks and
   εᵢ=‖(I−Pᵢ)CQᵢ‖≤ε,
   γᵢ=‖(I−Pᵢ)AUᵢ₊₁‖₂≤Γ,
   and Mᵢ=‖CQᵢ‖≤M. The local error is at most
   hᵢεᵢ+hᵢ²γᵢMᵢ/2. Exact-flow contractivity gives the global bound
   δ+Tε+ThmaxΓM/2, with M≤‖C‖. The assumptions concern the **actual
   numerical stages**, not just the exact target. No explicit inverse
   retained singular value or ‖A‖ occurs, but Γ can fail to be mesh-uniform.

The fifth result yields a periodic Fourier-Galerkin corollary for
∂tz=∂²xz+f(x,y), with time-independent f and fixed rank. For data in Hᵖ,
the continuous-to-semidiscrete spatial tail is bounded by
(1+(N+1)²)^(−p/2)(‖z₀‖Hᵖ+T‖f‖Hᵖ). Adding the conditional temporal/rank
bound gives the stated L² estimate. This is one-sided affine diffusion,
not a general two-sided nonlinear parabolic result. Uniform stage regularity
is assumed, not derived from exact-solution smoothness.

## Numerical corroboration and replay

All four shipped scripts were rerun in a fresh temporary directory against
the recorded result objects. The package declares NumPy 2.3.5, SciPy 1.17.0,
mpmath 1.3.0 and the observed Python 3.12.14 runtime. `run_checks.py` records
the actual versions, requires zero exit status and empty stderr, checks
strict result structure and explicit numerical tolerances, and reports
whether exact JSON equality also held. It writes no package files.

- `check_affine_counterexample.py`: nine high-precision evaluations of
  the two-sided example, comparing literal subflow formulas with a
  cancellation-aware rearrangement.
- `check_subclass_identities.py`: 24 seeded rank-two NumPy/SciPy tests of
  homogeneous exactness, both affine endpoint identities, and the local
  conditional bound, including initial retained singular values down to
  10⁻⁸.
- `audit_exact_subflows.py`: nine arbitrary-precision literal augmented-
  matrix evaluations across the two-sided, one-sided and rough-initializer
  families, independently implementing each affine subflow.
- `check_strang_obstruction.py`: four six-subflow Strang cases using that
  literal implementation, checking the adjoint identity, bound, positive
  S endpoints and nonzero QR endpoints. Entire-interval rank preservation
  rests on the analytic argument, not endpoint tests alone.

These 46 finite evaluations are **numerical corroboration**, not exact
proof certificates. Even arbitrary-precision matrix exponentials are
numerical approximations. Floating-point cancellation is controlled by
increasing precision in the examples, not proved absent by an interval
certificate. `REPRODUCIBILITY.md` documents every tolerance and precision
schedule; `REPLAY_VERIFICATION.json` records the observed results.

## Provenance and publication boundary

The source gate found no verified general resolution in the sources
inspected as of the research date. This bounded search is not proof that no
other result exists. It distinguishes the original full-field method from
later modified/stabilized methods, stability-only analyses and a separately
reported second-order preprint whose proof was not audited here.

Included source material is authored discussion with public citations and
public verification metadata: scholarly titles/URLs, PDF hashes and byte
counts, retrieval/inspection history, and corpus hashes/byte counts/match
results. The underlying corpus was recovered locally and freshly hashed,
not fetched afresh upstream. Raw source PDFs, extracted text, source images,
datasets, private sources, personal data, coordination material and caches
are excluded. Research-stage no-publication/no-queue-change statements in
preserved reports are historical; package preparation itself makes no
GitHub or queue change.

## Explicitly not established

- A full resolution of the original broad PDE problem.
- Failure for fixed smooth PDE data with exact projected initialization.
- An unconditional nonlinear or fully two-sided PDE convergence theorem.
- Robust second-order Strang convergence, arbitrary discretizations/norms,
  general hyperbolic PDEs, tensor formats, adaptive rank, or inexact subflows.
- External peer review, novelty, exhaustive literature coverage, or
  validated finite-precision implementation robustness.
