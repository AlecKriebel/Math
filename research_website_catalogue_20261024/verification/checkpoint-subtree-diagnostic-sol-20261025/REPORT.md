# Checkpoint subtree failure: rename presentation mismatch

The line-67 guard failed because its two Git comparisons used different
rename-detection defaults. The recovered existing tree pair reproduces the
reported failure exactly: **71 scoped names versus 72 full-tree names**.
The composed tree correctly preserves all 158 sibling root entries. This is
a comparison-format mismatch, not evidence that a sibling tree changed.

The minimal proposal adds explicit `--no-renames` to both changed-path
enumerations, at current helper lines 44 and 66. The complete original,
proposed source and two-line patch are retained here for root review. The
proposal has not been installed or executed; root owns the fix and push.

## Exact objects and path

| Role | Existing Git object |
| --- | --- |
| Last successful checkpoint / failed-run parent | ebd3c1c3040634fe0cff28765f86ed4b84dad488 |
| Recovered programme-only isolated root | af21da6d6b012b7836b29b3cf72e36105317f093 |
| Recovered composed full root | 2702d5aeb90a96bd003daff7a77ae8efa7e6e83a |
| Shared programme subtree in those two roots | 85b406cd0811ddfe73e5d080d3173102e130bc30 |

The two recovered roots were written at 14:54:03 UTC. The isolated tree has
exactly one entry, the programme. Replacing only that entry in the parent
root produces the recovered 159-entry full root exactly, including every
sibling mode, type, object ID and name. These are existing objects; no index,
tree object or commit was created for this diagnosis.

The sole missing name in the scoped comparison is:

`research_website_catalogue_20261024/verification/local-ambient-block-modulus-stage-sol-20261025/body_contract.py`

Git's scoped porcelain `diff` identifies an exact rename from that path to:

`research_website_catalogue_20261024/verification/local-ambient-block-modulus-stage-sol-20261025/history/body_contract.initial.py`

The rename status is `R100`; both entries use blob
`d51b3f815ed794f683e6c96118ba245aaacef502`. The original blob is retained only
in this diagnostic namespace. `--name-only` reports the rename destination,
whereas the plumbing `diff-tree` invocation reports the deletion and addition
as two changed paths. The two lists therefore differ by the old source path.
The raw name-status, NUL-delimited raw records and complete path lists are
preserved with command arguments and hashes in DIFF_REPRODUCTION.json and
its paired stdout/stderr files.

The helper's finally block removed its temporary index, as root confirmed.
Thus its cached comparison is reproduced by comparing the parent to its
existing written isolated tree, scoped to the programme. This reads precisely
the same staged tree content without recreating the index. The failure
session did not log its tree ID; FAILURE_REPORTED.json distinguishes root's
reported exception and cleanup from the independently recovered object
evidence, rather than inventing a missing original stdout transcript.

## Correction and bounded checks

Adding `--no-renames` makes both comparisons return the identical complete
72-path list, SHA256
`e401deff279879e4db230ef7bee75fb3f7d4d514f901072fde4176034168e8ca`.
All paths lie inside the programme. This retains deletion and addition names
explicitly and preserves the existing scope, root-composition and shared-
checkout guards.

The explicit flags also give identical 72-path results with `diff.renames`
forced both true and false. This removes reliance on user configuration or
different porcelain/plumbing defaults. The previous successful checkpoint's
existing isolated/composed trees were checked against its previous parent:
the original default comparisons both return **1325** names, explaining why
that checkpoint passed. CONTROLS.json is authoritative; a transient console
label in the control-generation call printed the last 72-path control count
under a prior-success label, while the saved prior-success evidence and this
report correctly retain 1325.

No helper rerun, fetch, add, read-tree, write-tree, mktree, commit-tree, push,
checkout, branch update or temporary-index reconstruction was performed.
All subsequent Git calls used `GIT_OPTIONAL_LOCKS=0`. One initial broad status
read preceded that setting; the actual index hash was then verified equal to
the original successful receipt, and remained so through final custody.
No private or production index was edited. The proposed change consists only
of two explicit Git options; it does not relax the failing equality check.

## Custody and handoff

The original helper SHA256 is
`dced5f659d47477cf4761e1696ce7d74ff9202de692f3a333303b76f72ac723a`.
The shared index remains
`349546fac30fa70129075b66a9d250a949e7c479726fbb046fdc73c65b9e87d7`;
local HEAD remains `a4ce3c37dad209339e490d18dcced6c48cf912d2`, branch main,
and origin/main remains the successful ebd3c1 checkpoint. Original push and
dry-run receipts, the helper, local refs, index and row103 final seal are
bound in CUSTODY.json. Every created evidence/proposal file is under this
new namespace. The original helper, main, shared index, unrelated work and
all earlier sealed packets are unchanged. Diagnosis completion estimate100%;
actual correction/publication remains root-owned and the overall programme
continues.
