# Three-terminal shortest-path blocking: reviewed proof packet

Problem 30000347 / OWR-1111-001, queue rank 962.
Disposition: **claimed_solved, 1/5 substantive proof-attempt turns**.

The complete [frozen proof](frozen_packet/PROOF.md) proves NP-completeness of undirected, unit-traversal-length, three-terminal Blocking Shortest Paths, even with unit deletion costs and all original terminal distances equal to 3. The exact optimization problem is NP-hard. Positive rational deletion costs and the optional finite-terminal-distance / exact 3-to-4 extension are treated explicitly.

Two independent full mathematical audits accepted the unchanged proof without required corrections: [audit A](independent_reduction_audit/AUDIT_REDUCTION.md) and [audit B](independent_audit_2/AUDIT.md). See [acceptance and limitations](ACCEPTANCE.md) and [source/model assessment](frozen_packet/SOURCE_AND_MODEL.md).

## Reproduce

Requires Python 3.10+ and its standard library only. From this directory:

    python3 verify_publication.py
    python3 -O verify_publication.py
    python3 mutation_tests.py

The verifier checks all published payload bytes, the original manifests, archive contents, and all three mathematical check suites. It runs unchanged scripts in a temporary copy and compares all deterministic result fields; historical result files remain untouched. It needs no network, source PDFs, source images, copied source text, datasets, credentials, or original workspace. Finite computation supports the written proof; it is not a formal certificate of a universal theorem.

## Historical integrity

The seven-file frozen packet and its original archive are preserved byte-for-byte. Both full audit reports, manifests, independent checkers and recorded results are preserved. Audit A's separately copied author rerun is also preserved. Audit B's duplicated author rerun and all rendered source images are omitted; they are not listed payloads of its audit manifest. The original frozen README and manifest retain their pre-audit status, now superseded for disposition by ACCEPTANCE.md. No original proof or audit was edited.

This is AI-assisted research and independent AI-assisted review. It is not human peer review, journal acceptance, formal proof-assistant certification, or a novelty/priority determination. The classification answers the exact historical mathematical question, without claiming it remained open until this work. Draft PR only; no merge, release or DOI.
