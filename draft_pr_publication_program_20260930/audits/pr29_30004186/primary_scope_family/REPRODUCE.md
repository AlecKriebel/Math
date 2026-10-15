# Reproduce the independent audit controls

Run from `/Users/alec/Documents/Math` with the existing `/usr/bin/python3` and SymPy1.14.0. No installation, queue generator, database write, branch change or original artifact edit is needed.

```sh
/usr/bin/python3 draft_pr_publication_program_20260930/audits/pr29_30004186/primary_scope_family/reproduce.py
```

The reproduction script checks the retained family manifest, immutable source-first seal, original Git blobs, cached pinned raw bytes and live readonly SQLite context, runs the independent controls in no-write mode, and runs three unchanged legacy scripts in a fresh ignored temporary directory. It prints results without modifying retained receipts. The foreign PDFs are deliberately not redistributed; SOURCE_RETRIEVAL_RECEIPT.json supplies URLs, byte hashes and retrieval times for independent retrieval. UPSTREAM_TREE_RECEIPT.json records the actual fetched immutable-tree metadata; reproducing against cached bytes does not make a new worldwide literature or historical absence claim.

Expected: family manifest and original candidate/seal match, raw prior join is `{}`, context SHA256 is `759ed8f6518e7a61a2356296cdc080f951f41bc93ca448182f1ce2143cda5a7b`, fresh controls16/rejected mutants12, legacy checks20/20/135. Reproduction does not prove PDE evolution, authenticate historical model/effort/query logs, or establish novelty.
