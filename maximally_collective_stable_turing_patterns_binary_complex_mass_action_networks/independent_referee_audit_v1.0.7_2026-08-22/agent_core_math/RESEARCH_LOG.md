# Independent core-mathematics audit log

## 2026-08-22T22:00:02-07:00 — audit opened (2%)

- Scope: independent reconstruction of the algebraic claims in packet v1.0.7, without treating stored `PASS` markers, certificates, helper routines, or review maps as proof.
- Working directory is isolated at `agent_core_math/`; packet and source snapshots will remain read-only.
- Immediate work plan: read the manuscript and supplement, reconstruct the reaction/Jacobian data from definitions, derive the principal-minor diffusion theorem and topology-specific minors independently, then test exceptional/boundary cases and contrast claims.
- Evidence classes will be kept distinct: deductive proof, exact symbolic computation, finite exhaustive computation, and floating-point falsification searches.

## 2026-08-22T22:11:31-07:00 — independent reconstruction checkpoint (55%)

- Read `repository/manuscript/main.tex` and `repository/manuscript/supplement.tex` completely (not merely the supplied review maps).
- Rebuilt source and stoichiometric matrices directly from the indexed reaction list, with no project imports. Exact checks for `m=3,4,5,6` reproduce rank `m`, the two-dimensional flux kernel, semipositive conservation, the full Jacobian, the negative full `X`-block signed determinant, and every order-`m` omission minor.
- Independently enumerated every induced set of size below `m` and its SCCs for `m=3,...,9`, both for generic parameters and exactly at `b=2a`; no SCC outside the manuscript classification occurred. This is finite corroboration; the all-dimensional proof is the graph-path argument.
- Direct exact expansion of the boundary triad reproduces its three characteristic coefficients and a 14-term coefficientwise-positive Routh gap. Its three two-vertex principal determinants are positive.
- Direct exact determinants reproduce the unit/scaled homogeneous and spatial chain factorizations for `m=3,4,5,6`.
- Independently regenerated the four modulus polynomials from their definitions: term counts `35,77,84,22` agree, coefficient signs agree, and separate axis restrictions establish the asserted equality cases (including the degenerate first-order `z` coefficient at the `5/4` certificate boundary).
- A seeded floating-point falsification search sampled 39,380 smaller principal blocks under log-wide positive scalings and included exact `b=2a` samples; no non-Hurwitz block was found. This is numerical evidence only.
- No mathematical defect has emerged. Remaining work: formalize the dependency map and proof assessment, document boundary/counterdomain checks, and prepare the referee findings with calibrated classifications and line references.

## 2026-08-22T22:29:37-07:00 — core audit complete (100%)

- Final independent script replay exited 0 and produced valid JSON in `independent_core_checks_output.json`.
- Added exact outside-domain controls: removal of the positive order-`(n-1)` sum (which breaks the post-threshold band), equality in the topology-specific diffusion criterion, the `T(H)=1` double-zero boundary, a homogeneously unstable `T(H)<1` realization, and the structurally invalid naïve `m=2` continuation.
- Checked the current `m=149` lower and upper endpoints and recovered the unstable pair at the superseded `L=1/21` endpoint as a falsification control.
- Inspected the load-bearing core verifiers semantically. Several are finite regressions against hard-coded expected formulas, and multiple `dd_` pairs use the same implementation; these limitations do not replace the manuscript's all-dimensional proofs.
- Produced `CORE_MATH_FINDINGS.md` with theorem-by-theorem classifications, an independently reconstructed dependency map, exact manuscript/code line references, commands/results, scope limitations, and defect/repair classifications.
- Bottom line: the assigned algebraic and linear core is independently verified; no mathematical correction or headline change is required. Whole-manuscript nonlinear and functional-analytic conclusions remain for the other audit streams.
