# Checker portability record

13 October 2026. These are packaging edits only. No new mathematical pass, source pass, theorem, or test range was added. The accepted proof, accepted independent audit, original result JSON files, and original source metadata are preserved byte-for-byte.

## Changes to the two checkers

- Converted all 18 `assert` statements in `check_claim.py` and all 9 in `audit/independent_checks.py` to calls to a small `require` function. It explicitly raises `AssertionError` on a failed condition, so optimization cannot remove the checks. The original condition expressions and existing failure details are unchanged. Assertions without a detail now identify their original line number. Existing tuple failure details are evaluated at the check call; they have no side effects in these checkers.
- Added an optional `--output` argument. Both scripts always print their JSON results. They write a UTF-8 JSON file only when an output path is explicitly supplied, rather than overwriting the preserved result beside the script on every run.
- Added the standard-library `argparse` import and the explicit output encoding. The proof checker's introductory note now points to this record and no longer assumes SymPy is preinstalled.

The algebra, exact arithmetic, matrices, finite fields, test bounds, and result schemas are unchanged. No original `assert` statement remains in the distributed checkers. The new manifest verifier likewise uses explicit checks rather than `assert`.

## Exact checker identities

| File | Version | Bytes | SHA256 |
| --- | --- | ---: | --- |
| `check_claim.py` | Original accepted input | 7824 | `4739bcaad564022accee18573a88c986cd4304f4aa88dd974cde77fbdb2e6e0d` |
| `check_claim.py` | Portable reader | 8845 | `2dc54f73ad1d3bdb4f5dccf91dd056711fae6d1e85dac078fc5763b03ad0013c` |
| `audit/independent_checks.py` | Original accepted input | 7657 | `b1eb845c335343b58fd5f6660d21aa51376ae9f8d11018d1b9862079c9a2eaf8` |
| `audit/independent_checks.py` | Portable reader | 8262 | `2a094202c0d7452bf6fdcecc59c94389702a069fc8f77c3d1058ba443a287700` |

The separate packaging report records mode-by-mode reruns, comparison against the preserved output bytes, representative forced-failure tests, and exact reader pins. These reruns check packaging equivalence; the mathematical acceptance remains the scope stated in the proof and audit.
