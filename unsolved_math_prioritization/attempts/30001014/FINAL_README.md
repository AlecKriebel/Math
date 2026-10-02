# Reading and replaying the five-turn packet

Read RESULT.md and SOURCE_SCOPE.md first, then the five proofs in order. TURN_1.md supplies the literal finite-spectrum correction. Turns2–5 explicitly investigate the added infinite-spectrum restriction. The latter remains unresolved5/5; it is not silently identified with the printed unrestricted assertion.

Run in this directory:

    python verify_turn1.py
    python verify_turn2.py
    python verify_turn3.py
    python verify_turn4.py
    python verify_turn5.py

Each stdout must equal its TURN_n_CHECKS.json receipt. The checkers use only the Python standard library and total194,884 exact finite assertions. They are not simulations of nonminimal tensor norms and do not certify the analytic spectrum arguments.

FINAL_AUTHOR_MANIFEST.json binds every other public file. All earlier manifest entries remain byte-for-byte valid. Source URLs, editions, byte counts and hashes are in SOURCE_MANIFEST.json; raw PDFs/imports are separate reading inputs and are not redistributed. SOURCE_ADDITION_T5.json records the final turn's self-contained norm-gap argument and its classical framework rather than inventing a new external source.

CURRENT_STATE_T5.json is the final author snapshot. Earlier state files and the first-turn review request are historical. Full independent review comes after this freeze; any correction must be additive. No further author turn or novelty certification is asserted.
