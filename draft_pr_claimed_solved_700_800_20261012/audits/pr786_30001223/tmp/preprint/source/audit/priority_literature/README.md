# PR786 priority literature packet

Actual RAM staging:
 /Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr786_30001223/tmp/priority_literature

Start with PRIORITY_REPORT.md and VERDICT.json. INDEPENDENT_INITIAL_POSITION.json and PROVISIONAL_FINDING.json preserve the pre-peer positions. PEER_CHALLENGE.md records the later authorized challenge. SOURCE_COMPARISONS.json gives actual-body locators and limits; QUERY_LEDGER.json gives76 queries in20 batches. Fetch receipts preserve exact body hashes, not full third-party paper bodies. AUTHOR_METADATA_RECEIPTS.json and CITATION_CATALOG_RECEIPTS.json are discovery metadata, not theorem evidence.

INPUT_RECEIPTS.json binds all41 original candidate files plus five authoritative intake/gate records. Their base is this folder's parent tmp workspace. The checker validates their exact original-tree inventory, each SHA256/length, all41 recorded Git blob identities, complete selected/prior hash and immutable head/gate eligibility. It also checks exact project-authored peer snapshots. The custody result certifies byte relationships, not mathematical correctness, publication priority or current remote PR state.

FROZEN_MANIFEST.json hashes every other packet file except these two explicit exceptions:

* FROZEN_MANIFEST.json: its own bytes are bound by a caller-supplied external SHA256.
* EXTERNAL_PIN.txt: convenience copy only, excluded to avoid a cycle and required to equal the caller-supplied external pin exactly.

Obtain the expected pin from the parent's trusted message/receipt. Do not derive trust merely from EXTERNAL_PIN.txt. Use the reviewed checker (its digest is supplied externally as well). No asserts, network, writes or imports of bundled code are used during verification.

From this directory, normal invocation:

    python3 -B verify_custody.py --expected-manifest-sha256 EXTERNAL_TRUSTED_PIN --input-root ..

Optimized invocation:

    python3 -O -B verify_custody.py --expected-manifest-sha256 EXTERNAL_TRUSTED_PIN --input-root ..

Absolute --root and --input-root arguments are supported. No package installation is needed. CUSTODY_TEST_RESULTS.json identifies its tested provisional manifest and verifier pin; after recording those controls, the final packet manifest is regenerated and both normal/-O final baselines are run. This avoids pretending that a pre-receipt manifest is the final packet.

The only full third-party-body fetches in this route were in memory and were not retained. Test copies are only in owned sibling priority_literature_scratch. Final packet is flat and contains no third-party PDF/image bodies. No Git, queue, source proof, external account or public posting changes were made by this worker; canonical/durable preservation belongs to the parent.
