# PR1156 ledger helper v3: independent adversarial review03

**Execution readiness: false for the exact reviewed v3.** Three operational gaps were reproduced. The proposed external-author attribution and limited existing-publication scope remain suitable as adopted input; this review does not reopen or extend the mathematical/priority claims. No real spreadsheet, Git, GitHub, Zenodo, GWS, or other external operation was performed.

Reviewed helper: `reconcile_external_ledger_v3.py`,15189bytes, SHA256 `7cfc02d7e3456e674a9b8d667dc5065828de85ca8ccc37b3df8c27882e804f50`. Reviewed plan SHA256 `83df78463704c63ea3969a87325f18ab21c21893d6e1b8b49c5b16a6b4e3b2e1`. All original input hashes remained unchanged at the closing check, and the real `ROOT_LEDGER_REVIEW03_ACCEPTANCE.json` remained absent. Mock acceptances were created only inside disposable offline fixtures.

## F01 — Account identities outside metadata/files are omitted

Lines116–121 scan only `item.metadata` and `item.files`, plus payload MD5 values. The complete authenticated record may carry recognized identity in top-level `id`, `conceptrecid`, `parent.id`, `doi`, or `pids.doi.identifier`. These fields are not inspected. Complete pagination and the known owned record23408971 do not repair the downstream omission.

In separate whole-helper controls, a record with generic metadata and an empty file list passed when its sole target lead was record ID23350364, parent ID23350363, or top-level DOI PID `10.5281/zenodo.23350364`. A fourth control containing top-level DOI/conceptrecid also passed. Every control produced one mock append and a `verified` receipt in normal Python, `-O`, and `-OO`. The receipt falsely recorded no account leads. These controls test lead reconciliation, not a claim that current live account records have these values.

Required repair: apply semantic/DOI review to the whole account record and explicitly reconcile recognized numeric record/concept/version-parent identities. Preserve full-account completeness checks, known-account positive control, all-file MD5 detection, and failure on unresolved aliases. Merely widening the metadata title pattern leaves the reproduced gap open.

## F02 — The parsed plan and hash-accepted plan can be different snapshots

Line48 parses one file read. Lines93–94 hash a second read after acceptance and dependency loading. The mutation consumes the first object.

The offline race control initially provided a plan whose notes had the extra text `UNREVIEWED ROW MARKER`; the externally SHA-anchored acceptance still pinned the original plan. When the helper read its acceptance, the mock restored the original plan bytes. The later plan hash succeeded, but the helper appended and verified the earlier, unadopted row. This reproduced in all three Python modes without changing helper or imported dependency bytes.

Required repair: retain a single `plan_bytes` snapshot and parse and hash those same bytes. The initial program source also requires a trusted launch boundary: the helper's reread of `__file__` does not by itself attest the instructions already loaded by Python. A launcher that externally hashes and executes the same retained helper bytes supplies that boundary.

## F03 — Contradictory nested append-response identity is accepted

The response guard checks top-level `spreadsheetId`, update cell counts/range, and echoed values. It ignores `updates.spreadsheetId`, `updates.updatedData.range`, and `updates.updatedData.majorDimension`. A response may contradict itself on these fields and still produce a `verified` receipt.

Three independent probes supplied respectively a foreign nested spreadsheet ID, a foreign sheet/row in the echoed data range, or `COLUMNS` in the echoed data dimension. Each produced one mock append and successful verification in every mode. The final readback still protected the intended sheet row in these tests; this finding concerns the claimed complete mutation-response verification, rather than a demonstrated wrong-destination write.

Required repair: bind the nested update spreadsheet ID and echoed range/dimension to the intended spreadsheet, exact final A:D row, and `ROWS`, in addition to the existing exact values/counts and final readback checks.

## Verified guard behavior

The final matrix contains82 distinct scenarios, each executed in normal Python, `-O`, and `-OO`:246 runs. Every outcome matched the recorded expectation, including intentionally expected fail-open probes above. This is **not** an all-safe verdict. No guard relies on Python `assert`.

The following control families blocked before any mock append: missing/wrong/not-ready acceptance; changed plan/helper/review/dependency hashes; incomplete dependency inventory; symlink dependency; wrong account positive control; incomplete/repeated/inexact/changed-total/foreign/looping account traversal; malformed account metadata/files schema; account metadata/file DOI aliases, unresolved short aliases, and matching MD5; record/concept/encoded identities anywhere in ledger rows; later-cell ambiguous aliases; wrong schema/gid/spreadsheet/range/dimension; changed public metadata/family/files/payload/submission/DOI destination; immediate ledger changes; exclusive-intent competition; changed PR head/base/body/state/merged/draft immediately before append; expired or backward-moving preappend clock; prior complete or partial uncertain intent without an exact row.

After a mock append, wrong top-level spreadsheet identity, wrong cell/column counts, wrong exact returned row, wrong values, extra or missing rows, duplicate target identity, and altered prior rows prevented a verified receipt. The intent remained present. The same-fixture lost-response test performed one simulated successful append whose response was lost; rerunning found the exact unique row and produced a receipt without a second append. Exact preexisting-row recovery likewise issued no append.

All six actual project source dependencies were copied and executed through the helper's own SHA-checked source-byte loader. The import closure is recorded separately. Poisoned preexisting project entries in `sys.modules`, earlier search-path shadow source/bytecode, and mutation of an already-cached dependency source did not change the imported runtime code. The unused function-local `zenodo.main -> metadata_updates` import is unreachable on this controlled non-main module path. The loader's dependency caching correctly avoids the plan's read/hash race.

## Scope, assumptions, and nonblocking boundary observations

The row explicitly attributes Alper Ferudun, leaves the solution-chat cell blank, identifies the existing version/concept family, limits the conclusion to the all-order finite CP-plus maximum and directly inferred exact-rank-stratum corollary, leaves Question1's gap and explicit all-order numeric p_n unresolved, credits the Perron lift, and disclaims chronological firstness. Root's adopted mathematical, priority and external-file reviews are inputs to this operational review. No new DOI, authorship transfer, publication, human peer review, or outreach is authorized or performed.

The mock fixture uses the exact copied helper/dependency/plan/provider/payload bytes, with a reduced inventory containing the exact original PR1156 entry. Every CLI invocation and every network request was intercepted. Unknown commands, non-GET authenticated methods, foreign authenticated routes, and fallback socket/process access were denied. The dummy account token never left the worker. This establishes reproducible runtime guard behavior under the modeled provider schemas, not freshness of the live services.

Current code allows unrelated trailing rows to appear during an exact-existing-row read-only recovery and does not enforce the180second append freshness gate on that no-append branch. Those cases do not create a duplicate write. Public file maps collapse duplicate identical file-key entries; this does not change the set of verified named payloads but leaves a provider-schema uniqueness assumption. The numeric lexical pattern conservatively blocks a foreign URL containing the target digits; that is an unnecessary stop rather than a duplicate-append hole. No cross-service transactional lock is claimed: a small race after final reads remains an external concurrency limit. Trusted Python/stdlib and executable resolution remain launch-environment assumptions.

Initial inspection was independent of previous ledger reports. After completing that inspection and constructing the first matrix, I read review01's report and review02's initial log for historical context. Root separately flagged the top-level account gap while my independent combined top-level probe was already running; it later identified the response-nesting fields, after which I independently reproduced them. Findings are limited to this unchanged v3. Repairs require a new exact-byte review.

Audit completion estimate:100% for the specified v3 review. Existing-publication ledger execution remains blocked pending repairs and independent adoption. No source files outside this review directory were changed.
