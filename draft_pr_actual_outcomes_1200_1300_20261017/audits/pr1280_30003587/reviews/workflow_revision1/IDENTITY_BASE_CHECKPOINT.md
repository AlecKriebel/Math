# Identity and base proposal checkpoint

Timestamp: 2026-10-18T03:21:33.649348+00:00

Completion estimate: **100% of the assigned source-only proposal and targeted validation**. Deployment, full workflow regressions, and sealing remain for root after its explicit go-ahead; this checkpoint grants no real publication clearance.

## Proposed source changes

- `proposed/program/audits/pr1280_30003587/publication/append_tracker.py`: bounded numeric problem identifier and canonical PR URL; bounded `PR1280`, `PR 1280`, and `#1280` markers; existing OWR aliases; exact known DOI and DOI URL tokens inside prose in any cell. Token continuation prefixes/suffixes are rejected; terminal sentence punctuation is accepted. With no known publication DOI, unrelated DOI rows remain eligible.
- `proposed/program/audits/pr1280_30003587/publication/update_pr_publication.py`: query and require `baseRefName == main` centrally; repeat the base check explicitly at initial branch processing, before branch push, and before/after body synchronization so direct test stubs cannot bypass it. No non-base updater changes.
- `proposed/program/publication_coordinators/pr1280.py`: request `baseRefName` and require main during live preflight before tracker or deposit mutations.
- `proposed/program/publication_coordinators/verify_pr1280_merge.py`: request `baseRefName` and require main before fetching/updating refs or accepting a merge. Tracker receipt vocabulary includes explicit PR markers.
- `proposed/program/audits/pr1280_30003587/publication/workflow_regression.py`: expand all-four-cell/all-three-action-time identity matrix, related postmerge duplicate/near-collision cases, central/explicit updater base cases, preflight and postmerge base cases, and query-field checks. Change `REPORT_ROOT` to `reviews/workflow_revision1`. Delete each previous identity case before creating the next; retain the final case through exact-row recovery and then remove it. Delete each coordinator fixture in `finally`; retain the baseline fixture needed by later controls.

## Checkable evidence

- `_local/IDENTITY_BASE_TARGETED_RECEIPT.json`: **708 identity cases + 2 preflight base rejections per mode**, exact-row read-only recovery, identical normal / `-O` / `-OO` results. This includes known DOI prose positives, all requested markers, numeric/PR/DOI near-collision negatives, and unknown-DOI preflight exceptions.
- `_local/BASE_PHASE_TARGETED_RECEIPT.json`: **12 base rejections + 3 main-base positive controls per mode**, identical normal / `-O` / `-OO` results. Direct `pr` stubs exercise explicit phase guards; no service or Git mutations are permitted by these fixtures.
- `_local/base_phase_targeted_checks.py`: small reproducible check source used by the second receipt.
- All five proposed Python files compile. All own temporary fixture directories were removed.

## Exact remaining gap

The complete workflow suite has not run in this task because root requested source-only work and lightweight serial checks while its other run is disk-constrained. The complete suite already contains the added controls for later execution. No actual helper, sealed family, publication output, repository state, remote, branch, or external service was modified. No other shard agent was contacted. No deployment or seal was created.

Historical checkpoint clarification, 2026-10-18T03:23:59Z: the source-only result above preceded the root's deliberate ambiguous-hash policy. The final deployed predicate requires an explicit PR marker or repository PR URL; standalone `#1280` and prose mathematical `#1280` are near-collision negatives. The final complete actual deployed three-mode replay supersedes these preliminary targeted results as release-workflow evidence.
