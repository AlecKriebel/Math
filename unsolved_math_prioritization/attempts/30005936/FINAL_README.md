# Replaying and reading the frozen packet

Start with RESULT.md and SOURCE_SCOPE.md, then read TURN_1.md through TURN_5.md in order. FINAL_REVIEW_REQUEST.md identifies the analytic/source pressure points. The final snapshot is CURRENT_STATE_T5.json; earlier state and manifest files remain immutable history.

Run, in this directory:

    python verify_turn1.py
    python verify_turn2.py
    python verify_turn3.py
    python verify_turn4.py
    python verify_turn5.py

Each stdout must equal the corresponding TURN_n_CHECKS.json exactly. The five receipts total99,505 assertions. They are exact finite algebraic controls and do not replace the analytic SPDE proof.

FINAL_AUTHOR_MANIFEST.json records byte counts and SHA-256 hashes for every other public file. Earlier *_MANIFEST.json files record nested historical snapshots; all their listed files retain the same bytes. Source PDFs are identified by URL, byte count and hash in SOURCE_MANIFEST.json and SOURCE_ADDITION_T*.json, but are not redistributed. The primary source was read in full for the relevant contribution and visually checked at the exact source/BCU theorem pages. Retrieval qualifications for Gyöngy's original spatial theorem and Mueller's original1991 paper are explicit.

This is a five-turn author packet awaiting independent review. It supplies a scoped negative mean-square subquestion and positive bounded-test theorems. The full original broad question remains unresolved5/5. No further author turn, novelty certification, raw source redistribution, or full-question resolution is asserted.
