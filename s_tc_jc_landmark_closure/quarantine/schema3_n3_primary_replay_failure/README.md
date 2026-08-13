# Preserved schema-3 n=3 primary replay failure

Status: **FALSE AS A GRAPH-BOUND CERTIFICATE**

At 2026-08-10 after merging the four disjoint root shards, the first exact
primary replay failed while rebuilding a stored strict-open-cube sign
certificate.  The terminal census is therefore not promoted.

Exact command:

```bash
../.venv/bin/python primary/verify_hard_cover_artifacts.py \
  primary/certificates/hard_cover_schema3_n3_full_summary.json \
  --output primary/certificates/hard_cover_schema3_n3_full_replay.json
```

Observed first traceback endpoint:

```text
primary/verify_hard_cover_artifacts.py, verify_run
assert rebuilt_sign == published_sign
AssertionError
```

The merged summary SHA-256 is
`4b45107251bd3c3296b1badf33123ef434d4510a60463db5baf45c31b4199854`.
No certificate or verifier bytes were changed before recording this failure.
The next step is to identify the exact state and determine independently
whether the stored sign is false, the replay selected a noncanonical proof
algorithm, or shard merging corrupted provenance.

The first mismatch was subsequently identified as JSON representation only:
the exact regenerated sign proof used tuples while the stored JSON used
lists.  After normalizing that representation, replay advanced and exposed a
second, substantive graph-to-polynomial mismatch at the assertion
`not source and actual == stored polynomial`.

The substantive failure was traced to caching a sparse Fourier descriptor by
`(selected_port_count, standard_mixed_code)`.  Distinct rooted presentations
with that common mixed code can have different rooted arc-variable orders.
The first exact graph witness and polynomial hashes are recorded in
`../descriptor_cache_scope_failure/README.md`; the failed streams are
quarantined there.  The active producer instead binds the descriptor to the
exact rooted graph ID and normalizes zero-sum split complements.  This file
remains the chronological record of the first replay failure and must never
be consumed as an active theorem certificate.
