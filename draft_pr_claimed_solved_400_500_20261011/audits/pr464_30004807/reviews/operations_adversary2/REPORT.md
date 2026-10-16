# Fresh independent PR464 operations adversary 2

**Verdict: REQUEST_CHANGES. One blocking local-operation issue; two required corrections. The four publication helpers have no new demonstrated defect in this review, but the reviewed archive builder must be repaired before operational acceptance.**

This is a fresh complete operations review for PR464, problem 30004807 / OWR-8415343-010, original head `97b2ed225574ca61bd03cb8db021a533e04938dc`. It covers the current four helpers, archive builder, preparer controls and contract, actual frozen candidate 2, original source history, and unchanged repository Zenodo kit. It is not mathematical, priority, human peer, or full-paper acceptance. The actual final publication gate was absent throughout the genuine missing-gate probes; no actual stage, publication, sheet append, Git object/ref write, PR change, merge, release, or external communication occurred.

All tests were offline. Real subprocess/service/network boundaries were denied during the reviewer controls; the unchanged kit was exercised with an explicit fake client, without reading credentials. Generated counterexamples and sentinel targets stayed inside temporary ignored `private_cases/` and were removed. The reviewer edited only this review's authored files. No reviewed helper, builder, source, package, freeze, or QUEUE status was changed.

## Independent evidence and method

The reviewer read all four current helper sources, the 64-line builder, the complete 812-line preparer control source, the unchanged 539-line kit, the current operational contract and the historical round-1 request-changes report. The previous repairs were hypotheses to test, not an authority for acceptance.

The reviewer wrote **160 independent expectations** across the full workflow and its boundaries. Normal and optimized Python produce byte-identical structured results: **154 expectations hold; six fail**. The failures are faithful adversarial evidence grouped into the two builder defects below; they are not presented as passing controls. All 160 records have integer-zero real external calls. The preparer's `Fixture` was reused only as a disclosed constructor of a temporary synthetic filesystem; attack definitions, mocks, assertions, kit client, download streams and integration service model were reviewer-written. Positive gate fixtures identify their fabricated reports and content as offline mocks, never actual acceptance or production receipts.

The reviewer separately reran all **158 preparer controls** and all **23 parent builder path guards**, normally and with optimized Python. Every case passes and each pair of results is byte-identical. These successful replays did not establish acceptance: their selected-input guards omit the generated-output write boundary tested here. Initial reviewer-driver setup mistakes were corrected only in the reviewer driver: the integration fixture lacked its fabricated tracker receipt, and an expectation incorrectly forbade read-only recovery of an exact surviving tracker row. Subsequent integration failures require the intended guard message, avoiding incidental fixture errors as false passes.

Direct read-only validation of the actual candidate verifies eight frozen top-level files, 181 ZIP entries including its 180-payload manifest, and exactly 185 positive install targets. All ZIP payload bytes match their local counterparts, the manifest, selected plan, CRC and history bindings. The actual freeze's PR/problem/head and three source/math/plan SHA bindings match current bytes. Canonical deposit metadata and exact public PDF/archive mapping match. Thirteen original snapshot files and all eleven supplied internal file references independently verify. The standalone author-manifest hash `b64fa97f0194f55cf516cb473a032b1a0bda8ab7c8550cc64e32a098ab6c156f` has no supplied path or bytes and matches none of the thirteen available files; it remains explicitly unattested.

Six probes using the **actual absent** `FINAL_ACCEPTANCE_GATE.json` test gate validation, default local check, stage with apply, publish with apply, tracker with apply, and integration with apply. Every probe rejects the missing gate before any dispatch. No fabricated gate was placed in the actual audit root.

## R1 — Generated output symlinks clobber unrelated local files (blocking)

Location: `build_preprint_package.py`, lines 39–41, 50, 53 and 56. `selected_path()` guards selected input payloads and subsequently re-read package outputs, but the builder's actual output writes use ordinary paths without checking their unresolved destinations first. `write_text()` and `ZipFile(..., 'w')` follow preexisting symlinks.

Five independent private fixtures supply a symlink at one generated output, pointing to an unrelated sentinel outside the synthetic `package/` but inside the review's private temporary tree. The expected invariant is: reject without changing the sentinel. The observed mechanisms are:

