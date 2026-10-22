# Independent v6 whole-helper ledger review

Verdict: no unresolved material blocker found for root adoption of the exact helper and plan below, within the stated trust and race assumptions. This review authorizes no service action by the reviewer.

The reviewed helper has 16,969 bytes and SHA-256 8ed805f7e3c1259b4e23064ce084e1ea8e86d3c27a53a6d3207755c27adef88a. The single reviewed plan SHA-256 is 83df78463704c63ea3969a87325f18ab21c21893d6e1b8b49c5b16a6b4e3b2e1.

## Exact claim and scope

The action under review is one GWS CLI append of the exact plan's four cells to sheet gid 1254632077, Math Puzzles A:D, if the row is missing and all fail-closed gates pass. An already identical unique row is idempotently adopted. This records the existing Alper Ferudun publication, record 23350364/concept 23350363. The row explicitly excludes Alec Kriebel authorship, a new publication, chronological-firstness inference, and a solution of Dickinson's Question(1). Mathematical, source-support and priority judgments already adopted by root were treated as prior scope decisions; this audit did not re-promote them.

Success required a complete clean main-entry run with exactly one simulated four-cell append and verified readback, plus rejection or safe idempotence under every listed fault. The scientific target is not an assumption that every conceivable URI is equivalent: unresolved forms are conservative review leads.

## Independence and method

I first read the entire v6 helper and current plan, then independently inspected the identity module, complete authenticated-account reader, and relevant imported dependency behavior. Only after that first inspection did I read and adapt ledger_adversary05's offline whole-helper harness. I retained its 238 controls and added 133 fresh v6 controls. I did not edit original helper, plan, dependencies, Git state or provider state.

All 371 cases passed in each of normal Python, -O, and -OO: 1,113 complete helper main-entry executions. Each fixture copied exact pinned original bytes to a short-lived private tree; root acceptance was synthetic and confined to the private fixtures. Service observations used pinned bytes plus deliberately synthetic perturbations. The helper itself compiled and executed its six checked dependency snapshots in the actual reviewed load order. Tests covered source shadows, invalid pyc files, per-dependency hash changes, and replacement of all six dependency files plus the plan after their initial reads. Successful snapshot-replacement controls confirm saved checked bytes remain authoritative.

The harness stubs subprocess, authenticated HTTPS, and public URL boundaries; a Python audit hook also denies underlying socket/DNS/process attempts. All three runs recorded zero actual network/process attempts, zero original source changes, and no retained case trees. Appends were in-memory mock-service events. This is reproducible offline evidence, not a claim that fresh production state was checked by this reviewer.

## Coverage and findings

The inherited full matrix challenges whole owned records across raw IDs, parent/pids/concept fields, semantic and nested encoded leads, all three known file MD5s, unrelated and matching drafts, complete pagination, and required positive record 23408971. Pagination failures include inexact/changing totals, loops, foreign destinations, missing pages, duplicates and malformed inventories. The final account scan is of complete records, not a metadata-only projection.

The four columns, all-string four-column schema, gid/title binding, single immutable plan, external acceptance SHA and review pins, all six exact source checks, 180-second freshness boundaries, final PR head/base/body/state/merged/draft, provider publication state/metadata/family and all three file sizes/MD5/SHA-256 bytes, and DOI destination are exercised. Source/plan/provider-baseline mismatches fail before append.

Intent tests verify exclusive creation, file and directory fsync before append, concurrent claim failure, preserved intent after either fsync failure or lost response, no automatic retry, absent-row/unknown-outcome blocking, and safe exact-row recovery. Append tests require requested RAW/INSERT_ROWS and one ROWS body, exact nested sheet IDs, four cells, four columns, one row, exact returned values and range, unchanged prefix, unique target/family row, and exact final row/range binding. Invalid responses after a simulated append are rejected with the intent retained.

My fresh controls specifically exercise two, three, four and 64 terminal DNS dots, case and optional-www/dx spellings, bare/protocol-relative/custom or malformed schemes, ports, backslashes, punctuation delimiters, percent-encoded hosts/dots, and one/two/seven/eight/nine nested decoding layers. Both account fields and all four ledger columns are challenged. The tested one, two, seven and eight layers reach the unresolved-alias gate; a ninth still-changing layer reaches the deep-encoding gate. Host homepages, explicit valid unrelated long DOIs, and bounded prefix/suffix/subdomain lookalikes remain nonleads in the explicit positive controls.

The v5 unresolved trailing-DNS-dot resolver family is closed by the v6 [.]* host extension in all these controls, including nested decoded aliases. Additional controls cover contradictory provider-family forms, third-page draft aliases, ambiguous rows following an exact target row, postappend alias additions, malformed pagination types/userinfo, and shifted response columns. No new material concern emerged.

## Trust and practical limits

The claim depends on an uncompromised Python interpreter, standard library and initial import environment; root actually reading the review and supplying its acceptance SHA externally; truthful authenticated installed gh/gws/provider implementations; and local exclusive-create and fsync semantics on trusted audit paths. SHA binding cannot establish root judgment by itself. The helper deliberately executes six exact checked project source snapshots instead of importing arbitrary project source or pyc files.

The helper creates no distributed transaction over Zenodo, the account, GitHub and Sheets. A remote actor can change one service after it was read; the immediate sheet comparison, final PR comparison, freshness bound, durable intent, response checks and readback narrow or expose races but do not eliminate that cross-service interval. Unknown outcomes require reconciliation, not a blind append retry.

The URL recognizer classifies bounded lexical leads; it does not prove all possible URL semantics, DNS behavior or DOI equivalence. This audit makes no claim of worldwide historical priority. The existing publication and the exact approved row must still pass the helper's live gates when root runs its exact initially SHA-checked source bytes with canonical __file__ and CLI arguments.

## Artifacts and reproduction

offline_whole_helper.py reproduces the matrix under Python3, Python3 -O, and Python3 -OO with --output set to a chosen JSON filename. It reads originals but writes only this review directory's private temporary fixtures and chosen result file. RESULTS_*.json preserve every case, expected result, observed error and gate counters. SOURCE_PINS.json records source/artifact hashes before and after; IMPORT_CLOSURE.json records the exact source inventory, imports and runtime assumptions. VERDICT.json is machine-readable. MANIFEST.json closes every retained nonprivate review file except itself with byte counts and SHA-256; no self-hash is claimed.

Completion estimate: 100% of this independent narrow operational review. No live helper run, external communication, Git/index/ref change, publication, DOI creation or service mutation was performed.
