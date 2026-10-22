# Shortest paths in line arrangements: accepted partial results

Problem 3800015 (AMR-037-0015), rank 1060. Status: exhausted, five of five substantive routes. The general exact subquadratic-algorithm or quadratic-lower-bound target remains unresolved. No novelty, priority, formal-proof, or arbitrary-real bit-complexity claim is made.

## Read in this order

1. [Acceptance and limits](ACCEPTANCE.md).
2. [Mathematical report](author/REPORT.md), the mandatory [source/output clarification](SOURCE_OUTPUT_CLARIFICATION.md), and the preserved [hop-witness correction](author/CORRECTIONS.md).
3. [Independent mathematical audit](audit/AUDIT.md).
4. Public bibliographic/retrieval metadata in [SOURCES.json](author/SOURCES.json) and [SOURCES_AUDIT.json](audit/SOURCES_AUDIT.json).

The author and audit subdirectories reproduce all sixteen files of their accepted source-free freezes byte-for-byte. Every file listed by either original manifest is included. The clarification is mandatory for this delivery even though the preserved historical audit describes its patch as optional. No third-party PDF, HTML, DOI JSON body, dataset contents, prior rejected report, or private coordination material is included. CORPUS_METADATA.json contains only public byte counts and hashes, not records.

## Reproduce

First obtain BOOTSTRAP.py's SHA-256 from the separately reviewed draft-PR body and verify a trusted external copy. A checksum obtained only from a mutable package is not an independent trust anchor. Run that external copy against a separately staged delivery directory and the exact proposed QUEUE.md. Do not execute the untrusted delivery's bootstrap before authenticating it.

Use Python 3.12.14, UID and EUID 1000, standard library only. Make the staged delivery and all its members read-only (directories 0555, files 0444); also make QUEUE.md read-only. The tests intentionally require operating-system rejection of existing-file writes and new-file creation. Owner-changeable modes demonstrate denied writes, not immutable storage or protection against a concurrent malicious owner.

    python3 -I -S -B /trusted/BOOTSTRAP.py /staged/delivery --queue /staged/QUEUE.md
    python3 -I -S -B -O /trusted/BOOTSTRAP.py /staged/delivery --queue /staged/QUEUE.md
    python3 -I -S -B -OO /trusted/BOOTSTRAP.py /staged/delivery --queue /staged/QUEUE.md

The fixed bootstrap pins the entire DELIVERY_MANIFEST.json. That manifest binds every public file, including acceptance, full expected streams, public execution receipts, and hostile-test evidence, plus the exact QUEUE bytes. Only the manifest and external bootstrap are excluded from manifest payload entries; the external bootstrap's digest is the trust root, and the staged bootstrap must match it byte-for-byte. Exact directory/file inventories reject extra files, missing files, empty directories, links, special files, unsafe names, and malformed or mistyped manifest entries. All JSON members are parsed with duplicate-key and nonfinite-number rejection.

REPLAY.py compares complete fresh child outputs, including exit codes, full stdout/stderr and recursively typed parsed objects, against the pinned EXPECTED_OUTPUTS.json. The full-stream mutation driver replaces only exact temporary-mutant and audit-directory prefixes with <MUTANTS> and <AUDIT>; no result fields or other text are normalized. Each outer optimization mode also runs the native mutation suite and its full-stream extension across all three optimization modes. The outer bootstrap additionally compares complete stdout bytes to the pinned mode-specific evidence.

For optional local source-byte matching, supply --source-dir containing eight regular files named S01 through S08 with bytes identified in author/SOURCES.json. For optional corpus-byte matching, supply both --problems and --research-results. Optional inputs are hashed locally and are never redistributed. Supplying them does not perform fresh retrieval, source inspection, or a record join. Absent inputs are explicitly NOT_RUN. --integrity-only authenticates the delivery and queue without mathematical execution; it cannot be combined with optional inputs.

Run TEST_DELIVERY.py with the trusted bootstrap, delivery directory, and queue to reproduce the package-tampering and schema controls. Fresh mathematical replay is finite exact-rational evidence, not a substitute for reading the proofs or a solution of the general target.
