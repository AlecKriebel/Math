# Coordinator's private exact-current replay

All commands below read the frozen review/current/families and Git/raw-cache inputs. Generated writes go into a new coordinator-owned private directory under this audit's ignored tmp area; never use the frozen review as the output directory after closure. Use /usr/bin/python3 with SymPy1.14.0. Exact byte input limits, output comparisons and allowed timestamp/private-path normalization are implemented in replay.py. No network/source retrieval or shared queue generator is required.

From /Users/alec/Documents/Math, choose a fresh private directory, for example the coordinator's own `draft_pr_publication_program_20260930/audits/pr35_2744/tmp/root_current_whole_replay`, then execute:

```
/usr/bin/python3 draft_pr_publication_program_20260930/audits/pr35_2744/current_whole_adversary/verify_closed.py

PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 draft_pr_publication_program_20260930/audits/pr35_2744/current_whole_adversary/replay.py \
  --repo /Users/alec/Documents/Math \
  --audit /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr35_2744 \
  --output-dir /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr35_2744/tmp/root_current_whole_replay/outer \
  --work /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr35_2744/tmp/root_current_whole_replay/outer/tmp/replay_repo

PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 draft_pr_publication_program_20260930/audits/pr35_2744/current_whole_adversary/audit_controls.py \
  --repo /Users/alec/Documents/Math \
  --audit /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr35_2744 \
  --output-dir /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr35_2744/tmp/root_current_whole_replay/new

/usr/bin/python3 draft_pr_publication_program_20260930/audits/pr35_2744/current_whole_adversary/verify_closed.py
```

Expected: closed review verification; nine outer runs plus three explicit originals and three current programs, allPASS with unchanged42+115 bindings;329 bookkeeping/control checks,33 independent scientific diagnostics, six actual scientific corruptions and four actually executed false-prose runs; final closed verification unchanged. The21 program is executed twice because the submitted copy is an identical historical artifact. Full original/current21/21/121 result files byte-match. Every outer written JSON result is compared in full, permitting only recorded UTC/private path changes where nondeterministic. The programs replay24 earlier actual mutants in addition to the six new ones. Parser-operation counts are not distinct-file/theorem counts. Numeric results do not certify arbitrary prose or the universal assertion.

The live selected35 row must still be queued0/5 before acceptance; all unrelated rows may legitimately have changed. This is explicitly a preintegration replay. After acceptance, that live-state precondition is intentionally no longer true; preserve these dated receipts rather than relabel a postintegration run as this earlier review. The mathematical/current bindings remain independently checkable with verify_closed. Imported third-party PDFs remain ignored source inputs with exact receipts; do not substitute alternative extracted text silently. Own and historical failures/corrections remain preserved.
