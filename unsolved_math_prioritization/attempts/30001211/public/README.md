# Uniform critical connectivity for minimal interval exchanges

Problem 30001211 / OWR-3396-010, queue rank 613.

**Unsolved after five substantive author approaches. No full solution or novelty
claim. Independent review is pending.**

- `RESULT.md`: exact target, source cautions, complete partial proofs, failed
  extension mechanisms, and exact remaining gap.
- `APPROACH_LOG.md` and `turns.json`: the five distinct approaches and budget.
- `SOURCES.json`: primary-source locations, dates, and bounded literature limits.
- `readiness.json`: scope and pre-attempt repository/source checks.
- `verification/check.py`: exact rational/quadratic-field bounded controls.
- `verification/result.json`: their reproducible output.
- `MANIFEST.json`: SHA-256 manifest of the frozen author packet.

Run with Python 3.10+ (standard library only):

    python verification/check.py > /tmp/iet-controls.json
    cmp verification/result.json /tmp/iet-controls.json

The code does not establish any new infinite-time theorem; the analytic proofs
carry those claims. Original source PDFs, source-page screenshots, full corpora,
and private coordination records are deliberately absent.
