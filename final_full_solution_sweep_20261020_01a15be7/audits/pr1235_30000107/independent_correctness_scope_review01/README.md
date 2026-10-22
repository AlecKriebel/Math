# Independent correctness and scope review

The source-free authored review is `REVIEW.md`. The additional affine consequence discovered during this review is written separately in `AFFINE_ADDENDUM.md`; it awaits an independent challenge before promotion. Neither document supplies priority or package-publication approval.

The new standard-library checker is `verify_independent.py`. Run it with Python3 normally, with `-O`, and with `-OO`; no third-party library or solver is required. The corresponding actual outputs are `normal.json`, `O.json`, and `OO.json`, bound by `reproduction_receipt.json`. Essential small mathematical witness/table data are embedded in the checker, independently of any author program or unavailable historical certificate file.

`original_identity_receipt.json` binds the full original integer-point question and the pinned catalog statement hash. `fresh_catalog_receipt.json` records the initial numeric-grid GWS read. `source_inspection_receipt.json` records fresh primary-source retrieval and page inspection without copied source content. `pinned_PR_receipt.json` binds all eight added exact-head files and the unchanged-QUEUE scope.

`PUBLIC_MANIFEST.json` hashes the authored review artifacts. `CLOSED_DIRECTORY_SEAL.json` inventories every regular file in this review directory, including nested manifests and private retained inputs, excluding only its own exact path. It is an internal provenance inventory, not permission to distribute its private members. The `private/` folder is ignored by Git and contains source, policy, catalog and SQL bodies retained solely for the internal audit. No public file copies those bodies.

The source statements, old audit claims and numerical discovery history remain untrusted inputs until checked in the new review. No historical test receipt is presented as a fresh execution. No Git/index/refs, root cursor, remote service state or other research folder was modified.
