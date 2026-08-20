# Replay status for the 19 August 2026 pre-submission exposition repair

This file distinguishes current-release verification from historical-lineage
verification. It supersedes the pre-repair replay logs, which were removed
because they described different sources and artifacts.

## Current repaired release: passed checks

The following were rerun after the high-dimensional endpoint repair and final
source edits:

- 18 mutation/regression tests;
- the complete symbolic aggregate, including the determinant-identity bridge,
  the 22-term homogeneous certificate, the 84-term spatial certificate, the
  exceptional `m=3` cubic, and the exact legacy-endpoint counterexample;
- current-profile and detached numerical provenance;
- finite integrated designs at `m=3,4,5,6,8,10`, with the repaired Pareto
  family also checked at `m=149`;
- full current-profile cosine-Galerkin simulations and the strengthened
  refinement audit (maximum recorded relative discrepancy
  `1.6246526173879546e-08`, below the `2e-8` gate);
- all eight principal PDFs: 17-page manuscript, 17-page supplement, 2-page
  theorem summary, 6-page proof skeleton, and four one-page figures;
- all seven ZIP integrity checks and all three detached submission-source
  builds; and
- a full portable replay in a detached copy of `public/repository`, including
  a replay-generated self-verifying manifest. The shipped pre-replay public
  tree has its own complete manifest; the replay regenerates numerical outputs
  and verification records for the downloader's local toolchain while
  retaining the canonical public file set.

The detached portable replay used Python 3.9.6, Matplotlib 3.7.1, NumPy 1.24.3,
Pandas 2.3.3, pypdf 6.10.0, pytest 8.4.2, SciPy 1.10.1, and SymPy 1.14.0.
Because pdfTeX was unavailable in the repair environment, its `pdflatex`
invocations were routed through a local Tectonic 0.16.9 compatibility shim;
Biber 2.17 generated the bibliography. Each submission source ZIP was also
built independently with Tectonic and Biber and produced the expected 17-page
main and 17-page supplement. Numerical outputs are certified to the recorded tolerances,
not asserted to be byte-identical across BLAS/SciPy toolchains.

## Historical-lineage stage: not rerun after the repair

The top-level command additionally requires five frozen source archives listed
in `release/reproducibility.md`. They were unavailable in the final repair
environment. Its preflight was exercised against an empty `FROZEN_BASE`: it
reported all five missing archives, exited with status 2, and did not create or
truncate `release/replay.log`.

Accordingly, this corrected release claims a current portable replay and direct
verification of the substantive stages above. It does **not** claim that the
post-repair tree completed the optional historical-lineage replay. The lineage
archives are not consumed by any current proof, data, document, or package
stage.
