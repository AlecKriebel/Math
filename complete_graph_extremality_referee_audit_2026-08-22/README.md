# Independent referee audit: complete-graph extremality

This directory contains an independent audit of the delivered referee package
`paper_i_complete_graph_extremality_referee_package_2026-08-22`.

The delivered package is treated solely as material to be checked. All
execution is performed on the disposable copy under `work/package`; the
original delivery is not modified.

## Layout

- `work/package/`: disposable byte-for-byte copy of the delivery.
- `records/`: research log, command transcript, environment records, and
  independent calculations.
- `report/`: theorem ledger, coverage tables, findings, and final report.

## Outcome

The final verdict is **valid after minor corrections**.  No mathematical
defect was found.  The required correction is to harden the replay against
optimized Python, which currently erases its load-bearing bare assertions while
still allowing a final PASS and exit status 0.

Start with:

- `report/REFEREE_REPORT.md` for the complete report and verdict;
- `report/THEOREM_LEDGER.md` for exact scopes and theorem statuses;
- `records/COMMANDS.log` for the full official transcript;
- `records/independent_crosschecks.py` for the standalone exact checker; and
- `records/adversarial_falsification.md` for the final hostile review.
