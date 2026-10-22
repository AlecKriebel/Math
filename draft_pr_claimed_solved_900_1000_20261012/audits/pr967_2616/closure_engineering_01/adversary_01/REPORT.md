# Read-only adversarial engineering audit

Checkpoint UTC: 2026-10-16T20:59:37Z. Static-review completion estimate for the two requested source files: 100%; remediation and independent execution validation: 0%. This estimate is not a scientific or whole-project completion estimate.

Scope: only `close_pr967.py` and `finalize_pr967_and_gate_next.py`. No priority-family reports or conclusions were opened. Neither helper, its entry point, nor its finalizer was executed. No service/network/Git mutation, installation, or external communication occurred. Findings below are source-level counterexample traces, not live reproductions or API documentation validation.

Reviewed source identities:

- `close_pr967.py`: SHA256 `99b8ed0ecf8c035e421f520dff192d938218efbc166a71a62279858fabf0c281`, 703 lines.
- `finalize_pr967_and_gate_next.py`: SHA256 `bf538840d34edc49d86bc4edb59d38a6d201639885bff12922b5a87dc3ab0a4b`, 133 lines.

This is an adversarial engineering review with unresolved findings. It is not a clean full-package review, a permission to execute, or scientific authority.

## F1 — P1: the entry point cannot authenticate its own first execution

Locations: `close_pr967.py:690-700`; `finalize_pr967_and_gate_next.py:120-130`.

Both advertised entry points begin executing repository bytes before `inventory()` compares those bytes with the externally supplied operations-inventory SHA. The worker bootstrap receives an already assembled bundle and trusts it. An altered entry point can perform an action before the check, omit the check, or change the bootstrap. A trusted Python interpreter plus an external expected SHA argument does not authenticate the program receiving that argument.

Counterexample: replace an entry point with an otherwise identical program having a side effect before `context=inventory(...)`. Launch it with the authentic expected inventory SHA. The side effect occurs before the intended mismatch rejection. No Python import-path attack is needed.

Required disposition: supply an independently trusted pre-execution launcher that authenticates the inventory and both source byte strings before compiling any repository source, or make independent external pre-execution authentication a concrete launch prerequisite. If an already approved external launch procedure does this, that procedure can discharge this finding; the two scripts alone cannot.

## F2 — P1: copied authority fields do not authenticate runtime intent origin

Locations: `close_pr967.py:434-454`, `478-516`, `521-535`.

Recovery trusts pre-existing runtime intent files when their public `authority` fields match. Those files are outside the externally pinned evidence inventory. The owner/mode check is only for a directory owned by the current Unix UID; another local task with that UID can populate it. A public operation nonce is an identifier, not a signature or proof that the authorized helper created the intent. The initial foreign-comment rejection at line 539 is bypassed whenever `COMMENT_POST_INTENT.json` already exists.

The chronology checks also do not tie either intent to `operation_authorization.utc`: `authority()` omits that timestamp; the comment intent merely parses its own local UTC; the close intent does not validate its own `utc` at all. An early `server_not_before_utc` and empty before-ID lists therefore make old events eligible.

Counterexample: suppose the exact same-body comment and the unmerged close were previously performed by the now-authorized GitHub actor, before the current root authorization. A foreign local writer copies the current authority fields into a comment intent, uses `before_comment_ids=[]`, and chooses a sufficiently early server lower bound. The writer supplies the deterministically derivable canonical comment receipt and a similarly backdated close intent with `before_event_ids=[]` and otherwise correct current native pins. Recovery can find the historical same-actor comment and close event and produce current canonical receipts. All currently tested actor, body, URL, head, and native-file conditions can hold, although the known-intent origin and authorization chronology are false.

Required disposition: define and enforce a trusted origin for a recovery journal independently of writable repository files. At minimum, validate authorization/intent/server-event chronology and reject preauthorization events; that minimum prevents the historical trace but does not prove journal authorship. If same-UID foreign intent creation is outside the threat model, say so explicitly and remove the stronger no-adoption claim.

