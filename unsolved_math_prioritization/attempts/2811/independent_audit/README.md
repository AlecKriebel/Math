# Audited surface-immersion partials: KP-3.13

The exact frozen author packet is accepted unchanged as elementary conditional work. Problem 2811 remains **unsolved, 3/5 substantive approaches**. Read AUDIT_REPORT.md for the independent all-size proof review, source scope, and limits. AUDIT_STATUS.json gives the current disposition. SOURCE_AUDIT.json contains public verification metadata only. BINDING.json pins the exact three enclosed original author artifacts.

## Safe reproduction

Use Python 3.10 or later; standard library only, no network or additional packages. Before executing any extracted script, independently compare this ZIP's byte count and SHA-256 with the separately delivered external manifest. Inspect archive member paths before extraction into a fresh directory. Do not trust an executable to authenticate its own replacement.

In the freshly extracted directory, run:

    python3 -B verify_audit.py --manifest-sha256 HASH

Use the `internal_manifest_sha256` from the independent external manifest as HASH. The verifier rejects unlisted, missing, symlink, or directory payloads, authenticates the original author artifacts, and replays both normal and optimized checks. It runs entirely from the safe packet. An internal manifest cannot authenticate itself.

For the finite controls alone, run:

    python3 -B independent_checks.py
    python3 -B -O independent_checks.py

Both outputs must match INDEPENDENT_RESULTS.json byte-for-byte. These runs authenticate and unpack the original author ZIP into temporary directories, reproduce the author's controls, execute independent controls, and challenge the author verifier with twenty corruption cases per mode. They do not reconstruct a hyperbolic manifold or prove the universal problem.

The original pending-audit text remains as historical content. This independently bound acceptance report records the completed audit without rewriting that history. No mathematical repair or derivative author packet is needed. Source documents, source extracts, dataset contents, and private coordination files are excluded. No publication or repository changes were performed by this audit.
