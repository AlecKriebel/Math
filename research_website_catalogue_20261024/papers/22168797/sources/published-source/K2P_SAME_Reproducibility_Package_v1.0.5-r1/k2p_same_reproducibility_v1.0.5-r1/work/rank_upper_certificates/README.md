# Four-port exact generic-rank upper certificates

This directory closes the rank-upper gap left by sampled Jacobian minors.
The sampled/exact minors prove lower bounds; the polynomial vector fields here
prove the matching upper bounds.

Primary artifacts:

- `PROOF.md`: mathematical proof and finite census.
- `syzygy_upper.py`: universal exact polynomial-field construction.
- `rank_upper_coverage.json`: exact-one coverage of all 4,379 descriptors.
- `exception_syzygies/`: 75 primitive representative certificates.
- `verify_rank_upper_certificates.py`: full fail-closed replay.
- `mutation_tests.py` and `mutation_report.json`: adversarial tests.
- `rank_upper_replay.json`: successful full replay result.

Release replay from the project root:

```sh
PYTHONPATH=package/referee/k2p_offline_sweep_portable/atlas:work/rank_upper_certificates \
  .venv/bin/python work/rank_upper_certificates/verify_rank_upper_certificates.py

PYTHONPATH=package/referee/k2p_offline_sweep_portable/atlas:work/rank_upper_certificates \
  .venv/bin/python work/rank_upper_certificates/mutation_tests.py \
  --output /tmp/k2p-rank-upper-mutations.json
```

The release replay must not use `--skip-base-recompute`.
Mutation output is caller-owned and must be outside the project tree.  The
maintainer-only authoritative reseal uses `--allow-authoritative-output` with
the exact canonical `mutation_report.json` path.  Both the mutation runner and
the rank verifier remove any validated pre-existing output before fallible
work, reject symlink/hardlink/input collisions, and publish success artifacts
only by atomic replacement.  The mutation suite first verifies both stored
manifest encodings against all 94 current proof/code inputs and runs the full
production verifier directly on that authoritative package, requiring its
new output to match the stored 4,379-descriptor replay byte-for-byte.
Fallible mathematical imports occur only after safe output removal, and an
isolated missing-dependency control verifies that stale PASS output cannot
survive an import failure.  Disposable
resealing is used only after this baseline passes.  `mutation_report.json` is
bound by the outer release lock rather than its own nested manifest, avoiding
a circular self-commitment.
