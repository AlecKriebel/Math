# Compact-schema implementation transition

Status: **VERIFIED AFTER CORRECTION**

The first one-path smoke summary was produced before
`schema_specification_sha256` became a mandatory field.  That mismatch was an
implementation-version transition, not a semantic relation failure.  The
current smoke was regenerated and binds the exact specification bytes:

- specification: `primary/COMPACT_PROBE_SCHEMA.md`;
- SHA-256: `af4de0d81a6597e627b5c5bd3ee92c86b8c5bd85bfd4caf4e0315fec5107d7a4`;
- regenerated summary SHA-256:
  `0c8469402313746a151b85679a99f741ac19d35fe9bfa6fa28faa8e93ce2e0d2`.

The clean-room replay verifies this binding before decoding any relation.
No `FIRST_SEMANTIC_FAILURE.json` was produced for the shard codec.

The earlier compiler-only normalized-parent-ID mismatch remains separately
preserved at `quarantine/compact_probe_first_smoke_failure.json` (SHA-256
`fc55586fc49de121adf6a93a66fe26ecdda861513a381d7ad41aeb4abaeac1d4`).
It made no mathematical claim and is not reclassified here.
