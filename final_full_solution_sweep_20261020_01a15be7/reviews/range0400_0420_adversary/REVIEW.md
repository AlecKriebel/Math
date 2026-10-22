# Independent adversarial review of PRs 400–420

Completed 2026-10-21 UTC. Review completion estimate: **100% of this assigned classification and publication-correspondence review**. This is not a percentage estimate for proving any underlying mathematical problem.

**Verdict: no disposition blocker or missed eligible full-solution claim found in PR400–420.** Accept the 19 explicit non-`claimed_solved` exclusions, PR415's missing-status/no-mathematical-claim exclusion, and PR411's already-published/correctly-recorded exclusion within the scope below.

## Rules and scope

I applied the sweep's `CLASSIFICATION_POLICY.md` and the user's exact eligibility rule. A genuinely corresponding explicit non-`claimed_solved` status excludes the problem entirely; a missing status requires reading the actual claim. Merged state is not publication evidence. I did not reopen proof correctness, novelty, priority, present openness, or prior referee conclusions for excluded/already-published results.

The work used read-only Git object comparisons, fresh GitHub metadata, read-only Google Sheets reads, public Zenodo reads/downloads, and archived primary-source text. I made no PR, Zenodo, Sheet, Git index, Git ref, commit, branch, or provider mutation. Substantive review artifacts are confined to this dedicated folder. A helper import briefly generated Python bytecode for `pinned_scope_check`; that generated cache was cleaned up and the review harness now disables bytecode generation. No scientific files were changed outside this folder. No outreach, external comments, or messages to other researchers were prepared or sent.

## Complete range coverage

The fresh GitHub metadata for all21 PRs agrees with the sweep's exact heads, bases, bodies/body hashes, and states. Each actual complete pinned `base...head` comparison agrees with the cached path list, cached file count, and live `changed_files` count. All added canonical QUEUE rows agree with the cached row text. There are **520 path observations** across the range and **469 distinct Git blobs**, independently SHA-256 hashed in `ALL_PINNED_BLOB_INPUTS.json`.

For all19 explicit exclusions, the changed own row is unique in both the added-row set and the full branch-head queue, its numeric ID matches the PR/result folder, and its source line and status match the disposition. The actual paths contain only the corresponding attempt/custom folder and canonical queue. No unrelated added row was used to exclude a claim. Their 420 cached per-file blob SHAs all match the branch tree. PR411's intentionally different cache schema is addressed separately below.

| PR | Own problem ID | Actual corresponding status | Complete changed paths | Disposition upheld |
| --- | --- | --- | ---: | --- |
| 400 | 30000997 | unsolved | 49 | Explicit exclusion |
| 401 | 30001568 | already_solved | 23 | Explicit exclusion |
| 402 | 30001957 | already_solved | 8 | Explicit exclusion |
| 403 | 30006342 | already_solved | 18 | Explicit exclusion |
| 404 | 30002136 | unsolved | 31 | Explicit exclusion |
| 405 | 30002637 | unsolved | 22 | Explicit exclusion |
| 406 | 30003786 | already_solved | 23 | Explicit exclusion |
| 407 | 30003813 | already_solved | 15 | Explicit exclusion |
| 408 | 6800004 | already_solved | 19 | Explicit exclusion |
| 409 | 30003840 | unsolved | 24 | Explicit exclusion |
| 410 | 6800009 | already_solved | 15 | Explicit exclusion |
| 411 | 6800014 | claimed_solved | 100 | Existing exact publication and ledger record |
| 412 | 10000083 | already_solved | 13 | Explicit exclusion |
| 413 | 30001005 | unsolved | 19 | Explicit exclusion |
| 414 | 11000048 | already_solved | 16 | Explicit exclusion |
| 415 | None | No changed problem row | 1 | Administrative patch; no mathematical claim |
| 416 | 2100406 | already_solved | 17 | Explicit exclusion |
| 417 | 10400067 | unsolved | 31 | Explicit exclusion |
| 418 | 7200087 | already_solved | 19 | Explicit exclusion |
| 419 | 20001284 | unsolved | 26 | Explicit exclusion |
| 420 | 20001506 | unsolved | 31 | Explicit exclusion |

### Custom folders and missing-status case

I read the live descriptions and immutable branch entrypoints for403/404/407/409, preserving those entrypoints and their blob/hash bindings. Each identifies the same original ID/alias as its own changed row:

