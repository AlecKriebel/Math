# Research log

## 2026-10-21T00:41Z — Initialization checkpoint — estimated completion 0%

- Created the explicitly requested persistent goal and dedicated program folder.
- Confirmed repository AlecKriebel/Math, shared branch main, extensive concurrent
  tracked and untracked edits, and a local main far behind its remote tracking ref.
  Do not checkout, reset, stash, clean, or use the shared index for this effort.
- Live GitHub plugin discovery found highest existing PR #1380. This is an initial
  observation, not a fixed upper bound. Refresh at reconciliation.
- PR #9 is merged and claims the discotope exposed-point irreducibility result,
  problem 30005473. No mathematical review or publication disposition yet.
- Initial required Google Workspace CLI read failed with expired/revoked OAuth
  credentials (invalid_grant). Live duplicate checks have not been completed.
- Read root AGENTS.md, GWS Sheets and read skills, and Zenodo tool README.
  Missing gws-shared prerequisite caused generation of the CLI skill catalog.
  The generator treated --help as a generation command and wrote its default
  skills/ and docs/skills.md paths. Preserve these shared paths; no recovery
  preimage is available and no deletion or blanket staging is permitted.
- No publication, merge, closure, or spreadsheet mutation has occurred.

## 2026-10-21T00:46Z — Complete metadata inventory checkpoint — estimated completion 2%

- Exhaustive REST pagination reached an empty terminal page; independent newest-PR
  read confirmed #1380. Collected all 1,380 PRs, including all 1,372 in scope
  from #9–#1380, with no numeric gaps. In-scope states: 1,144 open, 23 closed,
  205 merged. These are inventory counts, not final classifications.
- GraphQL pagination repeatedly failed on transient 502 responses after #200;
  retained partial receipts and completed the independent REST route instead.
- Captured the live main QUEUE blob and recorded PR9 publication leads without
  treating stale tracker reports as live confirmation.
- The mandatory live GWS read remains blocked by invalid_grant; requested human
  reauthentication. Cursor remains #9 and no candidate is finally disposed.
- Started increasing-number file-list/QUEUE-patch evidence collection, and a
  fresh independent adversarial inventory-tooling review. No candidate mathematics
  or external service mutation has occurred.

## 2026-10-21T00:59:44.077274+00:00 — Live ledger restored and PR9 checkpoint — estimated completion 3%

- Restored the existing CLI Google Sheets login through its ordinary browser
  flow. Chrome displayed a blocked loopback page, but the CLI subsequently
  confirmed successful completion; live metadata and full values reads passed.
  No user reauthentication remains necessary. No tokens/codes were saved here.
- Live Math Puzzles schema is A:D: Original Problem, Solution Chat URL, DOI,
  Notes; 173 populated rows including header. Both formula and formatted values
  were read; full responses are ignored local evidence.
- PR9 is already correctly published and recorded at row11, verified using
  original alias, result/hypotheses, title, PR reference, DOI, and both scientific
  file checksums. DOI resolves HTTP200 to record23074543. Local manifest keyword
  drift is an expected later metadata edit, not a reason to republish.
- First final disposition: skip PR9 entirely as already published. Cursor #10.
- Inventory extended through #1382 (1,374 in-scope PRs); new PRs continue to be
  discovered rather than imposing a fixed cap.
- Collector incident: two 3,000-file fallbacks for PR248/254 shadowed the receipt
  destination variable and overwrote one unrelated local QA Python file with
  structural JSON. Stopped the collector; restored the exact identical HEAD,
  index and live-main source (git status clean), preserved the receipt, renamed
  the variable and added an explicit output-directory guard before resuming.
  INCIDENT_RECOVERY.json records evidence and the limitation on ruling out an
  undetected intermediate concurrent edit. No remote mutation was involved.
- Two independent tooling reviews and follow-up found and repaired inventory
  regression and Git push URL-rewrite hazards. Actual checkpoint still pending.
