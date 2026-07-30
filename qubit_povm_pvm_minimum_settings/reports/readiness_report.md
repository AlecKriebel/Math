# Final readiness report

**Assessment date:** 2026-07-29  
**Scope:** public preprint, reproducibility release, arXiv source, and journal
submission package

## Outcome

The referee revision is internally complete enough for a public, versioned
preprint release and expert review. It is **not represented as independently
expert-verified**. No requested proof bridge remains only an assertion or a
verifier instance. The recommended overall label is:

> **READY FOR PUBLIC PREPRINT AND EXPERT SCRUTINY**

The central impact is easy to state: in the standard shared-randomness
convexified fixed-qubit Bell model, two inputs per party never make a genuine
POVM behaviorally indispensable, whereas an exact \(3\times2\) witness proves
that one additional input can.

## Confidence by dependency

| Dependency | Status | Basis and remaining concern |
|---|---|---|
| Exact \(3\times2\) separation | **READY, NEEDS EXPERT SCRUTINY** | Exact rational Bell coefficients, exact algebraic strategies, a global analytic PVM upper bound, all six PVM supports, and a passing symbolic verifier are present. The displayed lower and upper bounds are not claimed to be exact optima. |
| One-binary-party theorem | **READY, NEEDS EXPERT SCRUTINY** | The formal cone-circuit lemma, transposed canonical projectors, rank-one-total construction, all degeneracies, and one common shared variable for the complete behavior are explicit. |
| Residual-architecture reduction | **READY, NEEDS EXPERT SCRUTINY** | The compact-hull extreme-point lemma, pure-state and extremal-POVM selections, deterministic postprocessing, two-dimensional operator-system argument, and exact-three-rank-one conclusion are included. |
| Lorentz-incidence equality proof | **READY, NEEDS EXPERT SCRUTINY** | Lorentz factors, physical reconstruction, per-input multiplier pullback, Fredholm compatibility, second variation, exceptional fibers, and all four rank-zero blocks are written out. Exact programs regression-check the finite algebra; the quantified conclusions are manuscript proofs. |
| Combined universal equality theorem | **READY, NEEDS EXPERT SCRUTINY** | The dependency chain is complete, the C--K revision audit found no unresolved load-bearing step, and the theorem-to-artifact map identifies every executable boundary. No independent expert referee has yet certified the combined theorem. |
| Priority claim | **READY, NEEDS EXPERT SCRUTINY** for qualified wording; **NOT READY** for an absolute “first” claim | The current primary-source audit found the \(3\times2\) phenomenon to be prior art and found no earlier arbitrary-output \(2\times2\) closure or minimum-input classification. Use only “to our knowledge,” and repeat the search immediately before submission. |
| Computational reproducibility | **READY** | Python 3.14.6 and SymPy 1.14.0 are pinned. The offline runner verifies eight immutable source artifacts and passes the exact separation, 39 closure checks, and rank-zero construction. The executable boundary is disclosed. |

## Quality gates

- **Mathematical:** PASS after adversarial audit and incorporation of all
  publication-facing repairs.
- **Computational:** PASS with exact arithmetic, pinned SymPy, source hashes,
  and a one-command runner.
- **Literature:** PASS for conservative positioning; an immediate
  pre-submission refresh remains required.
- **Presentation:** PASS. The 34-page publication PDF and 34-page
  line-numbered review PDF compile without warnings. Every publication page
  was rendered and inspected, and the three figures were checked in context.
- **Scope discipline:** PASS. The paper consistently states convexified
  behavior-set equality, permits zero projectors/postprocessing, forbids
  dimension-increasing dilation, and disclaims same-state simulation and exact
  global optima.
- **CI:** CONFIGURED. The repository workflow runs `run_all.sh`, builds both
  PDFs with Tectonic 0.16.9, and uploads them; its first hosted run follows the
  release push.
- **External expert review:** NOT YET PERFORMED.
- **Journal/arXiv upload:** NOT PERFORMED; those account actions remain for the
  human author.
- **Archival DOI:** NOT YET ASSIGNED. The versioned public repository release
  supplies a timestamp but is not described as peer review or conclusive
  priority.

## Recommended next actions

1. Preserve the release commit and immutable tag URL.
2. The author may submit the identical source archive to arXiv; category
   endorsement may be required.
3. Independent expert scrutiny remains desirable, especially for D2, D3,
   incidence reconstruction, multiplier positivity, and exceptional fibers.
   Any external communication is solely for the author.
4. Refresh the literature and editorial-board checks immediately before
   journal submission.
5. Submit first to the venue selected from
   `submission/journal_options.md`; do not submit simultaneously elsewhere.