| Exact independent case | Observed result |
| --- | --- |
| `builder_write_boundary_SHA256SUMS.json` | The target is overwritten with a manifest; a later selected-path check rejects the symlink. |
| `builder_write_boundary_regular_zas_bianchi_verification_v1.zip` | The target is overwritten with a ZIP; a later selected-path check rejects the symlink. |
| `builder_write_boundary_ARCHIVE_RECEIPT.json` | The target is overwritten with the generated receipt; a later selected-path check rejects the symlink. |
| `builder_write_boundary_deposit.json` | The target is overwritten with the generated deposit; a later selected-path check rejects the symlink. |
| `builder_write_boundary_BRANCH_INSTALL_PLAN.json` | The target is overwritten with the install plan and the builder completes without rejecting the symlink. |

All five observations reproduce normally and with optimized Python; the sentinel's original bytes are lost in the private fixture. The four late rejections do not undo the preceding write. No actual repository or user file was damaged in testing, and no remote disclosure is observed. This is nevertheless a blocking local-operation defect: a publication-preparation command can write outside its intended output files before the gate can intervene.

Required correction: preflight **every generated output destination**, including the audit-root plan and any new freeze file, before the first output write. Validate canonical owned roots, unresolved leaves and ancestors, symlinks including dangling symlinks, containment and allowable existing file types. Ordinary existing owned regular output files must remain usable for authorized rebuilds. Write only to destinations that passed preflight; do not rely on a post-write selected-path check to establish safety. The repair need not claim atomic protection against a hostile concurrent filesystem change, but it must reject already-present unsafe destinations without changing any bytes.

Required fresh-review controls: all five demonstrated symlink attacks must reject before any output changes; additionally test dangling output/freeze symlinks and unsafe root/ancestor representations. Retain an end-to-end successful build with canonical regular outputs and a new positive freeze number, verifying every ZIP/manifest/install binding. No patched-source acceptance can be supplied by this historical reviewer.

## R2 — Existing immutable-freeze rejection occurs after changing current outputs (required)

Location: `build_preprint_package.py`, lines 57–59 after lines 39–56. The builder checks the positive freeze number and refuses to overwrite an existing frozen review **after** rebuilding the manifest, archive, receipt, deposit and install plan.

The sixth independent case, `builder_write_boundary_existing_freeze`, starts with an existing private candidate-2 freeze and valid selected inputs. Running the real builder logic with `--freeze 2` raises `Never overwrite a frozen review input`, and preserves that frozen file. However, the exact filesystem before/after comparison shows changed bytes at:

- `BRANCH_INSTALL_PLAN.json`
- `package/ARCHIVE_RECEIPT.json`
- `package/SHA256SUMS.json`
- `package/regular_zas_bianchi_verification_v1.zip`

The deposit is also rewritten by the source flow; its bytes happen to stay identical in this particular fixture and are therefore not counted as changed evidence. The test records the four actual differences rather than overstating the observed set. The resulting current outputs no longer match the still-preserved reviewed freeze. The publication gate would reject those discrepancies, so this is not a reproduced remote-write bypass, but it is a required preparation repair: an invocation rejected for an immutable destination must not first invalidate the current accepted candidate.

Required correction: validate the freeze request, its positive integer domain and destination nonexistence before any generated output write. A preexisting freeze or invalid requested number should leave current package, plan and existing freezes byte-identical. Apply the R1 output-destination checks to a new freeze. The source also performs the invalid-number check late; this ordering is a code deduction, while the existing-freeze case above is the reproduced computation.

Required fresh-review controls: normal/optimized preexisting-freeze rejection with complete before/after byte equality; invalid zero/negative freeze rejection before writes; and successful construction of a new freeze without editing earlier freezes. Do not silently rebuild actual candidate 2 while preserving a now-stale review binding.

## Whole-pipeline checks that hold for these exact helper bytes

