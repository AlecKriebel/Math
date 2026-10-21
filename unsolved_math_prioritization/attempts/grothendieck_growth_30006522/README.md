# Grothendieck Schubert-support growth: frozen bounded research

Row 1873; problem 30006522 / OWR-14299904-004. Status: **UNSOLVED**. Seven approaches are retained in `research/RESEARCH_REPORT.md`. No general proof, counterexample, or novelty claim is made. The exact skew-sum equivalence is auxiliary progress; the explicit examples refute stronger proof strategies, not the target conjecture.

## Scope and evidence

- Exhaustive divided-difference computation: all 40,320 permutations in S8, 1,315,946 support incidences and 1,271,255 non-top incidences, with no growth or sign failures. This is finite evidence only.
- Independent staircase pipe-dream implementation: through S6 only, all 32,768 subsets and 720 permutations. It is not an independent S8 implementation.
- Skew-sum polynomial factorization: 465 instances / 930 comparisons through total size six. General equivalence rests on the written proof, not the finite test.
- Left-weak convexity: exhaustive S7 missing-neighbor check, not a general theorem.
- Public source metadata records historical retrieval/inspection, not a new literature refresh or certification of third-party preprint proofs. `SOURCE_STATUS_GATE.md` records the initial gate; the research report and updated public metadata record the later full-HTML inspection of Weigandt's path formula.

## Files and reproducibility

`research/` contains the accepted report, mathematical audit, source scripts, exact statistics, and the historical original research manifest. That manifest describes the accepted input bytes, not the modified portable scripts. `verification/AST_PROVENANCE.json` records original and packaged hashes and whole-module AST equality after only output-path string normalization. All mathematical code, checks, imports and entry points are preserved. Pickles are transient locally generated replay intermediates, not included or accepted from outside.

Run from any directory with Python 3 (standard library only):

    python -B verification/verify_ast.py
    python -O -B verification/verify_ast.py
    python -B verification/negative_controls.py
    python -O -B verification/negative_controls.py
    python -B verification/replay.py /tmp/groth-replay-results

The replay runs all seven scripts/parameter cases separately in both normal and optimized mode. Every output JSON must match the accepted result exactly except the documented top-level `seconds` field in exact_n5/n7/n8.json only (finite, nonnegative numeric values, excluding booleans). It preserves examples, counts and failure lists, not just a summary success flag. The runner writes to isolated temporary workspaces and the explicit result destination, never overwriting frozen research artifacts. Whole-module provenance can additionally be checked against the original accepted research directory passed as the optional argument to `verify_ast.py`.

`NEGATIVE_CONTROLS_*.json` covers mathematical strategy obstructions, a deliberately false skew factorization, real nested FIFO and symlink rejection, extra files and mutated payloads. Socket/device modes are synthetically tested; no socket is created. `verify_inventory.py` classifies the full recursive tree before reading payloads, rejects all non-regular/non-directory objects, and compares exact directories, paths, byte counts and SHA-256 values against the separate freeze receipt. It uses non-following/nonblocking opens and identity checks to reduce race exposure; hostile concurrent replacement of ancestor directories is outside this local frozen-tree verification model.

## Delivery boundary

Local-only package. No publication or QUEUE edits. Copied PDFs, extracted source text, dataset contents, private coordination files and bytecode are excluded. Dataset/PDF hashes and public titles/URLs are metadata only. The external receipt is outside the package to avoid a self-referential hash inventory. Future external publication would require its own verified process; nothing here claims publication.
