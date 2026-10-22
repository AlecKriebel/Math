# Real polynomial derivative zeros

Rank 1033, 2304028 / AMR-022-4028: **already_solved, 0/5**. Read [the acceptance](ACCEPTANCE.md), [complete report](author/REPORT.md), and [independent audit](audit/MATHEMATICAL_AUDIT.md). Theorem A of Bergweiler–Eremenko–Langley (2005), crediting Sheil-Small, settles the real-polynomial target including repeated roots. Sharp parity minimum: 2 floor(d/2), attained by P=−z^d. No novelty or formal proof claim.

## Reproduce the source-free packet

Use trusted Python 3.12 or later, its standard library and operating system, as an actual nonroot user with equal real/effective UID. No network or extra package is required. Get the SHA-256 hashes of PUBLIC_MANIFEST.json, verify_publication.py and mutation_tests.py from the draft PR description or another independently trusted receipt. Verify program hashes before executing them. A manifest supplied by the same untrusted party as a payload is not an independent trust anchor.

    python -I -S -B verify_publication.py EXPECTED_MANIFEST_SHA256 /path/to/packet
    python -I -S -B -O verify_publication.py EXPECTED_MANIFEST_SHA256 /path/to/packet
    python -I -S -B -OO verify_publication.py EXPECTED_MANIFEST_SHA256 /path/to/packet
    python -I -S -B mutation_tests.py EXPECTED_MANIFEST_SHA256 /path/to/packet EXPECTED_WRAPPER_SHA256

The wrapper enforces a closed path inventory, ordinary nonlinked files/directories, finite JSON numbers, duplicate-key rejection, exact-type schemas, externally pinned manifest bytes, and hardcoded accepted-file pins. It captures verified bytes into a read-only temporary snapshot and runs the original author validator under the current optimization mode from a hostile working directory/environment. Permission-denial probes verify that read-only access is effective for the actual user. Success requires the complete typed receipt, including 24 cases and 25 internal rejections. The mutation driver independently checks the wrapper hash before executing it, exercises all three optimization modes, tests wrapper mutations, and reconstructs the original and additional independent validator controls with unchanged trusted validator code. Controlled semantic fixtures receive test-only pins; production pins stay fixed.

The wrapper authenticates preserved evidence; it does not rerun literature inspection or adjudicate scholarly claims from hashes. Missing source/corpus checks and the separate historical SymPy reconstruction are NOT_RUN. Historical acceptance/publication flags remain unchanged. This is a fixed-input integrity and finite-replay check, not a hostile-code sandbox, memory-exhaustion defense, concurrent-filesystem security guarantee, human peer review, or proof-assistant certificate. It reads files before some size checks and relies on trusted Python, the OS and the independently obtained pins.

## Inventory

- author/: exactly the four accepted report, metadata, ledger and validator files
- audit/: the accepted mathematical audit and independent verification record
- FREEZE.json, EXTERNAL_HASHES.json and ORIGINAL_PUBLIC_ALLOWLIST.json: unchanged original metadata
- ACCEPTANCE.md and this README: current source-free disposition and replay instructions
- verify_publication.py and mutation_tests.py: new authored publication integrity/replay programs
- PUBLIC_MANIFEST.json: exact byte/hash allowlist for all other files
