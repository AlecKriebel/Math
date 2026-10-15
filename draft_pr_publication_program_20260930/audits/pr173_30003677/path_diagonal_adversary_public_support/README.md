# Standalone public support for the PR173 path/diagonal audit

This additive package exports only the audit family's own safe exact controls and their receipts. It does not modify or replace the original private seals or inventory, and it does not authorize publication.

The baseline checks cover 20,016 finite competition instances, 25,176 protected-path witnesses and 159,474 explicit checks per execution. The driver runs the baseline ordinarily and with Python optimization, then runs nine false semantic variants in each mode. Each false variant must exit with an explicit `VerificationFailure`. The baseline itself also checks rejection of all nine variants.

From this directory, reproduce all twenty executions with:

```sh
python3 -B run_public_controls.py --output /tmp/pr173_path_controls_reproduction.json
```

The output path can be any writable location. Reproduction does not depend on the original repository, network access, external sources, private files, or copied original checkers. It reads the two included scripts and writes only the requested aggregate receipt.

For direct baseline executions:

```sh
python3 -B explicit_controls.py
python3 -B -O explicit_controls.py
```

For example, this deliberately false endpoint-only variant must exit nonzero in both modes:

```sh
python3 -B explicit_controls.py --variant endpoint_only
python3 -B -O explicit_controls.py --variant endpoint_only
```

Dependencies are Python 3 and its standard library only: `argparse`, `collections`, `datetime`, `fractions`, `hashlib`, `itertools`, `json`, `pathlib`, `platform`, `subprocess` and `sys`. The export was executed with CPython 3.14.6 on arm64 macOS. Earlier Python versions were not tested. No package installation, random seed, environment variable, source-data file or external program is required.

The nine variants are `endpoint_only`, `open_ball`, `voronoi`, `parallel_collapse`, `parity_plus_one`, `budget_without_rate`, `seed_divergence_without_floor`, `uniform_identity_without_uniform_root`, and `log_bound_replaced_by_size`.

`receipts/OWN_ORIGINAL_RUNS.json` contains the twenty actual own runs from the original sealed audit, with safe baseline output bodies and negative exception payloads. The two `original_baseline_*.json` files are byte-for-byte copies of the original own baseline standard output. Absolute traceback locations are excluded from negative records. `receipts/PUBLIC_REPRODUCTION_RUNS.json` records twenty new actual executions of the exported standalone scripts. Reproduction timestamps, interpreter fingerprints and stderr hashes may vary by machine or extraction directory. The control-source hash, exact baseline output, totals and semantic rejection payloads should remain the same.

These are finite deterministic and arithmetic controls. They do not prove the configuration-model local limit, nonexplosion theorem, full stochastic occupation result, source scope, or novelty. See `REPORT_REFERENCE_MAPPING.md` for evidence exported versus evidence retained privately, and `SAFE_IDENTITIES.json` for sanitized provenance fingerprints. Every public-support file is explicitly allowlisted in `PUBLIC_ALLOWLIST.json` and listed in the recursive inventory. The final seal fingerprints the inventory; its own hash is supplied separately to the parent audit to avoid cryptographic self-reference.
