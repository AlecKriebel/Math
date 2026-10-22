# R5: concrete evidence checks and their limits

The actual counterexample in helper_controls.py supplies an externally sealed nonempty map containing all six mandatory names. RESULT.json is a nonempty clean result; FULL_AUDIT.md, RESEARCH_LOG.md, AUTHENTICATION_START.json, AUTHENTICATION_END.json and COLD_REPLAY.json are all zero bytes. The actual current review-only gate accepts it. This is separate from review01's unlisted RESULT attack, which now rejects.

The minimum repair is to require positive exact integer byte counts and nonwhitespace actual contents for every mandatory file, authenticated before its use. Text audit/log artifacts must contain actual prose. Parse the three JSON evidence files as nonempty objects, reject duplicate/nonfinite JSON and invalid scalar types, and require checkable identity/provenance/replay fields rather than treating mere filenames as evidence.

The genuine01/02 records already contain the following fields, with different historical names. A validator can normalize the historical schemas without rewriting settled evidence:

| Evidence | Genuine01 field | Genuine02 field | Check |
|---|---|---|---|
| Both authentication endpoints | original_pr_head | original_pr_head | Exact original immutable head |
| Both endpoints | freeze_sha256 | freeze_sha256 | Match authenticated RESULT candidate_pins.freeze |
| Both endpoints | package_manifest_sha256 | manifest_sha256 | Match RESULT candidate_pins.manifest and that candidate's freeze |
| Original per-path identities | originals | all_actual_git_blob_mode_disk_archive_checks | Exactly44 expected original paths; exact byte counts/SHA256/Git mode100644, genuine Git blob IDs, and disk/archive match=true; compare the actual expected original inventory, not count alone |
| Helper identities | future_helpers | future_helpers | Equal reviewed candidate freeze's five helper fingerprints and RESULT.inspected_helper_hashes |
| Frozen candidate inventory | candidate_files (22 records) | frozen_files (count22) with external freeze check | Authenticate the relevant frozen candidate and its 22 files; do not treat the scalar count alone as byte authentication |
| End status | status=PASS | status=PASS | Require affirmative status;01 start instead has label=START and no status |
| Endpoint time | utc | utc | Valid timezone-aware UTC, start<=end within the review's started/completed interval |
| Cold top-level | status=PASS | status=PASS | Affirmative result |
| Cold package identity | package_manifest_sha256 | package_manifest_sha256 | Exact reviewed manifest anchor |
| Cold verifier identity | externally_pinned_verifier_sha256 | externally_pinned_verifier_sha256 | Equal reviewed freeze.files['verify_package.py'].sha256 |
| Fresh extraction declaration | cold_extraction=true | fresh_archive_extraction=true | Affirmative boolean |
| Mode rows | modes[].observed_outer_optimization; receipt | modes[].actual_outer_optimization; result | Four intended outer modes with actual scalar integer0,1,2,2; successful target-specific receipt for each |
| Worker and checks | receipt.worker_optimization; child_execution_guards | result.worker_optimization; child_execution_guards | Isolated nonoptimized worker; three expected author/planar/Meyer child scripts, each optimization0, isolated1; exact target/head/manifest linkage as available |
| Finite outputs | receipt.original_certificate, independent_controls | result.original_certificate, independent_controls | Original certificate PASS,104 letters,48 matrix, inertia23/25/0, signature-2,286 controls; both independent exact-JSON replay results PASS; matching manifest/target and explicit scope |

The gate should also retain explicit unique self-excluded allowlists, authenticated decisive RESULT and all current sequence/issue-resolution checks. It should reject swapped-target/stale-freeze/stale-manifest evidence, failed/missing cold runs and incomplete44-path maps. Check immutable old candidate freezes when validating old adverse reviews; do not require their pins to equal today's candidate.

These checks authenticate and crosscheck recorded claims. They cannot establish that a reviewer was independent, that a claimed execution really occurred, that an external pin is trustworthy, or that mathematical reasoning/priority is correct. Those remain responsibilities of the independent full-package review and trusted custody. A hash validator must not be described as a proof assistant or independent human review.
