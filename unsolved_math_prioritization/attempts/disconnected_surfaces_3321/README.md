# Frozen partial research: row 1876, ID 3321

Local-only authored partial-results package, frozen 21 October 2026. No publication, no QUEUE edits, no claim of a complete solution or novelty.

The target is **every** optimal drawing, on arbitrary surfaces, not existence of a separated optimum. All five approaches remain part of an unresolved overall investigation. The two limited positive exclusions are the crossing-budget bound and the orientable mixed-crossing forest/no-bridge result. The latter requires unrestricted drawings and orientable genus additivity and does not eliminate cycles. The lattice witness has L=M=20 and is not a graph counterexample. Homology and amplification are method obstructions, not solutions.

Known sphere/projective-plane cases and the connected-graph Klein-bottle theorem retain their source gate qualifications. The September 2026 Mohar–Šámal torus result is an announcement concerning existence, not an inspected full proof or a certificate for every optimum.

FIVE_APPROACHES.md and INDEPENDENT_AUDIT.md contain the mathematical reasoning. SOURCE_STATUS_GATE.md preserves known/announced attribution and unresolved obligations. Public source metadata records prior retrieval/inspection history; packaging does not independently re-retrieve source PDFs or private datasets. No source documents, dataset contents, or private coordination files are included. PROVENANCE.json traces each included input. AST_PROVENANCE.json records complete location-bearing AST dumps for all executable Python files, not just selected functions.

Run from any directory:

    python -B /path/to/package/verify.py /path/to/external/RECEIPT.json
    python -O -B /path/to/package/verify.py /path/to/external/RECEIPT.json

Both verifier modes replay the checker in normal and optimized Python, comparing complete JSON results. MUTATION_TESTS.json records semantic checker mutations and fail-closed inventory tests. These are finite implementation checks; the unbounded lattice minimum follows from the congruence proof, not enumeration.

The external receipt pins MANIFEST.json, which pins every other package file and requires exact inventory. Filesystem entries are checked before any package payload is read; symlinks, special files, and unexpected directories are rejected. The test suite uses a FIFO and symlink but creates no sockets. This is a static local integrity check, not protection against a concurrent hostile filesystem writer or a cryptographic third-party attestation. Trust the external receipt and verifier independently before executing code; self-verification alone is not a trust anchor.
