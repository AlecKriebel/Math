# Standalone verification package

This package accompanies Version 0.2 of *Positive Recurrence of Bimolecular Weakly Reversible Stochastic Reaction Networks with a Single Linkage Class*.

## Install and run

```bash
python -m pip install -e .
./reproduce.sh
```

Tested with Python 3.13.5. The package requires Python 3.11 or newer and has no runtime third-party dependencies.

The verifier distinguishes:

- exact symbolic/combinatorial checks: falling-factorial identities, channel marking, scalar-envelope branch conditions, and a deterministic finite top-complex atlas;
- floating numerical calibrations: none;
- fixed-seed random stress tests: four-species top-complex classifications with seed `20260806`, used only for adversarial testing and never as proof.

`verification_report.json` is canonical JSON serialized with sorted keys and fixed separators. It excludes elapsed times, timestamps, temporary paths, cache files, and platform-specific formatting. `reproduce.sh` generates the report twice and requires byte-for-byte equality.

The universal theorem is proved in the manuscript. These checks are not a substitute for the proof.
