# 30005717 — Even-dimensional stress-space reconstruction

**Disposition: unsolved, five substantive approaches completed.** This packet does not prove or disprove the full conjecture. It provides an exact reconstruction criterion, credited special cases and counterexamples to stronger auxiliary claims, an obstruction to a suspension shortcut, and reproducible rational checks.

The target is the even case of Conjecture 2 in the official Oberwolfach report, printed page 3303: for a simplicial \(2k\)-polytope in its natural embedding, with no missing faces of dimension at least \(k+1\), does its affine \(k\)-stress space determine its affine type?

The most important current-literature correction is that Novik–Zheng's April 2026 paper disproves **full lower-degree stress generation** and **universal face participation**. Those are stronger auxiliary assertions, not the target affine-reconstruction conjecture. The explicit three-triangle calculation here reproduces their family and carries no novelty claim.

- [RESEARCH.md](RESEARCH.md): definitions, five approaches, proofs of claimed reductions and calculations, remaining gap.
- [sources.json](sources.json): primary references, versions, locations, and source-byte hashes.
- [check_exact.py](check_exact.py): self-contained exact-rational verifier, requiring Python 3 and SymPy (tested with 1.14.0).
- [exact_results.json](exact_results.json): ten target-class examples, one odd-dimensional suspension control, and one excluded stacked-polytope negative control.
- [status.json](status.json): bounded disposition and attempt ledger.

Run python check_exact.py. It regenerates exact_results.json. No source download or source full text is needed. Facets are exhaustively enumerated with exact supporting-hyperplane tests; all stress support and differential equations are checked. Finite checks supplement the proofs and do not establish the unrestricted conjecture.

This is AI-assisted, unrefereed research and reproduction. No human peer review, formal proof-assistant verification, complete literature coverage, or historical novelty is claimed. Source PDFs and full texts are not part of this public packet.
