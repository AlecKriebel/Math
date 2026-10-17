# Draft PR eligibility checkpoint: #1200–#1300

The requested ascending range contains 101 open draft PRs and 103 distinct
referenced problem IDs. Every corresponding `QUEUE.md` Status cell is exactly
`queued`, both at the recorded PR head commit and on remote `main` at
`4477f00e0e27b185751b74f3ed7340ea3eccea0c`.

The user's required status is exactly `claimed_solved`. Accordingly, all 101
drafts are skipped at the eligibility gate. There is no mathematical acceptance
or rejection in this checkpoint. No proof audits, repairs, priority audits,
papers, PR comments or state changes, merges, Zenodo deposits, or spreadsheet
appends were performed. Queue statuses were not changed or inferred from titles.

## Evidence

- `pr_metadata_initial.json`: GitHub GraphQL metadata for every requested PR;
  no PR descriptions or proof content were requested.
- `eligibility/prNUMBER.json`: exact target ID(s), queue status, immutable head
  commit and queue blob identifiers, SHA-256 digest, and matching queue rows.
- `ELIGIBILITY_SUMMARY.json`: complete numeric coverage and status counts.
- `check_eligibility.py`: read-only reproduction using the saved PR metadata
  and GitHub's Contents API. A rerun checks those pinned PR commits against a
  newly captured remote-main commit and overwrites the generated receipts.
- `reviews/independent_eligibility/`: independent gate audit, separately obtained
  metadata and evidence, and comparison with the root inventory.
- `RESEARCH_LOG.md`: timestamps, decisions, completion estimates, and operational
  limitations.

PRs #1210 and #1214 each identify two targets, all of which were checked.
PR #1297's numeric target is identified in its branch name. All 103 target IDs
are distinct. Recorded status counts concern target rows; skip counts concern
PRs.

This is a finite snapshot, not a scheduled monitor. A future queue status change
requires a new eligibility check. The persistent goal is complete only after
the independent review and main-branch checkpoint have been verified.
