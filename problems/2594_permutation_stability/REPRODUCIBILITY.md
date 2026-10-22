# Reproduction and immutable history

Requirements: Python 3 standard library only. No floating-point spectral package, theorem prover, external data, network request or installed third-party package is needed by the checkers.

From this directory, for i=1,…,5, run `python turni/verify_turni.py` and compare stdout byte-for-byte with `turni/TURN_i_CHECKS.json`. The explicit commands are:

    python turn1/verify_turn1.py
    python turn2/verify_turn2.py
    python turn3/verify_turn3.py
    python turn4/verify_turn4.py
    python turn5/verify_turn5.py

Assertion totals in order: 591531, 478463, 237292, 223719, 102643. Combined total: 1633648. These count actual executed exact assertions, with overlap between some turn-specific algebra universes. The counts do not certify the unrestricted problem.

`FINAL_AUTHOR_MANIFEST.json` binds every other public file. Historical `CHECKPOINT_1_MANIFEST.json` through `CHECKPOINT_4_MANIFEST.json` bind the files present at those earlier freezes, and each turn has its own manifest. All entries use raw UTF-8 bytes and SHA-256. None of the historical proof, receipt, source-gate, state, log, or manifest bytes was overwritten.

Consequently the top-level `TURN_STATE.json` still says one turn consumed: it is the original checkpoint-1 historical state. Later turn directories have their own frozen states. `CURRENT_STATUS.json` is the authoritative final author disposition, five turns exhausted and original unresolved, pending independent review.

Source PDFs, screenshots and raw imported records remain separate reading inputs. Their hashes identify the exact consulted versions but those files are not included in this packet. Executable outputs and local upload/remote-verification receipts are also excluded unless explicitly listed in the final public manifest.
