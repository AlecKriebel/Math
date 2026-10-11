# Reading and replay guide

Read SOURCE_SCOPE.md, LITERAL_COROLLARY.md, RESULT.md, then TURN_1.md through TURN_5.md. The five CURRENT_STATE_Tn files and manifests are chronological; CURRENT_STATE.json is the preserved zero-turn source gate, not the final status.

Run from this directory:

    python replay_author.py

This replays all five finite checkers byte-for-byte against their receipts, verifies historical manifest entries, and checks all five source PDF hashes if a sibling ../source directory is present. The public research packet does not include the raw PDFs; their primary URLs and hashes are in SOURCE_MANIFEST.json. A source check reported unavailable means precisely that the local PDFs are absent, not that their claims were reverified.

The final manifest binds all other public author files. Historical manifests and source-gate records are preserved byte-for-byte. AUTHOR_REPLAY.json records the completed local replay with all five source PDFs available. The controls are exact rational/integer tests, not numerical evidence for an unproved limiting law.

Interpretation and limitations: the quantitative author scope is the explicit finite-prefix M(D), while the primary report's infinite supremum is separately credited. The sharp finite-prefix growth and original broader question remain unresolved after five substantive turns. The latest preprint's long proof was not fully independently audited, and no novelty or literature-completeness claim is made.
