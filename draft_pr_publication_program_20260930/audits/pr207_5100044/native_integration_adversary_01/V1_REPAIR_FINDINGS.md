# Frozen V1 required operational repairs

UTC: 2026-10-17T00:23:16.190934+00:00
Audit completion estimate: 55%.

Reviewed helper: native207.py, 31546 bytes, SHA256 8dcdda540bc8ea083feb5776227d3da971b1d9aca0b39aa84a58d7b0f1c7c910. All eleven explicit source files matched PREPARATION_MANIFEST.json 2280/SHA256 34ff0d31c6726c45f421ac5c4eabb2b8286889d95541519db691a061a7ea6c11 and PREPARATION_SEAL.json 768/SHA256 51fb59ed409fb231b1396f180ad629448dee60eeb8059aa4739292cc6ac27c0a. New helper read in full from an owned pinned copy. Preparer test code/results have not been read.

1. **Medium, required repair: QUEUE omission is accepted.** inputs lines126–129 enforce native22, original archive20 and five views, but do not require QUEUE. state lines226–227 apply own-row/foreign-line verification only if QUEUE was selected. Independent tiny fake-native fixture removes QUEUE from an otherwise valid merge95 manifest; candidate creation and full verification succeed, and the resulting native tree retains the exact queued0/5 own preimage, while phase publication facts claim 34 published. Require QUEUE selection in both phases and document it; completion100 already requires the whole QUEUE body unchanged when selected.

2. **Low, required repair: receipt byte count permits Boolean alias.** inputs line152 compares pin dictionaries using Python equality without strict bytepin validation. A selected one-byte test-only role event with receipt bytes=true is accepted as bytes=1. Apply bytepin to each role identity before body equality. No claim is made that a fake event's semantics are actually true; Root remains the explicit interpreter of heterogeneous event receipts.

Reproduce under Python -E -S -B -P with integration_controls_v1.py using the owned pinned frozen_v1 sources. V1_INDEPENDENT_CONTROLS.json records one positive and two unexpected acceptances. All fixtures are small owned temporary files and in-memory native objects. No network, Git, shared-view writes, actual event, actual acceptance or global pointer was created. Root and preparer were notified and frozen repair pins are required before clearance.
