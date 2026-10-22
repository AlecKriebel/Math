# Portable integrity and diagnostic verification

Requirements: Python 3 with its standard library. No network, third-party packages, copied source documents, or original workspace paths are needed.

From this directory run:

    python3 verify_publication.py
    python3 -O verify_publication.py

The verifier checks every allowlisted packet member's byte count and SHA-256 against PUBLICATION_MANIFEST.json, rejects unlisted files (except Python bytecode caches), validates the original manifest against the preserved author files, compares all nine original archive members byte-for-byte, verifies that neither audit is in the original archive, and reruns the frozen algebra script with and without Python optimization. Both diagnostic outputs must be byte-identical to authored/CHECK_RESULTS.json and report exactly 2,896 conditions with the invalid-R negative control detected. Explicit exceptions remain active under -O. The verifier writes no packet files.

For diagnostics alone, from any working directory:

    python3 path/to/this/packet/authored/check_algebra.py
    python3 -O path/to/this/packet/authored/check_algebra.py

The standard output can be compared with authored/CHECK_RESULTS.json. Reproducibility covers byte integrity and exact finite examples, not a machine proof of the full theorem. Read the complete proof and both audits to assess the global argument. PUBLICATION_MANIFEST.json cannot hash itself; its identity can be pinned by the Git commit and external publication receipt.

SOURCE_HASHES.json records public URLs and identities of previously inspected sources. It does not include source contents or promise that a later download has unchanged bytes. The original author manifest covers the original eight payload files, excluding itself; the original ZIP additionally includes that manifest. The two later audits are tracked by the publication manifest rather than retroactively added to the original archive.
