# Additive artifact integrity correction

The first73-payload manifest, SEAL.json and verify_artifacts.py remain unchanged. The first integrity script incorrectly compared its content-only `{bytes, sha256}` pin with the runner's richer raw-stream record containing stat fields. It rejected with `Raw/result pin differs`; it did not identify changed bytes. The failure was reproduced and its exact argv, actual runtime, verifier hash, raw stdout/stderr and exit1 are preserved in ARTIFACT_VERIFIER_ATTEMPT_01_BINDING.json.

verify_artifacts_02.py compares bytes/SHA256 with the same two fields selected from the binding. It validates the additive SAFE_MANIFEST_02.json and SEAL_02.json. These retain every original payload and the original manifest/seal, plus this correction and the failed artifact-verifier replay. Original operational sources, final05 normal/-O results and all five runner attempts remain unchanged. All660 operational checks pass in each mode.

Use the additive manifest/seal and `python3 -E -S -B -P verify_artifacts_02.py` for final integrity verification. This correction changes no live operator, Root authority contract, scientific package, ready90 receipt, actual phase, publication/tracker outcome or source adoption. No real service was called. Bounded source authoring remains complete; independent Root review/adoption is still separate.
