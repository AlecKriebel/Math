# Validation scope

Run `python -B verify.py` from any working directory to check the exact inventory, byte counts, hashes, typed claim schema, attempt ledger and deterministic finite controls. Run `python -B selftest.py` for the adversarial checks. Only the Python standard library is needed; no network or downloaded program is used.

The mathematical checks use exact rational arithmetic. They cover the polar curvature identity and finite support samples, the positive-metric matrix identities, nilpotent weighted-shift telescoping controls, block-form inequalities, and finite diagonal-gap surrogates. They supplement the written proofs; they do not verify the boundary PDE, a microlocal representation, all geometric deformations, or a high-frequency coercivity theorem.

The self-test is required to pass in ordinary Python, `-O`, and `-OO`. It tests checksum corruption, extra and missing files, symlinks, rebound false solved and smooth-counterexample claims, a false curvature claim, boolean/integer type confusion, an unknown claim, duplicate JSON keys, non-finite numbers, and truncated JSON. False-claim payload hashes are deliberately updated, so rejection cannot be credited only to stale hashes. All semantic validation uses explicit exceptions, never `assert`.

A separate relocated copy has all files set read-only and its directory nonwritable. All three modes must reproduce the exact normal output without changing the payload. The self-test creates and removes only disposable temporary directories.

Expected final results: 4,455 exact controls; six successful original/relocated mode replays; twelve mutation cases, each rejected in all three modes (36 rejections). The final external validation receipt records the actual observed result. No independent audit is implied.

The manifest binds the source-free author packet but is not itself a signed trust root. Compare its SHA-256 with the separately reported freeze receipt. A party able to replace both executable code and all trusted hashes can change what any local verifier claims.
