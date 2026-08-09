# Discovery worklog

This log records exact structural reductions, exploratory computations, and failed universal lemmas. Floating-point experiments are explicitly marked exploratory and are never used as final evidence.

## 2026-08-04: initialization

- Began parallel universal-proof and counterexample search.
- No literature was searched during discovery.
- Initial focus: molecularity/support closure, finite-step restoring paths, exact shell/generator identities, and small weakly reversible cycle enumeration.

## Exact failed lemmas recorded

1. Uncorrected one-step entropy drift fails on `0 -> A+B -> B -> 0` at `(n,0)`.
2. One-step total-count drift fails on the same boundary ray.
3. The most obvious coercive quadratic correction cannot repair that ray.
4. A universal finite-degree factorial-polynomial stationary ansatz already fails in the `0 <-> A` calibration unless exponential factors are allowed.

## Structural identity retained

Every enabled state transition lifts a directed complex-graph cycle.  If
`y->y'` fires from `x=r+y` and `y'=y_1->...->y_m=y` is a directed return path,
then the same reaction word is enabled successively from `r+y_j` and returns
exactly to `x`.  This is checked by `src/class_analyzer.py::lifted_cycle`.

## 2026-08-09: publication-readiness repair

- Reconstructed the load-bearing proof and found no theorem-breaking defect.
- Identified formal interfaces to clarify: positive CTMC return, the stopped
  episode chain, finite-index integrability, trace-excursion conditioning, and
  the population-level lower rate bound.
- Found release-integrity defects in the standalone report, package manifests,
  and discovery-provenance wording; these affect reproducibility claims but do
  not enter the universal proof.
- Began a clean-main repair covering the manuscript, verification package,
  literature positioning, declarations, archive instructions, and release
  checks. The public project webpage is intentionally outside this repair.
- Completed the integrated Version 0.3 repair: proof-interface clarifications,
  journal-facing exposition and declarations, deterministic current and
  archived verifiers, citation/licensing metadata, portable manifests, and
  clean-environment release checks.
- Reproduced the current verifier under CPython 3.11.8 and 3.14.6 with 38 tests
  and identical canonical output; reran all Phase II--V entry points in the
  exact archived environment and confirmed deterministic certificates.
- Rebuilt both 14-page manuscript wrappers twice with Tectonic 0.16.9,
  confirmed byte-identical repeats, scanned extracted text, and visually
  inspected every rendered page. Citation metadata passed the CFF 1.2 schema.
- Completed the requested fresh, read-only adversarial release audit.  An
  independent proof reconstruction found no remaining mathematical finding at
  any priority.  The release audit independently repeated the current verifier
  under CPython 3.11.8 and 3.14.6, every archived Phase II--V entry point in the
  exact tested environment, deterministic certificate generation, two builds
  of each manuscript wrapper, font/metadata/text checks, and a full rendered
  page review; all passed.
- Resolved the release audit's publication findings before the final rerun:
  corrected the hybrid Wiuf--Xu bibliography record, recorded the public 2022
  two-species priority announcement, included the MIT notice and PEP 639
  metadata in built wheels, corrected deterministic PDF dates, and identified
  the AI-assisted proof schematic in its caption.  The final audit also aligned
  the expert note's nonexplosion summary with the population-state construction
  used in the proof.
- Best-guess completion toward a submission-ready paper package: 100%.  This
  records that no actionable defect remains after the stated checks; it is not
  a substitute for journal peer review.
