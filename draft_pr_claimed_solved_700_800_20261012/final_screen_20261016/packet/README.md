# Checking the certificate

`CERTIFICATE.json` is the complete ascending 101-number inventory and own-row screen. `metadata_before_*.json` and `metadata_after_*.json` contain the complete alias queries and captured authenticated API responses. `queue_oids_*.json` binds every inspected queue to an immutable commit expression. `INITIAL_INVENTORY.json` is the byte-exact initial mapping source, whose SHA-256 is recorded in the certificate.

The externally pinned checker verifies the closed regular-file inventory, complete before/after coverage and equality, source query bindings, exact status parsing, all classifications, and all summary lists. With `--replay-blobs`, it also independently rereads each of the 90 complete source blobs through **read-only `git cat-file`**, verifies both SHA-1 Git OID and SHA-256, and re-extracts only the own row. It makes no network calls and writes nothing.

Run with Python 3 in normal or optimized mode:

```text
python3 -I -S -B /absolute/packet/verify_certificate.py /absolute/packet MANIFEST_SHA256 CHECKER_SHA256 /Users/alec/Documents/Math --replay-blobs
```

The manifest excludes itself and the checker. Supply their hashes from the parent's independent receipt. A self-provided manifest hash alone is not an external trust anchor.

`screen.py` is the byte-exact source used for the capture. Its original execution location was the parent directory of this sealed packet, `final_screen_20261016/screen.py`; its original relative program-root assumptions depend on that location. Use the checker for portable immutable-source reproduction. Do not blindly rerun the copied capture script inside `packet/`.

All assertions of completion concern this metadata screen only. No skipped mathematical work was reviewed, and no publication or merge action was performed.
