# Reproduce instability-family audit diagnostics

Run from `/Users/alec/Documents/Math` with existing `/usr/bin/python3` and SymPy 1.14.0. No installation is required.

```sh
/usr/bin/python3 draft_pr_publication_program_20260930/audits/pr29_30004186/instability_family/adversarial_checks.py
```

Expected: PASS, 66 exact assertions and six rejected false substitutes. This rewrites only the new family receipt. It is finite diagnostic evidence; universal conclusions rest on the written proof.

Unchanged original replays already ran in three isolated `ignoredtmp/replays` directories. Their metadata and receipt comparisons are in `replay_submitted.json`, `replay_reviewer.json`, and `replay_archived_submitted.json`. To reconstruct those after ignoredtmp cleanup, use `original_blob_manifest.json` to extract the exact Git blobs at assigned head 5ac4a57e08dd72a6f16768f2288b9c0349999431 into a fresh ignoredtmp directory and execute only the original scripts there. The submitted scripts write their deterministic receipt next to themselves, which is why no canonical original folder was executed.

`original_blob_manifest.json` gives all 17 immutable original files, byte counts, Git blob IDs and SHA256 hashes; `source_receipts.json` gives primary-source URLs and PDF/text hashes. The self-excluding family manifest hashes retained audit files and excludes itself and ignoredtmp.
