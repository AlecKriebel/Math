# Typical cells in hyperbolic tessellations

Problem 30006510 / OWR-14299586-001. **Original problem: unsolved, 5/5 approaches.**

The [frozen result](release/RESULT.md) and [full independent audit](audit/AUDIT_REPORT.md) establish scoped partial results. The audit verdict is PASS_SCOPED_PARTIAL with no blocking findings.

- Finite-volume cells, including unbounded ones, admit the stated median/Palm construction when reciprocal-volume intensity is positive and finite.
- The center-based and uniformly volume-rooted embedded laws are distinguished.
- Infinite-volume cells are not covered by that Palm probability. The ambient probability-root and bare-boundary obstructions do not rule out every alternative notion of typicality.
- No general natural scalar-intensity/typical-full-cell extension or historical novelty is claimed.

Run `python3 audit/check_audit.py` here. It checks the frozen author hashes, reproduces 40 author controls and passes 80 audit controls. These finite checks supplement the analytic review; they are not formal verification.

The author and audit files are included unchanged. Their historical pending-review and no-publication-authorization statements are provenance, not a change to the accepted audit disposition recorded in [PUBLICATION_STATUS.md](PUBLICATION_STATUS.md). OpenAI tools assisted this work; this is not human peer review.