## F3 — P1: mutation is not conditional on the inspected PR identity

Locations: `close_pr967.py:538-545`, `547-554`.

The POST and PATCH have no server-enforced relationship to the metadata that passed the status gate. In particular, the close request is only `PATCH /repos/.../pulls/967` with `{"state":"closed"}`. A new head, new base, or draft-state change after the final GET and before GitHub processes that PATCH does not prevent closure. `closure_receipt()` notices the changed state only after the irreversible service mutation.

Counterexample: the final `status_gate()` at line 551 validates the authorized head. Another actor pushes a new head while the intent is being saved. The unconditional PATCH closes that new head; the later receipt check fails. A rejected receipt cannot undo the unauthorized-target closure. The comment path has a larger gap because full comment pagination and actor lookup occur after its preflight and there is no final eligibility check immediately before POST.

Required disposition: obtain a server-enforced precondition for the exact mutable identity if the applicable API supports it, or explicitly resolve the unavoidable race through an approved serialization/authorization policy. A further GET narrows the window but does not make the action conditional. API support for a suitable precondition was not researched in this read-only/no-network assignment.

## F4 — P1: `atomic()` can overwrite a foreign write after its last check

Locations: `close_pr967.py:613-625`, `659-665`.

The function is described as an exact-byte compare-and-swap, but it performs a separate content check followed by unconditional `os.replace()`. The operation lock serializes cooperating helper instances, not other writers of the four shared local files. There is no atomic comparison at replacement time.

Counterexample interleaving: helper reads expected old bytes at line 623; another task saves a changed `CURRENT_STATE.json`; helper executes line 624 and replaces that new state with its staged bytes; line 625 reads the helper's own bytes and succeeds. Thus a foreign update is lost without a conflict or failed receipt. Directory descriptors and no-follow checks do not close this interval.

Required disposition: arrange actual serialization with all writers of these files, or use a storage/update mechanism with a real conditional commit. Document any dependence on cooperative locking. Do not claim unconditional foreign-writer preservation from these checks.

## F5 — P2: local completion can install a stale next-target gate

Locations: `close_pr967.py:594-599`, `640-653`, `671-682`.

The next-PR scan is computed before acquiring the operation lock and is not revalidated before local writes. On recovery, `reconcile_local()` discards the newly computed scan in favor of `plan['scan']`, potentially from an arbitrarily old partial attempt. No code checks that its selected next PR remains an open draft with the same head, base, row, and eligibility before writing it as the active target.

Counterexample: the saved scan selects PR968. Before the local finalization plan is applied, PR968 is closed or its head/status changes. Finalization still writes PR968 and the old head as the active target and completes its local receipt. Re-running the finalizer does not repair this because the staged old plan wins.

Required disposition: authenticate and revalidate the selected next gate at the local write boundary, including resumed plans. If a partially applied plan has become stale, stop for explicit reconciliation rather than reporting a current completed gate.

## Additional limits and observations

- The default read-only path can invoke `git fetch` from `remote_main()` (lines 284-291) when the actual remote main object is missing. That changes the local Git object database despite the broad read-only description. No fetch was run during this review.
- `prerequisites()` binds a comment-review hash and root decision, but has no explicit separately authenticated fresh full-package operations review artifact. Root-level procedural review can supply that authority; this source review does not establish that it has happened.
- No definite REST/GraphQL request-shape error was established by static inspection. API validity, endpoint precondition support, and actual response examples remain unverified here.
- The strict JSON parser, bounded named file reads, captured worker source, exact actor checks, no blind retry behavior, canonical receipt comparison, and staged narrow local projection are useful defenses. They do not discharge F1-F5.

Strongest verified result: source-level safety claims have the explicit counterexample traces F1-F5. Exact remaining gap: remediate or explicitly narrow each trust/concurrency claim, then independently validate the revised package and its externally trusted launch procedure before any live operation.