- **403:** `generalized_saxl_counterexample_30006342` explicitly credits the Rizzoli–Thomas result and marks the original universal target already solved. Its finite reproduction does not create a new eligible discovery claim under the user's status rule.
- **404:** `sl3_character_rigidity_30002136` explicitly leaves the original unrestricted fixed-pair trace-equivalence problem unresolved. It describes only a proper-subfamily partial theorem.
- **407:** `signed_adjacency_polytopes_30003813` retains a complete literal answer but expressly corrects its classification to `already_solved` by prior theorem coverage. The same ID, authoritative row, current description, correction file, and status file agree. The old complete-answer prose does not override the current explicit non-claim status. I did not reaudit the claimed prior coverage.
- **409:** `braided_thompson_conjugacy_30003840` explicitly leaves the original F_br/T_br conjugacy problem unresolved; the V_br theorem and finite linking classifier are not promoted as a complete resolution.

**415:** I read the entire current description and complete actual one-file patch. It restores the title/source prefix of QUEUE.md, adds no proof/report/result file, and changes no problem row. The two queue blobs have equal size; after the first112 bytes, all382,304 remaining bytes agree exactly. This is an actual missing-status claim classification, not an automatic `queued` skip. The parent receipt's header-only explanation is supported.

## PR411: publication identity and scope

The only actual `claimed_solved` row in this range belongs to6800014 / AMR-067-0014. The original Morgan–Pansu assertion concerns local maxima of Scal²/||Ric||² among left-invariant metrics on a specified solvable group and the derivation equation on that group's Lie algebra.

I independently read the original statement and solvsoliton definition from archived primary TeX. Its full42,288-byte file matches its pre-existing retrieval metadata SHA-256 `33d853a6de512584aeedfaf5b491bcc7f0cf02d2964e8b1f1be67a5b3b97c48e` (retrieved2026-10-02). A fresh direct fetch of the original PDF timed out, and later web fetches also failed; this limitation is recorded rather than described as a fresh successful PDF retrieval.

The actual published six-page note's first two pages were text-extracted and visually inspected. Its statement, source ZIP, pinned PUBLICATION.md, current PR description, record metadata, and full ledger row77 all agree on the following exact result: for the known five-dimensional family A_u=J⊕uE12, each0<u<1/2 gives a non-strict local maximum with F=1/3 among all nearby metrics on the fixed group, failing that group's derivation equation; a metric on the same group has F=9/17. Neither endpoint is included. The record and row preserve prior2018 credit and disclaim novelty, firstness, and present community-open status. This is identity/coverage verification, not a fresh proof or priority verdict.

### Direct challenge to the cached merged-context explanation

The pinned PR head is `2aed7ebe2ccb88d58777c6b01cbdb10634b0dd0a`; the pinned base is `452ba7a9bcccb81247d57dc8078818c833b61ee6`. The merge commit is `ead67e3d28e24ad1142cb6719239acebc5b83f6f`, with first parent `d9f66887131e39811aca3f8b1ed14a975c6c3dea` and second parent equal to the pinned PR head.

I verified rather than assumed the explanation in `PR0411_PINNED_SCOPE_VERIFICATION.json`:

1. The actual branch `base...head` and actual merge first-parent comparison both have the exact same100 paths as the cached receipt.
2. The branch QUEUE blob is `b0a1bc47a4a6d2c5ed94981154338739af15a7bb`.
3. The cached QUEUE blob `7ba6ce11defb9da24b3a53fd33a3ef8e4a186dc3` is exactly the actual merge QUEUE blob.
4. The original own added row is byte-identical in the branch comparison, merge comparison, and cache. The branch-versus-merge queue diff contains no6800014 change.
5. **All99 non-QUEUE changed file blobs are identical between the actual branch head and merge commit.** Thus the explanation does not conceal different scientific payloads.

The preliminary411 cache supplies null per-file SHAs for those99 files. Those null values are missing metadata, not99 blob contradictions. The one supplied queue SHA differs as explicitly disclosed. The independent complete Git blob manifest and direct branch/merge checks fill the relevant binding gap without rewriting that historical receipt.

### Fresh DOI, payloads, manifests, and ledger

The fresh Zenodo API read reports record23331232 as submitted/done. The actual DOI request returns HTTP200 and lands exactly at `https://zenodo.org/records/23331232`. I independently downloaded all three public files, checked recorded sizes and MD5 checksums, and obtained the same SHA-256 digests as both the sweep and pinned branch:

