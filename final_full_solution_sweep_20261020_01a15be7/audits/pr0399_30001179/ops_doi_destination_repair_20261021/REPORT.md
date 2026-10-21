# PR399 exact DOI destination repair

This bounded local repair addresses the sole new material finding P399-04-OPS-01. The final DOI landing destination is now checked against the literal intended HTTPS Zenodo record before any successful public-verification receipt. The appender independently repeats the destination check and requires exact matching destination evidence before the final account/sheet gate or any sheet read/append. This is an operations repair, not scientific clearance or a live publication outcome. `publication_ready` remains false. Root verification/reproduction and NEW complete history-free package review05 are required before root decides the next step. No `ROOT_PUBLICATION_CLEARANCE.json` was created or edited.

## Finding, full reading and preservation

I read the complete final review04 REPORT, VERDICT, entire9,457-byte `operations_checks.py`, and root's `ROOT_PACKAGE_REVIEW04_ACCEPTANCE.json`. The review's25-entry seal is `4822b258611ad2a7ddb57a5f4db2137ee1b8752883d9c50ef94923435f90d678`; all25 entries verified. The reviewer found no new mathematical/archive/source/rendering defect, resolved the previous DOI identity/directory/record-URL findings, and demonstrated this distinct final DOI-destination defect.

The actual `zenodo.doi_status` can return HTTP200 with a final URL for a different record. In the old binding, the actual public verifier accepted wrong sibling `https://zenodo.org/records/29999990` for intended29999991, and also accepted `https://example.org/unrelated`. The actual DOI-status→live-verifier→appender pipeline appended a synthetic row and returned false publication-link assurance despite the sibling destination. These are representable provider outcomes; no actual target DOI is asserted to exist or be misconfigured.

Before any canonical edit, all356 bound artifacts of seal `151a3c3c1dffa10750fad0ba8fdb189ba27698c30c3d0d2c000c98dbc48e732b`, its exact manifest/checksum and56 immutable inputs were copied audit-relatively into `pre_destination_binding`. Review04's25 artifacts, manifest/checksum and root acceptance were preserved. The executable preservation closure contains631 exact files, including older top-level context needed by the historical verifiers. Nothing under that preserved context has been rewritten. The preserved356 verifier was actually executed successfully, reconstructing its156 and42/26 lineage. The new immutable binding retains all624 current nonhelper context entries, while the seven changed/current helpers are separately bound.

The exact old review04 program was newly replayed in normal and optimized Python against the frozen356 helper source. Its55 other controls passed and its four DOI observations reproduced: actual DOI-status output, two direct wrong-destination acceptances, and actual final-verifier→appender acceptance. Only owned output/private custody and exact frozen helper/hash receipt lookups changed. The original source, SHA256 `08991cecd52cf1907d3b4bcd680e4f66de8cf207d6c70ba2d9c3aeee4201b936`, remains unchanged. `old_finding_normal` and `old_finding_optimized` retain those observations as old failures, not current successes.

## Narrow authenticated outcome policy

Only this exact literal URL is accepted for a positive integer expected record ID:

```text
https://zenodo.org/records/{expectedID}
```

The scheme and authority must have exactly those bytes. Explicit ports, including443 and leading-zero443, userinfo, foreign/suffix/subdomain hosts, host aliases/case variations, trailing dots, HTTP/other schemes, singular/API routes, dot segments, repeated separators, leading-zero/encoded IDs, path tails, trailing slash, query, fragment and whitespace all reject. Missing or non-string URLs reject. The DOI HTTP status must be an exact integer200; non200, strings, booleans and floats reject. Wrong sibling, concept or version IDs are never substituted. This deliberately narrow policy is not an assertion that every rejected URI is a different network resource. If the real resolver returns another form, root must inspect it and review a policy change rather than silently normalizing it.

A small pure `doi_destination_evidence` function in `ops_binding.py` enforces this policy. It does not call the conservative lexical ledger-lead recognizer. Its result contains exactly policy tag `pr399-exact-https-record-v1`, expected record ID, status200 and the literal URL. `verify_public_record` validates the actual final outcome and includes that evidence inside `doi_resolution.destination_verified` only after the existing intended metadata, DOI-name/record and exact file checks succeed. Existing authenticated/public metadata normalization, exact public ID and DOI name/URL, PDF/ZIP hashes/sizes/MD5 and archive checks remain in force.

The appender first retains its existing fresh-public-record, byte-verification, status and release checks. It then independently recomputes the expected evidence from the receipt's status and resolved URL, checks exact evidence equality and exact integer evidence types, and rejects missing, contradictory or extra evidence fields. Thus booleans or a forged positive proof cannot rescue a wrong URL; a correct URL without proof also fails. This happens before `collect`, any independent sheet read, intent or append. The successful literal-row idempotence and single append/readback mechanics are unchanged.

Only three canonical helper files changed: `ops_binding.py`, `verify_published_files.py` and `record_publication_ledger.py`. The other four helpers retain their exact previous bytes. `CURRENT_HELPER_BINDING.json` binds all seven; `REPAIR.diff` is the complete difference from frozen356. The existing ASCII DOI/percent-encoding rules, conservative URL/family leads, all-cell scans, target-before-exemption rules, selected directories/empty trees, source11/publication5/QUEUE/branch/merge bindings, exclusive fsynced intents and no-blind-retry protections were not relaxed.

## Actual-function controls and old regressions

