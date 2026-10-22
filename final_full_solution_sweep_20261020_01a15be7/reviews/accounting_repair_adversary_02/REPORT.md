# Independent accounting repair adversarial review 02

Review date: 2026-10-21 UTC. Bounded review completion estimate: **100%**. Overall sweep completion is not asserted.

## Verdict and strongest verified result

**The repair fixes all 13 originally demonstrated false accepts, preserves the four valid publications and historical/effective accounting, but still accepts materially incomplete or contradictory local evidence. Further accounting repair is required before treating this validator as fail-closed.** This review does not identify an incorrect canonical publication, require republishing, or authorize changes to scientific packages, public records or ledger rows.

The reviewed source is the individually captured `inputs/current/coverage_snapshot.py`, SHA256 `e131e827013e5fa632c38a072a7a064190685d69000a09778daaa1252c9560ed`. Its full source, preserved predecessor, generated diff, root replay receipt and root/nested publication receipts are retained. The canonical ordered sweep advanced while this review ran. The captured coherent baseline is next PR **464**, exact prefix **9–463**, **455** journal entries; no assertion is made that current canonical STATE or journal remains at that point.

All **1395** files in the prior review's output seal were independently rehashed successfully before this review's tests. Its evidence was not changed. Its complete recursive captured inputs were copied into this review, and the repaired implementation was mounted there for the original controls. Current captured inputs and evidence were mounted independently for new controls. Every case starts from a complete recursive copy; mutations and normal/optimized stdout/stderr are retained separately. Python bytecode writes were disabled.

## Validation results

| Test family | Cases per mode | Expected outcomes per mode | False accepts per mode | False rejects |
|---|---:|---:|---:|---:|
| Original controls, old captured inputs + repaired code | 21 | 21 | 0 | 0 |
| Fresh main controls, current captured inputs | 163 | 144 | 19 | 0 |
| Supplementary explicit nested contradictions | 10 | 0 | 10 | 0 |
| Total | 194 | 165 | 29 | 0 |

Both ordinary Python and `-O` give these same outcomes: **388** total executions. In the original21, the valid baseline is accepted and all20 corruptions are rejected, including all13 formerly accepted cases. In the fresh173, the valid baseline and completed-list permutation are accepted,142 corruptions are rejected, and29 are accepted. Two of the29 are lower-severity exact-type issues; the remaining27 concern material evidence or its target/contradictions. The tables count concrete cases, not distinct root causes.

The repair correctly rejects the tested malformed completed PR/record/row/problem/DOI/path/merge types, alternate DOI spellings, duplicate completed identities, missing/unbound completed entries, wrong root receipt identities, missing root PDF/ZIP material, malformed SHA256, missing bound ledger/public receipts when their paths remain required, wrong ledger PR/row, false read-back flag, wrong public-file record/hash, false/missing metadata verification flags, wrong archive payload counts, unsafe completed paths, canonical proof symlinks and symlinked canonical audit directories. It preserves the documented PR397 historical metadata flag and PR292 legacy baseline. Those are real improvements.

## Findings that remain

### R1 — Modern publications can silently use the unscoped legacy escape hatch

The conditional at captured source lines123–142 chooses the legacy fallback solely because `evidence.public_files` is absent. It does not require the documented legacy file schema or establish that this is the legacy receipt. For each of PR397, PR399 and reopened PR280, the isolated mutation removes `evidence.public_files`, removes the corresponding `ZENODO_PUBLIC_FILE_VERIFICATION.json`, and adds `reviewed_hashes` containing the PDF/ZIP hashes already present in the same root receipt. All three are accepted with four effective publications in both modes.

No legacy download fields are introduced: the modern proof remains modern. Self-copied SHA strings replace the required separately bound public-file evidence. This bypasses the repair's intended nested-receipt check and metadata confirmation, even though the nested receipt is physically absent. Cases: `modern_silent_legacy_fallback_397`, `_399`, `_280`.

The remaining gap is schema-qualified compatibility: preserve the actual documented legacy baseline while requiring modern receipts to bind their corresponding public-file receipt. Copying the root's own hashes into another root field cannot independently establish the missing receipt.

### R2 — The bound ledger receipt's actual row and sheet are ignored

Captured source lines117–122 check a ledger wrapper's PR, DOI, row number, status and two positive flags. The actual `values`, `spreadsheet_id` and `sheet_gid` are ignored. For each of the four publications, deleting `values` entirely, replacing `values[2]` by `https://doi.org/10.5281/zenodo.99999999`, changing `spreadsheet_id` to `another-spreadsheet`, or changing `sheet_gid` to1 is accepted. These are16 separate accepted cases per mode; the first12 are in the main controls and4 gid cases are supplementary.

The wrong actual DOI is a one-field contradiction: the receipt's read-back cell says a different DOI while its summary wrapper says the expected one. The repair therefore binds the filename and summary labels, without binding the local evidence of the actual ledger row to that publication and the configured sheet. The expected sheet identity is already present in captured STATE. This finding does not request a new network read or a new whole-ledger uniqueness certificate. The gap is local schema and consistency checking of the evidence already claimed.

Cases: `ledger_missing_values_<pr>`, `ledger_wrong_actual_doi_<pr>`, `ledger_wrong_sheet_<pr>`, and `nested_ledger_wrong_gid_<pr>` for292/397/399/280.

