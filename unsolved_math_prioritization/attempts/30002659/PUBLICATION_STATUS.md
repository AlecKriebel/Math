# Publication status: audited partial findings

2026-10-03 UTC. Problem 30002659 / OWR-13110-001 remains **unsolved, 5/5**.

The frozen author packet contains five substantive proof attempts. Every original author file, including SHA256SUMS, is published byte-for-byte unchanged. Its statements that independent review is pending are historical: the subsequent independent AI adversarial audit passes the stated partial claims and their limitations. Read [the full audit](audit/AUDIT_REPORT.md) for the evidence, equality-case checks, remaining gap, and nonblocking clarification suggestions. This is not a solution, a novelty certificate, or human peer review.

## Verification

- All 13 author-manifest entries match. The author SHA256SUMS file itself has SHA-256 121186eec27a64d42972f33fd155cf48ad6e6600b45b72cab75d320a7e189896.
- The author exact verifier reproduces its saved output and passes 156 assertions.
- The independent verifier reproduces its saved output and passes 265 checks, including manifest and reproduction checks. This is not a count of independent theorems.
- The 80 saved optimization runs are exploratory diagnostics only. They were not rerun for publication, and no claim relies on numerical optimization as a certificate.

From this folder, run:

    sha256sum -c SHA256SUMS
    python verify_exact.py
    python audit/audit_controls.py
    (cd audit && sha256sum -c SHA256SUMS)
    sha256sum -c PUBLICATION_SHA256SUMS

The exact author verifier requires SymPy; the independent verifier also requires NumPy. The recorded SymPy version is 1.14.0. The optional exploratory search additionally requires SciPy.

## Editorial provenance

The public audit preserves its complete mathematical assessment, controls, limitations, and source citations. Only repository-operation logistics were omitted, and relative-path wording was adapted to this repository layout. The independent checker differs from its reviewed version only in resolving the unchanged author packet from its parent folder rather than a sibling public folder. Its resulting JSON is unchanged. The author packet's SHA256SUMS remains its original frozen manifest; audit/SHA256SUMS covers the public audit files, and PUBLICATION_SHA256SUMS covers this complete publication packet except itself.

The remaining low-turn, nonplanar configurations with a non-antipodally-symmetric weighted normal measure remain untreated. No proof of the original every-shortest-orbit conjecture and no certified counterexample are claimed.
