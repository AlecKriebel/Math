# Genus-two RM Galois images: audited partial results

Problem 30001840 / OWR-11127-008; rank 981; **unsolved, 5/5**.

Start with [ACCEPTANCE.md](ACCEPTANCE.md), [the full expanded proof](audit_independent/corrected_public/PROOF.md), and [the full audit](audit_independent/AUDIT.md). Both the original freeze and corrected derivative are preserved. The [actual patch](audit_independent/PROPOSED.patch) expands proof details and repairs optimization-unsafe checks. The [prospective bridge](audit_independent/PROSPECTIVE_BRIDGE.md) supplies no additional accepted Jacobian-image coverage.

## Portable, source-free replay

Use trusted Python 3.9+ and its standard library, on a trusted operating system. No network, paper, dataset or third-party package is required. Obtain the PUBLIC_MANIFEST.json, verify_publication.py and mutation_tests.py SHA-256 values from the draft PR description or another independently trusted receipt. Check the verifier's bytes before running it. An adjacent checksum is not its own external trust anchor.

From any working directory:

    python -I -S -B /path/to/verify_publication.py MANIFEST_SHA256 /path/to/packet
    python -I -S -B -O /path/to/verify_publication.py MANIFEST_SHA256 /path/to/packet
    python -I -S -B -OO /path/to/verify_publication.py MANIFEST_SHA256 /path/to/packet

The wrapper enforces the exact inventory, sizes, hashes, three immutable manifest pins and nested manifests; rejects links, special files and unexpected entries; strictly reconstructs both patch targets in memory; and runs authenticated snapshots in temporary directories. Real child flags are recorded. Complete computed outputs are compared with the frozen receipts. Original optimized output reproduction is explicitly distinct from validation; corrected and independent explicit checks stay active. The frozen mutation harness separately launches actual ordinary and -O children in each replay; it does not test -OO mutants. Direct corrected/independent -OO checks are covered by an outer -OO run.

After authenticating both scripts, run the corruption suite:

    python -I -S -B /path/to/mutation_tests.py MANIFEST_SHA256 /path/to/packet

It repeats normal/-O/-OO and relocated replays and rejects deliberate missing, altered, extra, linked, malformed and manifest-laundered inputs. It leaves the supplied packet unchanged. This is integrity/reproducibility checking, not a hostile-code sandbox, race-resistant security boundary or formal mathematical proof.

PUBLIC_MANIFEST.json lists every other payload file. Public source metadata describes historical reading and retrieval. PUBLICATION_SOURCE_CHECK.json separately records publication-time rehashing of eight existing PDFs; portable replay does not repeat that rehash, retrieve papers, inspect pages or rehash the excluded public datasets. No new source reading is claimed by packaging. Historical inner status statements remain unchanged.
