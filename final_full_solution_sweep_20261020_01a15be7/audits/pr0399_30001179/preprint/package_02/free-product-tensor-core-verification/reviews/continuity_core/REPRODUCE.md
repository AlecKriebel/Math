# Reproduction of this family audit's finite controls

Run the standard-library-only `independent_controls.py` with Python3 normally and with `-O`. Both outputs must equal the complete captured JSON in `INDEPENDENT_CONTROLS.normal.json` and `INDEPENDENT_CONTROLS.optimized.json`. The captured runtime is in `REPLAY_COMPARISON.json`; no third-party package is required. The script writes only stdout.

For each `source_mutations` entry in `NEGATIVE_CONTROLS.json`, replace the unique literal `old` string with `new` in a disposable copy of the independent checker. Run each disposable copy normally and with `-O`; each of the eight executions must exit nonzero at an explicit guard. The exact captured exceptions are retained in that JSON. Do not modify the canonical checker or original research files.

The historical original `verify_public_packet.py` was run normally, and its exact stdout/runtime are retained in `ORIGINAL_REPLAY.json`. Its `assert` guards make optimized mode unsuitable for claiming historical checks were executed. The11 frozen files were also independently compared to actual Git bytes at the pinned head; see `SOURCE_SNAPSHOT_CHECK.json`.

Finite combinatorics and exact identities are auxiliary controls. The continuous-field, measure-null and infinite-sector statements depend on the full analytic arguments in `INDEPENDENT_RECONSTRUCTION.md` and `REPORT.md`. The original primary report is cited by official URL/hash and reading scope in `PRIMARY_SOURCE_READING.json`; source bodies and renders are held privately and are not redistributed.