Every final suite passes in normal Python and `-O`, with zero real provider attempts:

| Suite | Controls per mode |
| --- | ---: |
| New exact destination/evidence controls |170|
| Unchanged reviewer04 nonfinding controls |55|
| All previous current controls |1651|
| Total current obligations |1876|

The new controls execute actual `verify_public_record`, actual `verify_live` and actual `append_verified` with synthetic service boundaries. Three cases use actual `zenodo.doi_status` with a synthetic opener: correct canonical URL, wrong sibling and foreign destination. Successful canonical cases retain actual exact file downloads/metadata verification, durable append intent, literal row append and full unique readback; canonical idempotence appends zero rows. Wrong cases reject with zero final gate calls, zero sheet reads and zero appends. Independent upstream-bypass cases supply otherwise positive receipt booleans and even an apparently correct proof while varying the final URL; all wrong outcomes still reject. Other controls reject missing/forged evidence, wrong policy/record/type, extra fields, invalid expected-ID types and missing/malformed/non200 outcomes. The correct independent proof case succeeds, so this is not a blanket rejection fixture.

The reviewer04 first55 controls were executed from their exact source prefix without changing their outcomes. They test account pagination, prior lexical rules, every intended public metadata mutation, same-size PDF corruption and a correct public baseline. All service access is trapped or replaced explicitly. The clearance and fresh account/sheet prerequisites are simulated to reach the actual downstream checks; they do not claim real clearance or provider state.

All previous1651 obligations were meaningfully rerun:818 record-route pipeline controls,530 older identity/directory/ledger regressions and the unchanged303-case root benchmark. The cached176-row compatibility observation is retained separately. Five historical synthetic public receipt fixtures lacked the destination fields because that prerequisite was previously untested. The adapter verifies the exact old compile body, then adds only the literal expected URL and exact destination proof to those five fixtures: the818 program, old123 program, old83 program, original offline controls and original repair controls. They all use expected record999. The preexisting canonical inspection fixture already had the correct resolved URL and needed no change.

`evidence/*/previous/FIXTURE_ADAPTATION.diff` shows every fixture-only line change; `REPLAY_1651.json` binds before/after compile hashes and all five source selections. Original source files remain unchanged. The old directory fixture adapter remains byte-identical. No expected verdict, production check or guard was removed, changed or mocked out by the new adapter. Previously intended negative cases still reject for their actual condition; enriching their otherwise valid public prerequisite prevents the new guard from making them vacuous. The compile adapter recognizes only five exact source bodies/paths and cannot modify production helper code.

One actual development test exposed an implementation mistake: the new proof variable was overwritten by the preexisting file-download loop's destination variable. The correct canonical full-pipeline case rejected. The proof variable was renamed; no expected outcome changed. A new successful bypass fixture also needed its synthetic saved public receipt file to satisfy the preexisting intent hash prerequisite; that fixture file was added. The initial old-program replay used a public output path, which its private-custody guard rejected; the harness was corrected to private output and only synthetic result JSON was copied back. These corrections are recorded, rather than presented as old code failures or weakened production guards.

## Scientific and state boundaries

The11 original snapshots, exact scientific five payloads, RELEASE, metadata and three separate preparation notices are byte-unchanged. Root semantic lead reconciliation remains `af763826f5e22bb64887496eada7e4aaa9c944faf45db3a0c93386b9833fbe39`. No root lead exemption was copied or revised. Root's full review acceptance is preserved as parent-authored evidence, not new scientific clearance for the repaired helpers. Original399 head remains the pinned `08fc8833a56358d505e0b33ae1debe44ec320add` contract; this repair issued no Git command or fresh provider branch read. Actual immutable Git-parent/QUEUE checks and all prior scientific/priority/visual reports remain in their preserved generations.

All241 direct JSON and314 recursive regular local `.zenodo-state` files match their pre-edit sorted repository-relative path/size/SHA256 inventories. `LOCAL_STATE_PRESERVATION.json` distinguishes those two scopes. No actual provider, Git/index/ref/branch, PR, Zenodo saved state, GWS, ledger or global progress/log mutation occurred. Raw synthetic downloads and service fixtures remain in owned private custody; only the reproducible programs and result evidence are sealed here. No external individual or unrelated agent/chat was contacted.

## Private-output replay and remaining gate

Verify this exact new seal with:

```text
PYTHONDONTWRITEBYTECODE=1 python3 /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/ops_doi_destination_repair_20261021/seal_repair.py --verify
```

Replay the actual170+55 controls and all1651 regressions into a NEW private directory, preserving every sealed audit output:

```text
PYTHONDONTWRITEBYTECODE=1 python3 /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/ops_doi_destination_repair_20261021/replay_all.py --output /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/private/pr0399_doi_destination_repair/root_new_normal
PYTHONDONTWRITEBYTECODE=1 python3 -O /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/pr0399_30001179/ops_doi_destination_repair_20261021/replay_all.py --output /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/private/pr0399_doi_destination_repair/root_new_optimized
```

The runner checks current seven-helper hashes and, once frozen, all manifest artifacts/immutable inputs before testing. It refuses an existing output folder. No lifecycle command is part of this replay. Root alone may decide live work after fresh complete history-free reviewer05, its complete report/seal review, and required fresh account/sheet/local-state and branch/merge checks. This report claims no actual DOI resolution, target publication, row append, root authorization or future clearance.
