# Preserved failed certificate attempt 000000

This attempt made no proof claim and produced no normalized proof. The strict
normalizer rejected the requested layout before parsing because its output
and report paths did not share a directory:

```text
e NORMALIZATION REJECTED: output and report must share a directory
```

The exact stdout, stderr, resource record, and empty run lock are preserved
in this directory. The producer was then corrected so that
`proof.normalized.rup.bdrat` and `normalization-report.json` share the
`proof/` directory. No frozen instance, theorem, source, test, review,
solver-result, or raw-proof artifact was modified.
