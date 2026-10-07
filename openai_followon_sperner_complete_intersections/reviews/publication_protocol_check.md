# Publication and tracker protocol audit

Timestamp: 2026-10-07 05:41:30 UTC. Narrow protocol audit completion: 100%.
Mathematical/package completion estimates are unchanged by this operational audit;
the independent complete-package review and actual publication/tracker actions
remain the lead researcher's gates. This is not a mathematical review.

## Scope and actual inspection

Read `PROJECT_BRIEF.txt`, `verification/update_tracker.py`, the project manifest,
publication README, frozen candidate-v2 receipt, and repository Zenodo tool README
and relevant current implementation. Inspected installed gws 0.22.5 help and
schemas for `sheets.spreadsheets.get`, `sheets.spreadsheets.values.get`, and
`sheets.spreadsheets.values.append`. Read the installed gws-sheets instructions;
their referenced gws-shared skill is absent from the installed skill directories.
No skill-generation command was run. Current CLI help/schema provided the actual
request interface.

Inspected only the saved tracker snapshot's range, headers, and structural counts:
`'Math Puzzles'!A1:AQ1039`, four columns headed `Original Problem`,
`Solution Chat URL`, `DOI`, `Notes`, 43 returned nonempty rows and no interior empty
rows. Other projects' row contents were neither printed nor copied here.

No credentials were read. No network publication/tracker calls, outreach, commit,
push, branch change, or frozen-package modification were performed. The only
audit-authored file is this report. Test API calls and receipt writes were mocked
in memory; real candidate files were only read.

## Findings and repairs verified

1. **Publication receipt was initially insufficiently bound to this project.**
   The initial helper checked published state, production environment and DOI/ID,
   but would accept a different project's otherwise valid published receipt and
   compose the current title around its DOI. The lead researcher repaired this.
   The inspected revised helper explicitly checks receipt title, frozen manifest
   SHA-256, receipt payload names/sizes/SHA-256, and current local payload bytes.

2. **Operational assertions initially disappeared under Python optimization.**
   An in-memory reproduction with `compile(..., optimize=2)` accepted a draft
   receipt, called the mocked append once and wrote a mocked verified receipt.
   The lead researcher replaced every operational assertion with an explicit
   `require` raising `RuntimeError`. AST inspection of the revised helper found
   zero assertion statements. Optimized execution now rejects draft, sandbox,
   wrong-title and wrong-payload receipts before any mocked append.

3. **The retained generic local-check receipt is historical, not current.**
   At inspection, `receipts/zenodo_local_check.json` had the correct title but
   file size/SHA-256 values that did not equal frozen candidate v2. The candidate
   v2 manifest SHA and three actual local payload sizes/SHA values did match.
   The lead researcher reports a fresh current check already succeeded and will
   preserve the older receipt as v1 history, then run/save the mandatory fresh
   check separately after the complete review gate and before staging. This
   final retained current receipt is a required pending publication action.

Revised helper SHA-256 actually tested:
`90ccde6a04afcec7cba038072e21098ea80a43b7d4ddbbb1893098a6ec9f819e`.

Additional in-memory checks: altered tracker headers abort before append; altered
readback aborts without producing a verified receipt; a valid publication appends
once and a second serial invocation reconciles the same exact row without another
append. These checks used fabricated rows, never other researchers' data.

## Protocol correspondence and remaining operational limits

- Numeric sheet ID 1254632077 is resolved afresh from spreadsheet metadata to a
  uniquely matching tab. Quoted/escaped tab titles are used for both reads and
  append, avoiding the first-tab convenience-command failure. The four actual
  header positions are checked before writing. Current gws schemas support the
  exact resource command, structured JSON, RAW, INSERT_ROWS, response inclusion,
  and unformatted readback used by the helper.
- The tracker receipt must be the top-level JSON summary saved from this
  manifest's successful repository-tool `inspect`, after publication, at
  `receipts/zenodo_published_inspect.json`. A raw Zenodo deposition object has a
  different schema. Current tool summaries expose `environment`, `title`,
  `files` with name/size/SHA-256, and, for confirmed publication, `state`, `id`,
  `doi`, `doi_url`, `record_url`, and separate DOI-resolution status. Draft
  summaries say `ready_to_publish`; a reserved DOI is therefore rejected.
- The repository tool verifies the manifest's intended metadata, exact file set,
  sizes and MD5 values remotely before returning publication success. It reads
  back `submitted` after publish, does not automatically POST publish twice,
  and uses the same saved deposit ID for ambiguous-result reconciliation. DOI
  resolution is separate and cannot justify another deposit. The tool's local
  state is keyed by the absolute manifest path and environment; keep that path
  stable and preserve its state. The actual expected 24-character-hash production
  state file was absent at this audit. Absence of local state alone is not a
  search of the remote account, so reconcile any ambiguous earlier creation
  before restaging if one occurs.
- The current helper reconciles serial retries against DOI, title or record ID
  and refuses conflicting/multiple rows. Its DOI substring check can conservatively
  match a longer record ID having the same prefix; that produces a stop, not an
  extra append. If this happens, inspect only the conflicting identity and do not
  append to bypass the guard.
- Read-before-append is not an atomic cross-process uniqueness guarantee. Run one
  instance for this project; after a timeout/ambiguous append, reconcile the
  target tab rather than launching simultaneous retries. A future reusable helper
  could add a project-local process lock/pending-attempt journal. This is not a
  blocker for the lead's single sequential, inspected workflow.

No unresolved blocking defect was found in the revised helper under that workflow.
This verdict does not establish the mathematical review gate, actual Zenodo
publication, DOI assignment, or successful live tracker readback; those actions
are still pending and must supply their own nonsecret receipts.
