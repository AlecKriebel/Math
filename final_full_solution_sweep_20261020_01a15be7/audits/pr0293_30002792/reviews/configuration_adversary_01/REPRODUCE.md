# Reproduction and custody

Use Python 3.8 or later and its standard library, from this directory.

1. `python3 original_control_frozen.py --proof FROZEN_PUBLIC_TURN_2.md > ORIGINAL_CONTROLS_REPRODUCED.json`
2. `python3 independent_controls.py`
3. `python3 verify_artifacts.py`

The first output must reproduce 3888 assertions and proof hash `56d7aee2dbb567f1574952bfe905b5407c0f0b06ec60e4b53b72acda48c245e1`. The independent default output must report 59,535 exhaustive configurations, 125,930 assertions, 24 crosschecks of the original examples, and record-stream digest `0f7a69ad8b6507feaf4108c7ad5b8eba50d8850ac1a6f1c285657a7bc04e7c52`.

The elapsed runtime field varies between machines. Re-running changes the output JSON's byte hash when that field changes, so the final custody-manifest verifier will then correctly report a changed result file. To check original custody, run the verifier before replaying. The independent script hash, configuration digest, counts, and mathematical results are stable.

An optional `python3 independent_controls.py --maximum-size 6` reproduces the larger completed execution, but it is not required for the retained core audit and takes longer. It writes the same output filename; preserve a copy beforehand if desired. The original size-six aggregate was overwritten by the final default replay, as explicitly documented.

The preserved source PDFs were retrieved directly from the two primary URLs on 2026-10-21 UTC. `sources/SOURCES.json` records their hashes and selected extracted PDF pages. The primary source originals are not modified by these commands.

The final SHA256 manifest includes all retained files except `MANIFEST.json` itself. It intentionally excludes no report, source extract, code, result, or log.
