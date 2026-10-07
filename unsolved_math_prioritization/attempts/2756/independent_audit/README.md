# Kirby 2.8 independent acceptance package

This package independently accepts the exact frozen author work as a partial reduction, not as a complete solution.

- AUDIT.md contains the mathematical, source, scope, and artifact audit.
- EXACT_ACCEPTANCE.json identifies the accepted immutable author ZIP and external manifest.
- PIN_VERIFICATION.json records the 45 source, corpus, and artifact checks.
- BUILDER_REPLAY.json records 24 independent relocated author-builder checks.
- VALIDATOR_REPLAY_NORMAL.json and VALIDATOR_REPLAY_OPTIMIZED.json record the independent validator's 19-case suite in both harness modes.
- VERIFY_ACCEPTED_AUTHOR.py verifies the exact author ZIP and external manifest supplied as its two command-line arguments. It does not check mathematical proofs.
- The original author ZIP and its external manifest are included unchanged under original/.

Run the validator with Python 3, followed by the paths to the original author ZIP and external manifest. It can be run with -O from any working directory.

The scope remains partial, 3/5 approaches. No n >= 4 solution, universal finite generation, universal finite presentation, or novelty is certified. The frozen author's pending-audit fields record its historical state; this separate package supplies the acceptance.

Only authored analysis, reproducibility code, and verification metadata are included. No copied source documents, source text extracts, dataset records, or private coordination files are included.
