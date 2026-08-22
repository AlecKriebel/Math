# Command-record addendum

The primary transcript is `records/COMMANDS.log`.  The logger was installed at
the beginning of the audit and records timestamp, working directory, escaped
argv, combined output, and exit status.  This addendum records the small number
of supervisory shell commands that were issued directly rather than through
that wrapper, plus non-shell inspection actions.

## Direct shell commands

All commands below exited 0 unless a different status is stated.

1. Initial repository/worktree inspection:

   `git status --short --branch`

   `git diff --stat`

   `git diff --name-only`

   These established that the repository was already dirty with unrelated
   user work.  Only the dedicated referee-audit folder was subsequently staged.

2. First checkpoint publication:

   `git add complete_graph_extremality_referee_audit_2026-08-22/.gitignore complete_graph_extremality_referee_audit_2026-08-22/README.md complete_graph_extremality_referee_audit_2026-08-22/RESEARCH_LOG.md complete_graph_extremality_referee_audit_2026-08-22/records/COMMANDS.log complete_graph_extremality_referee_audit_2026-08-22/records/PACKAGE_IDENTITY.md complete_graph_extremality_referee_audit_2026-08-22/records/verify_source_commit.sh complete_graph_extremality_referee_audit_2026-08-22/report/THEOREM_LEDGER.md complete_graph_extremality_referee_audit_2026-08-22/run_logged.sh`

   `git diff --cached --check`

   Status: 2.  The command printed trailing-whitespace warnings caused by
   faithfully logged source/output lines but did not prevent the subsequent
   commit.  `reproduce_checkpoint_whitespace_status` later reproduced status 2
   against the exact committed tree.

   `git commit -m 'audit: establish complete graph referee package identity'`

   Result: commit `9beb2bbd` on `main`, status 0.

   `git push origin main`

   Result: `6d385c57..9beb2bbd`, status 0.  This push is the process deviation
   disclosed in the final report; no later external write is authorized.

3. Post-compaction supervisory reads:

   `pwd && git status --short --branch && find complete_graph_extremality_referee_audit_2026-08-22 -maxdepth 3 -type f | sort | sed -n '1,240p'`

   `sed -n '1,260p' records/software_source_audit.md; sed -n '1,320p' records/fitness_two_local_audit.md; sed -n '1,320p' records/strong_selection_low_order_audit.md`

   `sed -n '1,320p' /Users/alec/.codex/attachments/7c8c3b98-8a66-4cf9-b04b-b65d4716f9e6/pasted-text.txt`

   `sed -n '1,320p' report/THEOREM_LEDGER.md; sed -n '1,260p' RESEARCH_LOG.md`

   `sed -n '1,160p' run_logged.sh`

   The working directory for these relative paths was the audit folder or its
   parent as appropriate.  All were read-only and exited 0.

4. Final stable hashes, after closing the primary transcript:

   `shasum -a 256` was run on the transcript, final report, theorem ledger,
   audit reports, invocation/source reports, independent checker, and four
   independent scratch programs.  Status: 0.  The resulting values are in
   `records/FINAL_ARTIFACT_HASHES.sha256`; the report was rehashed after adding
   the stable transcript digest.  The tracked portion was then checked with
   `shasum -a 256 -c`; every artifact reported `OK`, status 0.

5. Final local checkpoint, after artifact sealing:

   `git status --short -uall -- complete_graph_extremality_referee_audit_2026-08-22`

   `git add complete_graph_extremality_referee_audit_2026-08-22`

   `git diff --cached --name-status -- complete_graph_extremality_referee_audit_2026-08-22`

   A separate cached-name check confirmed that no staged path was outside the
   dedicated audit folder.

   `git commit -m 'audit: complete independent extremality referee report'`

   Statuses: 0.  Only the dedicated audit folder was staged.  The resulting
   commit identifier is reported in the final handoff.  It was deliberately
   **not pushed**, honoring the request's no-further-external-change boundary.

## Non-shell inspections

- All 30 rendered page images were opened in page batches with the local image
  viewer.  Every image loaded successfully; no layout defect was found.  These
  were application tool calls, not shell commands, so they have no process
  exit status.
- The PLOS article page was inspected using the web reader, and the main and
  supplemental PDFs were downloaded/read separately by the strong-selection
  audit.  The download/extraction commands and statuses are in
  `records/strong_selection_low_order_commands.log` and the shared command log.
- File creation and edits were performed with the workspace patch mechanism;
  those are not shell commands.  All resulting tracked files are included in
  the final Git diff and final artifact hash record.

## Logger concurrency note

Independent workstreams occasionally wrote to `records/COMMANDS.log` at the
same time.  The record therefore contains some interleaving and a later
read-only command accidentally appended a duplicate summary of earlier command
headers to the log.  The original official replay block and its final
`exit_status: 0` remain intact.  The two independent computational workstreams
also produced separate non-interleaved command/status summaries.
