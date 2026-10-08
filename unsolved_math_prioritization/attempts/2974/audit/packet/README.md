# Independent Lefschetz-pencil audit

Read AUDIT_REPORT.md for the acceptance scope and JOHNSON_QUOTIENT_ADDENDUM.md for the stricter Johnson-module limitation and the intrinsic-index alternative. The universal problem remains unsolved here; the five-approach accounting is unchanged.

The original author freeze was preserved. AUTHOR_FREEZE_MANIFEST.json is a byte-for-byte copy of its external manifest, bound to the separate trusted hash recorded in the report. Source metadata and public URLs are included, with no source bodies.

## Reproduce

Python 3.9+ and the standard library suffice. For standalone independent arithmetic:

    python -B independent_checks.py
    python -B -O independent_checks.py
    python -B -OO independent_checks.py

For the full author replay and mutation suite, supply the original directory containing packet/, FREEZE_MANIFEST.json, and source_free_packet.tar.gz:

    python -B replay_and_mutations.py --author-root /path/to/author/directory

The harness requires actual UID and EUID 1000. It performs tests on disposable copies only, creates temporary directories, emits JSON to stdout, and verifies that original inputs remain unchanged. The standalone checker writes only to stdout. The full harness runs both checkers in normal, -O, and -OO modes using read-only copies and a read-only current directory.

The audit's separate external manifest and archive hash bind the final audit deliverable. Hashes are integrity pins, not signatures or proof certificates. The report discloses the odd-prime mutation that the author's limited finite models do not detect; the independent even-modulus control rejects it.
