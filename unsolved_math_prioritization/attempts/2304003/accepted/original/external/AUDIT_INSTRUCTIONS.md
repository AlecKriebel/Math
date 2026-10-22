# Independent audit instructions

Trust boundary: the reviewer must obtain the manifest and bootstrap SHA-256 pins independently of a potentially replaced packet. PINS.json is a convenient transport record, not a self-authenticating root of trust. The parent handoff records its SHA-256 separately.

1. Check bootstrap.py and MANIFEST.json against the externally trusted pins.
2. Run the authenticated bootstrap against the sibling public directory:

    python3 -I -B bootstrap.py ../public MANIFEST.json MANIFEST_SHA256 normal
    python3 -I -B -O bootstrap.py ../public MANIFEST.json MANIFEST_SHA256 O
    python3 -I -B -OO bootstrap.py ../public MANIFEST.json MANIFEST_SHA256 OO

Replace MANIFEST_SHA256 by the independently trusted 64-character pin. The outer and inner Python optimization levels are both tested. The bootstrap rejects additional entries, symlinks, malformed manifests, byte-count mismatches, and hash mismatches. It executes a memory snapshot of the checked verifier and supplies a memory snapshot of checked fixture bytes, rather than rereading those files after their hashes are verified.

The public directory must contain only the files listed in MANIFEST.json. TEST_RESULTS.json records actual positive, malformed-JSON, tamper, hostile-import, and nonroot read-only tests. Nonroot read-only tests include attempted writes that must be denied; merely observing mode bits is insufficient. test_harness.py reproduces those tests in newly created local temporary directories and writes its result to stdout. It does not access the network or source documents.

The software checks finite exact identities. Review REPORT.md separately for the infinite-family/analytic proofs, precise hypotheses, and unresolved original scope. A hash pass is not mathematical acceptance, and the packet deliberately has unresolved status.