| Payload | Bytes | SHA-256 |
| --- | ---: | --- |
| PDF | 90558 | `13d6fcdb924ea1461a6c44d4bb4e6aec1f278598218f8a34f26252d52ca0d37b` |
| Source ZIP | 21258 | `7d206d67b9c9f61f6ba8eff2c545ed9c2950970b7a6160ede68add8f1ce0162c` |
| Verification ZIP | 540328 | `6a8613bf2e83e7c849dfda02c2019f88b3baa1b0288f2623a14eceb5ba3017d5` |

Both ZIP CRC checks pass. The source manifest verifies exactly2 positive payloads plus itself; the support manifest verifies exactly99 positive payloads plus itself. Every expected payload exists with its stated byte count and hash, every archive member is accounted for, and neither archive nor manifest has duplicate names. The extracted TeX equals the pinned branch's standalone TeX. The support metadata explicitly labels selections outside the complete verification core as partial; no claim that it contains the entire private/source/review corpus is inferred. No mathematical verification program was rerun.

The fresh Sheets metadata confirms `Math Puzzles`, sheetId1254632077. I read canonical identity/notes columns A1:D1173 and the entire target row A77:AQ77. The whole row agrees exactly with the sweep's earlier receipt. Row77 is the unique exact/semantic lead for the PR, ID/alias, DOI, original page, Ricci-pinching title, Morgan–Pansu and Lauret/solvsoliton terms among those canonical identity columns. No unresolved duplicate or defective record was found. This is why411 is skipped; merge state plays no evidentiary role in the publication conclusion.

## Additional challenge to pinned_scope_check.py

At the parent's request I tested the new helper observationally, redirecting its output writer into review memory and preserving the resulting21 actual-range receipts here. No root receipt was overwritten. All21 pass against the same pinned inputs independently checked above.

Controls reject a mismatched evidence head, a missing actual changed path, and a tampered cached added-row status. As designed, a wrong cached whole-QUEUE SHA is accepted with `equal:false`; it is a disclosed mismatch rather than a byte-identity certification.

Two optional hardening opportunities were reproduced: duplicate entries in cached `changed_paths` are accepted because the comparison uses sets, and an incorrect cached `file_count` is ignored. The helper returns its independently computed actual count, so neither invalidates its stated path-set/added-row scope. This range independently has unique cached paths and matching counts. These are not disposition blockers here.

The helper also deliberately does not establish live-head freshness, publication state, custom-folder/row correspondence, semantic claim scope, every file's bytes, mathematical correctness, or novelty. It must remain a scope observation used alongside those separate checks. Its shared parser is not itself independent mathematical or source interpretation. The optional object-fetch fallback is local object acquisition, and this review replaced it with an existing-object assertion so no Git fetch/ref/index operation occurred.

## Strongest verified result and remaining gap

The strongest verified result is the complete21-PR classification coverage described above, supported by fresh provider reads, complete immutable diff/row bindings, all520 file blob hashes, actual custom-folder correspondence, and exact published411 package/ledger identity. No eligible unpublished complete claim was found in this assigned range.

There is no remaining blocker to these range dispositions. This review does not certify excluded or already-published proofs/priority anew, does not make an exhaustive global literature or account-wide semantic duplicate claim, and does not predict future PR/ledger changes. The original source PDF's fresh availability failed, while the archived primary TeX was independently hash-checked and read. These limits do not weaken the actual status exclusions or exact existing-publication identity established here.

## Evidence map

- `INPUT_MANIFEST.json`, `inputs/`, `inventory_snapshot.json`, `live_metadata.json`: source snapshots and bindings.
- `pinned_checks.json`, `ALL_PINNED_BLOB_INPUTS.json`, `GIT_BLOB_INPUT_MANIFEST.json`, `diffs/`, `queue_diffs/`: complete path/blob/row observations.
- `custom_entrypoints/`, `custom_entrypoint_inputs.json`, `pr0415_header_check.json`: custom correspondence and administrative missing-status evidence.
- `pr0411_merge_provenance.json`, `pr0411_public_vs_branch.json`: direct branch/merge/public-byte comparisons.
- `public_recheck.json`, `positive_manifest_checks.json`, `public/`: actual API response/downloads, positive coverage, original payloads and statement-page inspection artifacts.
- `live_ledger.json`, `ledger_identity_checks.json`, `original_source_receipt.json`: exact live ledger and archived primary-source correspondence.
- `scope_helper_actual_range_receipts.json`, `scope_helper_controls.json`: additional helper challenge.
- `VERDICT.json`, `RESEARCH_LOG.md`, `OUTPUT_MANIFEST.json`: decision, timestamped checkpoints, and complete output checksums.
