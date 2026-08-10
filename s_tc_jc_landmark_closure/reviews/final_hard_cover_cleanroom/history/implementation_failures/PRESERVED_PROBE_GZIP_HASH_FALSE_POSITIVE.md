# Preserved probe-stream hash false positive

Status: reviewer implementation failure; not a primary-stream failure.

The first clean-room probe audit compared each summary `sha256` field with
the bytes of the enclosing gzip file.  It therefore stopped before reading
any records and preserved
`probe_extension_first_failure.json`.  Independent inspection showed that
the summary hashes commit to the decompressed JSONL byte streams.  All four
logical-stream hashes match exactly:

- bindings: `87be8c6a4ec5725c453f7dae4a3c74828674701806a1959709c89f9ad7ae54fe`;
- graphs: `e65a4d5793424e92fbcc0548bdec0bf009dec1c9f80669733caf9ca8173d07fc`;
- polynomials: `f26df5a1484ba55b6812d569d10c47d9af68f164c58a336b94aae0a00706b052`;
- states: `c65820fcdb706f6eac0250b44d21237a04e9e8f49f01e45532edb3754cd2c99c`.

The failed artifact is retained to satisfy the fail-closed preservation rule.
The corrected auditor uses an explicit decompressed-stream hash function and
also records the physical gzip-file hashes separately in its final
certificate.
