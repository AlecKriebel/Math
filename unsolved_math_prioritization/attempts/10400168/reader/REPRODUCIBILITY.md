# Reproducing the checks and verifying the package

Use Python 3.10 or newer with only the standard library. The finite checker uses exact integer and rational arithmetic; it generates its groups, triangulations and examples algorithmically. No downloaded data fixtures or third-party packages are required. The checks were exercised with the Python version recorded in the original validation receipt.

From any directory, run the following commands, replacing the path to the public directory as appropriate:

```
python -I -B public/verify_package.py
python -I -B public/run_checks.py
python -I -B public/check_tamper_controls.py
```

The first command verifies canonical manifest encoding, the exact file and directory set, file sizes and SHA-256 hashes. It rejects symlinks and nonregular filesystem objects. It also verifies the original/public identity mapping and final audit/source acceptance bindings. To check an externally supplied manifest pin, add `--manifest-sha256` followed by the exact SHA-256 from the separate archive receipt.

The replay wrapper copies the payload to disposable directories. It executes the finite checker under normal Python, `-O`, and `-OO`, always with isolated-interpreter and no-bytecode flags. Every execution must return the retained exact output bytes and the expected 17,857 check count. An intentionally false explicit guard must fail in every mode. The wrapper additionally runs the original authored orchestration script in its own disposable copy; that script repeats the three-mode checks and guard probes and regenerates its output files. Thus one wrapper replay makes six finite-check executions and six negative guard probes. It verifies that the public tree was not changed.

The direct finite checker is [verify_examples.py](pass1_validation/verify_examples.py). Its detailed mathematical scope is described in [the validation report](pass1_validation/VALIDATION_REPORT.md). [CHECK_REPLAY.json](CHECK_REPLAY.json) records the wrapper replay. The tests are supplementary finite evidence. They do not replace the proof of the general trace identities or the published general defect-functor theorem.

## Original and public identities

[ORIGINAL_IDENTITIES.json](ORIGINAL_IDENTITIES.json) records each selected authored original's size and SHA-256 and the corresponding public copy's identity. Almost all copies are byte-for-byte. Two reports have limited public-edition adaptations: the historical source contract drops archival directions, and the final source-scope acceptance drops queue-publication recommendations. Their mathematical statements, acceptance, caveats and references are retained.

The nested [mathematical audit manifest](pass1_audit/MANIFEST.json) and [final source-scope manifest](pass1_scope/MANIFEST.json) are **original-input manifests**. In particular the latter pins the original source-scope acceptance text, not its adapted public edition. The `report` field in [the source disposition](pass1_scope/DISPOSITION.json) likewise refers to that original. [AUDIT_BINDINGS.json](AUDIT_BINDINGS.json) explicitly joins each acceptance pin to its original identity and its public identity. This preserves the reviewed original pins without claiming that a redacted edition has the same hash. The root [MANIFEST.json](MANIFEST.json) pins the exact files actually shipped.

The mathematical acceptance manifest was fixed at SHA-256 `ae7d65b3fda8741dc740e177b97af2a4d1edd6fab7f341cffcaba22b8433c4ad`. The final source-scope acceptance original was fixed at `ef7b9d186ae4a0f526ae1fadc1a39547d5fdf5b918a467cc1a919847070cef41`. These pins are checked before packaging. Neither hash alone certifies a mathematical theorem; they identify the reports whose reasoning is available for review.

## Adversarial controls and archive

[The tamper test](check_tamper_controls.py) creates only disposable copies. It tests changed bytes, same-size substitutions, missing and extra files, an extra directory, symlinks, a FIFO, unsafe and duplicate manifest paths, a manifest self-entry, wrong sizes and hashes, noncanonical JSON, duplicate JSON keys and a wrong external manifest pin. All 15 mutations must be rejected in normal, optimized and double-optimized execution, giving 45 rejection checks. [Retained control results](TAMPER_CONTROLS.json).

The archive contains only regular files under `public/`, with sorted paths, normalized ownership, mode 0444, timestamps zero and gzip timestamp zero. The archive is generated twice and compared byte-for-byte, restored to a disposable directory, checked against the exact file/byte inventory, and replayed there. The separate archive receipt pins both archive and root manifest, avoiding a circular self-hash.

Internal integrity checks cannot authenticate a maliciously replaced package whose verifier, manifest and all checks have been replaced together. Compare the archive or manifest against a trusted external receipt for that purpose. No source-document content or external dataset is needed to perform the package replays.
