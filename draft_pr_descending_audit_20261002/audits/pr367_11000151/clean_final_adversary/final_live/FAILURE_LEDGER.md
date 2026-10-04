# Preparation failure ledger

- Initial small preparation writes and later apply-patch/direct Python writes encountered Errno28/ENOSPC despite reported free disk space. Only this agent's ignored regenerable original execution copies were removed. All127 original public files, original seals and complete compressed streams remained intact. A later tiny private write probe and direct preparation writes succeeded. No live acceptance execution occurred.
- A read of a guessed preprint_review_02/FINAL_REVIEW.json path failed because that name did not exist. The actual completed REVIEW_STATUS.json and FINAL_SEAL.json were subsequently read in full.
- A schema inspection initially assumed a commands field in the original reproduction receipt and raised KeyError. The actual field is all_complete_captures; the gate handles that original schema and the family commands schema.
- The first prepared gate patch failed to open its own file for writing. Its previous28899-byte version remained intact and syntax-valid; the patch was later applied successfully. No candidate or original sealed artifact changed.

These are preparation access errors, not mathematical failures or acceptance results. Any live gate exception retains its entire traceback, checks and all completed stdout/stderr captures in receipts/FAILURE.json.

- 2026-10-03T16:23:56.053302+00:00: Exact-live attempt1 stopped after144 successful captured read/replay commands with a checker KeyError on AUTHOR_REPLAY.json. The106 nested records require resolution against each manifest parent. All failed captures, receipts, complete traceback and all four sealed checker sources are archived under failed_attempt_01, including every private compressed API/Git stream. No acceptance was credited. Only the additive checker path resolution and failed-output validator were repaired.