### R3 — Explicit negative public evidence can coexist with an accepted positive summary

For each modern nested public-file receipt, changing only `record_http_status` to404 or only `doi_resolution.resolved_url` to the unrelated canonical record99999999 is accepted. Root resolution remains200 for the expected record, so the local artifacts explicitly disagree. The public receipt block at lines126–135 ignores these known nested fields. Six supplementary cases demonstrate this in both modes: `nested_record_http_404_<pr>` and `nested_doi_wrong_destination_<pr>` for397/399/280.

For legacy PR292, adding `downloaded_and_matches_reviewed=false` and `http_status=404` to its ZIP entry is also accepted because the presence of `download_verified` chooses the other field family. Replacing its ZIP member list by just `arbitrary/a` and `arbitrary/b` is accepted even though no manifest member remains. Lines44–63 accept positive legacy flags and two safe names, without rejecting contradictory present download evidence or requiring manifest evidence in the listed archive contents. Cases: `legacy_conflicting_negative_download_evidence`, `legacy_zip_missing_manifest_member`.

This is eight accepted cases per mode. Compatibility should preserve the legacy schema without allowing an explicit present negative verification result to be hidden, and required manifest evidence should not be satisfiable by two arbitrary paths. No underlying public bytes were modified in these cases; they falsify acceptance of the local claimed evidence.

### R4 — Effective disposition PR types remain weaker than completed/root identities

Changing ordinary PR292's `pr` to292.0 in both its journal and saved disposition, or reopened PR280 replacement's `pr` to280.0, is accepted. Python numeric equality makes these values compare equal to integer identities; completed/root PRs do receive exact-int checks. Cases: `ordinary_effective_pr_float`, `reopened_replacement_pr_float`.

These two accepted cases do not change publication counts or associate a different numerical PR. They are lower-severity schema hardening gaps, separated from the material failures above. Exact types for all bound PR identities would make the invariant uniform.

## Independent current accounting and identities

A separate direct calculation, without executing `coverage_snapshot.py`, confirms the455-entry exact ordered prefix, equality of every saved disposition with its journal entry, and exactly one historical PR280 decision. Its historical bytes remain SHA256 `12786fed27bdc64dc25404de4d559f04611947006cfb62f0ee6e8bf1399009b1`, still `skip_priority_gate_not_met`, correctly bound by the replacement.

| Disposition | Historical journal | After single PR280 override |
|---|---:|---:|
| skip_entirely_already_published | 56 | 56 |
| skip_explicit_non_claimed_solved | 385 | 385 |
| skip_priority_gate_not_met | 3 | 2 |
| reconcile_existing_publication_record | 3 | 3 |
| published_verified_full_solution | 3 | 4 |
| reconcile_existing_external_publication_record | 1 | 1 |
| skip_inferred_no_full_solution_claim | 3 | 3 |
| skip_missing_status_no_full_solution_claim | 1 | 1 |

The completed list has exactly these four distinct identities, all matching the captured effective disposition, root verification and corresponding ledger DOI/row values:

| PR | Problem | Record | DOI suffix | Row | Merge commit |
|---|---|---:|---:|---:|---|
| 292 | 30001608 | 23524971 | 23524971 | 174 | 10c77bd03ac17afa6bcaabf6e82bacdd17cb92dc |
| 397 | 9700002 | 23527793 | 23527793 | 176 | 7f471f767d9d895850c0ebb6fdaf2b12a3472f24 |
| 399 | 30001179 | 23539283 | 23539283 | 177 | 1a80b81ce940d9f67d9a45b48176b47ab266a652 |
| 280 reopened | 30000156 | 23539734 | 23539734 | 178 | 0e0893c6d753140925558cfb3f0bad4204ac7517 |

Each DOI is `10.5281/zenodo.<suffix>`. The separate PR293 external-author reconciliation remains separate and is not a fifth own publication. Both valid baseline executions agree with these independent counts and identities. Full exact captured ledger cells, file evidence, hashes and identities are in `INDEPENDENT_ACCOUNTING.json`.

## Scope, reproduction and custody

The falsifiable target was that the repaired local structural summary preserves valid canonical accounting and rejects incomplete, malformed or cross-bound publication evidence. The original demonstrated failures are fixed; the new counterexamples prevent an unqualified repair acceptance. The exact remaining gap is the local evidence schema/consistency described in R1–R4. No mathematical proof, priority, universal novelty, public lifecycle deduplication, or new live-authority claim is made.

No new remote downloads were needed: the four actual publications and ledger rows were already independently verified, and the original sealed evidence was checked intact. Review executions use only captured local files. A nonzero process result counts as rejection, including malformed-type errors; acceptance is a successfully emitted snapshot. Every case's mutation and normal/optimized outputs are retained under `cases/`, with source files and programs sealed by `OUTPUT_MANIFEST.json`. `controls.py` and `supplementary.py` reproduce the tests using the captured inputs and write only within their review folder. `finalize.py` validates input custody, independent baseline comparisons and the review output seal.

All review writes were confined to this new `reviews/accounting_repair_adversary_02/` directory. No provider/GWS operation, Git status/index/ref/commit/push, PR/publication/release/Zenodo modification, scientific package edit, canonical code repair or external outreach was performed. `GIT_OPTIONAL_LOCKS=0` and bytecode suppression were set for the review programs. The parent alone decides and implements any further repair and publication of this review checkpoint.
