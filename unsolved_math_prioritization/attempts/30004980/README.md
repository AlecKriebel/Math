# Maximum twin-width: audited partial research record

Alec Kriebel · [ORCID](https://orcid.org/0009-0001-9320-500X)

Problem 30004980 / OWR-9790352-030. Status: **unsolved, 5/5 substantive attempts**. The exact maximum twin-width of an n-vertex graph remains unresolved by this work. Independent FULL PASS applies to the corrected partial record and its evidence boundaries, not to a solution of the open problem.

## Read the corrected record

- [Corrected release v1](release_v1/README.md), retaining all 18 independently reviewed file bytes.
- [Full corrected audit](audit/corrected_pass/PUBLIC_AUDIT_REPORT.md), including all five mathematical attempts, source review, exact computations, and correction re-review.
- [Portable independent controls](audit/corrected_pass/README.md).
- [Correction history](release_v1/CORRECTIONS.md) and [exact reviewed change map](audit/corrected_pass/reviewed_change_map.json).
- [Historical original HOLD report](audit/original_hold/PUBLIC_AUDIT_REPORT.md). The original 17-file author freeze remains available at [its immutable WIP commit](https://github.com/AlecKriebel/Math/tree/ab502620095141f19e983d835c5ca3ac885ed21c/unsolved_math_prioritization/attempts/30004980).

The corrected release's historical README and log say narrow review was pending at freeze time. The completed FULL PASS is recorded in the separate corrected audit; reviewed author bytes have not been silently rewritten. The original endpoint-definition error is preserved in the historical report, with its K2 counterexample. No original verdict or artifact was retroactively changed.

## Results and limits

The record includes a concrete obstruction to scheduling an arbitrary near-twin matching, exact finite maxima through six vertices, and a count of safe second contractions in conference graphs. Known first-step bounds, the additive pair-scheduling mechanism, symmetry results, and the six-vertex bound are explicitly credited. No novelty certification is claimed. Finite enumeration and random samples are not a general upper-bound proof. The current exact problem webpage was inaccessible; the official Oberwolfach report and cited primary literature supply the source scope.

## Reproduce

Using Python 3.10+ without optimization flags, from this directory:

```sh
python audit/corrected_pass/verify_readme.py release_v1
python audit/corrected_pass/independent_verify.py release_v1 --full
python audit/corrected_pass/independent_conference.py
```

Only the Python standard library is required. The first runner copies the release into a temporary directory and compares generated result bytes. Audit scripts write their result JSON beside themselves; use a disposable checkout if preserving every audit-file byte is desired. Each subpackage manifest binds its original reviewed bytes; PUBLICATION_MANIFEST.json binds the assembled public package.

Source PDFs, extracted source text, screenshots, full corpus files, and private context are excluded. This is an unrefereed AI-assisted research record. No merge, release, DOI, or external researcher outreach accompanies this publication.
