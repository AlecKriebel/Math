# External manifest anchor

Final family workflow completion: 100%. Original author proof-search record: 1/5; audit adds 0 turns. No substantive new approach.

The settled explicit public map is `MANIFEST.json`.

- SHA256: `2535f6fb265d1743400f76b90578fe1001ea7d98d9a9907ff4fa67ac0dbc6012`
- Bytes: 2113
- Explicit curated content files: 11
- The map excludes itself and this external anchor to prevent a hash cycle.
- All `private/**` bodies, extracts, temporary files and source-page renders are excluded.

Authenticate this map hash from the root's independently captured record, then run:

    python3 verify_manifest.py --manifest MANIFEST.json --manifest-sha256 2535f6fb265d1743400f76b90578fe1001ea7d98d9a9907ff4fa67ac0dbc6012

The root must also independently hash this anchor and the map itself if releasing them. The map cannot authenticate its own hash or its external anchor. The final parent message reports both metadata hashes so the root can add them to an outer explicit map.

All 29 selected original Git/disk files match at both ends. The exact proof SHA256 remains `6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`. The original head remains `c09ef9df8b1f4642be0396ba6343344be8fa25b0`.

Mathematical result: no unresolved mathematical gap found using the inspected Brendle v4 propositions and standard foundations. The journal publication record was verified; current journal main-text equivalence with v4 remains unverified. Priority/current-openness and publication decisions are deferred. No publication action was taken.
