# Draft submission source packages

This directory stages three release targets without contacting or submitting to
any journal or repository:

- `systematic_biology/`: initial Research Article submission to *Systematic
  Biology*;
- `journal_of_mathematical_biology/`: named, single-blind submission to the
  *Journal of Mathematical Biology*; and
- `arxiv/`: compact preprint source staging for arXiv.

The wrappers reuse the canonical article body in `manuscript/sections/` and the
canonical bibliography in `manuscript/references.bib`. They do not copy or
silently edit mathematical prose. `shared/full_abstract.tex` is an exact copy
of the canonical abstract and is checked against `manuscript/main.tex`; the JMB
wrapper uses a separate 150--250 word journal abstract.

Every release-time value that has not been supplied is written as an explicit
`@@TOKEN@@`. The validator treats every such token as a blocker and reports
`NOT_READY`. It recursively scans all materialized source-map inputs, including
the shared and canonical manuscript trees.  It also reports the intentionally
absent PDFs/source set and each `DRAFT_NOT_READY` manifest as release blockers.
Changing a `present` Boolean is insufficient: every present upload must name an
actual project file with exact byte count and SHA-256, and every PDF must bind a
visual-QA report.  A `READY` manifest may retain no declared release blockers.
Nothing here asserts a DOI, license, funding statement, competing-interest
statement, corresponding-author contact detail, submission exclusivity, or
repository deposit that has not been confirmed by the author.

Run the static gate from the project root:

```text
python3 submission/validate_submission_packages.py
```

Exit status `0` means `READY`, `2` means structurally valid but `NOT_READY`, and
`1` means `INVALID`. The present draft is expected to return `NOT_READY` until
the author resolves the listed tokens, the exact archive is deposited, and the
article and supplement PDFs pass render QA.

Official rules checked on 2026-08-25:

- Systematic Biology: <https://academic.oup.com/sysbio/pages/General_Instructions>
- Journal of Mathematical Biology: <https://link.springer.com/journal/285/submission-guidelines>
- arXiv TeX submissions: <https://info.arxiv.org/help/submit_tex.html>
- arXiv `00README` format: <https://info.arxiv.org/help/00README.html>

The official sites remain authoritative at release time; re-check them before
submission because publisher requirements can change.
