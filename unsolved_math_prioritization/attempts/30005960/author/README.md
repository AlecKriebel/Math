# Stability conditions from surface contractions

Problem 30005960, OWR-14298581-007. Literature checked 7 October 2026.

## Result

The literal request to obtain further examples by degenerating geometric surface stability conditions has a prior-literature answer. Vilches's 2025 Theorem 1.3 constructs such limits for simultaneous contractions of suitable rational chains, with the full support property in a specified chamber. Chou's revised 2025 paper separately constructs stability on a surface with one ADE singularity, compatible with a weak condition on its resolution.

This packet gives a fully specified application to the smooth toric resolution of the weighted projective plane P(1,3,8). Its exceptional locus has two disjoint chains, with self-intersections (-2,-2) and (-3,-3). The rational divisor beta, the limiting central charge, and a rational constant-volume ample path are explicit. The existence, Harder–Narasimhan property, full support property, and convergence are credited to Vilches, rather than claimed as new results or consequences of the arithmetic tests alone.

Suggested queue disposition after independent acceptance: `already_solved`, `0/5`, with the scope qualification “known constructions answer the literal existential direction; no universal classification claimed.” No five research attempts have been fabricated or counted for a request already answered by the literature.

## Files

- `REPORT.md`: exact scope, literature status, and attribution.
- `EXPLICIT_EXAMPLE.md`: the toric application and a separate singular-surface application.
- `SOURCE_AUDIT.md`: theorem dependencies and an independently checked D4 warning outside the selected chain application.
- `check_exact.py` and `CHECK_RESULTS.json`: dependency-free exact arithmetic controls.
- `SOURCES.json`: public bibliographic and retrieval metadata, including PDF hashes and byte counts.
- `MANIFEST.json`: frozen file identities.

Run `python3 check_exact.py` and compare its stdout byte-for-byte with `CHECK_RESULTS.json`. These tests are finite arithmetic checks and symbolic identities; they are not formal verification of a stability theorem.

All included text and code were authored for this packet. Third-party PDFs, extracted source text, dataset records, and private coordination material are excluded. The packet has not been independently accepted or published. The cited Vilches and Chou items are preprints in the inspected records; the present application and audit are AI-assisted, unrefereed, and not proof-assistant verified.
