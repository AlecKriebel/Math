# Independent PR464 operations adversary 1

**Verdict: REQUEST_CHANGES. Three blocking operational issues and four required corrections. Do not use these reviewed versions for external writes.**

This review concerns original PR head `97b2ed225574ca61bd03cb8db021a533e04938dc`, problem 30004807, and the four source-prepared publication helpers, their documentation and 127 controls, the archive builder, and the unchanged repository Zenodo kit. It is an operational review, not a new mathematical, priority, human peer, or complete-paper acceptance. The actual final acceptance gate was absent during testing. Five direct gate/stage/publish/tracker/integration probes rejected it before any service dispatch.

All activity was offline and read-only with respect to external services. The reviewer performed no real network call, stage, publication, sheet append, Git object/ref change, PR update, release, merge, or communication with an individual. All fabricated inputs were confined to ignored temporary `private_cases/` directories and removed. Valid summaries and reviewer-authored sources are explicitly whitelisted. No credentials or private foreign-source material were read or included.

## Evidence and independence

The full helper sources, archive builder, README, and original controls were read. The original 127 controls were independently rerun in normal and optimized Python with all 127 case records required to be true and integer-zero real calls. Both replay outputs are byte-identical. This successful replay does not establish acceptance: the reviewer additionally wrote 42 independent expectations, which produce byte-identical normal/optimized summaries. Twenty-nine expectations hold; thirteen unsafe behaviors are reproduced, grouped into the four defects below. They are reported as failed expectations, not disguised as passing safety tests.

The preparer's `Fixture` class was reused only as an openly disclosed constructor of the private synthetic filesystem. The new attack definitions, scenarios, mocked service responses, expected outcomes, and classifications were independently written. Real subprocess and socket boundaries were denied. Mock appends are expressly fabricated counterexample evidence, never production registration receipts. Finite controls provide falsification and consistency evidence, not formal certification or atomic concurrency guarantees.

`REVIEWED_INPUTS.json` records the exact reviewed originals. At the final original-source stability check, all seven helper/control/documentation/builder hashes still matched the recorded originals and the preparer's original positive whitelist. Subsequent repairs do not change this historical verdict. The reviewer did not inspect the remote checkpoint over the network.

## R1 — Reviewed freeze is not cross-bound to the actual source, mathematics, and install plan (blocking)

Location: `operations/common.py`, original lines 177–188 and 207. The final gate hashes the input manifest and current source receipt, mathematical gate, and install plan separately. It reads the manifest's `files` but never checks its own `source_receipt_sha256`, `mathematical_acceptance_gate_sha256`, or `branch_install_plan_sha256` against those current accepted bindings. It also ignores the manifest's PR, problem, and original-head identities.

An independently constructed valid baseline includes all those freeze fields. Keeping that reviewed manifest and the two final review bindings unchanged, the attacker changes one current referenced object and updates only the corresponding final-gate hash. `validate_gate()` accepts the mismatch. The three source/math/plan tests use a benign added annotation, so the acceptance cannot be explained by broken file bytes, a missing input, or a malformed object. They demonstrate that exact reviewed provenance is not enforced. Three additional tests put a wrong PR, problem, or original head in the frozen manifest, bind its SHA, and again receive acceptance.

Required correction: validate the freeze's exact PR/problem/original-head identity and require its three source/math/plan SHA fields to equal the final gate's checked actual bindings. Reject missing, malformed, or unequal fields. This must occur before any service read that could lead to a write, and regression controls should exercise all six discrepancies. Preserve the requirement for two successive, distinct, clean final reviews of the same accepted manifest SHA.

## R2 — A removed earlier verified tracker row authorizes another append (blocking)

Location: `operations/register_pr464_tracker.py`, original lines 37–43 and 58–73. The prior-operation no-repeat check covers only `append_attempted_once` and `outcome_unconfirmed`. It excludes the later `verified_registration` state, and the helper does not inspect an existing verified append receipt when the operation file is absent.

The first counterexample starts with a surviving `verified_registration` operation and verified receipt for the intended DOI/row, but the row is now absent from the sheet. The helper dispatches one new mock append and accepts it. The second counterexample leaves the verified receipt alone and likewise obtains one new append. A retained unconfirmed operation correctly rejects without an append; this is a positive control establishing that the mock boundary can observe the desired behavior.

Required correction: surviving evidence of a prior registration/write must require read-only reconciliation if its exact DOI row is absent. Account for both the operation and independently saved receipt, and do not let a read-only preflight erase the no-repeat evidence. An existing exact unique row may be verified with zero append. Explicitly retain the stated limitation: local guards do not provide a global atomic lock or guarantee recovery if all local evidence is deleted.

## R3 — Additional publication receipts and manifest can overwrite conflicting current-main resources (blocking)

Location: `operations/integrate_pr464_publication.py`, original lines 85–105 and 114–122. Current-main conflict checks cover the thirteen source paths and accepted package installs. The added `publication_receipts/` targets and `PUBLICATION_MANIFEST.json` are constructed afterward as installation targets but are not covered by those conflict checks.

One private mock main contains different existing bytes at `preprint_20261012/publication_receipts/SOURCE_RECEIPT.json`; another contains different existing bytes at `PUBLICATION_MANIFEST.json`. Both integration preflights accept and include replacement bytes in the prospective tree. Control cases at the installed paper and original `release/PROOF.md` correctly reject. These are preparation counterexamples: no actual Git write was made.

