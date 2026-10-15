# Independent queue operations protocol

Sealed before reading the producer helper, harness, results, or final disposition.
Initial checkpoint: 2026-10-12 21:32 UTC. Review completion estimate: 10%.

## Scope and hypothesis

The claim to test is that the implementation can safely classify PR 445's one selected queue row from `claimed_solved` to `already_solved`, leaving the original mathematical package and all other queue bytes untouched. Acceptance here concerns operations only. Mathematical validity, priority, authorship, publication readiness, and the gate's substantive decision are external inputs, not deductions in this review.

Frozen identity: repository `AlecKriebel/Math`; PR 445; OPEN; draft; base `main`; branch `research/diffraction-dynamical-30002737`; head `3242c84e06db7e99012c7fe581adde5c3f89fc89`; problem `30002737`; selected row status `claimed_solved`, turns `1/5`, empty DOI.

Expected original-source receipt SHA-256: `31ccb9e3e153117812391ca028e2ea458d30eb6ac44699ec575f7a0e07292913`.

No review command may mutate a live ref, read mathematical bodies after branch classification, change main or another branch, or contact anyone. Own public writes are confined to this review directory. Private fixtures must be under the separately assigned ignored fixture directory. No checkout, index, staging, reset, commit, or push is performed by this reviewer.

## Preconditions and evidence binding

1. Parse JSON with duplicate-key rejection. Reject nonobjects, missing mandatory fields, unknown type coercions, and invalid typed booleans (especially integer `1`, string `"true"`, and null).
2. Require exact repository, PR, problem, source/gate/caller-pin identities. Caller SHA pins must be supplied independently of helper-generated artifacts; a self-reported hash is not independent authentication.
3. Require fixed old and target row status, `1/5` turns, and blank DOI. Reject duplicate selected rows and mismatched row identity.
4. Require regular case-local files with path-component containment, including symlink/hardlink concerns where relevant; reject escapes, directories, missing files, and references to unchecked inputs.
5. Bind the complete original-source receipt bytes to the required digest. Confirm receipt format and all 12 original leaf identities, paths, modes, and object types. Never replace a failed prepare record.
6. Bind gate bytes to their caller-provided external digest. Check gate exact decision and operational authorization without re-evaluating mathematics.
7. Require original remote BODY reads/checks of all 12 leaves before the PATCH operation. Mere leaf SHA or tree checks do not substitute for these preclassification checks.
8. Verify PR metadata and branch-ref metadata independently enough to identify a race or changed head. Reject unexpected type or head and protect the exact branch path.

## Queue-only byte change

9. Discover queue column positions from the actual header; do not assume positional status/turns/DOI fields.
10. Preserve source bytes outside the selected row's status cell, including whitespace, delimiters, newline style/final newline, column order, header, comments, other cells, and every other row.
11. Require exact single-cell old bytes `claimed_solved` and new bytes `already_solved`; reject ambiguous headers, duplicate column names, malformed row widths, duplicate selected row, or unexpected status.
12. Independently compute the expected queue bytes and compare them with the produced blob. Audit binary/encoding and delimiter failure modes as applicable to the observed queue format.

## Scalable tree proof and write cardinality

13. A recursive whole-tree response with `truncated: true` is insufficient and must fail closed. The actual failed recursive prepare must remain in the audit record.
14. Use nonrecursive trees along each queue-path ancestor. Check `truncated` strictly false, tree shapes, names, modes, types, and SHAs.
15. Prove every sibling entry unchanged at every queue ancestor and all 12 original leaf identities unchanged. A local diff assertion alone is insufficient.
16. Require the created tree's only effective difference to be the expected queue blob. Reject modified modes, types, extra entries, omitted entries, and unrelated changes.
17. Exactly one new blob POST, one tree POST, one commit POST, and one nonforce branch PATCH are permitted on a successful write run. The commit must have the frozen head as its sole parent and the verified tree as its tree.
18. Reject a successful-looking but inconsistent POST response, including identity/content/parent mismatches, before advancing to the next mutation.

## Race and uncertain outcomes

19. Perform a fresh branch-head check immediately before PATCH. A `force: false` PATCH is a nonforce ref update; it is not an atomic compare-and-swap. Do not claim it excludes every race after the fresh read.
20. Changed head at any checked boundary halts writes. Preserve raw evidence and explain whether existing unreachable objects could remain.
21. An uncertain POST outcome halts the write protocol without retrying or proceeding to later writes. Preserve receipts sufficient for the uncertainty statement.
22. An uncertain PATCH outcome allows only once-only read-only ref/queue reconciliation. Never resend the PATCH. Classify applied, not applied, or unresolved from verifiable observations, not transport success alone.
23. No retries hidden in wrappers or transport defaults may violate the one-mutation constraints. Error and interruption handling must retain original raw outcomes.

## Postclassification boundary and receipts

24. After the branch is classified, read only essential administrative ref, queue, commit/tree, diff metadata, and receipt data. Do not read mathematical source or gate bodies after classification.
25. Verify the final branch/ref and queue bytes, commit ancestry, exact diff metadata, and unchanged original leaf IDs within that boundary.
26. Prevent close/ready/merge/comment actions, main or unrelated branch writes, paper creation, Zenodo/GWS calls, or ancillary publication actions.
27. Preserve immutable preparation and apply evidence separately, with timestamps, exact endpoint/method arguments, raw responses/errors, and local file hashes. A reported success must identify strongest verified facts and residual GitHub/caller-pin trust limits.

## Planned independent falsifications

Exercise a normal fixture and meaningful failures: duplicated JSON key, bool-as-int, path escape/symlink, receipt or external pin mismatch, wrong PR identity, reordered queue columns, duplicate row, byte preservation, truncated tree, sibling tampering, changed original leaf, wrong commit parent, pre-PATCH head drift, uncertain each POST stage, and uncertain PATCH reconciliation with applied/not-applied/unresolved results. Prefer independent expected-byte/tree logic to reusing helper validation. Harness execution must occur on copied files under the reviewer fixture directory, never in the producer's sealed folder.

Acceptance requires passing operational checks with no unresolved blocking defect. A nonblocking limit must explicitly identify the trusted external input or GitHub semantic dependency. A count of test cases alone is not evidence of coverage.
