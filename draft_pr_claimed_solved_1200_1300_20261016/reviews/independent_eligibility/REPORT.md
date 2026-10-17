# Independent eligibility audit: PRs #1200–#1300

Completed 2026-10-16 20:53 PDT (2026-10-17 03:53 UTC). Eligibility-gate completion: **100%**.

**No PR is eligible.** All 101 numbers are existing open draft PRs, resolving to 103 distinct primary problem IDs. Every target's exact `Status` cell is `queued`, at both its immutable PR head and immutable remote `main`. Therefore every PR must be skipped under the user's exact `claimed_solved` gate. No unresolved eligibility concern remains at the recorded snapshots.

The independently captured remote main commit is `4477f00e0e27b185751b74f3ed7340ea3eccea0c`; its QUEUE blob is `d2ed87c338c2904e234e484e5775c93cfca1318c`. The 101 independently retrieved head QUEUE receipts contain three blobs:

| Head QUEUE blob | PR count | All mapped target statuses |
| --- | ---: | --- |
| `bb8320cf1c1019f64e9dae30b1f83cd334225bde` | 80 | `queued` |
| `ef2f22fcbe3beced4fef7357d14db73131ff3068` | 11 | `queued` |
| `c7bd623b3c2ba3bc66c70ec18b5abe8faa795dec` | 10 | `queued` |

## Adversarial checks

- GraphQL requested every PR number from 1200 through 1300 exactly once, with number/title/state/draft/head branch/head commit metadata and no PR body. Every response is present, open and draft.
- Target mapping independently uses numeric title/branch tokens matched to exact primary `ID / code` identifiers. All 103 targets are unique. PR #1210 has targets `5000002` and `5000003`; #1214 has `30006433` and `30006435`. PR #1297's title has no numeric target; its branch identifies `30002198`.
- The only excluded tokens of four to eight digits are the branch date `20261011` and the secondary `EP1110` label for PR #1278, whose primary problem is `2497`. No other candidate identifier was omitted.
- GitHub Contents API reads use immutable commit SHAs at `unsolved_math_prioritization/QUEUE.md`. Every decoded payload's byte count and Git blob SHA-1 are verified; content SHA-256 is recorded. Each PR has a recorded immutable head-to-QUEUE-blob link.
- The actual header has twelve columns. `Status` is the eighth column (zero-based index 7); `ID / code` is the second (index 1). Eligibility compares the entire trimmed raw status cell to `claimed_solved`, with no substring or case matching.
- A second, separately implemented Markdown parser counts escape parity before each pipe. For all four distinct blobs, all 103 target rows have exactly twelve columns and an eighth-column value of `queued`. Thus escaped-pipe or column-shift ambiguity does not affect the result.
- All 101 parent per-PR receipts were compared only after independent derivation and structure verification. Metadata, target IDs, main/head commit and blob linkage, exact statuses and skip decisions agree without discrepancy.
- A final GraphQL read at 2026-10-16 20:53:22 PDT confirmed that remote main and all 101 selected PR metadata records were unchanged from the independent capture.

## Receipts and scope

`metadata_receipt.json` preserves the exact metadata query and capture. `independent_eligibility.json` records all 101 mappings, exact main/head statuses, commit/blob receipts and coverage counts. `structure_verification.json` records all 103 target rows for each unique blob as ID/status/column-count evidence. `parent_comparison.json` records the independent comparison; `final_metadata_stability.json` records the final unchanged-state check. The accompanying Python files reproduce the read-only checks.

This review read no PR bodies, proof files, manuscripts or mathematical claims and made no decision about mathematical validity. It did not modify, comment on, close, merge or publish any PR or contact any individual. All local writes remain in this audit directory; no branch/index mutation or commit was made. These are point-in-time eligibility findings; future queue or PR changes require a fresh gate check.