Required correction: inspect every prospective target against captured immutable current main before Git mutations. Existing bytes must match the intended bytes, except for explicitly authorized transformations: the selected QUEUE row and the landing publication note's documented frozen/current forms. Different existing publication receipt or manifest bytes must stop rather than silently be replaced. Preserve unrelated files/rows and keep exact post-creation whole-file and changed-path readbacks.

## R4 — Archive builder permits private environments and noncanonical names (required; contained before remote writes)

Location: `build_preprint_package.py`, original lines 7 and 11–16. Its forbidden set omits `venv` and `.venv`, while `Path` normalizes `notes/./same.txt` before the builder validates it. All three independently selected payloads are accepted. The `private_sources` control correctly rejects. No private environment data were read: test payloads are fabricated plain text.

The stronger `common.relative()` check rejects all three paths, so a package containing them would currently fail the final publication gate. The issue is therefore not an observed remote disclosure. It remains a required preparation repair because private environments and path aliases must never enter a purported publishable archive or selected package in the first place.

Required correction: make builder path validation use the same canonical relative POSIX representation and forbidden components as the operational gate, including both environment directory names. Reject absolute, parent, empty/dot, duplicate-separator, backslash/NUL, symlink, generated-bytecode, and forbidden paths before selecting or writing archive outputs.

## Checks that currently hold within their stated limits

- Review issue counts use `type(value) is int` and require actual zero, rejecting missing, booleans, strings, floating zeros, negatives, and positives. Distinct reviewer identities, positive integer rounds, successive final rounds, and final manifest SHA bindings are enforced.
- All thirteen original source files and their historical package copies match their recorded bytes and SHA-256 values. All eleven available internal file references check independently. The standalone author-manifest hash `b64fa97f0194f55cf516cb473a032b1a0bda8ab7c8550cc64e32a098ab6c156f` has no supplied path or bytes and matches none of the thirteen available files. It remains unattested. The helpers do not manufacture it or claim twelve available references.
- Local source checks and live eligibility guard exact PR/head/ref/base/repository/open-draft identity, exact `claimed_solved` status and original `1/5` attempts, original QUEUE SHA, all thirteen source bytes, and the original fourteen-path diff. Excluded statuses are rejected. Installed packets retain the original history and disclose current superseding publication notes.
- Install mappings are positively enumerated, package-contained, hash/size checked, and exactly equal ZIP payloads plus frozen external outputs. The final operational gate rejects path aliases, escapes, symlinks, private fixtures/environments, duplicate archive entries, and circular archive/PDF/deposit payloads. Original historical files are separately checked inside the accepted install set.
- The unchanged kit is SHA-bound and called with production default arguments. Canonical deposit metadata equals the frozen metadata. The wrapper rejects metadata normalizations and wrong title, environment, or upload bytes. Publishing requires the staged exact ID and metadata/package hashes, reinspects the unpublished draft, preserves attempted-write state, and avoids automatic repeat writes after uncertain stage/publish responses. Published states are reinspected; both actual public files are downloaded without authentication and hashed. The kit confines credentialed HTTPS requests to the selected Zenodo host and does not follow credentialed redirects.
- The tracker validates the requested spreadsheet, gid, exact tab and header, keeps the chat cell blank, checks DOI URL/token duplicates, verifies exact response size/range and final unique row, and uses the native GWS CLI. Unknown append responses trigger readback rather than immediate repeat; R2 identifies the later-state hole.
- Integration uses immutable Git trees/blobs rather than binary Contents readback, checks exact parent/compare/target bytes, captures latest main, retains unrelated files and other QUEUE rows, and sends one nonforced branch PATCH. Its saved operations reject repeat `--apply`; uncertain responses are reconciled by readback. No atomic expected-old-SHA or multi-runner guarantee is claimed. The helper intentionally does not mark ready or merge; those later parent actions need their own exact installed-head checks. R3 identifies uncovered target conflicts.

## Exact original bindings and disposition

| Reviewed source | SHA-256 |
| --- | --- |
| `operations/common.py` | `4263af99b97ec84373e53d7afd6bdc508c1cd81696463c12ff25dcf26f43a0a5` |
| `operations/zenodo_pr464.py` | `f9bf46bb315cb62687504a261ef007f5b94e1ac3812137ff6af1866a09b50995` |
| `operations/register_pr464_tracker.py` | `bc6325ea8a6448695b11c5160b9158e28076734a6f2766f9c5f89f501f6fd137` |
| `operations/integrate_pr464_publication.py` | `9810855ded2b9f115cf59eb90e7ef6df5f1d63269527d37db2c609ef6f982996` |
| `build_preprint_package.py` | `5bcd0a301286ec9348008e38d87cbca23894ac57c460082789657e46d3a0ff86` |
| unchanged `zenodo_deposit_tool/zenodo.py` | `a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca` |

Every issue is reasonably repairable. Correct all four, add regression controls, and obtain a **new independent operations adversary** bound to all final helper/builder/kit bytes. This historical request-changes report cannot become a clean acceptance by editing its count fields. Complete-paper reviews remain a separate prerequisite; no claim of ready preprint or production publication is made here.

The assigned operations-adversary audit is 100% complete. Progress toward clean operations acceptance remains incomplete until these repairs and a new review are done.
