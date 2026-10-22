# Initial odd ears and NP completeness

Problem ID 30002726, source question OWR-13353-012, queue row 1828.
Prepared 20 October 2026. Recorded status: **CLAIMED_SOLVED, 3/5 approaches**.
The full proof was reached after three substantive approaches; five completed
approaches are not claimed.

## Accepted mathematical result

Deciding whether beta(G) >= t is NP-complete, even for simple
2-vertex-connected graphs with a universal vertex whose deletion leaves a
connected bipartite graph. Here t is part of the input. Beta is the maximum
number of initial consecutive odd ears in an **open** ear decomposition; the
initial circuit and one-edge ears both count. Odd ears after the first even
ear do not count. The general input class is finite loopless graphs with at
least three vertices, and can allow parallel edges; the reduction uses none.

The result is supported by a complete Set Cover reduction and a separate
adversarial mathematical audit with verdict PASS. This is an authored proof
with internal independent review, not external peer review or a certification
of literature novelty. No fixed-threshold hardness or hardness for the
different maximum-total-odd-ear objective is asserted.

## Reading order

1. `NP_COMPLETENESS_PROOF.md`: the complete accepted proof, unchanged from
   the manuscript identified by the audit's SHA-256.
2. `AUDIT_HARDNESS.md`: exact-target alignment, cone identity, both reduction
   directions, polynomial output size, NP membership, and finite-test limits.
3. `ACCEPTANCE_REPORT.md`: acceptance scope, evidence, and exclusions.
4. `SOURCE_GATE.md`: historical source/literature verification before the
   proof. Its bounded prior-literature finding is not the present proof status.
5. `CORPUS_VERIFICATION.json` and `SOURCE_METADATA.json`: public hashes, byte
   counts, source URLs, and retrieval/inspection history only.

## Reproduction

Python 3.10 or later and the standard library suffice. No installation,
network access, source PDF, dataset, or private research file is needed.

From this directory run:

    python3 -I -S -B verify_manifest.py
    python3 -I -S -B run_checks.py

The second command copies the mathematical checker and expected result into
a fresh temporary directory, runs it in isolated Python mode, compares its
complete JSON output and generated file with the shipped result, and prints
a replay report. Neither command modifies the package. `REPRODUCIBILITY.md`
describes the checks and the role of `REPLAY_VERIFICATION.json`.

The exact deterministic checks cover 63 explicit block graphs, 14 cones
checked by full factor-critical subset enumeration, and 1,719 threshold
decisions over 441 set systems. There were zero discrepancies. Finite checks
corroborate the proof; they do not replace its universal arguments.

## Contents and boundaries

`MANIFEST.json` enumerates every other package file by byte count and SHA-256.
The package contains the complete audited primary proof, its audit, source
metadata, the standard-library checker, expected results, and replay tools.
Alternative SAT, multigraph, and odd-subdivision derivations are not included
and are not needed for acceptance. No third-party source document, dataset
content, private source, coordination file, or execution cache is included.
