# Gibbs leaf compatibility: reconstructed conditional correction

Problem 20001730 / AIM-GEOMETRY-0068, rank 673. **Unsolved; historical budget 5/5.**

The general construction problem remains unsolved in this work. Under the explicit strong hypotheses in `author/CORRECTED_THEOREM.md`, an already existing measurable whole-leaf Gibbs family obeys the second transport law on a possibly smaller invariant conull domain D'. The exceptional toral-leaf example shows why an arbitrary original domain D cannot necessarily be retained. No novelty is claimed.

## Review and preservation

- `author/` preserves all eleven newly frozen reconstruction files byte-for-byte.
- `audit/` preserves the complete fresh independent review and its six-file freeze. The review accepts the conditional theorem and counterexample under the stated hypotheses and ordinary second-countable smooth-foliation interpretation.
- `CLARIFICATIONS.md` separately expands the chart-local uniform-radius argument, specifies the product flat metric, and distinguishes orbit-leaf distinctness from genericity. Neither freeze was rewritten.
- `archives/` preserves both original frozen ZIPs and their hash sidecars.
- The older release, older audit, and exact historical diff were not recovered. The historical 5/5 budget is retained as reported, not represented as five freshly repeated attempts. Old acceptance is not inherited.

The author freeze's pending-review wording and both freezes' no-publication-at-preparation wording are preserved historical statements. The separate fresh audit records the completed review; this publication wrapper supplies the present reading order and checker.

## Required offline gate

With Python 3.9 or later and no external packages, from this directory run:

    python verify_publication.py
    python -O verify_publication.py

Use this gate or the pinned independent audit checker. **Do not rely on `author/verify_release.py` under Python optimization:** its integrity assertions disappear and it reproducibly accepts a modified proof. This defect is retained and prominently documented rather than hidden by editing the freeze.

The publication gate uses explicit runtime checks, pins both manifests and archives, validates the full inventory and archive members, runs the independent audit in normal and optimized modes, and tests publication mutations in both modes. The pinned audit supplies 1,444 independent finite checks and replays 4,177 original finite assertions in a nonoptimized subprocess. These are algebra and packaging checks, not a formal verification of disintegration, measurable selection, recurrence, ergodicity, or the continuous theorem.

Only authored mathematics, code, review, and public source-verification metadata are included. Source PDFs, raw or extracted source text, dataset contents, private sources, and private coordination files are excluded. Public source hashes describe previously inspected bytes; the offline replay does not recover or revalidate omitted sources.

The queue change is limited to this problem's Status (`unsolved`) and Turns (`5/5`). Its Findings field and all unrelated bytes, including the existing header, are preserved. No queue generator, merge, GitHub release, DOI, or outreach is part of this publication.
