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
  .venv/bin/python work/rank_upper_certificates/mutation_tests.py
```

The release replay must not use `--skip-base-recompute`.
