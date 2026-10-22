# 30005926: high-genus distance and diameter constants

**Unsolved, five substantive approaches. Independent audit pending.**

The typical-distance statement is already proved in Tanguy Lions's 2026 preprint, Theorem 1.1. This packet does not prove the diameter constant or its conjectured ratio three. It makes no novelty or priority claim.

Read `MATHEMATICAL_REPORT.md` for the exact model, twelve numbered results and their proofs, credited inputs, and remaining gaps. The authored material includes:

- Explicit parameter elimination and endpoint expansions
- Typical-pair to extreme-pair bounds, with their required rates
- A genus-preserving tube construction showing why typical distances alone are insufficient
- An exact first moment and cutoff for one specified removable tube family
- A conditional extreme-decoration theorem giving the constant beta + 2/alpha

The tube construction changes the distribution and does not refute the uniform-model conjecture. The conditional theorem is not asserted to apply to that model. A strict diameter-versus-typical gap is credited to Budzinski–Chapuy–Louf and combined with Lions, rather than presented as new.

## Reproduce finite controls

Python 3.10+; standard library only:

```
python verify.py
python -O verify.py
```

Both modes reproduce `RESULTS.json`. There are 57,304 checks: 57,292 exact finite controls and 12 Decimal numerical diagnostics. These include 772 connected labelled graphs through five vertices, 120 explicit triangulated-tube instances, 54 decorated graphs, and negative controls. They do not prove an asymptotic theorem. The tube mesh tests use simple-face examples; the repeated-corner case is covered by the written topological argument, not a complete combinatorial-map enumeration.

`TURN_LEDGER.json` separates the five mathematical approaches from retrieval, audit and packaging. `SOURCES.json` records public citations, retrieval/inspection limitations, byte counts and hashes. No source PDFs, source extracts, raw datasets, private sources or coordination files are included. `VERDICT.json` is the machine-readable scope declaration.
