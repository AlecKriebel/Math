# Final readiness report

**Assessment date:** 2026-07-29  
**Scope:** public preprint, reproducibility release, arXiv source, and journal
submission package

## Outcome

The internal publication package is complete enough for a public, versioned
preprint release. It is **not represented as independently expert-verified**.
The recommended overall label is:

> **READY, NEEDS EXPERT SCRUTINY**

The central impact is easy to state: in the standard shared-randomness
convexified fixed-qubit Bell model, two inputs per party never make a genuine
POVM behaviorally indispensable, whereas an exact \(3\times2\) witness proves
that one additional input can.

## Confidence by dependency

| Dependency | Status | Basis and remaining concern |
|---|---|---|
| Exact \(3\times2\) separation | **READY, NEEDS EXPERT SCRUTINY** | Exact rational Bell coefficients, exact algebraic strategies, a global analytic PVM upper bound, and a passing symbolic verifier are present. The displayed lower and upper bounds are not claimed to be exact optima. |
| One-binary-party theorem | **READY, NEEDS EXPERT SCRUTINY** | The manuscript proves one common convex decomposition of the complete behavior and treats degenerate cone images, repeated rays, zero effects, and rank-deficient totals. This theorem-sized argument deserves an independent specialist reading. |
| Residual-architecture reduction | **READY, NEEDS EXPERT SCRUTINY** | The full extreme-behavior/common-span proof is included, with zero effects deleted and reinserted, deterministic postprocessing handled, and four-outcome extrema excluded. This is the highest-priority referee checkpoint. |
| Lorentz-incidence closure | **READY, NEEDS EXPERT SCRUTINY** | Physical reconstruction, positive multipliers, second variation, exceptional fibers, and rank-zero simulation are all written out. Exact programs regression-check the main algebra, but the quantified geometric proof remains human mathematics. |
| Combined universal equality theorem | **READY, NEEDS EXPERT SCRUTINY** | The dependency chain is complete and the proof audit found no unresolved load-bearing step. No independent expert human has yet certified the combined theorem. |
| Priority claim | **READY, NEEDS EXPERT SCRUTINY** for qualified wording; **NOT READY** for an absolute “first” claim | The current primary-source audit found the \(3\times2\) phenomenon to be prior art and found no earlier arbitrary-output \(2\times2\) closure or minimum-input classification. Use only “to our knowledge,” and repeat the search immediately before submission. |
| Computational reproducibility | **READY** | The pinned, offline runner verifies eight immutable source artifacts and passes the exact separation, 39 closure checks, and rank-zero construction from a clean directory. The executable boundary is disclosed. |

## Quality gates

- **Mathematical:** PASS after adversarial audit and incorporation of all
  publication-facing repairs.
- **Computational:** PASS with exact arithmetic, pinned SymPy, source hashes,
  and a one-command runner.
- **Literature:** PASS for conservative positioning; an immediate
  pre-submission refresh remains required.
- **Presentation:** PASS. The 24-page PDF compiles without warnings, every
  page was rendered and inspected, and all three figures were checked in
  grayscale.
- **Scope discipline:** PASS. The paper consistently states convexified
  behavior-set equality, permits zero projectors/postprocessing, forbids
  dimension-increasing dilation, and disclaims same-state simulation and exact
  global optima.
- **External expert review:** NOT YET PERFORMED.
- **Journal/arXiv upload:** NOT PERFORMED; those account actions remain for the
  human author.
- **Archival DOI:** NOT YET ASSIGNED. The versioned public repository release
  supplies a timestamp but is not described as peer review or conclusive
  priority.

## Recommended next actions

1. Release the repository version and preserve its commit/tag URL.
2. Submit the same source archive to arXiv; obtain category endorsement if the
   account requires it.
3. Ask an independent expert reader to focus on D2, D3, the incidence
   reconstruction, and multiplier positivity.
4. Refresh the literature and editorial-board checks immediately before
   journal submission.
5. Submit first to the venue selected from
   `submission/journal_options.md`; do not submit simultaneously elsewhere.
