# OPG-37237: word problem for 2-knot complements

**Unresolved after five substantive attempts.** No smooth/locally flat PL 2-knot with undecidable word problem, and no universal decidability theorem, is claimed.

The packet includes:

- `PROOF.md`: rigorous partial results, exact failed steps, and source links.
- `ATTEMPT_LOG.md`: five distinct approaches and their outcomes.
- `SOURCE_GATE.md`: original-source checks, recent literature, scope safeguards, and prior-work checks.
- `verify.py` and `verification.json`: deterministic finite consistency checks.
- `SOURCE_HASHES.json`: hashes and public URLs of inspected source documents, which are not redistributed.
- `STATUS.json` and `SHA256SUMS`: outcome and frozen artifact integrity.

A concrete result is a rational-homology obstruction to using the September 2026 small undecidable group as a knot group: its second rational homology has dimension at least two. The packet also gives a full word-problem algorithm for an explicit non-residually-finite 2-knot group. These are partial exclusions, not a solution of the original question; novelty is not asserted.

Reproduce with Python 3 (standard library only):

    python verify.py > /tmp/3419-verification.json
    cmp verification.json /tmp/3419-verification.json
    sha256sum -c SHA256SUMS

The finite checks do not prove undecidability or certify a topological realization. Independent review is pending at this freeze.
