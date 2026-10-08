# Audited corrected partials: critical-value collisions

Problem 10800003 / AMR-107-0003, rank 1011. **Unsolved, 5/5 substantive approaches.** This source-free publication accepts only the corrected mathematical packet at `audit/corrected/author/PROOF_AND_STATUS.md`. The original `author/` and `freeze/` are preserved as historical evidence; their proof is superseded by the exact `audit/CORRECTIONS.patch`. All audit files are unchanged.

The accepted scope comprises local A1+A1/A2 endpoint models, normalized symmetric rank-two monodromy, a conditional geometric obstruction with collision-compatible common path transport, an integrable inverse-Jacobian continuation criterion with explicit regularity, and a nonversal X9 grid obstruction rejected by full-miniversal tangent interpolation. Separating curves on bordered surfaces lie in the intersection radical, but need not be null-homologous. The rejected Torelli pair and restricted-slice example are not counterexamples. The general prescribed small-neighborhood collision lift remains unresolved by this work.

The inspected 2026 quartic/X9 and J10 real-surgery results are credited. Global realization does not supply the prescribed local lift. Source titles, URLs, versions, hashes, sizes and historical inspection extents are in the preserved metadata. The original Jaworski proof was not independently inspected. No worldwide-openness, novelty, formal-verification or human-peer-review claim is made.

## Reproduction

Obtain the SHA-256 of `BOOTSTRAP.py` from an independently trusted publication receipt. Hash the file before executing it. The bootstrap authenticates the verifier and manifest; the verifier checks the complete path inventory and pinned original/audit/corrected bytes before running any child code. Exact historical receipt replay requires the non-root account with UID 1000, because the unchanged original validation driver and recorded audit receipts explicitly check that UID. Execute as UID 1000:

    python3 -I -S -B BOOTSTRAP.py /absolute/path/to/packet
    python3 -I -S -B -O BOOTSTRAP.py /absolute/path/to/packet
    python3 -I -S -B -OO BOOTSTRAP.py /absolute/path/to/packet

The full replay reproduces the 390-check corrected author diagnostic; reruns all 120 original validation cases and 115 independent audit cases, including 405 independent exact checks and exact patch reconstruction. Disposable copies and receipts are written outside the packet. Creation and append are actually denied on read-only non-root test copies. These finite tests are not formal analytic/geometric proof verification or an arbitrary-hostile-code sandbox; filesystem races and network isolation are not certified. The complete packet must not be concurrently changed during authentication/replay.

`TEST_MUTATIONS.py PACKET` tests the publication boundary, hostile substitutions, parser controls and whole-packet read-only execution in all three Python modes. Authenticate that script through the pinned publication manifest before executing it.

Source and corpus bytes are excluded. Default current reverification is `NOT_RUN`; preserved success receipts describe earlier checks only. Optional `--source-dir DIR` verifies six actual supplied files using the names in the author reproducibility document. Optional `--problems FILE --research-results FILE` streams and hashes both complete supplied corpora. Such matches establish byte identity only; they do not rerun source inspection, download current literature, or redo a record-level join. A missing/mismatching requested input fails closed. GitHub CI is reported separately and is never inferred from local replay.
