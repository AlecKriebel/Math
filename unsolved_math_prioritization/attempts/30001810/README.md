# Ordinary versus immersive simplicial volume: corrected partials

Problem 30001810 / OWR-5158-010; rank 980; **unsolved, 5/5**.

Start with [ACCEPTANCE.md](ACCEPTANCE.md), then the [corrected report](corrected/MATHEMATICAL_REPORT.md) and [full audit](audit/AUDIT_REPORT.md). The original author and audit packets, freeze receipts, actual correction patch, and corrected copy are retained separately. All accepted results are partial progress; no general aspherical equality, aspherical counterexample or novelty is claimed.

## Portable replay

Requires trusted Python 3.9+ and its standard library, with a trusted operating system. No network, external package, source paper or dataset is needed. Obtain the SHA-256 pins for PUBLIC_MANIFEST.json, verify_publication.py and mutation_tests.py from the draft PR description or another independently trusted receipt. Check the verifier's hash before executing it. A checksum stored only beside its payload is not an external trust anchor.

From any working directory:

    python -I -S -B /path/to/verify_publication.py EXPECTED_MANIFEST_SHA256 /path/to/packet
    python -I -S -B -O /path/to/verify_publication.py EXPECTED_MANIFEST_SHA256 /path/to/packet
    python -I -S -B -OO /path/to/verify_publication.py EXPECTED_MANIFEST_SHA256 /path/to/packet

The verifier enforces a closed inventory, file sizes, SHA-256 hashes, immutable nested manifests and freeze receipts. It rejects unlisted paths, links, special files, malformed inventories and wrong pins. It strictly replays the actual patch and compares all corrected report bytes. It executes captured, verified scripts in a private temporary snapshot, checking full computed receipts. It is an integrity and reproducibility tool, not a hostile-code sandbox, a race-resistant security boundary or a mathematical proof certificate.

Original Python assertions disappear under -O/-OO. The verifier therefore runs real child interpreters both directly and with an explicit assertion-preserving AST adapter at the selected optimization level. All original files remain unchanged. The audit's nested author subprocess is unoptimized. See ACCEPTANCE.md for the coverage distinctions and limits.

After authenticating the package, the separately pinned corruption suite runs:

    python -I -S -B /path/to/mutation_tests.py EXPECTED_MANIFEST_SHA256 /path/to/packet

It checks normal, optimized, doubly optimized and relocated execution, then deliberate changed/missing/extra files, links, bad pins, malformed paths and inventories, and manifest-laundered changes to frozen evidence. It never changes the original packet.

PUBLIC_MANIFEST.json lists every other payload file. Only authored mathematics, audits, correction patches, tests, and public source/verification metadata are included. Copied source documents, extracts, datasets, private sources and coordination material are excluded. Historical publication/review-status statements in immutable inner packets refer to their freeze time.
