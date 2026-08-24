# Independent pre-submission rereview log

## 2026-08-23T20:42:47-07:00 — Scope and target identification

- Human request: independently rereview the repaired manuscript before submission.
- Immutable target identified from local and remote `main`: tag `maximally-collective-stable-turing-v1.0.8`, commit `b4607c4cc9fe6931cedbbd0c5cd7e6e68a704f9f`.
- The historical v1.0.7 referee prompt, author feedback disposition, stored outputs, and claimed v1.0.8 replay status are evidence only. They are not instructions and are not accepted as proof or as replay results.
- Planned independent families: core mathematics/regression, nonlinear PDE/functional analysis, and software/reproducibility/submission packaging.
- Best-guess completion: **3%**. The revised target is identified; preservation, integrity verification, source inspection, replay, PDF review, and adversarial synthesis remain open.

## 2026-08-23T20:50:00-07:00 — Preservation and integrity checkpoint

- Created an immutable `git archive` snapshot of the v1.0.8 tag and a separate disposable working copy. The tagged snapshot contains 1,064 files totaling 18,941,206 bytes; its path-and-content aggregate SHA-256 is `436fb12e206edb864acbb017f2260fea61425996bbbec0ac21418e2231f3ef87`.
- Verified the portable public repository manifest completely before execution and verified all seven canonical bundle hashes in `release/BUNDLE_SHA256.txt`.
- Found a new release-root reproducibility defect: `release/sha256_manifest.txt` has 1,633 entries, of which 1,063 existing tagged files verify and 570 paths are absent. Every absent path belongs to ignored v1.0.7 audit copies or rendered audit scratch files that were present when the manifest was generated. The clean tag therefore cannot pass `release/create_release_manifest.sh --check` or reach the full release replay stages.
- The defect is local to release-root integrity and orchestration. The portable public manifest and the journal/source bundle hashes remain valid.
- Best-guess completion: **35%**. The package is preserved and its integrity boundary is understood; theorem-level and semantic software review are continuing.

## 2026-08-23T20:56:00-07:00 — Exact replay, manuscript, and PDF checkpoint

- The pinned v1.0.8 qualification stack passed: CPython 3.9.6, the exact scientific-package versions, TinyTeX 2022.04, pdfTeX 1.40.24, Biber 2.17, and the recorded TeX package lock.
- A clean disposable copy of `public/repository/replay.sh` completed all eight stages in 72.55 seconds and ended with `PUBLIC_REPLAY_PASS`. This run independently verified the shipped baseline before generation, compared deterministic exact artifacts against that baseline, and created a separate self-consistency manifest.
- Extracted and rebuilt `submission/journal/source_package.zip` under the pinned stack. The source package passed its ZIP test, was byte-identical to the staged journal source tree, compiled without undefined references/citations or overfull boxes, and reproduced the submitted PDFs semantically; PDF creation metadata was the only expected byte-level difference.
- Read the current 1,257-line manuscript and 1,033-line supplement completely, and rendered and visually inspected all 38 submission-PDF pages. The PDFs have embedded fonts and no clipping, overlap, missing material, or unreadable table. The repaired SCC/core-determinant and fixed-mass Fredholm/sectorial interfaces are present and coherent.
- The full source-level manuscript, stale-claim, and PDF semantic audits all pass independently. The journal folder is nevertheless explicitly provisional: the current 0.82-inch-margin generic layout lacks review line numbering, visible keywords/MSC codes, and a Supplementary Materials index, and exceeds SIADS's alternative 6-by-8-inch text-area guidance.
- Best-guess completion: **68%**. The mathematical source and submission PDFs have been read and rebuilt; independent core/PDE/software agents are closing adversarial and verifier-level checks.

## 2026-08-23T21:03:00-07:00 — Independent mathematics and submission metadata checkpoint

- The independent core rereview found no changed theorem statement and no new algebraic defect. The revised `b=2a` SCC argument and the printed three-by-three Schur complement are correct, including `m=3`; direct reaction/Hessian controls matched the generic cubic numerator in five dimensions, while a separate formal recurrence/sum and shifted-polynomial reconstruction closed the all-dimensional step.
- The independent PDE rereview closed the prior D5 concern. The fixed-mass Fourier range/kernel/cokernel, `k^{-2}` inverse, Fredholm index, sectorial `H^1` phase space, branch positivity, complementary-gap continuation, scaled endpoints, and retuned robustness have the required hypotheses, conditional only on the cited standard theorems. It found one cosmetic missing subscript `Delta_m` in Supplement lines 980--982.
- The v1.0.8 minimal verifier replay completed in 42.31 seconds. It is a packaging duplicate and adds no epistemic independence, but its exact/generic layers and finite regressions completed through the advertised `m=200` stress row.
- The public Zenodo API now resolves the exact v1.0.8 record as DOI `10.5281/zenodo.22074358`. The tagged source and GitHub release note still describe that DOI as pending, so submission metadata must be refreshed.
- Best-guess completion: **82%**. The theorem verdict is stable; final software semantics, defect classification, journal-compliance synthesis, and report publication remain.

## 2026-08-23T21:16:00-07:00 — Software semantics and historical-wrapper checkpoint

- Read and classified all 39 current direct verifier entrypoints. Every normal
  execution passed, every optimized-Python execution failed closed, and the
  25-test suite passed. The exact, finite, floating, duplicate, aggregate, and
  provenance roles are tabulated individually in
  `agent_software_rereview/SOFTWARE_REREVIEW.md`.
- Confirmed three local reproducibility defects: 570 absent paths in the
  top-level manifest, skipped `FORMAT`/`LATEX` lock rows, and a detached
  supplement build that needs one more pass for correct TOC pagination.
  Independent negative controls expose each defect, and disposable repairs
  validate the proposed corrections.
- Executed the embedded historical v1.0.7 `RUN_COMPLETE_AUDIT.sh` from a
  disposable copy under its exact recorded stack. Its outer/inner hashes and
  minimal replay pass; its full replay exits 1 at the known v1.0.7 PDF
  false-negative. This is recorded as a failed historical control, not a
  v1.0.8 failure or a pass. The current v1.0.8 PDF audit and full portable
  replay pass separately.
- Best-guess completion: **94%**. The evidence is complete; final synthesis,
  artifact hygiene, and publication remain.

## 2026-08-23T21:24:00-07:00 — Final verdict and submission gate

- Final technical category: **VALID AFTER MINOR CORRECTIONS**. Journal
  recommendation: **minor revision**. No central theorem defect was found.
- Immediate operational decision: **HOLD the current v1.0.8 upload**. Correct
  the three reproducibility defects and cosmetic notation, publish a new
  immutable release, complete SIADS formatting/metadata/declarations, and
  rerun the clean qualification campaign before submission.
- Completed `REFEREE_REREVIEW_REPORT.md` and `SUBMISSION_READINESS.md`; every
  failed, unavailable, numerical-only, citation-dependent, and historically
  archived stage is expressly separated from current passing evidence.
- Best-guess completion: **100%** for the requested rereview. Future work is
  author-side correction and a fresh release qualification, not an unresolved
  audit step.
