# PR397 portable derivative replay

This is a **new narrow replay wrapper**, not an edit to the historical packet. Place `replay.py`, `candidate-binding.json` and `comparison-policy.json` at the archive root, with the24 frozen original problem files in the sibling `candidate/` directory. Their internal paths must be preserved. Alternatively pass an explicit candidate directory.

## Requirements and commands

The complete successful run used Python3.9.6, NumPy2.0.2 and SciPy1.13.1. Exact package pins are in `requirements-tested.txt`; Python itself must be supplied separately. The wrapper installs nothing. Python3.9 or later is required by its standard-library interfaces. Other versions may pass the same narrow checks but are not promised bitwise compatibility. The tested runtime is not an environment-image or universal reproducibility guarantee.

From the extracted archive:

    python3 -B replay.py

The default reads `candidate/` beside the wrapper and creates a new evidence directory under `replay-output/`. To select paths:

    python3 -B replay.py --candidate candidate --output replay-output/my-run

An output directory must not already exist and must lie outside candidate/. Each original component runs once in a separate fresh disposable copy. Failed runs retain their receipt, completed evidence and component standard output/error; the wrapper never automatically retries. A timeout also stops the run. The default per-component limit is180seconds, adjustable with `--timeout`.

Targeted guard tests require only the standard library:

    python3 -B negative_controls.py --candidate candidate --output replay-output/guard-tests

The retained final test used Python3.9.6 and passed171 guard controls:44 expected accepts and127 required rejections. The suite tests the production verifier/comparator and failure receipt path. It is not a new independent mathematical review.

## Immutable input checks

The wrapper verifies the exact24-file candidate inventory, every byte count, SHA256 and Git blob identity against `candidate-binding.json`. That binding records PR397, source head3705c5102b58c48e29991c61771978bf756a62e7 and the source snapshot hash. Binding and comparison-policy bytes are themselves pinned by literal SHA256 values in the wrapper. Symlinks, unexpected files/directories, missing files and altered proof/checker/output bytes fail before component execution. The frozen source programs, original manifests and historical receipts are preserved unchanged.

Each fresh copy is checked again before execution. Its expected output bytes are cached before its old script can rewrite any file. The selected original candidate is rechecked at the end. No shared checkout, branch, Git index, external service or package installation is changed.

## Exactly what comparisons permit

Turn2 output must match its frozen `CHECKS.json` **byte for byte**, SHA256 c98e5388c9496b25ce37b966a59bdd29ff25325940f72dee789dc2d72b94c1d9.

The two other JSON receipts require exact key sets, list lengths, types and values except for explicitly enumerated rules in `comparison-policy.json`:

- Exactly37 turn1 floating diagnostic paths and3 portable Gamma-CDF diagnostic-sum paths have individual absolute tolerances. Each tolerance is four times its previously observed concrete discrepancy; relative tolerance is zero. The table retains the historical value, observed value and discrepancy. This is not a tolerance for arbitrary floating fields or model parameters.
- The portable receipt's Python, NumPy and SciPy strings must equal the independently imported current runtime values. Their original historical values are checked too. Version fields are retained in the new receipt, not discarded.
- The portable input-control name and count must be exactly the documented public projection: `Public frozen author inputs verified`,8 files, with a boolean true pass flag. The original review's corresponding25-file control remains preserved.

Booleans cannot substitute for integers or floats. NaN, infinities, duplicate JSON object keys, missing/extra fields and all other differences are rejected. All pass/fail flags, integer counts, seeds, exact witnesses and theorem/model parameters remain exact. A known-path difference exceeding its narrow tolerance fails. A semantically identical turn2 output with changed whitespace also fails its exact-byte requirement.

The tested successful run has45 declared differences:40 numerical diagnostics,3 runtime strings and2 projection fields. Full actual records, comparisons and process logs are retained in `TESTED_REPLAY/`; `expected-replay-receipt.json` is the identical tested top-level receipt. `PORTABLE_DEFAULT_REPLAY/receipt.json` additionally records a successful default-layout run from an extracted-layout directory containing spaces. These are dated test evidence, not requirements that later timestamps match.

## Independent probability controls

`probability_controls.py` is copied verbatim from the sealed independent probability review (SHA25649c317995f30319d8d4d434c5096d4fa550edf0679fd3ea331ce55e48df1951c). `expected-independent-controls.json` preserves its prior output. The code is standard-library only and checks695520 cut-size pairs and2796678 assertions; the report explains their finite scope. To run it without overwriting package evidence, copy the script to a new working directory and execute that copy. It writes its JSON result beside its own file. This optional computation is separate from the three original components run by `replay.py`.

Neither these finite controls nor successful replay proves a universal probability theorem, historical novelty or the subjective status of an open-ended toy-model request. The analytic proof and source/priority assessments remain the mathematical evidence.

## Historical failure and repair limits

The old `REPLAY_ALL.py` remains byte-identical in candidate/. It fails in the tested environment at a strict hash comparison of old turn1 floating diagnostics; its later exact comparison of portable diagnostic sums is similarly nonportable. The new derivative addresses this specific issue with audited path-specific comparisons and exact structure/type guards. It does not claim a successful unchanged historical wrapper, recover omitted original private source material, broaden any theorem, or establish compatibility with arbitrary future numerical libraries. A failure in another environment is evidence to inspect, not permission to loosen the policy without review.

No third-party full text is included in this repair. All changes are authored support files. Extensive AI assistance was used in developing and testing this derivative; it is not independent human peer review.