- **Final gate and provenance:** actual integer-zero issue counts reject missing, booleans, strings, floating zeros, negatives and positives. Final reviews must be fresh, distinct, clean, successive rounds and bind the same exact manifest. The repaired freeze rejects a changed current source receipt, mathematical gate or install plan while the reviewed freeze is held constant; it also rejects changed PR/problem/head identities. All current helper, kit, paper, metadata, selected source, install and archive bindings are read before service writes. This is validation of the operational contract, not the truth of fabricated mock review prose.
- **Scope and original history:** live checks bind PR464, repository, main base, exact head and branch/ref, open draft state, exact `claimed_solved`, original `1/5`, original QUEUE hash, thirteen historical source files and the fourteen-path original diff. Excluded statuses, altered attempts/source and truncated, renamed or unrelated diffs reject. No unavailable standalone manifest is reconstructed.
- **Archive and installs:** the actual 185-file positive plan equals exactly ZIP payloads plus frozen external outputs. Private/environment paths, escapes, aliases, symlinks, duplicate entries, unplanned installs and circular PDF/archive/deposit payloads reject. The repaired builder's selected-input path guard also rejects environments and canonical aliases. R1 and R2 identify the remaining distinction between safely selecting payloads and safely mutating generated outputs.
- **Zenodo:** the unchanged kit is SHA-bound and production arguments are verified. Canonical metadata, exact PDF/archive names and byte SHA/size identities are enforced by the wrapper; metadata normalizations reject. Publishing requires the confirmed staged ID and exact accepted metadata/package, with read-only reinspection before publishing. Mock stage/publish lost responses preserve attempted-write records and use inspect rather than repeating a write. The unchanged kit's actual code separately rejects wrong IDs/publication-state types, metadata and upload-checksum drift; it performs one publish attempt and reinspects after a lost response. Public verification independently streams both actual mock download bodies without authentication and checks exact sizes/SHA-256, rejecting both added-byte and same-length corruption. These are offline fake-service tests, not actual Zenodo records.
- **Tracker:** native GWS invocation, spreadsheet/gid/tab/header identity and exact A:D intent are checked. The chat cell stays blank. URL/token DOI aliases cannot produce duplicate rows. Surviving attempted or verified operation records, or a receipt without the operation, reject if their row disappears; defaults preserve those guards. An exact unique surviving row is recovered with zero append. New registrations make one mock append after saving intent; uncertain/malformed responses and later duplicate snapshots cause readback or rejection without another append. Other tracker rows remain untouched by the test service model.
- **Integration:** every prospective current-main payload destination is checked, including added publication receipts, generated manifest and landing note. Conflicting history, paper, source/math/final/reviewer/operations receipts, manifest and landing bytes reject before any Git object creation; identical bytes and the explicitly known frozen/current landing forms are accepted. Only the selected QUEUE row changes and original `1/5` is retained. The commit uses captured latest main as its tree base and exact parents `[original head, captured main]`. Unrelated main files and other rows are preserved. Binary whole-file immutable tree/blob readback, exact compare path set and parents detect corrupt targets, unexpected/duplicate/renamed diffs and incorrect bases. Head/main movement stops the ref update. A successful/lost-response flow makes one nonforced PATCH, saves it before dispatch and reconciles by reads without another write. No binary Contents endpoint is used.

Finite checks do not prove all possible executions. Local durable records are not a global atomic lock; deleting all local history defeats their ability to infer past writes. GitHub nonforced ref updates are not an atomic expected-old-head compare, and Sheets can admit a concurrent append. Those limitations are correctly disclosed. The helpers deliberately leave marking ready and merging to the parent, which must use fresh exact installed-head checks. Full paper acceptance remains a separate pending gate.

## Exact reviewed bindings and disposition

| Reviewed source | SHA-256 |
| --- | --- |
| `operations/common.py` | `ba508397f2999c90f1d6e8bc1ef327f4258cc3a6e9acb4a7fe255051506a74ac` |
| `operations/zenodo_pr464.py` | `f9bf46bb315cb62687504a261ef007f5b94e1ac3812137ff6af1866a09b50995` |
| `operations/register_pr464_tracker.py` | `6454154cc7a24fac9e5b85a0147ddfccc58e3db4f72b5f855c39ef0080e70d44` |
| `operations/integrate_pr464_publication.py` | `1f5629b7aea5c6de4dda3b67655540c9fae0a434130b872f485a662388f2ba5b` |
| `build_preprint_package.py` | `960c364c3b3dc10ecc6570f7069ea11150f90f8859f810872837a68161869074` |
| unchanged `zenodo_deposit_tool/zenodo.py` | `a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca` |
| `PACKAGE_REVIEW_INPUT_2.json` | `6354507a17d9eca504e5db085621b645fc4afb9cd00291e74ee0e5a145c8a352` |

Both builder defects are reasonably repairable. The parent should preserve the reviewed builder bytes, fix both globally, add the stated whole-build regression controls, and assign a **NEW fresh operations adversary 3** to all final helper/builder/kit bytes. This report and its failed expectation counts must remain historical REQUEST_CHANGES evidence rather than being edited into acceptance after repairs.

The assigned fresh operations review is 100% complete. Clean operations acceptance remains incomplete. No preprint-ready or actual-publication authority is granted.
