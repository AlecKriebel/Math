# Volumic scalar-curvature closure: audited partial results

**Rank 703 · ID 6700077 · AMR-066-0077 · unsolved here · 5/5 substantive approaches.**

The independent adversarial AI audit passed **only with explicit source-convention and scope qualifications**. The general closure question is not resolved. No historical novelty or global-openness claim is made. This work is unrefereed and has not undergone human peer review.

## Read these qualifications first

The source's printed lower-bound sign, comparison-radius threshold, and infimum convention are mutually inconsistent with its stated smooth scalar-curvature compatibility. The analysis uses an explicitly repaired interpretation: the lower-bound sign, radius `sqrt(2/kappa)`, and supremum convention. These are mathematical inferences, **not an author-approved erratum**. A literal unrepaired reading is not what the partial results prove. The small-radius comparison is interpreted throughout a sufficiently small interval.

The strongest theorem is restricted to **two-dimensional warped metrics** `dt^2 + f_j(t)^2 dy^2` in **fixed warped coordinates**, with locally finitely many piecewise-C2 pieces, a positive continuous warped limit, local uniform convergence, and **kappa >= 0**. It does not cover arbitrary continuous metrics, arbitrary surface gluings, changing coordinates, degenerate limits, negative kappa, or a global uniform radius on a noncompact cylinder. The audit justifies seam-domain deformation and local comparison without assuming a sequence-uniform injectivity radius.

The **relaxed numerical zero bound is distinct from exact Euclidean ball domination**. They cannot be interchanged in the general reductions. The restricted warped theorem proves the stronger Euclidean comparison at zero by its special distributional structure.

The live target page and raw underlying AI record were unavailable and were not independently inspected. The ID/rank association rests on the supplied descriptor and repository queue, not fresh raw-dataset verification. [Source scope](author/SOURCE_SCOPE.md) and [the audit](audit/AUDIT.md) give the exact reading boundaries. Publicly stated manuscript versions and inspection metadata are recorded without redistributing source PDFs, extracted text, or images.

## What is retained

1. [Fixed-witness-radius closure](author/APPROACH_1_FIXED_RADII.md), conditional on comparison radii shared across the approximating sequence for each model.
2. [A radial central-only control](author/APPROACH_2_RADIAL_CONTROL.md) refuting a shortcut. Its approximants fail the all-centers curvature hypothesis; it is not a counterexample to the conjecture.
3. [Second-order-contact transfer](author/APPROACH_3_SECOND_ORDER.md) for a centered local germ, with a sharpness example showing that little-o cannot be replaced by big-O.
4. [The restricted warped-corner closure theorem](author/APPROACH_4_WARPED_CORNERS.md), with the qualifications above and the audit's detailed geometric justification.
5. [Closed-hull and regularization reductions](author/APPROACH_5_REGULARIZATION.md) that explicitly separate two missing implications.

The general obstruction remains: individual small-ball witnesses can collapse along a C0-convergent sequence. No argument here supplies a common comparison radius in general, or either missing bridge identifying volumic and Ricci-flow scalar-curvature notions. Five approaches do not constitute five solutions.

## Frozen records and current assessment

`author/` is the exact 13-file authored snapshot, including its manifest. Its statements that independent review was pending and that no remote publication had occurred describe that earlier snapshot. `audit/` is the exact nine-file independent audit snapshot, including its manifest; its no-remote-write statement likewise describes the audit. Those historical files are preserved byte for byte. This guide records the later qualified audit outcome and preparation for one draft PR; no mathematical correction was needed.

External SHA-256 anchors:

- Author manifest: `b25e29914341432f65924b883eb5361158e3fee1249bcdab57b2281cfbb662b2`
- Audit manifest: `52273269abfb884acd862281b5ddce93e95734a9e2dd2c9d5c2d6b32d7040c40`
- Audit report: `4716d9bbf449d068608d1f6642c1d802e0543185105762ffbe5c6340b67759b0`

## Reproduce the bounded checks

Requires Python 3 and SymPy (the replay used Python 3.12 and SymPy 1.14). From any working directory:

    python3 -B /path/to/6700077/verify_publication.py

The wrapper checks the exact publication file set and frozen anchors, then runs the author and independent suites both normally and with `python3 -O`. It compares their JSON results with the frozen audit records. Per mode, the author suite reports 5,194 auxiliary checks, 25 rejected mathematical negatives, and six file-tampering rejections. The independent suite adds 108 exact symbolic checks, 35 rejected mathematical negatives, and ten external-anchor tampering rejections. An optional externally supplied publication-manifest hash strengthens the release binding:

    python3 -B /path/to/6700077/verify_publication.py --manifest-sha256 EXPECTED_HASH

Checksums and finite or symbolic controls supplement the analytic proofs. They do not mechanically prove the universal geometry, source identity, conjecture, novelty, or openness. The self-excluded publication manifest is not self-authenticating; compare its hash with an external trusted record. No CI pass is inferred from a lack of CI checks.

This package contains authored proofs, audit analysis, code, and public-source verification metadata only. The sole queue edit changes this ID's Status to `unsolved` and Turns to `5/5`; all Findings, Chat, DOI, other rows, and even the stale existing header are preserved. No queue regeneration is used.
