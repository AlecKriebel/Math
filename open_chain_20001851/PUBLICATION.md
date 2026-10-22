# Reviewed partial-results packet

Problem 20001851 / AIM-GEOMETRY-0189. Outcome: **unsolved, 5/5**.

The five author attempts and their accompanying source record, overview, log,
checker, and check output are preserved byte-for-byte. Their hashes and sizes
are recorded in `AUTHOR_MANIFEST.json`.

A fresh independent adversarial review passed this packet only as partial
work. The [full audit](review/AUDIT.md),
[independent checker](review/independent_checks.py), and
[independent output](review/independent_checks.txt) are included. No universal
connectivity result, locked equilateral chain, or computed component count
is certified.

## Additive clarification

Attempt 2 assumes the initial chain is **strict-simple**, as stipulated in
the source/model record. For unequal lengths, the scalar nonadjacent-interval
inequalities alone do not exclude adjacent overlap. The spherical-cap motion
starts at a non-overlapping configuration and avoids its sole adjacent-overlap
direction throughout. This clarification leaves the frozen proof unchanged.

The eight-bar construction concerns moving only the first endpoint while
holding the seven-bar tail fixed. It does not establish locking when all
vertices can move. The rational six-bar example is explicitly unlocked even
though every scalar-axis certificate fails.

## Portability and provenance

The audit's introduction now refers to the repository-relative author manifest.
The independent checker resolves `checks.json` relative to its own file rather
than an execution-workspace path. Its mathematics is unchanged, and its output
was reproduced byte-for-byte after this portability edit. Source PDFs, source
screenshots, cached corpus files, and private research history are omitted.

Run `python3 verify_publication.py` to check the file hashes and reproduce both
outputs. The author checker uses only the Python standard library. The separate
independent checker requires SymPy; it was reproduced with SymPy 1.14.0.
The wrapper reports a missing dependency as a failure rather than claiming an
unrun check passed.

The accompanying queue edit changes only this problem's status and turn-count
cells to `unsolved` and `5/5`. All other queue content is preserved.

AI tools were used extensively. This packet and its independent AI review are
unrefereed and do not constitute external human peer review. No novelty,
priority, or full-resolution claim is made.
