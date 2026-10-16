# Independent Zenodo compatibility audit

Decision: **CLEAR for the pinned compatibility source** `b51d1511409c53754293f53fe2229cad1195169d774edf1edb98e569f6be5ad0` (26,239 bytes). No source-level gap remains for this narrow repair. This is a software audit of the existing draft workflow, with no mathematical re-review or live publication performed.

## Frozen scope and observed trigger

Acceptance obligations were persisted at 2026-10-16T09:14:49.785968+00:00, before the proposal existed or was read. The original 25,740-byte source has SHA-256 `a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca`.

The safe actual-draft inspection records existing production ID 23414025, unsubmitted, intended `related_identifiers: []`, and a remote metadata object in which that key is absent. The JSON `related_identifiers_actual: null` in that diagnostic is accompanied by `related_identifiers_present: false`; it does not establish an explicit remote null. The [official metadata representation](https://developers.zenodo.org/#representation) marks related identifiers as an optional array of objects. Actual omission is supported by the parent’s authenticated read, not inferred solely from optionality.

I additionally read the later safe `ZENODO_EMPTY_OPTIONAL_LIST_DIAGNOSIS.json`: the parent reports exact agreement on the other 11 intended metadata fields and both uploaded assets, with only this missing-key representation difference. I made no authenticated network request myself.

## Source result and exact acceptance boundary

I read the complete original and modified source, complete narrow patch, new regressions and README, both existing offline suites, and the metadata-update implementation. The parsed source outside `verify` is unchanged, including identity/file checks, request transport, state persistence, create/upload/update/publish ordering and unknown-outcome handling. All 29 original deposit-test functions are unchanged; exactly three regression methods were added.

The only added exception requires all three conditions: the field is `related_identifiers`, `type(value) is list` and the intended list is empty, and the remote dictionary lacks the key. For this case, the original comparison is `None != []`; the repaired verifier accepts and reports exactly:

```json
[{"field": "related_identifiers", "kind": "empty_related_identifiers_omitted"}]
```

The added condition cannot be true for explicit remote null, any present remote value, a nonempty intended list, another field, or a non-list intended value. The three existing normalization mechanisms and their priority are unchanged. The input metadata, remote object and local manifest remain unchanged.

One pre-existing limitation is explicit: intended null plus remote omission is accepted by both versions because the original verifier uses dictionary `get` and Python equality. Equal invalid types can likewise pass existing equality semantics. This patch does not add those acceptances and is not global schema validation. The new regression’s skipped null subcase documents this pre-existing equality inside that method; it is not a unittest skip. Intended empty list plus explicit remote null is rejected.

The independent 256-pair matrix covered 16 intended/remote shapes, including absent, empty/nonempty/nested lists, null, dictionaries, strings, booleans and numbers. Exactly one acceptance changed: intended empty list plus remote absence. Empty tuple and empty list-subclass omission were also rejected. Ten unrelated-field omissions and nine description/creator counterexamples stayed rejected.

## Actual executions and candid failure history

The private process receipts preserve actual executable, flags, PID, UTC start/end, exit code, both full output streams and stream lengths/hashes. The two corrected successful receipts additionally record the exact probe-source hash. The first failed receipt has no probe-source hash field; its initial source snapshot is preserved separately. The public SAFE_PROCESS_SUMMARY.json exports actual flags, PID, UTC start/end, exit code and stream lengths/hashes without local executable, argument or working-directory paths. All original process receipts and streams remain unchanged and are excluded from the public envelope. Python was 3.14.6.

| Execution | PID | Flags | Tests | Result |
|---|---:|---|---:|---|
| First run | 90914 | `-B` | 75 | 74 passed, 1 reviewer path error |
| Corrected normal | 92111 | `-B` | 75 | 75 passed, zero errors/failures/skips |
| Corrected optimized | 92112 | `-B -O` | 75 | 75 passed, zero errors/failures/skips |

The first error selected the authoring `preprint/zenodo-deposit.json`, whose folder intentionally lacks the ZIP. The actual original stage used `package_assembly_01/candidate/zenodo-deposit.json`, with both assets present. These two manifests have identical 2,642-byte contents and SHA-256 `c88da5c4b34d70088f29927131418d12c80311ea8fba24dbcd384c096cf0cf04`. I corrected only the reviewer probe, preserved the first code/results/streams and reran. No artifact was copied, materialized or modified to conceal the error.

Each corrected run includes all 61 provided tests (58 pre-existing plus three regressions) and 14 independent test methods. These verify the matrix, immutable inputs, original normalization boundaries, 14 identity/state/asset/metadata rejection cases, exact confirmation/environment isolation, one-GET read-only inspection of a saved draft, publication response-loss recovery without another POST, unconfirmed outcomes without retries, and explicit published-but-unverified error reporting. All publish calls in tests are local fakes. A socket guard rejects unmocked networking; test state and temporary files are audit-local. Bytecode writing is disabled.

An initial `apply_patch` persistence attempt failed without an errno; direct `python3 -c` writing succeeded. Intermittent storage pressure was suspected, not proven. No foreign cleanup or evidence deletion occurred.

## Research artifacts and execution binding

Both runs recomputed the digest of the frozen 253-entry core and independently checked all 253 file lengths and SHA-256 values. The digest remains `c06bf8dfd12c840d0f4af7af32ef6253de1c9f8d3b47f7a0618dedd7fd17ed2b`. Protected note, metadata, manifests, build receipts and PDF are unchanged. The parent’s proposed authoring-only DRAFT_STATUS clarification is outside these content assertions and outside the frozen core.

The assembled PDF remains 93,764 bytes / SHA-256 `849aaf7d065061f0fb69e7f3c507d1c5c70301ededa142a61af11cbaddbef74d`; ZIP remains 515,447 bytes / SHA-256 `7b0142907fd2f5d453c095ed24176cbc0aad456eb9c54b01e81c74ba646b01ff`. Both local MD5/size pairs match the actual-draft safe inspection.

A read-only check of the actual existing state confirms that its manifest is the assembled candidate manifest, its environment is production and its ID is the exact integer 23414025, with no publication receipt yet. No state file was changed.

The planned executable is the real file `draft_pr_claimed_solved_800_900_20261012/zenodo.py`. Its resolved `parent.parent` is the repository root, so the unchanged source uses the original repository state and secrets locations. Direct execution of the nested proposal would instead bind to the wrong root. The planned snapshot did not yet exist at my readback; I did not spoof `__file__` or execute such a snapshot.

The remaining operational preflight belongs to the parent: materialize exact cleared bytes at that real path, authenticate both remote promotion paths, verify runtime root/state binding, then inspect the existing saved draft with the unchanged assembled manifest. There is no need for another stage, create, upload or metadata update. This review does not claim that future snapshot/promotion checks have already happened.

## Disposition

No counterexample to the narrow repair was found. Source clearance is exact-hash scoped and preserves the original safety mechanisms. Parent remains sole publishing authority. The audit performed no network writes, Git actions, shared checkout changes, mathematical package changes or external communication.

Audit completion: **100%**. Source gap: **none**. Pending parent operational preflight is listed above and is not represented as completed.
